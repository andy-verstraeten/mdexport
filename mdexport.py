import click
import markdown2
import weasyprint
import jinja2
from uuid import uuid4
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
    if value is not None and value not in get_available_templates():
        raise click.BadParameter(f"Please provide a valid template. \n{generate_template_help()}")
    return value

def get_templates_directory()->Path:
    """Get the path to the "templates" directory of this repo

    Returns:
        Path: Path to the directory holding the templates
    """
    return Path(__file__).resolve().parent / "templates"

def get_available_templates()->List[str]:
    """List all the directories in the templates directory

    Returns:
        [str]: Available templates
    """
    templates_directory = get_templates_directory()
    return [str(f.name) for f in templates_directory.iterdir() if f.is_dir()]

def generate_template_help():
    template_options = get_available_templates()
    return f"Provide one of the following templates: {",".join(template_options)}"

def fill_template(template:str, html_content: str)->str:
    current_template = get_templates_directory() / template / "template.html"
    template_html = jinja2.Template(current_template.read_text())
    return template_html.render(body=html_content)



def read_md_file(md_file: Path) -> str:
    return md_file.read_text()


def convert_md_to_html(md_content: str) -> str:
    return markdown2.markdown(md_content)

def write_html_to_pdf(html_content:str, output:Path)->None:
    weasyprint.HTML(string=html_content).write_pdf(output)



     
        
def write_template_to_pdf(template: str, filled_template: str, output:Path)->None:
    render_file = f".{uuid4()}.html"
    render_full_path = get_templates_directory() / template / render_file
    render_full_path.write_text(filled_template)
    weasyprint.HTML(render_full_path).write_pdf(output)
    render_full_path.unlink()


@click.command()
@click.argument("markdown_file", type=str, callback=validate_md_file)
@click.option("--output", "-o", required=True, type=str, callback=validate_output_file)
@click.option("--template", "-t",required=False, help=generate_template_help(), callback=validate_template)
def pdfgen(markdown_file: str, output: str, template: str) -> None:
    md_content = read_md_file(Path(markdown_file))
    html_content = convert_md_to_html(md_content)
    if not template:
        write_html_to_pdf(html_content, Path(output))
    else:
        filled_template = fill_template(template, html_content)
        print(filled_template)
        write_template_to_pdf(template, filled_template, Path(output))
if __name__ == "__main__":
    pdfgen()
