# -*- coding: utf-8 -*-



from pineboolib import decorators
from PyQt4.QtCore import QString
from pineboolib.flcontrols import ProjectClass

class FLTableMetaData(ProjectClass):
    
    fieldList_ = []
    
    def __init__(self, name):
        super(FLTableMetaData,self).__init__()
        self.name_ = str(name)
        self.fieldList_ = []
        table = self._prj.tables[self.name_]
        #if self._prj.tables[self.name_]:
        #    print("OLEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE",self.name_)
        #    print(self._prj.tables[self.name_])
            #if table.n == self.name_:
            #    print("LOCALIZADOOOOOOOO", self.name_)
        for field in table.fields:
            #if field.visible_grid:
            #self.sql_fields.append(field.name())
            #self.field_metaData.append(field)
                self.addField(field)
    
    def __del__(self):
        del self.fieldList_
    
    def name(self):
        return self.name_
    
    @decorators.NotImplementedWarn
    def relation(self, fN, fFN, fTN ):
        return None
        if fN.isEmpty():
            return None

        field = self.field(fN)
        
        if field:
            if field.d.relationM1_ and field.d.relationM1_.foreignField() == fFN.lower() and field.d.relationM1_.foreignField() == fTN.lower():
                return QString(field.d.relationM1_)
        
        relationList = field.d.relationList_
        if not relationList:
            return None
            
        if not relationList:
            return None
        
        for itR in relationList:
            if itR.foreignField() == fFN.lower() and itR.foreignTable() == fTN.lower():
                return QString(itR) 
        
        return None
    
    def addField(self, field):
        #print("FLTableMetaData.addField(%s.%s)" % (self.name_, field.name()))
        self.fieldList_.append(field)
        

    
    @decorators.NotImplementedWarn
    def inCache(self):
        return True
    
    def indexOf(self, name):
        i = 0
        for field in self.fieldList_:
            if field.name() == name:
                #print("FLTableMetaData.indexOf(%s) = %s" % (name, i))
                return i 
            i = i + 1
        
        print("FLTableMetaData.indexOf(%s) No encontrado" % (name))   
        return None
    
    def indexField(self, position):
        i = 0
        for field in self.fieldList_:
            if position == i:
                #print("FLTableMetaData.indexField(%s) = %s" % (position, field.name())) 
                return field 
            i = i + 1
        
        print("FLTableMetaData.indexField(%s) No encontrado" % position)    
        return None
    
        
    def pK(self):
        for field in self.fieldList_:
            if field.isPrimaryKey():
                print("FLTableMetaData(%s).pk(%s)" % (self.name_, field.name))
                return field
        
        print("FLTableMetaData(%s) tiene un tamaño de ... %s" % (self.name_,len(self.fieldList_)))
        return None
    
    def fieldList(self):
        #print("retornando fieldList(%s)" % len(self.fieldList_))
        return self.fieldList_
    
    def field(self, name):
        for field in self.fieldList_:
            if field.name() == str(name).lower():
                #print("FLTableMetaData(%s): Retornando field %s" % (self.name_, name))
                return field
        return None
    
    @decorators.NotImplementedWarn
    def isQuery(self):
        return False
        
    
    