import click
from pathlib import Path

from mdexport.cli import (
    validate_md_file,
    validate_output_file,
    generate_template_help,
    validate_template,
)
from mdexport.markdown import read_md_file, convert_md_to_html, extract_md_metadata
from mdexport.templates import (
    fill_template,
    match_metadata_to_template,
    ExpectedMoreMetaDataException,
)
from mdexport.exporter import write_html_to_pdf, write_template_to_pdf
from mdexport.config import config, CONFIG_HELP


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
    """Publish Markdown files to PDF."""
    config.pre_publish_config_check()
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


@click.group()
def options():
    """Manage MDExport options."""
    pass


@options.command()
def list():
    """List all available options."""
    click.echo("Available options:")
    for key, value in config.config.items():
        click.echo("")
        click.echo(f"   {key}: {value}")
        click.echo("")
        click.echo(CONFIG_HELP[key])


@options.command()
@click.argument("key")
@click.argument("value")
def set(key: str, value: str):
    """Set an option value."""
    print(key, value)
    config.set(key, value)
    config.save()


cli.add_command(publish)
cli.add_command(options)
if __name__ == "__main__":
    cli()
