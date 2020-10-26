import os
from pathlib import Path

import pytest


@pytest.fixture
def tmp_path_as_cwd(tmp_path: Path):
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        yield
    finally:
        os.chdir(cwd)
