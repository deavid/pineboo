# -*- coding: utf-8 -*-

from pineboolib.fllegacy.FLFormDB_old import FLFormDB
from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
from pineboolib import decorators
from pineboolib.utils import DefFun
from pineboolib import project
from PyQt4 import QtCore, QtGui, Qt
from pineboolib.utils import filedir
import pineboolib.emptyscript
import os.path, traceback
from pineboolib import qt3ui
import imp


class FLFormSearchDB( FLFormDB ):
    _accepted = None
    _cursor = None

    formReady = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        parent = None
        name = None

        if isinstance(args[0], str):
            name = args[0]
            self._cursor= FLSqlCursor(name)
            action = self._cursor.action()
            self._accepted = False

        elif isinstance(args[0], FLSqlCursor):
            self.cursor_ = args[0]
            action = args[1]
            parent = args[2]

        super(FLFormSearchDB,self).__init__(parent ,action)


    def __delattr__(self, *args, **kwargs):
        if self.cursor_:
            self.cursor_.restoreEditionFlag(self)
            self.cursor_.restoreBrowseFlag(self)

        FLFormDB.__delattr__(self, *args, **kwargs)

    def __getattr__(self, name): return DefFun(self, name)

    def setFilter(self, f):

        if not self.cursor_:
            return
        previousF = self.cursor_.mainFilter()
        newF = None
        if not previousF:
            newF = f
        elif previousF.contains(f):
            return
        else:
            newF = "%s AND %s" % (previousF, f)
        self.cursor_.setMainFilter(newF)


    def setCursor(self, cursor):
        print("Definiendo cursor")
        self._cursor = cursor

    @decorators.Incomplete
    def setMainWidget(self, w = None):
        if not self._cursor or not w:
            print("Creamos la ventana (ignorado)")
            return
        print("Creamos la ventana")

        if self.showed:
            if self.mainWidget_ and not self.mainWidget_ == w:
                self.initMainWidget(w)
        else:
            w.hide()

        if self.layoutButtons:
            del self.layoutButtons

        if self.layout:
            del self.layout


        w.setFont(QtGui.qApp.font())
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(w)
        self.layoutButtons = QtGui.QHBoxLayout()

        #pbSize = Qt.QSize(22,22)

        wt = QtGui.QToolButton.whatsThis()
        wt.setIcon(QtGui.QIcon(filedir("icons","gtk-find.png")))
        self.layoutButtons.addWidget(wt)
        wt.show()

        self.mainWidget_ = w

        self._cursor.setEdition(False)
        self._cursor.setBrowse(False)
        self._cursor.recordChoosed.emit(self.acepted)

    iface = None
    def load(self):
        if self.loaded: return
        print("Loading form %s . . . " % self.action.form)
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
            except Exception as e:
                print("ERROR al inicializar script de la accion %r:" % self.action.name, e)
                print(traceback.format_exc(),"---")

    def load_script(self,scriptname):
        python_script_path = None
        self.script = pineboolib.emptyscript # primero default, luego sobreescribimos
        if scriptname:
            print("Loading script %s . . . " % scriptname)
            # Intentar convertirlo a Python primero con flscriptparser2
            script_path = self.prj.path(scriptname+".qs")
            if not os.path.isfile(script_path): raise IOError
            python_script_path = (script_path+".xml.py").replace(".qs.xml.py",".py")
            if not os.path.isfile(python_script_path) or pineboolib.no_python_cache:
                print("Convirtiendo a Python . . .")
                #ret = subprocess.call(["flscriptparser2", "--full",script_path])
                from pineboolib.flparser import postparse
                postparse.pythonify(script_path)

            if not os.path.isfile(python_script_path):
                raise AssertionError(u"No se encontró el módulo de Python, falló flscriptparser?")
            try:
                self.script = imp.load_source(scriptname,python_script_path)
                #self.script = imp.load_source(scriptname,filedir(scriptname+".py"), open(python_script_path,"U"))
            except Exception as e:
                print("ERROR al cargar script QS para la accion %r:" % self.action.name, e)
                print(traceback.format_exc(),"---")

        self.script.form = self.script.FormInternalObj(action = self.action, project = self.prj, parent = self)
        self.widget = self.script.form
        self.iface = self.widget.iface





    def exec_(self, valor):
        print("  <<<< EXEC BEGIN ")
        print("Ejecutamos la ventana y esperamos respuesta, introducimos desde y hasta en cursor")
        self._cursor.setFilter("1=1")
        self.load()
        self.show()
        # Hay que intentar retener la ejecución aquí, hasta confirmación.
        # ... para eso es interesante QDialog, pero hay que ver si se puede integrar.
        for i in range(100):
            QtCore.QCoreApplication.processEvents() # No funciona, pero se ve la idea.

        print("  >>>> EXEC END")


    def accepted(self):
        return self._accepted
