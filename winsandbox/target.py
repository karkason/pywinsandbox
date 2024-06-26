"""
This script is the RPyC server that is uploaded to the Windows Sandbox.
It boots up the server, writes the IP:port data to a shared file and starts accepting connections.
"""

import argparse
from pathlib import Path
import socket
import sys
import subprocess
import site
import os

WINDOWS_SANDBOX_DEFAULT_DESKTOP = Path(r'C:\Users\WDAGUtilityAccount\Desktop')


def enable_python_incoming_firewall():
    # Using `{sys.base_exec_prefix}\python.exe` instead of `sys.executable` to support venvs.
    for python_executable in ['python.exe', 'python3.exe']:
        subprocess.run(
            'netsh advfirewall firewall add rule name=AllowPythonServer '
            'dir=in action=allow enable=yes program="{}\\{}"'.format(Path(sys.base_exec_prefix).resolve(), python_executable),
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )


def get_ip_address():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("address_path",
                        type=lambda p: Path(p))
    parser.add_argument("custom_user_site_packages",
                        type=str,
                        default='',
                        nargs='?')
    parser.add_argument("--disable-firewall", '-f', default=False, action='store_true')
    args = parser.parse_args()

    if args.disable_firewall:
        enable_python_incoming_firewall()

    if args.custom_user_site_packages:
        site.addsitedir(args.custom_user_site_packages)

    import rpyc.utils.server

    server = rpyc.utils.server.ThreadedServer(rpyc.classic.ClassicService, port=0)

    Path(WINDOWS_SANDBOX_DEFAULT_DESKTOP / args.address_path).write_text('{}:{}'.format(get_ip_address(),
                                                                                        server.port))
    server.start()


if __name__ == '__main__':
    main()
