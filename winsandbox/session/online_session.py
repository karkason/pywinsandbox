from ..utils.file import wait_for_file_creation
from ..utils.path import shared_folder_path_in_sandbox
from ..utils import dev_environment
from ..utils import venv

from ..folder_mapper import PythonMapper, FolderMapper, PythonUserSitePackagesMapper
from .. import target

import tempfile
import pathlib
import socket
import os
import sys


class ServerNotResponding(Exception):
    pass


def _is_server_responding(address, port):
    try:
        socket.create_connection((address, port), timeout=3).close()
        return True
    except socket.error:
        return False


def _get_shared_directory():
    shared_directory = pathlib.Path(tempfile.gettempdir()) / 'shared_windows_sandbox_dir'
    if not shared_directory.exists():
        shared_directory.mkdir()

    return shared_directory


class OnlineSession:
    def __init__(self, sandbox):
        self.sandbox = sandbox
        self.shared_directory = _get_shared_directory()
        self.server_address_path = pathlib.Path(self.shared_directory) / 'server_address'
        self.server_address_path_in_sandbox = shared_folder_path_in_sandbox(self.shared_directory) / 'server_address'

    def _get_logon_script(self, server_address_path):
        commands = []

        if dev_environment.is_dev_environment():
            # If we're in a dev environment we create the intermediate directory up to the egglink,
            # and then symlink the egglink to the mapped shared folder path.

            if dev_environment.get_egglink_path().drive != 'C:':
                # Handle this bizarre case by mapping a virtual drive from the actual drive letter to C:.
                # We'll then symlink the real development path to the shared folder on the desktop.
                commands.append('subst {} C:\\'.format(dev_environment.get_egglink_path().drive))

            commands.append('mkdir {}'.format(dev_environment.get_egglink_path().parent))

            commands.append('mklink /D {} {}'.format(
                dev_environment.get_egglink_path(),
                shared_folder_path_in_sandbox(dev_environment.get_egglink_path())))

        if venv.is_inside_venv():
            # If we're running in a virtual-environment we need to create a symlink between the
            # mapped base_prefix (shared folder path) and the path that the venv expects
            # the Python installation to be in.
            commands.append('mklink /D "{}" "{}"'.format(
                sys.base_prefix,
                shared_folder_path_in_sandbox(sys.base_prefix)))

        local_target_script_path = target.__file__
        remote_target_script_path = local_target_script_path.replace(str(PythonMapper().path()), str(
            shared_folder_path_in_sandbox(PythonMapper().path())))

        remote_python_path = sys.executable.replace(str(PythonMapper().path()), str(
            shared_folder_path_in_sandbox(PythonMapper().path())))

        user_site_path = PythonUserSitePackagesMapper().path()
        if user_site_path.exists():
            remote_user_site_packages_path = shared_folder_path_in_sandbox(user_site_path)
        else:
            remote_user_site_packages_path = ''

        # Launch the target script.
        commands.append(r'{} {} --disable-firewall {} {}'.format(
            remote_python_path,
            remote_target_script_path,
            str(server_address_path),
            remote_user_site_packages_path))
        print(commands[-1])

        return 'cmd.exe /c "{}"'.format(' && '.join(commands))

    def running_sandbox_server_information(self, allow_new_instance=False):
        """
        Get currently running server information (connection tuple).
        """
        try:
            # Try to connect to an already available targets.
            return self.connect_to_sandbox(timeout=0)
        except (ServerNotResponding, FileNotFoundError):
            # Server doesn't respond or a the connection data file doesn't exist.
            # We'll remove the connection data file and proceed.
            try:
                os.remove(str(self.server_address_path))
            except FileNotFoundError:
                pass

            if not allow_new_instance:
                raise ServerNotResponding("Sandbox is not currently running.")

    def configure_sandbox(self):
        """
        Configures the sandbox for a new online session.
        """

        extra_folder_mappers = [FolderMapper(self.shared_directory, read_only=False)]
        if dev_environment.is_dev_environment():
            # Let's map the egg link to the sandbox if we're in a dev environment.
            extra_folder_mappers.append(FolderMapper(dev_environment.get_egglink_path()))

        if venv.is_inside_venv():
            extra_folder_mappers.append(FolderMapper(sys.base_prefix))

        self.sandbox.config.logon_script = self._get_logon_script(self.server_address_path_in_sandbox)
        self.sandbox.config.folder_mappers.extend(extra_folder_mappers)

    def connect_to_sandbox(self, timeout=60):
        """
        Connect to the sandbox sever.
        Waits for the creation of the shared server address file, and checks that it responds.

        :returns: Connection tuple.
        """

        if wait_for_file_creation(str(self.server_address_path), timeout=timeout):
            address, port = self.server_address_path.read_text().split(':')
        else:
            raise FileNotFoundError("Sandbox server didn't startup")

        if not _is_server_responding(address, int(port)):
            raise ServerNotResponding()

        return address, int(port)
