"""Replacement for Python logging that adds trace and other methods

It allows MyPy/PyType to properly keep track of the new message types
"""
import logging


CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
MESSAGE = 25  # NEW
INFO = 20
HINT = 18  # NEW
NOTICE = 15  # NEW
DEBUG = 10
TRACE = 5  # NEW
NOTSET = 0


class Logger(logging.Logger):
    def message(self, message, *args, **kwargs):
        self.log(MESSAGE, message, args, **kwargs)

    def hint(self, message, *args, **kwargs):
        self.log(HINT, message, args, **kwargs)

    def notice(self, message, *args, **kwargs):
        self.log(NOTICE, message, args, **kwargs)

    def trace(self, message, *args, **kwargs):
        self.log(TRACE, message, args, **kwargs)


logging.Logger.manager.loggerClass = Logger  # type: ignore


def getLogger(name=None) -> Logger:
    """
    Return a logger with the specified name, creating it if necessary.
    If no name is specified, return the root logger.
    """
    if name:
        return logging.Logger.manager.getLogger(name)  # type: ignore
    else:
        raise Exception("Pineboo getLogger does not allow for root logger")


def addLoggingLevel(levelName: str, levelNum: int) -> None:
    methodName = levelName.lower()

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    if not hasattr(logging.getLoggerClass(), methodName):
        setattr(logging.getLoggerClass(), methodName, logForLevel)


addLoggingLevel("TRACE", TRACE)
addLoggingLevel("NOTICE", NOTICE)
addLoggingLevel("HINT", HINT)
addLoggingLevel("MESSAGE", MESSAGE)
