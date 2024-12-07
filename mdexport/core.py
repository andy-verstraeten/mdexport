from mdexport.markdown import convert_md_to_html, extract_md_metadata
from mdexport.templates import (
    fill_template,
    match_metadata_to_template,
    ExpectedMoreMetaDataException,
)
from pathlib import Path
import click


def generate_renderable_html(
    md_content: str, md_path: Path, template: str | None, toc_html=None
):
    html_content = convert_md_to_html(md_content, md_path)
    metadata = extract_md_metadata(md_path)
    if toc_html:
        metadata["toc"] = toc_html
    if template:
        try:
            match_metadata_to_template(template, metadata.keys())
        except ExpectedMoreMetaDataException as e:
            click.echo(f"!!!!! WARNING: {e}")
    return fill_template(template, html_content, metadata) if template else html_content
