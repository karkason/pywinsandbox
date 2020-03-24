import argparse
from IPython import embed
from traitlets.config import get_config

import winsandbox


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interactive", default=False, action="store_true",
                        help="Interactive mode with a `sandbox` instance available. Embeds an IPython shell.")
    parser.add_argument("--no-vgpu", default=False, action="store_true", help="Disable the virtual GPU.")
    parser.add_argument("-s", "--logon-script", required=False,
                        help="Logon script for non-interactive (ipy) sandbox.", default="")
    parser.add_argument("-f", "--folder", action="append",
                        help="Folders to map to the sandbox.", default=[])
    args = parser.parse_args()

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
