from unittest import mock

from gfworkflow.cli.api import clear_log_method


def test_clear_log_method_calls_clear_log():
    with mock.patch('gfworkflow.clear_log') as _clear_log:
        clear_log_method()
        _clear_log.assert_called_once()
