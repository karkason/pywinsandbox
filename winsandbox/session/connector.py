from . import target_connector, no_network_connector


def get_connector(instance):
    if instance.config.networking:
        return target_connector.NetworkedConnector(instance)
    else:
        return no_network_connector.NoNetworkConnector(instance)
