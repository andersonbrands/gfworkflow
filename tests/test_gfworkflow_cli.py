import argparse
from pathlib import Path
from typing import Any
from unittest import mock
from unittest.mock import Mock

import pytest

from gfworkflow import R, logger
from gfworkflow.cli import Args, _cli_callable_from_params, cli, api


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


def test_cli_uses_logger_handler():
    with mock.patch('gfworkflow.cli.logger_handler') as logger_handler_:
        cli()
        logger_handler_.assert_called_once()


class TestArgs:
    test_data = [
        (['--version'], Args.version, api.version_method),
        (['--clear-log'], Args.clear_log, api.clear_log_method),
        (['--dump-log', '.'], Args.dump_log, api.dump_log_method),
        (['--init'], Args.init, api.init_method),
        (['--bump-version', 'minor'], Args.bump_version, api.bump_version_method),
        (['--start-release', 'minor'], Args.start_release, api.start_release_method),
    ]

    @pytest.mark.parametrize('params', map(lambda x: x[0], test_data))
    def test_expected_params(self, params):
        assert Args(params)

    @pytest.mark.parametrize('params, param_property', map(lambda x: x[0:2], test_data))
    def test_args_param_property_is_true_when_param_in_args_list(self, params, param_property):
        args: Any = Args(params)
        assert param_property.getter(args)

    @pytest.mark.parametrize('params, api_method', map(lambda x: (x[0], x[2]), test_data))
    def test_cli_with_param_returns_cli_api_method(self, params, api_method):
        callable_ = _cli_callable_from_params(params)
        assert api_method == callable_ or api_method == callable_.func

    def test_unrecognized_arguments_raises_system_exit(self):
        with pytest.raises(SystemExit):
            Args(['--foo'])

    def test_args_dump_log_is_not_none_when_dump_log_dir_in_args_list(self):
        params = ['--dump-log', '.']
        assert Args(params).dump_log is not None

    def test_args_dump_log_defaults_to_cwd(self):
        cwd: Path = Path()
        params = ['--dump-log']
        assert Args(params).dump_log == cwd

    def test_non_existing_dir_raises_argument_type_error(self, tmp_path_as_cwd):
        with pytest.raises(SystemExit), pytest.raises(argparse.ArgumentTypeError):
            params = ['--dump-log', 'non_existing_dir']
            Args(params)

    def test_args_version_is_false_when_version_is_not_in_args_list(self):
        assert not Args([]).version

    @pytest.mark.parametrize('params', map(lambda x: x[0], test_data))
    def test_cli_callable_from_params_returns_working_callable(self, params, tmp_path_as_cwd):
        cli_callable = Mock(_cli_callable_from_params(params))
        cli_callable()
        cli_callable.assert_called_with()
