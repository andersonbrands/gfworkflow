from functools import partial
from unittest import mock

import pytest

from gfworkflow.cli.api import clear_log_method, dump_log_method, init_method, bump_version_method


@pytest.mark.parametrize(
    'api_method, matching_method', (
            (clear_log_method, 'gfworkflow.clear_log'),
            (partial(dump_log_method, '.'), 'gfworkflow.dump_log'),
            (init_method, 'gfworkflow.core.init'),
            (partial(bump_version_method, 'minor'), 'gfworkflow.core.bump_version'),
    )
)
def test_api_method_calls_matching_method(api_method, matching_method):
    with mock.patch(matching_method) as _patched:
        api_method()
        _patched.assert_called_once()
