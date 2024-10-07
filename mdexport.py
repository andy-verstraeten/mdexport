import click
from pathlib import Path


def validate_output_file(ctx: click.Context, param: click.Option, value: str):
    if ".pdf" not in value:
        raise click.BadParameter("Only export to pdf format is supported.")


@click.command()
@click.argument("md_file")
@click.option("--output", "-o", required=True, type=str, callback=validate_output_file)
def pdfgen(md_file: Path, output: str) -> None:
    print(f"hello {md_file}")


if __name__ == "__main__":
    pdfgen()
