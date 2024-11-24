from pytest import MonkeyPatch
from pathlib import Path
from mdexport.config import (
    _get_config_directory,
    APP_NAME,
    CONFIG_FILENAME,
    Config,
    ConfigStructure,
)
import mdexport.config
import sys


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


def test_config_init(monkeypatch: MonkeyPatch, tmp_path: Path):
    monkeypatch.setattr(mdexport.config, "_get_config_directory", lambda: tmp_path)
    Config()
    assert (tmp_path / CONFIG_FILENAME).is_file()


class MockConfigStructure:
    CONFIG1 = "config1"
    CONFIG2 = "config2"
    CONFIG3 = "config3"


def test_config_load(monkeypatch: MonkeyPatch, tmp_path: Path):
    monkeypatch.setattr(mdexport.config, "_get_config_directory", lambda: tmp_path)
    monkeypatch.setattr(mdexport.config, "DEFAULT_CONFIG", {"config3": "value3"})
    monkeypatch.setattr(mdexport.config, "ConfigStructure", MockConfigStructure)
    (tmp_path / CONFIG_FILENAME).write_text("""{"config1":"value1",
"config2":"value2"
}""")
    config = Config()
    config.load()
    assert config.config == {
        "config1": "value1",
        "config2": "value2",
        "config3": "value3",
    }


def test_config_save(monkeypatch: MonkeyPatch, tmp_path: Path):
    monkeypatch.setattr(mdexport.config, "_get_config_directory", lambda: tmp_path)
    config = Config()
    config.config = {"config1": "value1", "config2": "value2", "config3": "value3"}
    config.save()
    assert (
        tmp_path / CONFIG_FILENAME
    ).read_text() == '{"config1": "value1", "config2": "value2", "config3": "value3"}'


def test_config_set(monkeypatch: MonkeyPatch, tmp_path: Path):
    monkeypatch.setattr(mdexport.config, "_get_config_directory", lambda: tmp_path)
    monkeypatch.setattr(mdexport.config, "ConfigStructure", MockConfigStructure)
    savecalled = False

    def mock_save(_):
        nonlocal savecalled
        savecalled = True

    monkeypatch.setattr(mdexport.config.Config, "save", mock_save)
    config = Config()
    config.set("config1", "value2")
    assert config.config == {"config1": "value2"} and savecalled


def test_config_preflight_templatedir_not_set(monkeypatch: MonkeyPatch, tmp_path: Path):
    monkeypatch.setattr(mdexport.config, "_get_config_directory", lambda: tmp_path)

    exit_called = False

    def mock_exit():
        nonlocal exit_called
        exit_called = True

    monkeypatch.setattr(mdexport.config, "exit", mock_exit)
    config = Config()
    config.config = {ConfigStructure.TEMPLATE_DIR: ""}
    config.pre_publish_config_check()
    assert exit_called


def test_config_preflight_templatedir_invalid(monkeypatch: MonkeyPatch, tmp_path: Path):
    monkeypatch.setattr(mdexport.config, "_get_config_directory", lambda: tmp_path)

    exit_called = False

    def mock_exit():
        nonlocal exit_called
        exit_called = True

    monkeypatch.setattr(mdexport.config, "exit", mock_exit)
    config = Config()
    config.config = {ConfigStructure.TEMPLATE_DIR: (tmp_path / "not_a_dir")}
    config.pre_publish_config_check()
    assert exit_called
