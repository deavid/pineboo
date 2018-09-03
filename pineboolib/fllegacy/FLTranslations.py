# -*- coding: utf-8 -*-
import os
import logging
from subprocess import call

from PyQt5 import QtCore
from PyQt5.Qt import QFile, QTextStream, qApp

"""
Esta clase gestiona las diferenetes trducciones de módulos y aplicación
"""


class FLTranslations(QtCore.QObject):

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

    def loadTsFile(self, tor, tsFileName, verbose):
        qmFileName = tsFileName
        qmFileName = qmFileName[:-3]
        qmFileName = "%s.qm" % qmFileName
        print("qm", qmFileName)
        try:
            if not os.path.exists(qmFileName):
                tor.load(tsFileName)
        except Exception:
            self.logger.warn("For some reason, I cannot load '%s'", tsFileName)
            return False

        return True

    """
    Comprueba si el .qm se ha creado
    @param tor. Metatranslator
    @param qmFileName. Nombre del fichero .qm a comprobar
    @param verbose. Muestra verbose (True, False)
    @param stripped. No usado
    """

    def releaseMetaTranslator(self, tor, qmFileName, verbose, stripped):
        if verbose:
            self.logger.debug("Checking '%s'...", qmFileName)

        if not os.path.exists(qmFileName):
            self.logger.warn("For some reason, i cannot save '%s'", qmFileName)

    """
    Libera el fichero .ts
    @param tsFileName. Nombre del fichero .ts
    @param verbose. Muestra verbose (True, False)
    @param stripped. no usado
    """

    def releaseTsFile(self, tsFileName, verbose, stripped):
        tor = None
        if self.loadTsFile(tor, tsFileName, verbose):
            qmFileName = tsFileName
            qmFileName = qmFileName.replace(".ts", "")
            qmFileName = "%s.qm" % qmFileName
            self.releaseMetaTranslator(tor, qmFileName, verbose, stripped)

    """
    Convierte el fichero .ts en .qm
    @param tsImputFile. Nombre del fichero .ts origen
    @param qmOutputFile. Nombre del fichero .qm destino
    @param stripped. No usado
    """

    def lrelease(self, tsInputFile, qmOutputFile, stripped=True):
        import pineboolib
        verbose = pineboolib.project.debugLevel > 200
        metTranslations = False
        tor = metaTranslator()

        f = QFile(tsInputFile)
        if not f.open(QtCore.QIODevice.ReadOnly):
            self.logger.warn("Cannot open file '%s'", tsInputFile)
            return

        t = QTextStream(f)
        fullText = t.readAll()
        f.close()

        if fullText.find("<!DOCTYPE TS>") >= 0:
            if qmOutputFile is None:
                self.releaseTsFile(tsInputFile, verbose, stripped)
            else:
                if not self.loadTsFile(tor, tsInputFile, verbose):
                    return

        else:
            # modId = self.db_.managerModules().idModuleOfFile(tsInputFile)
            key = self.db_.managerModules().shaOfFile(tsInputFile)
            # dir = filedir("../tempdata/cache/%s/%s/file.ts/%s" %
            #               (self._prj.conn.db_name, modId, key))
            tagMap = fullText
            # TODO: hay que cargar todo el contenido del fichero en un diccionario
            for key, value in tagMap:
                toks = value.split(" ")

                for t in toks:
                    if key == "TRANSLATIONS":
                        metTranslations = True
                        self.releaseTsFile(t, verbose, stripped)

            if not metTranslations:
                self.logger.warn("Met no 'TRANSLATIONS' entry in project file '%s'", tsInputFile)

        if qmOutputFile:
            self.releaseMetaTranslator(tor, qmOutputFile, verbose, stripped)


"""
Esta clase llama al conversor  de fichero .qs
"""


class metaTranslator(object):

    # TODO: Esto en producción seria necesario hacerlo desde el programa.
    """
    Conversor
    @param nombre fichero origen
    """

    def load(self, filename):
        return call(["lrelease", filename])


"""
Devuelve la traducción si existe
"""


class FLTranslate(QtCore.QObject):

    group_ = None
    context_ = None
    pos_ = 0

    """
    Constructor
    @param Group. Grupo al que pertenece la traducción
    @param context. Texto a traducir
    @param Translate. Boolean que indica si se traduce realmente el texto pasado
    @param pos. Posición en la que se empieza a sustituir los argumentos pasados
    """

    def __init__(self, group, context, translate=True, pos=1):
        super(FLTranslate, self).__init__()
        self.pos_ = pos
        self.group_ = group
        if translate:
            self.context_ = qApp.translate(group, context)
        else:
            self.context_ = context

    """
    Argumento pasado a la traducción
    @param value. Texto a añadir a la traducción
    """

    def arg(self, value):
        if isinstance(value, list):
            for f in value:
                self.context_ = self.context_.replace(
                    "%s" % self.pos_, str(f))
                self.pos_ = self.pos_ + 1
        else:
            self.context_ = self.context_.replace(
                "%s" % self.pos_, str(value))

        return FLTranslate(self.group_, self.context_, False, self.pos_ + 1)

    """
    Retorna el valor traducido
    @return traducción completada con los argumentos
    """

    def __str__(self):
        return self.context_
