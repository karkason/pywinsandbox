from ..utils.file import watch_file
from ..utils.path import shared_folder_path_in_sandbox
from ..utils import dev_environment

from ..folder_mapper import PythonMapper, FolderMapper
from .no_network_connector import NoNetworkConnector

import multiprocessing.connection
import tempfile
import pathlib
import socket
import os

WINDOWS_SANDBOX_CONFIG_FILE_SUFFIX = '.wsb'


class ServerNotResponding(Exception):
    pass


def _is_server_responding(address, port):
    try:
        socket.create_connection((address, port), timeout=3).close()
        return True
    except socket.error:
        return False


def _connect_to_sandbox(server_address_path, timeout=60):
    if watch_file(str(server_address_path), timeout=timeout):
        address, port = server_address_path.read_text().split(':')
    else:
        raise FileNotFoundError("Sandbox server didn't startup")

    if not _is_server_responding(address, int(port)):
        raise ServerNotResponding()

    connection = multiprocessing.connection.Client((address, int(port)), authkey=b'handshake')
    return connection


def _get_shared_directory():
    shared_directory = pathlib.Path(tempfile.gettempdir()) / 'shared_windows_sandbox_dir'
    if not shared_directory.exists():
        shared_directory.mkdir()

    return shared_directory


class NetworkedConnector:
    def __init__(self, sandbox_instance):
        self.instance = sandbox_instance
        assert self.instance.sandbox_config.networking, "Networking not configured with a networked connector."

    def _get_logon_script(self, server_address_path):
        # Launch the target script.
        networking_logon_script = '"{}" -m winsandbox.target {}'.format(
            shared_folder_path_in_sandbox(PythonMapper().path()) / 'python.exe',
            str(server_address_path))

        if dev_environment.is_dev_environment():
            # If we're in a dev environment we create the intermediate directory up to the egglink,
            # and then symlink the egglink to the mapped shared folder path.
            networking_logon_script = 'cmd /c mkdir {} & mklink /D {} {} & {}'.format(
                dev_environment.get_egglink_path().parent,
                dev_environment.get_egglink_path(),
                shared_folder_path_in_sandbox(dev_environment.get_egglink_path()),
                networking_logon_script
            )

        return networking_logon_script

    def connect(self):
        shared_directory = _get_shared_directory()
        server_address_path = pathlib.Path(shared_directory) / 'server_address'
        server_address_path_in_sandbox = shared_folder_path_in_sandbox(shared_directory) / 'server_address'

        try:
            # Try to connect to an already available target.
            return _connect_to_sandbox(server_address_path, timeout=0)
        except (ServerNotResponding, FileNotFoundError):
            # Server doesn't respond or a the connection data file doesn't exist.
            # We'll remove the connection data file and proceed.
            try:
                os.remove(str(server_address_path))
            except FileNotFoundError:
                pass

        extra_folder_mappers = [FolderMapper(shared_directory, read_only=False)]
        if dev_environment.is_dev_environment():
            # Let's map the egg link to the sandbox if we're in a dev environment.
            extra_folder_mappers.append(FolderMapper(dev_environment.get_egglink_path()))

        logon_script = self._get_logon_script(server_address_path_in_sandbox)

        # And start the sandbox.
        NoNetworkConnector(self.instance).connect(logon_script, extra_folder_mappers)

        if self.instance.sandbox_config.networking:
            return _connect_to_sandbox(server_address_path)
