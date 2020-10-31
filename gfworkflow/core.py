import subprocess
from typing import Union, List


def run(command: Union[str, List[str]]):
    return subprocess.run(command)


def init():
    run('git flow init -d -f')
    run('git config gitflow.prefix.versiontag v')


def bump_version(part: str):
    run(f'bumpversion {part}')
