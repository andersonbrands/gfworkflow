import logging
from functools import partial
from typing import List

from gfworkflow import logger
from gfworkflow.cli import api
from gfworkflow.cli._arg_parse import Args


def _cli_callable_from_params(params: List[str] = None) -> callable:
    args: Args = Args(params)

    if args.version:
        return api.version_method

    if args.clear_log:
        return api.clear_log_method

    if args.dump_log:
        return partial(api.dump_log_method, args.dump_log)

    return lambda: None


def _create_console_handler() -> logging.Handler:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    return console_handler


def cli(params: List[str] = None):
    logger.addHandler(_create_console_handler())
    cli_callable: callable = _cli_callable_from_params(params)
    cli_callable()
    pass