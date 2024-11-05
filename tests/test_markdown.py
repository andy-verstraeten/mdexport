from pathlib import Path
from mdexport.markdown import (
    extract_md_metadata,
    read_md_file,
    convert_md_to_html,
    get_base_path,
    embed_to_img_tag,
    ATTACHMENT_DIRECTORY,
    convert_metadata_to_html,
)


def test_extract_md_metadata(tmp_path: Path):
    MOCK_MD = """---
metadata1: mockmetadata1
metadata2: mockmetadata2
metadata3: mockmetadata3
---

notmetadata: mocknotmetadata
"""
    mock_md_file = tmp_path / "mockfile.md"
    mock_md_file.write_text(MOCK_MD)
    assert extract_md_metadata(mock_md_file) == {
        "metadata1": "mockmetadata1",
        "metadata2": "mockmetadata2",
        "metadata3": "mockmetadata3",
    }


def test_read_md_file(tmp_path: Path):
    MOCK_MD = """---
metadata1: mockmetadata1
---

notmetadata: mocknotmetadata
"""
    mock_md_file = tmp_path / "mockfile.md"
    mock_md_file.write_text(MOCK_MD)
    assert read_md_file(mock_md_file) == "notmetadata: mocknotmetadata"


def test_convert_md_to_html():
    MOCK_MD = """# Title1
    content
"""
    assert (
        convert_md_to_html(MOCK_MD, Path("/"))
        == """<h1>Title1</h1>

<pre><code>content
</code></pre>
"""
    )


def test_get_base_path():
    assert get_base_path(Path("/")) == Path("/") / ATTACHMENT_DIRECTORY


def test_embed_to_img_tag():
    MOCK_MD = "![[test.jpg]]"
    assert (
        embed_to_img_tag(MOCK_MD, Path("/mock/path"))
        == '<img src="/mock/path/test.jpg" alt="test.jpg" />'
    )


def test_convert_metadata_to_html_no_surounding_p():
    metadata = "some metadata"
    html = convert_metadata_to_html(metadata)
    assert not html.startswith("<p>") and not html.endswith("</p>\n")
