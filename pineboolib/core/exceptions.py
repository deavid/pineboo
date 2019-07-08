class CodeDoesNotBelongHereException(Exception):
    """The code calling here is just wrong. This object should be unaware of this concept. Please look for other places to code this.
    Please don't code anything related to fllegacy/dgi here.
    """


class NotConnectedError(Exception):
    """Code expected a connection to be made already but it wasn't"""


class ForbiddenError(Exception):
    """Action attempted is not allowed"""
