import logging
from pathlib import Path
from unittest import mock

import pytest

from gfworkflow import R, logger, clear_log, dump_log, logger_handler
from gfworkflow.__main__ import main, _create_file_handler


@pytest.fixture
def version_file() -> Path:
    proj_dir: Path = Path(R.string.package_path).parent

    def are_we_in_development_project() -> bool:
        version_file: Path = proj_dir / 'VERSION'
        bumpversion_config_file: Path = proj_dir / '.bumpversion.cfg'
        return version_file.exists() and bumpversion_config_file.exists()

    if are_we_in_development_project():
        version_parent = proj_dir
    else:
        version_parent = Path(R.string.res_folder_path)
    return version_parent / 'VERSION'


def test_get_version_matches_version_file(version_file: Path):
    assert version_file.read_text() == R.string.version


def test_program_name_cli_is_non_empty_string():
    assert isinstance(R.string.program_name_cli, str)
    assert R.string.program_name_cli


def test_program_description_is_string():
    assert isinstance(R.string.program_description, str)


def test_package_path_exists():
    assert Path(R.string.package_path).exists()


def test_package_path_directory_name_matches_package_name():
    package_path_directory_name: str = Path(R.string.package_path).name
    assert package_path_directory_name == R.string.package_name


def test_main_uses_logger_handler():
    with mock.patch('gfworkflow.__main__.logger_handler') as logger_handler_:
        with mock.patch('gfworkflow.__main__._create_file_handler') as _create_file_handler_:
            _create_file_handler_.return_value = logging.NullHandler
            main()
        logger_handler_.assert_called_once()


def test_clear_log():
    clear_log()
    assert not R.path.log_file.exists()


def test_dump_existing_log(tmp_path: Path):
    with logger_handler(logger, _create_file_handler()):
        dump_log(tmp_path)
    dumped_log_file: Path = tmp_path / R.string.log_file_name
    assert dumped_log_file.exists()


def test_dump_non_existing_log(tmp_path: Path):
    clear_log()
    dump_log(tmp_path)
