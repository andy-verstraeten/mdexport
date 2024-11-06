import mdexport.config
from pytest import MonkeyPatch
import pytest
from pathlib import Path
from mdexport.config import (
    _get_config_directory,
    APP_NAME,
    CONFIG_FILENAME,
    load,
    save,
    get_templates_directory,
    TemplateDirNotSetException,
    ConfigStructure,
)
import mdexport


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


def test_load_config(monkeypatch: MonkeyPatch, tmp_path: Path):
    MOCK_CONFIG_TEXT = """
    {
    "mock_key":"mock_value"
    }"""
    (tmp_path / "config.json").write_text(MOCK_CONFIG_TEXT)
    monkeypatch.setattr(mdexport.config, "_get_config_directory", lambda: tmp_path)
    config = load()
    assert config
    assert config["mock_key"] == "mock_value"


def test_save_config(monkeypatch: MonkeyPatch, tmp_path: Path):
    MOCK_CONFIG = {"mock_key": "mock_value"}
    monkeypatch.setattr(mdexport.config, "_get_config_directory", lambda: tmp_path)
    save(MOCK_CONFIG)
    assert (tmp_path / CONFIG_FILENAME).read_text() == '{"mock_key": "mock_value"}'


def test_get_templates_directory_not_set(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(mdexport.config, "load", lambda: {})
    with pytest.raises(TemplateDirNotSetException):
        get_templates_directory()


def test_get_templates_directory_happy_path(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(
        mdexport.config,
        "load",
        lambda: {ConfigStructure.TEMPLATE_DIR.value: "/path/to/templates"},
    )
    assert get_templates_directory() == Path("/path/to/templates")
