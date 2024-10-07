import click
import markdown2
from pathlib import Path


def validate_output_file(ctx: click.Context, param: click.Option, value: str) -> str:
    if ".pdf" not in value:
        raise click.BadParameter("Only export to pdf format is supported.")
    return value


def validate_md_file(ctx: click.Context, param: click.Option, value: str) -> str:
    if ".md" not in value:
        raise click.BadParameter("Only markdown(.md) files are supported as input.")
    return value


def read_md_file(md_file: Path) -> str:
    return md_file.read_text()


def convert_md_to_html(md_content: str) -> str:
    return markdown2.markdown(md_content)


@click.command()
@click.argument("markdown_file", type=str, callback=validate_md_file)
@click.option("--output", "-o", required=True, type=str, callback=validate_output_file)
def pdfgen(markdown_file: str, output: str) -> None:
    md_content = read_md_file(Path(markdown_file))
    html_content = convert_md_to_html(md_content)
    print(html_content)


if __name__ == "__main__":
    pdfgen()
