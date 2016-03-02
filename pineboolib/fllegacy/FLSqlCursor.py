# -*- coding: utf-8 -*-

from pineboolib.flcontrols import ProjectClass
from pineboolib import decorators

from PyQt4 import QtCore,QtGui

from pineboolib.CursorTableModel import CursorTableModel

class FLSqlCursor(ProjectClass):
    Insert = 0
    Edit = 1
    Del = 2
    Browse = 3
    _micounterTran = None

    _current_changed = QtCore.pyqtSignal(int, name='currentChanged')

    def __init__(self, actionname=None):
        super(FLSqlCursor,self).__init__()
        self._valid = False
        self._mode = self.Browse #Browse
        if actionname is None: raise AssertionError
        self.setAction(actionname)
        self._activatedCommitActions = True
        self._currentregister = -1 #current register
        self._activatedCheckIntegrity = True
        self._micounterTran = 0

    def __getattr__(self, name): return DefFun(self, name)

    def mainFilter(self):
        return self._model.where_filters.get("main-filter", "")

    def setMainFilter(self, newFilter):
        print("New main filter:", newFilter)
        self._model.where_filters["main-filter"] = newFilter

    def setAction(self, actionname):
        try:
            self._action = self._prj.actions[actionname]
        except KeyError:
            print("Accion no encontrada:", actionname)
            self._action = self._prj.actions["articulos"]

        if self._action.table:
            self._model = CursorTableModel(self._action, self._prj)
            self._selection = QtGui.QItemSelectionModel(self._model)
            self._selection.currentRowChanged.connect(self.selection_currentRowChanged)
            self._currentregister = self._selection.currentIndex().row()
        self._valid = True
        self._activatedCheckIntegrity = True
        self._activatedCommitActions = True

    def action(self):
        return self._action.name

    @decorators.NotImplementedWarn
    def setActivatedCheckIntegrity(self, state):
        self._activatedCheckIntegrity = bool(state)
        return True

    def setActivatedCommitActions(self, state):
        self._activatedCommitActions = bool(state)
        return True

    def selection_currentRowChanged(self, current, previous):
        if self._currentregister == current.row(): return False
        self._currentregister = current.row()
        self._current_changed.emit(self.at())
        print("cursor:%s , row:%d" %(self._action.table, self._currentregister ))

    def selection(self): return self._selection

    def select(self, where_filter = ""):
        print("Select filter:", where_filter)
        self._model.where_filters["select"] = where_filter
        self._model.refresh()
        return True

    def isValid(self):
        return self._valid

    def isNull(self,fieldname):
        return self.valueBuffer(fieldname) is None

    def isCopyNull(self,fieldname):
        return self.valueBufferCopy(fieldname) is None

    @decorators.NotImplementedWarn
    def setNull(self,fieldname):
        if not self.valueBufferCopy(fieldname) is None:
            self.setValueBuffer(fieldname, None)
        self.__bufferChanged(fieldname)

    def valueBuffer(self, fieldname):
        if self._currentregister < 0 or self._currentregister > self._model.rows: return None
        return self._model.value(_currentregister, fieldname)

    @decorators.NotImplementedWarn 
    def valueBufferCopy(self,fieldname):
        return self._model.value(self._currentregister, fieldname)

    @decorators.NotImplementedWarn
    def setValueBuffer(self, fieldname, newvalue):
        if not fieldname == self._model.pK():
            value = self._model.value(self._currentregister, fieldname)
            if self._model.fieldType(fieldname) == "bool":
                if value:
                    valor = True
                else:
                    valor = False
            #if self._model.relation(fieldname): #FIXME: RELATION
                #parent = f.related.parent_model._meta.model_name
                #model, a, b, c = self._obtenermodelo(parent)
                #newvalue = model(newvalue)
            if not newvalue == self.valueBufferCopy(fieldname):
                self._model.setValue(fieldname,newvalue)
            self.__bufferChanged(fieldname)

    @decorators.NotImplementedWarn
    def transaction(self,lock = False):
        try:
            if lock:
                pass
            else:
                sql = 'savepoint s' + str(self._micounterTran)
                self._model._cursor.execute(sql)
                self._micounterTran+=1
        except:
            return False
        else:
            return True

    @decorators.NotImplementedWarn
    def commit(self):
        try:            
            self._micounterTran-=1
            self._model._cursor.execute('COMMIT')           
        except:
            return False
        else:
            return True

    @decorators.NotImplementedWarn
    def commitBuffer(self): #FIXME REVISAR
        return True
    """        
        if self.__beforeCommit():
            if self._mode == self.Edit: #Edit
                try:
                    anterior=model_to_dict(self._currentregister)
                    for k,v in self._update.items():
                        setattr(self._currentregister,k,v)
                        self._currentregister.save(force_update=True)
                        Forzamos que el valor del buffer sea el anterior para que sea accesible por ValueBufferCopy
                        self._currentregister=anterior
                        self.__afterCommit()
                        return True 
                except Exception as exc:
                    milog.error("Error al actualizar en %s ",self._stabla)
                    milog.debug("Error al actualizar en %s %s",self._stabla,exc.__str__())
                    return False                   
            elif self._mode == self.Del: #Del
                try:
                    self._currentregister.delete()
                    self._currentregister=None                
                except Exception as exc:
                    milog.error("Error al borrar en %s ",self._stabla)
                    milog.debug("Error al borrar en %s %s",self._stabla,exc.__str__())
                    return False                   
                return True 
            elif self._mode == self.Insert: #Insert
                try:
                    print(self._update)
                    nuevo=self._model.objects.create(**self._update)                      
                    self._currentregister=nuevo      
                    self.__afterCommit()         
                    return True
                except Exception as exc:
                    milog.error("Error al insertar en %s ",self._stabla)
                    milog.debug("Error al insertar en %s %s",self._stabla,exc.__str__())
                return False                   
            else:
                return True 
    """
    @decorators.NotImplementedWarn
    def rollback(self):
        try:           
            self._micounterTran-=1
            sql = 'rollback to savepoint s' + str(self._micounterTran)
            self._model._cursor.execute(sql)
        except:
            return False
        else:
            return True

    @decorators.NotImplementedWarn
    def transactionLevel(self):            
        return self._micounterTran  

    def refresh(self):
        self._model.refresh()

    def size(self):
        return self._model.rowCount()

    def at(self):
        row = self._currentregister
        if row < 0: return -1
        if row >= self._model.rows: return -2
        return row

    def move(self, row):
        if row < 0: row = -1
        if row >= self._model.rows: row = self._model.rows
        if self._currentregister == row: return False
        topLeft = self._model.index(row,0)
        bottomRight = self._model.index(row,self._model.cols-1)
        new_selection = QtGui.QItemSelection(topLeft, bottomRight)
        self._selection.select(new_selection, QtGui.QItemSelectionModel.ClearAndSelect)
        self._currentregister = row
        self._current_changed.emit(self.at())
        if row < self._model.rows and row >= 0: return True
        else: return False

    def moveby(self, pos):
        return self.move(pos+self._currentregister)

    def first(self): return self.move(0)

    def prev(self): return self.moveby(-1)

    def __next__(self): return self.moveby(1)

    def last(self): return self.move(self._model.rows-1)

    def setModeAccess(self, modeAccess):
        self._mode = modeAccess
        return True

    def modeAccess(self):
        return self._mode

    def refreshBuffer(self):
        self._update=dict() #cambiar
        if self.modeAccess() == self.Insert:
            if self._model.fieldType(self._model.pK()) == "serial":
                q = FLSqlQuery()
                q.setSelect(u"nextval('" + self._model._table + "_" + self._model._pk + "_seq')")
                q.setFrom("")
                q.setWhere("")
                if not q.exec():
                    print("not exec sequence")
                    return None
                if q.first():
                    val = q.value(0)
                    #self._update[pk] = val FIXME : Actualizar el registro con una consulta sql?
                else:
                    return None

    def table(self):
        return self._model._table

    def cursorRelation(self):
        return None

    def action(self):
        return self._model._action

    def primaryKey(self):
        return self._model.pK()

    def size(self):
        return len(self._model._table.fields)

    @decorators.NotImplementedWarn
    def commitBuffer(self):
        return True

    @QtCore.pyqtSlot()
    def insertRecord(self):
        print("Insert a row ", self._action.name)
        self._mode = self.Insert
        self._action.openDefaultFormRecord()

    @QtCore.pyqtSlot()
    def editRecord(self):
        print("Edit the row!", self._action.name)
        self._mode = self.Insert
        self._action.openDefaultFormRecord()


    @QtCore.pyqtSlot()
    def deleteRecord(self):
        self._mode = self.Delete
        print("Drop the row!", self._action.name)
        self._action.openDefaultFormRecord()

    @QtCore.pyqtSlot()
    def browseRecord(self):
        print("Inspect, inspect!", self._action.name)
        self._action.openDefaultFormRecord()

    @QtCore.pyqtSlot()
    def copyRecord(self):
        print("Clone your clone", self._action.name)

    def fieldDisabled(fN):
        if self._mode == self.Insert or self._mode == self.Edit:
            return True
        else:
            return False
    """
  if (d->modeAccess_ == INSERT || d->modeAccess_ == EDIT) {
    if (d->cursorRelation_ && d->relation_) {
      if (!d->cursorRelation_->metadata())
        return false;
      return (d->relation_->field().lower() == fN.lower());
    } else
      return false;
  } else
    return false;
}
    """
#PRIVADOS

    def __bufferChanged(self,fieldname):
        if self._bufferChanged==None:
            return True
        else:
            if self._bufferChanged(fieldname):
                return True 
            else:
                return False

    def __beforeCommit(self):
        if not self._activatedCommitActions:
            return True
        if self._beforeCommit==None:
            return True
        else:
            if self._beforeCommit(self):
                return True 
            else:
                return False

    def __afterCommit(self):
        if not self._activatedCommitActions:
            return True
        if self._afterCommit==None:
            return True
        else:
            if self._afterCommit(self):
                return True 
            else:
                return False


