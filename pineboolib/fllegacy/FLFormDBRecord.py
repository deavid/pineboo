# -*- coding: utf-8 -*-

import pineboolib
from pineboolib.fllegacy.FLFormDB_old import FLFormDB
from pineboolib import qt3ui
import traceback
import os
import imp
from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
from PyQt4 import QtGui
from pineboolib.utils import filedir

class FLFormDBRecord(FLFormDB):
    """ Controlador dedicado a las ventanas de edición de registro (emergentes) """
    iface = None
    
    
    def __init__(self, parent_or_cursor, action, load=False):
        if not isinstance(parent_or_cursor, FLSqlCursor):
            parent = parent_or_cursor
        else:
            parent = None
        super(FLFormDBRecord,self).__init__(parent, action, load)
        
        if isinstance(parent_or_cursor, FLSqlCursor):
            self._cursor = parent_or_cursor
            
        self.toolButtonAccept = QtGui.QToolButton()
        self.toolButtonAccept.setIcon(QtGui.QIcon(filedir("icons","gtk-add.png")))
        self.toolButtonAccept.clicked.connect(self.validateForm)
        self.bottomToolbar.layout.addWidget(self.toolButtonAccept) 
    
    def validateForm(self):
        if self.iface:
            try:
                if self.iface.validateForm():
                    self.close()
                else:
                    print("ValidateForm no es válido") 
            except Exception as e:
                print("ERROR en validateForm de la accion %r:" % self.action.name, e)
                print(traceback.format_exc(),"---")
    
    def loaded(self):
        return self.loaded

    
    def load(self):
        if self.loaded: return
        print("Loading (record) form %s . . . " % self.action.formrecord)
        self.script = None
        self.iface = None
        try: script = self.action.scriptformrecord or None
        except AttributeError: script = None
        self.load_script(script)
        self.resize(550,350)
        self.layout.insertWidget(0,self.widget)
        if self.action.form:
            form_path = self.prj.path(self.action.formrecord+".ui")
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
            try:
                if not os.path.isfile(python_script_path) or pineboolib.no_python_cache:
                    print("Convirtiendo a Python . . .")
                    #ret = subprocess.call(["flscriptparser2", "--full",script_path])
                    from pineboolib.flparser import postparse
                    postparse.pythonify(script_path)

                if not os.path.isfile(python_script_path):
                    raise AssertionError(u"No se encontró el módulo de Python, falló flscriptparser?")
                self.script = imp.load_source(scriptname,python_script_path)
                #self.script = imp.load_source(scriptname,filedir(scriptname+".py"), open(python_script_path,"U"))
            except Exception as e:
                print("ERROR al cargar script QS para la accion %r:" % self.action.name, e)
                print(traceback.format_exc(),"---")

        self.script.form = self.script.FormInternalObj(action = self.action, project = self.prj, parent = self)
        self.widget = self.script.form
        self.iface = self.widget.iface

