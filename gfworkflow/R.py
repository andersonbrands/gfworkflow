import gfworkflow.base_resources as base


class string(base.string):
    pass


class path(base.path):
    pass


class param(base.param):
    init = '--init'
    init_help = 'init git flow'
    bump_version = '--bump-version'
    bump_version_help = 'bumps version'
    start_release = '--start-release'
    start_release_help = 'starts a release'
    pass
