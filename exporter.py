import weasyprint
from uuid import uuid4
from pathlib import Path
from templates import get_templates_directory


def write_html_to_pdf(html_content: str, output: Path) -> None:
    weasyprint.HTML(string=html_content).write_pdf(output)


def write_template_to_pdf(template: str, filled_template: str, output: Path) -> None:
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
