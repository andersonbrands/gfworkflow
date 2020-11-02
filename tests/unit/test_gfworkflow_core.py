import sys
from unittest import mock
from unittest.mock import MagicMock, call

import pytest

from gfworkflow import core
from gfworkflow.exceptions import RunCommandException


def test_run_valid_command():
    assert 0 == core.run([sys.executable, '-V']).returncode


def test_run_command_output():
    assert 'python' in core.run([sys.executable, '-V']).stdout.lower()


def test_run_command_with_invalid_option():
    with pytest.raises(RunCommandException):
        core.run([sys.executable, '--invalid-option'])


def test_run_invalid_command():
    with pytest.raises(FileNotFoundError):
        core.run(['invalid-command'])


def test_init():
    with mock.patch('gfworkflow.core.run') as r:
        r: MagicMock
        core.init()
        calls = [call('git flow init -d -f'), call('git config gitflow.prefix.versiontag v')]
        r.assert_has_calls(calls)


def test_bump_version():
    with mock.patch('gfworkflow.core.run') as r:
        r: MagicMock
        core.bump_version('minor')
        r.assert_called_with('bumpversion minor')


def test_start_release():
    with mock.patch('gfworkflow.core.run') as r:
        r: MagicMock
        core.start_release('1.0.0')
        r.assert_called_with('git flow release start 1.0.0')


def test_get_new_version_with_config_file(tmp_path_as_cwd):
    config = tmp_path_as_cwd / '.bumpversion.cfg'
    config.write_text('[bumpversion]\ncurrent_version = 0.0.0')
    assert '0.1.0' == core.get_new_version('minor')


def test_get_new_version_without_config_file_raises_run_command_exception(tmp_path_as_cwd):
    with pytest.raises(RunCommandException):
        assert '0.1.0' == core.get_new_version('minor')


def test_get_current_branch_name(tmp_path_as_cwd):
    core.run('git init .')
    (tmp_path_as_cwd / 'add.txt').write_text('add')
    core.run('git add add.txt')
    core.run('git commit -m "Add"')
    core.run('git checkout -b develop')
    assert 'develop' == core.get_current_branch_name()


def test_finish_release():
    with mock.patch('gfworkflow.core.run') as run:
        run: MagicMock
        core.finish_release('0.0.0')
        run.assert_called_once_with('git flow release finish -m " - " 0.0.0')
