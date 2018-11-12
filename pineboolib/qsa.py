# -*- coding: utf-8 -*-

import os
import re
import traceback

from PyQt5 import QtCore
import logging

# FLObjects
from pineboolib.fllegacy.flposprinter import FLPosPrinter
from pineboolib.fllegacy.flformsearchdb import FLFormSearchDB
from pineboolib.fllegacy.flsqlquery import FLSqlQuery
from pineboolib.fllegacy.flsqlcursor import FLSqlCursor
from pineboolib.fllegacy.fltabledb import FLTableDB
from pineboolib.fllegacy.flcodbar import FLCodBar
from pineboolib.fllegacy.flnetwork import FLNetwork
from pineboolib.fllegacy.flreportviewer import FLReportViewer
from pineboolib.fllegacy.flvar import FLVar

from pineboolib.utils import ustr, ustr1, filedir

from pineboolib.pncontrolsfactory import *

logger = logging.getLogger(__name__)

util = FLUtil()  # <- para cuando QS erróneo usa util sin definirla
sys = SysType()

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
        self.list_ = []

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
        elif k == 'append':
            return self.list_.append

        else:
            return self.dict_[k]

    def __len__(self):
        len_ = 0

        for l in self.dict_:
            len_ = len_ + 1

        return len_

    def __str__(self):
        ret = " ".join(self.list_) if len(self.list_) > 0 else " ".join(self.dict_.keys())
        return ret


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

    def round(x):
        return round(x, 2)


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
    def getText(cls, question, prevtxt="", title="Pineboo"):
        text, ok = QtWidgets.QInputDialog.getText(None, title,
                                                  question, QtWidgets.QLineEdit.Normal, prevtxt)
        if not ok:
            return None
        return text

    @classmethod
    def getItem(cls, question, items_list=[], title="Pineboo", editable=True):
        text, ok = QtWidgets.QInputDialog.getItem(None, title, question, items_list, 0, editable)
        if not ok:
            return None
        return text


class NumberEdit(QtWidgets.QWidget):

    def __init__(self):
        super(NumberEdit, self).__init__()
        
        from PyQt5.Qt import QDoubleValidator
        self.line_edit = QLineEdit(self)
        self.label_line_edit = QLabel(self)
        self.label_line_edit.setMinimumWidth(150)
        lay = QHBoxLayout()
        lay.addWidget(self.label_line_edit)
        lay.addWidget(self.line_edit)
        lay.setContentsMargins(0,0,0,0)
        self.setLayout(lay)
        self.validator = QDoubleValidator()
        self.line_edit.setValidator(self.validator)
        

    def getValue(self):
        return float(self.line_edit.text)

    def setValue(self, value):
        self.line_edit.setText(value)

    def getDecimals(self):
        return self.line_edit.validator().decimals()

    def setDecimals(self, decimals):
        self.line_edit.validator().setDecimals(int(decimals))


    def setMinimum(self, min):
        self.line_edit.validator().setBottom(float(min))

    def getMinimum(self):
        return self.line_edit.validator().bottom()


    def getMaximum(self):
        return self.line_edit.validator().top()

    def setMaximum(self, max):
        return self.line_edit.validator().setTop(float(max))

    def getLabel(self):
        self.label_line_edit.text()

    def setLabel(self, label):
        
        self.label_line_edit.setText(label)

    label = property(getLabel, setLabel)
    value = property(getValue, setValue)
    decimals = property(getDecimals, setDecimals)
    mimimum = property(getMinimum, setMinimum)
    maximum = property(getMaximum, setMaximum)


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
        if not args:
            self.date_ = QtCore.QDate.currentDate()
            self.time_ = QtCore.QTime.currentTime()
        elif len(args) <= 2:
            date_ = args[0]
            format_ = args[1] if len(args) == 2 else "yyyy-MM-dd"
            self.time_ = None
            if isinstance(date_, str):
                if len(date_) == 10:
                    self.date_ = QtCore.QDate.fromString(date_, format_)
                else:
                    self.date_ = QtCore.QDate.fromString(date_[0:10], format_)
                    self.time_ = QtCore.QTime.fromString(date_[11:], "hh:mm:ss")
            
            elif isinstance(date_, Date):
                self.date_ = date_.date_
                self.time_ = date_.time_
                
               
            elif isinstance(date_, QtCore.QDate):
                self.date_ = date_
            if not self.time_:    
                self.time_ = QtCore.QTime(0, 0)
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
    
    def setDate(self, *args):
        if len(args) == 1:
            year_ = self.date_.toString("yyyy")
            month_ = self.date_.toString("MM")
            day_ = str(args[0])
            if len(day_) == 1:
                day_ = "0" + day_
            str_ = "%s-%s-%s" % (year_, month_, day_)
            self.date_ = QtCore.QDate.fromString(str_, "yyyy-MM-dd")
        else:
            logger.warn("DATE.setDate: Se han especificado %s", len(args))
    
    def addDays(self, d):
        return Date(self.date_.addDays(d).toString("yyyy-MM-dd"))
    
    def addMonths(self, m):
        return Date(self.date_.addMonths(m).toString("yyyy-MM-dd"))
    
    def addYears(self, y):
        return Date(self.date_.addYears(y).toString("yyyy-MM-dd"))      

    @classmethod
    def parse(cls, value):
        return QtCore.QDate.fromString(value, "yyyy-MM-dd")
    
    def __str__(self):
        return self.toString()





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
        os.chdir(val or filedir("."))

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
        f = codecs.open(file_,"r", encoding=encode)
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

    def write(*args):
        
        if not isinstance(args[0], str):
            fichero = self.fichero
            encode = self.encode_
        else:
            fichero = args[0]
            encode = "iso-8859-15"
        
        text = args[1]
            
        import codecs
        f = codecs.open(fichero, encoding=encode, mode="w+")
        f.write(text)
        f.seek(0)
        f.close()

    def exists(name):
        return os.path.exists(name)

    def isDir(dir_name):
        return os.path.isdir(dir_name)
    
    def getName(self):
        return super(File, self).fileName()
    
    name = property(getName)


class QString(str):
    def mid(self, start, length=None):
        if length is None:
            return self[start:]
        else:
            return self[start:start + length]


def debug(txt):
    logger.warn("---> " + ustr(txt))
