# # -*- coding: utf-8 -*-

from pineboolib.plugins.dgi.dgi_schema import dgi_schema
from flup.server.fcgi import WSGIServer
import traceback
import sys
import pineboolib

dependences = []

try:
    import flup  # noqa
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


class dgi_fcgi(dgi_schema):

    _fcgiCall = None
    _fcgiSocket = None

    def __init__(self):
        super(dgi_fcgi, self).__init__()  # desktopEnabled y mlDefault a True
        self._name = "fcgi"
        self._alias = "FastCGI"
        self._fcgiCall = "flfactppal.iface.fcgiProcessRequest"
        self._fcgiSocket = "%s/pineboo-fastcgi.socket" % pineboolib.project.getTempDir()
        self.setUseDesktop(False)
        self.setUseMLDefault(False)
        self.showInitBanner()

    def alternativeMain(self, main_):
        print("=============================================")
        print("FCGI:INFO: Listening socket", self._fcgiSocket)
        print("FCGI:INFO: Sending queries to", self._fcgiCall)
        par_ = parser(main_, self._fcgiCall)
        WSGIServer(par_.call, bindAddress=self._fcgiSocket).run()

    def setParameter(self, param):
        if param.find(":") > -1:
            p = param.split(":")
            self._fcgiCall = p[0]
            self._fcgiSocket = p[1]
        else:
            self._fcgiCall = param


class parser(object):
    _prj = None
    _callScript = None

    def __init__(self, prj, callScript):
        self._prj = prj
        self._callScript = callScript

    def call(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        fn = None
        try:
            import pineboolib.qsaglobals
            fn = eval(self._callScript, pineboolib.qsaglobals.__dict__)
        except Exception:
            print("No se encuentra la función buscada")
            print(self._callScript, environ["QUERY_STRING"])
            retorno_ = (
                '''<html><head><title>Hello World!</title></head><body><h1>Hello world!</h1></body></html>''')
            pass
        print("FCGI:INFO: Processing '%s' ..." % environ["QUERY_STRING"])
        aList = environ["QUERY_STRING"]
        if aList and fn:
            retorno_ = fn(aList)

        return retorno_
