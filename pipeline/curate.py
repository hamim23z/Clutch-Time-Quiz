"""Curation: pick the final prompts from the candidates and arrange them into dives.

  1. Per template family keep at most MAX_PER_FAMILY thresholds, the easiest (longest list) and the hardest
     (shortest list), so a family never gives two near-duplicates. If that leaves too few prompts, further
     thresholds are added back one family at a time (`extended` in the result says whether that happened).
  2. From that pool choose PLAYER_PER_DIVE x DIVES player prompts and TEAM_PER_DIVE x DIVES team prompts, with a
     target mix of difficulties and without piling up on one stat (the 'group' of a template).
  3. Deal the prompts into DIVES dives of DIVE_SIZE: no repeated stat or template in a dive, and each dive has
     easy, medium and hard prompts where the pool allows. Within a dive the order runs from easy to hard, with
     the team prompts in slots 3 and 5.

Everything is deterministic (fixed seeds), so the same candidates give the same file.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field

DIVES = 9
DIVE_SIZE = 7
PLAYER_PER_DIVE = 5
TEAM_PER_DIVE = 2
MAX_PER_FAMILY = 2
TEAM_SLOTS = (2, 4)  # 0-based positions of the two team prompts inside a dive
RANK = {"easy": 0, "medium": 1, "hard": 2}
SEED = 2026


@dataclass
class Item:
    prompt: dict
    template: str
    n: int | None
    group: str

    @property
    def difficulty(self) -> str:
        return self.prompt["difficulty"]

    @property
    def answer_type(self) -> str:
        return self.prompt["answerType"]

    @property
    def size(self) -> int:
        return len(self.prompt["answers"])


@dataclass
class Curated:
    items: list[Item]  # in file order: dive N is items[7N : 7N + 7]
    extended: list[str] = field(default_factory=list)  # families that gave more than MAX_PER_FAMILY prompts

    @property
    def prompts(self) -> list[dict]:
        return [i.prompt for i in self.items]

    def dive(self, number: int) -> list[Item]:
        return self.items[number * DIVE_SIZE:(number + 1) * DIVE_SIZE]


def build_items(prompts: list[dict], meta: list[dict], groups: dict[str, str]) -> list[Item]:
    by_id = {m["id"]: m for m in meta}
    return [Item(p, by_id[p["id"]]["template"], by_id[p["id"]]["n"], groups.get(by_id[p["id"]]["template"], by_id[p["id"]]["template"])) for p in prompts]


def mean_points(item: Item) -> float:
    answers = item.prompt["answers"]
    return sum(a["points"] for a in answers) / len(answers)


def _spread(family: list[Item]) -> list[Item]:
    """Easiest-and-longest first, hardest-and-shortest last."""
    return sorted(family, key=lambda i: (RANK[i.difficulty], -i.size, i.prompt["id"]))


def pool_for(items: list[Item], extra_per_family: int = 0) -> list[Item]:
    """Up to MAX_PER_FAMILY + extra_per_family items per template family, spread from easy to hard."""
    families: dict[str, list[Item]] = {}
    for i in items:
        families.setdefault(i.template, []).append(i)
    pool: list[Item] = []
    for key in sorted(families):
        ordered = _spread(families[key])
        keep = MAX_PER_FAMILY + extra_per_family
        if len(ordered) <= keep:
            pool += ordered
        else:
            # the two ends first, then the ones nearest the middle
            middle = ordered[1:-1]
            middle.sort(key=lambda i: abs(ordered.index(i) - (len(ordered) - 1) / 2))
            pool += [ordered[0], ordered[-1]] + middle[: keep - 2]
    return pool


def _quotas(pool: list[Item], target: int) -> dict[str, int]:
    """How many prompts of each difficulty to take: about 20% hard and 40% medium, as far as the pool has them."""
    have = {d: sum(1 for i in pool if i.difficulty == d) for d in RANK}
    hard = min(have["hard"], round(0.2 * target))
    medium = min(have["medium"], round(0.4 * target))
    easy = min(have["easy"], target - hard - medium)
    medium = min(have["medium"], target - hard - easy)  # an easy shortfall goes to medium
    hard = min(have["hard"], target - easy - medium)
    return {"hard": hard, "medium": medium, "easy": easy}


def choose(pool: list[Item], target: int) -> list[Item] | None:
    """target prompts from the pool, or None if the pool is too small."""
    if len(pool) < target:
        return None
    chosen: list[Item] = []
    group_count: dict[str, int] = {}
    family_count: dict[str, int] = {}

    def take(item: Item) -> None:
        chosen.append(item)
        group_count[item.group] = group_count.get(item.group, 0) + 1
        family_count[item.template] = family_count.get(item.template, 0) + 1

    def best(cands: list[Item]) -> Item:
        # fewest of the same stat and family so far; then the list with the highest average points (more deep cuts)
        return min(cands, key=lambda i: (group_count.get(i.group, 0) * 2 + family_count.get(i.template, 0), -mean_points(i), i.prompt["id"]))

    quotas = _quotas(pool, target)
    for cls in ("hard", "medium", "easy"):
        for _ in range(quotas[cls]):
            cands = [i for i in pool if i.difficulty == cls and i not in chosen]
            if not cands:
                break
            take(best(cands))
    while len(chosen) < target:
        take(best([i for i in pool if i not in chosen]))
    return chosen


def select(items: list[Item]) -> tuple[list[Item], list[Item], list[str]]:
    """The chosen player and team prompts, and the families that had to give more than MAX_PER_FAMILY.

    Starts with two thresholds per family and adds one more per family at a time only while the pool is too small
    for the slots. A shortage of hard or medium prompts is not a reason to add thresholds: it is passed to the
    other difficulty levels (see `_quotas`).
    """
    want = {"player": PLAYER_PER_DIVE * DIVES, "team": TEAM_PER_DIVE * DIVES}
    out: dict[str, list[Item]] = {}
    extended: set[str] = set()
    for kind, target in want.items():
        of_kind = [i for i in items if i.answer_type == kind]
        chosen = None
        for extra in range(0, 30):
            chosen = choose(pool_for(of_kind, extra), target)
            if chosen is not None:
                break
        if chosen is None:
            raise ValueError(f"only {len(of_kind)} {kind} candidates for {target} slots")
        per_family: dict[str, int] = {}
        for i in chosen:
            per_family[i.template] = per_family.get(i.template, 0) + 1
        extended |= {k for k, c in per_family.items() if c > MAX_PER_FAMILY}
        out[kind] = chosen
    return out["player"], out["team"], sorted(extended)


# --- dives ------------------------------------------------------------------------------------------------------

def _dive_cost(dive: list[Item], mean_score: float) -> float:
    cost = 0.0
    groups: dict[str, int] = {}
    families: dict[str, int] = {}
    for i in dive:
        groups[i.group] = groups.get(i.group, 0) + 1
        families[i.template] = families.get(i.template, 0) + 1
    cost += 10 * sum(c - 1 for c in groups.values())
    cost += 25 * sum(c - 1 for c in families.values())
    present = {i.difficulty for i in dive}
    cost += 8 * ("easy" not in present) + 4 * ("medium" not in present) + 6 * ("hard" not in present)
    score = sum(RANK[i.difficulty] for i in dive)
    cost += (score - mean_score) ** 2
    return cost


def deal(players: list[Item], teams: list[Item], seed: int = SEED, restarts: int = 12, steps: int = 6000) -> list[list[Item]]:
    """Split the prompts into DIVES lists of 5 player and 2 team prompts, minimizing repeats inside a dive."""
    rng = random.Random(seed)
    mean_score = sum(RANK[i.difficulty] for i in players + teams) / DIVES
    best_dives, best_cost = None, float("inf")
    for _ in range(restarts):
        p, t = players[:], teams[:]
        rng.shuffle(p)
        rng.shuffle(t)
        dives = [p[d * PLAYER_PER_DIVE:(d + 1) * PLAYER_PER_DIVE] + t[d * TEAM_PER_DIVE:(d + 1) * TEAM_PER_DIVE] for d in range(DIVES)]
        costs = [_dive_cost(d, mean_score) for d in dives]
        for _ in range(steps):
            a, b = rng.sample(range(DIVES), 2)
            if rng.random() < 0.7:
                ia, ib = rng.randrange(PLAYER_PER_DIVE), rng.randrange(PLAYER_PER_DIVE)
            else:
                ia, ib = PLAYER_PER_DIVE + rng.randrange(TEAM_PER_DIVE), PLAYER_PER_DIVE + rng.randrange(TEAM_PER_DIVE)
            dives[a][ia], dives[b][ib] = dives[b][ib], dives[a][ia]
            new_a, new_b = _dive_cost(dives[a], mean_score), _dive_cost(dives[b], mean_score)
            if new_a + new_b <= costs[a] + costs[b]:
                costs[a], costs[b] = new_a, new_b
            else:
                dives[a][ia], dives[b][ib] = dives[b][ib], dives[a][ia]
        total = sum(costs)
        if total < best_cost:
            best_dives, best_cost = [d[:] for d in dives], total
    assert best_dives is not None
    return best_dives


def order_dive(dive: list[Item]) -> list[Item]:
    """Players easy to hard, teams easy to hard, interleaved with the teams in TEAM_SLOTS."""
    key = lambda i: (RANK[i.difficulty], -i.size, i.prompt["id"])
    players = sorted((i for i in dive if i.answer_type == "player"), key=key)
    teams = sorted((i for i in dive if i.answer_type == "team"), key=key)
    out: list[Item] = []
    p, t = iter(players), iter(teams)
    for slot in range(DIVE_SIZE):
        out.append(next(t) if slot in TEAM_SLOTS else next(p))
    return out


def curate(prompts: list[dict], meta: list[dict], groups: dict[str, str]) -> Curated:
    players, teams, extended = select(build_items(prompts, meta, groups))
    dives = deal(players, teams)
    ordered = [i for d in dives for i in order_dive(d)]
    return Curated(items=ordered, extended=extended)
