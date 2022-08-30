import sys


def is_inside_venv():
    return sys.prefix != sys.base_prefix
