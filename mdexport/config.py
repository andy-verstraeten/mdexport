from pathlib import Path
import os
import json
import click
from enum import Enum

APP_NAME = "mdexport"
CONFIG_FILENAME = "config.json"


class ConfigStructure(Enum):
    TEMPLATE_DIR = "template_dir"


def _get_config_directory() -> Path:
    home_dir = Path.home()

    # Determine the appropriate config directory based on the platform
    if os.name == "nt":  # Windows
        config_dir = home_dir / "AppData" / "Local" / APP_NAME
    elif os.name == "posix":  # macOS and Linux
        config_dir = home_dir / ".config" / APP_NAME
    else:
        raise OSError("Unsupported operating system")

    # Create the directory if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def load() -> dict:
    config_path = _get_config_directory() / CONFIG_FILENAME
    if not config_path.exists():
        config_path.write_text("{}")
    with open(_get_config_directory() / CONFIG_FILENAME, "r") as config_file:
        return json.load(config_file)


def save(config: dict) -> None:
    with open(_get_config_directory() / CONFIG_FILENAME, "w") as config_file:
        json.dump(config, config_file)


def set_template_dir(template_dir: Path):
    settings = load()
    settings[ConfigStructure.TEMPLATE_DIR.value] = str(template_dir)
    save(settings)


def preflight_checks():
    if not (_get_config_directory() / CONFIG_FILENAME).is_file():
        (_get_config_directory() / CONFIG_FILENAME).write_text("{}")

    settings = load()
    if ConfigStructure.TEMPLATE_DIR.value not in settings.keys():
        click.echo(
            f"""ERROR: Template directory not set.
Please run:
{APP_NAME} settemplatedir /path/to/templates/
Your template directory should hold only folders named with the template name.
Inside the should be a Jinja2 template named "template.html"
"""
        )
        exit()
    if not Path(settings[ConfigStructure.TEMPLATE_DIR.value]).is_dir():
        click.echo(
            """ERROR: Template directory set in the configurations is invalid.
 Please run:
{APP_NAME} settemplatedir /path/to/templates/
Your template directory should hold only folders named with the template name.
Inside the should be a Jinja2 template named "template.html"                  
"""
        )
        exit()


class TemplateDirNotSetException(Exception):
    pass


def get_templates_directory() -> Path:
    """Get the path to the "templates" directory of this repo

    Returns:
        Path: Path to the directory holding the templates
    """
    settings = load()

    if ConfigStructure.TEMPLATE_DIR.value in settings.keys():
        return Path(settings[ConfigStructure.TEMPLATE_DIR.value])
    else:
        raise TemplateDirNotSetException()
