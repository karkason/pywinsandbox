"""
This script is part of a Windows Shell Extension that allows you to run executable files
in a sandboxed environment using the right click menu.
Note that the script maps the entire parent directory of the executable,
this is done in order to preserve potential local dependencies.
"""

import sys
import argparse
import pathlib

import winsandbox


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("executable", help="The executable path to run sandboxed")
    parser.add_argument("--network", default=False, action="store_true", help="Enable networking in the sandbox")
    parser.add_argument("--run", default=False, action="store_true", help="Run the executable inside the sandbox")

    return parser.parse_args()


def main():
    args = read_args()

    executable = pathlib.PurePath(args.executable)

    # Map executable folder to sandbox
    mapper = winsandbox.FolderMapper(folder_path=executable.parent, read_only=True)
    sandbox_mapped_dir = pathlib.PurePath(r'C:\Users\WDAGUtilityAccount\Desktop') / executable.parent.name

    if args.run:
        # Run the executable
        command = '{}'.format(sandbox_mapped_dir / executable.name)
    else:
        # Only open mapped folder
        command = 'explorer {}'.format(sandbox_mapped_dir)

    # Launch the sandbox
    winsandbox.new_sandbox(networking=args.network, logon_script=command, folder_mappers=[mapper])


if __name__ == '__main__':
    main()
