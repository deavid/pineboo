# -*- coding: utf-8 -*-

from PyQt5 import Qt
from pineboolib import decorators
import logging
logger = logging.getLogger("FLListViewItem")

class FLListViewItem(Qt.QStandardItem):
    
    _expandable = None
    _key = None
    _open = None
    _parent_model = None
    
    def __init__(self, parent = None):
        super().__init__()
        self._key = ""
        self._open = False
        if parent:
            self._parent_model = parent.model()
            if parent.model().item(0,0) is not None:
                parent.model().item(0,0).setChild(0,0, self)
            else:
                parent.model().setItem(0,0,self)
            
    

    def setText(self, *args):
        #logger.warning("Seteo texto %s" , args, stack_info = True )
        pos = 0
        if len(args) == 1:
            value = args[0]
        else:
            pos = args[0]
            value = str(args[1])
        
        if pos == 0:
            super().setText(value)
        else:
            item = self._parent_model.item(0,0).child(0,pos)
            if item is None:
                item = Qt.QStandardItem()
                self._parent_model.item(0,0).setChild(0, pos, item)
            
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
    
 