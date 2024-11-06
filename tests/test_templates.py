import mdexport.mdexport
from pytest import MonkeyPatch, raises
from pathlib import Path

from mdexport.templates import (
    extract_variables,
    get_available_templates,
    read_template,
    fill_template,
    match_metadata_to_template,
    ExpectedMoreMetaDataException,
    BODY_VAR,
)

import mdexport


def test_get_available_templates(monkeypatch: MonkeyPatch, tmp_path: Path):
    template1 = tmp_path / "template1"
    template1.mkdir()
    template2 = tmp_path / "template2"
    template2.mkdir()
    (tmp_path / "not_a_template.txt").touch()
    monkeypatch.setattr(mdexport.templates, "get_templates_directory", lambda: tmp_path)
    assert {*get_available_templates()} == {"template1", "template2"}


def test_read_template(monkeypatch: MonkeyPatch, tmp_path: Path):
    MOCK_TEMPLATE = "mock_template"
    (tmp_path / MOCK_TEMPLATE).mkdir()
    (tmp_path / MOCK_TEMPLATE / "template.html").write_text("<html></html>")
    monkeypatch.setattr(mdexport.templates, "get_templates_directory", lambda: tmp_path)
    assert read_template(MOCK_TEMPLATE) == "<html></html>"


def test_extract_variables():
    DUMMY_HTML_TEMPLATE = """<html>
    <header>{{var1}}</header>
    <body>
    {{body}}
    </body>
    </html>
"""
    assert extract_variables(DUMMY_HTML_TEMPLATE) == {"var1", "body"}


def test_fill_template(monkeypatch: MonkeyPatch):
    metadata = {"metadata1": "mock_metadata"}
    monkeypatch.setattr(
        mdexport.templates,
        "read_template",
        lambda _: "<html><header>{{metadata1}}</header><body>{{body}}</body></html>",
    )
    body = "mock_body"
    assert (
        fill_template("mock_template", "mock_body", metadata)
        == "<html><header>mock_metadata</header><body>mock_body</body></html>"
    )


def test_match_metadata_to_template(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(
        mdexport.templates,
        "read_template",
        lambda _: "",
    )
    monkeypatch.setattr(
        mdexport.templates,
        "extract_variables",
        lambda _: ["metadata1", "metadata2", BODY_VAR],
    )
    with raises(ExpectedMoreMetaDataException):
        match_metadata_to_template("MOCK_TEMPLATE", {"metadata1": "mock_metadata"})


def test_extract_varialbes():
    MOCK_TEMPLATE_STRING = """<html>
    <header>
    {{variable1}}
    {{variable1}}
    </header>
    <body>
    <h2>{{variable2}}</h2>
    <section>
    {{body}}
    </section>
    </body>
    </html>
"""
    assert extract_variables(MOCK_TEMPLATE_STRING) == {"variable1", "variable2", "body"}
