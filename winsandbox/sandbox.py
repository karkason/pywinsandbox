from .config.config_genereator import generate_config_file
from .session import offline_session, online_session

import copy
import subprocess
import cached_property
import rpyc
from warnings import warn_explicit


class OfflineSandbox:
    def __init__(self, config):
        self.config = config
        offline_session.OfflineSession(self).run()

    @staticmethod
    def start_sandbox(config_file_path):
        subprocess.Popen(['start', config_file_path],
                         shell=True)


class OnlineSandbox:
    def __init__(self, config, launch_new_instance=True):
        self.config = config

        assert config.networking, "Networking not configured with an online sandbox."
        if len(self.config.logon_script) != 0:
            warn_explicit("Logon scripts are ignored when the sandbox has networking enabled.")

        session = online_session.OnlineSession(self)

        # Try to connect to an already running server.
        self._connection_tuple = session.running_sandbox_server_information(launch_new_instance)

        # Server is down, let's boot the sandbox.
        if self._connection_tuple is None:
            session.configure_sandbox()
            OfflineSandbox(self.config)

        # And get the new sandbox connection tuple.
        self._connection_tuple = session.connect_to_sandbox()

    @cached_property.cached_property
    def rpyc(self):
        assert self.config.networking, "Networking is not enabled in this Sandbox."

        if self._connection_tuple is not None:
            return rpyc.classic.connect(*self._connection_tuple)
