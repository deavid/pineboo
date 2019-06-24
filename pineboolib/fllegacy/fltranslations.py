# -*- coding: utf-8 -*-
import os
import logging

from PyQt5 import QtCore, Qt


"""
Esta clase gestiona las diferenetes trducciones de módulos y aplicación
"""


class FLTranslations(object):

    TML = None
    qmFileName = None

    """
    Constructor
    """

    def __init__(self):
        super(FLTranslations, self).__init__()
        self.logger = logging.getLogger("FLTranslations")

    """
    Si no existe el .qm convierte el .ts que le damos a .qm
    @param tor. Objeto clase metatranslator.
    @param tsFileName. Nombre del fichero .ts a convertir
    @param verbose. Muestra verbose (True, False)
    @return Boolean. Proceso realizado correctamente
    """

    def loadTsFile(self, tor, ts_file_name, verbose):
        # qm_file_name = "%s.qm" % ts_file_name[:-3]
        ok = False
        if os.path.exists(ts_file_name):
            ok = tor.load(ts_file_name)

        if not ok:
            self.logger.warning("For some reason, I cannot load '%s'", ts_file_name)
        return ok

    """
    Comprueba si el .qm se ha creado
    @param tor. Metatranslator
    @param qmFileName. Nombre del fichero .qm a comprobar
    @param verbose. Muestra verbose (True, False)
    @param stripped. No usado
    """

    def releaseMetaTranslator(self, tor, qm_file_name, verbose, stripped):
        from pineboolib.fllegacy.flsettings import FLSettings

        if verbose:
            self.logger.debug("Updating '%s'...", qm_file_name)

        settings = FLSettings()
        if settings.readBoolEntry("ebcomportamiento/translations_from_qm", False):
            print("*** FAKE :: ", qm_file_name)
            if not tor.release(qm_file_name, verbose, "Stripped" if stripped else "Everything"):
                self.logger.warning("For some reason, i cannot save '%s'", qm_file_name)

    """
    Libera el fichero .ts
    @param tsFileName. Nombre del fichero .ts
    @param verbose. Muestra verbose (True, False)
    @param stripped. no usado
    """

    def releaseTsFile(self, ts_file_name, verbose, stripped):
        tor = None

        if self.loadTsFile(tor, ts_file_name, verbose):
            qm_file_name = "%s.qm" % ts_file_name[:-3]
            if not os.path.exists(qm_file_name):
                self.releaseMetaTranslator(tor, qm_file_name, verbose, stripped)

    """
    Convierte el fichero .ts en .qm
    @param tsImputFile. Nombre del fichero .ts origen
    @param qmOutputFile. Nombre del fichero .qm destino
    @param stripped. No usado
    """

    def lrelease(self, ts_input_file, qm_output_file, stripped=True):
        from pineboolib.translator.metatranslator import metaTranslator

        verbose = False
        metTranslations = False
        tor = metaTranslator()

        f = Qt.QFile(ts_input_file)
        if not f.open(QtCore.QIODevice.ReadOnly):
            self.logger.warning("Cannot open file '%s'", ts_input_file)
            return

        t = Qt.QTextStream(f)
        full_text = t.readAll()
        f.close()

        if full_text.find("<!DOCTYPE TS>") >= 0:
            if qm_output_file is None:
                self.releaseTsFile(ts_input_file, verbose, stripped)
            else:
                if not self.loadTsFile(tor, ts_input_file, verbose):
                    return

        else:
            # modId = self.db_.managerModules().idModuleOfFile(tsInputFile)
            key = self.db_.managerModules().shaOfFile(ts_input_file)
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
                self.logger.warning("Met no 'TRANSLATIONS' entry in project file '%s'", ts_input_file)

        if qm_output_file:
            self.releaseMetaTranslator(tor, qm_output_file, verbose, stripped)


"""
Esta clase llama al conversor  de fichero .qs
"""


"""
Devuelve la traducción si existe
"""


def FLTranslate(group, context, translate=True):
    return Qt.qApp.translate(group.encode(), context.encode()) if translate else context.encode()
