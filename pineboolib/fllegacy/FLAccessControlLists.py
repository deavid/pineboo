from PyQt5.Qt import QDomDocument, QProgressDialog

from pineboolib.flcontrols import ProjectClass
from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from pineboolib.fllegacy.FLAccessControlFactory import FLAccessControlFactory
from pineboolib import decorators

class FLAccessControlLists(ProjectClass):
  
    """
    Nombre que identifica la lista de control de acceso actualmente establecida.

    Generalmente corresponderá con el identificador del registro de la tabla "flacls" que se utilizó para crear "acl.xml".
    """
    name_ = None
    

    """
    Diccionario (lista) que mantiene los objetos de las reglas de control de acceso establecidas.
    La clave que identifica a cada objeto está formada por el siguiente literal:

    \code

    FLAccessControl::type + "::" + FLAccessControl::name + "::" + FLAccessControl::user

    \endcode
    """
    
    accessControlList_ = {}
  
  
    """
    Constructor
    """
  
    def __init__(self):
        super(FLAccessControlLists, self).__init__()
        
        self.name_ = None
        self.accessControlList_ = {}

    """
    Destructor
    """
    def __del__(self):
        if self.accessControlList_:
            self.accessControlList_.clear()
            del self.accessControlList_



    """
    Para obtener el nombre que identifica la lista de control de acceso actualmente establecida.

    @return Nombre la lista de control de acceso actual.
    """
    def name(self):
        return self.name_


    """
    Lee el fichero "acl.xml" y establece una nueva lista de control de acceso.

    Si el fichero "acl.xml" no se puede leer, la lista de control de acceso queda vacía y
    no se procesará ningún control de acceso sobre ningún objeto.
    
    @param  aclXml  Contenido XML con la definición de la lista de control de acceso.
    """
    def init_(self, aclXml = False):
      
        util = FLUtil()
        if aclXml == False:
            self.init_(self._prj.conn.managerModules().content("acl.xml"))
            return
      
        doc = QDomDocument("ACL")
        if self.accessControlList_:
            self.accessControlList_.clear()
            del self.accessControlList_
            self.accessControlList_ = {}
        
        if not util.domDocumentSetContent(doc, aclXml):
            print("FLAccessControlList : " + util.tr("Lista de control de acceso vacia o errónea"))
            return
        
        self.accessControlList_ = {}
        self.accessControlList_.setAutoDelete(True)
        
        docElem = doc.documentElement()
        no = docElem.firstChild()
        
        while no:
            e = no.toElement()
            if e:
                if e.tagName() == "name":
                    self.name_ = e.text()
                    no = no.nextSibling()
                    continue
            

                ac =  FLAccessControlFactory.create(e.tagName())
                if ac:
                    ac.set(e)
                    self.accessControlList_.replace("%s::%s::%s" % (ac.type(), ac.name(), ac.user()), ac)
                    no = no.nextSibling()
                    continue
            
            no = no.nextSibling()
            

    """
    Procesa un objeto de alto nivel según la lista de control de acceso establecida.

    @param obj Objeto de alto nivel al que aplicar el control de acceso. Debe ser o heredar de la clase QObject.
    """
    def process(self, obj):
        if not obj or not self.accessControlList_:
            return
        
        if not self.accessControlList_:
            return
        
        type = FLAccessControlFactory.type(obj)
        name = obj.name()
        user = self.database().user()
        
        if not type or not name or not user:
            return
        
        ac = self.accessControlList_["%s::%s::%s" % (type, name, user)]
        
        if ac:
            ac.processObject(obj)
    
    """
    Crea un nuevo fichero "acl.xml" y lo almacena sustituyendo el anterior, en el caso de que exista.

    @param idacl Identificador del registro de la tabla "flacls" a utilizar para crear "acl.xml".
    """
    def installACL(self, idacl):
        
        util = FLUtil()
        
        doc = QDomDocument("ACL")
        
        root = doc.createElement("ACL")
        doc.appendChild(root)
        
        name = doc.createElement("name")
        root.appendChild(name)
        n = doc.createTextNode(idacl)
        name.appendChild(n)
        
        q = FLSqlQuery()
        
        q.setTablesList("flacs")
        q.setSelect("idac,tipo,nombre,iduser,idgroup,degroup,permiso")
        q.setFrom("flacs")
        q.setWhere("idacl='%s'" % idacl)
        q.setOrderBy("prioridad DESC, tipo")
        q.setForwarOnly(True)
        
        if q.exec_():
            step = 0
            progress = util.ProgressDialog(util.tr("Instalando control de acceso..."), None, q.size(), None, None, True)
            progress.setCaption(util.tr("Instalando ACL"))
            progress.setMinimumDuration(0)
            progress.setProgress(++step)
            while q.next():
                self.makeRule(q, doc)
                progress.setProgress(++step)
            
            self.database().managerModules().setContent("acl.xml", "sys", doc.toString())
    
    

    #private:

    """
    Crea el/los nodo(s) DOM correspondiente(s) a un registro de la tabla "flacs".

    Utiliza FLAccessControlLists::makeRuleUser o FLAccessControlLists::makeRuleGroup dependiendo si el registro
    al que apunta la consulta indica que la regla es para un usuario o un grupo. Si el registro indica a un
    usuario se creará una regla de usuario, si indica a un grupo se creará una regla de usuario por cada uno de
    los usuarios miembros del grupo.

    @param q Consulta sobre la tabla "flacs" posicionada en el registro a utilizar para construir la(s) regla(s).
    @param d Documento DOM/XML en el que insertará(n) el/los nodo(s) que describe(n) la(s) regla(s) de control de acceso.
    """
    @decorators.BetaImplementation
    def makeRule(self, q, d):
        if not q or not d:
            return
        
        if q.value(5) in ("True",True,"true"):
            self.makeRuleGroup(q, d, str(q.value(4)))
        else:
            self.makeRuleUser(q, d, str(q.value(3))) 
        
    """
    Crea un nodo DOM correspondiente a un registro de la tabla "flacs" y para un usuario determinado.

    @param q Consulta sobre la tabla "flacs" posicionada en el registro a utilizar para construir la regla.
    @param d Documento DOM/XML en el que insertará el nodo que describe la regla de control de acceso.
    @param iduser Identificador del usuario utilizado en la regla de control de acceso.
    """
    def makeRuleUser(self, q, d, iduser):
        if not iduser or not q or not d:
            return 
        
        ac = FLAccesccControlFactory.create(str(q.value(1)))
        
        if ac:
            ac.setName(str(q.value(2)))
            ac.setUser(iduser)
            ac.setPerm(str(q.value(6)))
            
            qAcos = FLSqlQuery()
            qAcos.setTablesList("flacos")
            qAcos.setSelect("nombre,permiso")
            qAcos.setFrom("flacos")
            qAcos.setWhere("idac ='%s'" % q.value(0))
            qAcos.setForwardOnly()
            
            acos = None
            
            if qAcos.exec_():
                while qAcos.next():
                    acos << str(qAcos.value(0))
                    acos << str(qAcos.value(1))
            
            ac.setAcos(acos)
            ac.get(d)
            
            del ac

    """
    Crea varios nodos DOM correspondientes a un registro de la tabla "flacs" y para un grupo de usuarios determinado.

    La función de este método es crear una regla para cada uno de los usuarios miembros del grupo, utilizando
    FLAccessControlLists::makeRuleUser.

    @param q Consulta sobre la tabla "flacs" posicionada en el registro a utilizar para construir las reglas.
    @param d Documento DOM/XML en el que insertarán los nodos que describe las reglas de control de acceso.
    @param idgroup Identificador del grupo de usuarios.
    """
    def makeRuleGroup(self, q, d, idgroup):
        if not idgroup or not q or not d:
            return
        
        qU = FLSqlQuery()
        
        qU.setTablesList("flusers")
        qU.setSelect("iduser")
        qU.setFrom("flusers")
        qU.setWhere("'idgroup='%s'" % idgroup)
        qU.setForwardOnly(True)
        
        if qU.exec_():
            while qU.next():
                self.makeRuleUser(q, d, str(qU.value(0)))

