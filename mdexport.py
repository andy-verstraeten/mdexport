import click
from pathlib import Path

from cli import (
    validate_md_file,
    validate_output_file,
    generate_template_help,
    validate_template,
)
from markdown import read_md_file, convert_md_to_html, extract_md_metadata
from templates import fill_template
from exporter import write_html_to_pdf, write_template_to_pdf


@click.command()
@click.argument("markdown_file", type=str, callback=validate_md_file)
@click.option("--output", "-o", required=True, type=str, callback=validate_output_file)
@click.option(
    "--template",
    "-t",
    required=False,
    help=generate_template_help(),
    callback=validate_template,
)
def pdfgen(markdown_file: str, output: str, template: str) -> None:
    md_content = read_md_file(Path(markdown_file))
    html_content = convert_md_to_html(md_content)
    if not template:
        write_html_to_pdf(html_content, Path(output))
    else:
        metadata = extract_md_metadata(Path(markdown_file))
        filled_template = fill_template(template, html_content, metadata)
        write_template_to_pdf(template, filled_template, Path(output))


if __name__ == "__main__":
    pdfgen()
