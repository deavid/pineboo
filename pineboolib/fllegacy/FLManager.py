# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.Qt import qWarning, QApplication
from PyQt5.QtXml import QDomDocument


from pineboolib import decorators
from pineboolib.utils import filedir, auto_qt_translate_text, clearXPM

from pineboolib.fllegacy.FLTableMetaData import FLTableMetaData
from pineboolib.fllegacy.FLRelationMetaData import FLRelationMetaData
from pineboolib.fllegacy.FLFieldMetaData import FLFieldMetaData
from pineboolib.fllegacy.FLCompoundKey import FLCompoundKey
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery, FLGroupByQuery
from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
from pineboolib.fllegacy.FLAction import FLAction
from pineboolib.fllegacy.FLUtil import FLUtil
import pineboolib

from xml import etree
import logging
# import os
logger = logging.getLogger(__name__)


class FLManager(QtCore.QObject):
    """
    Esta clase sirve como administrador de la base de datos.

    Encargada de abrir los formularios u obtener sus definiciones (ficheros .ui).
    Tambien mantiene los metadatos de todas la tablas de la base de
    datos, ofreciendo la posibilidad de recuperar los metadatos
    mediante objetos FLTableMetaData de una tabla dada.

    @author InfoSiAL S.L.
    """

    listTables_ = []  # Lista de las tablas de la base de datos, para optimizar lecturas
    dictKeyMetaData_ = None  # Diccionario de claves de metadatos, para optimizar lecturas
    cacheMetaData_ = None  # Caché de metadatos, para optimizar lecturas
    cacheAction_ = None  # Caché de definiciones de acciones, para optimizar lecturas
    # Caché de metadatos de talblas del sistema para optimizar lecturas
    cacheMetaDataSys_ = None
    db_ = None  # Base de datos a utilizar por el manejador
    initCount_ = 0  # Indica el número de veces que se ha llamado a FLManager::init()
    buffer_ = None
    metadataCachedFails = []
    def __init__(self, db):
        """
        constructor
        """
        super(FLManager, self).__init__()
        self.db_ = db
        self.listTables_ = []
        self.dictKeyMetaData_ = {}
        self.initCount_ = 0
        self.cacheMetaData_ = []
        self.cacheMetaDataSys_ = []
        self.cacheAction_ = []
        QtCore.QTimer.singleShot(100, self.init)
        self.metadataCachedFails = []
        

    def __del__(self):
        """
        destructor
        """
        self.finish()

    def init(self):
        """
        Acciones de inicialización.
        """
        self.initCount_ = self.initCount_ + 1
        self.createSystemTable("flmetadata")
        self.createSystemTable("flseqs")

        if not self.db_.dbAux():
            return

        #q = FLSqlQuery(None, self.db_.dbAux())
        # q.setForwardOnly(True)

        self.createSystemTable("flsettings")
        """
        if not q.exec_("SELECT * FROM flsettings WHERE flkey = 'sysmodver'"):

            if pineboolib.project.conn.driver().cascadeSupport():
                q.exec_("DROP TABLE flsettings CASCADE")
            else:
                q.exec_("DROP TABLE flsettings")

            self.createSystemTable("flsettings")

        if not self.dictKeyMetaData_:
            self.dictKeyMetaData_ = {}
            # self.dictKeyMetaData_.setAutoDelete(True)
        else:
            self.dictKeyMetaData_.clear()

        q.exec_("SELECT tabla,xml FROM flmetadata")
        while q.next():
            self.dictKeyMetaData_[q.value(0)] = q.value(1)

        q.exec_("SELECT * FROM flsettings WHERE flkey = 'sysmodver'")
        if not q.next():

            if pineboolib.project.conn.driver().cascadeSupport():
                q.exec_("DROP TABLE flmetadata CASCADE")
            else:
                q.exec_("DROP TABLE flmetadata")

            self.createSystemTable("flmetadata")

            c = FLSqlCursor("flmetadata", True, self.db_.dbAux())
            for key, value in self.dictKeyMetaData_:
                buffer = c.primeInsert()
                buffer.setValue("tabla", key)
                buffer.setValue("xml", value)
                c.insert()
        """
        if not self.cacheMetaData_:
            self.cacheMetaData_ = []

        if not self.cacheAction_:
            self.cacheAction_ = []

        if not self.cacheMetaDataSys_:
            self.cacheMetaDataSys_ = []

    def finish(self):
        """
        Acciones de finalización.
        """
        self.dictKeyMetaData_ = {}
        self.listTables_ = []
        self.cacheMetaData_ = []
        self.cacheAction_ = []

    def metadata(self, n, quick=False):
        """
        Para obtener definicion de una tabla de la base de datos, a partir de un fichero XML.

        El nombre de la tabla corresponde con el nombre del fichero mas la extensión ".mtd"
        que contiene en XML la descripción de la tablas. Este método escanea el fichero
        y construye/devuelve el objeto FLTableMetaData correspondiente, además
        realiza una copia de estos metadatos en una tabla de la misma base de datos
        para poder determinar cuando ha sido modificados y así, si es necesario, reconstruir
        la tabla para que se adapte a la nuevos metadatos. NO SE HACEN
        CHEQUEOS DE ERRORES SINTÁCTICOS EN EL XML.

        IMPORTANTE :Para que estos métodos funcionen correctamente, es estrictamente
            necesario haber creado la base de datos en PostgreSQL con codificación
            UNICODE; "createdb -E UNICODE abanq".

        @param n Nombre de la tabla de la base de datos de la que obtener los metadatos
        @param quick Si TRUE no realiza chequeos, usar con cuidado
        @return Un objeto FLTableMetaData con los metadatos de la tabla solicitada
        """

        util = FLUtil()

        if not n:
            return None

        if isinstance(n, str):

            if not n or not self.db_.dbAux():
                return None

            ret = False
            acl = False
            key = n.strip()
            stream = None

            isSysTable = (n[0:3] == "sys" or self.isSystemTable(n))
            # if not isSysTable:
            #    stream = self.db_.managerModules().contentCached("%s.mtd" % key)

            #    if not stream:
            #        qWarning(
            #            "FLManager : Error al cargar los metadatos para la tabla %s" % n)

            #       return None

            #    if not key:
            #        key = n
            cacheFound_ = False
            if isSysTable:
                for fi in self.cacheMetaDataSys_:
                    if fi.name() == key:
                        ret = fi
                        cacheFound_ = True
                        break
            else:
                for fi in self.cacheMetaData_:
                    if fi.name() == key:
                        ret = fi
                        cacheFound_ = True
                        break

            if not cacheFound_:
                
                stream = self.db_.managerModules().contentCached("%s.mtd" % n)

                if not stream:
                    if not n in self.metadataCachedFails:
                        qWarning(
                            "FLManager : " + util.tr("Error al cargar los metadatos para la tabla %s" % n))
                        self.metadataCachedFails.append(n)
                    return None

                doc = QDomDocument(n)
                if not util.domDocumentSetContent(doc, stream):
                    if not n in self.metadataCachedFails:
                        qWarning(
                            "FLManager : " + util.tr("Error al cargar los metadatos para la tabla %s" % n))
                        self.metadataCachedFails.append(n)
                    return None

                docElem = doc.documentElement()
                ret = self.metadata(docElem, quick)
                if not ret or ret.name() != n:
                    return None

                if not isSysTable:
                    self.cacheMetaData_.append(ret)
                    if not ret.isQuery() and not self.existsTable(n):
                        self.createTable(ret)

                elif isSysTable:
                    self.cacheMetaDataSys_.append(ret)

            else:
                acl = pineboolib.project.acl()

            # if ret.fieldsNamesUnlock():
            #    ret = FLTableMetaData(ret)

            if acl:
                acl.process(ret)

            if not quick and not isSysTable and not ret.isQuery() and self.db_.mismatchedTable(n, ret) and self.existsTable(n):
                msg = util.translate(
                    "application",
                    "La estructura de los metadatos de la tabla '%1' y su estructura interna en la base de datos no coinciden.\n"
                    "Debe regenerar la base de datos.").replace("%1", n)
                logger.warn(msg)
                # throwMsgWarning(self.db_, msg)

            return ret

        else:
            # QDomDoc
            name = None
            q = None
            a = None
            ftsfun = None
            v = True
            ed = True
            cw = False
            dl = False

            no = n.firstChild()
            while not no.isNull():
                e = no.toElement()
                if not e.isNull():
                    if e.tagName() == "field":
                        no = no.nextSibling()
                        continue

                    if e.tagName() == "name":
                        name = e.text()
                        no = no.nextSibling()
                        continue

                    if e.tagName() == "query":
                        q = e.text()
                        no = no.nextSibling()
                        continue

                    if e.tagName() == "alias":
                        a = auto_qt_translate_text(e.text())
                        a = util.translate("Metadata", a)
                        no = no.nextSibling()
                        continue

                    if e.tagName() == "visible":
                        v = (e.text() == "true")
                        no = no.nextSibling()
                        continue

                    if e.tagName() == "editable":
                        ed = (e.text() == "true")
                        no = no.nextSibling()
                        continue

                    if e.tagName() == "concurWarn":
                        cw = (e.text() == "true")
                        no = no.nextSibling()
                        continue

                    if e.tagName() == "detectLocks":
                        dl = (e.text() == "true")
                        no = no.nextSibling()
                        continue

                    if e.tagName() == "FTSFunction":
                        ftsfun = (e.text() == "true")
                        no = no.nextSibling()
                        continue

                no = no.nextSibling()
            tmd = FLTableMetaData(name, a, q)
            cK = None
            assocs = []
            tmd.setFTSFunction(ftsfun)
            tmd.setConcurWarn(cw)
            tmd.setDetectLocks(dl)
            no = n.firstChild()

            while not no.isNull():
                e = no.toElement()
                if not e.isNull():
                    if e.tagName() == "field":
                        f = self.metadataField(e, v, ed)
                        if not tmd:
                            tmd = FLTableMetaData(name, a, q)
                        tmd.addFieldMD(f)
                        if f.isCompoundKey():
                            if not cK:
                                cK = FLCompoundKey()
                            cK.addFieldMD(f)

                        if f.associatedFieldName():
                            assocs.append(f.associatedFieldName())
                            assocs.append(f.associatedFieldFilterTo())
                            assocs.append(f.name())

                        no = no.nextSibling()
                        continue

                no = no.nextSibling()

            tmd.setCompoundKey(cK)
            aWith = None
            aBy = None

            for it in assocs:
                if not aWith:
                    aWith = it
                    continue
                if not aBy:
                    aBy = it
                    continue
                if not tmd.field(it):
                    continue
                tmd.field(it).setAssociatedField(tmd.field(aWith), aBy)

            if q and not quick:
                qry = self.query(q, tmd)

                if qry:
                    fL = qry.fieldList()
                    table = None
                    field = None
                    fields = tmd.fieldsNames()
                    # .split(",")
                    fieldsEmpty = (not fields)

                    for it in fL:
                        pos = it.find(".")
                        if pos > -1:
                            table = it[:pos]
                            field = it[pos + 1:]
                        else:
                            field = it

                        # if not (not fieldsEmpty and table == name and fields.find(field.lower())) != fields.end():
                        # print("Tabla %s nombre %s campo %s buscando en %s" % (table, name, field, fields))
                        # if not fieldsEmpty and table == name and (field.lower() in fields): Asi esta en Eneboo, pero incluye campos repetidos
                        if not fieldsEmpty and (field.lower() in fields):
                            continue

                        mtdAux = self.metadata(table, True)
                        if mtdAux:
                            fmtdAux = mtdAux.field(field)
                            if fmtdAux:
                                isForeignKey = False
                                if fmtdAux.isPrimaryKey() and not table == name:
                                    fmtdAux = FLFieldMetaData(fmtdAux)
                                    fmtdAux.setIsPrimaryKey(False)
                                    fmtdAux.setEditable(False)

                                # newRef = (not isForeignKey)
                                fmtdAuxName = fmtdAux.name().lower()
                                if fmtdAuxName.find(".") == -1:
                                    # fieldsAux = tmd.fieldsNames().split(",")
                                    fieldsAux = tmd.fieldsNames()
                                    # if not fieldsAux.find(fmtdAuxName) == fieldsAux.end():
                                    if fmtdAuxName not in fieldsAux:
                                        if not isForeignKey:
                                            FLFieldMetaData(fmtdAux)

                                        # fmtdAux.setName("%s.%s" % (table, field))

                                # if newRef:
                                #    fmtdAux.ref()

                                tmd.addFieldMD(fmtdAux)

                    del qry

            acl = pineboolib.project.acl()
            if acl:
                acl.process(tmd)

            return tmd

    @decorators.NotImplementedWarn
    def metadataDev(self, n, quick=None):
        return True

    def query(self, n, parent=None):
        """
        Para obtener una consulta de la base de datos, a partir de un fichero XML.

        El nombre de la consulta corresponde con el nombre del fichero mas la extensión ".qry"
        que contiene en XML la descripción de la consulta. Este método escanea el fichero
        y construye/devuelve el objeto FLSqlQuery. NO SE HACEN
        CHEQUEOS DE ERRORES SINTÁCTICOS EN EL XML.

        @param n Nombre de la consulta de la base de datos que se quiere obtener
        @return Un objeto FLSqlQuery que representa a la consulta que se quiere obtener
        """
        qryName = "%s.qry" % n
        qry_ = self.db_.managerModules().contentCached(qryName)

        if not qry_:
            return None

        # parser_ = etree.XMLParser(
        #    ns_clean=True,
        #    encoding="UTF-8",
        #    remove_blank_text=True,
        #)

        q = FLSqlQuery(parent, self.db_.connectionName())

        root_ = etree.ElementTree.fromstring(qry_)
        q.setSelect(root_.find("select").text.replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", ""))
        q.setFrom(root_.find("from").text.strip(' \t\n\r'))

        for where in root_.iter("where"):
            q.setWhere(where.text.strip(' \t\n\r'))

        q.setTablesList(root_.find("tables").text.strip(' \t\n\r'))

        orderBy_ = None
        try:
            orderBy_ = root_.find("order").text.strip(' \t\n\r')
            q.setOrderBy(orderBy_)
        except Exception:
            pass

        groupXml_ = root_.findall("group")

        if not groupXml_:
            groupXml_ = []
        # group_ = []
        i = 0
        while i < len(groupXml_):
            gr = groupXml_[i]
            if float(gr.find("level").text.strip(' \t\n\r')) == i:
                # print("LEVEL %s -> %s" % (i,gr.xpath("field/text()")[0].strip(' \t\n\r')))
                q.addGroup(FLGroupByQuery(i, gr.find(
                    "field").text.strip(' \t\n\r')))
                i = i + 1

        return q

    @decorators.Incomplete
    def action(self, n):
        """
        Obtiene la definición de una acción a partir de su nombre.

        Este método busca en los [id_modulo].xml la acción que se le pasa
        como nombre y construye y devuelve el objeto FLAction correspondiente.
        NO SE HACEN CHEQUEOS DE ERRORES SINTÁCTICOS EN EL XML.

        @param n Nombre de la accion
        @return Un objeto FLAction con la descripcion de la accion
        """
        if not n:
            return None

        name = str(n)

        for action in self.cacheAction_:
            if action.name() == name:
                return action

        actionN = FLAction()
        actionN.setName(name)
        actionN.setTable(name)
        self.cacheAction_.append(actionN)
        return actionN

    def existsTable(self, n, cache=True):
        """
        Comprueba si existe la tabla especificada en la base de datos.

        @param n      Nombre de la tabla que se quiere comprobar si existe
        @param cache  Si cierto consulta primero la cache de tablas, en caso contrario
                    realiza una consulta a la base para obtener las tablas existentes
        @return TRUE si existe la tabla, FALSE en caso contrario
        """

        sql_query = "SELECT * FROM %s WHERE 1 = 1 LIMIT 1" % n
        # Al usar dbAux no bloquea sql si falla
        cursor = pineboolib.project.conn.useConn("dbAux").cursor()
        try:
            cursor.execute(sql_query)
        except Exception:
            cursor.close()
            return False

        return True

    def checkMetaData(self, mtd1, mtd2):
        """
        Esta función es esencialmente igual a la anterior, se proporciona por conveniencia.

        Compara los metadatos de dos tablas,  la definición en XML de esas dos tablas se
        pasan como dos cadenas de caracteres.

        @param mtd1 Cadena de caracteres con XML que describe la primera tabla
        @param mtd2 Cadena de caracteres con XML que describe la primera tabla
        @return TRUE si las dos descripciones son iguales, y FALSE en caso contrario
        """
        if mtd1 == mtd2:
            return True
        return False

    def alterTable(self, mtd1=None, mtd2=None, key=None):
        """
        Modifica la estructura o metadatos de una tabla, preservando los posibles datos
        que pueda contener.

        Según la definición existente en un momento dado de los metadatos en el fichero .mtd, este
        método reconstruye la tabla con esos metadatos sin la pérdida de información o datos,
        que pudieran existir en ese momento en la tabla.

        @param n Nombre de la tabla a reconstruir
        @param mtd1 Descripcion en XML de la vieja estructura
        @param mtd2 Descripcion en XML de la nueva estructura
        @param key Clave sha1 de la vieja estructura
        @return TRUE si la modificación tuvo éxito
        """
        return self.db_.alterTable(mtd1, mtd2, key)

    def createTable(self, n_or_tmd):
        """
        Crea una tabla en la base de datos.

        @param n_tmd Nombre o metadatos de la tabla que se quiere crear
        @return Un objeto FLTableMetaData con los metadatos de la tabla que se ha creado, o
          0 si no se pudo crear la tabla o ya existía
        """

        util = FLUtil()
        if n_or_tmd is None:
            return False

        if isinstance(n_or_tmd, str):
            tmd = self.metadata(n_or_tmd)
            if not tmd:
                return False

            if self.existsTable(tmd.name()):
                self.listTables_.append(n_or_tmd)
                return tmd
            else:
                qWarning("FLMAnager :: No existe tabla %s" % n_or_tmd)

            return self.createTable(tmd)
        else:
            if n_or_tmd.isQuery() or self.existsTable(n_or_tmd.name(), False):
                return n_or_tmd

            if not self.db_.createTable(n_or_tmd):
                logger.warn("FLManager : %s", util.tr(
                    "No se ha podido crear la tabla ") + n_or_tmd.name())
                return False

            return n_or_tmd

    @decorators.NotImplementedWarn
    def formatValueLike(self, *args, **kwargs):
        """
        Devuelve el contenido del valor de de un campo formateado para ser reconocido
        por la base de datos actual en condiciones LIKE, dentro de la clausura WHERE de SQL.

        Este método toma como parametros los metadatos del campo definidos con
        FLFieldMetaData. Además de TRUE y FALSE como posibles valores de un campo
        lógico también acepta los valores Sí y No (o su traducción al idioma correspondiente).
        Las fechas son adaptadas al forma AAAA-MM-DD, que es el formato reconocido por PostgreSQL .

        @param fMD Objeto FLFieldMetaData que describre los metadatos para el campo
        @param v Valor que se quiere formatear para el campo indicado
        @param upper Si TRUE convierte a mayúsculas el valor (si es de tipo cadena)
        """
        return True

    @decorators.NotImplementedWarn
    def formatAssignValueLike(self, *args, **kwargs):
        """
        Devuelve el contenido del valor de de un campo formateado para ser reconocido
        por la base de datos actual, dentro de la clausura WHERE de SQL.

        Este método toma como parametros los metadatos del campo definidos con
        FLFieldMetaData. Además de TRUE y FALSE como posibles valores de un campo
        lógico también acepta los valores Sí y No (o su traducción al idioma correspondiente).
        Las fechas son adaptadas al forma AAAA-MM-DD, que es el formato reconocido por PostgreSQL .

        @param fMD Objeto FLFieldMetaData que describre los metadatos para el campo
        @param v Valor que se quiere formatear para el campo indicado
        @param upper Si TRUE convierte a mayúsculas el valor (si es de tipo cadena)
        """
        return True

    def formatValue(self, fMD_or_type, v, upper=False):

        if not fMD_or_type:
            return None

        if not isinstance(fMD_or_type, str):
            return self.formatValue(fMD_or_type.type(), v, upper)

        return self.db_.formatValue(fMD_or_type, v, upper)

    def formatAssignValue(self, *args, **kwargs):
        if not args[0]:
            # print("FLManager.formatAssignValue(). Primer argumento vacio %s" % args[0])
            return "1 = 1"

        # print("tipo 0", type(args[0]))
        # print("tipo 1", type(args[1]))
        # print("tipo 2", type(args[2]))]

        if isinstance(args[0], FLFieldMetaData) and len(args) == 3:
            fMD = args[0]
            mtd = fMD.metadata()
            if not mtd:
                return self.formatAssignValue(fMD.name(), fMD.type(), args[1], args[2])

            if fMD.isPrimaryKey():
                return self.formatAssignValue(mtd.primaryKey(True), fMD.type(), args[1], args[2])

            fieldName = fMD.name()
            if mtd.isQuery() and "." not in fieldName:
                prefixTable = mtd.name()
                qry = self.query(mtd.query())

                if qry:
                    fL = qry.fieldList()

                    for f in fL:
                        # print("fieldName = " + f)

                        fieldSection = None
                        pos = f.find(".")
                        if pos > -1:
                            prefixTable = f[:pos]
                            fieldSection = f[pos + 1:]
                        else:
                            fieldSection = f

                        # prefixTable = f.section('.', 0, 0)
                        # if f.section('.', 1, 1) == fieldName:
                        if fieldSection == fieldName:
                            break

                    del qry

                # fieldName.prepend(prefixTable + ".")
                fieldName = prefixTable + "." + fieldName

            return self.formatAssignValue(fieldName, args[0].type(), args[1], args[2])

        elif isinstance(args[1], FLFieldMetaData) and isinstance(args[0], str):
            return self.formatAssignValue(args[0], args[1].type(), args[2], args[3])

        elif isinstance(args[0], FLFieldMetaData) and len(args) == 2:
            return self.formatAssignValue(args[0].name(), args[0], args[1], False)
        else:
            if args[1] is None:
                return "1 = 1"

            formatV = self.formatValue(args[1], args[2], args[3])
            if not formatV:
                return "1 = 1"

            if len(args) == 4 and args[1] == "string":
                fName = "upper(%s)" % args[0]
            else:
                fName = args[0]

            # print("%s=%s" % (fName, formatV))
            if args[1] == "string":
                if formatV.find("%") > -1:
                    retorno = "%s LIKE %s" % (fName, formatV)
                else:
                    retorno = "%s = %s" % (fName, formatV)
            else:
                retorno = "%s = %s" % (fName, formatV)

            return retorno

    def metadataField(self, field, v=True, ed=True):
        """
        Crea un objeto FLFieldMetaData a partir de un elemento XML.

        Dado un elemento XML, que contiene la descripción de un
        campo de una tabla construye y agrega a una lista de descripciones
        de campos el objeto FLFieldMetaData correspondiente, que contiene
        dicha definición del campo. Tambien lo agrega a una lista de claves
        compuesta, si el campo construido pertenece a una clave compuesta.
        NO SE HACEN CHEQUEOS DE ERRORES SINTÁCTICOS EN EL XML.

        @param field Elemento XML con la descripción del campo
        @param v Valor utilizado por defecto para la propiedad visible
        @param ed Valor utilizado por defecto para la propiedad editable
        @return Objeto FLFieldMetaData que contiene la descripción del campo
        """
        if not field:
            return None

        util = FLUtil()

        ck = False
        n = None
        a = None
        ol = False
        rX = None
        assocBy = None
        assocWith = None
        so = None

        aN = True
        iPK = True
        c = False
        iNX = False
        uNI = False
        coun = False
        oT = False
        vG = True
        fullCalc = False
        trimm = False

        t = -1
        length = 0
        pI = 4
        pD = 0

        dV = None

        no = field.firstChild()

        while not no.isNull():
            e = no.toElement()
            if not e.isNull():
                if e.tagName() in ("relation", "associated"):
                    no = no.nextSibling()
                    continue

                if e.tagName() == "name":
                    n = e.text()
                    no = no.nextSibling()
                    continue

                if e.tagName() == "alias":
                    a = auto_qt_translate_text(e.text())
                    no = no.nextSibling()
                    continue

                if e.tagName() == "null":
                    aN = (e.text() == "true")
                    no = no.nextSibling()
                    continue

                if e.tagName() == "pk":
                    iPK = (e.text() == "true")
                    no = no.nextSibling()
                    continue

                if e.tagName() == "type":
                    if e.text() == "int":
                        t = "int"
                    elif e.text() == "uint":
                        t = "uint"
                    elif e.text() == "bool":
                        t = "bool"
                    elif e.text() == "double":
                        t = "double"
                    elif e.text() == "time":
                        t = "time"
                    elif e.text() == "date":
                        t = "date"
                    elif e.text() == "pixmap":
                        t = "pixmap"
                    elif e.text() == "bytearray":
                        t = "bytearray"
                    elif e.text() == "string":
                        t = "string"
                    elif e.text() == "stringlist":
                        t = "stringlist"
                    elif e.text() == "unlock":
                        t = "unlock"
                    elif e.text() == "serial":
                        t = "serial"
                    no = no.nextSibling()
                    continue

                if e.tagName() == "length":
                    length = int(e.text())
                    no = no.nextSibling()
                    continue

                if e.tagName() == "regexp":
                    rX = e.text()
                    no = no.nextSibling()
                    continue

                if e.tagName() == "default":
                    if e.text().find("QT_TRANSLATE_NOOP") > -1:
                        dV = auto_qt_translate_text(e.text())
                    else:
                        dV = e.text()

                    no = no.nextSibling()
                    continue

                if e.tagName() == "outtransaction":
                    oT = (e.text() == "true")
                    no = no.nextSibling()
                    continue

                if e.tagName() == "counter":
                    coun = (e.text() == "true")
                    no = no.nextSibling()
                    continue

                if e.tagName() == "calculated":
                    c = (e.text() == "true")
                    no = no.nextSibling()
                    continue

                if e.tagName() == "fullycalculated":
                    fullCalc = (e.text() == "true")
                    no = no.nextSibling()
                    continue

                if e.tagName() == "trimmed":
                    trimm = (e.text() == "true")
                    no = no.nextSibling()
                    continue

                if e.tagName() == "visible":
                    v = (e.text() == "true")
                    no = no.nextSibling()
                    continue

                if e.tagName() == "visiblegrid":
                    vG = (e.text() == "true")
                    no = no.nextSibling()
                    continue

                if e.tagName() == "editable":
                    ed = (e.text() == "true")
                    no = no.nextSibling()
                    continue

                if e.tagName() == "partI":
                    pI = int(e.text())
                    no = no.nextSibling()
                    continue

                if e.tagName() == "partD":
                    pD = int(e.text())
                    no = no.nextSibling()
                    continue

                if e.tagName() == "index":
                    iNX = (e.text() == "true")
                    no = no.nextSibling()
                    continue

                if e.tagName() == "unique":
                    uNI = (e.text() == "true")
                    no = no.nextSibling()
                    continue

                if e.tagName() == "ck":
                    ck = (e.text() == "true")
                    no = no.nextSibling()
                    continue

                if e.tagName() == "optionslist":
                    ol = e.text()
                    no = no.nextSibling()
                    continue

                if e.tagName() == "searchoptions":
                    so = e.text()
                    no = no.nextSibling()
                    continue

            no = no.nextSibling()

        f = FLFieldMetaData(n, util.translate("Metadata", a), aN, iPK, t,
                            length, c, v, ed, pI, pD, iNX, uNI, coun, dV, oT, rX, vG, True, ck)
        f.setFullyCalculated(fullCalc)
        f.setTrimed(trimm)

        if ol:
            f.setOptionsList(ol)
        if so is not None:
            f.setSearchOptions(so)

        no = field.firstChild()

        while not no.isNull():
            e = no.toElement()
            if not e.isNull():
                if e.tagName() == "relation":
                    f.addRelationMD(self.metadataRelation(e))
                    no = no.nextSibling()
                    continue

                if e.tagName() == "associated":
                    noas = e.firstChild()
                    while not noas.isNull():
                        eas = noas.toElement()
                        if not eas.isNull():
                            if eas.tagName() == "with":
                                assocWith = eas.text()
                                noas = noas.nextSibling()
                                continue

                            if eas.tagName() == "by":
                                assocBy = eas.text()
                                noas = noas.nextSibling()
                                continue

                        noas = noas.nextSibling()

                    no = no.nextSibling()
                    continue

            no = no.nextSibling()

        if assocWith and assocBy:
            f.setAssociatedField(assocWith, assocBy)

        return f

    def metadataRelation(self, relation):
        """
        Crea un objeto FLRelationMetaData a partir de un elemento XML.

        Dado un elemento XML, que contiene la descripción de una
        relación entre tablas, construye y devuelve el objeto FLRelationMetaData
        correspondiente, que contiene dicha definición de la relación.
        NO SE HACEN CHEQUEOS DE ERRORES SINTÁCTICOS EN EL XML.

        @param relation Elemento XML con la descripción de la relación
        @return Objeto FLRelationMetaData que contiene la descripción de la relación
        """
        if not relation:
            return False

        fT = ""
        fF = ""
        rC = FLRelationMetaData.RELATION_M1
        dC = False
        uC = False
        cI = True

        no = relation.firstChild()

        while not no.isNull():
            e = no.toElement()
            if not e.isNull():

                if e.tagName() == "table":
                    fT = e.text()
                    no = no.nextSibling()
                    continue

                if e.tagName() == "field":
                    fF = e.text()
                    no = no.nextSibling()
                    continue

                if e.tagName() == "card":
                    if e.text() == "1M":
                        rC = FLRelationMetaData.RELATION_1M

                    no = no.nextSibling()
                    continue

                if e.tagName() == "delC":
                    dC = (e.text() == "true")
                    no = no.nextSibling()
                    continue

                if e.tagName() == "updC":
                    uC = (e.text() == "true")
                    no = no.nextSibling()
                    continue

                if e.tagName() == "checkIn":
                    cI = (e.text() == "true")
                    no = no.nextSibling()
                    continue

            no = no.nextSibling()

        return FLRelationMetaData(fT, fF, rC, dC, uC, cI)

    @decorators.NotImplementedWarn
    def queryParameter(self, parameter):
        """
        Crea un objeto FLParameterQuery a partir de un elemento XML.

        Dado un elemento XML, que contiene la descripción de una
        parámetro de una consulta, construye y devuelve el objeto FLParameterQuery
        correspondiente.
        NO SE HACEN CHEQUEOS DE ERRORES SINTÁCTICOS EN EL XML.

        @param parameter Elemento XML con la descripción del parámetro de una consulta
        @return Objeto FLParameterQuery que contiene la descrición del parámetro
        """
        return True

    @decorators.NotImplementedWarn
    def queryGroup(self, group):
        """
        Crea un objeto FLGroupByQuery a partir de un elemento XML.

        Dado un elemento XML, que contiene la descripción de un nivel de agrupamiento
        de una consulta, construye y devuelve el objeto FLGroupByQuery correspondiente.
        NO SE HACEN CHEQUEOS DE ERRORES SINTÁCTICOS EN EL XML.

        @param group Elemento XML con la descripción del nivel de agrupamiento de una consulta.
        @return Objeto FLGroupByQuery que contiene la descrición del nivel de agrupamiento
        """
        return True

    def createSystemTable(self, n):
        """
        Crea una tabla del sistema.

        Este método lee directamente de disco el fichero con la descripción de una tabla
        del sistema y la crea en la base de datos. Su uso normal es para inicializar
        el sistema con tablas iniciales.

        @param n Nombre de la tabla.
        @return Un objeto FLTableMetaData con los metadatos de la tabla que se ha creado, o
          False si no se pudo crear la tabla o ya existía
        """
        util = FLUtil()
        if not self.existsTable(n):
            doc = QDomDocument()
            _path = filedir("..", "share", "pineboo", "tables")
            from pineboolib import qsa
            dir = qsa.Dir_Class(_path)
            _tables = dir.entryList("%s.mtd" % n)

            for f in _tables:
                path = "%s/%s" % (_path, f)
                _file = QtCore.QFile(path)
                _file.open(QtCore.QIODevice.ReadOnly)
                _in = QtCore.QTextStream(_file)
                _data = _in.readAll()
                if not util.domDocumentSetContent(doc, _data):
                    logger.warn("FLManager::createSystemTable: %s", util.tr(
                        "Error al cargar los metadatos para la tabla %1").arg(n))
                    return False
                else:
                    docElem = doc.documentElement()

                    mtd = self.createTable(self.metadata(docElem, True))
                    return mtd

                f.close()

        return False

    def loadTables(self):
        """
        Carga en la lista de tablas los nombres de las tablas de la base de datos
        """
        if not self.db_.dbAux():
            return

        if not self.listTables_:
            self.listTables_ = []
        else:
            self.listTables_.clear()

        self.listTables_ = self.db_.dbAux().tables()

    def cleanupMetaData(self):
        """
        Limpieza la tabla flmetadata, actualiza el cotenido xml con el de los fichero .mtd
        actualmente cargados
        """
        # util = FLUtil()
        if not self.existsTable("flfiles") or not self.existsTable("flmetadata"):
            return

        buffer = None
        table = ""

        # q.setForwardOnly(True)
        # c.setForwardOnly(True)

        if self.dictKeyMetaData_:
            self.dictKeyMetaData_.clear()
        else:
            self.dictKeyMetaData_ = {}

        self.loadTables()
        self.db_.managerModules().loadKeyFiles()
        self.db_.managerModules().loadAllIdModules()
        self.db_.managerModules().loadIdAreas()

        q = FLSqlQuery(None, self.db_.dbAux())
        q.exec_("SELECT tabla,xml FROM flmetadata")
        while q.next():
            self.dictKeyMetaData_[str(q.value(0))] = str(q.value(1))

        c = FLSqlCursor("flmetadata", True, self.db_.dbAux())

        q2 = FLSqlQuery(None, self.db_.dbAux())
        q2.exec_("SELECT nombre,sha FROM flfiles WHERE nombre LIKE '%.mtd'")
        while q2.next():
            table = str(q2.value(0))
            table = table.replace(".mtd", "")
            tmd = self.metadata(table)
            if not tmd:
                #qWarning("FLManager::cleanupMetaData " + QApplication.tr(self, "No se ha podido crear los metadatatos para la tabla %s") % table)
                continue
            if not self.existsTable(table):
                self.createTable(table)

            c.select("tabla='%s'" % table)
            if c.next():
                buffer = c.primeUpdate()
                buffer.setValue("xml", str(q2.value(1)))
                c.update()
            self.dictKeyMetaData_[table] = str(q2.value(1))

    def isSystemTable(self, n):
        """
        Para saber si la tabla dada es una tabla de sistema.

        @param n Nombre de la tabla.
        @return TRUE si es una tabla de sistema
        """

        # if not n[0:2] == "fl":
        #    return False

        if n in ("flfiles", "flmetadata", "flmodules", "flareas", "flserial", "flvar", "flsettings", "flseqs", "flupdates"):
            return True

        return False

    def storeLargeValue(self, mtd, largeValue):
        """
        Utilizado para almacenar valores grandes de campos en tablas separadas indexadas
        por claves SHA del contenido del valor.

        Se utiliza para optimizar consultas que incluyen campos con valores grandes,
        como por ejemplo imágenes, para manejar en las consulta SQL la referencia al valor
        que es de tamaño constante en vez del valor en sí. Esto disminuye el tráfico al
        reducir considerablemente el tamaño de los registros obtenidos.

        Las consultas pueden utilizar una referencia y obtener su valor sólo cuando se
        necesita mediante FLManager::fetchLargeValue().


        @param mtd Metadatos de la tabla que contiene el campo
        @param largeValue Valor de gran tamaño del campo
        @return Clave de referencia al valor
        """

        if largeValue[0:3] == "RK@" or not mtd:
            return None

        tableName = mtd.name()
        if self.isSystemTable(tableName):
            return None

        tableLarge = None

        if pineboolib.project.singleFLLarge():
            tableLarge = "fllarge"
        else:
            tableLarge = "fllarge_%s" % tableName
            if not self.existsTable(tableLarge):
                mtdLarge = FLTableMetaData(tableLarge, tableLarge)
                fieldLarge = FLFieldMetaData(
                    "refkey", "refkey", False, True, "string", 100)
                mtdLarge.addFieldMD(fieldLarge)
                fieldLarge2 = FLFieldMetaData(
                    "sha", "sha", True, False, "string", 50)
                mtdLarge.addFieldMD(fieldLarge2)
                fieldLarge3 = FLFieldMetaData(
                    "contenido", "contenido", True, False, "stringlist")
                mtdLarge.addFieldMD(fieldLarge3)
                mtdAux = self.createTable(mtdLarge)
                mtd.insertChild(mtdLarge)
                if not mtdAux:
                    return None

        util = FLUtil()
        sha = str(util.sha1(largeValue))
        refKey = "RK@%s@%s" % (tableName, sha)
        q = FLSqlQuery()
        q.setSelect("refkey")
        q.setFrom("fllarge")
        q.setWhere(" refkey = '%s'" % refKey)
        if q.exec_() and q.first():
            if not q.value(0) == sha:
                sql = "UPDATE %s SET contenido = '%s' WHERE refkey ='%s'" % (
                    tableLarge, largeValue, refKey)
                if not util.execSql(sql, "Aux"):
                    logger.warn("FLManager::ERROR:StoreLargeValue.Update %s.%s", tableLarge, refKey)
                    return None
        else:
            sql = "INSERT INTO %s (contenido,refkey) VALUES ('%s','%s')" % (
                tableLarge, largeValue, refKey)
            if not util.execSql(sql, "Aux"):
                logger.warn("FLManager::ERROR:StoreLargeValue.Insert %s.%s", tableLarge, refKey)
                return None

        return refKey

    def fetchLargeValue(self, refKey):
        """
        Obtiene el valor de gran tamaño segun su clave de referencia.

        @param refKey Clave de referencia. Esta clave se suele obtener mediante FLManager::storeLargeValue
        @return Valor de gran tamaño almacenado
        """
        if refKey is None:
            return None
        if not refKey[0:3] == "RK@":
            return None

        if pineboolib.project.singleFLLarge():
            tableName = "fllarge"
        else:
            tableName = "fllarge_" + refKey.split("@")[1]

        if not self.existsTable(tableName):
            return None

        q = FLSqlQuery()
        q.setSelect("contenido")
        q.setFrom(tableName)
        q.setWhere(" refkey = '%s'" % refKey)
        if q.exec_() and q.first():
            v = q.value(0)
            del q
            # print(v)
            v = clearXPM(v)
            # print(v)
            return v

    def initCount(self):
        """
        Uso interno. Indica el número de veces que se ha llamado a FLManager::init().
        """
        return self.initCount_
