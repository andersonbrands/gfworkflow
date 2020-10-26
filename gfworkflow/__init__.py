import logging
import shutil
from pathlib import Path
from typing import Union

from gfworkflow import R

logger: logging.Logger = logging.getLogger(R.string.package_name)
logger.setLevel(logging.DEBUG)


def clear_log():
    file_handlers = (
        tuple(filter(lambda x: isinstance(x, logging.FileHandler), logger.handlers))
    )
    if len(file_handlers) == 1:
        file_handlers[0].close()
        R.path.log_file.unlink(missing_ok=True)


def dump_log(dst: Union[str, Path]):
    logger.info(f'Dumping log file at: {dst}')
    shutil.copy2(R.path.log_file, dst)
