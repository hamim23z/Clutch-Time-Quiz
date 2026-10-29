import io
import urllib.error
import urllib.request

import pytest

import fetch


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


def test_urls_and_names_follow_the_release_layout():
    assert fetch.season_url("player", 2024).endswith("/espn_nba_player_boxscores/player_box_2024.parquet")
    assert fetch.season_url("team", 2002).endswith("/espn_nba_team_boxscores/team_box_2002.parquet")
    assert fetch.season_url("schedule", 2013).endswith("/espn_nba_schedules/nba_schedule_2013.parquet")
    assert fetch.season_url("officials", 2026).endswith("/espn_nba_officials/officials_2026.parquet")
    assert (fetch.FIRST_SEASON, fetch.LAST_SEASON) == (2002, 2026)


def test_download_retries_then_succeeds_and_skips_existing_files(tmp_path, monkeypatch):
    calls, sleeps = [], []

    def fake_urlopen(url, timeout):
        calls.append(url)
        if len(calls) == 1:
            raise urllib.error.URLError("connection reset")
        return FakeResponse(b"PAR1" + b"x" * 50)

    monkeypatch.setattr(fetch.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(fetch.time, "sleep", sleeps.append)
    existing = fetch.season_paths(tmp_path, 2024)["team"]
    existing.write_bytes(b"PAR1keep")
    paths = fetch.download_season(2024, tmp_path)
    assert all(p.exists() for p in paths.values())
    assert existing.read_bytes() == b"PAR1keep"  # already there: not downloaded again
    assert len(calls) == 4 and sleeps == [2]  # three missing files plus one retry
    assert not list(tmp_path.glob("*.part"))


def test_download_gives_up_and_rejects_non_parquet(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch.time, "sleep", lambda s: None)
    monkeypatch.setattr(fetch.urllib.request, "urlopen", lambda url, timeout: (_ for _ in ()).throw(urllib.error.URLError("down")))
    with pytest.raises(RuntimeError, match="could not download"):
        fetch.download_season(2024, tmp_path, backoff=(1,))
    monkeypatch.setattr(fetch.urllib.request, "urlopen", lambda url, timeout: FakeResponse(b"<html>"))
    with pytest.raises(RuntimeError, match="not a parquet"):
        fetch.download_season(2024, tmp_path, backoff=(1,))
