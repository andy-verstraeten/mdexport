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
    with open(_get_config_directory() / CONFIG_FILENAME, "r") as config_file:
        return json.load(config_file)


def save(config: dict) -> None:
    with open(_get_config_directory() / CONFIG_FILENAME, "w") as config_file:
        json.dump(config, config_file)


def preflight_checks():
    if not (_get_config_directory() / CONFIG_FILENAME).is_file():
        (_get_config_directory() / CONFIG_FILENAME).write_text("{}")

    settings = load()
    if ConfigStructure.TEMPLATE_DIR not in settings.keys():
        click.echo(
            f"""ERROR: Template directory not set.
Please run:
{APP_NAME} settemplatedir /path/to/templates/
Your template directory should hold only folders named with the template name.
Inside the should be a Jinja2 template named "template.html"
"""
        )
