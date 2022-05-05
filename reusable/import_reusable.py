from types import ModuleType

from helpers import call_pycode_method


class ReusableNotFound(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


def import_reusable(name):
    response = call_pycode_method('get_reusable', dict(name=name))

    if not response.ok:
        raise ReusableNotFound(name)

    import reusable
    code = response.json()['code']
    module = ModuleType(name)
    module_env = module.__dict__
    module_env.update(pycode=reusable)
    exec(code, module_env)
    return module
