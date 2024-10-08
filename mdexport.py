import click
import markdown2
import weasyprint
import jinja2
import frontmatter
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

def fill_template(template:str, html_content: str, metadata: dict={})->str:
    current_template = get_templates_directory() / template / "template.html"
    template_html = jinja2.Template(current_template.read_text())
    return template_html.render(body=html_content,**metadata)

def extract_md_metadata(md_file:Path)->dict:
    return frontmatter.load(md_file).metadata

def read_md_file(md_file: Path) -> str:
    return frontmatter.load(md_file).content


def convert_md_to_html(md_content: str) -> str:
    return markdown2.markdown(md_content)

def write_html_to_pdf(html_content:str, output:Path)->None:
    weasyprint.HTML(string=html_content).write_pdf(output)



     
        
def write_template_to_pdf(template: str, filled_template: str, output:Path)->None:
    """Writes the filled out html template to a uuid named html file in the template folder
    and renders it to the output path as a pdf. 

    Args:
        template (str): _description_
        filled_template (str): _description_
        output (Path): _description_
    """
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
        metadata = extract_md_metadata(Path(markdown_file))
        filled_template = fill_template(template, html_content,metadata)
        write_template_to_pdf(template, filled_template, Path(output))
if __name__ == "__main__":
    pdfgen()
