# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from pineboolib.utils import filedir

class FLFormDB(QtGui.QWidget):
    known_instances = {}
    _cursor = None
    
    def __init__(self, parent, action, load=False):
        try:
            assert (self.__class__,action) not in self.known_instances
        except AssertionError:
            print("WARN: Clase %r ya estaba instanciada, reescribiendo!. " % ((self.__class__,action),)
                + "Puede que se estén perdiendo datos!" )
        self.known_instances[(self.__class__,action)] = self
        QtGui.QWidget.__init__(self, parent)
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
    
    def cursor(self):
        return self._cursor
    