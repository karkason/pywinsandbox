from .folder_mapper import PythonMapper as _PythonMapper
from .config_genereator import generate_config_file as _generate_config_file

import tempfile
import os
try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib

_DEFAULT_FOLDER_MAPPERS = [_PythonMapper()]
WINDOWS_SANDBOX_CONFIG_FILE_SUFFIX = '.wsb'


class WindowsSandbox:
    def __init__(self, folder_mappers=None, networking=True, logon_script="", virtual_gpu=True):
        self.folder_mappers = folder_mappers or []
        self.folder_mappers.extend(_DEFAULT_FOLDER_MAPPERS)

        self.networking = networking
        self.logon_script = logon_script
        self.virtual_gpu = virtual_gpu

    def generate_config_file(self, path=None):
        config_xml = _generate_config_file(self.virtual_gpu, self.networking, self.folder_mappers, self.logon_script)

        if path is not None:
            path = pathlib.Path(path).with_suffix(WINDOWS_SANDBOX_CONFIG_FILE_SUFFIX)
            path.write_text(config_xml)

        return config_xml

    def run(self):
        with tempfile.NamedTemporaryFile() as temp:
            config_file_path = pathlib.Path(temp.name).with_suffix(WINDOWS_SANDBOX_CONFIG_FILE_SUFFIX)
            self.generate_config_file(config_file_path)
            os.system(str(config_file_path))
