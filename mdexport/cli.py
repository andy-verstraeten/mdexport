import click
from pathlib import Path
from .templates import get_available_templates


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
        raise click.BadParameter(
            f"Please provide a valid template. \n{generate_template_help()}"
        )
    return value


def generate_template_help():
    template_options = get_available_templates()
    return f"Provide one of the following templates: {",".join(template_options)}"


def validate_template_dir(
    ctx: click.Context, param: click.Parameter, template_dir: str
):
    template_path = Path(template_dir)
    if not template_path.exists():
        raise click.BadParameter(
            "Folder does not exist. Please provide an existing folder."
        )

    if not template_path.is_dir():
        raise click.BadParameter(
            "The provided path is not a folder. Please provide the path to a folder."
        )

    return Path(template_dir)
