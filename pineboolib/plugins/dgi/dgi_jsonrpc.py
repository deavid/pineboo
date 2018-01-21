# # -*- coding: utf-8 -*-

from pineboolib.plugins.dgi.dgi_schema import dgi_schema
from pineboolib.utils import Struct
from flup.server.fcgi import WSGIServer

dependences = []

try:
    import flup
except ImportError:
    print(traceback.format_exc())
    dependences.append("flup-py3")


if len(dependences) > 0:
    print()
    print("HINT: Dependencias incumplidas:")
    for dep in dependences:
        print("HINT: Instale el paquete %s e intente de nuevo" % dep)
    print()
    sys.exit(32)

arrayControles = {}

class dgi_jsonrpc(dgi_schema):

    _fcgiCall = None
    _fcgiSocket = None

    def __init__(self):
        super(dgi_fcgi, self).__init__()  # desktopEnabled y mlDefault a True
        self._name = "jsonrpc"
        self._alias = "JSON-RPC"
        self.setUseDesktop(True)
        self.setUseMLDefault(True)
        self.setLocalDesktop(False)
        self.showInitBanner()
        self._listenSocket = "/tmp/pineboo-JSONRPC.socket"

    def extraProyectInit(self):
        print("=============================================")
        print("============ EXTRA PROJECT INIT =============")
        print("=============================================")
        print("JSON-RPC:INFO: Listening socket", self._listenSocket)
        par_ = parser()
        WSGIServer(par_.query, bindAddress=self._fcgiSocket).run()
        print("End load extraProjectInit")

    def setParameter(self, param):
        self._listenSocket = param

class parser(object):

    def query(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        print("FCGI:INFO: Processing '%s' ..." % environ["QUERY_STRING"])

class FLLineEdit(object):

    _tipo = None
    _partDecimal = 0
    _partInteger = 0
    _maxValue = None
    autoSelect = True
    _name = None
    _longitudMax = None
    _parent = None
    _name = None
    lostFocus = QtCore.pyqtSignal()
    parentObj_ = None

    def __init__(self, parent, name=None):
        self.parentObj_ = parent
        self._name = self.parentObj_.objectName()
        
        obj_ = Struct()
        obj_.text = None
        obj_.label = self.parentObj_.textLabelDB
        arrayControles[self._name] = obj_
        
        self._name = name
        if isinstance(parent.fieldName_, str):
            self._fieldName = parent.fieldName_
            self._tipo = parent.cursor_.metadata().fieldType(self._fieldName)
            self._partDecimal = parent.partDecimal_
            self._partInteger = parent.cursor_.metadata().field(self._fieldName).partInteger()
            self._longitudMax = parent.cursor_.metadata().field(self._fieldName).length()
            # self.textChanged.connect(self.controlFormato)
            self._parent = parent

    def __getattr__(self, name):
        return DefFun(self, name)

    def controlFormato(self):
        #texto = str(super(FLLineEdit, self).text())
        denegarCambio_ = False
        denegarCambioEnteros_ = False
        cambiarComa_ = False
        decimales_ = None
        posComa_ = -1

        if texto == "" or texto == None:
            return
        """
        if self._tipo == "int" or self._tipo == "uint":
            if not texto is None:
                try:
                    float(decimales_)
                except:
                        denegarCambio_ = True
            
            texto = texto.replace(",",".")
            try:
                posComa_ = texto.index(".")
            except:
                if posComa_ > -1:
                    denegarCambio_ = True
            
        """
        if self._tipo == "string":
            if len(texto) > int(self._longitudMax):
                denegarCambio_ = True

        if self._tipo == "double":

            texto_old = texto
            if (QtCore.QLocale().decimalPoint() == ","):
                texto = texto.replace(".", ",")
            else:
                texto = texto.replace(",", ".")

            if not texto_old == texto:
                cambiarComa_ = True

            try:
                posComa_ = texto.index(".")
                #print("Coma encontrada en pos", posComa_, denegarCambio_)
            except:
                #print("Coma no encontrada", denegarCambio_)
                a = 1

            if posComa_ > -1:
                decimales_ = texto[posComa_ + 1:]

                if len(decimales_) > int(self._partDecimal):
                    #print("Parte decimal (%s) se pasa de %s" % (decimales_ , self._partDecimal))
                    denegarCambio_ = True

            enteros_ = texto

            if posComa_ > -1:
                enteros_ = texto[:posComa_]

            #print("enteros ...", enteros_)
            if len(enteros_) > int(self._partInteger):
                #print("Parte entera (%s) se pasa de %s" % (enteros_ , self._partInteger))
                denegarCambioEnteros_ = True

            #print("Decimales =", decimales_ , type(decimales_))
            if not decimales_ is None:
                try:
                    float(decimales_)
                except:
                    #print("Decimal esta mal", decimales_, len(decimales_))
                    if len(decimales_) > 0:
                        denegarCambio_ = True

            #print("Enteros =", enteros_, type(enteros_))
            try:
                float(enteros_)
            except:
                #print("Entero esta mal")
                denegarCambioEnteros_ = True
            # if not decimales_.isdecimal():
                #denegarCambio_ = True

            # if not enteros_.isdecimal():
                #denegarCambioEnteros_ = True

        #print("Procesado final", texto, denegarCambio_)

        if denegarCambio_ == True:
            texto = texto[0:len(texto) - 1]
            arrayControles[self._name].text = texto

        if denegarCambioEnteros_ == True and not decimales_ == None:
            texto = "%s%s%s" % (
                enteros_[0:len(enteros_) - 1], QtCore.QLocale().decimalPoint(), decimales_)
            arrayControles[self._name].text = texto
        elif denegarCambioEnteros_ == True and decimales_ == None:
            texto = enteros_[0:len(enteros_) - 1]
            arrayControles[self._name].text = texto

        if cambiarComa_ == True:
            arrayControles[self._name].text = texto

    def setText(self, texto, b=True):
        if self._maxValue:
            if self._maxValue < int(texto):
                texto = self._maxValue

        texto = str(texto)

        # Miramos si le falta digitos a la parte decimal ...
        if self._tipo == "double" and len(texto) > 0:
            if texto == "0":
                d = 0
                texto = "0."
                while d < self._partDecimal:
                    texto = texto + "0"
                    d = d + 1

            i = None
            l = len(texto) - 1
            try:
                i = texto.index(".")
            except:
                pass

            if i:
                #print("Posicion de . (%s) de %s en %s" % (i, l, texto))
                f = (i + self._partDecimal) - l
                #print("Part Decimal = %s , faltan %s" % (self._partDecimal, f))
                while f > 0:
                    texto = texto + "0"
                    f = f - 1

        arrayControles[self._name].text = texto
        self.textChanged.emit(texto)

    def text(self):
        texto = arrayControles[self._name].text

        if texto is "":
            texto = None

        if texto is None:
            if self._tipo == "string":
                texto = ""

            elif self._tipo == "double":
                d = 0
                texto = "0."
                while d < self._partDecimal:
                    texto = texto + "0"
                    d = d + 1

        return str(texto)

    """
    Especifica un valor máximo para el text (numérico)
    """

    def setMaxValue(self, value):
        self._maxValue = value

    """
    def focusInEvent(self, *f):
        print("focus in!! ---> ", f)
        if self._tipo == "double" or self._tipo == "int" or self._tipo == "Uint":
            self.blockSignals(True)
            s = self.text()
            super(FLLineEdit,self).setText(s)
            self.blockSignals(False)
        if self.autoSelect and self.selectedText().isEmpty() and not self.isReadOnly():
            self.selectAll()

        QtGui.QLineEdit.focusInEvent(f)

    def focusOutEvent(self, f):
        print("Adios --->", f)
        if self._tipo == "double" or self._tipo == "int" or self._tipo == "Uint":
            self.setText(self.text())

        super(FLLineEdit,self).focusOutEvent(self, f)

    """

