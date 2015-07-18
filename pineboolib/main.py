# encoding: UTF-8
import sys, imp
from optparse import OptionParser
import os.path, os
import re,subprocess
import traceback

try:
    from lxml import etree
except ImportError:
    print traceback.format_exc()
    print "HINT: Instale el paquete python-lxml e intente de nuevo"

try:
    import psycopg2
except ImportError:
    print traceback.format_exc()
    print "HINT: Instale el paquete python-psycopg2 e intente de nuevo"

try:
    from PyQt4 import QtGui, QtCore, uic
except ImportError:
    print traceback.format_exc()
    print "HINT: Instale el paquete python-pyqt4 e intente de nuevo"

import pineboolib
from pineboolib import qt3ui
from pineboolib.dbschema.schemaupdater import parseTable
from pineboolib.qsaglobals import aqtt
import pineboolib.emptyscript

from pineboolib import qsatype, qsaglobals, DlgConnect

Qt = QtCore.Qt

# TODO: Mover a un fichero de utilidades
def filedir(*path): return os.path.realpath(os.path.join(os.path.dirname(__file__), *path))

class WMainForm(QtGui.QMainWindow):
    def load(self,path):
        # self.ui = loadUi?? <-- borrame
        qt3ui.loadUi(path, self)

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
                    text = aqtt(child.text)
                    key = child.tag
                if isinstance(text, basestring): text = text.strip()
                setattr(self, key, text)
                self._attrs.append(key)
                # print self.__name__, key, text
    def __str__(self):
        attrs = [ "%s=%s" % (k,repr(getattr(self,k))) for k in self._attrs ]
        txtattrs = " ".join(attrs)
        return "<%s.%s %s>" % (self.__class__.__name__, self.__name__, txtattrs)

    def _v(self, k, default=None):
        return getattr(self, k, default)

class DBServer(XMLStruct):
    host = "127.0.0.1"
    port = "5432"

class DBAuth(XMLStruct):
    username = "postgres"
    password = "passwd"



class Project(object):
    def load(self, filename):
        self.parser = etree.XMLParser(
                        ns_clean=True,
                        encoding="UTF-8",
                        remove_blank_text=True,
                        )
        self.tree = etree.parse(filename, self.parser)
        self.root = self.tree.getroot()
        self.dbserver = DBServer(one(self.root.xpath("database-server")))
        self.dbauth = DBAuth(one(self.root.xpath("database-credentials")))
        self.dbname = one(self.root.xpath("database-name/text()"))
        self.apppath = one(self.root.xpath("application-path/text()"))
        self.tmpdir = filedir("../tempdata")

        self.actions = {}
        self.tables = {}
        pineboolib.project = self

    def path(self, filename):
        if filename not in self.files:
            print "WARN: Fichero %r no encontrado en el proyecto." % filename
            return None
        return self.files[filename].path()

    def dir(self, *x):
        return os.path.join(self.tmpdir,*x)

    def run(self):
        # TODO: Refactorizar esta función en otras más sencillas
        # Preparar temporal
        if not os.path.exists(self.dir("cache")):
            os.makedirs(self.dir("cache"))
        # Conectar:
        conninfostr = "dbname=%s host=%s port=%s user=%s password=%s connect_timeout=5" % (
                        self.dbname, self.dbserver.host, self.dbserver.port,
                        self.dbauth.username, self.dbauth.password
                    )
        self.conn = psycopg2.connect(conninfostr)
        try:
            self.conn.set_client_encoding("UTF8")
        except Exception:
            print traceback.format_exc()

        self.cur = self.conn.cursor()
        # Obtener modulos activos
        self.cur.execute(""" SELECT idarea, idmodulo, descripcion, icono FROM flmodules WHERE bloqueo = TRUE """)
        self.modules = {}
        for idarea, idmodulo, descripcion, icono in self.cur:
            self.modules[idmodulo] = Module(self, idarea, idmodulo, descripcion, icono)
        self.modules["sys"] = Module(self,"sys","sys","Administración",None)#Añadimos módulo sistema(falta icono)

        # Descargar proyecto . . .
        self.cur.execute(""" SELECT idmodulo, nombre, sha::varchar(16) FROM flfiles ORDER BY idmodulo, nombre """)
        f1 = open(self.dir("project.txt"),"w")
        self.files = {}
        if not os.path.exists(self.dir("cache")): raise AssertionError
        for idmodulo, nombre, sha in self.cur:
            if idmodulo not in self.modules: continue # I
            fileobj = File(self, idmodulo, nombre, sha)
            if nombre in self.files: print "WARN: file %s already loaded, overwritting..." % nombre
            self.files[nombre] = fileobj
            self.modules[idmodulo].add_project_file(fileobj)
            f1.write(fileobj.filekey+"\n")
            if os.path.exists(self.dir("cache",fileobj.filekey)): continue
            fileobjdir = os.path.dirname(self.dir("cache",fileobj.filekey))
            if not os.path.exists(fileobjdir):
                os.makedirs(fileobjdir)
            cur2 = self.conn.cursor()
            cur2.execute(""" SELECT contenido FROM flfiles WHERE idmodulo = %s AND nombre = %s AND sha::varchar(16) = %s""", [idmodulo, nombre, sha] )
            for (contenido,) in cur2:
                f2 = open(self.dir("cache",fileobj.filekey),"w")
                # La cadena decode->encode corrige el bug de guardado de AbanQ/Eneboo
                txt = ""
                try:
                    txt = contenido.decode("UTF-8").encode("ISO-8859-15")
                except Exception, e:
                    print "Error al decodificar" ,idmodulo, nombre
                    txt = contenido.decode("UTF-8","replace").encode("ISO-8859-15","replace")

                f2.write(txt)

        # Cargar el núcleo común del proyecto
        idmodulo = 'sys'
        for root, dirs, files in os.walk(filedir("..","share","eneboo")):
            for nombre in files:
                fileobj = File(self, idmodulo, nombre, basedir = root)
                self.files[nombre] = fileobj


class Module(object):
    def __init__(self, project, areaid, name, description, icon):
        self.prj = project
        self.areaid = areaid
        self.name = name
        self.description = description.decode("UTF-8")
        self.icon = icon
        self.files = {}
        self.tables = {}
        self.loaded = False
        self.path = self.prj.path

    def add_project_file(self, fileobj):
        self.files[fileobj.filename] = fileobj

    def load(self):
        #print "Loading module %s . . . " % self.name
        pathxml = self.path("%s.xml" % self.name)
        pathui = self.path("%s.ui" % self.name)
        if pathxml is None:
            print "ERROR: modulo %r: fichero XML no existe" % (self.name)
            return False
        if pathui is None:
            print "ERROR: modulo %r: fichero UI no existe" % (self.name)
            return False

        try:
            self.actions = ModuleActions(self, pathxml)
            self.actions.load()
            self.mainform = MainForm(self, pathui)
            self.mainform.load()
        except Exception,e:
            print "ERROR al cargar modulo %r:" % self.name, e
            print traceback.format_exc(),"---"
            return False

        # TODO: Load Main Script:
        self.mainscript = None
        # /-----------------------

        for tablefile in self.files:
            if not tablefile.endswith(".mtd"): continue
            name, ext = os.path.splitext(tablefile)
            contenido = unicode(open(self.path(tablefile)).read(),"ISO-8859-15")
            tableObj = parseTable(name, contenido)
            if tableObj is None:
                print "No se pudo procesar. Se ignora tabla %s/%s " % (self.name , name)
                continue
            self.tables[name] = tableObj
            self.prj.tables[name] = tableObj

        self.loaded = True
        return True

    def run(self,vBLayout):
        if self.loaded == False: self.load()
        if self.loaded == False:
            print "WARN: Ignorando modulo %r por fallo al cargar" % (self.name)
            return False
        #print "Running module %s . . . " % self.name
        vBLayout.setSpacing(0)
        vBLayout.setContentsMargins(1,5,5,0)
        for key in self.mainform.toolbar:
            action = self.mainform.actions[key]

            button = QtGui.QCommandLinkButton(action.text)
            button.clicked.connect(action.run)
            vBLayout.addWidget(button)
        #w.setLayout(w.layout)
        #w.show()


class File(object):
    def __init__(self, project, module, filename, sha = None, basedir = None):
        self.prj = project
        self.module = module
        self.filename = filename
        self.sha = sha
        self.name, self.ext = os.path.splitext(filename)
        if self.sha:
            self.filekey = "%s/file%s/%s/%s%s" % (module, self.ext, self.name, sha,self.ext)
        else:
            self.filekey = filename
        self.basedir = basedir

    def path(self):
        if self.basedir:
            # Probablemente porque es local . . .
            return self.prj.dir(self.basedir,self.filename)
        else:
            # Probablemente es remoto (DB) y es una caché . . .
            return self.prj.dir("cache",*(self.filekey.split("/")))

class DelayedObjectProxyLoader(object):
    def __init__(self, obj, *args, **kwargs):
        self._obj = obj
        self._args = args
        self._kwargs = kwargs
        self.loaded_obj = None

    def __load(self):
        if not self.loaded_obj:
            self.loaded_obj = self._obj(*self._args,**self._kwargs)
        return self.loaded_obj

    def __getattr__(self, name): # Solo se lanza si no existe la propiedad.
        obj = self.__load()
        return getattr(obj,name)

class ModuleActions(object):
    def __init__(self, module, path):
        self.mod = module
        self.prj = module.prj
        self.path = path
        assert(path)
    def load(self):
        self.parser = etree.XMLParser(
                        ns_clean=True,
                        encoding="ISO-8859-15",
                        remove_blank_text=True,
                        )

        self.tree = etree.parse(self.path, self.parser)
        self.root = self.tree.getroot()
        action = XMLAction(None)
        action.mod = self
        action.prj = self.prj
        action.name = self.mod.name
        action.alias = self.mod.name
        #action.form = self.mod.name
        action.form = None
        action.table = None
        action.scriptform = self.mod.name
        self.prj.actions[action.name] = action
        if hasattr(qsaglobals,action.name):
            print "INFO: No se sobreescribie variable de entorno", action.name
        else:
            setattr(qsaglobals,action.name, DelayedObjectProxyLoader(action.load))
        for xmlaction in self.root:
            action =  XMLAction(xmlaction)
            action.mod = self
            action.prj = self.prj
            try: name = action.name
            except AttributeError: name = "unnamed"
            self.prj.actions[name] = action
            #print action

    def __contains__(self, k): return k in self.prj.actions
    def __getitem__(self, k): return self.prj.actions[k]
    def __setitem__(self, k, v):
        raise NotImplementedError("Actions are not writable!")
        self.prj.actions[k] = v


class MainForm(object):
    def __init__(self, module, path):
        self.mod = module
        self.prj = module.prj
        self.path = path
        assert(path)

    def load(self):
        try:
            self.parser = etree.XMLParser(
                            ns_clean=True,
                            encoding="UTF8",
                            remove_blank_text=True,
                            )
            self.tree = etree.parse(self.path, self.parser)
        except etree.XMLSyntaxError:
            print "Error cargando modulo", self.path
            self.parser = etree.XMLParser(
                            ns_clean=True,
                            encoding="ISO-8859-15",
                            recover = True,
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

        self.toolbar = []
        for toolbar_action in self.root.xpath("toolbars//action"):
            self.toolbar.append( toolbar_action.get("name") )
        #self.ui = WMainForm()
        #self.ui.load(self.path)
        #self.ui.show()

class XMLMainFormAction(XMLStruct):
    name = "unnamed"
    text = ""
    def run(self):
        # Se asume conectada a "OpenDefaultForm()".
        print "Running MainFormAction:", self.name, self.text
        action = self.mod.actions[self.name]
        action.openDefaultForm()

class XMLAction(XMLStruct):
    def __init__(self, *args, **kwargs):
        super(XMLAction,self).__init__(*args, **kwargs)
        self.form = self._v("form")
        self.script = self._v("script")
        self.mainform = self._v("mainform")
        self.mainscript = self._v("mainscript")
        self.mainform_widget = None
        self._loaded = False

    def load(self):
        if self._loaded: return self.mainform_widget
        print "Loading action %s . . . " % (self.name)
        self.mainform_widget = FLMainForm(self, load = True)
        self._loaded = True
        print "End of action load %s (iface:%s ; widget:%s)" % (self.name, repr(self.mainform_widget.iface),repr(self.mainform_widget.widget))
        return self.mainform_widget

    def openDefaultForm(self):
        print "Opening default form for Action", self.name
        self.load()
        from pineboolib import mainForm # Es necesario importarlo a esta altura, QApplication tiene que ser construido antes que cualquier widget
        w = mainForm.mainWindow
        self.mainform_widget.init()
        w.addFormTab(self.mainform_widget)
        #self.mainform_widget.show()

class FLForm(QtGui.QWidget):
    known_instances = {}
    def __init__(self, action, load=False):
        try:
            assert((self.__class__,action) not in self.known_instances)
        except AssertionError:
            print "WARN: Clase %r ya estaba instanciada, reescribiendo!. Puede que se estén perdiendo datos!" % ((self.__class__,action),)
        self.known_instances[(self.__class__,action)] = self
        QtGui.QWidget.__init__(self)
        self.action = action
        self.prj = action.prj
        self.mod = action.mod
        self.layout = QtGui.QVBoxLayout()
        self.layout.setMargin(2)
        self.layout.setSpacing(2)
        self.setLayout(self.layout)
        # self.widget = QtGui.QWidget()
        # self.layout.addWidget(self.widget)
        self.bottomToolbar = QtGui.QFrame()
        self.bottomToolbar.setMaximumHeight(64)
        self.bottomToolbar.setMinimumHeight(16)
        self.bottomToolbar.layout = QtGui.QHBoxLayout()
        self.bottomToolbar.setLayout(self.bottomToolbar.layout)
        self.bottomToolbar.layout.setMargin(0)
        self.bottomToolbar.layout.setSpacing(0)
        self.bottomToolbar.layout.addStretch()
        self.toolButtonClose = QtGui.QToolButton()
        self.toolButtonClose.setIcon(QtGui.QIcon(filedir("icons","gtk-cancel.png")))
        self.toolButtonClose.clicked.connect(self.close)
        self.bottomToolbar.layout.addWidget(self.toolButtonClose)
        self.layout.addWidget(self.bottomToolbar)
        self.setWindowTitle(action.alias)
        self.loaded = False
        if load: self.load()

    def load(self):
        if self.loaded: return

class FLMainForm(FLForm):
    iface = None
    def load(self):
        if self.loaded: return
        print "Loading form %s . . . " % self.action.form
        self.script = None
        self.iface = None
        try: script = self.action.scriptform or None
        except AttributeError: script = None
        self.load_script(script)
        self.resize(550,350)
        self.layout.insertWidget(0,self.widget)
        if self.action.form:
            form_path = self.prj.path(self.action.form+".ui")
            qt3ui.loadUi(form_path, self.widget)

        self.loaded = True

    def init(self):
        if self.iface:
            try:
                self.iface.init()
            except Exception,e:
                print "ERROR al inicializar script de la accion %r:" % self.action.name, e
                print traceback.format_exc(),"---"

    def load_script(self,scriptname):
        python_script_path = None
        self.script = pineboolib.emptyscript # primero default, luego sobreescribimos
        if scriptname:
            print "Loading script %s . . . " % scriptname
            # Intentar convertirlo a Python primero con flscriptparser2
            script_path = self.prj.path(scriptname+".qs")
            if not os.path.isfile(script_path): raise IOError
            python_script_path = (script_path+".xml.py").replace(".qs.xml.py",".py")
            if not os.path.isfile(python_script_path) or pineboolib.no_python_cache:
                print "Convirtiendo a Python . . ."
                ret = subprocess.call(["flscriptparser2", "--full",script_path])
            if not os.path.isfile(python_script_path):
                raise AssertionError(u"No se encontró el módulo de Python, falló flscriptparser?")
            try:
                self.script = imp.load_source(scriptname,python_script_path)
                #self.script = imp.load_source(scriptname,filedir(scriptname+".py"), open(python_script_path,"U"))
            except Exception,e:
                print "ERROR al cargar script QS para la accion %r:" % self.action.name, e
                print traceback.format_exc(),"---"


        self.script.form = self.script.FormInternalObj(action = self.action, project = self.prj)
        self.widget = self.script.form
        self.iface = self.widget.iface



def main():
    # TODO: Refactorizar función en otras más pequeñas
    parser = OptionParser()
    parser.add_option("-l", "--load", dest="project",
                      help="load projects/PROJECT.xml and run it", metavar="PROJECT")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")
    parser.add_option("-a", "--action", dest="action",
                      help="load action", metavar="ACTION")
    parser.add_option("--no-python-cache",
                      action="store_true",dest="no_python_cache", default=False,
                      help="Always translate QS to Python")

    (options, args) = parser.parse_args()
    app = QtGui.QApplication(sys.argv)

    pineboolib.no_python_cache = options.no_python_cache

    if not options.project:
        w = DlgConnect.DlgConnect()
        w.load()
        w.show()
        ret = app.exec_()
        if (w.close()):
            prjpath = w.ruta
        if not prjpath:
            sys.exit(ret)




    else:
        if not options.project.endswith(".xml"):
            options.project += ".xml"
        prjpath = filedir("../projects", options.project)
        if not os.path.isfile(prjpath):
            raise ValueError("el proyecto %s no existe." % options.project)

    from pineboolib import mainForm # Es necesario importarlo a esta altura, QApplication tiene que ser construido antes que cualquier widget

    project = Project()
    project.load(prjpath)
    project.run()

    if options.action:
        objaction = None
        for k,module in project.modules.items():
            try:
                if not module.load(): continue
            except Exception,e:
                print "ERROR:", e.__class__.__name__, str(e)
                continue
            if options.action in module.actions:
                objaction = module.actions[options.action]
        if objaction is None: raise ValueError("Action name %s not found" % options.action)
        objaction.openDefaultForm()
        sys.exit(app.exec_())
    else:
        w = mainForm.mainWindow
        w.load()
        for module in project.modules.values():
            w.addModuleInTab(module)
        w.show()
        ret = app.exec_()
        del w
        del project
        sys.exit(ret)
