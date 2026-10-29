"""Curation: choose the final prompts from the candidates and arrange them into dives of 7.

Two steps, both deterministic (fixed seeds):

  1. select - pick DIVES x PLAYER_PER_DIVE player prompts and DIVES x TEAM_PER_DIVE team prompts. Hard rules: no two
     prompts with the same duplicate key (same family and parameters except the threshold), a cap per family, a cap
     per franchise and per star, and a bounded number of star-style (non-broad) player prompts. A local search then
     swaps prompts to bring the rarity of the whole set into its target: tiers 1 and 2 together at most
     TARGET_TIER12 of all valid answers and tiers 5 and 6 together at least TARGET_TIER56.
  2. deal - split them into dives of 5 player and 2 team prompts. Rules, kept by a local search with a cost: no
     two prompts in a dive from the same family or about the same franchise or star, at least MIN_BROAD_PER_DIVE
     broad-pool player prompts, easy, medium and hard all present; and, between neighbouring dives, no shared
     franchise or star and (softly) no shared family.
     Inside a dive the order runs easy to hard, with the team prompts in slots 3 and 5.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

DIVE_SIZE = 7
RANK = {"easy": 0, "medium": 1, "hard": 2}
TEAM_SLOTS = (2, 4)  # 0-based positions of the two team prompts inside a dive
TARGET_TIER12 = 0.45  # tiers 1 and 2 together: at most this share of all valid answers
TARGET_TIER56 = 0.12  # tiers 5 and 6 together: at least this share
SEED = 2026


@dataclass(frozen=True)
class Config:
    dives: int = 72
    player_per_dive: int = 5
    team_per_dive: int = 2
    min_broad_per_dive: int = 2
    family_cap: int = 30  # most prompts from one family (broad player families)
    team_family_cap: int = 14
    tag_cap: int = 22  # most prompts about one franchise
    star_style_range: tuple[int, int] = (24, 72)  # non-broad player prompts in the whole set
    margin: float = 0.015  # aim this far inside the targets so a re-export does not land on the line
    select_steps: int = 60000
    deal_steps_per_dive: int = 3000

    @property
    def player_slots(self) -> int:
        return self.dives * self.player_per_dive

    @property
    def team_slots(self) -> int:
        return self.dives * self.team_per_dive


@dataclass
class Item:
    prompt: dict
    template: str
    n: int | None
    group: str
    broad: bool = False
    tags: frozenset = frozenset()
    dup: tuple = ()
    tier_counts: tuple = (0, 0, 0, 0, 0, 0)
    param: tuple = ()

    @property
    def difficulty(self) -> str:
        return self.prompt["difficulty"]

    @property
    def answer_type(self) -> str:
        return self.prompt["answerType"]

    @property
    def size(self) -> int:
        return len(self.prompt["answers"])

    @property
    def tier12(self) -> int:
        return self.tier_counts[0] + self.tier_counts[1]

    @property
    def tier56(self) -> int:
        return self.tier_counts[4] + self.tier_counts[5]


@dataclass
class Curated:
    items: list[Item]  # in file order: dive N is items[7N : 7N + 7]
    stats: dict = field(default_factory=dict)

    @property
    def prompts(self) -> list[dict]:
        return [i.prompt for i in self.items]

    def dive(self, number: int) -> list[Item]:
        return self.items[number * DIVE_SIZE:(number + 1) * DIVE_SIZE]


def build_items(prompts: list[dict], meta: list[dict], groups: dict[str, str]) -> list[Item]:
    by_id = {m["id"]: m for m in meta}
    items = []
    for p in prompts:
        m = by_id[p["id"]]
        counts = tuple(m["tier_counts"][str(t)] for t in range(1, 7))
        items.append(Item(
            p, m["template"], m["n"], m.get("group") or groups.get(m["template"], m["template"]), bool(m.get("broad", False)),
            frozenset(m.get("tags", ())), tuple(m["dup"]) if "dup" in m else (m["template"],), counts, tuple(m.get("param") or ()),
        ))
    return items


def totals(items: list[Item]) -> dict:
    n = sum(i.size for i in items)
    return {"answers": n, "tier12": sum(i.tier12 for i in items), "tier56": sum(i.tier56 for i in items)}


def shares(items: list[Item]) -> tuple[float, float]:
    t = totals(items)
    return t["tier12"] / t["answers"], t["tier56"] / t["answers"]


# --- step 1: select ---------------------------------------------------------------------------------------------

class _Selection:
    """The chosen items with the counters the hard rules need."""

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.chosen: list[Item] = []
        self.dups: set[tuple] = set()
        self.family: dict[str, int] = {}
        self.tag: dict[str, int] = {}
        self.star_style = 0
        self.sums = [0, 0, 0]  # answers, tier 1 and 2, tier 5 and 6
        self.diff = {d: 0 for d in RANK}

    def cap(self, item: Item) -> int:
        return self.cfg.team_family_cap if item.answer_type == "team" else self.cfg.family_cap

    def allows(self, item: Item, replacing: Item | None = None) -> bool:
        """Would the item fit if `replacing` (or nothing) were taken out first?"""
        dups, family, tag = self.dups, self.family, self.tag
        if item.dup in dups and not (replacing and replacing.dup == item.dup):
            return False
        gone = replacing.template == item.template if replacing else False
        if family.get(item.template, 0) - (1 if gone else 0) >= self.cap(item):
            return False
        for t in item.tags:
            leaving = 1 if replacing and t in replacing.tags else 0
            limit = 1 if t.startswith("s:") else self.cfg.tag_cap
            if tag.get(t, 0) - leaving >= limit:
                return False
        if item.answer_type == "player":
            now = self.star_style + (0 if item.broad else 1) - (0 if not replacing or replacing.broad else 1)
            if now > self.cfg.star_style_range[1]:
                return False
        return True

    def add(self, item: Item) -> None:
        self.chosen.append(item)
        self.dups.add(item.dup)
        self.family[item.template] = self.family.get(item.template, 0) + 1
        for t in item.tags:
            self.tag[t] = self.tag.get(t, 0) + 1
        if item.answer_type == "player" and not item.broad:
            self.star_style += 1
        self.diff[item.difficulty] += 1
        self.sums[0] += item.size
        self.sums[1] += item.tier12
        self.sums[2] += item.tier56

    def remove(self, item: Item) -> None:
        self.chosen.remove(item)
        self.dups.discard(item.dup)
        self.family[item.template] -= 1
        for t in item.tags:
            self.tag[t] -= 1
        if item.answer_type == "player" and not item.broad:
            self.star_style -= 1
        self.diff[item.difficulty] -= 1
        self.sums[0] -= item.size
        self.sums[1] -= item.tier12
        self.sums[2] -= item.tier56

    def objective(self) -> float:
        """Zero rarity penalty once both targets hold with the margin; then prefer a wider spread of families."""
        n = self.sums[0] or 1
        over12 = max(0.0, 100 * self.sums[1] / n - 100 * (TARGET_TIER12 - self.cfg.margin))
        under56 = max(0.0, 100 * (TARGET_TIER56 + self.cfg.margin) - 100 * self.sums[2] / n)
        spread = sum(c * c for c in self.family.values()) * 0.02
        size = max(0.0, n - 60000) * 0.001
        need = math.ceil(1.3 * self.cfg.dives)  # each dive needs one of each difficulty; keep some slack for the dealing
        missing = sum(max(0, need - c) for c in self.diff.values())
        return 50 * (over12 + under56) + 50 * missing + spread + size


def select(items: list[Item], cfg: Config = Config(), seed: int = SEED) -> tuple[list[Item], list[Item]]:
    """The chosen player and team prompts. Raises ValueError if the candidates cannot fill the slots."""
    rng = random.Random(seed)
    out = {}
    for kind, slots in (("player", cfg.player_slots), ("team", cfg.team_slots)):
        pool = [i for i in items if i.answer_type == kind]
        if len({i.dup for i in pool}) < slots:
            raise ValueError(f"only {len({i.dup for i in pool})} distinct {kind} prompts for {slots} slots")
        out[kind] = (pool, slots)
    sel = _Selection(cfg)
    for kind in ("team", "player"):
        pool, slots = out[kind]
        order = pool[:]
        rng.shuffle(order)
        if kind == "player":  # fill the star-style quota first, then broad prompts
            low = cfg.star_style_range[0]
            star_first = [i for i in order if not i.broad]
            broad = [i for i in order if i.broad]
            rng.shuffle(broad)
            order = star_first + broad
            for item in star_first:  # the quota first, one per question (the duplicate rule skips the rest)
                if sel.star_style >= low:
                    break
                if sel.allows(item):
                    sel.add(item)
        taken = sel.star_style if kind == "player" else 0
        for item in order:
            if taken == slots:
                break
            if item.dup not in sel.dups and sel.allows(item):
                sel.add(item)
                taken += 1
        if taken < slots:
            raise ValueError(f"the caps leave room for only {taken} of {slots} {kind} prompts")
    best = sel.objective()
    for step in range(cfg.select_steps):
        kind = "player" if rng.random() < 0.75 else "team"
        current = rng.choice([i for i in sel.chosen if i.answer_type == kind])
        candidate = rng.choice(out[kind][0])
        if candidate is current:
            continue
        if not sel.allows(candidate, replacing=current):
            continue
        if kind == "player":  # keep the star-style count and the broad count in range
            star_after = sel.star_style + (0 if candidate.broad else 1) - (0 if current.broad else 1)
            if star_after < min(cfg.star_style_range[0], sel.star_style):
                continue  # never take the star-style count below its lower bound
        sel.remove(current)
        sel.add(candidate)
        value = sel.objective()
        if value <= best:
            best = value
        else:
            sel.remove(candidate)
            sel.add(current)
    players = [i for i in sel.chosen if i.answer_type == "player"]
    teams = [i for i in sel.chosen if i.answer_type == "team"]
    return players, teams


# --- step 2: deal into dives ------------------------------------------------------------------------------------

def _dive_cost(dive: list[Item], cfg: Config) -> float:
    cost = 0.0
    seen_family: dict[str, int] = {}
    seen_tag: dict[str, int] = {}
    seen_group: dict[str, int] = {}
    broad = 0
    for i in dive:
        seen_family[i.template] = seen_family.get(i.template, 0) + 1
        seen_group[i.group] = seen_group.get(i.group, 0) + 1
        for t in i.tags:
            seen_tag[t] = seen_tag.get(t, 0) + 1
        broad += 1 if (i.broad and i.answer_type == "player") else 0
    cost += 60 * sum(c - 1 for c in seen_family.values())
    cost += 60 * sum(c - 1 for c in seen_tag.values())
    cost += 3 * sum(c - 1 for c in seen_group.values())
    cost += 80 * max(0, cfg.min_broad_per_dive - broad)
    present = {i.difficulty for i in dive}
    cost += 25 * sum(1 for d in RANK if d not in present)
    return cost


def _adjacent_cost(a: list[Item], b: list[Item]) -> float:
    tags_a = {t for i in a for t in i.tags}
    tags_b = {t for i in b for t in i.tags}
    fam_a = {i.template for i in a}
    fam_b = {i.template for i in b}
    return 40 * len(tags_a & tags_b) + 4 * len(fam_a & fam_b)


def deal(players: list[Item], teams: list[Item], cfg: Config = Config(), seed: int = SEED) -> list[list[Item]]:
    """Split the prompts into cfg.dives lists of 5 player and 2 team prompts, minimizing the cost above."""
    rng = random.Random(seed)
    p, t = players[:], teams[:]
    rng.shuffle(p)
    rng.shuffle(t)
    pp, tp = cfg.player_per_dive, cfg.team_per_dive
    dives = [p[d * pp:(d + 1) * pp] + t[d * tp:(d + 1) * tp] for d in range(cfg.dives)]
    cost = [_dive_cost(d, cfg) for d in dives]
    adj = [_adjacent_cost(dives[d], dives[d + 1]) for d in range(cfg.dives - 1)]
    steps = cfg.deal_steps_per_dive * cfg.dives
    for step in range(steps):
        a, b = rng.sample(range(cfg.dives), 2)
        if rng.random() < 0.75:
            ia, ib = rng.randrange(pp), rng.randrange(pp)
        else:
            ia, ib = pp + rng.randrange(tp), pp + rng.randrange(tp)
        pairs = sorted({x for x in (a - 1, a, b - 1, b) if 0 <= x < cfg.dives - 1})
        before = cost[a] + cost[b] + sum(adj[x] for x in pairs)
        dives[a][ia], dives[b][ib] = dives[b][ib], dives[a][ia]
        new_a, new_b = _dive_cost(dives[a], cfg), _dive_cost(dives[b], cfg)
        new_adj = {x: _adjacent_cost(dives[x], dives[x + 1]) for x in pairs}
        after = new_a + new_b + sum(new_adj.values())
        temperature = 2.0 * (1 - step / steps)
        if after <= before or rng.random() < math.exp(-(after - before) / max(temperature, 1e-9)):
            cost[a], cost[b] = new_a, new_b
            for x, v in new_adj.items():
                adj[x] = v
        else:
            dives[a][ia], dives[b][ib] = dives[b][ib], dives[a][ia]
    return dives


def order_dive(dive: list[Item]) -> list[Item]:
    """Players easy to hard, teams easy to hard, interleaved with the teams in TEAM_SLOTS."""
    key = lambda i: (RANK[i.difficulty], -i.size, i.prompt["id"])
    players = sorted((i for i in dive if i.answer_type == "player"), key=key)
    teams = sorted((i for i in dive if i.answer_type == "team"), key=key)
    out: list[Item] = []
    p, t = iter(players), iter(teams)
    for slot in range(len(players) + len(teams)):
        out.append(next(t) if slot in TEAM_SLOTS else next(p))
    return out


def curate(prompts: list[dict], meta: list[dict], groups: dict[str, str], cfg: Config = Config()) -> Curated:
    players, teams = select(build_items(prompts, meta, groups), cfg)
    dives = deal(players, teams, cfg)
    ordered = [i for d in dives for i in order_dive(d)]
    t12, t56 = shares(ordered)
    return Curated(items=ordered, stats={"tier12": t12, "tier56": t56, **totals(ordered)})


def violations(curated: Curated, cfg: Config = Config()) -> list[str]:
    """Every rule the arrangement should satisfy, as readable problems (empty if it all holds)."""
    problems = []
    items = curated.items
    if len(items) != cfg.dives * DIVE_SIZE:
        problems.append(f"{len(items)} prompts, expected {cfg.dives * DIVE_SIZE}")
    if len({i.prompt["id"] for i in items}) != len(items):
        problems.append("repeated prompt ids")
    dups = [i.dup for i in items]
    problems += [f"near-duplicates: {d}" for d in set(dups) if dups.count(d) > 1]
    for d in range(cfg.dives):
        dive = curated.dive(d)
        label = f"dive {d + 1}"
        kinds = [i.answer_type for i in dive]
        if kinds.count("player") != cfg.player_per_dive or kinds.count("team") != cfg.team_per_dive:
            problems.append(f"{label}: {kinds.count('player')} player and {kinds.count('team')} team prompts")
        if sum(1 for i in dive if i.broad and i.answer_type == "player") < cfg.min_broad_per_dive:
            problems.append(f"{label}: fewer than {cfg.min_broad_per_dive} broad-pool player prompts")
        if len({i.template for i in dive}) != len(dive):
            problems.append(f"{label}: repeats a template family")
        tags = [t for i in dive for t in i.tags]
        if len(set(tags)) != len(tags):
            problems.append(f"{label}: two prompts about the same franchise or star")
        if {i.difficulty for i in dive} != set(RANK):
            problems.append(f"{label}: lacks one of easy, medium, hard")
        if d + 1 < cfg.dives:
            shared = {t for i in dive for t in i.tags} & {t for i in curated.dive(d + 1) for t in i.tags}
            if shared:
                problems.append(f"dives {d + 1} and {d + 2} share {sorted(shared)}")
    return problems
