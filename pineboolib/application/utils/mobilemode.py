"""
To detect if we are in mobile mode.
"""

MOBILE_MODE = None


def is_mobile_mode() -> bool:
    """
    Return if you are working in mobile mode.

    @return True or False
    """

    global MOBILE_MODE
    if MOBILE_MODE is None:
        MOBILE_MODE = check_mobile_mode()
    return MOBILE_MODE


def check_mobile_mode() -> bool:
    """
    Return if you are working in mobile mode, searching local settings or importing Android library.

    @return True or False.
    """

    from pineboolib.core.settings import config

    cfg_mobile = config.value(u"ebcomportamiento/mobileMode", None)
    if cfg_mobile is not None:
        return bool(cfg_mobile)

    try:
        import PyQt5.QtAndroidExtras  # type: ignore  # noqa   # FIXME

        return True
    except ImportError:
        return False
