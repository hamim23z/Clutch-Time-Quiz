"""Spike: can the sportsdataverse box score releases support the Deep Cut prompts?

Loads the player box, team box and schedule files for seasons 2002-2026 (the season number is
the year the season ends, so 2002 is 2001-02) and prints real counts. It is a one-off check,
not part of the pipeline.

Download the files first (see docs/data-source-boxscores.md; the officials files are optional and only
used by the last section), then run from the repo root:

    python3 pipeline/spike/boxscore_feasibility.py data/raw/boxscores
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

FIRST, LAST = 2002, 2026  # 2027 is the season in progress and is left out so counts stay fixed
PLAYER_STATS = ["points", "rebounds", "assists", "steals", "blocks"]
SUFFIX_RE = r"\s(?:Jr\.?|Sr\.?|II|III|IV)$"
PUNCT_RE = r"['.\-]"


def load(raw: Path, prefix: str) -> pd.DataFrame:
    frames = [pd.read_parquet(raw / f"{prefix}_{y}.parquet") for y in range(FIRST, LAST + 1)]
    return pd.concat(frames, ignore_index=True)


def section(title: str) -> None:
    print(f"\n{'=' * 8} {title} {'=' * 8}")


def nba_franchise_ids(team: pd.DataFrame) -> list[int]:
    """The 30 franchises: team ids with a full history of games. All-star, Rising Stars and
    exhibition sides (Team LeBron, USA, World, ...) have a few dozen team-games at most."""
    n = team.groupby("team_id").size()
    return sorted(n[n >= 300].index)


def classify_games(sched: pd.DataFrame, nba_ids: list[int]) -> pd.DataFrame:
    """One row per final game with a `kind`:
    regular, playoffs, finals, playin, cup_final or exhibition (all-star weekend and other non-NBA sides).

    season_type alone is not enough: season_type 2 also holds All-Star weekend games and the NBA
    Cup final, and some exhibition games are even typed STD, so a game only counts if both sides are
    NBA franchises. The 2002 and 2003 Finals are not labelled FINAL in the schedule, so the Finals
    are the series between the two teams in the last playoff game of each season.
    """
    g = sched[sched["status_type_name"] == "STATUS_FINAL"].copy()
    both_nba = g.home_id.isin(nba_ids) & g.away_id.isin(nba_ids)
    kind = pd.Series("other", index=g.index)
    kind[(g.season_type == 2) & (g.type_abbreviation == "STD")] = "regular"
    kind[g.type_abbreviation == "CC"] = "cup_final"  # season_type 2, but the NBA does not count it as regular season
    kind[g.season_type == 3] = "playoffs"
    kind[g.season_type == 5] = "playin"
    kind[~both_nba | (g.type_abbreviation == "ALLSTAR")] = "exhibition"
    g["kind"] = kind
    g["regulation"] = g["status_period"] == 4
    g["periods"] = g["status_period"]
    po = g[g.kind == "playoffs"].sort_values(["game_date", "game_id"])
    last = po.groupby("season").tail(1)
    finals_pairs = {(r.season, frozenset((r.home_id, r.away_id))) for r in last.itertuples()}
    in_finals = [(r.season, frozenset((r.home_id, r.away_id))) in finals_pairs for r in g.itertuples()]
    g.loc[(g.kind == "playoffs") & pd.Series(in_finals, index=g.index), "kind"] = "finals"
    g["labelled_finals"] = g.type_abbreviation == "FINAL"
    # notes_headline only carries "Game 7" style labels from 2020, so number each series' games by date instead
    g["series"] = [frozenset((h, a)) for h, a in zip(g.home_id, g.away_id)]
    po_games = g[g.kind.isin(["playoffs", "finals"])].sort_values(["game_date", "game_id"])
    g["series_game"] = po_games.groupby(["season", "series"]).cumcount() + 1
    return g[["game_id", "season", "kind", "regulation", "periods", "labelled_finals", "game_date", "series_game", "home_id", "away_id",
              "home_display_name", "away_display_name", "notes_headline"]]


def coverage(games: pd.DataFrame, team: pd.DataFrame, player: pd.DataFrame) -> None:
    section("1. Games per season (final games only)")
    t = games.pivot_table(index="season", columns="kind", values="game_id", aggfunc="nunique", fill_value=0)
    t["in_team_box"] = team.groupby("season").game_id.nunique()
    t["in_player_box"] = player.groupby("season").game_id.nunique()
    t["total"] = games.groupby("season").game_id.nunique()
    print(t.to_string())
    print("\ntotals:", games.groupby("kind").game_id.nunique().to_dict())
    print("Game 7s (numbered by date within each series):", int((games.series_game == 7).sum()),
          "- schedule notes_headline names only", int(games.notes_headline.fillna("").str.contains("Game 7").sum()))
    real = games[games.kind.isin(["regular", "playoffs", "finals", "playin", "cup_final"])]
    no_team = real[~real.game_id.isin(team.game_id)]
    no_player = real[~real.game_id.isin(player.game_id)]
    print(f"NBA games with no team box rows: {len(no_team)}; with no player box rows: {len(no_player)} (of {len(real)})")
    print("no player box rows, by season:", no_player.groupby("season").size().to_dict())
    print("no team box rows, by season:", no_team.groupby("season").size().to_dict())
    print("examples with no player box rows:")
    for r in no_player.sort_values("game_date").head(8).itertuples():
        print(f"    {r.game_id} {str(r.game_date)[:10]} {r.away_display_name} at {r.home_display_name} ({r.kind})")
    expected = {2012: 990, 2020: 1059, 2021: 1080}
    reg = games[games.kind == "regular"].groupby("season").game_id.nunique()
    off = {int(y): int(n) for y, n in reg.items() if n != expected.get(y, 1189 if y <= 2004 else 1230)}
    print("seasons whose regular-season game count differs from the league schedule (30 teams x 82 / 2 = 1230; 1189 for 29 teams):", off)


def integrity(team: pd.DataFrame, player: pd.DataFrame) -> pd.DataFrame:
    section("2. Integrity")
    print("duplicate (game, athlete) rows:", int(player.duplicated(["game_id", "athlete_id"]).sum()))
    print("duplicate (game, team) rows:", int(team.duplicated(["game_id", "team_id"]).sum()))
    print("team rows per game:", team.groupby("game_id").size().value_counts().to_dict())
    flag = player.groupby("season").did_not_play.mean().round(3)
    nulls = player.groupby("season").points.apply(lambda s: s.isna().mean()).round(3)
    print("\ndid_not_play share vs share with no stats (the flag is unreliable in 2006-2012):")
    print(pd.DataFrame({"did_not_play": flag, "null_stats": nulls}).loc[[2002, 2005, 2006, 2009, 2012, 2013, 2020, 2026]].to_string())
    played = player[player.points.notna()]  # rule used from here on: appeared = has a points value
    print("\nplayers with stats per team-game:", played.groupby(["game_id", "team_id"]).size().describe()[["min", "50%", "max"]].to_dict())
    pts = played.groupby(["game_id", "team_id"]).points.sum().rename("player_points").reset_index()
    m = team[["game_id", "team_id", "team_score"]].merge(pts, on=["game_id", "team_id"], how="left")
    print(f"team-games: {len(m)}; no player rows: {int(m.player_points.isna().sum())}; "
          f"player points != team score: {int((m.player_points.notna() & (m.player_points != m.team_score)).sum())}")
    top = played.nlargest(3, "points")[["athlete_display_name", "game_date", "points"]]
    print("\nhighest scoring games (Kobe Bryant's 81 on 2006-01-22 is the known check):",
          [(r.athlete_display_name, str(r.game_date)[:10], int(r.points)) for r in top.itertuples()])
    return played


def universe(team: pd.DataFrame, played: pd.DataFrame, nba_ids: list[int]) -> None:
    section("3. Players and teams")
    names = played.athlete_display_name.dropna()
    print(f"distinct athletes who appeared: {played.athlete_id.nunique()}; display names: {names.nunique()}")
    var = played.groupby("athlete_id").athlete_display_name.nunique()
    print(f"stat lines with no athlete name: {int(played.athlete_display_name.isna().sum())} "
          f"(with no athlete id: {int(played.athlete_id.isna().sum())}, points total {played[played.athlete_display_name.isna()].points.sum():.0f})")
    seasons = played.groupby("athlete_id").season.nunique()
    print(f"seasons played per athlete: median {int(seasons.median())}, max {int(seasons.max())}")
    print(f"athlete ids with more than one display name over time: {int((var > 1).sum())}")
    for aid in var[var > 1].index:
        d = played[played.athlete_id == aid].groupby("athlete_display_name").season.agg(["min", "max"])
        print("   ", int(aid), "; ".join(f"{n} ({r['min']}-{r['max']})" for n, r in d.iterrows()))
    shared = played.dropna(subset=["athlete_display_name"]).groupby("athlete_display_name").athlete_id.nunique()
    print(f"display names shared by more than one athlete id: {int((shared > 1).sum())} -> {sorted(shared[shared > 1].index)}")
    odd = sorted({n for n in names.unique() if n != " ".join(n.split())})
    print("names with stray whitespace:", [repr(n) for n in odd])
    print("names with non-ASCII characters:", int(sum(any(ord(c) > 127 for c in n) for n in names.unique())))
    uniq = names.drop_duplicates()
    n_suffix = int(uniq.str.contains(SUFFIX_RE).sum())
    n_punct = int(uniq.str.contains(PUNCT_RE).sum())
    print(f"names ending in a suffix (Jr., Sr., II, III, IV): {n_suffix}; names containing an apostrophe, period or hyphen: {n_punct}")
    last = names.drop_duplicates().str.replace(r"\s+(Jr\.?|Sr\.?|II|III|IV)$", "", regex=True).str.split().str[-1]
    print(f"share of players whose last name (suffix removed) is unique: {(last.map(last.value_counts()) == 1).mean():.3f}")
    print("aliases for renamed people (for example Ron Artest): present?", bool(names.str.contains("Artest").any()))
    short = played.dropna(subset=["athlete_short_name"]).groupby("athlete_id").athlete_short_name.unique()
    multi = short[short.map(len) > 1]
    accented = sorted({n for v in short for n in v if any(ord(c) > 127 for c in n)})
    print(f"athlete ids with more than one athlete_short_name: {len(multi)}; short names with accents: {accented}")
    print("   examples:", [list(v) for v in multi.head(6)])

    nba = team[team.team_id.isin(nba_ids)]
    non_nba = sorted(set(team.team_display_name) - set(nba.team_display_name))
    print(f"\nteam ids in team box: {team.team_id.nunique()}; NBA franchises (300+ team-games): {len(nba_ids)}")
    print("non-NBA 'teams' to exclude (all-star and exhibition sides):", non_nba)
    names_by_id = nba.assign(name=nba.team_display_name.str.replace(r"\s+", " ", regex=True)).groupby("team_id").name.unique()
    renamed = {int(i): list(v) for i, v in names_by_id.items() if len(v) > 1}
    abbr = nba.groupby("team_id").team_abbreviation.unique()
    print("franchises with more than one abbreviation:", {int(i): list(v) for i, v in abbr.items() if len(v) > 1})
    print("franchises whose display name changed (same team_id):")
    for i, v in renamed.items():
        print("   ", i, v)


def finals_check(games: pd.DataFrame, team: pd.DataFrame) -> None:
    section("4. Finals and playoff series completeness")
    f = games[games.kind == "finals"]
    lab = games[games.labelled_finals]
    print(f"Finals derived as the last playoff series: {len(f)} games in {f.season.nunique()} seasons; "
          f"schedule label FINAL covers {len(lab)} games in {lab.season.nunique()} seasons (first {lab.season.min()}); "
          f"labelled games missing from the derived set: {len(set(lab.game_id) - set(f.game_id))}; "
          f"derived games from seasons the label covers but not labelled: {len(set(f[f.season >= lab.season.min()].game_id) - set(lab.game_id))}")
    wins = team[team.game_id.isin(f.game_id) & team.team_winner].merge(f[["game_id"]], on="game_id")
    champ = wins.groupby(["season", "team_display_name"]).size().rename("wins").reset_index()
    top = champ.sort_values("wins", ascending=False).drop_duplicates("season").sort_values("season")
    print(f"seasons where the Finals leader has 4 wins: {int((top.wins == 4).sum())} of {f.season.nunique()}")
    print("games per Finals:", f.groupby("season").size().to_dict())
    print("champions found:", ", ".join(f"{r.season}:{r.team_display_name}" for r in top.itertuples()))
    p = games[games.kind.isin(["playoffs", "finals"])].merge(team[team.team_winner][["game_id", "team_id"]], on="game_id")
    p["pair"] = [tuple(sorted(x)) for x in zip(p.home_id, p.away_id)]
    series = p.groupby(["season", "pair"]).team_id.apply(lambda s: s.value_counts().max()).rename("max_wins").reset_index()
    short = series[~((series.max_wins >= 4) | ((series.season == 2002) & (series.max_wins >= 3)))]
    print(f"playoff series found: {len(series)}; with a winner short of 4 wins (best-of-5 first round in 2002 allowed 3): {len(short)}")


def player_prompts(played: pd.DataFrame, games: pd.DataFrame) -> None:
    section("5. Player prompt feasibility: distinct players per template (since 2002)")
    p = played.merge(games[["game_id", "kind", "series_game"]], on="game_id")
    reg, po, fin = p[p.kind == "regular"], p[p.kind.isin(["playoffs", "finals"])], p[p.kind == "finals"]
    rows = []

    def add(label: str, df: pd.DataFrame, mask: pd.Series) -> None:
        hit = df[mask.reindex(df.index, fill_value=False)]
        rows.append((label, hit.athlete_id.nunique(), len(hit)))

    for n in (30, 35, 40, 45, 50, 55, 60, 70):
        add(f"{n}+ points, regular season", reg, reg.points >= n)
    for n in (35, 40, 45, 50):
        add(f"{n}+ points, playoffs", po, po.points >= n)
    for n in (30, 35, 40):
        add(f"{n}+ points, Finals", fin, fin.points >= n)
    add("30+ points in a Game 7", po, (po.points >= 30) & (po.series_game == 7))
    cats = lambda d: (d[PLAYER_STATS] >= 10).sum(axis=1)  # noqa: E731
    for label, df in (("regular season", reg), ("playoffs", po), ("Finals", fin)):
        add(f"triple-double, {label}", df, cats(df) >= 3)
    add("quadruple-double, any game", p, cats(p) >= 4)
    add("30+ point triple-double, any game", p, (cats(p) >= 3) & (p.points >= 30))
    for n in (20, 25):
        add(f"{n}+ rebounds, any game", p, p.rebounds >= n)
    for n in (18, 20, 22):
        add(f"{n}+ assists, any game", p, p.assists >= n)
    for n in (8, 9, 10):
        add(f"{n}+ blocks, any game", p, p.blocks >= n)
    for n in (7, 8, 9):
        add(f"{n}+ steals, any game", p, p.steals >= n)
    for n in (10, 11, 12):
        add(f"{n}+ threes made, any game", p, p.three_point_field_goals_made >= n)
    add("perfect shooting: 10+ field goals, no misses", p, (p.field_goals_attempted >= 10) & (p.field_goals_made == p.field_goals_attempted))
    out = pd.DataFrame(rows, columns=["template", "distinct_players", "games"])
    out["meets_15_minimum"] = out.distinct_players >= 15
    print(out.to_string(index=False))
    print("\nregular-season 40+ point games by season (completeness check):", reg[reg.points >= 40].groupby("season").size().to_dict())


def team_prompts(team: pd.DataFrame, games: pd.DataFrame, nba_ids: list[int]) -> None:
    section("6. Team prompt feasibility: distinct franchises per template (since 2002)")
    t = team[team.team_id.isin(nba_ids)].merge(games[["game_id", "kind", "regulation"]], on="game_id")
    reg = t[t.kind == "regular"]
    rows = []

    def add(label: str, df: pd.DataFrame, mask: pd.Series) -> None:
        hit = df[mask]
        rows.append((label, hit.team_id.nunique(), len(hit)))

    season_rec = reg.groupby(["season", "team_id"]).agg(wins=("team_winner", "sum"), games=("game_id", "size")).reset_index()
    season_rec["losses"] = season_rec.games - season_rec.wins
    for n in (55, 60, 62, 65, 67, 70):
        hit = season_rec[season_rec.wins >= n]
        rows.append((f"{n}+ regular-season wins in a season", hit.team_id.nunique(), len(hit)))
    for n in (60, 62, 65, 68, 70):
        hit = season_rec[season_rec.losses >= n]
        rows.append((f"{n}+ regular-season losses in a season", hit.team_id.nunique(), len(hit)))
    allg = t[t.kind.isin(["regular", "playoffs", "finals"])]
    for n in (130, 140, 150, 160):
        add(f"{n}+ points in a game (regular season or playoffs)", allg, allg.team_score >= n)
    for n in (130, 140, 150):
        add(f"{n}+ points in a regulation game", allg, (allg.team_score >= n) & allg.regulation)
    for n in (40, 50, 60):
        add(f"won by {n}+ points", allg, allg.team_winner & (allg.team_score - allg.opponent_team_score >= n))
    for n in (60, 65, 70):
        add(f"scored under {n} points in a game", allg, allg.team_score < n)
    for n in (22, 25, 28):
        add(f"{n}+ threes made in a game", allg, allg.three_point_field_goals_made >= n)
    # longest regular-season winning streaks
    seq = reg.sort_values(["team_id", "game_date", "game_id"]).copy()
    seq["run"] = seq.groupby("team_id").team_winner.transform(lambda s: (s != s.shift()).cumsum())
    streak = seq[seq.team_winner].groupby(["team_id", "run"]).size()
    for n in (12, 15, 18, 20):
        rows.append((f"{n}+ game winning streak (regular season, across seasons)", streak[streak >= n].reset_index().team_id.nunique(), int((streak >= n).sum())))
    f = t[t.kind == "finals"]
    champs = f[f.team_winner].groupby(["season", "team_id"]).size().reset_index().sort_values(0).drop_duplicates("season", keep="last")
    rows.append(("won the NBA title (champion of the Finals)", champs.team_id.nunique(), len(champs)))
    out = pd.DataFrame(rows, columns=["template", "distinct_franchises", "instances"])
    out["meets_5_minimum"] = out.distinct_franchises >= 5
    print(out.to_string(index=False))
    for n in (140, 150):
        g_any = allg[allg.team_score >= n].game_id.nunique()
        g_reg = allg[(allg.team_score >= n) & allg.regulation].game_id.nunique()
        print(f"distinct games (not team-games) where a team scored {n}+: {g_any}; in regulation: {g_reg}")
    top = season_rec.sort_values("wins", ascending=False).head(5)
    print("\nmost regular-season wins:", [(int(r.season), int(r.team_id), int(r.wins)) for r in top.itertuples()])
    print("regular-season games per team-season: min", int(season_rec.games.min()), "max", int(season_rec.games.max()),
          "- lockout and COVID seasons are short:", season_rec.groupby("season").games.max().loc[[2012, 2020, 2021]].to_dict())


def referees(raw: Path, games: pd.DataFrame, played: pd.DataFrame) -> None:
    section("7. Referees (espn_nba_officials release)")
    if not all((raw / f"officials_{y}.parquet").exists() for y in range(FIRST, LAST + 1)):
        print("officials_<year>.parquet files not found in", raw, "- skipped")
        return
    o = load(raw, "officials")
    print(f"rows: {len(o)}; games: {o.game_id.nunique()}; distinct official names: {o.official_full_name.nunique()}; "
          f"positions: {o.official_position.value_counts().to_dict()}")
    print("officials per game:", o.groupby("game_id").size().value_counts().sort_index().to_dict())
    print("columns:", list(o.columns), "(no official id column)")
    clash = o[o.duplicated(["game_id", "official_order"], keep=False)]
    print(f"rows sharing an official_order within a game (two names for one slot): {len(clash)} in {clash.game_id.nunique()} games, "
          f"by season: {clash.groupby('season').game_id.nunique().to_dict()}")
    names = sorted(o.official_full_name.unique())
    key = lambda n: (n.split()[-1].lower(), n.split()[0][0].lower())  # noqa: E731
    groups: dict[tuple[str, str], list[str]] = {}
    for n in names:
        groups.setdefault(key(n), []).append(n)
    print("name pairs with the same last name and first initial (variants or different people):",
          [v for v in groups.values() if len(v) > 1])
    print("names with stray whitespace:", [repr(n) for n in names if n != " ".join(n.split())])
    o = o.drop_duplicates(["game_id", "official_full_name"])

    nba = games[games.kind.isin(["regular", "playoffs", "finals", "playin", "cup_final"])].copy()
    nba["has_officials"] = nba.game_id.isin(o.game_id)
    print(f"\nNBA games with officials: {int(nba.has_officials.sum())} of {len(nba)} ({nba.has_officials.mean():.1%}); "
          f"officials rows for games not in the schedule: {len(set(o.game_id) - set(games.game_id))}")
    by = nba.groupby(["season", "kind"]).has_officials.mean().unstack().round(3)
    print("share of games with officials, seasons where any kind is below 100%:")
    print(by[(by < 1).any(axis=1)].to_string())
    gaps = nba[~nba.has_officials]
    print("games without officials by kind:", gaps.groupby("kind").size().to_dict(), "; Finals games without:",
          gaps[gaps.kind == "finals"].groupby("season").size().to_dict())

    per_ref = o.groupby("official_full_name").game_id.nunique()
    print(f"\ngames per official: median {int(per_ref.median())}, max {int(per_ref.max())}; "
          f"{int((per_ref >= 1000).sum())} worked 1000+, {int((per_ref >= 500).sum())} worked 500+, {int((per_ref <= 10).sum())} worked 10 or fewer")
    m = o.merge(games[["game_id", "kind", "season", "series_game", "periods"]], on="game_id", suffixes=("", "_g"))
    big = played[played.points >= 60].game_id.unique()
    rows = [
        ("officiated an NBA Finals game (2009-2011 are missing)", m[m.kind == "finals"]),
        ("officiated an NBA Finals game, 2012 on (complete years)", m[(m.kind == "finals") & (m.season >= 2012)]),
        ("officiated a playoff Game 7", m[m.series_game == 7]),
        ("officiated a game with a 60+ point scorer", m[m.game_id.isin(big)]),
        ("officiated a triple-overtime or longer game", m[m.periods >= 7]),
        ("officiated 1000+ games", m[m.official_full_name.isin(per_ref[per_ref >= 1000].index)]),
    ]
    out = pd.DataFrame([(label, d.official_full_name.nunique(), d.game_id.nunique()) for label, d in rows],
                       columns=["template", "distinct_officials", "games"])
    out["meets_15_minimum"] = out.distinct_officials >= 15
    print("\nreferee prompt feasibility (distinct names since 2002):")
    print(out.to_string(index=False))


def main() -> None:
    raw = Path(sys.argv[1])
    sched, team, player = load(raw, "nba_schedule"), load(raw, "team_box"), load(raw, "player_box")
    nba_ids = nba_franchise_ids(team)
    games = classify_games(sched, nba_ids)
    coverage(games, team, player)
    played = integrity(team, player)
    universe(team, played, nba_ids)
    finals_check(games, team)
    player_prompts(played, games)
    team_prompts(team, games, nba_ids)
    referees(raw, games, played)


if __name__ == "__main__":
    main()
