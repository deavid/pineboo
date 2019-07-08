# # -*- coding: utf-8 -*-
from pineboolib import logging
from flup.server.fcgi import WSGIServer
from pineboolib.plugins.dgi.dgi_schema import dgi_schema
from pineboolib.application.utils.check_dependencies import check_dependencies

from pineboolib.application import project


logger = logging.getLogger(__name__)

check_dependencies({"flup": "flup-py3"})


class dgi_fcgi(dgi_schema):

    _fcgiCall = None
    _fcgiSocket = None

    def __init__(self):
        super(dgi_fcgi, self).__init__()  # desktopEnabled y mlDefault a True
        self._name = "fcgi"
        self._alias = "FastCGI"
        self._fcgiCall = "flfactppal.iface.fcgiProcessRequest"
        self._fcgiSocket = "pineboo-fastcgi.socket"
        self.setUseDesktop(False)
        self.setUseMLDefault(False)
        self.showInitBanner()

    def alternativeMain(self, main_):
        logger.info("=============================================")
        logger.info("FCGI:INFO: Listening socket %s", self._fcgiSocket)
        logger.info("FCGI:INFO: Sending queries to %s", self._fcgiCall)
        par_ = parser(main_, self._fcgiCall)
        WSGIServer(par_.call, bindAddress=self._fcgiSocket).run()

    def setParameter(self, param):
        if param.find(":") > -1:
            p = param.split(":")
            self._fcgiCall = p[0]
            self._fcgiSocket = p[1]
        else:
            self._fcgiCall = param


"""
Esta clase lanza contra el arbol qsa la consulta recibida y retorna la respuesta proporcionada, si procede
"""


class parser(object):
    _prj = None
    _callScript = None

    def __init__(self, prj, callScript):
        self._prj = prj
        self._callScript = callScript

    def call(self, environ, start_response):
        start_response("200 OK", [("Content-Type", "text/html")])
        aList = environ["QUERY_STRING"]
        try:
            retorno_ = project.call(self._callScript, aList)
        except Exception:
            from pineboolib import pncontrolsfactory

            logger.info(self._callScript, environ["QUERY_STRING"])
            retorno_ = (
                """<html><head><title>Pineboo %s - FastCGI - </title></head><body><h1>Function %s not found!</h1></body></html>"""
                % (pncontrolsfactory.SysType().version(), self._callScript)
            )
            pass
        logger.info("FCGI:INFO: Processing '%s' ...", environ["QUERY_STRING"])

        return retorno_
