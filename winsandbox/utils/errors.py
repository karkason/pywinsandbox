_WINDOWS_SANDBOX_ARTICLE_LINK = "https://techcommunity.microsoft.com/t5/windows-kernel-internals/windows-sandbox" \
                                "/ba-p/301849"


class SandboxFeatureIsNotAvailableError(RuntimeError):
    """
    Raised when failed getting any information about the windows sandbox feature.
    """
    def __init__(self):
        super(SandboxFeatureIsNotAvailableError, self).__init__(
            'Could not find the windows sandbox feature on this computer.\n'
            'Please visit "{}"\n'
            'for prerequisites for using this feature.'.format(_WINDOWS_SANDBOX_ARTICLE_LINK))


class SandboxFeatureIsNotEnabledError(RuntimeError):
    def __init__(self):
        """
        Raised when the windows sandbox is available on the computer but isn't enabled.
        """
        super(SandboxFeatureIsNotEnabledError, self).__init__(
            'The optional feature of windows sandbox is not enabled!\n'
            'Please visit "{}"\n'
            'for information  on how to enable it.'.format(_WINDOWS_SANDBOX_ARTICLE_LINK))
