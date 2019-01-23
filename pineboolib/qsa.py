# -*- coding: utf-8 -*-

import os
import re
import traceback
import math

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
from functools import total_ordering

logger = logging.getLogger(__name__)

util = FLUtil()  # <- para cuando QS erróneo usa util sin definirla
sys = SysType()

undefined = None
LogText = 0
RichText = 1


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
    from pineboolib.flparser.pytnyzer import write_python_file
    import io
    prog = flscriptparse.parse(qs_source)
    tree_data = flscriptparse.calctree(prog, alias_mode=0)
    ast = postparse.post_parse(tree_data)

    f1 = io.StringIO()

    write_python_file(f1, ast)
    pyprog = f1.getvalue()
    print("Resultado: ", pyprog)
    glob = {}
    loc = {}
    exec(pyprog, glob, loc)
    # ... y lo peor es que funciona. W-T-F.

    # return loc["anon"]
    return getattr(loc["FormInternalObj"], "anon")


def Object(x=None):
    """
    Objeto tipo object
    """
    if x is None:
        x = {}

    from pineboolib.utils import StructMyDict
    return StructMyDict(x)

def String(value):
    """
    Devuelve una cadena de texto
    @param value. Valor a convertir
    @return cadena de texto.
    """
    return str(value)

class Array(object):
    """
    Objeto tipo Array
    """
    dict_ = None
    key_ = None
    names_ = None
    pos_iter = None

    def __init__(self, *args):
        import collections
        self.dict_ = collections.OrderedDict()

        if not len(args):
            return
        elif isinstance(args[0], int) and len(args) == 1:
            return
        elif isinstance(args[0], list):
            for field in args[0]:
                
                field_key = field
                while field_key in self.dict_.keys():
                    field_key = "%s_bis" % field_key
                    
                self.dict_[field_key] = field

        elif isinstance(args[0], str):
            for f in args:
                self.__setitem__(f, f)
        else:
            self.dict_ = args
    
    def __iter__(self):
        """
        iterable
        """
        self.pos_iter = 0
        return self
    
    def __next__(self):
        """
        iterable
        """
        ret_ = None
        i = 0
        if self.dict_:
            for k in self.dict_.keys():
                if i == self.pos_iter:
                   ret_ = self.dict_[k]
                   break
                
                i += 1
            
        if ret_ is None:
                raise StopIteration
        else:     
            self.pos_iter += 1
            
        return ret_
    

    def __setitem__(self, key, value):
        """
        Especificamos una nueva entrada
        @param key. Nombre del registro
        @param value. Valor del registro
        """

        self.dict_[key] = value

    def __getitem__(self, key):
        """
        Recogemos el valor de un registro
        @param key. Valor que idenfica el registro a recoger
        @return Valor del registro especificado
        """
        if isinstance(key, int):                
            i = 0
            for k in self.dict_.keys():
                if key == i:
                    return self.dict_[k]
                i +=1
            
            
        elif isinstance(key, slice):
            logger.warn("FIXME: Array __getitem__%s con slice" % key)
        else:
            return self.dict_[key] if key in self.dict_.keys() else None
        
        return None

    def __getattr__(self, k):
        if k == 'length':
            return len(self.dict_)
        else:
            return self.dict_[k]

    def __len__(self):
        return len(self.dict_)

    def __str__(self):
        return " ".join(self.dict_.keys())
    
    def append(self, val):
        k = repr(val)
        while True:
            if hasattr(self.dict_, k):
                k = "%s_" % k
            else:
                break
        
        self.dict_[k] = val
            


def Boolean(x=False):
    """
    Retorna Booelan de una cadena de texto
    """ 
    ret = False
    if x in ["true","True",True,1] or isinstance(x, int) > 0 or isinstance(x, float) > 0:
        ret = True
    
    return ret


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
    """
    Convierte a float un valor dado
    @param x. valor a convertir
    @return Valor tipo float, o parametro x , si no es convertible
    """
    try:
        ret = 0 if x is None else float(x) 
        if ret == int(ret):
            ret = int(ret)
        
        return ret
    except Exception:
        return x

def parseString(obj):
    """
    Convierte a str un objeto dado
    @param obj. valor a convertir
    @return str del objeto dado
    """
    return obj.toString() if hasattr(obj, "toString") else str(obj)


def parseInt(x):
    """
    Convierte en int un valor dado
    @param x. Valor a convertir
    @return Valor convertido
    """
    return int(x) if x is not None else 0


def isNaN(x):
    """
    Comprueba si un valor dado en numerico
    @param x. Valor numérico
    @return True o False
    """
    
    if not x:
        return True

    try:
        float(x)
        return False
    except ValueError:
        return True


class Input(object):
    """
    Dialogo de entrada de datos
    """
    @classmethod
    def getText(cls, question, prevtxt="", title="Pineboo"):
        """
        Recoge texto
        @param question. Label del diálogo.
        @param prevtxt. Valor inicial a especificar en el campo
        @param title. Título del diálogo
        @return cadena de texto recogida
        """
        text, ok = QtWidgets.QInputDialog.getText(None, title,
                                                  question, QtWidgets.QLineEdit.Normal, prevtxt)
        if not ok:
            return None
        return text

    @classmethod
    def getItem(cls, question, items_list=[], title="Pineboo", editable=True):
        """
        Recoge Item
        @param question. Label del diálogo.
        @param item_list. Lista de items.
        @param title. Título del diálogo.
        @return item, Item seleccionado.
        """
        
        text, ok = QtWidgets.QInputDialog.getItem(None, title, question, items_list, 0, editable)
        if not ok:
            return None
        return text


class NumberEdit(QtWidgets.QWidget):
    """
    Diálogo para recoger un número
    """

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
        """
        Recoge el valor
        @return valor actual
        """
        return self.line_edit.text

    def setValue(self, value):
        """
        Setea el valor dado como valor actual
        @param value. Nuevo valor actual
        """
        self.line_edit.setText(value)

    def getDecimals(self):
        """
        Recoge decimales
        @return decimales del valor actual
        """
        return self.line_edit.validator().decimals()

    def setDecimals(self, decimals):
        """
        Setea decimales al valor actual
        @param decimals. Decimales a setear
        """
        self.line_edit.validator().setDecimals(int(decimals))


    def setMinimum(self, min):
        """
        Setea valor mínimo
        @param min. Valor mínimo especificable
        """
        self.line_edit.validator().setBottom(float(min))

    def getMinimum(self):
        """
        Recoge el valor mínimo seteable
        @return valor mínimo seteable
        """
        return self.line_edit.validator().bottom()


    def getMaximum(self):
        """
        Recoge el valor máximo seteable
        @return Valor máximo posible
        """
        return self.line_edit.validator().top()

    def setMaximum(self, max):
        """
        Setea valor máximo
        @param max. Valor maximo especificable
        """
        return self.line_edit.validator().setTop(float(max))

    def getLabel(self):
        """
        Recoge la etiqueta del diálogo
        @return texto de la etiqueta del diálogo
        """
        self.label_line_edit.text()

    def setLabel(self, label):
        """
        Setea la nueva etiqueta del diálogo
        @param label. Etiqueta del diálogo
        """
        self.label_line_edit.setText(label)

    label = property(getLabel, setLabel)
    value = property(getValue, setValue)
    decimals = property(getDecimals, setDecimals)
    mimimum = property(getMinimum, setMinimum)
    maximum = property(getMaximum, setMaximum)


def qsa_length(obj):
    """
    Parser para recoger el length de un campo
    @param obj, objeto a obtener longitud
    @return longitud del objeto
    """
    if hasattr(obj, "length"):
        if isinstance(obj.length, int):
            return obj.length
        else:
            return obj.length()
    
    else:
        return len(obj)


def qsa_text(obj):
    """
    Parser para recoger valor text de un objeto dado
    @param obj. Objeto a procesar
    @return Valor de text o text()
    """
    try:
        return obj.text()
    except Exception:
        return obj.text


def RegExp(strRE):
    """
    Regexp
    @param strRE. Cadena de texto
    @return valor procesado
    """
    if strRE[-2:] == "/g":
        strRE = strRE[:-2]

    if strRE[:1] == "/":
        strRE = strRE[1:]

    return qsaRegExp(strRE)


class qsaRegExp(object):

    strRE_ = None
    result_ = None

    def __init__(self, strRE):
        print("Nuevo Objeto RegExp de " + repr(strRE))
        self.strRE_ = repr(strRE)

    def search(self, text):
        print("Buscando " + self.strRE_ + " en " + text)
        self.result_ = re.search(self.strRE_, text)
    
    def replace(self, target , new_value):
        return re.sub(r"%s" % self.strRE_, new_value, target)

    def cap(self, i):
        if self.result_ is None:
            return None

        try:
            return self.result_.group(i)
        except Exception:
            return None
    
    def __str__(self):
        print("devolviendo", self.strRE_)
        return self.strRE_


@total_ordering
class Date(object):
    """
    Case que gestiona un objeto tipo Date
    """
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
                    tmp = date_.split("-")
                    if len(tmp[2]) == 4:
                        from pineboolib.fllegacy.flutil import FLUtil
                        date_ = FLUtil().dateDMAtoAMD(date_)
                    
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

    def toString(self):
        """
        Retorna una cadena de texto con los datos de fecha y hora.
        @return cadena de texto con los datos de fecha y hora
        """
        
        texto = "%s-%s-%sT%s:%s:%s" % (self.date_.toString("yyyy"), self.date_.toString("MM"), self.date_.toString(
            "dd"), self.time_.toString("hh"), self.time_.toString("mm"), self.time_.toString("ss"))
        return texto

    def getYear(self):
        """
        Retorna el año
        @return año
        """
        return self.date_.year()
    
    def setYear(self, yyyy):
        """
        Setea un año dado
        @param yyyy. Año a setear
        """
        if yyyy is not None:
            self.date_ = QtCore.QDate.fromString("%s-%s-%s" % (yyyy, self.date_.toString("MM"), self.date_.toString("dd")), "yyyy-MM-dd")

    def getMonth(self):
        """
        Retorna el mes
        @return mes
        """
        return self.date_.month()
    
    def setMonth(self, mm):
        """
        Setea un mes dado
        @param mm. Mes a setear
        """
        
        if mm is not None:
            if len(str(mm)) == 1:
                mm = "0%s" % mm
            self.date_ = QtCore.QDate.fromString("%s-%s-%s" % (self.date_.toString("yyyy"), mm, self.date_.toString("dd")), "yyyy-MM-dd")
    

    def getDay(self):
        """
        Retorna el día
        @return día
        """
        return self.date_.day()
    
    def setDay(self, dd):
        """
        Setea un dia dado
        @param dd. Dia a setear
        """
        if dd is not None:
            if len(str(dd)) == 1:
                dd = "0%s" % dd
                
            self.date_ = QtCore.QDate.fromString("%s-%s-%s" % (self.date_.toString("yyyy"), self.date_.toString("mm"), dd), "yyyy-MM-dd")
    

    def getHours(self):
        """
        Retorna horas
        @return horas
        """
        return self.time_.hour()

    def getMinutes(self):
        """
        Retorna minutos
        @return minutos
        """
        return self.time_.minute()

    def getSeconds(self):
        """
        Retorna segundos
        @return segundos
        """
        return self.time_.second()

    def getMilliseconds(self):
        """
        Retorna milisegundos
        @return milisegundos
        """
        return self.time_.msec()
    
    def setDate(self, date):
        """
        Se especifica fecha
        @param date. Fecha a setear
        """
        year_ = self.date_.toString("yyyy")
        month_ = self.date_.toString("MM")
        day_ = str(date)
        if len(day_) == 1:
            day_ = "0" + day_
         
        str_ = "%s-%s-%s" % (year_, month_, day_)
        self.date_ = QtCore.QDate.fromString(str_, "yyyy-MM-dd") 
    
    def addDays(self, d):
        """
        Se añaden dias a una fecha dada
        @param d. Dias a sumar (o restar) a la fecha dada
        @return nueva fecha calculada
        """
        return Date(self.date_.addDays(d).toString("yyyy-MM-dd"))
    
    def addMonths(self, m):
        """
        Se añaden meses a una fecha dada
        @param m. Meses a sumar (o restar) a la fecha dada
        @return nueva fecha calculada
        """
        return Date(self.date_.addMonths(m).toString("yyyy-MM-dd"))
    
    def addYears(self, y):
        """
        Se añaden años a una fecha dada
        @param y. Años a sumar (o restar) a la fecha dada
        @return nueva fecha calculada
        """
        return Date(self.date_.addYears(y).toString("yyyy-MM-dd"))      

    @classmethod
    def parse(cls, value):
        return QtCore.QDate.fromString(value, "yyyy-MM-dd")
    
    def __str__(self):
        return self.toString()
    
    def __le__(self, other):
        """
        Esta función junto con total_ordering, sirve para poder comparar este tipo con otro similar
        return Boolean. True si este objeto es menor que el comparado
        """
        return self.toString() < other.toString()




class Dir(object):
    """
    Gestiona un directorio
    """
    path_ = None
    Files = "*.*"

    from os.path import expanduser
    home = expanduser("~")

    def __init__(self, path=None):
        self.path_ = path

    def entryList(self, patron, type_=None):
        """
        Lista de ficheros que coinciden con un patron dado
        @param patron. Patron a usa para identificar los ficheros
        @return lista con los ficheros que coinciden con el patrón
        """
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

    def fileExists(self, file_name):
        """
        Retorna si existe el fichero dado o no
        @param file_name. Nombre del fichero
        @return Boolean. Si existe el ficehro o no.
        """
        return os.path.exists(file_name)

    def cleanDirPath(name):
        """
        Devuelve la ruta del ficehro limpia
        @param name. Rtua del ficehro a limpiar
        @return ruta limpia
        """
        return str(name)

    @decorators.Deprecated
    def convertSeparators(filename):
        """
        Retona el mismo valor
        """
        return filename

    def setCurrent(self, val=None):
        """
        Especifica la ruta como path actual
        @param val. Ruta especificada
        """ 
        os.chdir(val or filedir("."))

    def mkdir(self, name=None):
        """
        Crea un directorio
        @param name. Nombre de la ruta a crear
        """
        if name is None:
            name = self.path_
        try:
            os.stat(name)
        except:
            os.mkdir(name)


class File(QtCore.QFile):
    """
    Para gestionar un fichero
    """
    fichero = None
    mode = None
    path = None

    from PyQt5.Qt import QIODevice
    ReadOnly = QIODevice.ReadOnly
    WriteOnly = QIODevice.WriteOnly
    ReadWrite = QIODevice.ReadWrite
    encode_ = None
    last_seek = None

    def __init__(self, rutaFichero, encode=None):
        self.encode_ = "iso-8859-15"
        if isinstance(rutaFichero, tuple):
            rutaFichero = rutaFichero[0]
        self.fichero = str(rutaFichero)
        super().__init__(rutaFichero)
        self.path = os.path.dirname(self.fichero)
        
        if encode is not None:
            self.encode_ = encode

    def read(self, byte = False):
        """
        Lee el fichero al completo
        @param byte. Especifica si se lee en modo texto o en bytes
        @retunr contenido del fichero
        """
        if isinstance(self, str):
            file_ = self
            encode = "iso-8859-15"
        else:
            file_ = self.fichero
            encode = self.encode_
        import codecs
        f = codecs.open(file_,"r" if not byte else "rb", encoding=encode)
        ret = ""
        for l in f:
            ret = ret + l

        f.close()
        return ret

    def write(self, data, length = -1):
        """
        Escribe datos en el fichero
        @param data. Valores a guardar en el fichero
        @param length. Tamaño de data. (No se usa)
        """
        if isinstance(self, str):
            file_ = self
            encode = "iso-8859-15"
        else:
            file_ = self.fichero
            encode = self.encode_

        import codecs
        f = codecs.open(file_, encoding=encode, mode="w+")
        f.write(data)
        f.close()

    def exists(name):
        """
        Comprueba si un fichero exite
        @param name. Nombre del fichero.
        @return boolean informando si existe o no el fichero.
        """
        return QtCore.QFile.exists(name)

    def isDir(dir_name):
        """
        Indica si la ruta data es un directorio
        @param. Nombre del directorio
        @return. boolean informando si la ruta dada es un directorio o no.
        """
        return os.path.isdir(dir_name)
    
    def isFile(file_name):
        """
        Indica si la ruta data es un fichero
        @param. Nombre del fichero
        @return. boolean informando si la ruta dada es un fichero o no.
        """
        return os.path.isfile(file_name)
        
    
    def getName(self):
        """
        Retorna el nombre del fichero
        @return Nombre del fichero
        """
        path_, file_name = os.path.split(self.fichero)
        return file_name

    
    def writeLine(self, data):
        """
        Escribe un nueva linea en un fichero
        @param data. Datos a añadir en el fichero
        """
        import codecs
        f = codecs.open(self.fichero, encoding=self.encode_, mode="a")
        f.write("%s\n" % data)
        f.close()
    
    def readLine(self):
        """
        Lee una linea de un fichero dado
        @return cadena de texto con los datos de la linea actual
        """
        if self.last_seek is None:
            self.last_seek = 0
        
        f = codecs.open(self.fichero,"r", encoding=self.encode_)
        ret = f.readline(self.last_seek)
        self.last_seek += 1
        f.close()
        return ret
        
    
    def readLines(self):
        """
        Lee todas las lineas de un fichero y devuelve un array
        @return array con las lineas del fichero.
        """
        ret = None
        import codecs
        f = codecs.open(self.fichero, encoding=self.encode_, mode="a")
        if self.last_seek is not None:
            f.seek(self.last_seek)
        ret = f.readlines()
        f.close()
        return ret
    
    def readByte(self):
        """
        Lee una linea (bytes) de un fichero dado
        @return Bytes con los datos de la linea actual
        """
        return self.read(True)
    
    def writeByte(self, data_b):
        """
        Escribe un nueva linea en un fichero
        @param data_b. Datos a añadir en el fichero
        """
            
        import codecs
        f = codecs.open(self.fichero, encoding=self.encode_, mode="wb+")
        f.write(data_b)
        f.close()
    
    def remove(self):
        """
        Borra el fichero dado
        @return Boolean . True si se ha borrado el fichero, si no False.
        """
        return super().remove()
        
    
    name = property(getName)


class QString(str):
    """
    Clase QString para simular la original que no existe en PyQt5
    """
    def mid(self, start, length=None):
        """
        Recoje una sub cadena a partir de una cadena
        @param start. Posición inicial
        @param length. Longitud de la cadena. Si no se especifica , es hasta el final
        @return sub cadena de texto.
        """ 
        if length is None:
            return self[start:]
        else:
            return self[start:start + length]


def debug(txt):
    """
    Mensajes debug en qsa
    @param txt. Mensaje.
    """
    logger.warn("---> " + ustr(txt))
