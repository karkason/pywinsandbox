import netifaces
import subprocess
import itertools


def get_adapter_name(guid):
    equals_separated = subprocess.check_output(
        'wmic path Win32_NetworkAdapter where GUID="{}" get NetConnectionID /format:value'.format(guid),
        stderr=subprocess.DEVNULL).strip()
    if len(equals_separated) == 0:
        return ''

    _, value = equals_separated.split(b'=', maxsplit=1)
    return value


def get_ipv4_addresses(guid):
    all_addresses = netifaces.ifaddresses(guid)
    nested_addresses = tuple(tuple(address_info['addr'] for address_info in data)
                             for if_type, data in all_addresses.items() if if_type == netifaces.AF_INET)

    return tuple(itertools.chain(*nested_addresses))


def get_adapter_addresses():
    all_interfaces_guid = netifaces.interfaces()

    return {get_adapter_name(guid): get_ipv4_addresses(guid) for guid in all_interfaces_guid}
