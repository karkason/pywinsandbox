import wmi
import os

from .errors import SandboxFeatureIsNotAvailableError

_WINDOWS_SANDBOX_FEATURE_NAME = 'Containers-DisposableClientVM'
_ENABLED_STATE = 1


def is_sandbox_feature_enabled():
    """
    Checks whether or not the optional feature of windows sandboxes is enabled.
    """
    if "PYTEST_CURRENT_TEST" in os.environ:
        # We are running under pytest, always enable importing the library.
        return

    wmi_client = wmi.WMI()
    matching_features = wmi_client.Win32_OptionalFeature(Name=_WINDOWS_SANDBOX_FEATURE_NAME)
    if not matching_features:
        raise SandboxFeatureIsNotAvailableError()

    assert len(matching_features) == 1  # Make sure that there isn't any funny business and there's only 1 feature.
    sandbox_feature = matching_features[0]
    return sandbox_feature.InstallState == _ENABLED_STATE
