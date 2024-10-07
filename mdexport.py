import click
from pathlib import Path


def validate_output_file(ctx: click.Context, param: click.Option, value: str):
    if ".pdf" not in value:
        raise click.BadParameter("Only export to pdf format is supported.")


def validate_md_file(ctx: click.Context, param: click.Option, value: str):
    if ".md" not in value:
        raise click.BadParameter("Only markdown(.md) files are supported as input.")


@click.command()
@click.argument("markdown_file", type=str, callback=validate_md_file)
@click.option("--output", "-o", required=True, type=str, callback=validate_output_file)
def pdfgen(markdown_file: str, output: str) -> None:
    print(f"hello {markdown_file}")


if __name__ == "__main__":
    pdfgen()
