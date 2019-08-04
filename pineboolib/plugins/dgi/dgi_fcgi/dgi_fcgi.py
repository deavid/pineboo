# # -*- coding: utf-8 -*-
from pineboolib import logging
from pineboolib.plugins.dgi.dgi_schema import dgi_schema
from pineboolib.application.utils.check_dependencies import check_dependencies

from pineboolib.application import project

from typing import Any, Mapping


logger = logging.getLogger(__name__)


class dgi_fcgi(dgi_schema):

    _fcgiCall = None
    _fcgiSocket = None

    def __init__(self) -> None:
        super(dgi_fcgi, self).__init__()  # desktopEnabled y mlDefault a True
        self._name = "fcgi"
        self._alias = "FastCGI"
        self._fcgiCall = "flfactppal.iface.fcgiProcessRequest"
        self._fcgiSocket = "pineboo-fastcgi.socket"
        self.setUseDesktop(False)
        self.setUseMLDefault(False)
        self.showInitBanner()
        check_dependencies({"flup": "flup-py3"})

    def alternativeMain(self, main_) -> None:
        from flup.server.fcgi import WSGIServer  # type: ignore

        logger.info("=============================================")
        logger.info("FCGI:INFO: Listening socket %s", self._fcgiSocket)
        logger.info("FCGI:INFO: Sending queries to %s", self._fcgiCall)
        par_ = parser(main_, self._fcgiCall)
        WSGIServer(par_.call, bindAddress=self._fcgiSocket).run()

    def setParameter(self, param: str) -> None:
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
    _callScript: str = ""

    def __init__(self, prj, callScript) -> None:
        self._prj = prj
        self._callScript = callScript

    def call(self, environ: Mapping[str, Any], start_response) -> Any:
        start_response("200 OK", [("Content-Type", "text/html")])
        aList = environ["QUERY_STRING"]
        try:
            retorno_: Any = project.call(self._callScript, aList)
        except Exception:
            from pineboolib.fllegacy.systype import SysType

            qsa_sys = SysType()

            logger.info(self._callScript, environ["QUERY_STRING"])
            retorno_ = (
                """<html><head><title>Pineboo %s - FastCGI - </title></head><body><h1>Function %s not found!</h1></body></html>"""
                % (qsa_sys.version(), self._callScript)
            )
            pass
        logger.info("FCGI:INFO: Processing '%s' ...", environ["QUERY_STRING"])

        return retorno_
