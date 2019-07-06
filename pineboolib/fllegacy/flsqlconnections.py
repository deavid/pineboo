from pineboolib.core import decorators


class FLSqlConnections(object):
    @classmethod
    @decorators.NotImplementedWarn
    def database(cls):
        return True
