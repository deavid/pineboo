# -*- coding: utf-8 -*-

from PyQt5 import Qt
from pineboolib import decorators
import pineboolib
import logging
logger = logging.getLogger("FLListViewItem")

class FLListViewItem(Qt.QStandardItem):
    
    _expandable = None
    _key = None
    _open = None
    _root = None
    _index_child = None
    
    def __init__(self, parent = None):
        super().__init__()
        self._root = False
        self._parent = None
        self.setKey("")
        self.setEditable(False)
        self._index_child = 0
        
        #Comprueba que tipo de parent es
        if isinstance(parent, pineboolib.plugins.dgi.dgi_qt.dgi_objects.qlistview.QListView):
            #self._root = True
            parent.model().setItem(0,0, self)
        else:
            if isinstance(parent, pineboolib.plugins.dgi.dgi_qt.dgi_objects.fllistviewitem.FLListViewItem):
                #print("Añadiendo nueva linea a", parent.text(0))
                parent.appendRow(self)
        
        
        
        
        
        
        #if parent:
        #    self._parent = parent
        #    self._row = self._parent.model().rowCount()
        #    if self._parent.model().item(0,0) is not None:
        #        self._parent.model().item(0,0).setChild(self._row,0, self)
        #        self._parent.model().item(0,0)._rowcount += 1
        #    else:
        #        self._parent.model().setItem(self._row,0,self)
            
        #    self._rows = self._parent.model().item(0,0)._rowcount - 1
    
    def firstChild(self):
        self._index_child = 0
        item = self.child(self._index_child)           
        return item   
    
    def nextSibling(self):
        self._index_child += 1
        item = self.child(self._index_child)           
        return item
    
    def isExpandable(self):
        return True if self.child(0) is not None else False   
    

    def setText(self, *args):
        #print("Seteando", args, self.parent())
        #logger.warning("Seteo texto %s" , args, stack_info = True )
        col = 0
        if len(args) == 1:
            value = args[0]
        else:
            col = args[0]
            value = str(args[1])
        
        if col == 0:
            #if self._root:
                #print("Inicializando con %s a %s" % ( value, self.parent()))
            super().setText(value)
        else:
            item = self.parent().child(self.row(), col)
            if item is None:
                item = FLListViewItem()
                self.parent().setChild(self.row(), col, item)
            
            item.setText(value)
        
        
            


    def text(self, col):
        ret = ""
        if col == 0:
            ret = super().text()
        
        return str(ret)
    
    @decorators.NotImplementedWarn
    def setPixmap(self, *args):
        pass
    
    def setExpandable(self, b):
        self._expandable = b
    
    
    def setKey(self, k):
        self._key = str(k)
    
    def key(self):
        return self._key
    
    def setOpen(self, o):
        self._open = o
    
 