import argparse
import logging
from pathlib import Path
from typing import List
from unittest import mock
from unittest.mock import Mock

import pytest

from gfworkflow import R, logger
from gfworkflow.cli import Args, _cli_callable_from_params, cli
from gfworkflow.cli.api import version_method, clear_log_method, dump_log_method, init_method


def test_unrecognized_arguments_raises_system_exit():
    with pytest.raises(SystemExit):
        Args(['--foo'])


@pytest.mark.parametrize('params', [
    ['--version'],
    ['--dump-log', '.'],
    ['--clear-log'],
    ['--init']
])
def test_expected_params(params: List[str]):
    assert Args(params)


def test_args_dump_log_is_not_none_when_dump_log_dir_in_args_list():
    params = ['--dump-log', '.']
    assert Args(params).dump_log is not None


def test_args_dump_log_defaults_to_cwd():
    cwd: Path = Path()
    params = ['--dump-log']
    assert Args(params).dump_log == cwd


def test_non_existing_dir_raises_argument_type_error(tmp_path_as_cwd):
    with pytest.raises(SystemExit), pytest.raises(argparse.ArgumentTypeError):
        params = ['--dump-log', 'non_existing_dir']
        Args(params)


@pytest.mark.parametrize(
    'params, param_property', (
        (['--version'], Args.version),
        (['--clear-log'], Args.clear_log),
        (['--init'], Args.init),
    )
)
def test_args_boolean_param_property_is_true_when_param_in_args_list(params, param_property):
    assert param_property.getter(Args(params))


def test_args_version_is_false_when_version_is_not_in_args_list():
    assert not Args([]).version


@pytest.mark.parametrize(
    'params, api_method', (
            (['--version'], version_method),
            (['--clear-log'], clear_log_method),
            (['--dump-log'], dump_log_method),
            (['--init'], init_method),
    )
)
def test_cli_with_param_returns_cli_api_method(params, api_method):
    callable_ = _cli_callable_from_params(params)
    assert api_method == callable_ or api_method == callable_.func


def test_cli_callable_from_params_with_no_param_returns_working_callable():
    _cli_callable_from_params()()


def test_cli_calls_cli_callable_from_params():
    with mock.patch('gfworkflow.cli._cli_callable_from_params') as cli_callable:
        cli()
        cli_callable.assert_called_once()


def test_cli_calls_cli_callable_from_params_result():
    with mock.patch('gfworkflow.cli._cli_callable_from_params') as cli_callable:
        cli_callable_result = Mock()
        cli_callable.return_value = cli_callable_result
        cli()
        cli_callable_result.assert_called_once()


def test_cli_logger_name_matches_package_name():
    assert logger.name == R.string.package_name


def test_cli_adds_console_handler_to_logger():
    cli()
    assert logging.StreamHandler in map(type, logger.handlers)
