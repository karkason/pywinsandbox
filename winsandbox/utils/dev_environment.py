import sys
import pathlib


def get_egglink_path():
    egg_link = pathlib.Path(sys.executable).parent / 'Lib' / 'site-packages' / 'pywinsandbox.egg-link'
    if egg_link.exists():
        return pathlib.Path(egg_link.read_text().splitlines()[0])

    return None


def is_dev_environment():
    return get_egglink_path() is not None
