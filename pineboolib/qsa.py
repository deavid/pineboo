# -*- coding: utf-8 -*-

import os
import re
import traceback

from PyQt5 import QtCore
import logging

# AQSObjects
from pineboolib.fllegacy.aqsobjects.AQSettings import AQSettings
from pineboolib.fllegacy.aqsobjects.AQUtil import AQUtil
from pineboolib.fllegacy.aqsobjects.AQSql import AQSql
from pineboolib.fllegacy.aqsobjects.AQS import AQS
# FLObjects
from pineboolib.fllegacy.FLPosPrinter import FLPosPrinter
from pineboolib.fllegacy.FLFormSearchDB import FLFormSearchDB
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
from pineboolib.fllegacy.FLTableDB import FLTableDB
from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib.fllegacy.FLCodBar import FLCodBar
from pineboolib.fllegacy.FLNetwork import FLNetwork
from pineboolib.fllegacy.FLReportViewer import FLReportViewer

from pineboolib.utils import ustr, ustr1

from pineboolib.pncontrolsfactory import *
logger = logging.getLogger(__name__)

util = FLUtil()  # <- para cuando QS erróneo usa util sin definirla
sys = SysType()
AQS = AQS()
AQUtil = AQUtil()
undefined = None


def Function(args, source):
    # Leer código QS embebido en Source
    # asumir que es una funcion anónima, tal que:
    #  -> function($args) { source }
    # compilar la funcion y devolver el puntero
    qs_source = """
function anon(%s) {
    %s
} """ % (args, source)
    print("Compilando QS en línea: ", qs_source)
    from pineboolib.flparser import flscriptparse
    from pineboolib.flparser import postparse
    from pineboolib.flparser.pytnyzer import write_python_file, string_template
    import io
    prog = flscriptparse.parse(qs_source)
    tree_data = flscriptparse.calctree(prog, alias_mode=0)
    ast = postparse.post_parse(tree_data)
    tpl = string_template

    f1 = io.StringIO()

    write_python_file(f1, ast, tpl)
    pyprog = f1.getvalue()
    print("Resultado: ", pyprog)
    glob = {}
    loc = {}
    exec(pyprog, glob, loc)
    # ... y lo peor es que funciona. W-T-F.

    # return loc["anon"]
    return getattr(loc["FormInternalObj"], "anon")


def Object(x=None):
    if x is None:
        x = {}

    from pineboolib.utils import StructMyDict
    return StructMyDict(x)


class Array(object):

    dict_ = None
    key_ = None
    names_ = None

    def __init__(self, *args):
        self.names_ = []
        self.dict_ = {}

        if not len(args):
            return
        elif isinstance(args[0], int) and len(args) == 1:
            return
        elif isinstance(args[0], list):
            for field in args[0]:
                self.names_.append(field)
                self.dict_[field] = field

        elif isinstance(args[0], str):
            for f in args:
                self.__setitem__(f, f)
        else:
            self.dict_ = args

    def __setitem__(self, key, value):
        # if isinstance(key, int):
        #   key = str(key)
        if key not in self.names_:
            self.names_.append(key)

        self.dict_[key] = value

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.dict_[self.names_[key]]
        else:
            # print("QSATYPE.DEBUG: Array.getItem() " ,key,  self.dict_[key])
            return self.dict_[key]

    def __getattr__(self, k):
        if k == 'length':
            return len(self.dict_)
        else:
            return self.dict_[k]

    def __len__(self):
        len_ = 0

        for l in self.dict_:
            len_ = len_ + 1

        return len_


def Boolean(x=False):
    return bool(x)


class Math(object):

    def abs(x):
        return math.fabs(x)

    def ceil(x):
        return math.ceil(x)

    def floor(x):
        return math.floor(x)

    def pow(x, y):
        return math.pow(x, y)


def parseFloat(x):
    if x is None:
        return 0
    return float(x)


def parseString(obj):
    try:
        return obj.toString()
    except Exception:
        return str(obj)


def parseInt(x):
    if x is None:
        return 0
    return int(x)


def isNaN(x):
    if not x:
        return True

    try:
        float(x)
        return False
    except ValueError:
        return True


class Input(object):
    @classmethod
    def getText(cls, question, prevtxt, title):
        text, ok = QtWidgets.QInputDialog.getText(None, title,
                                                  question, QtWidgets.QLineEdit.Normal, prevtxt)
        if not ok:
            return None
        return text


def qsa_length(obj):
    lfn = getattr(obj, "length", None)
    if lfn:
        return lfn()
    return len(lfn)


def qsa_text(obj):
    try:
        return obj.text()
    except Exception:
        return obj.text


def RegExp(strRE):
    if strRE[-2:] == "/g":
        strRE = strRE[:-2]

    if strRE[:1] == "/":
        strRE = strRE[1:]

    return qsaRegExp(strRE)


class qsaRegExp(object):

    strRE_ = None
    result_ = None

    def __init__(self, strRE):
        print("Nuevo Objeto RegExp de " + strRE)
        self.strRE_ = strRE

    def search(self, text):
        print("Buscando " + self.strRE_ + " en " + text)
        self.result_ = re.search(self.strRE_, text)

    def cap(self, i):
        if self.result_ is None:
            return None

        try:
            return self.result_.group(i)
        except Exception:
            return None


class Date(object):

    date_ = None
    time_ = None

    def __init__(self, *args):
        super(Date, self).__init__()
        if len(args) == 1:
            date_ = args[0]
            if isinstance(date_, str):
                self.date_ = QtCore.QDate.fromString(date_, "yyyy-MM-dd")
            else:
                self.date_ = QtCore.QDate(date_)
            self.time_ = QtCore.QTime(0, 0)
        elif not args:
            self.date_ = QtCore.QDate.currentDate()
            self.time_ = QtCore.QTime.currentTime()
        else:
            self.date_ = QtCore.QDate(args[0], args[1], args[2])
            self.time_ = QtCore.QTime(0, 0)

    def toString(self, *args, **kwargs):
        texto = "%s-%s-%sT%s:%s:%s" % (self.date_.toString("yyyy"), self.date_.toString("MM"), self.date_.toString(
            "dd"), self.time_.toString("hh"), self.time_.toString("mm"), self.time_.toString("ss"))
        return texto

    def getYear(self):
        return self.date_.year()

    def getMonth(self):
        return self.date_.month()

    def getDay(self):
        return self.date_.day()

    def getHours(self):
        return self.time_.hour()

    def getMinutes(self):
        return self.time_.minute()

    def getSeconds(self):
        return self.time_.second()

    def getMilliseconds(self):
        return self.time_.msec()

    @classmethod
    def parse(cls, value):
        return QtCore.QDate.fromString(value)


class Process(QtCore.QProcess):

    running = None
    stderr = None
    stdout = None

    def __init__(self, *args):
        super(Process, self).__init__()
        self.readyReadStandardOutput.connect(self.stdoutReady)
        self.readyReadStandardError.connect(self.stderrReady)
        self.stderr = None
        if args:
            self.runing = False
            self.setProgram(args[0])
            argumentos = args[1:]
            self.setArguments(argumentos)

    def start(self):
        self.running = True
        super(Process, self).start()

    def stop(self):
        self.running = False
        super(Process, self).stop()

    def writeToStdin(self, stdin_):
        import sys
        encoding = sys.getfilesystemencoding()
        stdin_as_bytes = stdin_.encode(encoding)
        self.writeData(stdin_as_bytes)
        # self.closeWriteChannel()

    def stdoutReady(self):
        self.stdout = str(self.readAllStandardOutput())

    def stderrReady(self):
        self.stderr = str(self.readAllStandardError())

    def __setattr__(self, name, value):
        if name == "workingDirectory":
            self.setWorkingDirectory(value)
        else:
            super(Process, self).__setattr__(name, value)

    def execute(comando):
        import sys
        encoding = sys.getfilesystemencoding()
        pro = QtCore.QProcess()
        if isinstance(comando, str):
            comando = comando.split(" ")

        programa = comando[0]
        argumentos = comando[1:]
        pro.setProgram(programa)
        pro.setArguments(argumentos)
        pro.start()
        pro.waitForFinished(30000)
        Process.stdout = pro.readAllStandardOutput().data().decode(encoding)
        Process.stderr = pro.readAllStandardError().data().decode(encoding)


QProcess = QtCore.QProcess


class Dir(object):
    path_ = None
    Files = "*.*"

    from os.path import expanduser
    home = expanduser("~")

    def __init__(self, path=None):
        self.path_ = path

    def entryList(self, patron, type_=None):
        # p = os.walk(self.path_)
        retorno = []
        try:
            import fnmatch
            for file in os.listdir(self.path_):
                if fnmatch.fnmatch(file, patron):
                    retorno.append(file)
        except Exception as e:
            print("Dir_Class.entryList:", e)

        return retorno

    def fileExists(self, name):
        return os.path.exists(name)

    def cleanDirPath(name):
        return str(name)

    def convertSeparators(filename):
        # Retorno el mismo path del fichero ...
        return filename

    def setCurrent(self, val=None):
        if val is None:
            val = filedir(".")
        os.chdir(val)

    def mkdir(self, name=None):
        if name is None:
            name = self.path_
        try:
            os.stat(name)
        except:
            os.mkdir(name)


class File(QtCore.QFile):
    fichero = None
    mode = None
    path = None

    from PyQt5.Qt import QIODevice
    ReadOnly = QIODevice.ReadOnly
    WriteOnly = QIODevice.WriteOnly
    ReadWrite = QIODevice.ReadWrite
    encode_ = None

    def __init__(self, rutaFichero, encode=None):
        self.encode_ = "iso-8859-15"
        if isinstance(rutaFichero, tuple):
            rutaFichero = rutaFichero[0]
        self.fichero = str(rutaFichero)
        super(File, self).__init__(rutaFichero)
        self.path = os.path.dirname(self.fichero)

        if encode is not None:
            self.encode_ = encode

    # def open(self, mode):
    #    super(File, self).open(self.fichero, mode)

    def read(self):

        if isinstance(self, str):
            file_ = self
            encode = "iso-8859-15"
        else:
            file_ = self.fichero
            encode = self.encode_
        import codecs
        f = codecs.open(file_, encoding=encode)
        ret = ""
        for l in f:
            ret = ret + l

        f.close()
        return ret
        # if isinstance(self, str):
        #    f = File(self)
        #    f.open(File.ReadOnly)
        #    return f.read()

        #in_ = QTextStream(self)
        # return in_.readAll()

    def write(self, text):
        import codecs
        f = codecs.open(self.fichero, encoding=self.encode_, mode="w+")
        f.write(text)
        f.seek(0)
        f.close()

    def exists(name):
        return os.path.isfile(name)


class QString(str):
    def mid(self, start, length=None):
        if length is None:
            return self[start:]
        else:
            return self[start:start + length]


def debug(txt):
    logger.message("---> " + ustr(txt))
