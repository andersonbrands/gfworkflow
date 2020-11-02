from gfworkflow import core
from gfworkflow.cli import api


def test_complete_flow(tmp_path_as_cwd):
    core.run('git init .')
    api.init_method()
    core.run('git flow feature start bump-config')
    assert 'feature/bump-config' == core.get_current_branch_name()
    config = tmp_path_as_cwd / '.bumpversion.cfg'
    config.write_text('[bumpversion]\n'
                      'current_version = 0.0.0\n'
                      'commit = True\n')
    core.run('git add .')
    core.run('git commit -m "-"')
    core.run('git flow feature finish')

    part = 'minor'
    api.start_release_method(part)
    assert 'release/0.1.0' == core.get_current_branch_name()
    after_bump = config.read_text().replace('0.0.0', '0.1.0')
    api.bump_version_method(part)
    assert after_bump == config.read_text()
    api.finish_release_method()
    assert 'develop' == core.get_current_branch_name()
