from .folder_mapper import PythonMapper
from .instance import SandboxInstance

try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib

_DEFAULT_FOLDER_MAPPERS = [PythonMapper()]


class WindowsSandbox:
    def __init__(self, folder_mappers=None, networking=True, logon_script="", virtual_gpu=True):
        self.folder_mappers = folder_mappers or []
        self.folder_mappers.extend(_DEFAULT_FOLDER_MAPPERS)

        self.networking = networking
        self.logon_script = logon_script
        self.virtual_gpu = virtual_gpu

    def run(self):
        return SandboxInstance(sandbox_config=self)
