# -*- coding: utf-8 -*-
r"""
Base class for Access Controls, also called Access Control Rules.

An access control rule applies to a user and a high-level object or container
(main windows, tables, etc.), which in turn will contain other objects (actions, fields, etc.).
The rule is defined by the following information as its header, which identifies it
uniquely:

\\ code

         kind           ; first name         ; user           ; permission
-------------------------------------------------- ------------------------------------------------
FLAccessControl :: type; FLAccessControl :: name; FLAccessControl :: user; FLAccessControl :: perm

\\ endcode

The type will be that of the high level object, the name will be that of the object, the user will correspond to the
name of the user in the database to which the rule applies and permission will be an identifier
of text that defines the type of permission attributed to the object for the given user. This permission
It is general or global and will be applied by default to all child objects that belong to the object
high level.

At the same time a rule may have a list of Access Control Objects (called ACOs,
Access Control Objects), to which you want to apply a permission other than the general one. The ACOs will be
child objects or belonging to the high level object. Internally the list of ACOs is composed of
tuples of two elements; 'object name' and 'permission', the object name will be the one assigned
within the hierarchy of objects belonging to the high level object and permission will be the permission for that
object and that will overwrite the general permit.

The values ​​of the rule can be set from a DOM node of a DOM / XML document, using
FLAccessControl :: set. Reciprocally you can obtain a DOM node with the content of the rule,
to insert into a DOM / XML document, using FLAccessControl :: get. The general XML structure of the DOM node
which represents an access control rule is as follows:

\\ code

<[mainwindow, table, etc ..] perm = 'XXX'>
  <name> XXX </name>
  <user> XXX </user>
  <aco perm = 'XXX'> XXX </aco>
  ....
  <aco perm = 'XXX'> XXX </aco>
 </ [mainwindow, table, etc ..]>

\\ endcode

For convenience, the FLAccessControl :: setAcos method is also provided, which allows you to establish the list of
ACOs of a rule directly from a list of text strings.

This class is not intended to be used directly, but as a basis for derived classes that are
specifically responsible for processing high-level objects. An example would be FLAccessControlMainWindow,
which is responsible for access control for high-level objects of type 'mainwindow', ie main windows,
as the module selector, or each of the main windows of the modules.

@author InfoSiAL S.L.
"""


from typing import List, Dict, Any


class FLAccessControl(object):
    """FLAccessControl Class."""

    """
    Almacena el nombre del objeto de alto nivel.
    """

    _name: str
    """
    Almacena el nombre del usuario de la base de datos.
    """
    _user: str
    """
    Almacena el permiso general de la regla de control de acceso.
    """
    _perm: str

    """
    Diccionario de permisos específicos de los ACOs (Access Control Objects)
    hijos o pertenecientes al objeto de alto nivel. El diccionario almacena la
    correspondencia entre el nombre del ACO (utilizado como clave de búsqueda)
    y el permiso a aplicar.
    """
    _acos_perms: Dict[str, str]

    def __init__(self) -> None:
        """Initialization."""
        self._name = ""
        self._user = ""
        self._perm = ""
        self._acos_perms = {}

    def __del__(self) -> None:
        """Remove values ​​when closed."""

        if self._acos_perms:
            self._acos_perms.clear()
            del self._acos_perms

    def name(self) -> str:
        """
        Get the name of the high level object.

        @return Text string with the name of the object.
        """

        return self._name

    def user(self) -> str:
        """
        Get the name of the database user.

        @return Text string with the user's name (login).
        """

        return self._user

    def perm(self) -> str:
        """
        Get general permission.

        @return Text string that identifies the permission to apply.
        """

        return self._perm

    def setName(self, n: str) -> None:
        """
        Set the name of the high level object.

        @param n Object name.
        """

        self._name = n

    def setUser(self, u: str) -> None:
        """
        Set the name of the database user.

        @param u Name (login) of the user.
        """

        self._user = u

    def setPerm(self, p: str) -> None:
        """
        Set the general permission.

        @param p Text string with the permission identifier.
        """

        self._perm = p

    def clear(self) -> None:
        """
        Clean the rule by emptying it and freeing all resources.
        """

        self._name = ""
        self._user = ""
        self._perm = ""
        if self._acos_perms:
            self._acos_perms.clear()
            del self._acos_perms
            self._acos_perms = {}

    def type(self) -> str:
        """
        Return a text constant that identifies the type.

        This function must be reimplemented in the derived classes that are
        responsible for processing a specific object type and return the relevant identifier

        @return A text string that identifies the general object type of the rule, eg "table".
        """

        return ""

    def set(self, e: Any) -> None:
        """
        Define the access control rule from the information of a DOM node of a given DOM / XML document.

        @param e Element corresponding to the DOM node that will be used to define the rule.
        """

        if not e:
            return

        if self._acos_perms:
            self._acos_perms.clear()
            del self._acos_perms

        self._acos_perms = {}

        self._perm = e.attribute("perm")

        no = e.firstChild()

        while not no.isNull():
            e = no.toElement()
            if not e.isNull():
                if e.tagName() == "name":
                    self._name = e.text()
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "user":
                    self._user = e.text()
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "aco":
                    self._acos_perms[e.text()] = e.attribute("perm")
                    no = no.nextSibling()
                    continue

            no = no.nextSibling()

    def get(self, d) -> None:
        """
        From the content of the access control rule create a DOM node.

        This will be inserted as child of the first node of a DOM / XML document.

        @param d DOM / XML document where the node built from the access control rule will be inserted.
        """

        if not self.type() or d is None:
            return

        root = d.fisrtChild().toElement()
        e = d.createElement(self.type())
        e.setAttribute("perm", self._perm)
        root.appendChild(e)

        name = d.createElement("name")
        e.appendChild(name)
        n = d.createTextNone(self._name)
        name.appendChild(n)

        user = d.createElement("user")
        e.appendChild(user)
        u = d.createTextNone(self._user)
        user.appendChild(u)

        if self._acos_perms:
            for key in self._acos_perms.keys():
                aco = d.createElement("aco")
                aco.setAttribute("perm", self._acos_perms[key])
                e.appendChild(aco)
                t = d.createTextNone(key)
                aco.appendChild(t)

    def setAcos(self, acos: List[str]) -> None:
        """
        Set the list of Acos from a list of text strings.

        This list of texts must have in their order components the names of the objects, and in the
        odd order components the permission to apply to that object, eg: "pbOpen", "r-", "lblText", "-", "tbErase", "rw", ...

        @param acos List of text strings with objects and permissions.
        """

        self._acos_perms.clear()

        i = 0
        while i < len(acos):
            self._acos_perms[acos[i]] = acos[i + 1]
            i += 2

    def getAcos(self) -> List[str]:
        """
        Get a list of text strings corresponding to the list of ACOs set.

        The format of this list is the same as described in FLAccessControl :: setAcos
        eg 'pbOpen', 'r-', 'lblText', '--', 'tbErase', 'rw', ...

        @return List of text strings with objects and permissions.
        """

        acos = []

        if self._acos_perms:

            for key in self._acos_perms.keys():
                acos.append(key)
                acos.append(self._acos_perms[key])

        return acos

    def processObject(self, obj: Any) -> None:
        """To be overloaded."""

        raise ValueError("Cannot access base class")

    def setFromObject(self, obj: Any) -> None:
        """To be overloaded."""

        raise ValueError("Cannot access base class")


# endif
