import click
import markdown2
import weasyprint
from typing import List
from pathlib import Path


def validate_output_file(ctx: click.Context, param: click.Option, value: str) -> str:
    if ".pdf" not in value:
        raise click.BadParameter("Only export to pdf format is supported.")
    return value


def validate_md_file(ctx: click.Context, param: click.Parameter, value: str) -> str:
    if ".md" not in value:
        raise click.BadParameter("Only markdown(.md) files are supported as input.")
    if not Path(value).exists():
        raise click.BadParameter(f"{value} file does not exist.")
    return value

def validate_template(ctx: click.Context, param: click.Option, value: str) -> str:
    if value not in get_available_templates():
        raise click.BadParameter(f"Please provide a valid template. \n{generate_template_help()}")
    return value

def get_available_templates()->List[str]:
    """List all the directories in the "templates" directory of this repo

    Returns:
        [str]: Available templates
    """
    templates_directory = Path(__file__).resolve().parent / "templates"
    return [str(f.name) for f in templates_directory.iterdir() if f.is_dir()]

def generate_template_help():
    template_options = get_available_templates()
    return f"Provide one of the following templates: {",".join(template_options)}"

def read_md_file(md_file: Path) -> str:
    return md_file.read_text()


def convert_md_to_html(md_content: str) -> str:
    return markdown2.markdown(md_content)

def write_html_to_pdf(html_content:str, output:Path)->None:
    weasyprint.HTML(string=html_content).write_pdf(output)

@click.command()
@click.argument("markdown_file", type=str, callback=validate_md_file)
@click.option("--output", "-o", required=True, type=str, callback=validate_output_file)
@click.option("--template", "-t", help=generate_template_help(), callback=validate_template)
def pdfgen(markdown_file: str, output: str, template: str) -> None:
    md_content = read_md_file(Path(markdown_file))
    html_content = convert_md_to_html(md_content)
    write_html_to_pdf(html_content, Path(output))


if __name__ == "__main__":
    pdfgen()
