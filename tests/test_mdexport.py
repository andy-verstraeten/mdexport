from mdexport.mdexport import set_template_dir
from pytest import MonkeyPatch
import mdexport


def test_set_template_dir(monkeypatch: MonkeyPatch):
    def mock_save(config: dict):
        assert config["mock_key"] == "mock_value"
        assert config["template_dir"] == "/mock/template/dir"

    monkeypatch.setattr(mdexport.config, "load", lambda: {"mock_key": "mock_value"})
    monkeypatch.setattr(mdexport.config, "save", mock_save)
    set_template_dir(None, "/mock/template/dir")
