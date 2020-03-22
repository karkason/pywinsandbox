import tempfile
import pathlib
from ..config import generate_config_file

WINDOWS_SANDBOX_CONFIG_FILE_SUFFIX = '.wsb'


class OfflineSession:
    def __init__(self, sandbox):
        self.sandbox = sandbox

    def run(self):
        config_file = generate_config_file(self.sandbox.config)

        # And start the sandbox.
        with tempfile.NamedTemporaryFile() as temp:
            config_file_path = pathlib.Path(temp.name).with_suffix(WINDOWS_SANDBOX_CONFIG_FILE_SUFFIX)
            config_file_path.write_text(config_file)
            self.sandbox.start_sandbox(str(config_file_path))
