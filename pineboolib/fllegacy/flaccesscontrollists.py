# -*- coding: utf-8 -*-
"""
FLAccessControlList Module.

Manage access lists to limit the application to users..
"""

from PyQt5.QtXml import QDomDocument  # type: ignore
from PyQt5 import QtCore  # type: ignore

from pineboolib.application.database.pnsqlquery import PNSqlQuery
from pineboolib.fllegacy.flaccesscontrolfactory import FLAccessControlFactory
from pineboolib import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class FLAccessControlLists(object):
    """FLAccessControlList Class."""

    """
    Nombre que identifica la lista de control de acceso actualmente establecida.

    Generalmente corresponderá con el identificador del registro de la tabla "flacls" que se utilizó para crear "acl.xml".
    """
    _name: str

    """
    Diccionario (lista) que mantiene los objetos de las reglas de control de acceso establecidas.
    La clave que identifica a cada objeto está formada por el siguiente literal:

    \\code

    FLAccessControl::type + "::" + FLAccessControl::name + "::" + FLAccessControl::user

    \\endcode
    """

    _access_control_list: Dict[str, Any]

    def __init__(self):
        """Initialize the class."""

        self._name = None
        self._access_control_list = []

    def __del__(self) -> None:
        """Process when destroying the class."""

        if self._access_control_list:
            self._access_control_list.clear()
            del self._access_control_list

    def name(self) -> str:
        """
        Return the name that identifies the currently established access control list.

        @return Name the current access control list.
        """
        return self._name

    def init(self, aclXml: str = None) -> None:
        """
        Read the file "acl.xml" and establish a new access control list.

        If the file "acl.xml" cannot be read, the access control list is empty and
        no access control will be processed on any object.

        @param aclXml XML content with the definition of the access control list.
        """
        from pineboolib.fllegacy.flutil import FLUtil

        util = FLUtil()
        if aclXml is None:
            from pineboolib.application import project

            if project.conn is None:
                raise Exception("Project is not connected yet")

            aclXml = project.conn.managerModules().content("acl.xml")

        doc = QDomDocument("ACL")
        if self._access_control_list:
            self._access_control_list.clear()
            del self._access_control_list
            self._access_control_list = {}

        if aclXml and not util.domDocumentSetContent(doc, aclXml):
            QtCore.qWarning(
                "FLAccessControlList : " + FLUtil().tr("Lista de control de acceso errónea")
            )
            return

        self._access_control_list = {}
        # self._access_control_list.setAutoDelete(True)

        docElem = doc.documentElement()
        no = docElem.firstChild()

        while not no.isNull():
            e = no.toElement()
            if e:
                if e.tagName() == "name":
                    self._name = e.text()
                    no = no.nextSibling()
                    continue

                ac = FLAccessControlFactory().create(e.tagName())
                if ac:
                    ac.set(e)
                    self._access_control_list["%s::%s::%s" % (ac.type(), ac.name(), ac.user())] = ac
                    no = no.nextSibling()
                    continue

            no = no.nextSibling()

    def process(self, obj: Any) -> None:
        """
        Process a high-level object according to the established access control list.

        @param obj High-level object to which access control is applied. It must be or inherit from the QObject class.
        """
        if obj is None or not self._access_control_list:
            return

        if not self._access_control_list:
            return

        type = FLAccessControlFactory().type(obj)
        name = obj.objectName() if hasattr(obj, "objectName") else ""

        from pineboolib.application import project

        if project.conn is None:
            raise Exception("Project is not connected yet")

        user = project.conn.user()
        if type == "" or name == "" or user == "":
            return

        ac = self._access_control_list["%s::%s::%s" % (type, name, user)]
        if ac:
            ac.processObject(obj)

    def installACL(self, idacl: str) -> None:
        """
        Create a new file "acl.xml" and store it replacing the previous one, if it exists.

        @param idacl Record identifier of the "flacls" table to use to create "acl.xml".
        """
        doc = QDomDocument("ACL")

        root = doc.createElement("ACL")
        doc.appendChild(root)

        name = doc.createElement("name")
        root.appendChild(name)
        n = doc.createTextNode(idacl)
        name.appendChild(n)

        q = PNSqlQuery()

        q.setTablesList("flacs")
        q.setSelect("idac,tipo,nombre,iduser,idgroup,degroup,permiso")
        q.setFrom("flacs")
        q.setWhere("idacl='%s'" % idacl)
        q.setOrderBy("prioridad DESC, tipo")
        q.setForwardOnly(True)

        if q.exec_():
            # step = 0
            # progress = util.ProgressDialog(util.tr("Instalando control de acceso..."), None, q.size(), None, None, True)
            # progress.setCaption(util.tr("Instalando ACL"))
            # progress.setMinimumDuration(0)
            # progress.setProgress(++step)
            while q.next():
                self.makeRule(q, doc)
                # progress.setProgress(++step)

            from pineboolib.application import project

            if project.conn is None:
                raise Exception("Project is not connected yet")

            project.conn.managerModules().setContent("acl.xml", "sys", doc.toString())

    def makeRule(self, q: PNSqlQuery, d: Any) -> None:
        """
        Create the corresponding DOM node (s) to a record in the "flacs" table.

        Use FLAccessControlLists :: makeRuleUser or FLAccessControlLists :: makeRuleGroup depending on whether the registry
        to which the query points indicates that the rule is for a user or a group. If the record indicates a
        user will create a user rule, if you indicate a group a user rule will be created for each of
        Group member users.

        @param q Query about the "flacs" table positioned in the register to be used to construct the rule (s).
        @param d DOM / XML document in which you will insert the node (s) that describe the access control rule (s).
        """
        if not q or not d:
            return

        if q.value(5) in ("True", True, "true"):
            self.makeRuleGroup(q, d, str(q.value(4)))
        else:
            self.makeRuleUser(q, d, str(q.value(3)))

    def makeRuleUser(self, q: PNSqlQuery, d: Any, iduser: str) -> None:
        """
        Create a DOM node corresponding to a record in the "flacs" table and for a given user.

        @param q Query about the "flacs" table positioned in the register to be used to construct the rule.
        @param d DOM / XML document in which you will insert the node that describes the access control rule.
        @param iduser Identifier of the user used in the access control rule.
        """
        if not iduser or not q or not d:
            return

        ac = FLAccessControlFactory().create(str(q.value(1)))

        if ac:
            ac.setName(str(q.value(2)))
            ac.setUser(iduser)
            ac.setPerm(str(q.value(6)))

            qAcos = PNSqlQuery()
            qAcos.setTablesList("flacos")
            qAcos.setSelect("nombre,permiso")
            qAcos.setFrom("flacos")
            qAcos.setWhere("idac ='%s'" % q.value(0))
            qAcos.setForwardOnly(True)

            acos = []

            if qAcos.exec_():
                while qAcos.next():
                    acos.append(str(qAcos.value(0)))
                    acos.append((qAcos.value(1)))

            ac.setAcos(acos)
            ac.get(d)

            del ac

    def makeRuleGroup(self, q: PNSqlQuery, d: Any, idgroup: str = "") -> None:
        """
        Create several DOM nodes corresponding to a record in the "flacs" table and for a specific user group.

        The function of this method is to create a rule for each of the group member users, using
        FLAccessControlLists :: makeRuleUser.

        @param q Query about the "flacs" table positioned in the register to use to build the rules.
        @param d DOM / XML document in which the nodes that describe the access control rules will be inserted.
        @param idgroup Identifier of the user group.
        """
        if idgroup == "" or not q or not d:
            return

        qU = PNSqlQuery()

        qU.setTablesList("flusers")
        qU.setSelect("iduser")
        qU.setFrom("flusers")
        qU.setWhere("'idgroup='%s'" % idgroup)
        qU.setForwardOnly(True)

        if qU.exec_():
            while qU.next():
                self.makeRuleUser(q, d, str(qU.value(0)))
