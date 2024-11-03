import mdexport.exporter
import uuid
from mdexport.exporter import (
    insert_base_style,
    BASE_STYLE_HTML,
    write_html_to_pdf,
    write_template_to_pdf,
)
import mdexport.templates
from pytest import MonkeyPatch
import mdexport
from pathlib import Path


def test_insert_base_style(monkeypatch: MonkeyPatch):
    MOCK_STYLE = """
    <style>
    body {}
    </style>
"""
    monkeypatch.setattr(mdexport.exporter, "BASE_STYLE_HTML", MOCK_STYLE)
    MOCK_HTML = """
<html>
<head>
</head>
</html>
"""
    EXPECTED_HTML = """
<html>
<head>
</head>
<style>
body {}
</style>
</html>
"""
    assert "".join(insert_base_style(MOCK_HTML).split()) == "".join(
        EXPECTED_HTML.split()
    )


def test_write_html_to_pdf(monkeypatch: MonkeyPatch):
    MOCK_HTML_CONTENT = "<html><h1>MOCK</h1></html>"
    MOCK_OUTPUT_PATH = Path("/mock/path") / "output.pdf"

    def fake_insert_base_style(html_content: str) -> str:
        assert html_content == "<html><h1>MOCK</h1></html>"
        return html_content

    class Write_Pdf_Mock:
        def write_pdf(self, output):
            assert output == Path("/mock/path") / "output.pdf"

    def HTML_Mock(string: str, base_url: str):
        assert string == MOCK_HTML_CONTENT
        return Write_Pdf_Mock()

    monkeypatch.setattr(mdexport.exporter, "insert_base_style", fake_insert_base_style)
    monkeypatch.setattr("weasyprint.HTML", HTML_Mock)
    write_html_to_pdf(MOCK_HTML_CONTENT, MOCK_OUTPUT_PATH)


def test_write_template_to_pdf(monkeypatch: MonkeyPatch, tmp_path: Path):
    def fake_insert_base_style(html_content: str) -> str:
        assert html_content == "<html><h1>MOCK</h1></html>"
        return html_content

    MOCK_TEMPLATE = "MOCK_TEMPLATE"
    FILLED_TEMPLATE = "<html><h1>MOCK</h1></html>"
    MOCK_OUTPUT = tmp_path / "output.pdf"
    (tmp_path / MOCK_TEMPLATE).mkdir()
    monkeypatch.setattr(
        mdexport.exporter,
        "get_templates_directory",
        lambda: tmp_path,
    )
    monkeypatch.setattr(mdexport.exporter, "insert_base_style", fake_insert_base_style)
    monkeypatch.setattr(
        mdexport.exporter, "uuid4", lambda: "5e558a5b-b886-4bd3-a575-80902a967d25"
    )
    write_template_to_pdf(MOCK_TEMPLATE, FILLED_TEMPLATE, MOCK_OUTPUT)
