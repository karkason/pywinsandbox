import tempfile
import pathlib

WINDOWS_SANDBOX_CONFIG_FILE_SUFFIX = '.wsb'


class NoNetworkConnector:
    def __init__(self, sandbox_instance):
        self.instance = sandbox_instance

    def connect(self, logon_script=None, extra_folder_mappers=None):
        logon_script = logon_script or self.instance.sandbox_config.logon_script
        extra_folder_mappers = extra_folder_mappers or []

        config_file = self.instance.generate_config_file(logon_script=logon_script,
                                                         extra_folder_mappers=extra_folder_mappers)

        # And start the sandbox.
        with tempfile.NamedTemporaryFile() as temp:
            config_file_path = pathlib.Path(temp.name).with_suffix(WINDOWS_SANDBOX_CONFIG_FILE_SUFFIX)
            config_file_path.write_text(config_file)
            self.instance.start_sandbox(str(config_file_path))
