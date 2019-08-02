# -*- coding: utf-8 -*-
import hashlib
import datetime

from PyQt5 import QtCore  # type: ignore

from pineboolib.application.qsatypes.sysbasetype import SysBaseType
from pineboolib.core import decorators
from pineboolib import logging

from typing import List, Optional, Union, Any, TYPE_CHECKING
from pineboolib.application.types import Date

if TYPE_CHECKING:
    from PyQt5.QtXml import QDomDocument  # type: ignore

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

    vecUnidades: List[str] = [
        "",
        "uno",
        "dos",
        "tres",
        "cuatro",
        "cinco",
        "seis",
        "siete",
        "ocho",
        "nueve",
        "diez",
        "once",
        "doce",
        "trece",
        "catorce",
        "quince",
        "dieciseis",
        "diecisiete",
        "dieciocho",
        "diecinueve",
        "veinte",
        "veintiun",
        "veintidos",
        "veintitres",
        "veinticuatro",
        "veinticinco",
        "veintiseis",
        "veintisiete",
        "veintiocho",
        "veintinueve",
    ]

    vecDecenas: List[str] = ["", "", "", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa"]
    vecCentenas: List[str] = [
        "",
        "ciento",
        "doscientos",
        "trescientos",
        "cuatrocientos",
        "quinientos",
        "seiscientos",
        "setecientos",
        "ochocientos",
        "novecientos",
    ]

    @staticmethod
    def deleteCascade(collector, field, sub_objs, using) -> None:  # FIXME TIPEADO
        for o in sub_objs:
            try:
                from pineboolib.application.database.pnsqlcursor import PNSqlCursor

                cursor = PNSqlCursor(field.model._meta.db_table)
                cursor.select(field.model._meta.pk.name + "=" + str(o.pk))
                if cursor.next():
                    cursor.setModeAccess(cursor.Del)
                    if not cursor.commitBuffer():
                        raise Exception("No pudo eliminar " + str(field.model._meta.db_table) + " : " + str(o.pk))
            except Exception:
                raise Exception("No pudo eliminar " + str(field.model._meta.db_table) + " : " + str(o.pk))

    @staticmethod
    def partInteger(n: float) -> int:
        """
        Obtiene la parte entera de un número.

        Dado un número devuelve la parte entera correspondiente, es decir,
        cifras en la parte izquierda de la coma decimal.

        @param n Número del que obtener la parte entera. Debe ser positivo
        @return La parte entera del número, que puede ser cero
        """
        i, d = divmod(n, 1)
        return int(i)

    @staticmethod
    def partDecimal(n: float) -> int:
        """
        Obtiene la parte decimal de un número.

        Dado un número devuelve la parte decimal correspondiente, es decir,
        cifras en la parte derecha de la coma decimal
        @param n Número del que obtener la parte decimal. Debe ser positivo
        @return La parte decimal del número, que puede ser cero
        """
        i, d = divmod(n, 1)
        d = round(d, 2)
        d = d * 100
        return int(d)

    @classmethod
    def unidades(cls, n: int) -> str:
        """
        Enunciado de las unidades de un número.

        @param n Número a tratar. Debe ser positivo
        """
        if n >= 0:
            return cls.vecUnidades[n]
        else:
            raise ValueError("Parameter 'n' must be a positive integer")

    @staticmethod
    @decorators.NotImplementedWarn
    def utf8(s: str) -> str:
        """
        Pasa una cadena a codificación utf-8

        @param s: Cadena
        @return Cadena en formato UTF-8
        """
        return s

    @classmethod
    def centenamillar(cls, n: int) -> str:
        """
        Enunciado de las centenas de millar de un número.

        @param n Número a tratar. Debe ser positivo
        """
        buffer = ""
        if n < 0:
            raise ValueError("Param n must be positive integer")
        if n < 10000:
            buffer = cls.decenasmillar(n)
            return buffer

        buffer = cls.centenas(n / 1000)
        buffer = buffer + " mil "
        buffer = buffer + cls.centenas(n % 1000)

        return buffer

    @classmethod
    def decenas(cls, n: Union[int, float]) -> str:
        """
        Enunciado de las decenas de un número.

        @param n Número a tratar. Debe ser positivo
        """
        buffer = ""

        if n < 0:
            raise ValueError("Param n must be positive integer")
        if n < 30:
            buffer = cls.unidades(int(n))
        else:
            buffer = cls.vecDecenas[cls.partInteger(n / 10)]
            if n % 10:
                buffer = buffer + " y "
                buffer = buffer + cls.unidades(int(n % 10))

        return buffer

    @classmethod
    def centenas(cls, n: Union[int, float]) -> str:
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
            buffer = cls.decenas(int(n))
        else:
            buffer = buffer + cls.vecCentenas[cls.partInteger(n / 100)]
            buffer = buffer + " "
            buffer = buffer + cls.decenas(int(n % 100))

        return buffer

    @classmethod
    def unidadesmillar(cls, n: int) -> str:
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
            buffer = cls.unidades(int(n / 1000))
            buffer = buffer + " mil "

        buffer = buffer + cls.centenas(int(n % 1000))

        return buffer

    @classmethod
    def decenasmillar(cls, n: int) -> str:
        """
        Enunciado de las decenas de millar de un número.

        @param n Número a tratar. Debe ser positivo
        """
        buffer = ""
        if n < 10000:
            buffer = cls.unidadesmillar(n)
            return buffer

        buffer = cls.decenas(n / 1000)
        buffer = buffer + " mil "
        buffer = buffer + cls.centenas(int(n % 10000))
        return buffer

    @classmethod
    def enLetra(cls, n: int) -> str:
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
            buffer = cls.centenamillar(int(n))
            return buffer
        else:
            if n / 1000000 == 1:
                buffer = "un millon"
            else:
                buffer = cls.centenas(int(n / 1000000))
                buffer = buffer + " millones "

        buffer = buffer + cls.centenamillar(int(n % 1000000))
        return buffer.upper()

    @classmethod
    @decorators.BetaImplementation
    def enLetraMoneda(cls, n: int, m: str) -> str:
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
        entero = cls.partInteger(nTemp)
        decimal = cls.partDecimal(nTemp)
        res = ""

        if entero > 0:
            res = cls.enLetra(entero) + " " + m

        if entero > 0 and decimal > 0:
            # res += QString(" ") + QT_TR_NOOP("con") + " " + enLetra(decimal) + " " + QT_TR_NOOP("céntimos");
            res += " " + "con" + " " + cls.enLetra(decimal) + " " + "céntimos"

        if entero <= 0 and decimal > 0:
            # res = enLetra(decimal) + " " + QT_TR_NOOP("céntimos");
            res = cls.enLetra(decimal) + " " + "céntimos"

        if n < 0.00:
            # res = QT_TR_NOOP("menos") + QString(" ") + res;
            res = "menos" + " " + res

        return res.upper()

    @classmethod
    @decorators.BetaImplementation
    def enLetraMonedaEuro(cls, n: int) -> str:
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
        return cls.enLetraMoneda(n, "euros")

    @classmethod
    def letraDni(cls, n: int) -> str:
        """
        Obtiene la letra asociada al némero del D.N.I. español.

        @param n Numero de D.N.I
        @return Caracter asociado al núemro de D.N.I
        """
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        return letras[n % 23]

    @classmethod
    def nombreCampos(cls, tablename: str) -> List[Union[str, int]]:
        """
        Obtiene la lista de nombres de campos de la tabla especificada.
        El primer string de la lista contiene el número de campos de la tabla

        @param tabla. Nombre de la tabla
        @return Lista de campos
        """

        from pineboolib.fllegacy.flapplication import aqApp

        campos = aqApp.db().manager().metadata(tablename).fieldNames()
        return [len(campos)] + campos

    @classmethod
    def calcularDC(cls, n: int) -> str:
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
        Tabla: List[int] = [6, 3, 7, 9, 10, 5, 8, 4, 2, 1]

        DC = None
        Suma = 0
        nDigitos = len(str(n)) - 1

        ct = 1

        while ct <= len(str(n)):
            valor_tabla: int = Tabla[nDigitos]
            valor_n = str(n)[ct - 1]
            Suma += valor_tabla * int(valor_n)
            nDigitos = nDigitos - 1
            ct = ct + 1

        DC = 11 - (Suma % 11)
        if DC == 11:
            DC = 0
        elif DC == 10:
            DC = 1

        char = chr(DC + 48)
        return char

    @classmethod
    def dateDMAtoAMD(cls, f) -> Optional[str]:
        """
        Convierte fechas del tipo DD-MM-AAAA, DD/MM/AAAA o
        DDMMAAAA al tipo AAAA-MM-DD.

        @param  f Cadena de texto con la fecha a transformar
        @return Cadena de texto con la fecha transformada
        """
        from pineboolib.application.utils.date_conversion import date_dma_to_amd

        return date_dma_to_amd(f)

    @classmethod
    def dateAMDtoDMA(cls, f) -> Optional[str]:
        """
        Convierte fechas del tipo AAAA-MM-DD, AAAA-MM-DD o
        AAAAMMDD al tipo DD-MM-AAAA.

        @param  f Cadena de texto con la fecha a transformar
        @return Cadena de texto con la fecha transformada
        """
        from pineboolib.application.utils.date_conversion import date_amd_to_dma

        return date_amd_to_dma(f)

    @classmethod
    @decorators.BetaImplementation
    def formatoMiles(cls, s: str) -> str:
        """
        Formatea una cadena de texto poniéndole separadores de miles.

        La cadena que se pasa se supone que un número, convirtiendola
        con QString::toDouble(), si la cadena no es número el resultado es imprevisible.

        @param s Cadena de texto a la que se le quieren poder separadores de miles
        @return Devuelve la cadena formateada con los separadores de miles
        """
        s = str(s)
        decimal = ""
        entera = ""
        ret = ""
        # dot = QApplication::tr(".")
        dot = "."
        neg = s[0] == "-"

        if "." in s:
            # decimal = QApplication::tr(",") + s.section('.', -1, -1)
            aStr = s.split(".")
            decimal = "," + aStr[-1]
            entera = aStr[-2].replace(".", "")
        else:
            entera = s

        if neg:
            entera.replace("-", "")

        length = len(entera)

        while length > 3:
            ret = dot + entera[-3:] + ret
            entera = entera[:-3]
            length = len(entera)

        ret = entera + ret + decimal

        if neg:
            ret = "-" + ret

        return ret

    @classmethod
    def translate(cls, group: str, text_: str) -> str:
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
            group, text_ = text_, group

        text_ = text_.replace(" % ", " %% ")

        return str(FLTranslate(group, text_))

    @classmethod
    def numCreditCard(cls, num: str) -> bool:
        """
        Devuelve si el numero de tarjeta de Credito es valido.

        El parametro que se pasa es la cadena de texto que contiene el numero de tarjeta.

        @param num Cadena de texto con el numero de tarjeta
        @return Devuelve verdadero si el numero de tarjeta es valido
        """
        n_sum = 0
        n_rest = int(num)
        i = 0
        while i < 10:
            n_sum += int(num[i])
            n_rest = int(num[i + 1]) * 2
            if n_rest > 9:
                n_rest -= 9

            n_sum += n_rest
            i += 2

        return True if n_sum % 10 == 0 else False

    @classmethod
    def nextCounter(cls, *args) -> Any:
        from pineboolib.application.database.utils import nextCounter

        return nextCounter(*args)

    @classmethod
    @decorators.NotImplementedWarn
    def nextSequence(cls, nivel: int, secuencia: str, ultimo: str) -> str:
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
        return ""

    @classmethod
    def isFLDefFile(cls, head: str) -> bool:
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

    @classmethod
    def addDays(cls, fecha: Any, offset: int) -> Optional["Date"]:
        """
        Suma dias a una fecha.

        @param fecha Fecha con la que operar
        @param offset Numero de dias que sumar. Si es negativo resta dias
        @return Fecha con el desplazamiento de dias
        """

        if isinstance(fecha, str):
            fecha = Date(fecha, "yyyy-MM-dd")
        if not isinstance(fecha, Date):
            logger.error("addDays: No reconozco el tipo de dato %s", type(fecha))
            logger.trace("Detalle:", stack_info=True)
            return None
        return fecha.addDays(offset)

    @classmethod
    def addMonths(cls, fecha: Any, offset: int) -> Optional["Date"]:
        """
        Suma meses a una fecha.

        @param fecha Fecha con la que operar
        @param offset Numero de meses que sumar. Si es negativo resta meses
        @return Fecha con el desplazamiento de meses
        """

        if isinstance(fecha, str):
            fecha = Date(fecha)
        if not isinstance(fecha, Date):
            logger.error("addMonths: No reconozco el tipo de dato %s", type(fecha))
            logger.trace("Detalle:", stack_info=True)
            return None
        return fecha.addMonths(offset)

    @classmethod
    def addYears(cls, fecha: Any, offset: int) -> Optional["Date"]:
        """
        Suma años a una fecha.

        @param fecha Fecha con la que operar
        @param offset Numero de años que sumar. Si es negativo resta años
        @return Fecha con el desplazamiento de años
        """

        if isinstance(fecha, str):
            fecha = Date(fecha)
        if not isinstance(fecha, Date):
            logger.error("addYears: No reconozco el tipo de dato %s", type(fecha), stack_info=True)
            return None
        return fecha.addYears(offset)

    @classmethod
    def daysTo(cls, d1: Any, d2: Any) -> Optional[int]:
        """
        Diferencia de dias desde una fecha a otra.

        @param d1 Fecha de partida
        @param d2 Fecha de destino
        @return Número de días entre d1 y d2. Será negativo si d2 es anterior a d1.
        """
        from datetime import date

        if isinstance(d1, Date):
            d1 = d1.toString()

        if isinstance(d1, date):
            d1 = str(d1)

        if isinstance(d1, str):
            d1 = d1[:10]

        if not isinstance(d1, str) or d1 == "":
            if d1 not in (None, ""):
                logger.error("daysTo: No reconozco el tipo de dato %s", type(d1))
            return None

        if isinstance(d2, Date):
            d2 = d2.toString()

        if isinstance(d2, date):
            d2 = str(d2)

        if isinstance(d2, str):
            d2 = d2[:10]

        if not isinstance(d2, str) or d2 == "":
            if d2 not in (None, ""):
                logger.error("daysTo: No reconozco el tipo de dato %s", type(d2))
            return None
        d1 = datetime.datetime.strptime(d1, "%Y-%m-%d").date()
        d2 = datetime.datetime.strptime(d2, "%Y-%m-%d").date()
        return (d2 - d1).days

    @classmethod
    def buildNumber(cls, v: Union[int, float, str], tipo: str, partDecimal: int) -> str:
        """
        Construye un string a partir de un número, especificando el formato y precisión

        @param v. Número a convertir a QString
        @param tipo. Formato del número
        @param partDecimal. Precisión (número de cifras decimales) del número

        @return Cadena que contiene el número formateado
        """
        val_str: str = str(v)
        if val_str.endswith("5"):
            val_str += "1"

        ret = round(float(val_str)) if partDecimal == 0 else round(float(val_str), partDecimal)
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
        return str(ret)

    @classmethod
    def readSettingEntry(cls, key: str, def_: Any = u"") -> Any:
        """
        Lee el valor de un setting en el directorio de la instalación de AbanQ

        @param key. Clave identificadora del setting
        @param def. Valor por defecto en el caso de que el setting no esté establecido
        @param ok. Indicador de que la lectura es correcta

        @return Valor del setting
        """
        from pineboolib.core.settings import settings

        return settings.value(key, def_)

    @classmethod
    def writeSettingEntry(cls, key: str, value: Any) -> None:
        """
        Establece el valor de un setting en el directorio de instalación de AbanQ

        @param key. Clave identificadora del setting
        @param Valor del setting

        @return Indicador de si la escritura del settings se realiza correctamente
        """
        from pineboolib.core.settings import settings

        return settings.set_value(key, value)

    @classmethod
    def readDBSettingEntry(cls, key: str) -> Any:
        """
        Lee el valor de un setting en la tabla flsettings

        @param key. Clave identificadora del setting

        @return Valor del setting
        """
        from pineboolib.fllegacy.flsqlquery import FLSqlQuery

        ret = None
        q = FLSqlQuery()
        q.setSelect("valor")
        q.setFrom("flsettings")
        q.setWhere("flkey = '%s'" % key)
        q.setTablesList("flsettings")
        if q.exec_() and q.first():
            ret = q.value(0)
            if ret in ["false", "False"]:
                ret = False
            elif ret in ["true", "True"]:
                ret = True

        return ret

    @classmethod
    def writeDBSettingEntry(cls, key: str, value: Any) -> bool:
        """
        Establece el valor de un setting en la tabla flsettings

        @param key. Clave identificadora del setting
        @param Valor del setting

        @return Indicador de si la escritura del settings se realiza correctamente
        """
        # result = False
        from pineboolib.application import project

        where = "flkey = '%s'" % key
        found = cls.readDBSettingEntry(key)
        cursor = project.conn.cursor()
        if found is None:
            sql = "INSERT INTO flsettings (flkey, valor) VALUES ('%s', '%s')" % (key, value)
        else:
            sql = "UPDATE flsettings SET valor = '%s' WHERE %s" % (value, where)
        try:
            cursor.execute(sql)

        except Exception:
            logger.exception("writeDBSettingEntry: Error al ejecutar SQL: %s", sql)
            # FIXME: Quito el rollback porque esta función no inicia transacción
            # cursor.rollback()
            return False

        cursor.close()
        return True

    @classmethod
    def roundFieldValue(cls, value: Union[float, int, str], table_name: str, field_name: str) -> str:
        """
        Redondea un valor en función de la precisión especificada para un campo tipo double de la base de datos

        @param n. Número a redondear
        @param table. Nombre de la tabla
        @param field. Nombre del campo

        @return Número redondeado
        """

        from pineboolib.fllegacy.flapplication import aqApp

        tmd = aqApp.db().manager().metadata(table_name)
        if tmd is None:
            return ""
        fmd = tmd.field(field_name)
        return cls.buildNumber(value, "float", fmd.partDecimal()) if fmd is not None else ""

    @classmethod
    def sqlSelect(cls, f: str, s: str, w: str, tL: Optional[Union[str, List]] = None, size: int = 0, connName: str = "default") -> Any:
        from pineboolib.application.database.utils import sqlSelect

        return sqlSelect(f, s, w, tL, size, connName)

    @classmethod
    def quickSqlSelect(cls, f: str, s: str, w: str, connName: str = "default") -> Any:
        from pineboolib.application.database.utils import quickSqlSelect

        return quickSqlSelect(f, s, w, connName)

    @classmethod
    def sqlInsert(cls, t: str, fL: Union[str, List], vL: Union[str, List], connName: str = "default") -> Any:
        from pineboolib.application.database.utils import sqlInsert

        return sqlInsert(t, fL, vL, connName)

    @classmethod
    def sqlUpdate(cls, t: str, fL: Union[str, List], vL: Union[str, List], w: str, connName: str = "default") -> Any:
        from pineboolib.application.database.utils import sqlUpdate

        return sqlUpdate(t, fL, vL, w, connName)

    @classmethod
    def sqlDelete(cls, t: str, w: str, connName: str = "default"):
        from pineboolib.application.database.utils import sqlDelete

        return sqlDelete(t, w, connName)

    @classmethod
    def quickSqlDelete(cls, t: str, w: str, connName: str = "default"):
        from pineboolib.application.database.utils import quickSqlDelete

        return quickSqlDelete(t, w, connName)

    @classmethod
    def execSql(cls, sql: str, connName: str = "default"):
        from pineboolib.application.database.utils import execSql

        return execSql(sql, connName)

    @classmethod
    def createProgressDialog(cls, title: str, steps: int, id_: str = "default") -> Any:
        """
        Crea un diálogo de progreso

        @param l Label del diálogo
        @param tS Número total de pasos a realizar
        """
        from pineboolib.application import project

        return project.message_manager().send("progress_dialog_manager", "create", [title, steps, id_])

    @classmethod
    def destroyProgressDialog(cls, id_: str = "default") -> None:
        """
        Destruye el diálogo de progreso
        """

        from pineboolib.application import project

        project.message_manager().send("progress_dialog_manager", "destroy", [id_])

    @classmethod
    def setProgress(cls, step_number: int, id_: str = "default") -> None:
        """
        Establece el grado de progreso del diálogo

        @param p Grado de progreso
        """

        from pineboolib.application import project

        project.message_manager().send("progress_dialog_manager", "setProgress", [step_number, id_])

    @classmethod
    def setLabelText(cls, l: str, id_: str = "default") -> None:
        """
        Cambia el texto de la etiqueta del diálogo

        @param l Etiqueta
        """

        from pineboolib.application import project

        project.message_manager().send("progress_dialog_manager", "setLabelText", [l, id_])

    @classmethod
    def setTotalSteps(cls, tS: int, id_: str = "default") -> None:
        """
        Establece el número total de pasos del diálogo

        @param ts Número total de pasos
        """

        from pineboolib.application import project

        project.message_manager().send("progress_dialog_manager", "setTotalSteps", [tS, id_])

    @classmethod
    def domDocumentSetContent(cls, doc: "QDomDocument", content: str) -> bool:
        """
        Establece el contenido de un documento XML.

        Establece un documento DOM a partir del XML. Chequea errores, y si existen
        muestra el error encontrado y la linea y columna donde se encuentra.

        @param doc Documento DOM a establecer
        @param content Contenido XML
        @return FALSE si hubo fallo, TRUE en caso contrario
        """
        if not content:
            logger.warning("Se ha intentado cargar un fichero XML vacío", stack_info=False)
            return False

        ErrMsg = ""
        errLine = 0
        errColumn = 0

        # if not doc.setContent(content, ErrMsg, errLine, errColumn):
        if not doc.setContent(content):
            logger.warning("Error en fichero XML.\nError : %s\nLinea : %s\nColumna : %s", ErrMsg, errLine, errColumn)
            return False

        return True

    @classmethod
    def sha1(cls, str_: Optional[str]) -> str:
        """
        Obtiene la clave SHA1 de una cadena de texto.

        @param str Cadena de la que obtener la clave SHA1
        @return Clave correspondiente en digitos hexadecimales
        """
        if str_ is None:
            str_ = ""
        sha_ = hashlib.new("sha1", str_.encode())
        st = "%s" % sha_.hexdigest()
        st = st.upper()
        return st

    @classmethod
    @decorators.NotImplementedWarn
    def usha1(cls, data, _len):
        pass

    @classmethod
    @decorators.NotImplementedWarn
    def snapShotUI(cls, n):
        """
        Obtiene la imagen o captura de pantalla de un formulario.

        @param n Nombre del fichero que contiene la descricpción del formulario.
        """
        pass

    @classmethod
    @decorators.NotImplementedWarn
    def saveSnapShotUI(cls, n, pathFile):
        """
        Salva en un fichero con formato PNG la imagen o captura de pantalla de un formulario.

        @param n Nombre del fichero que contiene la descricpción del formulario.
        @param pathFile Ruta y nombre del fichero donde guardar la imagen
        """
        pass

    @classmethod
    @decorators.NotImplementedWarn
    def flDecodeType(cls, fltype):
        """
        Decodifica un tipo de AbanQ a un tipo QVariant

        @param fltype Tipo de datos de AbanQ.
        @return Tipo de datos QVariant.
        """
        pass

    @classmethod
    @decorators.NotImplementedWarn
    def saveIconFile(cls, data, pathFile):
        """
        Guarda la imagen de icono de un botón de un formulario en un ficher png. Utilizado para documentación

        @param data Contenido de la imagen en una cadena de caracteres
        @param pathFile Ruta completa al fichero donde se guadará la imagen
        """
        pass

    @classmethod
    def getIdioma(cls) -> str:
        """
        Devuelve una cadena de dos caracteres con el código de idioma del sistema

        @return Código de idioma del sistema
        """
        return QtCore.QLocale().name()[:2]

    @classmethod
    def getOS(cls) -> str:
        return SysBaseType.osName()

    @classmethod
    @decorators.NotImplementedWarn
    def serialLettertoNumber(cls, letter: str) -> str:
        """
        Esta función convierte una cadena que es una serie de letras en su correspondiente valor numerico.

        @param letter Cadena con la serie.
        @return Una cadena pero que contiene numeros.
        """
        return ""

    @classmethod
    @decorators.NotImplementedWarn
    def serialNumbertoLetter(cls, number: Union[int, float]) -> str:
        """
        Esta función convierte un numero a su correspondiente secuencia de Letras.

        @param number Número a convertir
        """
        return ""

    @classmethod
    @decorators.NotImplementedWarn
    def findFiles(cls, paths: str, filter_: str = "*", break_on_first_match: bool = False) -> List[str]:
        """
        Busca ficheros recursivamente en las rutas indicadas y según el patrón indicado
        @param  paths   Rutas de búsqueda
        @param  filter  Patrón de filtrado para los ficheros. Admite varios separados por espacios "*.gif *.png".
                      Por defecto todos, "*"
        @param  breakOnFirstMatch Si es TRUE al encontrar el primer fichero que cumpla el patrón indicado, termina
                                la búsqueda y devuelve el nombre de ese fichero
        @return Lista de los nombres de los ficheros encontrados
        """

        import glob

        files_found = []
        for p in paths:
            for file_name in glob.iglob("%s/**/%s" % (p, filter_), recursive=True):
                files_found.append(file_name)
                if break_on_first_match:
                    break

        return files_found

    @classmethod
    @decorators.NotImplementedWarn
    def savePixmap(cls, data: str, filename: str, format_: str) -> None:
        """
        Guarda imagen Pixmap en una ruta determinada.

        @param data Contenido de la imagen en una cadena de caracteres
        @param filename: Ruta al fichero donde se guardará la imagen
        @param fmt Indica el formato con el que guardar la imagen
        @author Silix
        """
        pass

    @classmethod
    def fieldType(cls, fn: str, tn: str, conn_name: str = "default") -> Optional[str]:
        """
        Retorna el tipo numérico de un campo
        @param field_name. Nombre del campo
        @param table_name. Nombre de la tabla que contiene el campo
        @param conn_name. Nombre de la conexión a usar
        @return id del tipo de campo
        """

        from pineboolib.fllegacy.flapplication import aqApp

        conn = aqApp.db().useConn(conn_name)
        mtd = conn.manager().metadata(tn)

        return None if mtd is None else mtd.fieldType(fn)

    @classmethod
    def fieldLength(cls, fn: str, tn: Optional[str], conn_name: str = "default") -> int:
        """
        Retorna la longitud de un campo
        @param fn. Nombre del campo
        @param tn. Nombre de la tabla que contiene el campo
        @param conn_name. Nombre de la conexión a usar
        @return longitud del campo solicitado
        """
        if tn is None:
            return 0

        from pineboolib.fllegacy.flapplication import aqApp

        conn = aqApp.db().useConn(conn_name)
        mtd = conn.manager().metadata(tn)

        return 0 if mtd is None else mtd.fieldLength(fn)

    @classmethod
    def fieldNameToAlias(cls, fn: str, tn: Optional[str], conn_name: str = "default") -> str:
        """
        Retorna el alias de un campo a partir de su nombre
        @param fn. Nombre del campo
        @param tn. Nombre de la tabla que contiene el campo
        @param conn_name. Nombre de la conexión a usar
        @return Alias del campo especificado
        """
        if tn is None:
            return fn

        from pineboolib.fllegacy.flapplication import aqApp

        conn = aqApp.db().useConn(conn_name)
        mtd = conn.manager().metadata(tn)

        return fn if mtd is None else mtd.fieldNameToAlias(fn)

    @classmethod
    def tableNameToAlias(cls, tn: Optional[str], conn_name: str = "default") -> Optional[str]:
        """
        Retorna el nombre de una tabla a partir de su alias
        @param tn. Nombre de la tabla
        @param conn_name. Nombre de la conexión a usar
        @return Alias de la tabla especificada
        """

        if tn is None:
            return None

        from pineboolib.fllegacy.flapplication import aqApp

        conn = aqApp.db().useConn(conn_name)
        mtd = conn.manager().metadata(tn)

        return None if mtd is None else mtd.alias()

    @classmethod
    def fieldAliasToName(cls, an: str, tn: Optional[str], conn_name: str = "default") -> str:

        """
        Retorna el nombre de un campo a partir de su alias
        @param fn. Nombre del campo
        @param tn. Nombre de la tabla que contiene el campo
        @param conn_name. Nombre de la conexión a usar
        @return Alias del campo especificado
        """

        if tn is None:
            return an

        from pineboolib.fllegacy.flapplication import aqApp

        conn = aqApp.db().useConn(conn_name)
        mtd = conn.manager().metadata(tn)

        return an if mtd is None else mtd.fieldAliasToName(an)

    @classmethod
    def fieldAllowNull(cls, fn: str, tn: Optional[str], conn_name: str = "default") -> bool:
        """
        Retorna si el campo permite dejarse en blanco
        @param fn. Nombre del campo
        @param tn. Nombre de la tabla que contiene el campo
        @param conn_name. Nombre de la conexión a usar
        @return Boolean. Si acepta o no dejar en blanco el valor del campo
        """

        if tn is None:
            return False

        from pineboolib.fllegacy.flapplication import aqApp

        conn = aqApp.db().useConn(conn_name)
        mtd = conn.manager().metadata(tn)

        return False if mtd is None else mtd.fieldAllowNull(fn)

    @classmethod
    def fieldIsPrimaryKey(cls, fn: str, tn: Optional[str], conn_name: str = "default") -> bool:
        """
        Retorna si el campo es clave primaria de la tabla
        @param fn. Nombre del campo
        @param tn. Nombre de la tabla que contiene el campo
        @param conn_name. Nombre de la conexión a usar
        @return Boolean. Si es clave primaria o no
        """
        if tn is None:
            return False

        from pineboolib.fllegacy.flapplication import aqApp

        conn = aqApp.db().useConn(conn_name)
        mtd = conn.manager().metadata(tn)

        return False if mtd is None else mtd.fieldIsPrimaryKey(fn)

    @classmethod
    def fieldIsCompoundKey(cls, fn: str, tn: Optional[str], conn_name: str = "default") -> bool:
        """
        Retorna si el campo es clave compuesta de la tabla
        @param fn. Nombre del campo
        @param tn. Nombre de la tabla que contiene el campo
        @param conn_name. Nombre de la conexión a usar
        @return Boolean. Si es clave compuesta o no
        """
        if tn is None:
            return False

        from pineboolib.fllegacy.flapplication import aqApp

        conn = aqApp.db().useConn(conn_name)
        mtd = conn.manager().metadata(tn)

        if mtd is None:
            return False
        return False
        # field = None  # FIXME: field is not defined anywhere
        # return False if field is None else field.isCompoundKey()

    @classmethod
    def fieldDefaultValue(cls, fn: str, tn: Optional[str], conn_name: str = "default") -> Any:
        """
        Retorna el valor por defecto de un campo
        @param fn. Nombre del campo
        @param tn. Nombre de la tabla que contiene el campo
        @param conn_name. Nombre de la conexión a usar
        @return Valor por defecto del campo
        """
        if tn is None:
            return None  # return QVariant

        from pineboolib.fllegacy.flapplication import aqApp

        conn = aqApp.db().useConn(conn_name)
        mtd = conn.manager().metadata(tn)

        if mtd is None:
            return None  # return QVariant

        field = mtd.field(fn)
        if field is None:
            return None  # return QVariant

        return field.defaultValue()

    @classmethod
    def formatValue(cls, t: str, v: Any, upper: bool, conn_name: str = "default") -> Any:
        """
        Retorna valor formateado
        @param t. Tipo de campo
        @param v. Valor del campo
        @param conn_name. Nombre de la conexión a usar
        @return Valor formateado
        """

        from pineboolib.fllegacy.flapplication import aqApp

        conn = aqApp.db().useConn(conn_name)
        return conn.manager().formatValue(t, v, upper)

    @classmethod
    def nameUser(cls) -> str:

        return SysBaseType.nameUser()

    # FIXME: Missing in SysType:
    # @classmethod
    # def userGroups(cls) -> str:
    #
    #     return SysType().userGroups()
    #
    # @classmethod
    # def isInProd(cls) -> bool:
    #
    #     return SysType().isInProd()
    #
    # @classmethod
    # def request(cls) -> str:
    #
    #     return SysType().request()

    @classmethod
    def nameBD(cls) -> str:

        return SysBaseType.nameBD()
