from .utils.sandbox_feature_state import verify_sandbox_feature_is_enabled
from .folder_mapper import PythonMapper
from .sandbox import OnlineSandbox, OfflineSandbox
from .config import SandboxConfig

_DEFAULT_FOLDER_MAPPERS = [PythonMapper()]


def new_sandbox(folder_mappers=None, networking=True, logon_script="", virtual_gpu=True):
    """
    Create a new sandbox or connect to an existing running instance.
    When networking=False:
    - Boots up a windows sandbox with the requested configuration.

    When networking=True:
    - Boots a sandbox with python mapped to it
    - Starts an RPyC server
    - Returns an OnlineSandbox instance with a `.rpyc` property.
    """

    folder_mappers = folder_mappers or []
    folder_mappers.extend(_DEFAULT_FOLDER_MAPPERS)

    config = SandboxConfig(folder_mappers=folder_mappers,
                           networking=networking,
                           logon_script=logon_script,
                           virtual_gpu=virtual_gpu)
    if networking:
        return OnlineSandbox(config)
    else:
        return OfflineSandbox(config)


def connect_to_sandbox():
    """
    Connect to an existing running sandbox which was created with `new_sandbox(networking=True)`.
    It connects to the already running RPyC server in the sandbox.
    """

    config = SandboxConfig(folder_mappers=[],
                           networking=True,
                           logon_script="",
                           virtual_gpu=True)
    return OnlineSandbox(config, launch_new_instance=False)


# Do not allow importing if the feature isn't enabled
verify_sandbox_feature_is_enabled()
