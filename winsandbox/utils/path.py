from pathlib import PureWindowsPath, Path

WINDOWS_SANDBOX_DEFAULT_DESKTOP = Path(PureWindowsPath(r'C:\Users\WDAGUtilityAccount\Desktop'))


def shared_folder_path_in_sandbox(local_path):
    local_path = Path(PureWindowsPath(local_path))
    if local_path.exists() and not local_path.is_dir():
        local_path = local_path.parent

    return WINDOWS_SANDBOX_DEFAULT_DESKTOP / local_path.name
