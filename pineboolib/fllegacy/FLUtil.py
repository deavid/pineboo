# -*- coding: utf-8 -*-

from pineboolib.flcontrols import ProjectClass
from pineboolib import decorators
#from PyQt4.QtCore import QString
from PyQt4 import QtCore, QtGui
import pineboolib
from pineboolib.utils import DefFun
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from pineboolib.fllegacy.FLSettings import FLSettings


class FLUtil(ProjectClass):

    progress_dialog_stack = []
    vecUnidades = ['','uno','dos','tres','cuatro','cinco','seis', 'siete','ocho','nueve','diez','once','doce','trece',
                   'catorce','quince','dieciseis','diecisiete','dieciocho','diecinueve','veinte','veintiun','veintidos',
                   'veintitres','veinticuatro','veinticinco','veintiseis','veintisiete','veintiocho','veintinueve']

    vecDecenas = ['','','','treinta','cuarenta','cincuenta','sesenta','setenta','ochenta','noventa']
    vecCentenas = ['','ciento','doscientos','trescientos','cuatrocientos','quinientos','seiscientos',
                   'setecientos','ochocientos','novecientos']



    """
    Clase con métodos, herramientas y utiles necesarios para ciertas operaciones.

    Es esta clase se encontrarán métodos genéricos que
    realizan operaciones muy específicas pero que
    son necesarios para ciertos procesos habituales
    en las distintas tareas a desempeñar en la gestión
    empresarial.

    @author InfoSiAL S.L.
    """

    def __getattr__(self, name): return DefFun(self, name)

    """
    Obtiene la parte entera de un número.

    Dado un número devuelve la parte entera correspondiente, es decir,
    cifras en la parte izquierda de la coma decimal.

    @param n Número del que obtener la parte entera. Debe ser positivo
    @return La parte entera del número, que puede ser cero
    """
    def partInteger(self, n):
        i, d = divmod(n, 1)
        return int(i)

    """
    Obtiene la parte decimal de un número.

    Dado un número devuelve la parte decimal correspondiente, es decir,
    cifras en la parte derecha de la coma decimal
    @param n Número del que obtener la parte decimal. Debe ser positivo
    @return La parte decimal del número, que puede ser cero
    """
    def partDecimal(self, n):
        i, d = divmod(n, 1)
        d = d * 100
        return int(d)

    """
    Enunciado de las unidades de un número.

    @param n Número a tratar. Debe ser positivo
    """
    def unidades(self, n):
        if n > 0:
            return self.vecUnidades[n]

    """
    Pasa una cadena a codificación utf-8

    @param s: Cadena
    @return Cadena en formato UTF-8
    """
    @decorators.NotImplementedWarn
    def utf8(self, s):
        return s

    """
    Enunciado de las centenas de millar de un número.

    @param n Número a tratar. Debe ser positivo
    """
    def centenamillar(self, n):
        buffer = None

        if n < 10000:
            buffer = self.decenasmillar(n)
            return buffer

        buffer = self.centenas(n / 1000)
        buffer = buffer + " mil "
        buffer = buffer + self.centenas(n % 1000)

        return buffer


    """
    Enunciado de las decenas de un número.

    @param n Número a tratar. Debe ser positivo
    """
    def decenas(self, n):
        buffer = None

        if n < 30:
            buffer = self.unidades(n)
        else:
            buffer = self.vecDecenas[self.partInteger(n / 10)]
            if n % 10:
                buffer = buffer + " y "
                buffer = buffer + self.unidades(n % 10)


        return buffer

    """
    Enunciado de las centenas de un número.

    @param n Número a tratar. Debe ser positivo
    """
    def centenas(self, n):
        buffer = None
        if n == 100:
            buffer = "cien"

        elif n < 100:
            buffer = self.decenas(n)
        else:
            buffer = buffer + self.vecCentenas[self.partInteger(n / 100)]
            buffer = buffer + " "
            buffer = buffer + self.decenas( n % 100)

        return buffer

    """
    Enunciado de las unidades de millar de un número.

    @param n Número a tratar. Debe ser positivo
    """
    def unidadesmillar(self, n):
        buffer = None
        if n < 1000:
            buffer = ""

        if n/1000 == 1:
            buffer = "mil "

        if n/1000 > 1:
            buffer = self.unidades(n / 1000)
            buffer = buffer + " mil "

        buffer = buffer + self.centenas( n % 1000)

        return buffer



    """
    Enunciado de las decenas de millar de un número.

    @param n Número a tratar. Debe ser positivo
    """
    def decenasmillar(self, n):
        buffer = None
        if n < 10000:
            buffer = self.unidadesmillar(n)
            return buffer

        buffer = self.decenas(n / 1000)
        buffer = buffer + " mil "
        buffer = buffer + self.centenas( n % 10000)
        return buffer

    """
    Obtiene la expresión en texto de como se enuncia un número, en castellano.

    Dado un número entero, devuelve su expresión en texto de como se
    enuncia de forma hablada; por ejemplo dado el número 130,
    devolverá la cadena de texto "ciento treinta".

    @param n Número a transladar a su forma hablada. Debe ser positivo
    @return Cadena de texto con su expresión hablada
    """
    def enLetra(self, n):
        buffer = None
        if n > 1000000000:
            buffer = "Sólo hay capacidad hasta mil millones"
            return buffer

        if n < 1000000:
            buffer = self.centenamillar(n)
            return buffer
        else:
            if n / 1000000 == 1:
                buffer = "un millon"
            else:
                buffer = self.centenas(n / 1000000)
                buffer = buffer + " millones "

        buffer = buffer + self.centenamillar(n % 1000000)
        return buffer.upper()

    """
    Obtiene la expresión en texto de como se enuncia una cantidad monetaria, en castellano
    y en cualquier moneda indicada.

    Dado un número doble, devuelve su expresión en texto de como se
    enuncia de forma hablada en la moneda indicada; por ejemplo dado el número 130.25,
    devolverá la cadena de texto "ciento treinta 'moneda' con veinticinco céntimos".

    @param n Número a transladar a su forma hablada. Debe ser positivo
    @param m Nombre de la moneda
    @return Cadena de texto con su expresión hablada
    """
    @decorators.BetaImplementation
    def enLetraMoneda(self, n, m):
        nTemp = n * -1.00 if n < 0.00 else n
        entero = self.partInteger(nTemp)
        decimal = self.partDecimal(nTemp)
        res = ""

        if entero > 0:
            res = self.enLetra(entero) + " " + m

        if entero > 0 and decimal > 0:
            # res += QString(" ") + QT_TR_NOOP("con") + " " + enLetra(decimal) + " " + QT_TR_NOOP("céntimos");
            res += " " + "con" + " " + self.enLetra(decimal) + " " + "céntimos"

        if entero <= 0 and decimal > 0:
            # res = enLetra(decimal) + " " + QT_TR_NOOP("céntimos");
            res = self.enLetra(decimal) + " " + "céntimos"

        if n < 0.00:
            # res = QT_TR_NOOP("menos") + QString(" ") + res;
            res = "menos" + " " + res

        return res.upper()

    """
    Obtiene la expresión en texto de como se enuncia una cantidad monetaria, en castellano
    y en Euros.

    Dado un número doble, devuelve su expresión en texto de como se
    enuncia de forma hablada en euros; por ejemplo dado el número 130.25,
    devolverá la cadena de texto "ciento treinta euros con veinticinco céntimos".

    @param n Número a transladar a su forma hablada. Debe ser positivo
    @return Cadena de texto con su expresión hablada
    """
    @decorators.BetaImplementation
    def enLetraMonedaEuro(self, n):
        # return enLetraMoneda(n, QT_TR_NOOP("euros"));
        return self.enLetraMoneda(n, "euros")

    """
    Obtiene la letra asociada al némero del D.N.I. español.

    @param n Numero de D.N.I
    @return Caracter asociado al núemro de D.N.I
    """
    def letraDni(self, n):
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        return letras[n % 23]

    """
    Obtiene la lista de nombres de campos de la tabla especificada.
    El primer string de la lista contiene el número de campos de la tabla

    @param tabla. Nombre de la tabla
    @return Lista de campos
    """
    def nombreCampos(self, tablename):
        campos = pineboolib.project.conn.manager().metadata(tablename).fieldsNames()
        return [len(campos)] + campos

    """
    Obtiene el número del digito de control, para cuentas bancarias.

    Los números de las cuentas corrientes se organizan de la forma siguiente:

    4 Digitos----->Código del banco   (ej. 0136 Banco Arabe español)
    4 Digitos----->Código de la oficina
    1 Digito de control------>de los 8 primeros digitos
    1 Digito de control------>del número de cuenta (de los 10 ultimos digitos)
    10 Digitos del número de la cuenta

    Para comprobar el numero de cuenta se pasa primero los 8 primeros digitos
    obteniendo asi el primer digito de control, después se pasan los 10 digitos
    del número de la cuenta obteniendo el segundo digito de control.

    @param n Número del que se debe obtener el dígito de control
    @return Caracter con el dígito de control asociado al número dado
    """
    @decorators.NotImplementedWarn
    def calcularDC(self, n):
        pass

    """
    Convierte fechas del tipo DD-MM-AAAA, DD/MM/AAAA o
    DDMMAAAA al tipo AAAA-MM-DD.

    @param  f Cadena de texto con la fecha a transformar
    @return Cadena de texto con la fecha transformada
    """
    def dateDMAtoAMD(self, f):
        dia_ = None
        mes_ = None
        ano_ = None
        
        f = str(f)
        
        array_ = f.split("-")
        if len(array_) == 3:
            dia_ = array_[0]
            mes_ = array_[1]
            ano_ = array_[2]
        else:
            array_ = f.split("/")
            if len(array_) == 3:
                dia_ = array_[0]
                mes_ = array_[1]
                ano_ = array_[2]
            else:
                dia_ = f[0:2]
                mes_ = f[2:2]
                ano_ = f[4:4]
         
            
        retorno = "%s-%s-%s" % (ano_, mes_, dia_)
        return retorno

    """
    Convierte fechas del tipo AAAA-MM-DD, AAAA-MM-DD o
    AAAAMMDD al tipo DD-MM-AAAA.

    @param  f Cadena de texto con la fecha a transformar
    @return Cadena de texto con la fecha transformada
    """
    
    def dateAMDtoDMA(self, f):
        dia_ = None
        mes_ = None
        ano_ = None
        
        array_ = f.split("-")
        if len(array_) == 3:
            ano_ = array_[0]
            mes_ = array_[1]
            dia_ = array_[2]
        else:
            array_ = f.split("/")
            if len(array_) == 3:
                ano_ = array_[0]
                mes_ = array_[1]
                dia_ = array_[2]
            else:
                ano_ = f[0:4]
                mes_ = f[4:2]
                dia_ = f[6:2]
         
            
        retorno = "%s-%s-%s" % (dia_, mes_, ano_)
        return retorno
    """
    Formatea una cadena de texto poniéndole separadores de miles.

    La cadena que se pasa se supone que un número, convirtiendola
    con QString::toDouble(), si la cadena no es número el resultado es imprevisible.

    @param s Cadena de texto a la que se le quieren poder separadores de miles
    @return Devuelve la cadena formateada con los separadores de miles
    """
    @decorators.BetaImplementation
    def formatoMiles(self, s):
        s = str(s)
        decimal = ''
        entera = ''
        ret = ''
        # dot = QApplication::tr(".")
        dot = '.'
        neg = s[0] == '-'

        if '.' in s:
            # decimal = QApplication::tr(",") + s.section('.', -1, -1)
            aStr = s.split('.')
            decimal = ',' + aStr[-1]
            entera = aStr[-2].replace('.', '')
        else:
            entera = s

        if neg:
            entera.replace('-', '')

        length = len(entera)

        while length > 3:
            ret = dot + entera[-3:] + ret
            entera = entera[:-3]
            length = len(entera)

        ret = entera + ret + decimal

        if neg:
            ret = '-' + ret

        return ret

    """
    Traducción de una cadena al idioma local

    Se hace una llamada a la función tr() de la clase QObject para hacer la traducción.
    Se utiliza para traducciones desde fuera de objetos QObject

    @param contexto Contexto en el que se encuentra la cadena, generalmente se refiere a la clase en la que está definida
    @param s Cadena de texto a traducir
    @return Devuelve la cadena traducida al idioma local
    """
    @decorators.BetaImplementation
    def translate(self, group, string):
        return str(string)
        # return qApp->translate(contexto, s);

    """
    Devuelve si el numero de tarjeta de Credito es valido.

    El parametro que se pasa es la cadena de texto que contiene el numero de tarjeta.

    @param num Cadena de texto con el numero de tarjeta
    @return Devuelve verdadero si el numero de tarjeta es valido
    """
    @decorators.NotImplementedWarn
    def numCreditCard(self, num):
        pass

    """
    Este metodo devuelve el siguiente valor de un campo tipo contador de una tabla.

    Este metodo es muy util cuando se insertan registros en los que
    la referencia es secuencial y no nos acordamos de cual fue el ultimo
    numero usado. El valor devuelto es un QVariant del tipo de campo es
    el que se busca la ultima referencia. Lo más aconsejable es que el tipo
    del campo sea 'String' porque así se le puede dar formato y ser
    usado para generar un código de barras. De todas formas la función
    soporta tanto que el campo sea de tipo 'String' como de tipo 'double'.

    @param name Nombre del campo
    @param cursor_ Cursor a la tabla donde se encuentra el campo.
    @return Qvariant con el numero siguiente.
    @author Andrés Otón Urbano.
    """

    """
    dpinelo: Este método es una extensión de nextCounter pero permitiendo la introducción de una primera
    secuencia de caracteres. Es útil cuando queremos mantener diversos contadores dentro de una misma tabla.
    Ejemplo, Tabla Grupo de clientes: Agregamos un campo prefijo, que será una letra: A, B, C, D.
    Queremos que la numeración de los clientes sea del tipo A00001, o B000023. Con esta función, podremos
    seguir usando los métodos counter cuando agregamos esa letra.

    Este metodo devuelve el siguiente valor de un campo tipo contador de una tabla para una serie determinada.

    Este metodo es muy util cuando se insertan registros en los que
    la referencia es secuencial según una secuencia y no nos acordamos de cual fue el último
    numero usado. El valor devuelto es un QVariant del tipo de campo es
    el que se busca la ultima referencia. Lo más aconsejable es que el tipo
    del campo sea 'String' porque así se le puede dar formato y ser
    usado para generar un código de barras. De todas formas la función
    soporta tanto que el campo sea de tipo 'String' como de tipo 'double'.

    @param serie serie que diferencia los contadores
    @param name Nombre del campo
    @param cursor_ Cursor a la tabla donde se encuentra el campo.
    @return Qvariant con el numero siguiente.
    @author Andrés Otón Urbano.
    """
    def nextCounter(self, *args, **kwargs):

        if len(args) == 2:
            name = args[0]
            cursor_ = args[1]

            if not cursor_:
                return None

            tMD = cursor_.metadata()
            if not tMD:
                return None

            field = tMD.field(name)
            if not field:
                return None

            type_ = field.type()

            if not type_ == "string" and not not type_ == "double":
                return None

            _len = field.length()
            cadena = None

            q = FLSqlQuery(None, cursor_.db().connectionName())
            q.setForwardOnly(True)
            q.setTablesList(tMD.name())
            q.setSelect(name)
            q.setFrom(tMD.name())
            q.setWhere("LENGTH(%s)=%d" % (name, _len))
            q.setOrderBy(name + " DESC")

            if not q.exec():
                return None

            maxRange = 10 ** _len
            numero = maxRange

            while numero >= maxRange:
                if not q.next():
                    numero = 1
                    break

                numero = float(q.value(0))
                numero = numero + 1


            if type_ == "string":
                cadena = str(numero)
                if len(cadena) < _len:
                    relleno = None
                    relleno = cadena.rjust(_len - len(cadena), '0')
                    cadena = str + cadena

                return cadena

            if type_ == "double":
                return numero

            return None

        else:
            serie = args[0]
            name = args[1]
            cursor_ = args[2]

            if not cursor_:
                return None

            tMD = cursor_.metadata()
            if not tMD:
                return None

            field = tMD.field(name)
            if not field:
                return None

            type_ = field.type()
            if not type_ == "string" and not type_ == "double":
                return None

            _len = field.length() - len(serie)
            cadena = None

            where = "length(%s)=%d AND substring(%s FROM 1 for %d) = '%s'" % (name, field.length(), name, len(serie), serie)
            select = "substring(%s FROM %d) as %s" % (name, len(serie) + 1, name)
            q = FLSqlQuery(None, cursor_.db().connectionName())
            q.setForwardOnly(True)
            q.setTablesList(tMD.name())
            q.setSelect(select)
            q.setFrom(tMD.name())
            q.setWhere(where)
            q.setOrderBy(name + " DESC")

            if not q.exec():
                return None

            maxRange = 10 ** _len
            numero = maxRange

            while numero >= maxRange:
                if not q.next():
                    numero = 1
                    break

                numero = float(q.value(0))
                numero = numero + 1

            if type_ == "string" or type_ == "double":
                cadena = numero
                if len(cadena) < _len:
                    relleno = cadena.rjust(_len - len(cadena), '0')
                    cadena = relleno + cadena

                #res = serie + cadena
                return cadena

            return None

    """
    Nos devuelve el siguiente valor de la secuencia segun la profundidad indicada por nivel.
    Para explicar el funcionamiento pondremos un ejemplo. Supongamos una secuencia tipo %A-%N.
    %A indica que se coloque en esa posicion una secuencia en letras y %N una secuencia en numero.
    La numeración de niveles va de derecha a izquierda asi el nivel 1 es %N y el nivel 2 %A.
    Si hacemos un nextSequence a nivel 1 el valor de vuelto será un %A que estubiera y un %N sumando 1
    al anterior. Si el nivel es 2 obtendremos un %A + 1, trasformado a letras, y todos los niveles a
    la derecha de este se ponen a 1 o su correspondiente en letra que seria A.

    @param nivel Indica la profundidad a la que se hace el incremento.
    @param secuencia Estructura de la secuencia.
    @param ultimo Ultimo valor de la secuencia para poder dar el siguiente valor.
    @return La secuencia en el formato facilitado.
    @author Andrés Otón Urbano
    """
    @decorators.NotImplementedWarn
    def nextSequence(self,  nivel, secuencia, ultimo):
        pass

    """
    Para comprobar si la cabecera de un fichero de definición corresponde
    con las soportadas por AbanQ.

    Este método no sirve para los scripts, sólo para los ficheros de definición;
    mtd, ui, qry, xml, ts y kut.

    @param head Cadena de caracteres con la cabecera del fichero, bastaría
        con las tres o cuatro primeras linea del fichero no vacías
    @return TRUE si es un fichero soportado, FALSE en caso contrario
    """
    @decorators.NotImplementedWarn
    def isFLDefFile(self, head):
        pass

    """
    Suma dias a una fecha.

    @param fecha Fecha con la que operar
    @param offset Numero de dias que sumar. Si es negativo resta dias
    @return Fecha con el desplazamiento de dias
    """
    def addDays(self, fecha, offset):
        if isinstance(fecha, str):
            fecha = QtCore.QDate.fromString(fecha)
        if not isinstance(fecha, QtCore.QDate):
            print("FATAL: FLUtil.addDays: No reconozco el tipo de dato %r" % type(fecha))
        return fecha.addDays(offset)

    """
    Suma meses a una fecha.

    @param fecha Fecha con la que operar
    @param offset Numero de meses que sumar. Si es negativo resta meses
    @return Fecha con el desplazamiento de meses
    """
    def addMonths(self, fecha, offset):
        if isinstance(fecha, str):
            fecha = QtCore.QDate.fromString(fecha)
        if not isinstance(fecha, QtCore.QDate):
            print("FATAL: FLUtil.addMonths: No reconozco el tipo de dato %r" % type(fecha))
        return fecha.addMonths(offset)

    """
    Suma años a una fecha.

    @param fecha Fecha con la que operar
    @param offset Numero de años que sumar. Si es negativo resta años
    @return Fecha con el desplazamiento de años
    """
    def addYears(self, fecha, offset):
        if isinstance(fecha, str):
            fecha = QtCore.QDate.fromString(fecha)
        if not isinstance(fecha, QtCore.QDate):
            print("FATAL: FLUtil.addYears: No reconozco el tipo de dato %r" % type(fecha))
        return fecha.addYears(offset)

    """
    Diferencia de dias desde una fecha a otra.

    @param d1 Fecha de partida
    @param d2 Fecha de destino
    @return Número de días entre d1 y d2. Será negativo si d2 es anterior a d1.
    """
    @decorators.NotImplementedWarn
    def daysTo(self, d1, d2):
        pass

    """
    Construye un string a partir de un número, especificando el formato y precisión

    @param v. Número a convertir a QString
    @param tipo. Formato del número
    @param partDecimal. Precisión (número de cifras decimales) del número

    @return Cadena que contiene el número formateado
    """
    @decorators.BetaImplementation
    def buildNumber(self, v, tipo, partDecimal):
        d = float(v) * 10**partDecimal
        d = round(d)
        d = d / 10**partDecimal
        # ret.setNum(d, tipo, partDecimal)
        # formamos algo de este tipo: '{:.3f}'.format(34.14159265358979)
        # '34.142'
        f = '{:.' + str(partDecimal) + 'f}'
        ret = f.format(d)
        return ret

    """
    Lee el valor de un setting en el directorio de la instalación de AbanQ

    @param key. Clave identificadora del setting
    @param def. Valor por defecto en el caso de que el setting no esté establecido
    @param ok. Indicador de que la lectura es correcta

    @return Valor del setting
    """

    def readSettingEntry(self, key, def_=None, ok=False):
        return FLSettings().readEntry(key, def_, ok)
    """
    Establece el valor de un setting en el directorio de instalación de AbanQ

    @param key. Clave identificadora del setting
    @param Valor del setting

    @return Indicador de si la escritura del settings se realiza correctamente
    """
    def writeSettingEntry(self, key, value):
        FLSettings().writeEntry( key, value)
    """
    Lee el valor de un setting en la tabla flsettings

    @param key. Clave identificadora del setting

    @return Valor del setting
    """
    def readDBSettingEntry(self, key):
        q = FLSqlQuery()
        q.setSelect("valor")
        q.setFrom("flsettings")
        q.setWhere("flkey = '%s'" % key)
        q.setTablesList("flsettings")
        if q.exec() and q.first():
            return q.value(0)
        
        return None

    """
    Establece el valor de un setting en la tabla flsettings

    @param key. Clave identificadora del setting
    @param Valor del setting

    @return Indicador de si la escritura del settings se realiza correctamente
    """
    @decorators.BetaImplementation
    def writeDBSettingEntry(self, key, value):
        result = None
        where = "flkey='%s'" % key
        found = self.sqlSelect("flsettings", "valor", where, "flsettings")
        if not found:
            result = self.sqlInsert("flsettings", "flkey,valor","%s,%s" % (key, value))
        else:
            result = self.sqlUpdate("flsettings", "valor", value, where)
        
        return result
        
    """
    Redondea un valor en función de la precisión especificada para un campo tipo double de la base de datos

    @param n. Número a redondear
    @param table. Nombre de la tabla
    @param field. Nombre del campo

    @return Número redondeado
    """
    @decorators.BetaImplementation
    def roundFieldValue(self, n, table, field):
        from pineboolib.fllegacy.FLSqlConnections import FLSqlConnections
        tmd = FLSqlConnections().database().manager().metadata(table)
        if not tmd:
            return 0
        fmd = tmd.field(field)
        if not fmd:
            if tmd and not tmd.inCache():
                del tmd
            return 0

        ret = self.buildNumber(n, 'f', fmd.partDecimal())
        if tmd and not tmd.inCache():
            del tmd
        return ret

    """
    Ejecuta una query de tipo select, devolviendo los resultados del primer registro encontrado

    @param f: Sentencia from de la query
    @param s: Sentencia select de la query, que será el nombre del campo a devolver
    @param w: Sentencia where de la query
    @param tL: Sentencia tableslist de la query. Necesario cuando en la sentencia from se incluya más de una tabla
    @param size: Número de líneas encontradas. (-1 si hay error)
    @param connName Nombre de la conexion
    @return Valor resultante de la query o falso si no encuentra nada.
    """
    
    def sqlSelect(self, f, s, w, tL=None, size=0, connName="default"):
        q = FLSqlQuery(None, connName)
        if tL:
            q.setTablesList(tL)
        else:
            q.setTablesList(f)

        q.setSelect(s)
        q.setFrom(f)
        q.setWhere(w)
        q.setForwardOnly(True)
        if not q.exec():
            return False

        if q.next():
            return q.value(0)

        if size:
            return False

    """
    Versión rápida de sqlSelect. Ejecuta directamente la consulta sin realizar comprobaciones.
    Usar con precaución.
    """
    @decorators.BetaImplementation
    def quickSqlSelect(self, f, s, w, connName="default"):
        from pineboolib.fllegacy.FLSqlConnections import FLSqlConnections
        if not w:
            sql = "select " + s + " from " + f
        else:
            sql = "select " + s + " from " + f + " where " + w
        q = FLSqlQuery(sql, FLSqlConnections().database(connName).db())
        return q.value(0) if q.next() else False

    """
    Realiza la inserción de un registro en una tabla mediante un objeto FLSqlCursor

    @param t Nombre de la tabla
    @param fL Lista separada con comas de los nombres de los campos
    @param vL Lista separada con comas de los valores correspondientes
    @param connName Nombre de la conexion
    @return Verdadero en caso de realizar la inserción con éxito, falso en cualquier otro caso
    """
    @decorators.BetaImplementation
    def sqlInsert(self, t, fL, vL, connName="default"):
        
        if not fL.len == vL:
            return False
        
        c = FLSqlCursor(t, True, connName)
        c.setModeAccess(FLSqlCursor.Insert)
        c.refreshBuffer()
        
        for f,v in (fL,vL):
            if v == "NULL":
                c.bufferSetNull(f)
            else:
                c.setValueBuffer(f,v)
        
        return c.commitBuffer()
        
        

    """
    Realiza la modificación de uno o más registros en una tabla mediante un objeto FLSqlCursor

    @param t Nombre de la tabla
    @param fL Lista separada con comas de los nombres de los campos
    @param vL Lista separada con comas de los valores correspondientes
    @param w Sentencia where para identificar los registros a editar.
    @param connName Nombre de la conexion
    @return Verdadero en caso de realizar la inserción con éxito, falso en cualquier otro caso
    """
    @decorators.NotImplementedWarn
    def sqlUpdate(self, t, fL, vL, w, connName="default"):
        pass
    """
    Borra uno o más registros en una tabla mediante un objeto FLSqlCursor

    @param t Nombre de la tabla
    @param w Sentencia where para identificar los registros a borrar.
    @param connName Nombre de la conexion
    @return Verdadero en caso de realizar la inserción con éxito, falso en cualquier otro caso
    """
    @decorators.BetaImplementation
    def sqlDelete(self, t, w, connName="default"):
        from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
        c = FLSqlCursor(t, True, connName)
        c.setForwardOnly(True)

        # if not c.select(w):
        #     return False
        c.select(w)

        while c.next():
            c.setModeAccess(FLSqlCursor.DEL)
            c.refreshBuffer()
            if not c.commitBuffer():
                return False

        return True

    """
    Versión rápida de sqlDelete. Ejecuta directamente la consulta sin realizar comprobaciones y sin disparar señales de commits.
    Usar con precaución.
    """
    @decorators.NotImplementedWarn
    def quickSqlDelete(self, t, w, connName="default"):
        pass
    """
    Crea un diálogo de progreso

    @param l Label del diálogo
    @param tS Número total de pasos a realizar
    """
    def createProgressDialog(self, title, steps, id_ = "default"):
        pd_widget = QtGui.QProgressDialog(title, self.translate("scripts","Cancelar"),0,steps)
        self.__class__.progress_dialog_stack.append(pd_widget)

    """
    Destruye el diálogo de progreso
    """
    def destroyProgressDialog(self, id_ = "default"):
        pd_widget = self.__class__.progress_dialog_stack[-1]
        del self.__class__.progress_dialog_stack[-1]
        pd_widget.hide()
        pd_widget.close()

    """
    Establece el grado de progreso del diálogo

    @param p Grado de progreso
    """
    def setProgress(self, step_number, id_ = "default"):
        pd_widget = self.__class__.progress_dialog_stack[-1]
        pd_widget.setValue(step_number)

    """
    Cambia el texto de la etiqueta del diálogo

    @param l Etiqueta
    """
    def setLabelText(self, l, id_ = "default"):
        pd_widget = self.__class__.progress_dialog_stack[-1]
        pd_widget.setLabelText(l)

    """
    Establece el número total de pasos del diálogo

    @param ts Número total de pasos
    """
    def setTotalSteps(self, tS, id_ = "default"):
        pd_widget = self.__class__.progress_dialog_stack[-1]
        pd_widget.setTotalSteps(tS)

    """
    Establece el contenido de un documento XML.

    Establece un documento DOM a partir del XML. Chequea errores, y si existen
    muestra el error encontrado y la linea y columna donde se encuentra.

    @param doc Documento DOM a establecer
    @param content Contenido XML
    @return FALSE si hubo fallo, TRUE en caso contrario
    """
    @decorators.NotImplementedWarn
    def domDocumentSetContent(self, doc, content):
        pass
    """
    Obtiene la clave SHA1 de una cadena de texto.

    @param str Cadena de la que obtener la clave SHA1
    @return Clave correspondiente en digitos hexadecimales
    """
    @decorators.NotImplementedWarn
    def sha1(self, str_):
        pass

    @decorators.NotImplementedWarn
    def usha1(self, data,_len):
        pass

    """
    Obtiene la imagen o captura de pantalla de un formulario.

    @param n Nombre del fichero que contiene la descricpción del formulario.
    """
    @decorators.NotImplementedWarn
    def snapShotUI(self, n):
        pass

    """
    Salva en un fichero con formato PNG la imagen o captura de pantalla de un formulario.

    @param n Nombre del fichero que contiene la descricpción del formulario.
    @param pathFile Ruta y nombre del fichero donde guardar la imagen
    """
    @decorators.NotImplementedWarn
    def saveSnapShotUI(self, n, pathFile):
        pass
    """
    Decodifica un tipo de AbanQ a un tipo QVariant

    @param fltype Tipo de datos de AbanQ.
    @return Tipo de datos QVariant.
    """
    @decorators.NotImplementedWarn
    def flDecodeType(self, fltype):
        pass
    """
    Guarda la imagen de icono de un botón de un formulario en un ficher png. Utilizado para documentación

    @param data Contenido de la imagen en una cadena de caracteres
    @param pathFile Ruta completa al fichero donde se guadará la imagen
    """
    @decorators.NotImplementedWarn
    def saveIconFile(self, data, pathFile):
        pass

    """
    Devuelve una cadena de dos caracteres con el código de idioma del sistema

    @return Código de idioma del sistema
    """
    @decorators.NotImplementedWarn
    def getIdioma(self):
        pass

    """
    Devuelve el sistema operativo sobre el que se ejecuta el programa

    @return Código del sistema operativo (WIN32, LINUX, MACX)
    """
    @decorators.NotImplementedWarn
    def getOS(self):
        pass

    """
    Esta función convierte una cadena que es una serie de letras en su correspondiente valor numerico.

    @param letter Cadena con la serie.
    @return Una cadena pero que contiene numeros.
    """
    @decorators.NotImplementedWarn
    def serialLettertoNumber(self, letter):
        pass

    """
    Esta función convierte un numero a su correspondiente secuencia de Letras.

    @param number Número a convertir
    """
    @decorators.NotImplementedWarn
    def serialNumbertoLetter(self, number):
        pass

    """
    Busca ficheros recursivamente en las rutas indicadas y según el patrón indicado

    Ejemplo:

    C++:
    QStringList filesFound = FLUtil::findFiles(QStringList() << "/home/user/Documents", "*.odt *.gif");
    for (QStringList::Iterator it = filesFound.begin(); it != filesFound.end(); ++it)
        qWarning(*it);

    QSA:
    var util = new FLUtil;
    var filesFound = util.findFiles( [ "/home/user/Documents" ], "*.odt *.gif");

    for(var i = 0; i < filesFound.length; ++i)
        debug(filesFound[i]);


    @param  paths   Rutas de búsqueda
    @param  filter  Patrón de filtrado para los ficheros. Admite varios separados por espacios "*.gif *.png".
                  Por defecto todos, "*"
    @param  breakOnFirstMatch Si es TRUE al encontrar el primer fichero que cumpla el patrón indicado, termina
                            la búsqueda y devuelve el nombre de ese fichero
    @return Lista de los nombres de los ficheros encontrados
    """
    @decorators.NotImplementedWarn
    def findFiles(self, paths, filter_ = "*", breakOnFirstMatch = False):
        pass

    """
    Uso interno
    """
    @decorators.NotImplementedWarn
    def execSql(self, sql, connName = "default"):
        pass
    """
    Guarda imagen Pixmap en una ruta determinada.

    @param data Contenido de la imagen en una cadena de caracteres
    @param filename: Ruta al fichero donde se guardará la imagen
    @param fmt Indica el formato con el que guardar la imagen
    @author Silix
    """
    @decorators.NotImplementedWarn
    def savePixmap(self, data, filename, format_):
        pass


from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from pineboolib.fllegacy.FLSettings import FLSettings
