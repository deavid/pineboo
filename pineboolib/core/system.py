"""System Module."""

import os


class System(object):
    @staticmethod
    def setenv(name: str, val: str) -> None:
        os.environ[name] = val

    @staticmethod
    def getenv(name: str) -> str:
        ret_ = ""
        if name in os.environ.keys():
            ret_ = os.environ[name]

        return ret_
