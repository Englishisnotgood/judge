import os
from dmoj.executors.base_executor import reversion, version_cache
from dmoj.executors.python_executor import PythonExecutor


class Executor(PythonExecutor):
    command = 'pypy'
    test_program = "print __import__('sys').stdin.read()"
    name = 'PYPY'

    if os.name != 'nt':
        from dmoj.cptbox.handlers import ACCESS_DENIED
        syscalls = [('unlink', ACCESS_DENIED)]

    @classmethod
    def parse_version(cls, command, output):
        try:
            cls._pypy_versions = [tuple(map(int, version.split('.'))) for version in reversion.findall(output)]
            return cls._pypy_versions[1]
        except:
            return None

    @classmethod
    def get_runtime_versions(cls):
        # A little hack to report implemented Python version too
        return tuple(list(super(Executor, cls).get_runtime_versions()) +
                     [('implementing python', cls._pypy_versions[0])])
