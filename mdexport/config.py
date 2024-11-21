from pathlib import Path
import os
import json
import click


APP_NAME = "mdexport"
CONFIG_FILENAME = "config.json"


class ConfigStructure:
    TEMPLATE_DIR = "template_dir"
    ATTACHMENTS_FOLDER = "attachments"


def get_possible_config_keys() -> list[str]:
    return [
        getattr(ConfigStructure, key)
        for key in vars(ConfigStructure)
        if not key.startswith("__")
    ]


DEFAULT_CONFIG = {
    ConfigStructure.TEMPLATE_DIR: "",
    ConfigStructure.ATTACHMENTS_FOLDER: "attachments",
}

CONFIG_HELP = {
    ConfigStructure.TEMPLATE_DIR: "Directory where you store your templates. Each template should be in a different folder and contain a template.html file.",
    ConfigStructure.ATTACHMENTS_FOLDER: "If you use a tool like Obsidian that uses wikilinks for images and stores them in a custom subfolder.",
}


class InvalidKeyException(Exception):
    pass


class Config:
    config = {}

    def __init__(self):
        if not (_get_config_directory() / CONFIG_FILENAME).is_file():
            json_string = json.dumps(DEFAULT_CONFIG)
            (_get_config_directory() / CONFIG_FILENAME).write_text(json_string)

    def load(self):
        with open(_get_config_directory() / CONFIG_FILENAME, "r") as config_file:
            self.config = json.load(config_file)
        for key in get_possible_config_keys():
            if key not in self.config.keys():
                self.set(key, DEFAULT_CONFIG[key])

    def save(self) -> None:
        with open(_get_config_directory() / CONFIG_FILENAME, "w") as config_file:
            json.dump(self.config, config_file)

    def set(self, key, value):
        if key in get_possible_config_keys():
            self.config[key] = value
            self.save()
        else:
            raise InvalidKeyException(
                """{key} is not a valid options. Use 'mdexports options list' to see a list of valid option keys."""
            )

    def pre_publish_config_check(self):
        if (
            ConfigStructure.TEMPLATE_DIR not in self.config.keys()
            or self.config[ConfigStructure.TEMPLATE_DIR] == ""
        ):
            click.echo(
                f"""ERROR: Template directory not set.
Please run:
{APP_NAME} options set {ConfigStructure.TEMPLATE_DIR} /path/to/templates/
Your template directory should hold only folders named with the template name.
Inside the should be a Jinja2 template named "template.html"
"""
            )
            exit()

        if not Path(self.config[ConfigStructure.TEMPLATE_DIR]).is_dir():
            click.echo(
                """ERROR: Template directory set in the configurations is invalid.
 Please run:
{APP_NAME} options set {ConfigStructure.TEMPLATE_DIR} /path/to/templates/
Your template directory should hold only folders named with the template name.
Inside the should be a Jinja2 template named "template.html"                  
"""
            )
            exit()


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


class TemplateDirNotSetException(Exception):
    pass


def get_templates_directory() -> Path:
    """Get the path to the "templates" directory of this repo

    Returns:
        Path: Path to the directory holding the templates
    """

    if ConfigStructure.TEMPLATE_DIR in config.config.keys():
        return Path(config.config[ConfigStructure.TEMPLATE_DIR])
    else:
        raise TemplateDirNotSetException()


def get_attachment_dir() -> Path:
    return Path(config.config[ConfigStructure.ATTACHMENTS_FOLDER])


config = Config()
config.load()
