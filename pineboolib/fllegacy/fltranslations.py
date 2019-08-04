# -*- coding: utf-8 -*-
import os
from pineboolib import logging
from pineboolib.core import decorators

from PyQt5 import QtCore, Qt  # type: ignore
from typing import Any, Union


"""
Esta clase gestiona las diferenetes trducciones de módulos y aplicación
"""


class FLTranslations(object):

    TML = None
    qmFileName = None

    """
    Constructor
    """

    def __init__(self) -> None:
        super(FLTranslations, self).__init__()
        self.logger = logging.getLogger("FLTranslations")

    """
    Si no existe el .qm convierte el .ts que le damos a .qm
    @param tor. Objeto clase metatranslator. type: "FLTranslator"
    @param tsFileName. Nombre del fichero .ts a convertir
    @param verbose. Muestra verbose (True, False)
    @return Boolean. Proceso realizado correctamente
    """

    def loadTsFile(self, tor: Any, ts_file_name: Union[bytes, int, str], verbose) -> bool:
        # qm_file_name = "%s.qm" % ts_file_name[:-3]
        ok = False
        if os.path.exists(ts_file_name):
            ok = tor.load(ts_file_name)

        if not ok:
            self.logger.warning("For some reason, I cannot load '%s'", ts_file_name)
        return ok

    """
    Libera el fichero .ts
    @param tsFileName. Nombre del fichero .ts
    @param verbose. Muestra verbose (True, False)
    @param stripped. no usado
    """

    @decorators.Deprecated
    def releaseTsFile(self, ts_file_name: str, verbose: bool, stripped: bool) -> None:
        pass
        # tor = None

        # if self.loadTsFile(tor, ts_file_name, verbose):
        #    pass
        # qm_file_name = "%s.qm" % ts_file_name[:-3]
        # FIXME: self.releaseMetaTranslator - does not exist in this class
        # if not os.path.exists(qm_file_name):
        #     self.releaseMetaTranslator(tor, qm_file_name, verbose, stripped)

    """
    Convierte el fichero .ts en .qm
    @param tsImputFile. Nombre del fichero .ts origen
    @param qmOutputFile. Nombre del fichero .qm destino
    @param stripped. No usado
    """

    def lrelease(self, ts_input_file: str, qm_output_file: str, stripped: bool = True) -> None:
        from pineboolib.application import project

        verbose = False
        metTranslations = False

        f = Qt.QFile(ts_input_file)
        if not f.open(QtCore.QIODevice.ReadOnly):
            self.logger.warning("Cannot open file '%s'", ts_input_file)
            return

        t = Qt.QTextStream(f)
        full_text = t.readAll()
        f.close()

        if full_text.find("<!DOCTYPE TS>") >= 0:
            self.releaseTsFile(ts_input_file, verbose, stripped)

        else:
            if project.conn is None:
                raise Exception("Project has no connection yet")
            # modId = self.db_.managerModules().idModuleOfFile(tsInputFile)
            key = project.conn.managerModules().shaOfFile(ts_input_file)
            # dir = filedir("../tempdata/cache/%s/%s/file.ts/%s" %
            #               (self._prj.conn.db_name, modId, key))
            tagMap = full_text
            # TODO: hay que cargar todo el contenido del fichero en un diccionario
            for key, value in tagMap:
                toks = value.split(" ")

                for t in toks:
                    if key == "TRANSLATIONS":
                        metTranslations = True
                        self.releaseTsFile(t, verbose, stripped)

            if not metTranslations:
                self.logger.warning(
                    "Met no 'TRANSLATIONS' entry in project file '%s'", ts_input_file
                )


"""
Esta clase llama al conversor  de fichero .qs
"""


"""
Devuelve la traducción si existe
"""


def FLTranslate(group: str, context: str, translate: bool = True) -> str:
    return Qt.qApp.translate(group.encode(), context.encode()) if translate else context
