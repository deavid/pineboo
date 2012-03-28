# encoding: UTF-8
import sys
from lxml import etree
from optparse import OptionParser
import psycopg2
import os.path, os
from PyQt4 import QtGui, QtCore, uic
from pineboolib import qt3ui
import re
Qt = QtCore.Qt

def filedir(*path): return os.path.realpath(os.path.join(os.path.dirname(__file__), *path))

class DlgConnect(QtGui.QWidget):
    def load(self):
        self.ui = uic.loadUi(filedir('forms/dlg_connect.ui'), self)

class WMainForm(QtGui.QMainWindow):
    def load(self,path):
        self.ui = qt3ui.loadUi(path, self)

def one(x, default = None):
    try:
        return x[0]
    except IndexError:
        return default
        
class Struct(object):
    "Dummy"

class XMLStruct(Struct):
    def __init__(self, xmlobj):
        self._attrs = []
        if xmlobj is not None:
            self.__name__ = xmlobj.tag
            for child in xmlobj:
                if child.tag == "property":
                    key, text = qt3ui.loadProperty(child)
                else:
                    text = child.text
                    if text.find("QT_TRANSLATE") != -1:
                        match = re.search(r"""QT_TRANSLATE\w*\(.+,["'](.+)["']\)""", text)
                        if match: text = match.group(1)
                    key = child.tag
                if text: text = text.strip()
                setattr(self, key, text)
                self._attrs.append(key)
                # print self.__name__, key, text
    def __str__(self):
        attrs = [ "%s=%s" % (k,repr(getattr(self,k))) for k in self._attrs ] 
        txtattrs = " ".join(attrs)
        return "<%s.%s %s>" % (self.__class__.__name__, self.__name__, txtattrs)
        
    
class Project(object):
    def load(self, filename):
        self.parser = etree.XMLParser(
                        ns_clean=True,
                        encoding="UTF-8",
                        remove_blank_text=True,
                        )
        self.tree = etree.parse(filename, self.parser)
        self.root = self.tree.getroot()
        self.dbserver = XMLStruct(one(self.root.xpath("database-server")))
        self.dbauth = XMLStruct(one(self.root.xpath("database-credentials")))
        self.dbname = one(self.root.xpath("database-name/text()"))
        self.apppath = one(self.root.xpath("application-path/text()"))
        self.tmpdir = filedir("../tempdata")
    def dir(self, *x):
        return os.path.join(self.tmpdir,*x)    
        
    def run(self):
        # Preparar temporal
        if not os.path.exists(self.dir("cache")):
            os.makedirs(self.dir("cache"))
        # Conectar:
        conninfostr = "dbname=%s host=%s port=%s user=%s password=%s connect_timeout=5" % (
                        self.dbname, self.dbserver.host, self.dbserver.port, 
                        self.dbauth.username, self.dbauth.password
                    )
        self.conn = psycopg2.connect(conninfostr)
        self.cur = self.conn.cursor()
        # Obtener modulos activos
        self.cur.execute(""" SELECT idarea, idmodulo, descripcion, icono FROM flmodules WHERE bloqueo = TRUE """)
        self.modules = {}
        for idarea, idmodulo, descripcion, icono in self.cur:
            self.modules[idmodulo] = Module(self, idarea, idmodulo, descripcion, icono)
            
        # Descargar proyecto . . . 
        self.cur.execute(""" SELECT idmodulo, nombre, sha::varchar(16) FROM flfiles ORDER BY idmodulo, nombre """)
        f1 = open(self.dir("project.txt"),"w")
        self.files = {}
        for idmodulo, nombre, sha in self.cur:
            if idmodulo not in self.modules: continue # I
            fileobj = File(self, idmodulo, nombre, sha)
            if nombre in self.files: print "WARN: file %s already loaded, overwritting..." % filename
            self.files[nombre] = fileobj
            self.modules[idmodulo].add_project_file(fileobj)
            f1.write(fileobj.filekey+"\n")
            if os.path.exists(self.dir("cache",fileobj.filekey)): continue
            cur2 = self.conn.cursor()
            cur2.execute(""" SELECT contenido FROM flfiles WHERE idmodulo = %s AND nombre = %s AND sha::varchar(16) = %s""", [idmodulo, nombre, sha] )
            for (contenido,) in cur2:
                f2 = open(self.dir("cache",fileobj.filekey),"w")
                # La cadena decode->encode corrige el bug de guardado de AbanQ/Eneboo
                f2.write(contenido.decode("UTF-8").encode("ISO-8859-15"))

  
class Module(object):                
    def __init__(self, project, areaid, name, description, icon):
        self.prj = project
        self.areaid = areaid
        self.name = name
        self.description = description.decode("UTF-8")
        self.icon = icon
        self.files = {}
        self.loaded = False
        
    def add_project_file(self, fileobj):
        self.files[fileobj.filename] = fileobj
        
    def load(self):
        print "Loading module %s . . . " % self.name
        self.actions = ModuleActions(self, self.path("%s.xml" % self.name))
        self.actions.load()
        
        self.mainform = MainForm(self, self.path("%s.ui" % self.name))
        self.mainform.load()
        
        self.loaded = True
        
    def path(self, filename):
        if filename not in self.files: return None
        return self.files[filename].path()
        
    def run(self):
        if self.loaded == False: self.load()
        print "Running module %s . . . " % self.name
        self.widget = QtGui.QWidget()
        w = self.widget
        w.layout = QtGui.QVBoxLayout()
        label = QtGui.QLabel(u"Módulo %s\nEscoja una acción:" % self.description)
        w.layout.addWidget(label)
        for key, action in self.mainform.actions.items():
            button = QtGui.QCommandLinkButton(action.text)
            button.clicked.connect(action.run)
            w.layout.addWidget(button)
        w.setLayout(w.layout)
        w.show()
            
        
class File(object):
    def __init__(self, project, module, filename, sha):
        self.prj = project
        self.module = module
        self.filename = filename
        self.sha = sha
        self.filekey = "%s.%s.%s" % (module, filename, sha)
        
    def path(self):
        return self.prj.dir("cache",self.filekey)
        
class ModuleActions(object):
    def __init__(self, module, path):
        self.mod = module
        self.prj = module.prj
        self.path = path
        
    def load(self):
        self.parser = etree.XMLParser(
                        ns_clean=True,
                        encoding="ISO-8859-15",
                        remove_blank_text=True,
                        )
        self.tree = etree.parse(self.path, self.parser)
        self.root = self.tree.getroot()
        self.tree = etree.parse(self.path, self.parser)
        self.root = self.tree.getroot()
        self.actions = {}
        for xmlaction in self.root:
            action =  XMLAction(xmlaction)
            action.mod = self
            action.prj = self.prj
            self.actions[action.name] = action
            #print action
    def __getitem__(self, k): return self.actions[k]
    def __setitem__(self, k, v): 
        raise NotImplementedError, "Actions are not writable!"
        self.actions[k] = v

        
class MainForm(object):
    def __init__(self, module, path):
        self.mod = module
        self.prj = module.prj
        self.path = path
        
    def load(self):
        self.parser = etree.XMLParser(
                        ns_clean=True,
                        encoding="UTF8",
                        remove_blank_text=True,
                        )
        self.tree = etree.parse(self.path, self.parser)
        self.root = self.tree.getroot()
        self.actions = {}
        for xmlaction in self.root.xpath("actions//action"):
            action =  XMLMainFormAction(xmlaction)
            action.mainform = self
            action.mod = self.mod
            action.prj = self.prj
            self.actions[action.name] = action
        #self.ui = WMainForm()
        #self.ui.load(self.path)
        #self.ui.show()

class XMLMainFormAction(XMLStruct):
    def run(self):
        # Se asume conectada a "OpenDefaultForm()".
        print "Running MainFormAction:", self.name, self.text
        action = self.mod.actions[self.name]
        action.openDefaultForm()
        
class XMLAction(XMLStruct):
    def openDefaultForm(self):
        print "Opening default form for Action", self.name
        print self
        
            
def main():
    
    parser = OptionParser()
    parser.add_option("-l", "--load", dest="project",
                      help="load projects/PROJECT.xml and run it", metavar="PROJECT")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")

    (options, args) = parser.parse_args()    
    app = QtGui.QApplication(sys.argv)
    if not options.project:
        w = DlgConnect()
        w.load()
        w.show()
        sys.exit(app.exec_())
    else:
        if not options.project.endswith(".xml"): 
            options.project += ".xml"
        prjpath = filedir("../projects", options.project)
        if not os.path.isfile(prjpath):
            raise ValueError("el proyecto %s no existe." % options.project)
            
        project = Project()
        project.load(prjpath)
        project.run()
        w = QtGui.QWidget()
        w.layout = QtGui.QVBoxLayout()
        label = QtGui.QLabel(u"Escoja un módulo:")
        w.layout.addWidget(label)
        for module in project.modules.values():
            button = QtGui.QCommandLinkButton(module.description,module.name)
            button.clicked.connect(module.run)
            w.layout.addWidget(button)
        
        w.setLayout(w.layout)
        w.show()
        sys.exit(app.exec_())
