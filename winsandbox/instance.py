from .config.config_genereator import generate_config_file
from .session import connector

import copy
import subprocess


class SandboxInstance:
    def __init__(self, sandbox_config):
        self.sandbox_config = sandbox_config
        self.connection = connector.get_connector(self).connect()

    def generate_config_file(self,
                             logon_script,
                             extra_folder_mappers):
        folder_mappers = copy.copy(self.sandbox_config.folder_mappers)
        folder_mappers.extend(extra_folder_mappers)

        config_xml = generate_config_file(self.sandbox_config.virtual_gpu,
                                          self.sandbox_config.networking,
                                          folder_mappers,
                                          logon_script)

        return config_xml

    def start_sandbox(self, config_file_path):
        subprocess.Popen(['start', config_file_path],
                         shell=True)
