import weasyprint
import click
from uuid import uuid4
from pathlib import Path
from mdexport.templates import (
    get_templates_directory,
    TemplateDirNotSetException,
    APP_NAME,
)
import re

BASE_STYLE_HTML = """
<style>
img {
  max-width: 100%;
}

table,tr,td,th {
border-collapse: collapse;
border: 1px solid black;
}
td,th {
padding: 5px;
}
</style>
"""


class MissingHTMLTagException(Exception):
    pass


def insert_base_style(html_text: str) -> str:
    """Insert the BASE_STYLE_HTML into the html string. Base style insures
    basic restraints like image size. Style is insert before end of the </head>
    tag or if it is not preset straight after opening <html> tag

    Args:
        html_text (str): html string

    Returns:
        str: html string with base style injected
    """
    if "</head>" in html_text.lower():
        html_text = re.sub(
            "</head>", f"</head>\n{BASE_STYLE_HTML}\n", html_text, flags=re.IGNORECASE
        )
    elif "<html>" in html_text.lower():
        html_text = re.sub(
            "<html>", f"<html>\n{BASE_STYLE_HTML}\n", html_text, flags=re.IGNORECASE
        )
    else:
        html_text = f"""<html>
        <head>
        {BASE_STYLE_HTML}
        </head>
        <body>
        {html_text}
        </body>
        </html>
        """

    return html_text


def write_html_to_pdf(html_content: str, output: Path) -> None:
    html_content = insert_base_style(html_content)
    # base_url refers to the highest root directory. Required to render absolute path image paths
    weasyprint.HTML(string=html_content, base_url=Path.cwd().root).write_pdf(output)


def write_template_to_pdf(template: str, filled_template: str, output: Path) -> None:
    """Writes the filled out html template to a uuid named html file in the template folder
    and renders it to the output path as a pdf.

    Args:
        template (str): _description_
        filled_template (str): _description_
        output (Path): _description_
    """
    try:
        filled_template = insert_base_style(filled_template)
        render_file = f".{uuid4()}.html"
        render_full_path = get_templates_directory() / template / render_file
        render_full_path.write_text(filled_template)
        weasyprint.HTML(render_full_path).write_pdf(output)
        render_full_path.unlink()
    except TemplateDirNotSetException:
        click.echo(
            f"""ERROR: Template directory not set in mdexport config.
Please run:
{APP_NAME} settemplatedir /path/to/templates/
Your template directory should hold only folders named with the template name.
Inside the should be a Jinja2 template named "template.html"  
            """
        )
        exit()
