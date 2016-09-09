# -*- coding: utf-8 -*-

import pineboolib
from pineboolib.fllegacy.FLFormDB import FLFormDB
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
            self.setCursor(parent_or_cursor)
            
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



