from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from pineboolib import decorators
from pineboolib.flcontrols import ProjectClass


class FLDiskCache(ProjectClass):

    absoluteDirPath = ""

    @decorators.BetaImplementation
    def aqDiskCacheFind(self, key, string):
        return self.find(key, string)

    @decorators.BetaImplementation
    def aqDiskCacheInsert(self, key, string):
        return self.insert(key, string)

    @decorators.BetaImplementation
    def find(self, key, d):
        if isinstance(d, str):
            fileCache = self.AQ_DISKCACHE_DIRPATH + '/' + key
            fi = QtCore.QFile(fileCache)
            if not fi.open(Qt.IO_ReadOnly):
                return False
            t = QtCore.QTextStream(fi)
            d = t.read()
            fi.close()
            return d
        else:
            fileCache = self.AQ_DISKCACHE_DIRPATH + '/' + key + "-BIN"
            fi = QtCore.QFile(fileCache)
            if not fi.open(Qt.IO_ReadOnly):
                return False
            dat = QtCore.QDataStream(fi)
            dat >> d
            fi.close()
            return d

    @decorators.BetaImplementation
    def insert(self, key, d):
        if isinstance(d, str):
            fileCache = self.AQ_DISKCACHE_DIRPATH + '/' + key
            fi = QtCore.QFile(fileCache)
            drc = QtCore.QDir(self.AQ_DISKCACHE_DIRPATH)
            if not drc.exists():
                drc.mkdir(self.AQ_DISKCACHE_DIRPATH)
            elif fi.exists():
                return True
            if d and d != "":
                if fi.open(self.IO_WriteOnly):
                    t = QtCore.QTextStream(fi)
                    t << d
                    fi.close()
                    return True
            return False
        else:
            fileCache = self.AQ_DISKCACHE_DIRPATH + '/' + key + "-BIN"
            fi = QtCore.QFile(fileCache)
            drc = QtCore.QDir(self.AQ_DISKCACHE_DIRPATH)
            if not drc.exists():
                drc.mkdir(self.AQ_DISKCACHE_DIRPATH)
            elif fi.exists():
                return True
            if not d.isEmpty():
                if fi.open(self.IO_WriteOnly):
                    dat = QtCore.QDataStream(fi)
                    dat << d
                    fi.close()
                    return True
            return False

    @decorators.BetaImplementation
    def clear(self):
        drc = QtCore.QDir(self.AQ_DISKCACHE_DIRPATH)
        if drc.exists():
            lst = drc.entryList("*; *.*")
            for it in lst:
                drc.remove(self.AQ_DISKCACHE_DIRPATH + '/' + it)

    @decorators.BetaImplementation
    def absoluteFilePath(self, key):
        fileCache = self.AQ_DISKCACHE_DIRPATH + '/' + key
        if not QtCore.QFile.exists(fileCache):
            return ""
        return fileCache

    @decorators.BetaImplementation
    def aqSetAndCreateDirPath(self, path):
        self.AQ_DISKCACHE_DIRPATH = path
        drc = QtCore.QDir(self.AQ_DISKCACHE_DIRPATH)
        if not drc.exists():
            drc.mkdir(self.AQ_DISKCACHE_DIRPATH)

    @decorators.BetaImplementation
    def init(self, app=0):
        codec = QtCore.QTextCodec.codecForLocale()
        localEncode = codec.mimeName() if codec else ""
        if not app:
            self.aqSetAndCreateDirPath(AQ_USRHOME + '/.aqcache')
            if localEncode and localEncode != "":
                self.aqSetAndCreateDirPath(self.AQ_DISKCACHE_DIRPATH + '/' + localEncode)
        else:
            dbName = app.db().database()
            if app.db().driverName() == "FLsqlite":
                dbName.replace(self.AQ_DISKCACHE_DIRPATH, "")
            self.aqSetAndCreateDirPath(AQ_USRHOME + '/.aqcache/' + dbName)
            if localEncode and localEncode != "":
                self.aqSetAndCreateDirPath(self.AQ_DISKCACHE_DIRPATH + '/' + localEncode)

            drc = QtCore.QDir(self.AQ_DISKCACHE_DIRPATH)
            if drc.exists():
                lst = drc.entryList("*.*", QtCore.QDir.Files)
                for it in lst:
                    drc.remove(self.AQ_DISKCACHE_DIRPATH + '/' + str(it))

    AQ_DISKCACHE_INS = insert
    AQ_DISKCACHE_FIND = find
    AQ_DISKCACHE_CLR = clear
    AQ_DISKCACHE_FILEPATH = absoluteFilePath
    AQ_DISKCACHE_DIRPATH = absoluteDirPath
