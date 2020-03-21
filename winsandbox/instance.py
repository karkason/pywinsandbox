from .utils.file import watch_file
from .utils.path import shared_folder_path_in_sandbox
from .utils import dev_environment

from .folder_mapper import PythonMapper, FolderMapper
from .config.config_genereator import generate_config_file

import multiprocessing.connection
import copy
import subprocess
import tempfile

try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib

WINDOWS_SANDBOX_CONFIG_FILE_SUFFIX = '.wsb'
SHARED_ADDRESS_FILE_NAME = 'shared_address_file'


class SandboxInstance:
    def __init__(self, sandbox_config):
        self.sandbox_config = sandbox_config
        self.connection = self._run()

    def _generate_config_file(self,
                              logon_script,
                              extra_folder_mappers,
                              path=None):
        folder_mappers = copy.copy(self.sandbox_config.folder_mappers)
        folder_mappers.extend(extra_folder_mappers)

        config_xml = generate_config_file(self.sandbox_config.virtual_gpu,
                                          self.sandbox_config.networking,
                                          folder_mappers,
                                          logon_script)

        if path is not None:
            path = pathlib.Path(path).with_suffix(WINDOWS_SANDBOX_CONFIG_FILE_SUFFIX)
            path.write_text(config_xml)

        return config_xml

    def _connect_to_sandbox(self, server_address_path, timeout=60):
        if watch_file(str(server_address_path), timeout=timeout):
            address, port = server_address_path.read_text().split(':')
        else:
            raise RuntimeError("Sandbox server didn't startup")

        connection = multiprocessing.connection.Client((address, int(port)), authkey=b'handshake')
        return connection

    def _get_logon_script(self, server_address_path):
        if not self.sandbox_config.networking:
            return self.sandbox_config.logon_script

        # Launch the target script.
        networking_logon_script = '"{}" -m winsandbox.target {}'.format(
            shared_folder_path_in_sandbox(PythonMapper().path()) / 'python.exe',
            str(server_address_path))

        if dev_environment.is_dev_environment():
            print("wat")
            # If we're in a dev environment we create the directory chain up to the egglink,
            # and then symlink the egglink to the mapped shared folder path.
            networking_logon_script = 'cmd /c mkdir {} & mklink /D {} {} & {}'.format(
                dev_environment.get_egglink_path().parent,
                dev_environment.get_egglink_path(),
                shared_folder_path_in_sandbox(dev_environment.get_egglink_path()),
                networking_logon_script
            )

        print(networking_logon_script)
        return networking_logon_script

    def _run(self):
        shared_directory = tempfile.mkdtemp(prefix='shared_dir')
        server_address_path = pathlib.Path(shared_directory) / 'server_address'
        server_address_path_in_sandbox = shared_folder_path_in_sandbox(shared_directory) / 'server_address'

        extra_folder_mappers = [FolderMapper(shared_directory, read_only=False)]

        if dev_environment.is_dev_environment():
            # Let's map the egg link to the sandbox if we're in a dev environment.
            extra_folder_mappers.append(FolderMapper(dev_environment.get_egglink_path()))

        with tempfile.NamedTemporaryFile() as temp:
            config_file_path = pathlib.Path(temp.name).with_suffix(WINDOWS_SANDBOX_CONFIG_FILE_SUFFIX)
            print(self._generate_config_file(path=config_file_path,
                                             extra_folder_mappers=extra_folder_mappers,
                                             logon_script=self._get_logon_script(server_address_path_in_sandbox)))

            self.sandbox_process = subprocess.Popen(['start', str(config_file_path)],
                                                    shell=True)

            if self.sandbox_process.poll() is not None:
                raise RuntimeError("Sandbox exited")

        if self.sandbox_config.networking:
            return self._connect_to_sandbox(server_address_path)
