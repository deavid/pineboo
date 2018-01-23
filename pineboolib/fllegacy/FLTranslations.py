# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.Qt import QFile, QTextStream, qApp
from pineboolib.flcontrols import ProjectClass
# from pineboolib.utils import filedir
from subprocess import call
import os


class FLTranslations(ProjectClass):

    TML = None
    qmFileName = None

    def __init__(self):
        super(FLTranslations, self).__init__()

    def loadTsFile(self, tor, tsFileName, verbose):
        qmFileName = tsFileName
        qmFileName = qmFileName.replace(".ts", "")
        qmFileName = "%s.qm" % qmFileName
        # dir_ = tsFileName[0:len(tsFileName) - 44]
        # fileName_ = tsFileName[len(tsFileName) - 43:]

        try:
            if not os.path.exists(qmFileName):
                tor.load(tsFileName)
        except Exception:
            print("lrelease warning: For some reason, I cannot load '%s'" %
                  tsFileName)
            return False

        return True

    def releaseMetaTranslator(self, tor, qmFileName, verbose, stripped):
        if verbose:
            print("Checking '%s'..." % qmFileName)

        if not os.path.exists(qmFileName):
            print("lrelease warning: For some reason, i cannot save '%s'" %
                  qmFileName)

    def releaseTsFile(self, tsFileName, verbose, stripped):
        tor = None
        if self.loadTsFile(tor, tsFileName, verbose):
            qmFileName = tsFileName
            qmFileName = qmFileName.replace(".ts", "")
            qmFileName = "%s.qm" % qmFileName
            self.releaseMetaTranslator(tor, qmFileName, verbose, stripped)

    def lrelease(self, tsInputFile, qmOutputFile, stripped=True):
        verbose = False
        metTranslations = False
        tor = metaTranslator()

        f = QFile(tsInputFile)
        if not f.open(QtCore.QIODevice.ReadOnly):
            print("lrelease error: Cannot open file '%s'" % tsInputFile)
            return

        t = QTextStream(f)
        fullText = t.readAll()
        f.close()

        if fullText.find("<!DOCTYPE TS>") >= 0:
            if qmOutputFile is None:
                self.releaseTsFile(tsInputFile, verbose, stripped)
            else:
                self.loadTsFile(tor, tsInputFile, verbose)

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
                print(
                    "lrelease warning: Met no 'TRANSLATIONS' entry in project file '%s'" % tsInputFile)

        if qmOutputFile:
            self.releaseMetaTranslator(tor, qmOutputFile, verbose, stripped)


class metaTranslator(object):

    # TODO: Esto en producción seria necesario hacerlo desde el programa.
    def load(self, filename):
        return call(["lrelease", filename])


class FLTranslate(ProjectClass):

    group_ = None
    context_ = None
    pos_ = 0

    def __init__(self, group, context, translate=True, pos=1):
        super(FLTranslate, self).__init__()
        self.pos_ = pos
        self.group_ = group
        if translate:
            self.context_ = qApp.translate(group, context)
        else:
            self.context_ = context

    def arg(self, value):
        if isinstance(value, list):
            for f in value:
                self.context_ = self.context_.replace(
                    "%" + str(self.pos_), str(f))
                self.pos_ = self.pos_ + 1
        else:
            self.context_ = self.context_.replace(
                "%" + str(self.pos_), str(value))

        return FLTranslate(self.group_, self.context_, False, self.pos_ + 1)

    def __str__(self):
        return self.context_
