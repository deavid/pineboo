from pineboolib.core import decorators
from pineboolib.flcontrols import ProjectClass


class FLSqlConnections(ProjectClass):
    pass

    @classmethod
    @decorators.NotImplementedWarn
    def database(cls):
        return True
