# # -*- coding: utf-8 -*-

import sys
import traceback
import logging
from flup.server.fcgi import WSGIServer

from pineboolib.plugins.dgi.dgi_schema import dgi_schema
from pineboolib.fllegacy.pncontrolsfactory import SysType
from pineboolib.utils import checkDependencies

import pineboolib


logger = logging.getLogger(__name__)


dependences = []


checkDependencies({"flup": "flup-py3"})


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
        logger.info("=============================================")
        logger.info("FCGI:INFO: Listening socket", self._fcgiSocket)
        logger.info("FCGI:INFO: Sending queries to", self._fcgiCall)
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
        start_response('200 OK', [('Content-Type', 'text/html')])
        fn = None
        aList = environ["QUERY_STRING"]
        try:
            retorno_ = pineboolib.project.call(self._callScript, aList)
        except Exception:
            logger.info(self._callScript, environ["QUERY_STRING"])
            retorno_ = ('''<html><head><title>Pineboo %s - FastCGI - </title></head><body><h1>Function %s not found!</h1></body></html>''' %
                        (SysType().version(), self._callScript))
            pass
        logger.info("FCGI:INFO: Processing '%s' ...", environ["QUERY_STRING"])

        return retorno_
