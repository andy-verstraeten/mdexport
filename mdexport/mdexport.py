import click
from pathlib import Path

from .cli import (
    validate_md_file,
    validate_output_file,
    generate_template_help,
    validate_template,
    validate_template_dir,
)
from .markdown import read_md_file, convert_md_to_html, extract_md_metadata
from .templates import (
    fill_template,
    match_metadata_to_template,
    ExpectedMoreMetaDataException,
)
from .exporter import write_html_to_pdf, write_template_to_pdf
import mdexport.config as config


@click.group()
def cli():
    pass


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
def publish(markdown_file: str, output: str, template: str) -> None:
    config.preflight_checks()
    md_path = Path(markdown_file)
    md_content = read_md_file(md_path)
    html_content = convert_md_to_html(md_content, md_path)
    if not template:
        write_html_to_pdf(html_content, Path(output))
    else:
        metadata = extract_md_metadata(Path(markdown_file))
        try:
            match_metadata_to_template(template, metadata.keys())
        except ExpectedMoreMetaDataException as e:
            click.echo(f"!!!!! WARNING: {e}")
        filled_template = fill_template(template, html_content, metadata)
        write_template_to_pdf(template, filled_template, Path(output))


@click.command()
@click.argument("template_dir", type=str, callback=validate_template_dir)
def set_template_dir(template_dir: Path):
    config.set_template_dir(template_dir)


cli.add_command(publish)
cli.add_command(set_template_dir, "settemplatedir")
if __name__ == "__main__":
    cli()
