try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib

WINDOWS_SANDBOX_DEFAULT_DESKTOP = pathlib.Path(r'C:\Users\WDAGUtilityAccount\Desktop')


def shared_folder_path_in_sandbox(local_path):
    local_path = pathlib.Path(local_path)
    if local_path.exists() and not local_path.is_dir():
        local_path = local_path.parent

    return WINDOWS_SANDBOX_DEFAULT_DESKTOP / local_path.name
