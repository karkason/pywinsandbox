import sys
import os
import argparse
import winreg
import pathlib

from IPython import embed
from traitlets.config import get_config

import winsandbox


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interactive", default=False, action="store_true",
                        help="Interactive mode with a `sandbox` instance available. Embeds an IPython shell.")
    parser.add_argument("--no-vgpu", default=False, action="store_true", help="Disable the virtual GPU.")
    parser.add_argument("-s", "--logon-script", required=False,
                        help="Logon script for non-interactive (ipy) sandbox.", default="")
    parser.add_argument("-f", "--folder", action="append",
                        help="Folders to map to the sandbox.", default=[])

    parser.add_argument("-r", "--register", default=False, action="store_true", 
                        help="Register a Shell extension that allows opening executable files in the sandbox")
    parser.add_argument("-u", "--unregister", default=False, action="store_true", 
                        help="Unregister the Shell extension")

    return parser.parse_args()


def register_shell_extension():
    key = winreg.CreateKeyEx(winreg.HKEY_CLASSES_ROOT, r'exefile\shell\Open Sandboxed')

    # Calculate paths
    repo_root_dir = pathlib.Path(__file__).absolute().parent.parent
    shell_script_path = repo_root_dir / 'shell-extension' / 'open_sandboxed.py'
    icon_path = repo_root_dir / 'shell-extension' / 'sandbox.ico'

    # Set icon
    winreg.SetValueEx(key, 'Icon', 0, winreg.REG_SZ, str(icon_path))

    # Set shell script command
    command_key = winreg.CreateKeyEx(key, 'Command')
    command = '{} {} %1'.format(sys.executable, shell_script_path)
    winreg.SetValue(command_key, None, winreg.REG_SZ, command)

    print("Registered the shell extension successfully!")


def unregister_shell_extension():
    try:
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r'exefile\shell\Open Sandboxed\Command')
    except FileNotFoundError:
        print("Shell extension is not registered")
        return

    winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r'exefile\shell\Open Sandboxed')

    print("Unregistered the shell extension successfully!")


def main():

    args = read_args()

    # Handle shell extension commands
    try:
        if args.register:
            register_shell_extension()
            return
        elif args.unregister:
            unregister_shell_extension()
            return
    except PermissionError:
        print("Try running again as an Administrator")
        return

    # Launch a new sandbox
    sandbox = winsandbox.new_sandbox(networking=args.interactive,
                                     virtual_gpu=not args.no_vgpu,
                                     logon_script=args.logon_script,
                                     folder_mappers=[winsandbox.FolderMapper(folder_path=folder, read_only=False)
                                                     for folder in args.folder])

    if args.interactive:
        config = get_config()
        config.InteractiveShellEmbed.colors = "Neutral"  # Workaround to enable colors in embedded IPy.

        embed(config=config,
              header='Welcome to the Windows Sandbox!\nUse the `sandbox` object to control the sandbox.')


if __name__ == '__main__':
    main()
