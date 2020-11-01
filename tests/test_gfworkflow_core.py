import sys
from unittest import mock
from unittest.mock import MagicMock, call

import pytest

from gfworkflow.core import run, init, bump_version, start_release, get_new_version
from gfworkflow.exceptions import RunCommandException


def test_run_valid_command():
    assert 0 == run([sys.executable, '-V']).returncode


def test_run_command_output():
    assert 'python' in run([sys.executable, '-V']).stdout.lower()


def test_run_command_with_invalid_option():
    with pytest.raises(RunCommandException):
        run([sys.executable, '--invalid-option'])


def test_run_invalid_command():
    with pytest.raises(FileNotFoundError):
        run(['invalid-command'])


def test_init():
    with mock.patch('gfworkflow.core.run') as r:
        r: MagicMock
        init()
        calls = [call('git flow init -d -f'), call('git config gitflow.prefix.versiontag v')]
        r.assert_has_calls(calls)


def test_bump_version():
    with mock.patch('gfworkflow.core.run') as r:
        r: MagicMock
        bump_version('minor')
        r.assert_called_with('bumpversion minor')


def test_start_release():
    with mock.patch('gfworkflow.core.run') as r:
        r: MagicMock
        start_release('1.0.0')
        r.assert_called_with('git flow release start 1.0.0')


def test_get_new_version_with_config_file(tmp_path_as_cwd):
    config = tmp_path_as_cwd / '.bumpversion.cfg'
    config.write_text('[bumpversion]\ncurrent_version = 0.0.0')
    assert '0.1.0' == get_new_version('minor')


def test_get_new_version_without_config_file_raises_run_command_exception(tmp_path_as_cwd):
    with pytest.raises(RunCommandException):
        assert '0.1.0' == get_new_version('minor')
