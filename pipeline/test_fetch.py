import io
import urllib.request
import urllib.error

import pytest

import fetch


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


def test_url_and_path():
    assert fetch.season_url(2024).endswith("/espn_nba_pbp/play_by_play_2024.parquet")
    assert fetch.raw_path(fetch.Path("data/raw"), 2024).name == "play_by_play_2024.parquet"


def test_download_retries_then_succeeds(tmp_path, monkeypatch):
    calls = []
    sleeps = []

    def fake_urlopen(url, timeout):
        calls.append(url)
        if len(calls) < 3:
            raise urllib.error.URLError("connection reset")
        return FakeResponse(b"PAR1" + b"x" * 100)

    monkeypatch.setattr(fetch.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(fetch.time, "sleep", sleeps.append)
    path = fetch.download_season(2024, tmp_path)
    assert path.read_bytes().startswith(b"PAR1")
    assert len(calls) == 3
    assert sleeps == [2, 4]
    assert not list(tmp_path.glob("*.part"))


def test_download_gives_up_after_the_last_retry(tmp_path, monkeypatch):
    def fake_urlopen(url, timeout):
        raise urllib.error.URLError("no route")

    monkeypatch.setattr(fetch.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(fetch.time, "sleep", lambda s: None)
    with pytest.raises(RuntimeError, match="season 2024"):
        fetch.download_season(2024, tmp_path)
    assert not list(tmp_path.glob("*"))


def test_download_rejects_a_file_that_is_not_parquet(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch.urllib.request, "urlopen", lambda url, timeout: FakeResponse(b"<html>nope</html>"))
    monkeypatch.setattr(fetch.time, "sleep", lambda s: None)
    with pytest.raises(RuntimeError, match="not a parquet"):
        fetch.download_season(2024, tmp_path, backoff=(1,))
