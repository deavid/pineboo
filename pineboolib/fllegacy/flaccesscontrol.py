# -*- coding: utf-8 -*-
"""
Clase base para Controles de Acceso, también denominados Reglas de Control de Acceso.

Una regla de control de acceso se aplica a un usuario y a un objeto de alto nivel o contenedor
(ventanas principales,tablas, etc..), que a su vez contendrán otros objetos (acciones, campos, etc..).
La regla está definida por la siguiente información como cabecera de la misma, que la identifica
unívocamente:

\\code

         tipo           ;         nombre         ;      usuario           ;      permiso
--------------------------------------------------------------------------------------------------
FLAccessControl::type ; FLAccessControl::name ; FLAccessControl::user ; FLAccessControl::perm

\\endcode

El tipo será el del objeto de alto nivel, el nombre será el del objeto, el usuario corresponderá al
nombre del usuario en la base de datos al que se le aplica la regla y permiso será un identificador
de texto que define el tipo de permiso que se atribuye al objeto para el usuario dado. Este permiso
es general o global y se aplicará por defecto a todos los objetos hijos o que pertenezcan al objeto
de alto nivel.

Al mismo tiempo una regla podrá tener una lista de Objetos de Control de Acceso (denominados ACOs,
Access Control Objects), a los que se les quiere aplicar un permiso distinto al general. Los ACOs serán
objetos hijo o pertenecientes al objeto de alto nivel. Internamente la lista de ACOs está compuesta por
tuplas de dos elementos; "nombre de objeto" y "permiso", el nombre de objeto será el que tiene asignado
dentro de la jerarquía de objetos pertenecientes al objeto de alto nivel y permiso será el permiso para ese
objeto y que sobreescribirá al permiso general.

Los valores de la regla se podrán establecer a partir de un nodo DOM de un documento DOM/XML, mediante
FLAccessControl::set . De forma recíproca se podrá obtener un nodo DOM con el contenido de la regla,
a insertar en un documento DOM/XML, mediante FLAccessControl::get . La estructura general en XML del nodo DOM
que representa una regla de control de acceso es la siguiente:

\\code

 <[mainwindow,table,etc..] perm="XXX">
  <name>XXX</name>
  <user>XXX</user>
  <aco perm="XXX">XXX</aco>
  ....
  <aco perm="XXX">XXX</aco>
 </[mainwindow,table,etc..]>

\\endcode

Por comodidad, también se proporciona el método FLAccessControl::setAcos, que permite establecer la lista de
ACOs de una regla directamente a partir de una lista de cadenas de texto.

Esta clase no está pensada para ser usada directamente, sino como base para clases derivadas que se
encargan específicamente del procesamiento de objetos de alto nivel. Un ejemplo sería FLAccessControlMainWindow,
que se encarga de control de acceso para objetos de alto nivel de tipo "mainwindow", es decir ventanas principales,
como el selector de módulos, o cada una de las ventanas principales de los módulos.

@author InfoSiAL S.L.
"""


from typing import List, Dict, Any
from typing import NoReturn


class FLAccessControl(object):

    """
    Almacena el nombre del objeto de alto nivel.
    """

    name_: str
    """
    Almacena el nombre del usuario de la base de datos.
    """
    user_: str
    """
    Almacena el permiso general de la regla de control de acceso.
    """
    perm_: str

    """
    Diccionario de permisos específicos de los ACOs (Access Control Objects)
    hijos o pertenecientes al objeto de alto nivel. El diccionario almacena la
    correspondencia entre el nombre del ACO (utilizado como clave de búsqueda)
    y el permiso a aplicar.
    """
    acosPerms_: Dict[str, str]

    def __init__(self) -> None:
        self.name_ = ""
        self.user_ = ""
        self.perm_ = ""
        self.acosPerms_ = {}

    """
    Destructor
    """

    def __del__(self) -> None:
        if self.acosPerms_:
            self.acosPerms_.clear()
            del self.acosPerms_

    """
    Obtiene el nombre del objeto de alto nivel.

    @return Cadena de texto con el nombre del objeto.
    """

    def name(self) -> str:
        return self.name_

    """
    Obtiene el nombre del usuario de la base de datos.

    @return Cadena de texto con el nombre (login) del usuario.
    """

    def user(self) -> Any:
        return self.user_

    """
    Obtiene el permiso general.

    @return Cadena de texto que identifica el permiso a aplicar.
    """

    def perm(self) -> str:
        return self.perm_

    """
    Establece el nombre del objeto de alto nivel.

    @param n Nombre del objeto.
    """

    def setName(self, n: str) -> None:
        self.name_ = n

    """
    Establece el nombre del usuario de la base de datos.

    @param u Nombre (login) del usuario.
    """

    def setUser(self, u) -> None:
        self.user_ = u

    """
    Establece el permiso general.

    @param p Cadena de texto con el identificador del permiso.
    """

    def setPerm(self, p: str) -> None:
        self.perm_ = p

    """
    Limpia la regla vaciándola y liberando todos los recursos
    """

    def clear(self) -> None:
        self.name_ = ""
        self.user_ = ""
        self.perm_ = ""
        if self.acosPerms_:
            self.acosPerms_.clear()
            del self.acosPerms_
            self.acosPerms_ = {}

    """
    Devuelve una constante de texto que identifica el tipo.

    Esta función deberá ser reimplementada en las clases derivadas que se
    encargan del procesamiento de un tipo de objeto concreto y devolver
    el identificador pertinente.

    @return Cadena de texto que identifica al tipo de objeto general de la regla, p.e.: "table".
    """

    def type(self) -> str:
        return ""

    """
    Define la regla de control de acceso a partir de la información de un nodo DOM de un documento DOM/XML dado.

    @param e Elemento correspondiente al nodo DOM que se utilizará para definir la regla.
    """

    def set(self, e) -> None:
        if not e:
            return

        if self.acosPerms_:
            self.acosPerms_.clear()
            del self.acosPerms_

        self.acosPerms_ = {}

        self.perm_ = e.attribute("perm")

        no = e.firstChild()

        while not no.isNull():
            e = no.toElement()
            if not e.isNull():
                if e.tagName() == "name":
                    self.name_ = e.text()
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "user":
                    self.user_ = e.text()
                    no = no.nextSibling()
                    continue

                elif e.tagName() == "aco":
                    self.acosPerms_[e.text()] = e.attribute("perm")
                    no = no.nextSibling()
                    continue

            no = no.nextSibling()

    """
    A partir del contenido de la regla de control de acceso crea un nodo DOM que se insertará como
    hijo del primer nodo de un documento DOM/XML.

    @param d Documento DOM/XML donde se insertará el nodo construido a partir de la regla de control de acceso.
    """

    def get(self, d) -> None:
        if not self.type() or d is None:
            return

        root = d.fisrtChild().toElement()
        e = d.createElement(self.type())
        e.setAttribute("perm", self.perm_)
        root.appendChild(e)

        name = d.createElement("name")
        e.appendChild(name)
        n = d.createTextNone(self.name_)
        name.appendChild(n)

        user = d.createElement("user")
        e.appendChild(user)
        u = d.createTextNone(self.user_)
        user.appendChild(u)

        if self.acosPerms_:
            for key in self.acosPerms_.keys():
                aco = d.createElement("aco")
                aco.setAttribute("perm", self.acosPerms_[key])
                e.appendChild(aco)
                t = d.createTextNone(key)
                aco.appendChild(t)

    """
    Establece la lista de Acos a partir de una lista de cadenas de texto.

    Esta lista de textos deberá tener en sus componentes de orden par los nombres de los objetos,y en los
    componentes de orden impar el permiso a aplicar a ese objeto, p.e.: "pbAbrir", "r-", "lblTexto", "--", "tbBorrar", "rw",...

    @param acos Lista de cadenas de texto con los objetos y permisos.
    """

    def setAcos(self, acos: List[str]) -> None:
        if acos is None:
            return

        if self.acosPerms_:
            self.acosPerms_.clear()
            del self.acosPerms_

        self.acosPerms_ = {}

        # nameAcos = None
        i = 0
        while i < len(acos):
            self.acosPerms_[acos[i]] = acos[i + 1]
            i += 2

    """
    Obtiene una lista de cadenas de texto correspondiente a la lista de ACOs establecida

    El formato de esta lista es igual al descrito en FLAccessControl::setAcos
    p.e.: "pbAbrir", "r-", "lblTexto", "--", "tbBorrar", "rw",...

    @return Lista de cadenas de texto con los objetos y permisos.
    """

    def getAcos(self) -> List[str]:
        acos = []

        if self.acosPerms_:

            for key in self.acosPerms_.keys():
                acos.append(key)
                acos.append(self.acosPerms_[key])

        return acos

    def processObject(self, o) -> NoReturn:
        raise ValueError("Cannot access base class")

    def setFromObject(self, obj: object) -> None:
        raise ValueError("Cannot access base class")


# endif
