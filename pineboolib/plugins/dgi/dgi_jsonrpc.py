# # -*- coding: utf-8 -*-

from pineboolib.plugins.dgi.dgi_schema import dgi_schema
from flup.server.fcgi import WSGIServer

dependences = []

try:
    import flup
except ImportError:
    print(traceback.format_exc())
    dependences.append("flup-py3")


if len(dependences) > 0:
    print()
    print("HINT: Dependencias incumplidas:")
    for dep in dependences:
        print("HINT: Instale el paquete %s e intente de nuevo" % dep)
    print()
    sys.exit(32)


class dgi_jsonrpc(dgi_schema):

    _fcgiCall = None
    _fcgiSocket = None

    def __init__(self):
        super(dgi_fcgi, self).__init__()  # desktopEnabled y mlDefault a True
        self._name = "jsonrpc"
        self._alias = "JSON-RPC"
        self.setUseDesktop(True)
        self.setUseMLDefault(False)
        self.setLocalForms(False)
        self.showInitBanner()

    def alternativeMain(self, main_):
        pass

    def setParameter(self, param):
        if param.find(":") > -1:
            p = param.split(":")
            self._fcgiCall = p[0]
            self._fcgiSocket = p[1]
        else:
            self._fcgiCall = param
