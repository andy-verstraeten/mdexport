from pathlib import Path
from typing import List

from jinja2 import meta
import jinja2


class ExpectedMoreMetaDataException(Exception):
    pass


BODY_VAR = "body"


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


def read_template(template: str) -> str:
    current_template = get_templates_directory() / template / "template.html"
    return current_template.read_text()


def fill_template(template: str, html_content: str, metadata: dict = {}) -> str:
    template_html = jinja2.Template(read_template(template))
    return template_html.render(body=html_content, **metadata)


def match_metadata_to_template(template: str, metadata_keys):
    template_html = read_template(template)
    template_variables = extract_variables(template_html)
    not_included_metadata = list(
        set(template_variables) - set(metadata_keys) - {BODY_VAR}
    )
    if len(not_included_metadata) > 0:
        raise ExpectedMoreMetaDataException(f"The used template expects the following variable values to be passed as frontmatter metadata: {",".join(not_included_metadata)} ")


def extract_variables(template_string: str) -> List[str]:
    """Extract all variables used in a jinja2 template

    Args:
        template_string (str): jinja2 html template string

    Returns:
        List[str]: variable names
    """
    env = jinja2.Environment()
    parsed_content = env.parse(template_string)
    variables = meta.find_undeclared_variables(parsed_content)
    return list(variables)
