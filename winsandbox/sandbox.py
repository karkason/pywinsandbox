from .folder_mapper import PythonMapper
from .instance import SandboxInstance

from collections import namedtuple
from warnings import warn_explicit

_DEFAULT_FOLDER_MAPPERS = [PythonMapper()]
SandboxConfig = namedtuple("SandboxConfig", ['folder_mappers', 'networking', 'logon_script', 'virtual_gpu'])


def new_sandbox(folder_mappers=None, networking=True, logon_script="", virtual_gpu=True):
    """
    Create a new sandbox or connect to an existing running instance.
    """

    if networking and len(logon_script) != 0:
        warn_explicit("Logon scripts are ignored when the sandbox has networking enabled.")

    folder_mappers = folder_mappers or []
    folder_mappers.extend(_DEFAULT_FOLDER_MAPPERS)

    return SandboxInstance(config=SandboxConfig(folder_mappers=folder_mappers,
                                                networking=networking,
                                                logon_script=logon_script,
                                                virtual_gpu=virtual_gpu))


def connect_to_sandbox():
    """
    Connect to an existing running sandbox.
    """

    return SandboxInstance(config=SandboxConfig(folder_mappers=None,
                                                networking=True,
                                                logon_script="",
                                                virtual_gpu=True),
                           launch_new_instance_if_needed=False)
