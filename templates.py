from pathlib import Path
from typing import List

import jinja2


def get_templates_directory() -> Path:
    """Get the path to the "templates" directory of this repo

    Returns:
        Path: Path to the directory holding the templates
    """
    return Path(__file__).resolve().parent / "templates"


def get_available_templates() -> List[str]:
    """List all the directories in the templates directory

    Returns:
        [str]: Available templates
    """
    templates_directory = get_templates_directory()
    return [str(f.name) for f in templates_directory.iterdir() if f.is_dir()]


def fill_template(template: str, html_content: str, metadata: dict = {}) -> str:
    current_template = get_templates_directory() / template / "template.html"
    template_html = jinja2.Template(current_template.read_text())
    return template_html.render(body=html_content, **metadata)
