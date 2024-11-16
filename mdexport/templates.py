from pathlib import Path
from typing import List, Set, Union

from jinja2 import meta
import jinja2
import click
import re
from mdexport.config import (
    get_templates_directory,
    TemplateDirNotSetException,
    APP_NAME,
)


class ExpectedMoreMetaDataException(Exception):
    pass


BODY_VAR = "body"


def get_available_templates() -> List[str]:
    """List all the directories in the templates directory

    Returns:
        [str]: Available templates
    """
    try:
        templates_directory = get_templates_directory()

        # return an empty list if the directory does not exist.
        if not templates_directory.is_dir():
            return []
        return [str(f.name) for f in templates_directory.iterdir() if f.is_dir()]
    except TemplateDirNotSetException:
        return []


def read_template(template: str):
    try:
        current_template = get_templates_directory() / template / "template.html"
        return current_template.read_text()
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


def fill_template(template: str, html_content: str, metadata: dict = {}) -> str:
    # TODO: decouple read_template
    template_html = jinja2.Template(read_template(template))
    return template_html.render(body=html_content, **metadata)


def match_metadata_to_template(template: str, metadata_keys: List[str]):
    # TODO: rename function to something more describing the action
    template_html = read_template(template)
    template_variables = extract_variables(template_html)
    not_included_metadata = list(
        set(template_variables) - set(metadata_keys) - {BODY_VAR}
    )
    if len(not_included_metadata) > 0:
        not_included_comma = ",".join(not_included_metadata)
        raise ExpectedMoreMetaDataException(
            f"The used template expects the following variable values to be passed as frontmatter metadata: {not_included_comma} "
        )


def extract_variables(template_string: str) -> Set[str]:
    """Extract all variables used in a jinja2 template

    Args:
        template_string (str): jinja2 html template string

    Returns:
        List[str]: variable names
    """
    env = jinja2.Environment()
    parsed_content = env.parse(template_string)
    variables = meta.find_undeclared_variables(parsed_content)
    return set(variables)
