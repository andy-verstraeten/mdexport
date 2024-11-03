from mdexport.cli import validate_template_dir
from pathlib import Path
import pytest
import click


def test_validate_template_dir_invalid(tmp_path: Path):
    with pytest.raises(click.BadParameter):
        NON_EXISTENT_FOLDER = tmp_path / "I_DONT_EXIST"
        validate_template_dir(None, None, str(NON_EXISTENT_FOLDER))


def test_validate_template_dir_is_not_folder(tmp_path: Path):
    with pytest.raises(click.BadParameter):
        NOT_A_FOLDER = tmp_path / "FILE"
        NOT_A_FOLDER.touch()
        validate_template_dir(None, None, str(NOT_A_FOLDER))


def test_validate_template_dir_valid(tmp_path: Path):
    assert validate_template_dir(None, None, str(tmp_path)) == tmp_path
