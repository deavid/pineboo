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
        self.setUseMLDefault(True)
        self.setLocalDesktop(False)
        self.showInitBanner()
        self._listenSocket = "/tmp/pineboo-JSONRPC.socket"

    def extraProyectInit(self):
        print("=============================================")
        print("============ EXTRA PROJECT INIT =============")
        print("=============================================")
        print("JSON-RPC:INFO: Listening socket", self._listenSocket)
        par_ = parser()
        WSGIServer(par_.query, bindAddress=self._fcgiSocket).run()
        print("End load extraProjectInit")

    def setParameter(self, param):
        self._listenSocket = param

class parser(object):

    def query(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        print("FCGI:INFO: Processing '%s' ..." % environ["QUERY_STRING"])
