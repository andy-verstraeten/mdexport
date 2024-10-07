import click
from pathlib import Path


@click.command()
@click.argument("md_file")
def pdfgen(md_file: Path) -> None:
    print(f"hello {md_file}")


if __name__ == "__main__":
    pdfgen()
