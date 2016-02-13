# encoding: UTF-8
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
import traceback
import sip
sip.setapi('QString', 1)

from PyQt4 import QtGui, QtCore # , uic

import pineboolib
#from pineboolib.qsaglobals import ustr
from pineboolib.utils import DefFun, filedir

Qt = QtCore.Qt
# TODO: separar en otro fichero de utilidades

def ustr1(t):
    if isinstance(t, str): return t
    #if isinstance(t, QtCore.QString): return str(t)
    #if isinstance(t, str): return str(t,"UTF-8")
    try:
        return str(t)
    except Exception as e:
        print("ERROR Coercing to string:", repr(t))
        print("ERROR", e.__class__.__name__, str(e))
        return None

def ustr(*t1):
    return "".join([ ustr1(t) for t in t1 ])

def NotImplementedWarn(fn):
    def newfn(*args,**kwargs):
        ret = fn(*args,**kwargs)
        x_args = [ repr(a) for a in args] + [ "%s=%s" % (k,repr(v)) for k,v in list(kwargs.items())]
        print("WARN: Function not yet implemented: %s(%s) -> %s" % (fn.__name__,", ".join(x_args),repr(ret)))
        return ret
    return newfn

def WorkingOnThis(fn):
    def newfn(*args,**kwargs):
        ret = fn(*args,**kwargs)
        x_args = [ repr(a) for a in args] + [ "%s=%s" % (k,repr(v)) for k,v in list(kwargs.items())]
        print("WARN: A developer is working on this function : %s(%s) -> %s" % (fn.__name__,", ".join(x_args),repr(ret)))
        return ret
    return newfn

class QLayoutWidget(QtGui.QWidget):
    pass

class ProjectClass(QtCore.QObject):
    def __init__(self):
        super(ProjectClass, self).__init__()
        self._prj = pineboolib.project

class QCheckBox(QtGui.QCheckBox):
    def __getattr__(self, name): return DefFun(self, name)

    @QtCore.pyqtProperty(int)
    def checked(self):
        return self.isChecked()

    @checked.setter
    def checked(self, v):
        self.setCheckState(v)



class QComboBox(QtGui.QComboBox):
    def __getattr__(self, name): return DefFun(self, name)
    @property
    def currentItem(self): return self.currentIndex

    def setCurrentItem(self, i): return self.setCurrentIndex(i)

class QButtonGroup(QtGui.QFrame):
    def __getattr__(self, name): return DefFun(self, name)
    @property
    def selectedId(self): return 0

class FLSqlQuery(ProjectClass):
    """
    Implementacion de FlSqlquery de Abanq para compatibilidad con python
    """
    def __init__(self):
        self._sSELECT=""
        self._columns=[]
        self._sWHERE=""
        self._sFROM=""
        self._sORDER=""
        self.__tables=[]
        self._sTablas=""
        self._cursor=None
        self._datos=None
        self._posicion=None
        self._row=None

       #Establecimiento de valores
    def setSelect(self,sSELECT):
        self._sSELECT=sSELECT
        self._columns=[]
        for scolumna in self._sSELECT.split(","):
            self._columns.append(scolumna.strip().upper())

    def select(self):
        return self._sSELECT

    def setFrom(self,sFROM):
        self._sFROM=sFROM

    def From(self):
        return self._sFROM

    def setWhere(self,swhere):
        self._sWHERE=swhere

    def where(self):
        return self._sWHERE

    def setOrderBy(self,orderBy):
        self._sORDER=orderBy

    def orderBy(self):
        return self._sORDER

    def setTablesList(self,tablas):
        self._sTablas=tablas
        self._tables=[]
        for stable in self._sTablas.split(","):
            self._tables.append(stable.strip().upper())

    def sql(self):
        sSQL= "SELECT " + self._sSELECT
        if self._sFROM : 
            sSQL=sSQL + " FROM " +self._sFROM
        if self._sWHERE : 
            sSQL=sSQL + " WHERE " +self._sWHERE
        if self._sORDER : 
            sSQL=sSQL + " ORDER BY " +self._sORDER
        return sSQL


    def setForwardOnly(self,valor):
        #De principio nada
        pass
    #ejecucion de consulta y scroll
    def exec(self,connection=None):
        try:
            micursor=self.__damecursor(connection)
            micursor.execute(self.sql())
            self._cursor=micursor
        except:
            return False
        else:
            return True 

    def exec_(self,connection=None):
        return self.exec(connection)

    def first(self):
        self._posicion=0
        if self._datos:
            self._row==self._datos[0]
            return True 
        else:
            try:
                self._row=self._cursor.fetchone()
                if self._row==None:
                    return False
                else:
                    return  True
            except:
                return False 
        
    def next(self):        
        if self._posicion is None:
            self._posicion=0            
        else:
            self._posicion+=1
        if self._datos:
            if self._posicion>=len(self._datos):
                return False
            self._row=self._datos[self._posicion]
            return True 
        else:
            try:
                self._row=self._cursor.fetchone()
                if self._row==None:
                    return False
                else:
                    return  True
            except:
                return False 
    
    def last(self):
        __cargarDatos
        if self._datos:
            self._posicion=len(self._datos)-1
            self._row==self._datos[self._posicion]
        else:
            return False

    def prev(self):
        self._posicion-=1
        if self._datos:
            if self._posicion<0:
                return False
            self._row==self._datos[self._posicion]
            return True 
        else:
            return False 


    def size(self):
        self.__cargarDatos()
        if self._datos:
            return len(self._datos)
        else:
            return 0
    #acceso valores
    def value(self,sCampo):
        i=self.__damePosDeCadena(sCampo)
        return self._row[i]

    def isNull(self,sCampo):
        i=self.__damePosDeCadena(sCampo)
        return (self._row[i]==None)



    #PRIVADAS
    def __del__(self):
        try:                        
            del self._datos
            self._cursor.close()
            del self._cursor
        except:
            pass
    
    def __cargarDatos(self):
        if self._datos:
            pass
        else:
            self._datos=self._cursor.fetchall()


    @classmethod
    def __damecursor(cls,miconnection=None):
        if miconnection:
            return connections[miconnection].cursor()
        else:
            return dameConexionDef().cursor()
    def __damePosDeCadena(self,sCampo):
        if isinstance(sCampo, int):
            return sCampo
        else:
            try:
                return self._columns.index(sCampo.strip().upper())
            except:
                try:
                    sAux=sCampo.split(".")[-1]
                except:
                    sAux=sCampo
                i=0                
                for x in self._cursor.description:
                    if x.name==sAux: 
                        return i
                    i+=1
                raise NameError("Error columna " +sCampo)



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

    @NotImplementedWarn
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

    @NotImplementedWarn
    def setNull(self,fieldname):
        if not self.valueBufferCopy(fieldname) is None:
            self.setValueBuffer(fieldname, None)
        self.__bufferChanged(fieldname)

    def valueBuffer(self, fieldname):
        if self._currentregister < 0 or self._currentregister > self._model.rows: return None
        return self._model.value(_currentregister, fieldname)

    @NotImplementedWarn 
    def valueBufferCopy(self,fieldname):
        return self._model.value(self._currentregister, fieldname)

    @NotImplementedWarn
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

    @NotImplementedWarn
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

    @NotImplementedWarn
    def commit(self):
        try:            
            self._micounterTran-=1
            self._model._cursor.execute('COMMIT')           
        except:
            return False
        else:
            return True

    @NotImplementedWarn
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
    @NotImplementedWarn
    def rollback(self):
        try:           
            self._micounterTran-=1
            sql = 'rollback to savepoint s' + str(self._micounterTran)
            self._model._cursor.execute(sql)
        except:
            return False
        else:
            return True

    @NotImplementedWarn
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

    @NotImplementedWarn
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


class ProgressDialog(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(ProgressDialog,self).__init__(*args, **kwargs)
        self.title = "Untitled"
        self.step = 0
        self.steps = 100
    def __getattr__(self, name): return DefFun(self, name)

    def setup(self, title, steps):
        self.title = title
        self.step = 0
        self.steps = steps
        self.setWindowTitle("%s - %d/%d" % (self.title,self.step,self.steps))
        self.setWindowModality(QtCore.Qt.ApplicationModal)

    def setProgress(self, step):
        self.step = step
        self.setWindowTitle("%s - %d/%d" % (self.title,self.step,self.steps))
        if step > 0: self.show()
        self.update()
        QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.ExcludeUserInputEvents)


class FLUtil(ProjectClass):
    progress_dialog_stack = []
    def __getattr__(self, name): return DefFun(self, name)

    def translate(self, group, string):
        return QtCore.QString(string)

    def sqlSelect(self, table, fieldname, where):
        if where: where = "AND " + where
        cur = pineboolib.project.conn.cursor()

        cur.execute("""SELECT %s FROM %s WHERE 1=1 %s LIMIT 1""" % (fieldname, table, where))
        for ret, in cur:
            return ret

    def createProgressDialog(self, title, steps):
        pd_widget = ProgressDialog()
        pd_widget.setup(title, steps)
        self.__class__.progress_dialog_stack.append(pd_widget)

    def setProgress(self, step_number):
        pd_widget = self.__class__.progress_dialog_stack[-1]
        pd_widget.setProgress(step_number)

    def destroyProgressDialog(self):
        pd_widget = self.__class__.progress_dialog_stack[-1]
        del self.__class__.progress_dialog_stack[-1]
        pd_widget.hide()
        pd_widget.close()

    def nombreCampos(self, tablename):
        prj = pineboolib.project
        table = prj.tables[tablename]
        campos = [ field.name for field in table.fields ]
        return [len(campos)]+campos

    def addMonths(self, fecha, offset):
        if isinstance(fecha, str) or isinstance(fecha, QtCore.QString):
            fecha = QtCore.QDate.fromString(fecha)
        if not isinstance(fecha, QtCore.QDate):
            print("FATAL: FLUtil.addMonths: No reconozco el tipo de dato %r" % type(fecha))
        return fecha.addMonths(offset)




class CursorTableModel(QtCore.QAbstractTableModel):
    rows = 15
    cols = 5
    _cursor = None

    def __init__(self, action,project, *args):
        super(CursorTableModel,self).__init__(*args)
        from pineboolib.qsaglobals import aqtt

        self._action = action
        self._prj = project
        if action and action.table:
            self._table = project.tables[action.table]
        else:
            raise AssertionError
        self.sql_fields = []
        self.field_aliases = []
        self.field_type = []
        for field in self._table.fields:
            if field.visible_grid:
                self.sql_fields.append(field.name)
                self.field_aliases.append(aqtt(field.alias))
            self.field_type.append(field.mtd_type)    
            if field.pk: self._pk = field.name

        self._data = []
        self.cols = len(self.sql_fields)
        self.rows = 0
        self.where_filters = {}
        self.refresh()

    def refresh(self):
        parent = QtCore.QModelIndex()
        oldrows = self.rows
        self.beginRemoveRows(parent, 0, oldrows )
        where_filter = ""
        for k, wfilter in sorted(self.where_filters.items()):
            if wfilter is None: continue
            wfilter = wfilter.strip()
            if not wfilter: continue
            where_filter += " AND " + wfilter
        self._cursor = self._prj.conn.cursor()
        # FIXME: Cuando la tabla es una query, aquí hay que hacer una subconsulta.
        # FIXME: Agregado limit de 5000 registros para evitar atascar pineboo
        # TODO: Convertir esto a un cursor de servidor
        sql = """SELECT %s FROM %s WHERE 1=1 %s LIMIT 5000""" % (", ".join(self.sql_fields),self._table.name, where_filter)
        self._cursor.execute(sql)
        self.rows = 0
        self.endRemoveRows()
        if oldrows > 0:
            self.rowsRemoved.emit(parent, 0, oldrows - 1)
        newrows = self._cursor.rowcount
        self.beginInsertRows(parent, 0, newrows - 1)
        print("QUERY:", sql)
        self.rows = newrows
        self._data = []
        for row in self._cursor:
            self._data.append(row)
        self.endInsertRows()
        topLeft = self.index(0,0)
        bottomRight = self.index(self.rows-1,self.cols-1)
        self.dataChanged.emit(topLeft,bottomRight)
        print("rows:", self.rows)

    def value(self, row, fieldname):
        if row < 0 or row >= self.rows: return None
        col = self.sql_fields.index(fieldname)
        return self._data[row][col]

    @NotImplementedWarn
    def setValue(self,fieldname, value):
        return True

    def pK(self): #devuelve el nombre del campo pk
        return self._pk

    def fieldType(self, fieldName): # devuelve el tipo de campo
        return self.field_type[self.sql_fields.index(fieldname)]

    def columnCount(self, parent = None):
        if parent is None: parent = QtCore.QModelIndex()
        if parent.isValid(): return 0
        #print "colcount", self.cols
        return self.cols

    def rowCount(self, parent = None):
        if parent is None: parent = QtCore.QModelIndex()
        if parent.isValid(): return 0
        #print "rowcount", self.rows
        return self.rows

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                return "%s" % self.field_aliases[section]
        return QtCore.QAbstractTableModel.headerData(self, section, orientation, role)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        row = index.row()
        col = index.column()
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            try:
                val = self._data[row][col]
                ret = ustr(val)
                #print " data -> ", row, col, ret
                return ret
            except Exception as e:
                print("CursorTableModel.data:", row,col,e)
                print(traceback.format_exc())
                raise

        return None


class FLTableDB(QtGui.QWidget):
    _tableView = None
    _vlayout = None
    _lineEdit = None
    _comboBox_1 = None
    _comboBox_2 = None

    def __init__(self, parent = None, action_or_cursor = None, *args):
        print("FLTableDB:", parent, action_or_cursor , args)
        # TODO: Falta el lineeditsearch y el combo, que los QS lo piden
        super(FLTableDB,self).__init__(parent,*args)
        # TODO: LA inicialización final hay que hacerla más tarde, en el primer
        # show(), porque sino obligas a tenerlo todo preparado en el constructor.
        self._tableView = QtGui.QTableView()
        self._lineEdit = QtGui.QLineEdit()
        _label1 = QtGui.QLabel()
        _label2 = QtGui.QLabel()
        self._comboBox_1 = QtGui.QComboBox()
        self._comboBox_2 = QtGui.QComboBox()
        _label1.setText("Buscar")
        _label2.setText("en")
        self._vlayout = QtGui.QVBoxLayout()
        _hlayout =  QtGui.QHBoxLayout()
        self._tableView._v_header = self._tableView.verticalHeader()
        self._tableView._v_header.setDefaultSectionSize(18)
        self._tableView._h_header = self._tableView.horizontalHeader()
        self._tableView._h_header.setDefaultSectionSize(70)
        _hlayout.addWidget(_label1)
        _hlayout.addWidget(self._lineEdit)
        _hlayout.addWidget(_label2)
        _hlayout.addWidget(self._comboBox_1)
        _hlayout.addWidget(self._comboBox_2)
        self._vlayout.addLayout(_hlayout)
        self._vlayout.addWidget(self._tableView)
        self.setLayout(self._vlayout)
        self._parent = parent
        while True:
            parent_cursor = getattr(self._parent,"_cursor", None)
            if parent_cursor: break
            new_parent = self._parent.parentWidget()
            if new_parent is None: break
            self._parent = new_parent
            print(self._parent)

        self._tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self._tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self._tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self._tableView.setAlternatingRowColors(True)

        if action_or_cursor is None and parent_cursor:
            action_or_cursor = parent_cursor
        if isinstance(action_or_cursor,FLSqlCursor):
            self._cursor = action_or_cursor
        elif isinstance(action_or_cursor,str):
            self._cursor = FLSqlCursor(action_or_cursor)
        else:
            self._cursor = None
        if self._cursor:
            self._tableView._h_header.setResizeMode(QtGui.QHeaderView.ResizeToContents)
            self._tableView.setModel(self._cursor._model)
            self._tableView.setSelectionModel(self._cursor.selection())
        self.tableRecords = self # control de tabla interno

        #Carga de comboBoxs y connects .- posiblemente a mejorar
        if self._cursor:
            for column in range(self._cursor._model.columnCount()):
                self._comboBox_1.addItem(self._cursor._model.headerData(column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole))
                self._comboBox_2.addItem(self._cursor._model.headerData(column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole))
        self._comboBox_1.addItem("*")
        self._comboBox_2.addItem("*")
        self._comboBox_1.setCurrentIndex(0)
        self._comboBox_2.setCurrentIndex(1)
        self._comboBox_1.currentIndexChanged.connect(self.comboBox_putFirstCol)
        self._comboBox_2.currentIndexChanged.connect(self.comboBox_putSecondCol)        

        self.sort = []
        self.timer_1 = QtCore.QTimer(self)
        self.timer_1.singleShot(100, self.loaded)

    def __getattr__(self, name): return DefFun(self, name)

    def loaded(self):
        # Es necesario pasar a modo interactivo lo antes posible
        # Sino, creamos un bug en el cierre de ventana: se recarga toda la tabla para saber el tamaño
        print("FLTableDB: setting columns in interactive mode")
        self._tableView._h_header.setResizeMode(QtGui.QHeaderView.Interactive)

    def cursor(self):
        assert self._cursor
        return self._cursor

    def obj(self):
        return self

    def comboBox_putFirstCol(self):
        self.putFirstCol(str(self._comboBox_1.currentText()))

    def comboBox_putSecondCol(self):
        self.putSecondCol(str(self._comboBox_2.currentText()))

    def putFirstCol(self, fN):
        _oldPos= None
        _oldFirst = self._tableView._h_header.logicalIndex(0)    
        for column in range(self._cursor._model.columnCount()):
            if self._cursor._model.headerData(column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole).lower() == fN.lower():
                _oldPos = self._tableView._h_header.visualIndex(column) 
                if not self._comboBox_1.currentText() == fN:
                    self._comboBox_1.setCurrentIndex(column)
                    return False
                break

        if not _oldPos or fN == "*":
            return False
        else:         
            self._tableView._h_header.swapSections(_oldPos, 0)
            self._comboBox_2.setCurrentIndex(_oldFirst)
            return True

    def putSecondCol(self, fN):
        _oldPos= None
        _oldSecond = self._tableView._h_header.logicalIndex(1)
        for column in range(self._cursor._model.columnCount()):
            if self._cursor._model.headerData(column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole).lower() == fN.lower():
                _oldPos = self._tableView._h_header.visualIndex(column)
                break

        if not _oldPos or fN == "*":
            return False
        if not self._comboBox_1.currentText() == fN:           
            self._tableView._h_header.swapSections(_oldPos, 1)
        else:
            self._comboBox_1.setCurrentIndex(_oldSecond)
        return True

    @QtCore.pyqtSlot()
    def close(self):
        print("FLTableDB: close()")

    @QtCore.pyqtSlot()
    def refresh(self):
        print("FLTableDB: refresh()", self.parent().parent().parent())
        self._cursor.refresh()

    @QtCore.pyqtSlot()
    def show(self):
        print("FLTableDB: show event")
        super(FLTableDB, self).show()

    @QtCore.pyqtSlot()
    def insertRecord(self):
        self._cursor.insertRecord()

    @QtCore.pyqtSlot()
    def editRecord(self):
        self._cursor.editRecord()

    @QtCore.pyqtSlot()
    def deleteRecord(self):
        self._cursor.deleteRecord()

    @QtCore.pyqtSlot()
    def browseRecord(self):
        self._cursor.browseRecord()

    @QtCore.pyqtSlot()
    def copyRecord(self):
        self._cursor.copyRecord()


class FLTable(QtGui.QTableWidget):
    def __getattr__(self, name): return DefFun(self, name)

class FLForm(QtGui.QWidget):
    known_instances = {}
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

class FLFormSearchDB( QtGui.QWidget ):
    _accepted = None
    _cursor = None

    def __init__(self,cursor):
        super(FLFormSearchDB,self).__init__()
        self._accepted = False
        self._cursor = FLSqlCursor(cursor)

    def __getattr__(self, name): return DefFun(self, name)

    @NotImplementedWarn
    def setCursor(self):
        print("Definiendo cursor")

    @NotImplementedWarn
    def setMainWidget(self):

        print("Creamos la ventana")
        

    @NotImplementedWarn
    def exec_(self, valor):
        print("Ejecutamos la ventana y esperamos respuesta, introducimos desde y hasta en cursor")
        return valor

    @NotImplementedWarn
    def setFilter(self):
        print("configuramos Filtro")

    @NotImplementedWarn
    def accepted(self):
        return self._accepted

    @NotImplementedWarn
    def cursor(self):
        return self._cursor


class FLReportViewer(ProjectClass):
    Append = 0x01
    Display = 0x02
    PageBreak = 0x04

    _requestUpdateReport = QtCore.pyqtSignal(int, name='requestUpdateReport')

    def __init__(self, *args):
        super(FLReportViewer,self).__init__()
        #  FLReportViewerInterface() : QObject(0), obj_(0) {
        #  FLReportViewerInterface(FLReportViewer *obj) : QObject(obj), obj_(0) {
        #  FLReportViewerInterface(QWidget *w, bool) : QObject(w) {
        #  FLReportViewerInterface(FLReportEngine *r) : QObject(0) {
        self.connects()

    def __getattr__(self, name): return DefFun(self, name)

    def connects(self):
        pass

    @NotImplementedWarn
    def renderReport(self, initRow = 0, initCol = 0, append = False, displayReport = True):
        return True

    @NotImplementedWarn
    def renderReport2(self, initRow = 0, initCol = 0, flags = Display):
        return True

    @NotImplementedWarn
    def setReportData(self, xmlDoc_Or_Query):
        return None

    @NotImplementedWarn
    def setReportTemplate(self,  t, style = None):
        return True

    @NotImplementedWarn
    def reportData(self):
        return None

    @NotImplementedWarn
    def reportTemplate(self):
        return None

    @NotImplementedWarn
    def exec_(self):
        return

    @NotImplementedWarn
    def show(self):
        return

    @NotImplementedWarn
    def csvData(self):
        return None

    @NotImplementedWarn
    def printReport(self): return None

    @NotImplementedWarn
    def printReportToPS(self,outPsFile): return None

    @NotImplementedWarn
    def printReportToPDF(self,outPdfFile): return None

    @NotImplementedWarn
    def setNumCopies(self,numCopies): return None

    @NotImplementedWarn
    def setPrintToPos(self,ptp): return None

    @NotImplementedWarn
    def setPrinterName(self,pName): return None

    @NotImplementedWarn
    def reportPrinted(self): return True

    @NotImplementedWarn
    def reparent(self,parentFrame): return None

    @NotImplementedWarn
    def slotFirstPage(self): return None

    @NotImplementedWarn
    def slotLastPage(self): return None

    @NotImplementedWarn
    def slotNextPage(self): return None

    @NotImplementedWarn
    def slotPrevPage(self): return None

    @NotImplementedWarn
    def slotZoomUp(self): return None

    @NotImplementedWarn
    def slotZoomDown(self): return None

    @NotImplementedWarn
    def exportFileCSVData(self): return None

    @NotImplementedWarn
    def exportToPDF(self): return None

    @NotImplementedWarn
    def sendEMailPDF(self): return None

    @NotImplementedWarn
    def saveSVGStyle(self): return None

    @NotImplementedWarn
    def saveSimpleSVGStyle(self): return None

    @NotImplementedWarn
    def loadSVGStyle(self): return None

    @NotImplementedWarn
    def setAutoClose(self,b): return None

    @NotImplementedWarn
    def setResolution(self,dpi): return None

    @NotImplementedWarn
    def setPixel(self,relDpi): return None

    @NotImplementedWarn
    def setDefaults(self): return None

    @NotImplementedWarn
    def updateReport(self): return None

    @NotImplementedWarn
    def updateDisplay(self): return None

"""
  void setStyleName(const QString &style) {
  MReportViewer *rptViewer() {
  void setReportEngine(FLReportEngine *r) {
  void rptViewerEmbedInParent(QWidget *parentFrame) {
  void setReportPages(FLReportPages *pgs) {
  FLPicture *getCurrentPage() {
  FLPicture *getFirstPage() {
  FLPicture *getPreviousPage() {
  FLPicture *getNextPage() {
  FLPicture *getLastPage() {
  FLPicture *getPageAt(uint i) {
  void clearPages() {
  void appendPage() {
  int getCurrentIndex() {
  void setCurrentPage(int idx) {
  void setPageSize(int s) {
  void setPageOrientation(int o) {
  void setPageDimensions(QSize dim) {
  int pageSize() {
  int pageOrientation() {
  QSize pageDimensions() {
  int pageCount() {
  QObject *child(const QString &objName) {
  void disableSlotsPrintExports(bool disablePrints = true, bool disableExports = true) {
  void setName(const QString &n) {
  FLReportViewer *obj() {
"""


class QLineEdit(QtGui.QLineEdit):
    def __init__(self, *args, **kwargs):
        super(QLineEdit, self).__init__(*args,**kwargs)
        class TextEmul:
            def __init__(self, parent, f):
                self.parent = parent
                self.f = f
            def __call__(self):
                return self.f()
            def __str__(self):
                return self.f()
            def __getattr__(self, name):
                return getattr(self.f(),name)

        self.text = TextEmul(self, super(QLineEdit,self).text)

    def __getattr__(self, name):
        print("flcontrols.QLineEdit: Emulando método %r" % name)
        return self.defaultFunction

    def defaultFunction(self, *args, **kwargs):
        print("flcontrols.QLineEdit: llamada a método no implementado", args,kwargs)

class QListView(QtGui.QListView):
    def __init__(self, *args, **kwargs):
        super(QListView, self).__init__(*args, **kwargs)

    def __getattr__(self, name):
        print("flcontrols.QListView: Emulando método %r" % name)
        return self.defaultFunction

    def defaultFunction(self, *args, **kwargs):
        print("flcontrols.QListView: llamada a método no implementado", args,kwargs)

class QPushButton(QtGui.QPushButton):
    @property
    def pixmap(self):
        return self.icon()

    @pixmap.setter
    def pixmap(self, value):
        return self.setIcon(value)

    def setPixmap(self, value):
        return self.setIcon(value)

    def getToggleButton(self):
        return self.isCheckable()
    def setToggleButton(self, v):
        return self.setCheckable(v)

    toggleButton = property(getToggleButton,setToggleButton)


class FLFieldDB(QtGui.QWidget):
    _fieldName = "undefined"
    _label = None
    _lineEdit = None 
    _layout = None
    

    def __init__(self, parent, *args):
        super(FLFieldDB,self).__init__(parent,*args)
        print("FLFieldDB:", parent, args)
        #TODO: Detectar el tipo de campo y añadir los controles adecuados, Por defecto todos son campos de texto
        self._lineEdit = QtGui.QLineEdit()
        self._layout = QtGui.QHBoxLayout()
        self._label = QtGui.QLabel()
        spacer = QtGui.QSpacerItem(40,0,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Expanding)
        self._layout.addItem(spacer)
        self._layout.addWidget(self._label)
        self._layout.addWidget(self._lineEdit)
        self.setLayout(self._layout)
    
    def __getattr__(self, name): return DefFun(self, name)
            
    @property
    def fieldName(self):
        return self._fieldName

    @fieldName.setter
    def fieldName(self, fN):
        self._fieldName = fN
        self._label.setText(self._fieldName)
        

    def setFieldName(self, fN):
        self._fieldName = fN
        self._label.setText(self._fieldName)
       
    @QtCore.pyqtSlot()
    def searchValue(self):
        print("FLFieldDB: searchValue()")

    def setShowAlias(self, show):
        if not show:
            self._label.setText("")
