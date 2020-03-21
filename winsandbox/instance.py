from .config.config_genereator import generate_config_file
from .session import connector

import copy
import subprocess
import cached_property
import rpyc


class SandboxInstance:
    def __init__(self, config, launch_new_instance_if_needed=True):
        self.config = config
        self._connection_tuple = connector.get_connector(self).connect(launch_new_instance_if_needed)

    def generate_config_file(self,
                             logon_script,
                             extra_folder_mappers):
        folder_mappers = copy.copy(self.config.folder_mappers)
        folder_mappers.extend(extra_folder_mappers)

        config_xml = generate_config_file(self.config.virtual_gpu,
                                          self.config.networking,
                                          folder_mappers,
                                          logon_script)

        return config_xml

    @staticmethod
    def start_sandbox(config_file_path):
        subprocess.Popen(['start', config_file_path],
                         shell=True)

    @cached_property.cached_property
    def rpyc(self):
        assert self.config.networking, "Networking is not enabled in this Sandbox."

        if self._connection_tuple is not None:
            return rpyc.classic.connect(*self._connection_tuple)
