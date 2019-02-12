# -*- coding: utf-8 -*-
from pineboolib import decorators
from PyQt5 import QtCore
import pineboolib
from pineboolib.fllegacy.flsqlquery import FLSqlQuery
from pineboolib.fllegacy.flsettings import FLSettings
import platform
import hashlib
import datetime
import logging
logger = logging.getLogger(__name__)


class FLUtil(QtCore.QObject):
    """
    Clase con métodos, herramientas y utiles necesarios para ciertas operaciones.

    Es esta clase se encontrarán métodos genéricos que
    realizan operaciones muy específicas pero que
    son necesarios para ciertos procesos habituales
    en las distintas tareas a desempeñar en la gestión
    empresarial.

    @author InfoSiAL S.L.
    """

    progress_dialog_stack = []
    vecUnidades = ['', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve', 'diez', 'once', 'doce', 'trece',
                   'catorce', 'quince', 'dieciseis', 'diecisiete', 'dieciocho', 'diecinueve', 'veinte', 'veintiun', 'veintidos',
                   'veintitres', 'veinticuatro', 'veinticinco', 'veintiseis', 'veintisiete', 'veintiocho', 'veintinueve']

    vecDecenas = ['', '', '', 'treinta', 'cuarenta',
                  'cincuenta', 'sesenta', 'setenta', 'ochenta', 'noventa']
    vecCentenas = ['', 'ciento', 'doscientos', 'trescientos', 'cuatrocientos', 'quinientos', 'seiscientos',
                   'setecientos', 'ochocientos', 'novecientos']

    def deleteCascade(self, collector, field, sub_objs, using):
        for o in sub_objs:
            try:
                from pineboolib.fllegacy.flsqlcursor import FLSqlCursor
                cursor = FLSqlCursor(field.model._meta.db_table)
                cursor.select(field.model._meta.pk.name + "=" + str(o.pk))
                if cursor.next():
                    cursor.setModeAccess(cursor.Del)
                    if not cursor.commitBuffer():
                        raise Exception("No pudo eliminar " + str(field.model._meta.db_table) + " : " + str(o.pk))
            except Exception:
                raise Exception("No pudo eliminar " + str(field.model._meta.db_table) + " : " + str(o.pk))

    def partInteger(self, n):
        """
        Obtiene la parte entera de un número.

        Dado un número devuelve la parte entera correspondiente, es decir,
        cifras en la parte izquierda de la coma decimal.

        @param n Número del que obtener la parte entera. Debe ser positivo
        @return La parte entera del número, que puede ser cero
        """
        i, d = divmod(n, 1)
        return int(i)

    def partDecimal(self, n):
        """
        Obtiene la parte decimal de un número.

        Dado un número devuelve la parte decimal correspondiente, es decir,
        cifras en la parte derecha de la coma decimal
        @param n Número del que obtener la parte decimal. Debe ser positivo
        @return La parte decimal del número, que puede ser cero
        """
        i, d = divmod(n, 1)
        d = d * 100
        return int(d)

    def unidades(self, n):
        """
        Enunciado de las unidades de un número.

        @param n Número a tratar. Debe ser positivo
        """
        if n >= 0:
            return self.vecUnidades[n]
        else:
            raise ValueError("Parameter 'n' must be a positive integer")

    @decorators.NotImplementedWarn
    def utf8(self, s):
        """
        Pasa una cadena a codificación utf-8

        @param s: Cadena
        @return Cadena en formato UTF-8
        """
        return s

    def centenamillar(self, n):
        """
        Enunciado de las centenas de millar de un número.

        @param n Número a tratar. Debe ser positivo
        """
        buffer = ""
        if n < 0:
            raise ValueError("Param n must be positive integer")
        if n < 10000:
            buffer = self.decenasmillar(n)
            return buffer

        buffer = self.centenas(n / 1000)
        buffer = buffer + " mil "
        buffer = buffer + self.centenas(n % 1000)

        return buffer

    def decenas(self, n):
        """
        Enunciado de las decenas de un número.

        @param n Número a tratar. Debe ser positivo
        """
        buffer = ""

        if n < 0:
            raise ValueError("Param n must be positive integer")
        if n < 30:
            buffer = self.unidades(n)
        else:
            buffer = self.vecDecenas[self.partInteger(n / 10)]
            if n % 10:
                buffer = buffer + " y "
                buffer = buffer + self.unidades(n % 10)

        return buffer

    def centenas(self, n):
        """
        Enunciado de las centenas de un número.

        @param n Número a tratar. Debe ser positivo
        """
        buffer = ""
        if n < 0:
            raise ValueError("Param n must be positive integer")
        if n == 100:
            buffer = "cien"

        elif n < 100:
            buffer = self.decenas(n)
        else:
            buffer = buffer + self.vecCentenas[self.partInteger(n / 100)]
            buffer = buffer + " "
            buffer = buffer + self.decenas(n % 100)

        return buffer

    def unidadesmillar(self, n):
        """
        Enunciado de las unidades de millar de un número.

        @param n Número a tratar. Debe ser positivo
        """
        buffer = ""
        if n < 1000:
            buffer = ""

        if n / 1000 == 1:
            buffer = "mil "

        if n / 1000 > 1:
            buffer = self.unidades(n / 1000)
            buffer = buffer + " mil "

        buffer = buffer + self.centenas(n % 1000)

        return buffer

    def decenasmillar(self, n):
        """
        Enunciado de las decenas de millar de un número.

        @param n Número a tratar. Debe ser positivo
        """
        buffer = ""
        if n < 10000:
            buffer = self.unidadesmillar(n)
            return buffer

        buffer = self.decenas(n / 1000)
        buffer = buffer + " mil "
        buffer = buffer + self.centenas(n % 10000)
        return buffer

    def enLetra(self, n):
        """
        Obtiene la expresión en texto de como se enuncia un número, en castellano.

        Dado un número entero, devuelve su expresión en texto de como se
        enuncia de forma hablada; por ejemplo dado el número 130,
        devolverá la cadena de texto "ciento treinta".

        @param n Número a transladar a su forma hablada. Debe ser positivo
        @return Cadena de texto con su expresión hablada
        """
        buffer = ""
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

    @decorators.BetaImplementation
    def enLetraMoneda(self, n, m):
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

    @decorators.BetaImplementation
    def enLetraMonedaEuro(self, n):
        """
        Obtiene la expresión en texto de como se enuncia una cantidad monetaria, en castellano
        y en Euros.

        Dado un número doble, devuelve su expresión en texto de como se
        enuncia de forma hablada en euros; por ejemplo dado el número 130.25,
        devolverá la cadena de texto "ciento treinta euros con veinticinco céntimos".

        @param n Número a transladar a su forma hablada. Debe ser positivo
        @return Cadena de texto con su expresión hablada
        """
        # return enLetraMoneda(n, QT_TR_NOOP("euros"));
        return self.enLetraMoneda(n, "euros")

    def letraDni(self, n):
        """
        Obtiene la letra asociada al némero del D.N.I. español.

        @param n Numero de D.N.I
        @return Caracter asociado al núemro de D.N.I
        """
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        return letras[n % 23]

    def nombreCampos(self, tablename):
        """
        Obtiene la lista de nombres de campos de la tabla especificada.
        El primer string de la lista contiene el número de campos de la tabla

        @param tabla. Nombre de la tabla
        @return Lista de campos
        """
        from pineboolib.pncontrolsfactory import aqApp
        campos = aqApp.db().manager().metadata(tablename).fieldsNames()
        return [len(campos)] + campos

    def calcularDC(self, n):
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
        Tabla = [6, 3, 7, 9, 10, 5, 8, 4, 2, 1]

        DC = None
        Suma = 0
        nDigitos = len(n) - 1

        ct = 1

        while ct <= len(n):
            Suma = Suma + (Tabla[nDigitos] * (int(n[ct - 1]) - 0))
            nDigitos = nDigitos - 1
            ct = ct + 1

        DC = 11 - (Suma % 11)
        if DC == 11:
            DC = 0
        elif DC == 10:
            DC = 1

        char = chr(DC + 48)
        return char

    def dateDMAtoAMD(self, f):
        """
        Convierte fechas del tipo DD-MM-AAAA, DD/MM/AAAA o
        DDMMAAAA al tipo AAAA-MM-DD.

        @param  f Cadena de texto con la fecha a transformar
        @return Cadena de texto con la fecha transformada
        """
        dia_ = None
        mes_ = None
        ano_ = None

        if not f:
            return None

        f = str(f)

        if f.find("T") > -1:
            f = f[:f.find("T")]

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

    def dateAMDtoDMA(self, f):
        """
        Convierte fechas del tipo AAAA-MM-DD, AAAA-MM-DD o
        AAAAMMDD al tipo DD-MM-AAAA.

        @param  f Cadena de texto con la fecha a transformar
        @return Cadena de texto con la fecha transformada
        """
        dia_ = None
        mes_ = None
        ano_ = None
        array_ = str(f).split("-")
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

    @decorators.BetaImplementation
    def formatoMiles(self, s):
        """
        Formatea una cadena de texto poniéndole separadores de miles.

        La cadena que se pasa se supone que un número, convirtiendola
        con QString::toDouble(), si la cadena no es número el resultado es imprevisible.

        @param s Cadena de texto a la que se le quieren poder separadores de miles
        @return Devuelve la cadena formateada con los separadores de miles
        """
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

    def translate(self, group, text_):
        """
        Traducción de una cadena al idioma local

        Se hace una llamada a la función tr() de la clase QObject para hacer la traducción.
        Se utiliza para traducciones desde fuera de objetos QObject

        @param group Contexto en el que se encuentra la cadena, generalmente se refiere a la clase en la que está definida
        @param s Cadena de texto a traducir
        @return Devuelve la cadena traducida al idioma local
        """
        from pineboolib.fllegacy.fltranslations import FLTranslate
        
        if text_ == "MetaData":
            a = group
            group = text_
            text_ = a
            
        
        
        text_ = text_.replace(" % ", " %% ")
        
        return str(FLTranslate(group, text_))

    @decorators.NotImplementedWarn
    def numCreditCard(self, num):
        """
        Devuelve si el numero de tarjeta de Credito es valido.

        El parametro que se pasa es la cadena de texto que contiene el numero de tarjeta.

        @param num Cadena de texto con el numero de tarjeta
        @return Devuelve verdadero si el numero de tarjeta es valido
        """
        pass

    def nextCounter(self, *args, **kwargs):
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

            _len = int(field.length())
            cadena = None

            q = FLSqlQuery(None, cursor_.db().connectionName())
            q.setForwardOnly(True)
            q.setTablesList(tMD.name())
            q.setSelect(name)
            q.setFrom(tMD.name())
            q.setWhere("LENGTH(%s)=%s" % (name, _len))
            q.setOrderBy(name + " DESC")

            if not q.exec_():
                return None

            maxRange = 10 ** _len
            numero = maxRange

            while numero >= maxRange:
                if not q.next():
                    numero = 1
                    break
                
                try:
                    numero = int(q.value(0))
                    numero = numero + 1
                except Exception:
                    pass
                

            if type_ == "string":
                cadena = str(numero)

                if len(cadena) < _len:
                    relleno = None
                    relleno = cadena.rjust(_len, '0')
                    cadena = relleno

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

            where = "length(%s)=%d AND substring(%s FROM 1 for %d) = '%s'" % (
                name, field.length(), name, len(serie), serie)
            select = "substring(%s FROM %d) as %s" % (
                name, len(serie) + 1, name)
            q = FLSqlQuery(None, cursor_.db().connectionName())
            q.setForwardOnly(True)
            q.setTablesList(tMD.name())
            q.setSelect(select)
            q.setFrom(tMD.name())
            q.setWhere(where)
            q.setOrderBy(name + " DESC")

            if not q.exec_():
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

                # res = serie + cadena
                return cadena

            return None

    @decorators.NotImplementedWarn
    def nextSequence(self, nivel, secuencia, ultimo):
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
        pass

    def isFLDefFile(self, head):
        """
        Para comprobar si la cabecera de un fichero de definición corresponde
        con las soportadas por AbanQ.

        Este método no sirve para los scripts, sólo para los ficheros de definición;
        mtd, ui, qry, xml, ts y kut.

        @param head Cadena de caracteres con la cabecera del fichero, bastaría
            con las tres o cuatro primeras linea del fichero no vacías
        @return TRUE si es un fichero soportado, FALSE en caso contrario
        """
        while head.startswith(" "):
            head = head[1:]
        
        ret = False
        
        if head.find("<!DOCTYPE UI>") == 0:
            ret = True
        elif head.find("<!DOCTYPE QRY>") == 0:
            ret = True
        elif head.find("<!DOCTYPE KugarTemplate") == 0:
            ret = True
        elif head.find("<!DOCTYPE TMD>") == 0:
            ret = True
        elif head.find("<!DOCTYPE TS>") == 0:
            ret = True
        elif head.find("<ACTIONS>") == 0:
            ret = True
        elif head.find("<jasperReport") == 0:
            ret = True

        return ret

    def addDays(self, fecha, offset):
        """
        Suma dias a una fecha.

        @param fecha Fecha con la que operar
        @param offset Numero de dias que sumar. Si es negativo resta dias
        @return Fecha con el desplazamiento de dias
        """
        from pineboolib.qsa import Date
        if isinstance(fecha, str):
            fecha = Date(fecha, "yyyy-MM-dd")
        if not isinstance(fecha, Date):
            logger.error("addDays: No reconozco el tipo de dato %s", type(fecha), stack_info=True)
            return None
        return fecha.addDays(offset)

    def addMonths(self, fecha, offset):
        """
        Suma meses a una fecha.

        @param fecha Fecha con la que operar
        @param offset Numero de meses que sumar. Si es negativo resta meses
        @return Fecha con el desplazamiento de meses
        """
        from pineboolib.qsa import Date
        if isinstance(fecha, str):
            fecha = Date(fecha)
        if not isinstance(fecha, Date):
            logger.error("addMonths: No reconozco el tipo de dato %s", type(fecha), stack_info=True)
            return None
        return fecha.addMonths(offset)

    def addYears(self, fecha, offset):
        """
        Suma años a una fecha.

        @param fecha Fecha con la que operar
        @param offset Numero de años que sumar. Si es negativo resta años
        @return Fecha con el desplazamiento de años
        """
        from pineboolib.qsa import Date
        if isinstance(fecha, str):
            fecha = Date(fecha)
        if not isinstance(fecha, Date):
            logger.error("addYears: No reconozco el tipo de dato %s", type(fecha), stack_info=True)
        return fecha.addYears(offset)

    def daysTo(self, d1, d2):
        """
        Diferencia de dias desde una fecha a otra.

        @param d1 Fecha de partida
        @param d2 Fecha de destino
        @return Número de días entre d1 y d2. Será negativo si d2 es anterior a d1.
        """
        from pineboolib.qsa import Date
        from datetime import date
        if isinstance(d1, Date):
            d1 = d1.toString()

        if isinstance(d1, date):
            d1 = str(d1)

        if isinstance(d1, str):
            d1 = d1[:10]

        if not isinstance(d1, str) or d1 is "":
            if d1 not in (None, ""):
                logger.error("daysTo: No reconozco el tipo de dato %s", type(d1))
            return None

        if isinstance(d2, Date):
            d2 = d2.toString()

        if isinstance(d2, date):
            d2 = str(d2)

        if isinstance(d2, str):
            d2 = d2[:10]

        if not isinstance(d2, str) or d2 is "":
            if d2 not in (None, ""):
                logger.error("daysTo: No reconozco el tipo de dato %s", type(d2))
            return None
        d1 = datetime.datetime.strptime(d1, "%Y-%m-%d").date()
        d2 = datetime.datetime.strptime(d2, "%Y-%m-%d").date()
        return (d2 - d1).days

    def buildNumber(self, v, tipo, partDecimal):
        """
        Construye un string a partir de un número, especificando el formato y precisión

        @param v. Número a convertir a QString
        @param tipo. Formato del número
        @param partDecimal. Precisión (número de cifras decimales) del número

        @return Cadena que contiene el número formateado
        """
        if not v:
            v = 0
        
        v = str(v)
        if v.endswith("5"):
           v += "1" 
        
        ret = round(float(v)) if partDecimal == 0 else round(float(v), partDecimal)
        """    
        d = float(v) * 10**partDecimal
        d = round(d)
        d = d / 10**partDecimal
        # ret.setNum(d, tipo, partDecimal)
        # formamos algo de este tipo: '{:.3f}'.format(34.14159265358979)
        # '34.142'
        f = '{:.' + str(partDecimal) + 'f}'
        ret = f.format(d)
        if tipo == "float":
            ret = float(ret)
        return ret
        """        
        return ret
        
    def readSettingEntry(self, key, def_=u""):
        """
        Lee el valor de un setting en el directorio de la instalación de AbanQ

        @param key. Clave identificadora del setting
        @param def. Valor por defecto en el caso de que el setting no esté establecido
        @param ok. Indicador de que la lectura es correcta

        @return Valor del setting
        """
        return FLSettings().readEntry(key, def_)

    def writeSettingEntry(self, key, value):
        """
        Establece el valor de un setting en el directorio de instalación de AbanQ

        @param key. Clave identificadora del setting
        @param Valor del setting

        @return Indicador de si la escritura del settings se realiza correctamente
        """
        FLSettings().writeEntry(key, value)

    def readDBSettingEntry(self, key):
        """
        Lee el valor de un setting en la tabla flsettings

        @param key. Clave identificadora del setting

        @return Valor del setting
        """
        q = FLSqlQuery()
        q.setSelect("valor")
        q.setFrom("flsettings")
        q.setWhere("flkey = '%s'" % key)
        q.setTablesList("flsettings")
        if q.exec_() and q.first():
            return q.value(0)

        return None

    def writeDBSettingEntry(self, key, value):
        """
        Establece el valor de un setting en la tabla flsettings

        @param key. Clave identificadora del setting
        @param Valor del setting

        @return Indicador de si la escritura del settings se realiza correctamente
        """
        # result = False
        where = "flkey = '%s'" % key
        found = self.readDBSettingEntry(key)
        cursor = pineboolib.project.conn.cursor()
        if found is None:
            sql = "INSERT INTO flsettings (flkey, valor) VALUES ('%s', '%s')" % (
                key, value)
        else:
            sql = "UPDATE flsettings SET valor = '%s' WHERE %s" % (
                value, where)
        try:
            cursor.execute(sql)

        except Exception:
            logger.exception("writeDBSettingEntry: Error al ejecutar SQL: %s", sql)
            # FIXME: Quito el rollback porque esta función no inicia transacción
            # cursor.rollback()
            return False

        cursor.close()
        return True

    def roundFieldValue(self, value, table_name, field_name):
        """
        Redondea un valor en función de la precisión especificada para un campo tipo double de la base de datos

        @param n. Número a redondear
        @param table. Nombre de la tabla
        @param field. Nombre del campo

        @return Número redondeado
        """
        from pineboolib.pncontrolsfactory import aqApp
        tmd = aqApp.db().manager().metadata(table_name)
        if tmd is None:
            return 0
        fmd = tmd.field(field_name)
        return self.buildNumber(value, 'float', fmd.partDecimal()) if fmd is not None else 0
    
    def sqlSelect(self, f, s, w, tL=None, size=0, connName="default"):
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
        if w is None or w == "":
            return False

        q = FLSqlQuery(None, connName)
        if tL:
            q.setTablesList(tL)
        else:
            q.setTablesList(f)

        q.setSelect(s)
        q.setFrom(f)
        q.setWhere(w)
        # q.setForwardOnly(True)
        if not q.exec_():
            return False

        if q.next():
            valor = q.value(0)
            #if isinstance(valor, datetime.date):
            #    valor = str(valor)
            return valor

        return False

    def quickSqlSelect(self, f, s, w, connName="default"):
        """
        Versión rápida de sqlSelect. Ejecuta directamente la consulta sin realizar comprobaciones.
        Usar con precaución.
        """
        if not w:
            sql = "select " + s + " from " + f
        else:
            sql = "select " + s + " from " + f + " where " + w

        q = FLSqlQuery(None, connName)
        if not q.exec_(sql):
            return False

        return q.value(0) if q.first() else False

    def sqlInsert(self, t, fL, vL, connName="default"):
        """
        Realiza la inserción de un registro en una tabla mediante un objeto FLSqlCursor

        @param t Nombre de la tabla
        @param fL Lista separada con comas de los nombres de los campos
        @param vL Lista separada con comas de los valores correspondientes
        @param connName Nombre de la conexion
        @return Verdadero en caso de realizar la inserción con éxito, falso en cualquier otro caso
        """
        from pineboolib.fllegacy.flsqlcursor import FLSqlCursor

        fL = fL.split(",")
        vL = vL.split(",")

        if not len(fL) == len(vL):
            return False

        c = FLSqlCursor(t, True, connName)
        c.setModeAccess(FLSqlCursor.Insert)
        c.refreshBuffer()

        i = 0
        for f in fL:
            if vL[i] is None:
                c.bufferSetNull(f)
            else:
                c.setValueBuffer(f, vL[i])

            i = i + 1

        return c.commitBuffer()

    def sqlUpdate(self, t, fL, vL, w, connName="default"):
        """
        Realiza la modificación de uno o más registros en una tabla mediante un objeto FLSqlCursor

        @param t Nombre de la tabla
        @param fL Lista separada con comas de los nombres de los campos
        @param vL Lista separada con comas de los valores correspondientes
        @param w Sentencia where para identificar los registros a editar.
        @param connName Nombre de la conexion
        @return Verdadero en caso de realizar la inserción con éxito, falso en cualquier otro caso
        """
        from pineboolib.fllegacy.flsqlcursor import FLSqlCursor
        c = FLSqlCursor(t, True, connName)
        c.select(w)
        c.setForwardOnly(True)
        while c.next():

            c.setModeAccess(FLSqlCursor.Edit)
            c.refreshBuffer()

            if isinstance(fL, list):
                i = 0
                for f in fL:
                    c.setValueBuffer(f, vL[i])
                    i = i + 1
            else:
                c.setValueBuffer(fL, vL)

            if not c.commitBuffer():
                return False

        return True

    def sqlDelete(self, t, w, connName="default"):
        """
        Borra uno o más registros en una tabla mediante un objeto FLSqlCursor

        @param t Nombre de la tabla
        @param w Sentencia where para identificar los registros a borrar.
        @param connName Nombre de la conexion
        @return Verdadero en caso de realizar la inserción con éxito, falso en cualquier otro caso
        """
        from pineboolib.fllegacy.flsqlcursor import FLSqlCursor
        c = FLSqlCursor(t, True, connName)

        # if not c.select(w):
        #     return False
        c.select(w)
        c.setForwardOnly(True)

        while c.next():
            c.setModeAccess(FLSqlCursor.Del)
            c.refreshBuffer()
            if not c.commitBuffer():
                return False

        return True

    @decorators.NotImplementedWarn
    def quickSqlDelete(self, t, w, connName="default"):
        """
        Versión rápida de sqlDelete. Ejecuta directamente la consulta sin realizar comprobaciones y sin disparar señales de commits.
        Usar con precaución.
        """
        pass

    def createProgressDialog(self, title, steps, id_="default"):
        """
        Crea un diálogo de progreso

        @param l Label del diálogo
        @param tS Número total de pasos a realizar
        """
        from PyQt5 import QtWidgets
        
        pd_widget = QtWidgets.QProgressDialog(str(title), str(
            self.translate("scripts", "Cancelar")), 0, steps)
        self.__class__.progress_dialog_stack.append(pd_widget)
        QtWidgets.qApp.processEvents()
        return pd_widget

    def destroyProgressDialog(self, id_="default"):
        """
        Destruye el diálogo de progreso
        """
        pd_widget = self.__class__.progress_dialog_stack[-1]
        del self.__class__.progress_dialog_stack[-1]
        pd_widget.hide()
        pd_widget.close()

    def setProgress(self, step_number, id_="default"):
        """
        Establece el grado de progreso del diálogo

        @param p Grado de progreso
        """
        from PyQt5 import QtWidgets
        
        pd_widget = self.__class__.progress_dialog_stack[-1]
        pd_widget.setValue(step_number)
        QtWidgets.qApp.processEvents()

    def setLabelText(self, l, id_="default"):
        """
        Cambia el texto de la etiqueta del diálogo

        @param l Etiqueta
        """
        from PyQt5 import QtWidgets
        
        pd_widget = self.__class__.progress_dialog_stack[-1]
        pd_widget.setLabelText(str(l))
        QtWidgets.qApp.processEvents()

    def setTotalSteps(self, tS, id_="default"):
        """
        Establece el número total de pasos del diálogo

        @param ts Número total de pasos
        """
        from PyQt5 import QtWidgets
        
        pd_widget = self.__class__.progress_dialog_stack[-1]
        pd_widget.setRange(0, tS)
        QtWidgets.qApp.processEvents()

    def domDocumentSetContent(self, doc, content):
        """
        Establece el contenido de un documento XML.

        Establece un documento DOM a partir del XML. Chequea errores, y si existen
        muestra el error encontrado y la linea y columna donde se encuentra.

        @param doc Documento DOM a establecer
        @param content Contenido XML
        @return FALSE si hubo fallo, TRUE en caso contrario
        """
        if not content:
            logger.warn("Se ha intentado cargar un fichero XML vacío", stack_info=False)
            return False

        ErrMsg = ""
        errLine = 0
        errColumn = 0

        # if not doc.setContent(content, ErrMsg, errLine, errColumn):
        if not doc.setContent(content):
            logger.warn("Error en fichero XML.\nError : %s\nLinea : %s\nColumna : %s", ErrMsg, errLine, errColumn)
            return False

        return True

    def sha1(self, str_):
        if str_ is None:
            str_ = ""
        """
        Obtiene la clave SHA1 de una cadena de texto.

        @param str Cadena de la que obtener la clave SHA1
        @return Clave correspondiente en digitos hexadecimales
        """
        sha_ = hashlib.new("sha1", str_.encode())
        st = "%s" % sha_.hexdigest()
        st = st.upper()
        return st

    @decorators.NotImplementedWarn
    def usha1(self, data, _len):
        pass

    @decorators.NotImplementedWarn
    def snapShotUI(self, n):
        """
        Obtiene la imagen o captura de pantalla de un formulario.

        @param n Nombre del fichero que contiene la descricpción del formulario.
        """
        pass

    @decorators.NotImplementedWarn
    def saveSnapShotUI(self, n, pathFile):
        """
        Salva en un fichero con formato PNG la imagen o captura de pantalla de un formulario.

        @param n Nombre del fichero que contiene la descricpción del formulario.
        @param pathFile Ruta y nombre del fichero donde guardar la imagen
        """
        pass

    @decorators.NotImplementedWarn
    def flDecodeType(self, fltype):
        """
        Decodifica un tipo de AbanQ a un tipo QVariant

        @param fltype Tipo de datos de AbanQ.
        @return Tipo de datos QVariant.
        """
        pass

    @decorators.NotImplementedWarn
    def saveIconFile(self, data, pathFile):
        """
        Guarda la imagen de icono de un botón de un formulario en un ficher png. Utilizado para documentación

        @param data Contenido de la imagen en una cadena de caracteres
        @param pathFile Ruta completa al fichero donde se guadará la imagen
        """
        pass

    def getIdioma(self):
        """
        Devuelve una cadena de dos caracteres con el código de idioma del sistema

        @return Código de idioma del sistema
        """
        return QtCore.QLocale().name()[:2]

    def getOS(self):
        """
        Devuelve el sistema operativo sobre el que se ejecuta el programa

        @return Código del sistema operativo (WIN32, LINUX, MACX)
        """
        if platform.system() == "Windows":
            return "WIN32"
        elif platform.system() == "Linux" or platform.system() == "Linux2":
            return "LINUX"
        elif platform.system() == "Darwin":
            return "MACX"
        else:
            return platform.system()

    @decorators.NotImplementedWarn
    def serialLettertoNumber(self, letter):
        """
        Esta función convierte una cadena que es una serie de letras en su correspondiente valor numerico.

        @param letter Cadena con la serie.
        @return Una cadena pero que contiene numeros.
        """
        pass

    @decorators.NotImplementedWarn
    def serialNumbertoLetter(self, number):
        """
        Esta función convierte un numero a su correspondiente secuencia de Letras.

        @param number Número a convertir
        """
        pass

    @decorators.NotImplementedWarn
    def findFiles(self, paths, filter_="*", breakOnFirstMatch=False):
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
        pass

    def execSql(self, sql, connName="default"):
        """
        Uso interno
        """
        conn_ = pineboolib.project.conn.useConn(connName)
        cur = conn_.cursor()
        try:
            cur.execute(sql)
            conn_.conn.commit()
            return True
        except Exception:
            logger.exception("execSql: Error al ejecutar la SQL: %s", sql)
            return False

    @decorators.NotImplementedWarn
    def savePixmap(self, data, filename, format_):
        """
        Guarda imagen Pixmap en una ruta determinada.

        @param data Contenido de la imagen en una cadena de caracteres
        @param filename: Ruta al fichero donde se guardará la imagen
        @param fmt Indica el formato con el que guardar la imagen
        @author Silix
        """
        pass
    
    def fieldType(self, fn, tn, conn_name = 'default'):
        """
        Retorna el tipo numérico de un campo
        @param field_name. Nombre del campo
        @param table_name. Nombre de la tabla que contiene el campo
        @param conn_name. Nombre de la conexión a usar
        @return id del tipo de campo
        """
        from pineboolib.pncontrolsfactory import aqApp
        conn = aqApp.db().useConn(conn_name)
        mtd = conn.manager().metadata(tn)
        
        return None if mtd is None else mtd.fieldType(fn)
    
    def fieldLength(self, fn, tn, conn_name = 'default'):
        """
        Retorna la longitud de un campo
        @param fn. Nombre del campo
        @param tn. Nombre de la tabla que contiene el campo
        @param conn_name. Nombre de la conexión a usar
        @return longitud del campo solicitado
        """
        if tn is None:
            return 0
        
        from pineboolib.pncontrolsfactory import aqApp
        conn = aqApp.db().useConn(conn_name)
        mtd = conn.manager().metadata(tn)
        
        return 0 if mtd is None else mtd.fieldLength(fn)
        
        
    
    def fieldNameToAlias(self, fn, tn, conn_name = 'default'):
        """
        Retorna el alias de un campo a partir de su nombre
        @param fn. Nombre del campo
        @param tn. Nombre de la tabla que contiene el campo
        @param conn_name. Nombre de la conexión a usar
        @return Alias del campo especificado
        """
        if tn is None:
            return fn
        
        from pineboolib.pncontrolsfactory import aqApp
        conn = aqApp.db().useConn(conn_name)
        mtd = conn.manager().metadata(tn)
        
        return fn if mtd is None else mtd.fieldNameToAlias(fn)

    
    def tableNameToAlias(self, tn, conn_name= 'default'):
        """
        Retorna el nombre de una tabla a partir de su alias
        @param tn. Nombre de la tabla
        @param conn_name. Nombre de la conexión a usar
        @return Alias de la tabla especificada
        """
        
        if tn is None:
            return None
        
        from pineboolib.pncontrolsfactory import aqApp
        conn = aqApp.db().useConn(conn_name)
        mtd = conn.manager().metadata(tn)

        return None if mtd is None else mtd.alias()
    
    def fieldAliasToName(self, an, tn, conn_name= 'default'):
        
        """
        Retorna el nombre de un campo a partir de su alias
        @param fn. Nombre del campo
        @param tn. Nombre de la tabla que contiene el campo
        @param conn_name. Nombre de la conexión a usar
        @return Alias del campo especificado
        """
        
        if tn is None:
            return an
        
        from pineboolib.pncontrolsfactory import aqApp
        conn = aqApp.db().useConn(conn_name)
        mtd = conn.manager().metadata(tn)
    
        return an if mtd is None else mtd.fieldAliasToName(an)
        
        
    def fieldAllowNull(self, fn , tn, conn_name = 'default'):
        """
        Retorna si el campo permite dejarse en blanco
        @param fn. Nombre del campo
        @param tn. Nombre de la tabla que contiene el campo
        @param conn_name. Nombre de la conexión a usar
        @return Boolean. Si acepta o no dejar en blanco el valor del campo
        """
        
        if tn is None:
            return False
        
        from pineboolib.pncontrolsfactory import aqApp
        conn = aqApp.db().useConn(conn_name)
        mtd = conn.manager().metadata(tn)
        
        return False if mtd is None else mtd.fieldAllowNull(fn)
    
    def fieldIsPrimaryKey(self, fn, tn, conn_name='default'):
        """
        Retorna si el campo es clave primaria de la tabla
        @param fn. Nombre del campo
        @param tn. Nombre de la tabla que contiene el campo
        @param conn_name. Nombre de la conexión a usar
        @return Boolean. Si es clave primaria o no
        """
        if tn is None:
            return False
        
        from pineboolib.pncontrolsfactory import aqApp
        conn = aqApp.db().useConn(conn_name)
        mtd = conn.manager().metadata(tn)
        
        return False if mtd is None else mtd.fieldIsPrimaryKey(fn)
    
    def fieldIsCompoundKey(self, fn, tn, conn_name='default'):
        """
        Retorna si el campo es clave compuesta de la tabla
        @param fn. Nombre del campo
        @param tn. Nombre de la tabla que contiene el campo
        @param conn_name. Nombre de la conexión a usar
        @return Boolean. Si es clave compuesta o no
        """
        if tn is None:
            return False
        
        from pineboolib.pncontrolsfactory import aqApp
        conn = aqApp.db().useConn(conn_name)
        mtd = conn.manager().metadata(tn)
        
        if mtd is None:
            return False
        
        return False if field is None else field.isCompoundKey()
    
    
    def fieldDefaultValue(self, fn, tn, conn_name = 'default'):
        """
        Retorna el valor por defecto de un campo
        @param fn. Nombre del campo
        @param tn. Nombre de la tabla que contiene el campo
        @param conn_name. Nombre de la conexión a usar
        @return Valor por defecto del campo
        """
        if tn is None:
            return None #return QVariant
        
        from pineboolib.pncontrolsfactory import aqApp
        conn = aqApp.db().useConn(conn_name)
        mtd = conn.manager().metadata(tn)
        
        if mtd is None:
            return None #return QVariant
        
        field = mtd.field(fn)
        if field is None:
            return None #return QVariant
        
        return field.defaultValue()
    
    
    def formatValue(self, t, v, upper, conn_name = 'default'):
        """
        Retorna valor formateado
        @param t. Tipo de campo
        @param v. Valor del campo
        @param conn_name. Nombre de la conexión a usar
        @return Valor formateado
        """
        
        from pineboolib.pncontrolsfactory import aqApp
        conn = aqApp.db().useConn(conn_name)    
        return conn.manager().formatValue(t, v, upper)
        
        
    
    
        
        
    def nameUser(self):
        from pineboolib.pncontrolsfactory import SysType
        return SysType().nameUser()

    def userGroups(self):
        from pineboolib.pncontrolsfactory import SysType
        return SysType().userGroups()


    def isInProd(self):
        from pineboolib.pncontrolsfactory import SysType
        return SysType().isInProd()


    def request(self):
        from pineboolib.pncontrolsfactory import SysType
        return SysType().request()


    def nameBD(self):
        from pineboolib.pncontrolsfactory import SysType
        return SysType().nameBD()        
        
    
