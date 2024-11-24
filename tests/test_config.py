from pytest import MonkeyPatch
from pathlib import Path
from mdexport.config import (
    _get_config_directory,
    APP_NAME,
)


def test_config_directory_windows(monkeypatch: MonkeyPatch, tmp_path: Path):
    monkeypatch.setattr("os.name", "nt")
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

    config_dir = _get_config_directory()
    assert config_dir == tmp_path / "AppData" / "Local" / APP_NAME


def test_config_directory_unix(monkeypatch: MonkeyPatch, tmp_path: Path):
    monkeypatch.setattr("os.name", "posix")
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
    config_dir = _get_config_directory()
    assert config_dir == tmp_path / ".config" / APP_NAME


# TODO: implement more tests here
