from .launch import new_sandbox, connect_to_sandbox
from .folder_mapper import FolderMapper


def _verify_sandbox_feature_is_enabled():
    from .utils.sandbox_feature_state import is_sandbox_feature_enabled
    from .utils.errors import SandboxFeatureIsNotEnabledError

    if not is_sandbox_feature_enabled():
        raise SandboxFeatureIsNotEnabledError()


# Do not allow importing if the feature isn't enabled
_verify_sandbox_feature_is_enabled()
