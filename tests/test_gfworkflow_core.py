import sys
from unittest import mock
from unittest.mock import MagicMock, call

import pytest

from gfworkflow.core import run, init, bump_version


def test_run_valid_command():
    assert 0 == run([sys.executable, '-V']).returncode


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
