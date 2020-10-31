import gfworkflow.base_resources as base


class string(base.string):
    pass


class path(base.path):
    pass


class param(base.param):
    init = '--init'
    init_help = 'init git flow'
    pass
