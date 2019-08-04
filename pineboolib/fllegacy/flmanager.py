# -*- coding: utf-8 -*-
from PyQt5 import QtCore  # type: ignore
from PyQt5.QtXml import QDomDocument  # type: ignore


from pineboolib.core import decorators
from pineboolib.core.settings import config
from pineboolib.core.utils.utils_base import filedir, auto_qt_translate_text
from pineboolib.application.utils.xpm import cacheXPM


from pineboolib.application.metadata.pncompoundkeymetadata import PNCompoundKeyMetaData
from pineboolib.application.metadata.pntablemetadata import PNTableMetaData
from pineboolib.application.metadata.pnrelationmetadata import PNRelationMetaData
from pineboolib.application.metadata.pnfieldmetadata import PNFieldMetaData

from pineboolib.fllegacy.flutil import FLUtil

from xml import etree  # type: ignore
from pineboolib import logging
from pineboolib.interfaces import IManager

from PyQt5.QtXml import QDomElement  # type: ignore


from pineboolib.application.database.pnsqlquery import PNSqlQuery
from pineboolib.application.database.pngroupbyquery import PNGroupByQuery
from pineboolib.application.database.pnsqlcursor import PNSqlCursor

from typing import Optional, Union, Any, List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.interfaces.iconnection import IConnection
    import pineboolib.fllegacy.flaction

logger = logging.getLogger(__name__)

# FIXME: This class is emulating Eneboo, but the way is set up it is a core part of Pineboo now.
# ... we should probably create our own one. Not this one.


class FLManager(QtCore.QObject, IManager):
    """
    Esta clase sirve como administrador de la base de datos.

    Encargada de abrir los formularios u obtener sus definiciones (ficheros .ui).
    Tambien mantiene los metadatos de todas la tablas de la base de
    datos, ofreciendo la posibilidad de recuperar los metadatos
    mediante objetos PNTableMetaData de una tabla dada.

    @author InfoSiAL S.L.
    """

    listTables_: List[str] = []  # Lista de las tablas de la base de datos, para optimizar lecturas
    dictKeyMetaData_: Dict[str, str]  # Diccionario de claves de metadatos, para optimizar lecturas
    cacheMetaData_: Dict[str, PNTableMetaData]  # Caché de metadatos, para optimizar lecturas
    cacheAction_: Dict[
        str, "pineboolib.fllegacy.flaction.FLAction"
    ]  # Caché de definiciones de acciones, para optimizar lecturas
    # Caché de metadatos de talblas del sistema para optimizar lecturas
    cacheMetaDataSys_: Dict[str, PNTableMetaData]
    db_ = None  # Base de datos a utilizar por el manejador
    initCount_ = 0  # Indica el número de veces que se ha llamado a FLManager::init()
    buffer_ = None
    metadataCachedFails: List[str]

    def __init__(self, db: "IConnection") -> None:
        """
        constructor
        """
        super(FLManager, self).__init__()
        self.db_ = db
        self.listTables_ = []
        self.dictKeyMetaData_ = {}
        self.initCount_ = 0
        self.cacheMetaData_ = {}
        self.cacheMetaDataSys_ = {}
        self.cacheAction_ = {}
        QtCore.QTimer.singleShot(100, self.init)
        self.metadataCachedFails = []

    def init(self) -> None:
        """
        Acciones de inicialización.
        """
        self.initCount_ = self.initCount_ + 1
        self.createSystemTable("flmetadata")
        self.createSystemTable("flseqs")

        if not self.db_:
            raise Exception("FLManagar.__init__. self.db_ is empty!")

        if not self.db_.dbAux():
            return

        # q = PNSqlQuery(None, self.db_.dbAux())
        # q.setForwardOnly(True)

        self.createSystemTable("flsettings")
        """
        if not q.exec_("SELECT * FROM flsettings WHERE flkey = 'sysmodver'"):

            if project.conn.driver().cascadeSupport():
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

            if project.conn.driver().cascadeSupport():
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
            self.cacheMetaData_ = {}

        if not self.cacheAction_:
            self.cacheAction_ = {}

        if not self.cacheMetaDataSys_:
            self.cacheMetaDataSys_ = {}

    def finish(self) -> None:
        self.dictKeyMetaData_ = {}
        self.listTables_ = []
        self.cacheMetaData_ = {}
        self.cacheAction_ = {}

        del self

    def metadata(
        self, n: Union[str, QDomElement], quick: Optional[bool] = None
    ) -> Optional["PNTableMetaData"]:
        """
        Para obtener definicion de una tabla de la base de datos, a partir de un fichero XML.

        El nombre de la tabla corresponde con el nombre del fichero mas la extensión ".mtd"
        que contiene en XML la descripción de la tablas. Este método escanea el fichero
        y construye/devuelve el objeto PNTableMetaData correspondiente, además
        realiza una copia de estos metadatos en una tabla de la misma base de datos
        para poder determinar cuando ha sido modificados y así, si es necesario, reconstruir
        la tabla para que se adapte a la nuevos metadatos. NO SE HACEN
        CHEQUEOS DE ERRORES SINTÁCTICOS EN EL XML.

        IMPORTANTE :Para que estos métodos funcionen correctamente, es estrictamente
            necesario haber creado la base de datos en PostgreSQL con codificación
            UNICODE; "createdb -E UNICODE abanq".

        @param n Nombre de la tabla de la base de datos de la que obtener los metadatos
        @param quick Si TRUE no realiza chequeos, usar con cuidado
        @return Un objeto PNTableMetaData con los metadatos de la tabla solicitada
        """

        util = FLUtil()

        if not n:
            return None

        if not self.db_:
            raise Exception("metadata. self.db_ is empty!")

        if quick is None:
            dbadmin = config.value("application/dbadmin_enabled", False)
            quick = not bool(dbadmin)

        if isinstance(n, str):
            if not n:
                return None

            ret: Any = False
            acl: Any = False
            key = n.strip()
            stream = None
            isSysTable = n[0:3] == "sys" or self.isSystemTable(n)

            if n in self.metadataCachedFails:
                return None

            elif isSysTable:
                if key in self.cacheMetaDataSys_.keys():
                    ret = self.cacheMetaDataSys_[key]
            else:
                if key in self.cacheMetaData_.keys():
                    ret = self.cacheMetaData_[key]

            if not ret:
                stream = self.db_.managerModules().contentCached("%s.mtd" % n)

                if not stream:
                    if n.find("alteredtable") == -1:
                        logger.info(
                            "FLManager : "
                            + util.tr("Error al cargar los metadatos para la tabla %s" % n)
                        )
                    self.metadataCachedFails.append(n)
                    return None

                doc = QDomDocument(n)

                if not util.domDocumentSetContent(doc, stream):
                    logger.info(
                        "FLManager : "
                        + util.tr("Error al cargar los metadatos para la tabla %s" % n)
                    )
                    self.metadataCachedFails.append(n)
                    return None

                docElem = doc.documentElement()
                ret = self.metadata(docElem, quick)
                if ret is None:
                    return None

                if not ret.isQuery() and not self.existsTable(n):
                    self.createTable(ret)

                # acl = project.acl()
                acl = None  # FIXME: Add ACL later

                # if ret.fieldNamesUnlock():
                #    ret = PNTableMetaData(ret)

                if acl is not None:
                    acl.process(ret)

                if not isSysTable:
                    self.cacheMetaData_[key] = ret
                else:
                    self.cacheMetaDataSys_[key] = ret

                if (
                    not quick
                    and not isSysTable
                    and not ret.isQuery()
                    and self.db_.mismatchedTable(n, ret)
                    and self.existsTable(n)
                ):
                    msg = util.translate(
                        "application",
                        "La estructura de los metadatos de la tabla '%1' y su estructura interna en la base de datos no coinciden.\n"
                        "Regenerando la base de datos.",
                    ).replace("%1", n)
                    logger.warning(msg)

                    must_alter = self.db_.mismatchedTable(n, ret)
                    if must_alter:
                        if not self.alterTable(stream, stream, None, True):
                            logger.warning("La regeneración de la tabla %s ha fallado", n)

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

                    elif e.tagName() == "name":
                        name = e.text()
                        no = no.nextSibling()
                        continue

                    elif e.tagName() == "query":
                        q = e.text()
                        no = no.nextSibling()
                        continue

                    elif e.tagName() == "alias":
                        a = auto_qt_translate_text(e.text())
                        a = util.translate("Metadata", a)
                        no = no.nextSibling()
                        continue

                    elif e.tagName() == "visible":
                        v = e.text() == "true"
                        no = no.nextSibling()
                        continue

                    elif e.tagName() == "editable":
                        ed = e.text() == "true"
                        no = no.nextSibling()
                        continue

                    elif e.tagName() == "concurWarn":
                        cw = e.text() == "true"
                        no = no.nextSibling()
                        continue

                    elif e.tagName() == "detectLocks":
                        dl = e.text() == "true"
                        no = no.nextSibling()
                        continue

                    elif e.tagName() == "FTSFunction":
                        ftsfun = e.text()
                        no = no.nextSibling()
                        continue

                no = no.nextSibling()
            tmd = PNTableMetaData(name, a, q)
            cK = None
            assocs = []
            tmd.setFTSFunction(ftsfun or "")
            tmd.setConcurWarn(cw)
            tmd.setDetectLocks(dl)
            no = n.firstChild()

            while not no.isNull():
                e = no.toElement()
                if not e.isNull():
                    if e.tagName() == "field":
                        f = self.metadataField(e, v, ed)
                        if not tmd:
                            tmd = PNTableMetaData(name, a, q)
                        tmd.addFieldMD(f)
                        if f.isCompoundKey():
                            if not cK:
                                cK = PNCompoundKeyMetaData()
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
                elif not aBy:
                    aBy = it
                    continue

                elif tmd.field(it) is None:
                    continue

                if tmd.field(aWith) is not None:
                    tmd.field(it).setAssociatedField(tmd.field(aWith), aBy)
                aWith = None
                aBy = None

            if q and not quick:
                qry = self.query(q, tmd)

                if qry:
                    fL = qry.fieldList()
                    table = None
                    field = None
                    fields = tmd.fieldNames()
                    # .split(",")
                    fieldsEmpty = not fields

                    for it2 in fL:
                        pos = it2.find(".")
                        if pos > -1:
                            table = it2[:pos]
                            field = it2[pos + 1 :]
                        else:
                            field = it2

                        # if not (not fieldsEmpty and table == name and fields.find(field.lower())) != fields.end():
                        # print("Tabla %s nombre %s campo %s buscando en %s" % (table, name, field, fields))
                        # if not fieldsEmpty and table == name and (field.lower() in fields): Asi
                        # esta en Eneboo, pero incluye campos repetidos
                        if not fieldsEmpty and (field.lower() in fields):
                            continue

                        if table is None:
                            raise ValueError("table is empty!")

                        mtdAux = self.metadata(table, True)
                        if mtdAux is not None:
                            fmtdAux = mtdAux.field(field)
                            if fmtdAux is not None:
                                isForeignKey = False
                                if fmtdAux.isPrimaryKey() and not table == name:
                                    fmtdAux = PNFieldMetaData(fmtdAux)
                                    fmtdAux.setIsPrimaryKey(False)
                                    fmtdAux.setEditable(False)

                                # newRef = not isForeignKey
                                fmtdAuxName = fmtdAux.name().lower()
                                if fmtdAuxName.find(".") == -1:
                                    # fieldsAux = tmd.fieldNames().split(",")
                                    fieldsAux = tmd.fieldNames()
                                    if fmtdAuxName not in fieldsAux:
                                        if not isForeignKey:
                                            fmtdAux = PNFieldMetaData(fmtdAux)

                                        fmtdAux.setName("%s.%s" % (table, field))
                                        # newRef = False

                                # FIXME: ref() does not exist. Probably a C++ quirk from Qt to reference counting.
                                # if newRef:
                                #    fmtdAux.ref()

                                tmd.addFieldMD(fmtdAux)

                    del qry

            # acl = project.acl()
            acl = None  # FIXME: Add ACL later
            if acl:
                acl.process(tmd)

            return tmd

    @decorators.NotImplementedWarn
    def metadataDev(self, n, quick=None):
        return True

    def query(self, n, parent=None) -> Optional["PNSqlQuery"]:
        """
        Para obtener una consulta de la base de datos, a partir de un fichero XML.

        El nombre de la consulta corresponde con el nombre del fichero mas la extensión ".qry"
        que contiene en XML la descripción de la consulta. Este método escanea el fichero
        y construye/devuelve el objeto FLSqlQuery. NO SE HACEN
        CHEQUEOS DE ERRORES SINTÁCTICOS EN EL XML.

        @param n Nombre de la consulta de la base de datos que se quiere obtener
        @return Un objeto FLSqlQuery que representa a la consulta que se quiere obtener
        """
        if self.db_ is None:
            raise Exception("query. self.db_ is empty!")

        qryName = "%s.qry" % n
        qry_ = self.db_.managerModules().contentCached(qryName)

        if not qry_:
            return None

        # parser_ = etree.XMLParser(
        #    ns_clean=True,
        #    encoding="UTF-8",
        #    remove_blank_text=True,
        # )
        from pineboolib.application.database.pnsqlquery import PNSqlQuery

        q = PNSqlQuery(parent, self.db_.connectionName())

        root_ = etree.ElementTree.fromstring(qry_)
        elem_select = root_.find("select")
        elem_from = root_.find("from")

        if elem_select is not None:
            if elem_select.text is not None:
                q.setSelect(
                    elem_select.text.replace(" ", "")
                    .replace("\n", "")
                    .replace("\t", "")
                    .replace("\r", "")
                )
        if elem_from is not None:
            if elem_from.text is not None:
                q.setFrom(elem_from.text.strip(" \t\n\r"))

        for where in root_.iter("where"):
            if where.text is not None:
                q.setWhere(where.text.strip(" \t\n\r"))

        elem_tables = root_.find("tables")
        if elem_tables is not None:
            if elem_tables.text is not None:
                q.setTablesList(elem_tables.text.strip(" \t\n\r"))

        elem_order = root_.find("order")
        if elem_order is not None:
            if elem_order.text is not None:
                orderBy_ = elem_order.text.strip(" \t\n\r")
                q.setOrderBy(orderBy_)

        groupXml_ = root_.findall("group")

        if not groupXml_:
            groupXml_ = []
        # group_ = []

        for i in range(len(groupXml_)):
            gr = groupXml_[i]
            if gr is not None:
                elem_level = gr.find("level")
                elem_field = gr.find("field")
                if elem_field is not None and elem_level is not None:
                    if elem_level.text is not None and elem_field.text is not None:
                        if float(elem_level.text.strip(" \t\n\r")) == i:
                            # print("LEVEL %s -> %s" % (i,gr.xpath("field/text()")[0].strip(' \t\n\r')))
                            q.addGroup(PNGroupByQuery(i, elem_field.text.strip(" \t\n\r")))

        return q

    def action(self, n: str) -> "pineboolib.fllegacy.flaction.FLAction":
        """
        Obtiene la definición de una acción a partir de su nombre.

        Este método busca en los [id_modulo].xml la acción que se le pasa
        como nombre y construye y devuelve el objeto FLAction correspondiente.
        NO SE HACEN CHEQUEOS DE ERRORES SINTÁCTICOS EN EL XML.

        @param n Nombre de la accion
        @return Un objeto FLAction con la descripcion de la accion

        """
        if not self.db_:
            raise Exception("action. self.db_ is empty!")

        # FIXME: This function is really inefficient. Pineboo already parses the actions much before.
        if self.cacheAction_ and n in self.cacheAction_.keys():
            return self.cacheAction_[n]

        from pineboolib.fllegacy.flaction import FLAction

        util = FLUtil()
        doc = QDomDocument(n)
        list_modules = self.db_.managerModules().listAllIdModules()
        content_actions = ""

        for it in list_modules:

            content_actions = self.db_.managerModules().contentCached("%s.xml" % it)
            if not content_actions:
                continue

            if content_actions.find("<name>%s</name>" % n) > -1:
                break

        if n not in list_modules:
            if (
                not util.domDocumentSetContent(doc, content_actions)
                and n.find("alteredtable") == -1
            ):
                logger.warning(
                    "FLManager : "
                    + FLUtil().translate("application", "Error al cargar la accion ")
                    + n
                )

        doc_elem = doc.documentElement()
        no = doc_elem.firstChild()

        a = FLAction(n)
        # a.setTable(n)
        while not no.isNull():
            e = no.toElement()

            if not e.isNull():
                if e.tagName() == "action":
                    nl = e.elementsByTagName("name")
                    if nl.count() == 0:
                        self.logger.warning("Debe indicar la etiqueta <name> en acción '%s'" % n)
                        no = no.nextSibling()
                        continue
                    else:
                        it = nl.item(0).toElement()
                        if it.text() != n:
                            no = no.nextSibling()
                            continue

                    no2 = e.firstChild()
                    e2 = no2.toElement()

                    is_valid_name = False

                    while not no2.isNull():
                        e2 = no2.toElement()
                        if not e2.isNull():
                            if e2.tagName() == "name":
                                is_valid_name = e2.text() == n
                                break
                        no2 = no2.nextSibling()

                    no2 = e.firstChild()
                    e2 = no2.toElement()
                    if is_valid_name:
                        if not e2.isNull():
                            if e2.tagName() != "name":
                                logger.debug(
                                    "WARN: El primer tag de la acción '%s' no es name, se encontró '%s'."
                                    % (n, e2.tagName())
                                )
                        else:
                            self.logger.debug("WARN: Se encontró una acción vacia para '%s'." % n)

                    while is_valid_name and not no2.isNull():
                        e2 = no2.toElement()

                        if not e2.isNull():
                            if e2.tagName() == "name":
                                a.setName(e2.text())
                                no2 = no2.nextSibling()
                                continue
                            elif e2.tagName() == "scriptformrecord":
                                a.setScriptFormRecord(e2.text())
                                no2 = no2.nextSibling()
                                continue
                            elif e2.tagName() == "scriptform":
                                a.setScriptForm(e2.text())
                                no2 = no2.nextSibling()
                                continue
                            elif e2.tagName() == "table":
                                a.setTable(e2.text())
                                no2 = no2.nextSibling()
                                continue
                            elif e2.tagName() == "form":
                                a.setForm(e2.text())
                                no2 = no2.nextSibling()
                                continue
                            elif e2.tagName() == "formrecord":
                                a.setFormRecord(e2.text())
                                no2 = no2.nextSibling()
                                continue
                            elif e2.tagName() == "caption":
                                txt_ = e2.text()
                                txt_ = auto_qt_translate_text(txt_)
                                a.setCaption(txt_)
                                no2 = no2.nextSibling()
                                continue
                            elif e2.tagName() == "description":
                                txt_ = e2.text()
                                txt_ = auto_qt_translate_text(txt_)

                                if a.caption() == "":
                                    a.setDescription(txt_)
                                no2 = no2.nextSibling()
                                continue
                            elif e2.tagName() == "alias":
                                txt_ = e2.text()
                                txt_ = auto_qt_translate_text(txt_)

                                a.setCaption(txt_)
                                no2 = no2.nextSibling()
                                continue

                        no2 = no2.nextSibling()

                    no = no.nextSibling()
                    continue

            no = no.nextSibling()
        logger.trace("action: saving cache and finishing %s", n)

        self.cacheAction_[n] = a
        return a

    def existsTable(self, n: str, cache: bool = True) -> bool:
        """
        Comprueba si existe la tabla especificada en la base de datos.

        @param n      Nombre de la tabla que se quiere comprobar si existe
        @param cache  Si cierto consulta primero la cache de tablas, en caso contrario
                    realiza una consulta a la base para obtener las tablas existentes
        @return TRUE si existe la tabla, FALSE en caso contrario
        """
        if not self.db_ or n is None:
            return False

        if cache and n in self.listTables_:
            return True
        else:
            return self.db_.existsTable(n)

    def checkMetaData(self, mtd1, mtd2) -> Any:
        """
        Compara los metadatos de dos tablas,  la definición en XML de esas dos tablas se
        pasan como dos cadenas de caracteres.

        @param mtd1 Cadena de caracteres con XML que describe la primera tabla
        @param mtd2 Cadena de caracteres con XML que describe la segunda tabla
        @return TRUE si las dos descripciones son iguales, y FALSE en caso contrario
        """
        if isinstance(mtd1, str):
            if mtd1 == mtd2:
                return True
            return False
        else:
            if not mtd1 or not mtd2:
                return mtd1 == mtd2

            field_list = mtd1.fieldList()

            for field1 in field_list:
                if field1.isCheck():
                    continue

                field2 = mtd2.field(field1.name())
                if field2 is None:
                    return False

                if field2.isCheck():
                    continue

                if field1.type() != field2.type() or field1.allowNull() != field2.allowNull():
                    return False

                if field1.isUnique() != field2.isUnique() or field1.isIndex() != field2.isIndex():
                    return False

                if (
                    field1.length() != field2.length()
                    or field1.partDecimal() != field2.partDecimal()
                    or field1.partInteger() != field2.partInteger()
                ):
                    return False

            field_list = mtd2.fieldList()
            for field1 in field_list:
                if field1.isCheck():
                    continue

                field2 = mtd1.field(field1.name())
                if field2 is None:
                    return False

                if field2.isCheck():
                    continue

                if field1.type() != field2.type() or field1.allowNull() != field2.allowNull():
                    return False

                if field1.isUnique() != field2.isUnique() or field1.isIndex() != field2.isIndex():
                    return False

                if (
                    field1.length() != field2.length()
                    or field1.partDecimal() != field2.partDecimal()
                    or field1.partInteger() != field2.partInteger()
                ):
                    return False

            return True

    def alterTable(self, mtd1=None, mtd2=None, key=None, force=False) -> bool:
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
        if not self.db_:
            raise Exception("alterTable. self.db_ is empty!")

        return self.db_.dbAux().alterTable(mtd1, mtd2, key, force)

    def createTable(self, n_or_tmd) -> Any:
        """
        Crea una tabla en la base de datos.

        @param n_tmd Nombre o metadatos de la tabla que se quiere crear
        @return Un objeto PNTableMetaData con los metadatos de la tabla que se ha creado, o
          0 si no se pudo crear la tabla o ya existía
        """
        if not self.db_:
            raise Exception("createTable. self.db_ is empty!")

        util = FLUtil()
        if n_or_tmd is None:
            logger.debug("createTable: Called with no table.")
            return False

        if isinstance(n_or_tmd, str):
            tmd = self.metadata(n_or_tmd)
            if not tmd:
                return False

            if self.existsTable(tmd.name()):
                self.listTables_.append(n_or_tmd)
                return tmd
            else:
                if not tmd.isQuery():
                    logger.warning("FLMAnager :: No existe tabla %s", n_or_tmd)

            return self.createTable(tmd)
        else:
            if n_or_tmd.isQuery() or self.existsTable(n_or_tmd.name(), False):
                return n_or_tmd

            if not self.db_.createTable(n_or_tmd):
                logger.warning(
                    "createTable: %s", util.tr("No se ha podido crear la tabla ") + n_or_tmd.name()
                )
                return False
            else:
                logger.info("createTable: Created new table %r", n_or_tmd.name())

            return n_or_tmd

    def formatValueLike(self, *args, **kwargs) -> str:
        """
        Devuelve el contenido del valor de de un campo formateado para ser reconocido
        por la base de datos actual en condiciones LIKE, dentro de la clausura WHERE de SQL.

        Este método toma como parametros los metadatos del campo definidos con
        PNFieldMetaData. Además de TRUE y FALSE como posibles valores de un campo
        lógico también acepta los valores Sí y No (o su traducción al idioma correspondiente).
        Las fechas son adaptadas al forma AAAA-MM-DD, que es el formato reconocido por PostgreSQL .

        @param fMD Objeto PNFieldMetaData que describre los metadatos para el campo
        @param v Valor que se quiere formatear para el campo indicado
        @param upper Si TRUE convierte a mayúsculas el valor (si es de tipo cadena)
        """
        if not self.db_:
            raise Exception("formatValueLike. self.db_ is empty!")

        if not isinstance(args[0], str):
            if args[0] is None:
                return ""

            return self.formatValueLike(args[0].type(), args[1], args[2])
        else:
            return self.db_.formatValueLike(args[0], args[1], args[2])

    def formatAssignValueLike(self, *args, **kwargs) -> str:
        """
        Devuelve el contenido del valor de de un campo formateado para ser reconocido
        por la base de datos actual, dentro de la clausura WHERE de SQL.

        Este método toma como parametros los metadatos del campo definidos con
        PNFieldMetaData. Además de TRUE y FALSE como posibles valores de un campo
        lógico también acepta los valores Sí y No (o su traducción al idioma correspondiente).
        Las fechas son adaptadas al forma AAAA-MM-DD, que es el formato reconocido por PostgreSQL .

        @param fMD Objeto PNFieldMetaData que describre los metadatos para el campo
        @param v Valor que se quiere formatear para el campo indicado
        @param upper Si TRUE convierte a mayúsculas el valor (si es de tipo cadena)
        """
        if isinstance(args[0], PNFieldMetaData):
            # Tipo 1
            if args[0] is None:
                return "1 = 1"

            mtd = args[0].metadata()

            if not mtd:
                return self.formatAssignValueLike(args[0].name(), args[0].type(), args[1], args[2])

            if args[0].isPrimaryKey():
                return self.formatAssignValueLike(
                    mtd.primaryKey(True), args[0].type(), args[1], args[2]
                )

            fieldName = args[0].name()
            if mtd.isQuery() and fieldName.find(".") == -1:
                qry = PNSqlQuery(mtd.query())

                if qry:
                    fL = qry.fieldList()

                for it in fL:
                    if it.find(".") > -1:
                        itFieldName = it[it.find(".") + 1 :]
                    else:
                        itFieldName = it

                    if itFieldName == fieldName:
                        break
                # FIXME: deleteLater() is a C++ internal to clear the memory later. Not used in Python
                # qry.deleteLater()
            prefixTable = mtd.name()
            return self.formatAssignValueLike(
                "%s.%s" % (prefixTable, fieldName), args[0].type(), args[1], args[2]
            )

        elif isinstance(args[1], PNFieldMetaData):
            # tipo 2
            if args[1] is None:
                return "1 = 1"

            return self.formatAssignValueLike(args[0], args[1].type(), args[2], args[3])

        else:
            # tipo 3
            # args[0] = fieldName
            # args[1] = type
            # args[2] = valor
            # args[3] = upper

            if args[0] is None or not args[1]:
                return "1 = 1"

            is_text = args[1] in ["string", "stringlist"]
            format_value = self.formatValueLike(args[1], args[2], args[3])

            if not format_value:
                return "1 = 1"

            field_name = args[0]
            if is_text:
                if args[3]:
                    field_name = "upper(%s)" % args[0]

            return "%s%s" % (field_name, format_value)

    def formatValue(self, fMD_or_type: str, v: Any, upper: bool = False) -> str:
        # FIXME: This function sometimes returns integers!
        if not self.db_:
            raise Exception("formatValue. self.db_ is empty!")

        if not fMD_or_type:
            raise ValueError("fMD_or_type is required")

        if not isinstance(fMD_or_type, str):
            return self.formatValue(fMD_or_type.type(), v, upper)

        return self.db_.formatValue(fMD_or_type, v, upper)

    def formatAssignValue(self, *args, **kwargs) -> str:
        if args[0] is None:
            # print("FLManager.formatAssignValue(). Primer argumento vacio %s" % args[0])
            return "1 = 1"

        # print("tipo 0", type(args[0]))
        # print("tipo 1", type(args[1]))
        # print("tipo 2", type(args[2]))]

        if isinstance(args[0], PNFieldMetaData) and len(args) == 3:
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
                            fieldSection = f[pos + 1 :]
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

        elif isinstance(args[1], PNFieldMetaData) and isinstance(args[0], str):
            return self.formatAssignValue(args[0], args[1].type(), args[2], args[3])

        elif isinstance(args[0], PNFieldMetaData) and len(args) == 2:
            return self.formatAssignValue(args[0].name(), args[0], args[1], False)
        else:
            if args[1] is None:
                return "1 = 1"

            formatV = self.formatValue(args[1], args[2], args[3])
            if formatV is None:
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

    def metadataField(
        self, field: QDomElement, v: bool = True, ed: bool = True
    ) -> "PNFieldMetaData":
        """
        Crea un objeto PNFieldMetaData a partir de un elemento XML.

        Dado un elemento XML, que contiene la descripción de un
        campo de una tabla construye y agrega a una lista de descripciones
        de campos el objeto PNFieldMetaData correspondiente, que contiene
        dicha definición del campo. Tambien lo agrega a una lista de claves
        compuesta, si el campo construido pertenece a una clave compuesta.
        NO SE HACEN CHEQUEOS DE ERRORES SINTÁCTICOS EN EL XML.

        @param field Elemento XML con la descripción del campo
        @param v Valor utilizado por defecto para la propiedad visible
        @param ed Valor utilizado por defecto para la propiedad editable
        @return Objeto PNFieldMetaData que contiene la descripción del campo
        """
        if not field:
            raise ValueError("field is required")

        util = FLUtil()

        ck = False
        n: str
        a: str
        ol: Optional[str] = None
        rX = None
        assocBy = None
        assocWith = None
        so = None

        aN = True
        iPK = False
        c = False
        iNX = False
        uNI = False
        coun = False
        oT = False
        vG = True
        fullCalc = False
        trimm = False

        t: Optional[str] = None
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

                elif e.tagName() == "name":
                    n = e.text()
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "alias":
                    a = auto_qt_translate_text(e.text())
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "null":
                    aN = e.text() == "true"
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "pk":
                    iPK = e.text() == "true"
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "type":
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

                elif e.tagName() == "length":
                    length = int(e.text())
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "regexp":
                    rX = e.text()
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "default":
                    if e.text().find("QT_TRANSLATE_NOOP") > -1:
                        dV = auto_qt_translate_text(e.text())
                    else:
                        dV = e.text()

                    no = no.nextSibling()
                    continue

                elif e.tagName() == "outtransaction":
                    oT = e.text() == "true"
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "counter":
                    coun = e.text() == "true"
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "calculated":
                    c = e.text() == "true"
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "fullycalculated":
                    fullCalc = e.text() == "true"
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "trimmed":
                    trimm = e.text() == "true"
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "visible":
                    v = e.text() == "true"
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "visiblegrid":
                    vG = e.text() == "true"
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "editable":
                    ed = e.text() == "true"
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "partI":
                    pI = int(e.text())
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "partD":
                    pD = int(e.text())
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "index":
                    iNX = e.text() == "true"
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "unique":
                    uNI = e.text() == "true"
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "ck":
                    ck = e.text() == "true"
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "optionslist":
                    ol = e.text()
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "searchoptions":
                    so = e.text()
                    no = no.nextSibling()
                    continue

            no = no.nextSibling()

        f = PNFieldMetaData(
            n,
            util.translate("Metadata", a),
            aN,
            iPK,
            t,
            length,
            c,
            v,
            ed,
            pI,
            pD,
            iNX,
            uNI,
            coun,
            dV,
            oT,
            rX,
            vG,
            True,
            ck,
        )
        f.setFullyCalculated(fullCalc)
        f.setTrimed(trimm)

        if ol is not None:
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

                elif e.tagName() == "associated":
                    noas = e.firstChild()
                    while not noas.isNull():
                        eas = noas.toElement()
                        if not eas.isNull():
                            if eas.tagName() == "with":
                                assocWith = eas.text()
                                noas = noas.nextSibling()
                                continue

                            elif eas.tagName() == "by":
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

    def metadataRelation(self, relation: QDomElement) -> "PNRelationMetaData":
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
            raise ValueError("relation is required")

        fT = ""
        fF = ""
        rC = PNRelationMetaData.RELATION_M1
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

                elif e.tagName() == "field":
                    fF = e.text()
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "card":
                    if e.text() == "1M":
                        rC = PNRelationMetaData.RELATION_1M

                    no = no.nextSibling()
                    continue

                elif e.tagName() == "delC":
                    dC = e.text() == "true"
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "updC":
                    uC = e.text() == "true"
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "checkIn":
                    cI = e.text() == "true"
                    no = no.nextSibling()
                    continue

            no = no.nextSibling()

        return PNRelationMetaData(fT, fF, rC, dC, uC, cI)

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

    def createSystemTable(self, n: str) -> bool:
        """
        Crea una tabla del sistema.

        Este método lee directamente de disco el fichero con la descripción de una tabla
        del sistema y la crea en la base de datos. Su uso normal es para inicializar
        el sistema con tablas iniciales.

        @param n Nombre de la tabla.
        @return Un objeto PNTableMetaData con los metadatos de la tabla que se ha creado, o
          False si no se pudo crear la tabla o ya existía
        """
        util = FLUtil()
        if not self.existsTable(n):
            doc = QDomDocument()
            _path = filedir("..", "share", "pineboo", "tables")
            from pineboolib.application.types import Dir

            dir = Dir(_path)
            _tables = dir.entryList("%s.mtd" % n)

            for f in _tables:
                path = "%s/%s" % (_path, f)
                _file = QtCore.QFile(path)
                _file.open(QtCore.QIODevice.ReadOnly)
                _in = QtCore.QTextStream(_file)
                _data = _in.readAll()
                if not util.domDocumentSetContent(doc, _data):
                    logger.warning(
                        "FLManager::createSystemTable: %s",
                        self.tr("Error al cargar los metadatos para la tabla %s" % n),
                    )
                    return False
                else:
                    docElem = doc.documentElement()

                    mtd = self.createTable(self.metadata(docElem, True))
                    if mtd:
                        return True
                    else:
                        return False
                # FIXME: f.close() is closing an unknown object. it is a file?
                # ... also, close, but we have return inside the loop.
                # f.close()

        return False

    def loadTables(self) -> None:
        """
        Carga en la lista de tablas los nombres de las tablas de la base de datos
        """
        if not self.db_:
            raise Exception("loadTables. self.db_ is empty!")

        if not self.listTables_:
            self.listTables_ = []
        else:
            self.listTables_.clear()

        self.listTables_ = self.db_.dbAux().tables()

    def cleanupMetaData(self) -> None:
        """
        Limpieza la tabla flmetadata, actualiza el cotenido xml con el de los fichero .mtd
        actualmente cargados
        """
        if not self.db_:
            raise Exception("cleanupMetaData. self.db_ is empty!")

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

        q = PNSqlQuery(None, "dbAux")
        q.exec_("SELECT tabla,xml FROM flmetadata")
        while q.next():
            self.dictKeyMetaData_[str(q.value(0))] = str(q.value(1))

        c = PNSqlCursor("flmetadata", True, "dbAux")

        q2 = PNSqlQuery(None, "dbAux")
        q2.exec_(
            "SELECT nombre,sha FROM flfiles WHERE nombre LIKE '%.mtd' and nombre not like '%%alteredtable%'"
        )
        while q2.next():
            table = str(q2.value(0))
            table = table.replace(".mtd", "")
            tmd = self.metadata(table)
            if not self.existsTable(table):
                self.createTable(table)
            if not tmd:
                logger.warning(
                    "FLManager::cleanupMetaData %s",
                    FLUtil().translate(
                        "application", "No se ha podido crear los metadatatos para la tabla %s"
                    )
                    % table,
                )

            c.select("tabla='%s'" % table)
            if c.next():
                buffer = c.primeUpdate()
                buffer.setValue("xml", q2.value(1))
                c.update()
            self.dictKeyMetaData_[table] = q2.value(1)

    def isSystemTable(self, n: str) -> bool:
        """
        Para saber si la tabla dada es una tabla de sistema.

        @param n Nombre de la tabla.
        @return TRUE si es una tabla de sistema
        """
        from pineboolib.application import project

        if project._DGI and n in project.DGI.sys_mtds():
            return True

        if n[0:2] != "fl":
            return False

        if n.endswith(".mtd"):
            n = n[:-4]

        if n in (
            "flfiles",
            "flmetadata",
            "flmodules",
            "flareas",
            "flserial",
            "flvar",
            "flsettings",
            "flseqs",
            "flupdates",
        ):
            return True

        return False

    def storeLargeValue(self, mtd, largeValue: str) -> Optional[str]:
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
        if not self.db_:
            raise Exception("storeLareValue. self.db_ is empty!")

        if largeValue[0:3] == "RK@" or not mtd:
            return None

        tableName = mtd.name()
        # if self.isSystemTable(tableName):
        #    return None

        tableLarge = None
        from pineboolib.fllegacy.flapplication import aqApp

        if aqApp.singleFLLarge():
            tableLarge = "fllarge"
        else:
            tableLarge = "fllarge_%s" % tableName
            if not self.existsTable(tableLarge):
                mtdLarge = PNTableMetaData(tableLarge, tableLarge)
                fieldLarge = PNFieldMetaData("refkey", "refkey", False, True, "string", 100)
                mtdLarge.addFieldMD(fieldLarge)
                fieldLarge2 = PNFieldMetaData("sha", "sha", True, False, "string", 50)
                mtdLarge.addFieldMD(fieldLarge2)
                fieldLarge3 = PNFieldMetaData("contenido", "contenido", True, False, "stringlist")
                mtdLarge.addFieldMD(fieldLarge3)
                mtdAux = self.createTable(mtdLarge)
                mtd.insertChild(mtdLarge)
                if not mtdAux:
                    return None

        util = FLUtil()
        sha = str(util.sha1(largeValue))
        # print("-->", tableName, sha)
        refKey = "RK@%s@%s" % (tableName, sha)
        q = PNSqlQuery(None, "dbAux")
        q.setSelect("refkey")
        q.setFrom("fllarge")
        q.setWhere(" refkey = '%s'" % refKey)
        if q.exec_() and q.first():
            if not q.value(0) == sha:
                sql = "UPDATE %s SET contenido = '%s' WHERE refkey ='%s'" % (
                    tableLarge,
                    largeValue,
                    refKey,
                )
                if not util.execSql(sql, "Aux"):
                    logger.warning(
                        "FLManager::ERROR:StoreLargeValue.Update %s.%s", tableLarge, refKey
                    )
                    return None
        else:
            sql = "INSERT INTO %s (contenido,refkey) VALUES ('%s','%s')" % (
                tableLarge,
                largeValue,
                refKey,
            )
            if not util.execSql(sql, "Aux"):
                logger.warning("FLManager::ERROR:StoreLargeValue.Insert %s.%s", tableLarge, refKey)
                return None

        return refKey

    def fetchLargeValue(self, refKey: str) -> Optional[str]:
        """
        Obtiene el valor de gran tamaño segun su clave de referencia.

        @param refKey Clave de referencia. Esta clave se suele obtener mediante FLManager::storeLargeValue
        @return Valor de gran tamaño almacenado
        """
        if refKey is None:
            return None
        if not refKey[0:3] == "RK@":
            return None

        from pineboolib.fllegacy.flapplication import aqApp

        tableName = "fllarge" if aqApp.singleFLLarge() else "fllarge_" + refKey.split("@")[1]

        if not self.existsTable(tableName):
            return None

        q = PNSqlQuery(None, "Aux")
        q.setSelect("contenido")
        q.setFrom(tableName)
        q.setWhere(" refkey = '%s'" % refKey)
        if q.exec_() and q.first():
            v = q.value(0)
            del q
            # print(v)
            v = cacheXPM(v)
            # print(v)

            return v

        return None

    def initCount(self) -> int:
        """
        Uso interno. Indica el número de veces que se ha llamado a FLManager::init().
        """
        return self.initCount_
