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
            fi = Qt.QFile(fileCache)
            if not fi.open(Qt.IO_ReadOnly):
                return False
            t = Qt.QTextStream(fi)
            d = t.read()
            fi.close()
            return d
        else:
            fileCache = self.AQ_DISKCACHE_DIRPATH + '/' + key + "-BIN"
            fi = Qt.QFile(fileCache)
            if not fi.open(Qt.IO_ReadOnly):
                return False
            dat = Qt.QDataStream(fi)
            dat >> d
            fi.close()
            return d

    @decorators.BetaImplementation
    def insert(self, key, d):
        if isinstance(d, str):
            fileCache = self.AQ_DISKCACHE_DIRPATH + '/' + key
            fi = Qt.QFile(fileCache)
            drc = Qt.QDir(self.AQ_DISKCACHE_DIRPATH)
            if not drc.exists():
                drc.mkdir(self.AQ_DISKCACHE_DIRPATH)
            elif fi.exists():
                return True
            if d and d != "":
                if fi.open(self.IO_WriteOnly):
                    t = Qt.QTextStream(fi)
                    t << d
                    fi.close()
                    return True
            return False
        else:
            fileCache = self.AQ_DISKCACHE_DIRPATH + '/' + key + "-BIN"
            fi = Qt.QFile(fileCache)
            drc = Qt.QDir(self.AQ_DISKCACHE_DIRPATH)
            if not drc.exists():
                drc.mkdir(self.AQ_DISKCACHE_DIRPATH)
            elif fi.exists():
                return True
            if not d.isEmpty():
                if fi.open(self.IO_WriteOnly):
                    dat = Qt.QDataStream(fi)
                    dat << d
                    fi.close()
                    return True
            return False

    @decorators.BetaImplementation
    def clear(self):
        drc = Qt.QDir(self.AQ_DISKCACHE_DIRPATH)
        if drc.exists():
            lst = drc.entryList("*; *.*")
            it = lst.begin()
            while it != lst.end():
                drc.remove(self.AQ_DISKCACHE_DIRPATH + '/' + it)
                it = it + 1

    @decorators.BetaImplementation
    def absoluteFilePath(self, key):
        fileCache = self.AQ_DISKCACHE_DIRPATH + '/' + key
        if not Qt.QFile.exists(fileCache):
            return ""
        return fileCache

    @decorators.BetaImplementation
    def aqSetAndCreateDirPath(self, path):
        self.AQ_DISKCACHE_DIRPATH = path
        drc = Qt.QDir(self.AQ_DISKCACHE_DIRPATH)
        if not drc.exists():
            drc.mkdir(self.AQ_DISKCACHE_DIRPATH)

    @decorators.BetaImplementation
    def init(self, app=0):
        codec = Qt.QTextCodec.codecForLocale()
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

            drc = Qt.QDir(self.AQ_DISKCACHE_DIRPATH)
            if drc.exists():
                lst = drc.entryList("*.*", Qt.QDir.Files)
                it = lst.begin()
                while it != lst.end():
                    drc.remove(self.AQ_DISKCACHE_DIRPATH + '/' + str(it))
                    it = it + 1

    AQ_DISKCACHE_INS = insert
    AQ_DISKCACHE_FIND = find
    AQ_DISKCACHE_CLR = clear
    AQ_DISKCACHE_FILEPATH = absoluteFilePath
    AQ_DISKCACHE_DIRPATH = absoluteDirPath
