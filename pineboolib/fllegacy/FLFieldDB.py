# -*- coding: utf-8 -*-

from PyQt4 import QtCore,QtGui

from pineboolib import decorators
from pineboolib.fllegacy.FLFieldMetaData import FLFieldMetaData
from mailcap import show
from idlelib.EditorWindow import EditorWindow
from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from asyncio.windows_events import NULL
from pineboolib.fllegacy.FLRelatiomMetaData import FLRelationMetaData
from builtins import False
from pineboolib.flcontrols import QComboBox
from pineboolib.flparser.qsatype import FLSqlCursor
from distlib.compat import IDENTIFIER

class FLFieldDB(QtGui.QWidget):
    
    editor_ = 0 #Editor para el contenido del campo que representa el componente
    fieldName_ = None #Nombre del campo de la tabla al que esta asociado este componente
    tableName_ = None #Nombre de la tabla fóranea
    actionName_ = None #Nombre de la accion
    foreignField_ = None #Nombre del campo foráneo
    fieldRelation_ = None #Nombre del campo de la relación
    filter_ = None #Nombre del campo de la relación
    cursor_ = 0 #Cursor con los datos de la tabla origen para el componente
    cursorAux = 0 #  Cursor auxiliar de uso interno para almacenar los registros de la tabla relacionada con la de origen
    cursorInit = False #Indica que si ya se ha inicializado el cursor
    cursorAuxInit = False #Indica que si ya se ha inicializado el cursor auxiliar
    topWidget_ = 0 #Ventana superior
    showed = False #Indica que el componete ya ha sido mostrado una vez
    cursorBackup_ = None #Backup del cursor por defecto para acceder al modo tabla externa
    showAlias_ = False #Variable que almacena el estado de la propiead showAlias
    textFormat_ = Qt.AutoText #El formato del texto
    """
    Seleccionador de fechas.
    """
    datePopup_ = 0
    dateFrame_ = 0
    datePickerOn_ = False

    accel_ = 0 #Aceleradores de combinaciones de teclas
    keepDisabled_ = False #Indica que el componente permanezca deshabilitado evitando que vuelva a habilitarse en sucesivos refrescos. Ver FLFieldDB::refresh().
    editorImg_ = 0 #Editor para imagenes
    pbAux_ = 0 #Boton auxiliar multifunción
    pbAux2_ = 0 #Boton auxiliar multifunción
    pbAux3_ = 0 #Boton auxiliar multifunción
    pbAux4_ = 0 #Boton auxiliar multifunción
    fieldAlias_ = None #Almacena el alias del campo que será mostrado en el formulario
    showEditor_ = True #Almacena el valor de la propiedad showEditor
    partDecimal_= None #Valor de cifras decimales en caso de ser distinto del definido en los metadatos del campo

    """
    Tamaños maximo y minimos iniciales
    """
    initMaxSize_ = None
    initMinSize_ = None

    """
    Para asistente de completado automático.
    """
    autoComPopup_= 0
    autoComFrame_= 0
    autoComFieldName_= None
    autoComFieldRelation_ = None
    autoCompMode_ = OnDemandF4
    timerAutoComp_ = 0

    """
    Auxiliares para poder repetir llamada a setMapValue y refrescar filtros
    """
    fieldMapValue_ = 0
    mapValue_ = None

    maxPixImages_ = None #Tamaño máximo de las imágenes en los campos pixmaps (en píxeles) @author Silix
    initNotNullColor_ = False #Colorear campos obligatorios @author Aulla

  


    def __init__(self ,parent, name = None, *args):
        super(FLFieldDB,self).__init__(parent, name = None, *args)
        self.pushButtonDB.setFlat(True)
        
        if not self.maxPixImages_:
            self.maxPixImages_ = 600
            
        self.topwidget_ = self.topLevelWidget()
        
        if self.topWidget_ and not self.topWidget_.inherits("FLFormDB"):
            topWid = QtCore.QWidget(self.parentWidget())
            while topWid and not topWid.inherits("FLFormDB"):
                topWid = topWid.parentWidget()
            self.topWidget_ = topWid
            
        if not self.topWidget_:
            print("FLFieldDB : El widget de nivel superior deber ser de la clase FLFormDB o heredar de ella - %r" % name)
        else:
            self.cursor_ = self.topWidget_.cursor()
        
        if not name:
            self.setName("FLieldDB")
        
        self.cursorBackup_ = 0
        self.partDecimal_ = -1
        


    
    def __getattr__(self, name): return DefFun(self, name)

    """
  Para obtener el nombre de la accion.

  @return Nombre de la accion
    """  

    def actionName(self):
        return self.actionName_
            

    """
  Para establecer el nombre de la accion.

  @param aN Nombre de la accion
    """  

    def setActionName(self, aN):
        self.actionName_ = aN
        if self.showed and self.topWidget_:
            self.initCursor()
            self.initEditor()
        else:
            self.initFakeEditor()

    """
  Para obtener el nombre del campo.

  @return Nombre del campo
    """

    def fieldName(self):
        return self.fieldName_

    """
  Para añadir un filtro al cursor.

    """

    def setFilter(self, f):
        if not self.filter_ == f:
            self.filter_ = f
            self.setMaValue()

    """
  Para obtener el filtro del cursor.

    """

    def filter(self):
        return self.fliter_


    """
  Para establecer el nombre del campo.

  @param fN Nombre del campo
    """

    def setFieldName(self, fN):
        self.fieldName_ = fN
        if self.showed:
            if self.topWidget_:
                self.initCursor()
                self.initEditor()
            else:
                self.initFakeEditor()
    """
  Para obtener el nombre de la tabla foránea.

  @return Nombre de la tabla
    """

    def tableName(self):
        return self.tableName_
    """
  Para establecer el nombre de la tabla foránea.

  @param fT Nombre de la tabla
    """

    def setTableName(self, fT):
        self.tableName_ = fT
        if self.showed:
            if self.topWidget:
                self.initCursor()
                self.initEditor()
            else:
                self.initFakeEditor()


    """
  Para obtener el nombre del campo foráneo.

  @return Nombre del campo
    """

    def foreignField(self):
        return self.foreingField_

    """
  Para establecer el nombre del campo foráneo.

  @param fN Nombre del campo
    """

    def setForeignField(self, fN):
        self.foreignField_ = fN
        if self.showed:
            if self.topWidget:
                self.initCursor()
                self.initEditor()
            else:
                self.initFakeEditor()

    """
  Para obtener el nombre del campo relacionado.

  @return Nombre del campo
    """

    def fieldRelation(self):
        return self.fieldRelation_

    """
  @return Alias del campo, es el valor mostrado en la etiqueta
    """
 
    def fieldAlias(self):
        return self.fieldAlias_

    """    
  Para obtener el widget editor.

  @return Objeto con el editor del campo
    """

    def editor(self):
        return self.editor_

    """
  Para establecer el nombre del campo relacionado.

  @param fN Nombre del campo
    """

    def setFieldRelation(self, fN):
        self.fieldRelation_ = fN
        if self.showed:
            if self.topWidget:
                self.initCursor()
                self.initEditor()
            else:
                self.initFakeEditor()

    """
  Para establecer el alias del campo, mostrado en su etiqueta si showAlias es true

  @param alias Alias del campo, es el valor de la etiqueta. Si es vacio no hace nada.
    """

    def setFieldAlias(self, alias):
        if alias:
            self.filedAlias_ = alias
            if self.showAlias_:
                self.textLabelDB.setText(self.fieldAlias_)

    """
  Establece el formato del texto

  @param f Formato del campo
    """

    def setTextFormat(self, f):
        self.textFormat_ = f
        ted = self.editor_
        if ted:
            ted.setTextFormat(self.textFormat_)

    """
  @return El formato del texto
    """

    def textFormat(self):
        ted = self.editor_
        if ted:
            return ted.textFormat()
        return self.textFormat_

    """
  Establece el modo de "echo"

  @param m Modo (Normal, NoEcho, Password)
    """

    def setEchoMode(self, m):
        led = self.editor_
        if led:
            led.setEchoMode(m.echoMode())


    """
  @return El mode de "echo" (Normal, NoEcho, Password)
    """

    def echoMode(self):
        led = self.editor_
        if led:
            return led.echoMode()
        return Qtgui.QlineEdit.Normal
    """
  Establece el valor contenido en elcampo.

  @param v Valor a establecer
    """

    def setValue(self, v):
        if not self.cursor_:
            return
        tMD = self.cursor_.metadata()
        if not tMD:
            return
        field = tMD.field(self.fielName_)
        if not field:
            print("FLFieldDB::setValue() : No existe el campo ",field)
            return

        cv = QtCore.QVariant(v)
        if field.hasOptionsList(): #{
            idxItem = -1
            if v.type() == QtCore.QVariant.String:
                idxItem = field.optionsList().findIndex(v.toString())
            if idxItem == -1:
                idxItem = v.toInt()
            self.editor_.setCurrentItem(idxItem)
            self.updateValue(self.editor_.currentText())#updateValue(::qt_cast<QComboBox *>(editor_)->currentText());
        return
        #}

        type_ = field.type()
        fltype = FLFieldMetaData.flDecodeType(type_)
        if v.type() == QtCore.QVariant.Bool and not fltype == QtCore.QVariant.Bool:# {
            if type_ == QtCore.QVariant.Double or type_ == QtCore.QVariant.Int or type_ == QtCore.QVariant.UInt:
                v = 0
            else:
                v.clear()
        #}
        if v.type() == QtCore.QVariant.String and not v.toString() == "": # .isEmpty()
            if type_ == QtCore.QVariant.Double and type_ == QtCore.QVariant.Int and type_ == QtCore.QVariant.UInt:
                v.clear()

        isNull = bool(not v.isValid() and v.isNull())
        if isNull and not field.allowNull():# {
            defVal = QtCore.QVariant(field.defaultValue())
            if defVal.isValid() and not defVal.isNull(): #{
                v = defVal
                isNull = False
    #}
  #}

        v.cast(fltype)

        if type_ == QtCore.QVariant.UInt or type_ == QtCore.QVariant.Int or type_ == QtCore.QVariant.String:
            if self.editor_:
                if self.editor_.text() == "":#bool doHome = (::qt_cast<FLLineEdit *>(editor_)->text().isEmpty()); 
                    doHome = True
                else:
                    doHome = False
                    
                    
                if isNull: #::qt_cast<FLLineEdit *>(editor_)->setText(isNull ? QString() : v.toString());
                    self.editor_.setText("")
                else:
                    self.editor_.setText(v.toString())
                
                
                if doHome:
                    self._editor.home(False)#::qt_cast<FLLineEdit *>(editor_)->home(false); 
        if type_ == QtCore.QVariant.StringList:
            if not self.editor_:
                return
            
            if isNull:#::qt_cast<QTextEdit *>(editor_)->setText(isNull ? QString() : v.toString()); 
                self.editor_.setText("")
            else:
                self.editor_.SetText(v.tostring())
      
        if type_ == QtCore.QVariant.Double:
            if not self.editor_:
                s= None
                if not isNull:
                    if not self.partDecimal_ == -1:#s.setNum(v.toDouble(), 'f', self.partDecimal_ != -1 ? self.partDecimal_ : field.partDecimal()) 
                        partDecimal = self.partDecimal_
                    else:
                        partDecimal = field.partDecimal()
                        
                    s.setNum(v.toDouble(),"f", partDecimal)

                self.editor_.setText(s)#::qt_cast<FLLineEdit *>(editor_)->setText(s);

        if type_ == FLFieldMetaData.Serial:

            if self.editor_:
                if isNull :#::qt_cast<FLSpinBox *>(editor_)->setValue(isNull ? 0 : v.toUInt()); 
                    self.editor_.setValue(0)
                else:
                    self.editor_.setValue(v.toUInt())
    
        if type_ == QtCore.QVariant.Pixmap:
            if self.editorImg_: #{
                cs= None
                if not isNull:
                    cs = v.toCString()
                if cs.isEmpty(): # {
                    self.editorImg.clear()
                    return
                #}
                pix = QtGui.QPixmap 
                if not QtGui.QPixmapCache.find(cs.left(100), pix): # { 
                    pix.loadFromData(cs)
                    QtGui.QPixmapCache.insert(cs.left(100), pix) 
                    # }
                if not pix.isNull():
                    self.editorImg_.setPixmap(pix)
                else:
                    self.editorImg_.clear()
        #}
        if type_ == QtCore.QVariant.Date:
            if (self.editor_):
                if isNull:
                    self.editor_.setdate(QtCore.QDate)
                else:
                    self.editor_.setDate(v.toDate())#::qt_cast<FLDateEdit *>(editor_)->setDate(isNull ? QDate() : v.toDate());

        if type_ == QtCore.QVariant.Time:
            if self.editor_:
                if isNull:
                    self.editor_.setTime(QtCore.Qtime)
                else:
                    self.editor_.setTime(v.toTime())#::qt_cast<QTimeEdit *>(editor_)->setTime(isNull ? QTime() : v.toTime());
                    
        if type_ == QtCore.QVariant.Bool:
            if self.editor_ and not isNull:
                self.editor_.setChecked(v.toBool())#::qt_cast<QCheckBox *>(editor_)->setChecked(v.toBool()); 


    """
  Obtiene el valor contenido en el campo.
    """
    @decorators.NotImplementedWarn
    def value(self):
        
        if not self.cursor_:
            return QtCore.QVariant
        
        tMD = self.cursor_.metadata()
        if not tMD:
            return QtCore.QVariant
        
        field = tMD.field(self.fieldName_)
        if not field:
            print("FLFieldDB::value() : No existe el campo ", self.fieldName_)
            return QtCore.QVariant
        
        v = QtCore.QVariant
        
        if field.hasOptionsList():
            v = self.editor_.currentItem()
            v.cast(QtCore.QVariant.Int)
            return v
        
        _type = field.type()
        fltype = FLFieldMetaData.flDecodeType(_type)
        if self.cursor_.bufferIsNull(self.fieldName_):
            if _type == QtCore.QVariant.Double or _type == QtCore.QVariant.Int or _type == QtCore.QVariant.UInt:
                return 0
            
        
        
        if _type == QtCore.QVariant.Double or _type == QtCore.QVariant.Int or _type == QtCore.QVariant.UInt or _type == QtCore.QVariant.String or _type == QtCore.QVariant.StringList:
            if self.editor_:
                ed_= FLLineEdit (self.editor_) #
                if ed_:
                    
                    v = ed_.text()
        
        elif _type == FLFieldMetaData.Serial:
            if(self.editor_):
                ed_ = FLSpinBox(self.editor_) # 
                if ed_:
                    v = ed_.value()
        
        elif _type == QtCore.QVariant.Pixmap:
            v = self.cursor_.valueBuffer(self.fieldName_)
        
        elif _type == QtCore.QVariant.Date:
            if self.editor_:
                v = self.editor_.date().toString(Qt.ISODate)

        elif _type == QtCore.QVariant.Time:
            if self.editor_:
                v = self.editor_.time().toString(Qt.ISODate)
        
        elif _type == QtCore.QVariant.Bool:
            if self.editor_:
                v = QtCore.QVariant(self.editor_.isChecked(),0)
    
    v.cast(fltype)
    return v


    """
  Marca como seleccionado el contenido del campo.
    """

    def selectAll(self):
        if not self.cursor_:
            return
        
        if not self.cursor_.metadata():
            return
        
        field = FLFieldMetaData(self.cursor_.metadata().field(self.fieldName_))
        
        if not field:
            return
        
        if field.type() == QtCore.QVariant.Double or field.type() == QtCore.QVariant.Int or field.type() == QtCore.QVariant.UInt or field.type() == QtCore.QVariant.String:
            if self.editor_:
                self.editor_.selectAll() #::qt_cast<FLLineEdit *>(editor_)->selectAll();
        elif field.type() == FLFieldMetaData.Serial:
            if self.editor_:
                self.editor_.selectAll() #::qt_cast<FLSpinBox *>(editor_)->selectAll();

    """
  Devuelve el cursor de donde se obtienen los datos. Muy util
  para ser usado en el modo de tabla externa (fieldName y tableName
  definidos, foreingField y fieldRelation en blanco).
    """

    def cursor(self):
        return self.cursor_

    """
  Devuelve el valor de la propiedad showAlias. Esta propiedad es
  usada para saber si hay que mostrar el alias cuando se está
  en modo de cursor relacionado.
    """

    def showAlias(self):
        return self.showAlias_
        

    """
  Establece el estado de la propiedad showAlias.
    """

    def setShowAlias(self, value):
        if not self.showAlias_ == value:
            self.showAlias_ = value 
            if self.showAlias_:
                self.textLabelDB.show()
            else:
                self.textLabelDB.hide()

    """
  Inserta como acelerador de teclado una combinación de teclas, devolviendo su identificador

  @param key Cadena de texto que representa la combinación de teclas (p.e. "Ctrl+Shift+O")
  @return El identificador asociado internamente a la combinación de teclas aceleración insertada
    """
    @decorators.NotImplementedWarn
    def insertAccel(self, key): #FIXME
        if not self.accel_:
            self.accel_ = QtCore.QAccel(self.editor_)
            #connect(accel_, SIGNAL(activated(int)), this, SLOT(emitActivatedAccel(int)));#FIXME
        
        id = self.accel_.findKey(QtCore.QKeySequence(key))
        
        if not id == -1:
            return 
        id = self.accel_.insertItem(QtCore.QKeySequence(key))
        return id
            

    """
  Elimina, desactiva, una combinación de teclas de aceleración según su identificador.

  @param identifier Identificador de la combinación de teclas de aceleración
    """
    @decorators.NotImplementedWarn
    def removeAccel(self, identifier): #FIXME
        if not self.accel_:
            return
        self.accel_.removeItem(identifier)
    

    """
  Establece la capacidad de mantener el componente deshabilitado ignorando posibles
  habilitaciones por refrescos. Ver FLFieldDB::keepDisabled_ .

  @param keep TRUE para activar el mantenerse deshabilitado y FALSE para desactivar
    """

    def setKeepDisabled(self, keep):
        self.keepDisabled_ = keep

    """
  Devuelve el valor de la propiedad showEditor.
    """
    
    def showEditor(self):
        return self.showEditor_

    """
  Establece el valor de la propiedad showEditor.
    """

    def setShowEditor(self, show):
        self.showEditor_ = show
        ed = QtGui.QWidget
        if self.editor_:
            ed = self.editor_
        elif self.editorImg_:
            ed = self.editorImg_
            
        if ed:
            if show:
                ed.show()
            else:
                ed.hide()
                
        

    """
  Establece el número de decimales
    """
    @decorators.NotImplementedWarn
    def setPartDecimal(self, d):
        editor = FLLineEdit(self.editor_)
        if editor and editor.type == QtCore.QVariant.Double:
            self.partDecimal_ = d
            self.refreshQuick(self.fieldName_)
            editor.setText(editor.text()) 
        

    """
  Para asistente de completado automático.
    """
    def setAutoCompletionMode(self, m):
        self.autoCompMode_ = m
  
    def autoCompletionMode(self):
        return autoCompMode_


    #SLOTS

    """
  Refresca el contenido del campo con los valores del cursor de la tabla origen.

  Si se indica el nombre de un campo sólo "refresca" si el campo indicado
  coincide con la propiedad fieldRelation, tomando como filtro el valor del campo
  fieldRelation de la tabla relacionada. Si no se indica nigún nombre de
  campo el refresco es llevado a cabo siempre.

  @param fN Nombre de un campo
    """
    @decorators.NotImplementedWarn
    def refresh(self, fN = None):
        if not self.cursor_:
            return
        
        tMD = FLTableMetaData(self.cursor_.metadata())
        if not tMD:
            return
        
        v = QtCore.QVariant
        null = bool
        if fN.isEmpty():
            v = self.cursor_.valueBuffer(self.fieldName_)
            null = self.cursor_.bufferIsNull(self.fieldName_)
        else:
            if not self.cursorAux and fN.lower == self.fieldRelation_.lower:
                if self.cursor_.bufferIsNull(self.fliedRelation_):
                    return
                
                mng = FLManager(self.cursor_.db().manager())
                field = FLFieldMetaData(tMD.field(self.fieldRelation_))
                tmd = mng.metadata(field.relationM1().foreingTable())
                if not tmd:
                    return
            
            if self.topWidget_ and not self.topWidget_.isShown() and not self.cursor_.modeAccess() == FLSqlCursor.INSERT:
                if tmd and not tmd.inCache():
                    tmd = None
                return
            
            if not field:
                if tmd and not tmd.inCache():
                    tmd = None
                return
            
            if not field.relationM1():
                print("FLFieldDB : El campo de la relación debe estar relacionado en M1")
                
                if tmd and not tmd.inCache():
                    tmd = None
                return
            
            v = QtCore.QVariant(self.cursor_.valueBuffer(self.fieldRelation_))
            q = FLSqlQuery(0, self.cursor_.db.connectionName())
            q.setForwardOnly(True)
            q.setTablesList(field.relationM1().foreignTable())
            q.setSelect(self.foreignField_ + "," + field.relationM1().foreignField())
            q.setFrom(field.relationM1().foreignTable())
            
            where_ = mng.formatAssignValue(field.relationM1.foreignField(), field, v, True)
            filterAc = self.cursor_.filterAssoc(self.fieldRelation_, tmd)
            
            if not filterAc.isEmpty():
                if where.isEmpty():
                    where = filterAc
                else:
                    where += " AND " + filterAc
            
            if self.filter_.isEmpty():
                q.setWhere(where)
            else:
                q.setWhere(self.filter_ + " AND " + where)
            
            if q.exec() and q.next():
                
                v0 = QtCore.QVariant(q.value(0))
                v1 = QtCore.QVariant(q.value(1))
                
                if not v0 == self.value():
                    self.setValue(v0)
                    
                if not v1 == v:
                    self.cursor_.setValueBuffer(self.fieldRelation_, v1)
            
            if tmd and tmd.inCache():
                tmd = None
        
        return
    
    field = FLFieldMetaData(tmd.field(self.fieldName_))
    if not field:
        return
    
    type_ = field.type()
    if not type_ == QtCore.QVariant.Pixmap and not self.editor_:
        return
    
    modeAccess = self.modeAccess()
    
    if not self.partDecimal_ == -1:
        partDecimal = self.partDecimal_
    else:
        partDecimal = field.partDecimal()
    
    ol = bool(field.hasOptionsList())
    fDis = (self.keepDisabled_ or self.cursor_.fieldDisabled(self.fieldName_) or (modeAccess == FLSqlCursor.EDIT and (field.isPrimaryKey() or tMD.fieldListOfCompoundKey(self.fieldName_)))
            or not field.editable() or modeAccess == FLSqlCursor.BROWSE)
    self.setDisabled(fDis)
    
    if type_ == QtCore.QVariant.Double:
        #disconnect(self.editor_, SIGNAL(textChanged(const QString &)), this,SLOT(self.updateValue(const QString &)));#FIXME
        s = QtCore.QString
        if not null:
            s.setNum(v.toDouble(),'f', partDecimal)
        self.editor_.setText(s)#::qt_cast<FLLineEdit *>(editor_)->setText(s);
        #connect(editor_, SIGNAL(textChanged(const QString &)), this,SLOT(updateValue(const QString &))); #FIXME
        
    elif type_ == QtCore.QVariant.String:
        doHome = False
        if not ol:
            doHome = self.editor_.text().isEmpty()
        
        #disconnect(editor_, SIGNAL(textChanged(const QString &)), this,SLOT(updateValue(const QString &)));  #FIXME
        if not null:
            if ol:
                self.editor_.setCurrentItem(field.optionsList().findIndex(v.toString()))
            else:
                self.editor_.setText(v.toString())#FLLineEdit
        else:
            if ol:
                self.editor_.setCurrentItem(0)#QComboBox
            else:
                self.editor_.setText(None)#FLLineEdit
        
        if not ol and doHome:
            self.editor_.home(False)#FLLineEdit
        #connect(editor_, SIGNAL(textChanged(const QString &)), this, SLOT(updateValue(const QString &)));#FIXME
        
    elif type_ == QtCore.QVariant.UInt:
        #disconnect(editor_, SIGNAL(textChanged(const QString &)), this,SLOT(updateValue(const QString &)));#FIXME
        if not null:
            s.setNum(v.toUInt())
            self.editor_.setText(s)#FLLineEdit
        #connect(editor_, SIGNAL(textChanged(const QString &)), this,SLOT(updateValue(const QString &))); #FIXME
    
    elif type_ == QtCore.QVariant.Int:
        #      disconnect(editor_, SIGNAL(textChanged(const QString &)), this,SLOT(updateValue(const QString &))); #FIXME
        if not null:
            s.setNum(v.toInt())
            self.editor_.setText(s)
        #connect(editor_, SIGNAL(textChanged(const QString &)), this,SLOT(updateValue(const QString &)));#FIXME
    
    elif type_ == FLFieldMetaData.Serial:
        #disconnect(editor_, SIGNAL(valueChanged(const QString &)), this,SLOT(updateValue(const QString &)));#FIXME
        self.editor_.setValue(0)#FLSpinBox 
        #connect(editor_, SIGNAL(valueChanged(const QString &)), this,SLOT(updateValue(const QString &)));#FIXME
    
    elif type_ == QtCore.QVariant.Pixmap:
        if not self.editorImg_:
            self.editorImg_ = FLPixmapView(self);
            self.editorImg_.setFocusPolicy(QtCore.QWidget.NoFocus)
            self.editorImg_.setSizePolicy(self.sizePolicy())
            self.editorImg_.setMaximumSize(self.initMaxSize_)
            self.editorImg_.setMinimumSize(self.initMinSize_)
            self.editorImg_.setAutoScaled(True)
            FLWidgetFieldDBLayout.addWidget(self.editorImg_)
            if field.visible():
                self.editorImg_.show()
        
        if modeAccess == FLSqlCursor.BROWSE:
            self.setDisabled(False)
        if field.visible():
            if not null:
                cs = v.toCString()
            if cs.isEmpty():
                self.editorImg_.clear()
                return
            
            pix = QtGui.QPixmap #QPixmap pix;
            if not QPixmapCache.find(cs.left(100), pix):
                pix.loadFromData(cs);
                QPixmapCache.insert(cs.left(100), pix)
            
            if not pix.isNull():
                self.editorImg_.setPixmap(pix)
            else:
                self.editorImg_.clear()
        
        if modeAccess == FLSqlCursor.BROWSE:
            self.pushButtonDB.setDisabled(True)


    elif type_ == QtCore.QVariant.Date:
        if self.cursor_.modeAccess() == FLSqlCursor.INSERT and null and not field.allowNull():
            defVal = QVariant(field.defaultValue())
            if not defVal.isValid() or defVal.isNull():
                self.editor_.setDate(QtCore.QDate.currentDate()) #FLDateEdit
            else:
                self.editor_.setDate(defVal.toDate())
        else:
            #disconnect(editor_, SIGNAL(valueChanged(const QDate &)), this,SLOT(updateValue(const QDate &)));#FIXME
            self.editor_.setDate(v.toDate())
            #connect(editor_, SIGNAL(valueChanged(const QDate &)), this,SLOT(updateValue(const QDate &)));#FIXME
    
    elif type_ == QtCore.QVariant.Time:
        if self.cursor_.modeAccess() == FLSqlCursor.INSERT and null and not field.allowNull():
            defVal = QtCore.QVariant(field.defaultValue())
            if not defVal.isValid() or defVal.isNull():
                self.editor_.setTime(QtCore.Qtime.currentTime()) #QTimeEdit
            else:
                self.editor_.setTime(defVal.toTime())#QTimeEdit
        else:
            #disconnect(editor_, SIGNAL(valueChanged(const QTime &)), this,SLOT(updateValue(const QTime &))); #FIXME
            self.editor_.setTime(v.toTime())#QTimeEdit
            #connect(editor_, SIGNAL(valueChanged(const QTime &)), this,SLOT(updateValue(const QTime &)));#FIXME
            
    elif type_ == QtCore.QVariant.StringList:
        #disconnect(editor_, SIGNAL(textChanged()), this, SLOT(updateValue())); #FIXME
        self.editor_.setText(v.toString()) #QTextEdit
        #connect(editor_, SIGNAL(textChanged()), this, SLOT(updateValue())); #FIXME
    
    elif type_ == QtCore.QVariant.Bool:
        #disconnect(editor_, SIGNAL(toggled(bool)), this, SLOT(updateValue(bool))); #FIXME
        self.editor_.setChecked(v.toBool())#QCheckBox
        #connect(editor_, SIGNAL(toggled(bool)), this, SLOT(updateValue(bool)));#FIXME
    
    if not field.visible():
        if self.editor_:
            self.editor_.hide()
        elif self.editorImg_:
            self.editorImg_.hide()
        self.setDisabled(True)


    """
  Refresco rápido
    """
    
    @decorators.NotImplementedWarn
    def refreshQuick(self, fN = None):
        
        if fN.isEmpty() or not fN == self.fieldName_ or not self.cursor_:
            return
        tMD = slef.cursor_.metadata()
        if not tMD:
            return
        field = tMD.field(self.fieldName_)
        if not field:
            return
        if field.outTransaction():
            return
        type_ = field.type()
        if not type_ == QtCore.QVariant.Pixmap and not self.editor_:
            return
        
        v = QVariant(self.cursor_.valueBuffer(self.fieldName_))
        null = self.cursor_.bufferIsNull(self.fieldName_)
        if not self.partDecimal_ == -1:
            partDecimal =  self.partDecimal_
        else:
            partDecimal = field.partDecimal()
        ol = filed.hasOptionsList()
        
        if type_ == QtCore.QVariant.Double:
            if v.toDouble() == self.editor_.text().toDouble():
                return
            #disconnect(editor_, SIGNAL(textChanged(const QString &)), this, SLOT(updateValue(const QString &))); #FIXME
            if not null:
                s.setNum(v.toDouble(),'f',partDecimal)
                self.editor_.setText(s)
            #connect(editor_, SIGNAL(textChanged(const QString &)), this, SLOT(updateValue(const QString &))); #FIXME
            
        elif type_ == QtCore.QVariant.String:
            doHome = False
            if ol:
                if v.toString() == self.editor_.currentText(): #QComboBox 
                    return
            else:
                if v.toString() == self.editor_.text():#FLLineEdit
                    return
                doHome = self.editor_.text().isEmpty()#FLLineEdit
            #disconnect(editor_, SIGNAL(textChanged(const QString &)), this,SLOT(updateValue(const QString &)));#FIXME
            if v.isValid() and not v.isNull():
                if ol:
                    self.editor_.setCurrentItem(field.optionsList().findIndex(v.toString()))#QComboBox
                else:
                    self.editor_.setText(v.toString())#FLLineEdit
            else:
                if ol:
                    self.editor_.setCurrentItem(0)#QComboBox
                else:
                    self.editor_.setText(None)
            
            if not ol and doHome:
                self.editor_.home(False)#FLLineEdit
            #connect(editor_, SIGNAL(textChanged(const QString &)), this,SLOT(updateValue(const QString &)));#FIXME
        
        elif type_ == QtCore.QVariant.UInt:
            if v.toUInt() == self.editor_.text().toUInt():  #FLLineEdit 
                return
            #disconnect(editor_, SIGNAL(textChanged(const QString &)), this,SLOT(updateValue(const QString &))); #FIXME
            
            if not null:
                s.setNum(v.toInt())
            self.editor_.setText(s)#FLLineEdit
            
            #connect(editor_, SIGNAL(textChanged(const QString &)), this, SLOT(updateValue(const QString &)));#FIXME
            
        elif type_ == QtCore.QVariant.Int:
            if v.toInt() == self.editor_.text().toInt():
                return
                       
            #disconnect(editor_, SIGNAL(textChanged(const QString &)), this, SLOT(updateValue(const QString &))); #FIXME
            s = None
            if not null:
                s.setNum(v.toInt())
            
            self.editor_.setText(s)
            #connect(editor_, SIGNAL(textChanged(const QString &)), this, SLOT(updateValue(const QString &)));#FIXME
        
        elif type_ == FLFieldMetaData.serial:
            if v.toInt() == self.editor_.value():
                return
            #disconnect(editor_, SIGNAL(valueChanged(const QString &)), this, SLOT(updateValue(const QString &)));#FIXME
            self.editor_.setValue(v.toInt())
            #connect(editor_, SIGNAL(valueChanged(const QString &)), this, SLOT(updateValue(const QString &)));#FIXME
        
        elif type_ == QtCore.QVariant.Pixmap:
            if not self.editorImg_:
                self.editorImg_ = FLPixmapView(self)
                self.editorImg_.setFocusPolicy(QtCore.QWidget.NoFocus)
                self.editorImg_.setSizePolicy(self.sizePolicy())
                self.editorImg_.setMaximumSize(self.initMaxSize_)
                self.editorImg_.setMinimumSize(self.initMinSize_)
                self.editorImg_.setAutoScaled(True)
                FLWidgetFieldDBLayout.addWidget(self.editorImg_)
                if field.visible():
                    self.editorImg_.show()
                
            cs = None
            if not null:
                cs = v.toCString()
                
            if cs.isEmpty():
                self.editorImg_.clear()
                return
                
            pix = QtCore.QPixmap
            if not QtCore.QPixmapCache.find(cs.left(100), pix):
                pix.loadFromData(cs)
                QtCore.QPixmapCache.insert(cs.left(100), pix)
                
            if pix.isNull():
                self.editorImg_.clear()
            else:
                self.editorImg_.setPixmap(pix)
            
        elif type_ == QtCore.QVariant.Date:
            if v.toDate() == self.editor_.date():
                return
            
            #disconnect(editor_, SIGNAL(valueChanged(const QDate &)), this, SLOT(updateValue(const QDate &)));#FIXME
            self.editor_.setDate(v.toDate())
            #connect(editor_, SIGNAL(valueChanged(const QDate &)), this, SLOT(updateValue(const QDate &))); #FIXME
        
        elif type_ == QtCore.QVariant.Time:
            if v.toTime() == self.editor_.time():
                return
            
            #disconnect(editor_, SIGNAL(valueChanged(const QTime &)), this,SLOT(updateValue(const QTime &)));#FIXME
            self.editor_.setTime(v.toTime())
            #connect(editor_, SIGNAL(valueChanged(const QTime &)), this, SLOT(updateValue(const QTime &)));#FIXME
        
        elif type_ == QtCore.QVariant.StringList:
            if v.toString() == self.editor_.text():
                return
            
            #disconnect(editor_, SIGNAL(textChanged()), this, SLOT(updateValue())); #FIXME
            self.editor_.setText(v.toString())
            #connect(editor_, SIGNAL(textChanged()), this, SLOT(updateValue())); #FIXME
        
        elif type_ == QtCore.QVariant.Bool:
            if v.toBool() == self.editor_.isChecked():
                return
            #disconnect(editor_, SIGNAL(toggled(bool)), this, SLOT(updateValue(bool))); #FIXME
            self.editor_.setChecked(v.toBool())
            #connect(editor_, SIGNAL(toggled(bool)), this, SLOT(updateValue(bool))); #FIXME        

    
    """
  Inicia el cursor segun este campo sea de la tabla origen o de
  una tabla relacionada
    """
    @decorators.NotImplementedWarn
    def initCursor(self):
        
        if not self.tableName_.isEmpty() and self.foreignField_.isEmpty() and self.fieldRelation_.isEmpty():
            self.cursorBackup_ = self.cursor_
            if self.cursor_:
                self.cursor_ = FLSqlCursor(self.tableName_, True, self.cursor_.db().connectionName(), 0,0, self)
            else:
                if not self.topWidget_:
                    return
                self.cursor_ = FLSqlCursor(self.tableName_, True, FLSqlConnections.database().connectionName(), 0,0, self)
            
            self.cursor_.setModeAccess(FLSqlCursor.BROWSE)
            if self.showed:
                #disconnect(cursor_, SIGNAL(cursorUpdated()), this, SLOT(refresh())); #FIXME
                #connect(cursor_, SIGNAL(cursorUpdated()), this, SLOT(refresh())); #FIXME
                return
            else:
                if self.cursorBackup_:
                    #disconnect(cursor_, SIGNAL(cursorUpdated()), this, SLOT(refresh())); #FIXME
                    self.cursor_ = self.cursorBackup_
                    self.cursorBackup_ = 0
            
            if not self.cursor_:
                return
            
            if not self.cursor_.metadata():
                return
            
            if self.tableName_.isEmpty() or self.foreignField_.isEmpty() || self.fieldRelation_.isEmpty():
                if not self.foreignField_.isEmpty() and not self.fieldRelation_.isEmpty():
                    if self.showed:
                        #disconnect(cursor_, SIGNAL(bufferChanged(const QString &)), this,SLOT(refresh(const QString &)));#FIXME
                    
                    #connect(cursor_, SIGNAL(bufferChanged(const QString &)), this, SLOT(refresh(const QString &)));#FIXME
                
                if self.showed:
                    #disconnect(cursor_, SIGNAL(newBuffer()), this, SLOT(refresh())); #FIXME
                    #disconnect(cursor_, SIGNAL(bufferChanged(const QString &)), this, SLOT(refreshQuick(const QString &))); #FIXME
                
                #connect(cursor_, SIGNAL(newBuffer()), this, SLOT(refresh())); #FIXME
                #connect(cursor_, SIGNAL(bufferChanged(const QString &)), this, SLOT(refreshQuick(const QString &))); #FIXME
                return
            
            if not self.cursorAux:
                if self.cursorAuxInit:
                    return
                
                tMD = FLTableMetaData(self.cursor_.db().manager(.metadata(self.tableName_)))
                if not tMD:
                    return
                
                #disconnect(cursor_, SIGNAL(newBuffer()), this, SLOT(refresh())); #FIXME
                #disconnect(cursor_, SIGNAL(bufferChanged(const QString &)), this, SLOT(refreshQuick(const QString &)));#FIXME
                
                self.cursorAux = self.cursor_
                curName = QString(self.cursor_.metadata().name())
                rMD = tMD.relation(self.fieldRelation_,self.foreignField_, curName)
                if not rMD:
                    checkIntegrity = bool(False)
                    testM1 = FLRelationMetaData(self.cursor_.metadata().relation(self.foreignField_, self.fieldRelation_, self.tableName_))
                    
                if testM1:    
                    if testM1.cardinality() == FLRelationMetaData.RELATION_M1:
                        checkIntegrity = True
                    else:
                        checkIntegrity = False
                
                fMD = FLFieldMetaData(tMD.field(self.fieldRelation_))
                if fMD:
                    rMD = FLRelationMetaData(curName, self.foreignField_, FLRelationMetaData.RELATION_1M, False, False, checkIntegrity)
                    fMD.addRelationMD(rMD)
                    #qWarning(tr("FLFieldDB : La relación entre la tabla del formulario ( %1 ) y la tabla ( %2 ) de este campo ( %3 ) no existe, pero sin embargo se han indicado los campos de relación( %4, %5 )").arg(curName).arg(tableName_).arg(fieldName_).arg(fieldRelation_).arg(foreignField_)); #FIXME
                    #qWarning(tr("FLFieldDB : Creando automáticamente %1.%2 --1M--> %3.%4").arg(tableName_).arg(fieldRelation_).arg(curName).arg(foreignField_)); #FIXME
                else:
                    #qWarning(tr("FLFieldDB : El campo ( %1 ) indicado en la propiedad fieldRelation no se encuentra en la tabla ( %2 )").arg(fieldRelation_).arg(tableName_)); #FIXME
            
            self.cursor_ = FLSqlCursor(self.tableName_, False, self.cursor_.db().connectionName(), self.cursorAux_, rMD, self)
            if not self.cursor_:
                self.cursor_ = self.cursorAux
                if self.showed:
                    #disconnect(cursor_, SIGNAL(newBuffer()), this, SLOT(refresh()));#FIXME
                    #disconnect(cursor_, SIGNAL(bufferChanged(const QString &)), this,SLOT(refreshQuick(const QString &)));#FIXME
                
                #connect(cursor_, SIGNAL(newBuffer()), this, SLOT(refresh()));#FIXME
                #connect(cursor_, SIGNAL(bufferChanged(const QString &)), this, SLOT(refreshQuick(const QString &)));#FIXME
                self.cursorAux = 0
                if tMD and not tMD.inCache():
                    delete tMD
                return
            else:
                if self.showed:
                    #disconnect(cursorAux, SIGNAL(newBuffer()), this, SLOT(setNoShowed())); #FIXME
                #connect(cursorAux, SIGNAL(newBuffer()), this, SLOT(setNoShowed())); #FIXME
            
            self.cursor_.setModeAccess(FLSqlCursor.BROWSE)
            if self.showed:
                #disconnect(cursor_, SIGNAL(newBuffer()), this, SLOT(refresh())); #FIXME
                #disconnect(cursor_, SIGNAL(bufferChanged(const QString &)), this,SLOT(refreshQuick(const QString &)));#FIXME
            
            #connect(cursor_, SIGNAL(newBuffer()), this, SLOT(refresh()));#FIXME
            #connect(cursor_, SIGNAL(bufferChanged(const QString &)), this,SLOT(refreshQuick(const QString &)));#FIXME
            
            self.cursorAuxInit = True;
            self.cursor_.append(self.cursor_.db.db.recordInfo(self.tableName_).find(self.fieldName_))
            self.cursor_.append(self.cursor_.db.db.recordInfo(self.tableName_).find(self.fieldRelation_))
            if tMD and not tMD.inCache():
                delete tMD
    
            
                



    """
  Crea e inicia el editor apropiado para editar el tipo de datos
  contenido en el campo (p.e: si el campo contiene una fecha crea
  e inicia un QDataEdit)
    """
    @decorators.NotImplementedWarn
    def initEditor(self):
        
        if not self.cursor_:
            return
        
        if self.editor_:
            delete self.editor_
            self.editor_ = 0
            
        if self.editorImg_:
            delete self.editorImg_
            self.editorImg_ = 0
        
        tMD = FLTableMetaData(self.cursor_.metadata())
        if not tMD:
            return
        
        field = FLFieldMetaData(tMD.field(self.fieldName_))
        if not field:
            return
        
        type_ = field.type()
        len = field.length()
        partInteger = field.partInteger()
        partDecimal = self.partDecimal_ > -1 ? self.partDecimal_ : field.partDecimal()
        rX = QtCore.QString(field.regExpValidator())
        ol = bool(field.hasOptionsList())
        
        rt = QtCore.QString()
        if field.relationM1():
            if not field.relationM1().foreignTable() == tMD.name():
                rt = field.relationM1().foreignTable()
        
        hasPushButtonDB = bool(False)
        self.fieldAlias_ = field.alias()
        
        self.textLabelDB.setFont(qApp.font())
        if self.showAlias_ and not type_ == QtCore.QVariant.Pixmap and not type_ == QtCore.QVariant.Bool:
            if self.showAlias_ and field.editable():
                textLabelDB.setText(self.fieldAlias_ + QtCora.QString.fromLatin1("*"))
            else:
                textLabelDB.setText(self.fieldAlias_)
        else:
            textLabelDb.hide()
        
        if not rt.isEmpty():
            hasPushButtonDB = bool(True)
            tmd = FLTableMetaData(self.cursor_.db().manager().metadata(rt))
            if not tmd:
                self.pushButtonDB.setDisabled(True)
            
            if tmd and not tmd.inCache():
                    delete tmd
            
        self.initMaxSize_ = self.maximumSize() 
        self.initMinSize_ = self.minimumSize()
        
        if type_ == QtCore.QVariant.UInt or type_ == QtCore.QVariant.Int or type_ == QtCore.QVariant.Double or type_ == QtCore.QVariant.String:
            if ol:
                self.editor_ = QtGui.QComboBox(True,self, "editor")
                self.editor_.setEditable(False)
                self.editor_.setAutoCompletion(True)
                self.editor_.setFont(qApp.font())
                if not self.cursor_.modeAccess() == FLSqlCursor.BROWSE:
                    if not field.allowNull():
                        self.editor_.setPaletteBackgroundColor(self.notNullColor())
                
                olTranslated = QtCore.QStringList
                olNoTranslated(field.optionsList())
                countOl = olNoTranslated.count()
                
                for i in range(countOl):
                    olTranslated.append(FLUtil.translate("MetaData", olNoTranslated[i]))
                
                this.self.editor_.insertStringList(olTranslated)
                self.editor_.installEventFilter(self)
                
                if self.showed:
                    #disconnect(editor_, SIGNAL(activated(const QString &)), this, SLOT(updateValue(const QString &)));#FIXME
                    #connect(editor_, SIGNAL(activated(const QString &)), this, SLOT(updateValue(const QString &)));#FIXME
            else:
                self.editor_ = FLLineEdit(self,"editor")
                self.editor_.setFont(qApp.font())
                self.editor_.type = type_
                self.editor_.partDecimal = partDecimal
                if not self.cursor_.modeAccess() == FLSqlCursor.BROWSE:
                    if not field.allowNull():
                        self.editor_.setPaletteBackgroundColor(self.notNullColor())
                self.editor_.installEventFilter(self)
                
                if type_ == QtCore.QVariant.Double:
                    self.editor.setValidator(FLDoubleValidator(0, pow(10,partInteger) - 1, partDecimal, self.editor_))
                    self.editor_.setAlignment(QtCore.Qt.AlignRight)
                elif type_ == QtCore.QVariant.UInt or type_ == QtCore.QVariant.Int:
                    if type_ == QtCore.QVariant.UInt:
                        self.editor_.setValidator(FLUIntValidator(0,((int) pow (10, partInteger) - 1), self.editor_))
                    else:
                        self.editor_.setValidator(FLIntValidator(((int)(pow(10, partInteger) - 1) * (-1)),((int) pow(10,partInteger) -1 ), self.editor_))
                    self.editor_.setAlignment(QtCore.Qt.AlignRight)
                
                else:
                    self.editor_.setMaxLength(len)
                    if not rX.isEmpty():
                        r = QtCore.QregExp(rX)
                        self.editor_.setValidator(QtCore.QRegExpValidator(r, self.editor_))   
                    
                    self.editor_.setAlignment(Qtcore.Qt.AlignLeft)
                    #connect(this, SIGNAL(keyF4Pressed()), this, SLOT(toggleAutoCompletion())); #FIXME
                    if self.autoCompMode_ == self.OnDemmandF4:
                        #QToolTip::add(editor_, tr("Para completado automático pulsar F4")); #FIXME
                        #QWhatsThis::add(editor_, tr("Para completado automático pulsar F4")); #FIXME
                    elif self.autoCompMode_ == self.AlwaisAuto:
                        #QToolTip::add(editor_, tr("Completado automático permanente activado")); #FIXME
                        #QWhatsThis::add(editor_, tr("Completado automático permanente activado")); #FIXME
                    else:
                        #QToolTip::add(editor_, tr("Completado automático desactivado")); #FIXME
                        #QWhatsThis::add(editor_, tr("Completado automático desactivado")); #FIXME
            
                if self.showed:
                    #disconnect(editor_, SIGNAL(lostFocus()), this, SLOT(emitLostFocus())); #FIXME
                    #disconnect(editor_, SIGNAL(textChanged(const QString &)), this, SLOT(updateValue(const QString &))); #FIXME
                    #disconnect(editor_, SIGNAL(textChanged(const QString &)), this, SLOT(emitTextChanged(const QString &)));#FIXME
            
                #connect(editor_, SIGNAL(lostFocus()), this, SLOT(emitLostFocus())); #FIXME
                #connect(editor_, SIGNAL(textChanged(const QString &)), this, SLOT(updateValue(const QString &))); #FIXME
                #connect(editor_, SIGNAL(textChanged(const QString &)), this, SLOT(emitTextChanged(const QString &))); #FIXME
            
                if hasPushButtonDB:
                    if self.showed:
                        #disconnect(this, SIGNAL(keyF2Pressed()), pushButtonDB, SLOT(animateClick())); #FIXME
                        #disconnect(this, SIGNAL(labelClicked()), this, SLOT(openFormRecordRelation())); #FIXME
                
                    #connect(this, SIGNAL(keyF2Pressed()), pushButtonDB, SLOT(animateClick())); #FIXME
                    #connect(this, SIGNAL(labelClicked()), this, SLOT(openFormRecordRelation())); #FIXME
                    self.textLabelDB.installEventFilter(self)
                    tlF = self.textLabelDB.font()
                    tlF.setUnderLine(True)
                    self.textLabelDB.setFont(tlF)
                    cB = Qcore.QColor("blue")
                    self.textLabelDB.setPaletteForegroundColor(cB)
                    #self.textLabelDB.setCursor(QCursor::PointingHandCursor) #FIXME
        
            self.editor_.setSizePolicy(QtCore.QSizePolicy((QtCore.QSizePolicy.SizeType) 7, (QtCore.QSizePolicy.SizeType) 0, self.editor_.sizePolizy().hasHeightForWidth()))
            self.FLWidgetFieldDBLayout.addWidget(self.editor_)
        
        if (type_ == FLFieldMetaData.Serial):
            self.editor_ = FLSpinBox(self,"editor")
            self.editor_.setFont(qApp.font())
            self.editor_.setMaxValue(((int) pow(10, partIntger) - 1))
            self.editor_.setSizePolicy(QtCore.QSizePolicy((QtCore.QsizePolicy.SizeType) 7, (QtCore.QSizePolicy.SizeType) 0, self.editor_.sizePolicy().hesHeightForWidth()))
            self.FLWidgetFieldDBLayout.addWidget(self.editor_)
            self.editor_.installEventFilter(self)
            
            if self.showed:
                #disconnect(editor_, SIGNAL(valueChanged(const QString &)), this, SLOT(updateValue(const QString &)));#FIXME
                #connect(editor_, SIGNAL(valueChanged(const QString &)), this, SLOT(updateValue(const QString &))); #FIXME
                
            
        if type_ == QtCore.QVariant.Pixmap:
            if not self.cursor_.modeAccess() == FLSqlCursor.BROWSE:
                self.FLWidGetFieldDBLayout.setDirection(QtGui.QBoxLayout.Down)
                self.editorImg_ = FLPixmapView(self)
                self.editorImg_.setFocusPolicy(QtGui.QWidget.NoFocus)
                self.editorImg_.setSizePolicy(self.sizePolicy())
                self.editorImg_.setMaximumSize(self.initMaxSize_)
                self.editorImg_.setMinimumSize(self.initMinSize_)
                self.editorImg_.setAutoScaled(True)    
                self.FLWidGetFieldDBLayout.addWidget(self.editorImg_)
                
                if not self.pbAux3_:
                    spcBut = QtGui.QSpacerItem(20, 20,QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
                    self.lytButtons.addItem(spcBut)
                    self.pbAux3_ = QtGui.QPushButton(self, "pbAux3")
                    self.pbAux3_.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePloicy.Fixed, QtGui.QSizePloicy.Fixed, self.pbAux3_.sizePolicy().hasHeightForWidth() ))
                    self.pbAux3_.setMinimumSize(QtGui.Qsize(22, 22))
                    self.pbAux3_.setFocusPolicy(QtGui.QPushButton.NoFocus)
                    self.pbAux3_.setIconSet(QtGui.QIconSet(QtGui.QPixmap.fromMineSource("file_open.png")))
                    self.pbAux3_.setText(QtCore.QString(""))
                    #QToolTip::add(pbAux3_, tr("Abrir fichero de imagen")); #FIXME
                    #QWhatsThis::add(pbAux3_, tr("Abrir fichero de imagen")); #FIXME
                    self.lytButtons.addWidget(self.pbAux3_)
                    if self.showed:
                        # disconnect(pbAux3_, SIGNAL(clicked()), this, SLOT(searchPixmap())); #FIXME
                    #connect(pbAux3_, SIGNAL(clicked()), this, SLOT(searchPixmap())); #FIXME
                    
                    if not hasPushButtonDB:
                        if self.showed:
                            #disconnect(this, SIGNAL(keyF2Pressed()), pbAux3_, SLOT(animateClick())); #FIXME
                        #connect(this, SIGNAL(keyF2Pressed()), pbAux3_, SLOT(animateClick())); #FIXME
                        self.pbAux3_.setFocusPolicy(QtGui.QPushButton.StringFocus)
                        self.pbAux3_.installEventFilter(self)
                
                if not self.pbAux4_:
                    self.pbAux4_ = Qtgui.QPushButton(self, "pbAux4")
                    self.pbAux4_.setSizePolicy(QtGui.QSizePolicy(QtGui.QsizePolicy.Fixed, QtGui.QSizePolicy.Fixed, self.pbAux4_.sizePolicy().hasHeightForWidth()))
                    self.pbAux4_.setMinimumSize(QtGui.Qsize(22, 22))
                    self.pbAux4_.setFocusPolicy(QtGui.QPushButton.NoFocus)
                    self.pbAux4_.setIconSet(QtGui.QIconSet(QtGui.QPixmap.fromMineSource("paste.png")))
                    self.pbAux4_.setText(QtCore.QString(""))
                    #QToolTip::add(pbAux4_, tr("Pegar imagen desde el portapapeles")); #FIXME
                    #QWhatsThis::add(pbAux4_, tr("Pegar imagen desde el portapapeles")); #FIXME
                    self.lytButtons.addWidget(self.pbAux4_)
                    if self.showed:
                        #disconnect(pbAux4_, SIGNAL(clicked()), this, SLOT(setPixmapFromClipboard())); #FIXME
                    #connect(pbAux4_, SIGNAL(clicked()), this, SLOT(setPixmapFromClipboard())); #FIXME
                
                if not self.pbAux_:
                    self.pbAux_ = Qtgui.QPushButton(self, "pbAux")
                    self.pbAux_.setSizePolicy(QtGui.QSizePolicy(QtGui.QsizePolicy.Fixed, QtGui.QSizePolicy.Fixed, self.pbAux_.sizePolicy().hasHeightForWidth()))
                    self.pbAux_.setMinimumSize(QtGui.Qsize(22, 22))
                    self.pbAux_.setFocusPolicy(QtGui.QPushButton.NoFocus)
                    self.pbAux_.setIconSet(QtGui.QIconSet(QtGui.QPixmap.fromMineSource("eraser.png")))
                    self.pbAux_.setText(QtCore.QString(""))
                    #QToolTip::add(pbAux_, tr("Borrar imagen"));#FIXME
                    #QWhatsThis::add(pbAux_, tr("Borrar imagen")); #FIXME
                    self.lytButtons.addWidget(self.pbAux_)
                    if self.showed:
                        #disconnect(pbAux_, SIGNAL(clicked()), this, SLOT(clearPixmap())); #FIXME
                    #connect(pbAux_, SIGNAL(clicked()), this, SLOT(clearPixmap())); #FIXME
                
                if not self.pbAux2_:
                    self.pbAux2_ = Qtgui.QPushButton(self, "pbAux2")
                    savepixmap = QtGui.QMenuBar()
                    for id in range(fmt):
                        savepixmap.addMenu(fmt(i))
                    self.pbAux2_.setPopup(savepixmap)
                    self.pbAux2_.setSizePolicy(QtGui.QSizePolicy(QtGui.QsizePolicy.Fixed, QtGui.QSizePolicy.Fixed, self.pbAux2_.sizePolicy().hasHeightForWidth()))
                    self.pbAux2_.setMinimumSize(QtGui.Qsize(22, 22))
                    self.pbAux2_.setFocusPolicy(QtGui.QPushButton.NoFocus)
                    self.pbAux2_.setIconSet(QtGui.QIconSet(QtGui.QPixmap.fromMineSource("filesaveas.png")))
                    self.pbAux2_.setText(QtCore.QString(""))
                    #QToolTip::add(pbAux2_, tr("Guardar imagen como..."));#FIXME
                    #QWhatsThis::add(pbAux_, tr("Guardar imagen como..")); #FIXME
                    self.lytButtons.addWidget(self.pbAux2_)
                    if self.showed:
                        # disconnect(savepixmap, SIGNAL(activated(int)), this, SLOT(savePixmap(int))); #FIXME
                    #connect(savepixmap, SIGNAL(activated(int)), this, SLOT(savePixmap(int))); #FIXME
                
                if hasPushButtonDB:
                    self.pushButtonDB.installEventFilter(self)
                
               
        if type_ == QtCore.QVariant.Date:
            self.editor_ = FLDateEdit(self,"editor")
            self.editor_.setFont(qApp.font())
            self.editor_.setSizePolicy(QtGui.QSizePolicy((QtGui.QSizePolicy.SizeType) 7, (QtGui.QSizePolicy.SizePolicy.SizeType) 0, self.editor_.sizePolicy().hasHeightForWidth()))
            self.FLWidgetFieldDBLayout.insertWidget(1, self.editor_)
            self.editor_.setOrder(QtGui.QDateEdit.DMY)
            self.editor_.setAutoAdvance(True)
            self.editor_.setSeparator("-")
            self.editor_.installEventFilter(self)
            
            if not self.cursor_.modeAccess() == FLSqlCursor.BROWSE:
                if not self.pbAux_:
                    self.pbAux_ = QtGui.QPushButton(self,"pbAux")
                    self.pbAux_.setFlat(True)
                    self.pbAux_.setSizePolicy(QtGui.QSizePolicy((QtGui.QSizePolicy.SizeType) 7, (QtGui.QSizePolicy.SizePolicy.SizeType) 0, self.pbAux_.sizePolicy().hasHeightForWidth()))           
                    self.pbAux_.setMinimumSize(QtGui.QSize(25, 25))
                    self.pbAux_.setFocusPolicy(QtGui.QSize(25, 25))
                    self.pbAux_.setIconSet(QtGui.QIconSet(QtGui.QPixmap.fromMineSource("date.png")))
                    self.pbAux_.setText(QtCore.QString(""))
                    #QToolTip::add(pbAux_, tr("Seleccionar fecha (F2)")); #FIXME
                    #QWhatsThis::add(pbAux_, tr("Seleccionar fecha (F2)")); #FIXME
                    self.lytButtons.addWidget(self.pbAux_)
                    if self.showed:
                        #disconnect(pbAux_, SIGNAL(clicked()), this, SLOT(toggleDatePicker())); #FIXME
                        # disconnect(this, SIGNAL(keyF2Pressed()), pbAux_, SLOT(animateClick())); #FIXME
                    
                    #connect(pbAux_, SIGNAL(clicked()), this, SLOT(toggleDatePicker())); #FIXME
                    #connect(this, SIGNAL(keyF2Pressed()), pbAux_, SLOT(animateClick())); #FIXME
            
            if self.showed:
                #disconnect(editor_, SIGNAL(valueChanged(const QDate &)), this, SLOT(updateValue(const QDate &)));#FIXME
            #connect(editor_, SIGNAL(valueChanged(const QDate &)), this, SLOT(updateValue(const QDate &))); #FIXME
            if self.cursor_,modeAccess() == FLSqlCursor.INSERT and not field.allowNull():
                defVal = QtCore.QVarinat(field.defaultValue())
                if not defVal.isValid() or defVal.isNull():
                    self.editor_.setDate(QtCore.QDate.currentDate())
                else:
                    self.editor_.setDate(defVal.toDate())
        
        if type_ == QtCore.QVariant.Time:
            self.editor_ = QtGui.QTimeEdit(self, "editor")
            self.editor_.setFont(qApp.font())
            self.editor_.setAutoAdvance(True)
            self.editor_.setSizePolicy(QtGui.QSizePlicy((QtGui.QSizePolicy.SizeType) 7,(QtGui.QSizePolicy.SizePolicy) 0, self.editor_.sizePolicy().hasHeightForWidth()))
            self.FLWidgetFieldDBLayout.addWidget(self.editor_)
            self.editor_.installEventFilter(self)
            
            if self.showed:
                #disconnect(editor_, SIGNAL(valueChanged(const QTime &)), this, SLOT(updateValue(const QTime &))); #FIXME
            
            #connect(editor_, SIGNAL(valueChanged(const QTime &)), this, SLOT(updateValue(const QTime &))); #FIXME
            if self.cursor_.modeAccess() == FLSqlCursor.INSERT and not field.allowNull():
                defVal = QtCore.QVariant(field.defaultValue())
                if not defVal.isValid() or defVal.isNull():
                    self.editor_.setTime(QtCore.Qtime.currentTime())
                else:
                    self.editor_.setTime(defVal.toTime())
        
        if type_ == QtCore.QVariant.StringList:
            ted = QtGui.QTextEdit(self,"editor")
            self.editor_ = ted
            
            ted.setFont(qApp.font())
            ted.setTabChangesFocus(True)
            self.editor_.setSizePolicy(QtGui.QSizePlicy((QtGui.QSizePolicy.SizeType) 7,(QtGui.QSizePolicy.SizePolicy) 0, self.editor_.sizePolicy().hasHeightForWidth()))
            ted.setTextFormat(self.textFormat_)
            
            if self.textFormat_ == QtCore.Qt.RichText and not self.cursor_.modeAccess() == FLSqlCursor.BROWSE:
                self.FLWidgetFieldDBLayout.setDirection(QtGui.QBoxLayout.Down)
                self.FLWidgetFieldDBLayout.remove(self.textLabelDB)
                textEditTab_  = AQTextEditBar(self, "texEditTab_", self.textLabelDB)
                texEditTab_.doConnections(ted)
                self.FLWidgetFieldDBLayout.addWidget(texEditTab_)
            
            self.FLWidgetFieldDBLayout.addWidget(self.editor_)
            self.editor_.installEventFilter(self)
            
            if self.showed:
                #disconnect(editor_, SIGNAL(textChanged()), this, SLOT(updateValue())); #FIXME
            #connect(editor_, SIGNAL(textChanged()), this, SLOT(updateValue())); #FIXME
            # connect(this, SIGNAL(keyF4Pressed()), this, SLOT(toggleAutoCompletion())); #FIXME
            if self.autoCompMode_ == self.OnDemmandF4:
                #QToolTip::add(editor_, tr("Para completado automático pulsar F4")); #FIXME
                #QWhatsThis::add(editor_, tr("Para completado automático pulsar F4")); #FIXME
            elif self.autoCompMode_ == self.AlwaisAuto:
                #QToolTip::add(editor_, tr("Completado automático permanente activado")); #FIXME
                #QWhatsThis::add(editor_, tr("Completado automático permanente activado")); #FIXME
            else:
                #QToolTip::add(editor_, tr("Completado automático desactivado")); #FIXME
                #QWhatsThis::add(editor_, tr("Completado automático desactivado")); #FIXME
            
        if type_ == QtCore.QVariant.Bool:
            self.editor_ = QtGui.QCheckBox(self,"editor")
            self.editor_.setText(tMD.fieldNameToAlias(self.fieldName_))
            self.editor_.setFont(qApp.font())
            self.editor_.installEventFilter(self)
            #self.editor_.setMinimumWidth(fontMetrics().width(tMD->fieldNameToAlias(fieldName_)) + fontMetrics().maxWidth() * 2);)#FIXME
            self.editor_.setSizePolicy(QtGui.QSizePlicy((QtGui.QSizePolicy.SizeType) 7,(QtGui.QSizePolicy.SizePolicy) 0, self.editor_.sizePolicy().hasHeightForWidth()))
            self.FLWidgetFieldDBLayout.addWidget(self.editor_)
            
            if self.showed:
                #disconnect(editor_, SIGNAL(toggled(bool)), this, SLOT(updateValue(bool)));#FIXME
            #connect(editor_, SIGNAL(toggled(bool)), this, SLOT(updateValue(bool))); #FIXME
        
        if self.editor_:
            self.editor_.setFocusPolicy(QtGui.QWidget.StrongFocus)
            self.setFocusProxy(self.editor_)
            self.setTabOrder(self.pushButtonDB, self.editor_)
            if hasPushButtonDB:
                self.pushButtonDB.setFocusPolicy(QtGui.QWidget.NoFocus)
                #QToolTip::add(editor_, tr("Para buscar un valor en la tabla relacionada pulsar F2")); #FIXME
                #QWhatsThis::add(editor_, tr("Para buscar un valor en la tabla relacionada pulsar F2")); #FIXME
        elif self.editorImg_:
            self.editorImg_.setFocusPolicy(QtGui.QWidget.NoFocus)
            if hasPushButtonDB:
                self.pushButtonDB.setFocusPolicy(QtGui.QWidget.StrongFocus)
        
        if not hasPushButtonDB:
            self.pushButtonDB.hide()
        
        if self.initMaxSize.width() < 80:
            self.setShowEditor(False)
        else:
            self.setShowEditor(self.showEditor_)


    """
  Actualiza el valor del campo con una cadena de texto.

  @param t Cadena de texto para actualizar el campo
    """
    @decorators.NotImplementedWarn
    def updateValue(self, t):

    """
    {
  if (!cursor_)
    return;

  FLTableMetaData *tMD = cursor_->metadata();
  if (!tMD)
    return;
  FLFieldMetaData *field = tMD->field(fieldName_);
  if (!field)
    return;

  bool ol = field->hasOptionsList();
  QString tAux(t);

  if (ol && editor_)
    tAux = field->optionsList()[::qt_cast<QComboBox *>(editor_)->currentItem()];

  if (!cursor_->bufferIsNull(fieldName_)) {
    if (tAux == cursor_->valueBuffer(fieldName_).toString()) {
      return;
    }
  } else if (tAux.isEmpty())
    return;

  QString s(tAux);
  if (field->type() == QVariant::String && !ol) {
    if (s.startsWith(" ")) {
      disconnect(cursor_, SIGNAL(bufferChanged(const QString &)), this,
                 SLOT(refreshQuick(const QString &)));
      cursor_->setValueBuffer(fieldName_, s.remove(0, 1));
      connect(cursor_, SIGNAL(bufferChanged(const QString &)), this,
              SLOT(refreshQuick(const QString &)));
      return;
    }
    s.remove("\\");
    s.replace("'", "\'");
  }

  if (editor_ && (field->type() == QVariant::Double ||
                  field->type() == QVariant::Int ||
                  field->type() == QVariant::UInt)) {
    s = ::qt_cast<FLLineEdit *>(editor_)->text();
  }

  if (s.isEmpty())
    cursor_->setValueBuffer(fieldName_, QVariant());
  else
    cursor_->setValueBuffer(fieldName_, s);

  if (isVisible() && hasFocus() && field->type() == QVariant::String &&
      field->length() == s.length())
    focusNextPrevChild(true);
}
  Actualiza el valor del campo con una fecha.

  @param d Fecha para actualizar el campo
    """
    @decorators.NotImplementedWarn
    def updateValue(self, d):
        if not self.cursor_:
            return 
        isNull = bool( not d.isValid() or d.isNull())
        if self.cursor_.bufferIsNull(self.fieldName_):
            if d == self.cursor_.valueBuffer(self.fieldName_).toDate():
                return
        elif isNull:
            return
        if isNull:
            self.cursor_.setValueBuffer(self.fieldName_,QtCore.QDate())
        else:
            self.cursor_.setValueBuffer(self.fieldName_, d)
        

    """
  Actualiza el valor del campo con una hora.

  @param t Hora para actualizar el campo
    """
    @decorators.NotImplementedWarn
    def updateValue(self,QCore.QTime t):
        if not self.cursor_:
            return 
        isNull = bool( not t.isValid() or t.isNull())
        if self.cursor_.bufferIsNull(self.fieldName_):
            if t == self.cursor_.valueBuffer(self.fieldName_).toTime():
                return
        elif isNull:
            return
        if isNull:
            self.cursor_.setValueBuffer(self.fieldName_,QtCore.QTime())
        else:
            self.cursor_.setValueBuffer(self.fieldName_, t)
             

    """
  Actualiza el valor del campo con un valor logico.

  @param b Valor logico para actualizar el campo
    """
    @decorators.NotImplementedWarn
    def updateValue(self,bool b):
        if not self.cursor_:
            return
        if not self.cursor_.bufferIsNull(self.fieldName_):
            if b == self.cursor_.valueBuffer(self.fieldName_).toBool():
                return
        self.cursor_.setValueBuffer(self.fieldName_, QtCore.QVariant(b, 0))
    """
  Actualiza el valor del campo con un texto, si el componente
  es del tipo QTextEdit
    """
    @decorators.NotImplementedWarn
    def updateValue(self):

    """
    {
  if (!cursor_)
    return;
  QTextEdit *ted = ::qt_cast<QTextEdit *>(editor_);
  if (!ted)
    return;
  QString t(ted->text());
  if (!cursor_->bufferIsNull(fieldName_)) {
    if (t == cursor_->valueBuffer(fieldName_).toString())
      return;
  } else if (t.isEmpty())
    return;
  t.remove("\\");
  t.replace("'", "\'");
  if (t.isEmpty())
    cursor_->setValueBuffer(fieldName_, QVariant());
  else
    cursor_->setValueBuffer(fieldName_, t);
}
  Muestra/Oculta el seleccionador de fechas.
    """
    @decorators.NotImplementedWarn
    def toggleDatePicker(self):

    """
    {
  if (!dateFrame_) {
    dateFrame_ = new QVBox(this, "dateFrame", WType_Popup);
    dateFrame_->setFrameStyle(QFrame::PopupPanel | QFrame::Raised);
    dateFrame_->setFixedSize(200, 200);
    dateFrame_->setLineWidth(3);
    dateFrame_->hide();
    if (!datePopup_) {
      datePopup_ = new VDatePopup(dateFrame_, QDate::currentDate());
      connect(datePopup_, SIGNAL(dateSelected(const QDate &)), ::qt_cast<FLDateEdit *>(editor_),
              SLOT(setDate(const QDate &)));
    }
  }

  if (!datePickerOn_) {
    QPoint tmpPoint = mapToGlobal(pbAux_->geometry().bottomRight());
    dateFrame_->setGeometry(tmpPoint.x() - 207, tmpPoint.y(), 200, 200);
    QDate date = ::qt_cast<FLDateEdit *>(editor_)->date();
    if (date.isValid()) {
      datePopup_->setDate(date);
    } else {
      datePopup_->setDate(QDate::currentDate());
    }
    datePickerOn_ = true;
    dateFrame_->show();
  }

  if (!dateFrame_->isVisible())
    datePickerOn_ = false;
}
  Borra imagen en campos tipo Pixmap.
    """
    @decorators.NotImplementedWarn
    def clearPixmap(self):

    """
    {
  if (editorImg_) {
    editorImg_->clear();
    cursor_->setValueBuffer(fieldName_, QVariant());
  }
}
  Guarda imagen en campos tipo Pixmap.

  @param fmt Indica el formato con el que guardar la imagen
    """
    @decorators.NotImplementedWarn
    self savePixmap(self, f):

    """
{
  if (editorImg_) {
    QStrList fmtl = QImage::outputFormats();
    const char *fmt = fmtl.at(f);
    QString ext = QString(fmt).lower();
    QString filename = "imagen." + ext;
    QString savefilename = QFileDialog::getSaveFileName(filename.lower(), "*." + ext, this,
                                                        filename, tr("Guardar imagen como"));
    if (!savefilename.isEmpty()) {
      QPixmap pix;
      QApplication::setOverrideCursor(waitCursor);
      pix.loadFromData(value().toCString());
      if (!pix.isNull())
        if (!pix.save(savefilename, fmt))
          QMessageBox::warning(this, tr("Error"), tr("Error guardando fichero"));
      QApplication::restoreOverrideCursor();
    }
  }
}
  Muestra/Oculta el asistente de completado automático.
    """
    @decorators.NotImplementedWarn
    self toggleAutoCompletion(self):

    """
{
  if (autoCompMode_ == NeverAuto)
    return;

  if (!autoComFrame_ && cursor_) {
    autoComFrame_ = new QVBox(this, "autoComFrame", WType_Popup);
    autoComFrame_->setFrameStyle(QFrame::PopupPanel | QFrame::Raised);
    autoComFrame_->setLineWidth(1);
    autoComFrame_->hide();

    if (!autoComPopup_) {
      FLTableMetaData *tMD = cursor_->metadata();
      FLFieldMetaData *field = tMD ? tMD->field(fieldName_) : 0;

      if (field) {
        autoComPopup_ = new FLDataTable(autoComFrame_, "autoComPopup", true);
        FLSqlCursor *cur;

        if (!field->relationM1()) {
          if (!fieldRelation_.isEmpty() && !foreignField_.isEmpty()) {
            autoComFieldName_ = foreignField_;

            FLFieldMetaData *fRel = tMD ? tMD->field(fieldRelation_) : 0;
            if (!fRel) {
              return;
            }
            autoComFieldRelation_ = fRel->relationM1()->foreignField();
            cur = new FLSqlCursor(fRel->relationM1()->foreignTable(), false,
                                  cursor_->db()->connectionName(), 0, 0, autoComFrame_);
            tMD = cur->metadata();
            field = tMD ? tMD->field(autoComFieldName_) : field;
          } else {
            autoComFieldName_ = fieldName_;
            autoComFieldRelation_ = QString::null;
            cur = new FLSqlCursor(tMD->name(), false, cursor_->db()->connectionName(), 0, 0,
                                  autoComFrame_);
          }
        } else {
          autoComFieldName_ = field->relationM1()->foreignField();
          autoComFieldRelation_ = QString::null;
          cur = new FLSqlCursor(field->relationM1()->foreignTable(), false,
                                cursor_->db()->connectionName(), 0, 0, autoComFrame_);
          tMD = cur->metadata();
          field = tMD ? tMD->field(autoComFieldName_) : field;
        }

        cur->append(QSqlFieldInfo(autoComFieldName_, FLFieldMetaData::flDecodeType(field->type()),
                                  -1, field->length(), -1));

        QStringList fieldsNames = QStringList::split(',', tMD->fieldsNames());
        for (QStringList::Iterator it = fieldsNames.begin(); it != fieldsNames.end(); ++it) {
          if (!cur->QSqlCursor::field((*it))) {
            field = tMD->field(*it);
            if (field)
              cur->append(QSqlFieldInfo(field->name(),
                                        FLFieldMetaData::flDecodeType(field->type()), -1,
                                        field->length(), -1, QVariant(), 0, true));
          }
        }

        if (!autoComFieldRelation_.isEmpty() && topWidget_) {
          QObjectList *l = static_cast<QObject *>(topWidget_)->queryList("FLFieldDB");
          QObjectListIt itf(*l);
          FLFieldDB *fdb = 0;
          while ((fdb = static_cast<FLFieldDB *>(itf.current())) != 0) {
            ++itf;
            if (fdb->fieldName() == autoComFieldRelation_)
              break;
          }
          delete l;

          if (fdb && !fdb->filter().isEmpty())
            cur->setMainFilter(fdb->filter());
        }
        autoComPopup_->setFLSqlCursor(cur);
        autoComPopup_->setTopMargin(0);
        autoComPopup_->setLeftMargin(0);
        autoComPopup_->horizontalHeader()->hide();
        autoComPopup_->verticalHeader()->hide();

        connect(cur, SIGNAL(newBuffer()), this, SLOT(autoCompletionUpdateValue()));
        connect(autoComPopup_, SIGNAL(recordChoosed()), this, SLOT(autoCompletionUpdateValue()));
      }
    }
  }

  if (autoComPopup_) {
    FLSqlCursor *cur = autoComPopup_->cursor();
    FLTableMetaData *tMD = cur->metadata();
    FLFieldMetaData *field = tMD ? tMD->field(autoComFieldName_) : 0;

    if (field) {
      QString filter(cursor_->db()->manager()->formatAssignValueLike(field, value(), true));
      cur->setFilter(filter);
      autoComPopup_->setFilter(filter);
      autoComPopup_->setSort(QStringList() << autoComFieldName_ + " ASC");
      autoComPopup_->QDataTable::refresh();
    }

    if (!autoComFrame_->isVisible() && cur->size() > 1) {
      QPoint tmpPoint;
      if (showAlias_)
        tmpPoint = mapToGlobal(textLabelDB->geometry().bottomLeft());
      else if (pushButtonDB && pushButtonDB->isShown())
        tmpPoint = mapToGlobal(pushButtonDB->geometry().bottomLeft());
      else
        tmpPoint = mapToGlobal(editor_->geometry().bottomLeft());
      int frameWidth = width();
      if (frameWidth < autoComPopup_->width())
        frameWidth = autoComPopup_->width();
      if (frameWidth < autoComFrame_->width())
        frameWidth = autoComFrame_->width();
      autoComFrame_->setGeometry(tmpPoint.x(), tmpPoint.y(), frameWidth, 300);
      autoComFrame_->show();
      autoComFrame_->setFocus();
    } else if (autoComFrame_->isVisible() && cur->size() == 1)
      autoComFrame_->hide();

    cur->first();
  }
}
  Actualiza el valor del campo a partir del contenido que
  ofrece el asistente de completado automático.
    """
    @decorators.NotImplementedWarn
    self autoCompletionUpdateValue(self):
    """
    {
  if (!autoComPopup_ || !autoComFrame_)
    return;

  FLSqlCursor *cur = autoComPopup_->cursor();
  if (!cur || !cur->isValid())
    return;

  if (::qt_cast<FLDataTable *>(sender())) {
    setValue(cur->valueBuffer(autoComFieldName_));
    autoComFrame_->hide();
#ifdef Q_OS_WIN32
    if (editor_)
      editor_->releaseKeyboard();
    if (autoComPopup_)
      autoComPopup_->releaseKeyboard();
#endif
  } else if (::qt_cast<QTextEdit *>(editor_)) {
    setValue(cur->valueBuffer(autoComFieldName_));
  } else {
    FLLineEdit *ed = ::qt_cast<FLLineEdit *>(editor_);
    if (autoComFrame_->isVisible() && !ed->hasFocus()) {
      if (!autoComPopup_->hasFocus()) {
        QString cval(cur->valueBuffer(autoComFieldName_).toString());
        QString val(ed->text());
        ed->autoSelect = false;
        ed->setText(cval);
        ed->QLineEdit::setFocus();
        ed->setCursorPosition(cval.length());
        ed->cursorBackward(true, cval.length() - val.length());
#ifdef Q_OS_WIN32
        ed->grabKeyboard();
#endif
      } else {
        setValue(cur->valueBuffer(autoComFieldName_));
      }
    } else if (!autoComFrame_->isVisible()) {
      QString cval(cur->valueBuffer(autoComFieldName_).toString());
      QString val(ed->text());
      ed->autoSelect = false;
      ed->setText(cval);
      ed->QLineEdit::setFocus();
      ed->setCursorPosition(cval.length());
      ed->cursorBackward(true, cval.length() - val.length());
    }
  }
  if (!autoComFieldRelation_.isEmpty() && !autoComFrame_->isVisible()) {
    cursor_->setValueBuffer(fieldRelation_, cur->valueBuffer(autoComFieldRelation_));
  }
}
"""


    #public slots:

    """
  Abre un formulario de edición para el valor seleccionado en su acción correspondiente
    """
    @decorators.NotImplementedWarn
    def openFormRecordRelation(self):
"""
{
  if (!cursor_)
    return;

  if (fieldName_.isEmpty())
    return;
  FLTableMetaData *tMD = cursor_->metadata();
  if (!tMD)
    return;

  FLFieldMetaData *field = tMD->field(fieldName_);
  if (!field)
    return;

  if (!field->relationM1()) {
#ifdef FL_DEBUG
    qWarning("FLFieldDB : " + tr("El campo de búsqueda debe tener una relación M1"));
#endif
    return;
  }

  FLSqlCursor *c = 0;
  FLFieldMetaData *fMD = field->associatedField();
  FLAction *a = 0;

  QVariant v(cursor_->valueBuffer(field->name()));
  if (v.toString().isEmpty() || (fMD && cursor_->bufferIsNull(fMD->name()))) {
    QMessageBox::warning(qApp->focusWidget(), tr("Aviso"),
                         tr("Debe indicar un valor para %1").arg(field->alias()), QMessageBox::Ok,
                         0, 0);
    return;
  }
  FLManager *mng = cursor_->db()->manager();
  c = new FLSqlCursor(field->relationM1()->foreignTable(), true, cursor_->db()->connectionName());
  c->select(mng->formatAssignValue(field->relationM1()->foreignField(), field,
                                   v, true));
  if (c->size() <= 0)
    return;
  c->next();

  if (actionName_.isEmpty())
    a = mng->action(field->relationM1()->foreignTable());
  else
    a = mng->action(actionName_);

  c->setAction(a);

  int modeAccess = cursor_->modeAccess();
  if (modeAccess == FLSqlCursor::INSERT || modeAccess == FLSqlCursor::DEL)
    modeAccess = FLSqlCursor::EDIT;
  c->openFormInMode(modeAccess, false);
}
"""

    """
  Abre un dialogo para buscar en la tabla relacionada
    """
    @decorators.NotImplementedWarn
    def searchValue(self):
"""
{
  if (!cursor_)
    return;

  if (fieldName_.isEmpty())
    return;
  FLTableMetaData *tMD = cursor_->metadata();
  if (!tMD)
    return;
  FLFieldMetaData *field = tMD->field(fieldName_);
  if (!field)
    return;

  if (!field->relationM1()) {
#ifdef FL_DEBUG
    qWarning("FLFieldDB : " + tr("El campo de búsqueda debe tener una relación M1"));
#endif
    return;
  }

  FLFormSearchDB *f = 0;
  FLSqlCursor *c = 0;
  FLFieldMetaData *fMD = field->associatedField();
  FLAction *a = 0;

  if (fMD) {
    if (!fMD->relationM1()) {
#ifdef FL_DEBUG
      qWarning("FLFieldDB : " + tr("El campo asociado debe tener una relación M1"));
#endif
      return;
    }

    QVariant v(cursor_->valueBuffer(fMD->name()));
    if (v.toString().isEmpty() || cursor_->bufferIsNull(fMD->name())) {
      QMessageBox::warning(qApp->focusWidget(), tr("Aviso"),
                           tr("Debe indicar un valor para %1").arg(fMD->alias()), QMessageBox::Ok,
                           0, 0);
      return;
    }
    FLManager *mng = cursor_->db()->manager();
    c = new FLSqlCursor(fMD->relationM1()->foreignTable(), true, cursor_->db()->connectionName());
    c->select(mng->formatAssignValue(fMD->relationM1()->foreignField(), fMD,
                                     v, true));
    if (c->size() > 0)
      c->next();

    if (actionName_.isEmpty())
      a = mng->action(field->relationM1()->foreignTable());
    else {
      a = mng->action(actionName_);
      a->setTable(field->relationM1()->foreignTable());
    }

    f = new FLFormSearchDB(c, a->name(), topWidget_);
  } else {
    FLManager *mng = cursor_->db()->manager();
    if (actionName_.isEmpty()) {
      a = mng->action(field->relationM1()->foreignTable());
      if (!a)
        return;
    } else {
      a = mng->action(actionName_);
      if (!a)
        return;
      a->setTable(field->relationM1()->foreignTable());
    }

    c = new FLSqlCursor(a->table(), true, cursor_->db()->connectionName());
    f = new FLFormSearchDB(c, a->name(), topWidget_);
  }

  f->setMainWidget();

  QObjectList *lObjs = f->queryList("FLTableDB");
  QObject *obj = lObjs->first();
  delete lObjs;
  FLTableDB *objTdb = ::qt_cast<FLTableDB *>(obj);
  if (fMD && objTdb) {
    objTdb->setTableName(field->relationM1()->foreignTable());
    objTdb->setFieldRelation(field->associatedFieldFilterTo());
    objTdb->setForeignField(fMD->relationM1()->foreignField());
    if (fMD->relationM1()->foreignTable() == tMD->name())
      objTdb->setReadOnly(true);
  }

  f->setFilter(filter_);

  if (f->mainWidget()) {
    if (objTdb) {
      QVariant curValue(value());
      if (field->type() == QVariant::String && !curValue.toString().isEmpty()) {
        objTdb->setInitSearch(curValue.toString());
        objTdb->putFirstCol(field->relationM1()->foreignField());
      }
      QTimer::singleShot(0, objTdb->lineEditSearch, SLOT(setFocus()));
    }
    QVariant v(f->exec(field->relationM1()->foreignField()));
    if (v.isValid() && !v.isNull()) {
      setValue(QVariant());
      setValue(v);
    }
  }

  f->close();

  if (c) {
    disconnect(c, 0, 0, 0);
    c->deleteLater();
  }
}
"""

    """
  Abre un dialogo para buscar un fichero de imagen.

  Si el campo no es de tipo Pixmap no hace nada
    """
    @decorators.NotImplementedWarn
    def searchPixmap(self):
"""
{
  if (!cursor_ || !editorImg_)
    return;

  if (fieldName_.isEmpty())
    return;
  FLTableMetaData *tMD = cursor_->metadata();
  if (!tMD)
    return;
  FLFieldMetaData *field = tMD->field(fieldName_);
  if (!field)
    return;

  if (field->type() == QVariant::Pixmap) {
    QFileDialog *fd = new QFileDialog(this, 0, true);
    FLPixmapView *p = new FLPixmapView(fd);

    p->setAutoScaled(true);
    fd->setContentsPreviewEnabled(TRUE);
    fd->setContentsPreview(p, p);
    fd->setPreviewMode(QFileDialog::Contents);
    fd->setCaption(tr("Elegir archivo"));
    fd->setFilter("*");

    QString filename;
    if (fd->exec() == QDialog::Accepted)
      filename = fd->selectedFile();
    if (filename.isEmpty())
      return;
    setPixmap(filename);
  }
}
"""


    """
  Carga una imagen en el campo de tipo pixmap
  @param filename: Ruta al fichero que contiene la imagen
    """
    @decorators.NotImplementedWarn
    def setPixmap(self, filename):
"""
{
  QImage img(filename);

  if (img.isNull())
    return;

  QApplication::setOverrideCursor(waitCursor);

  QPixmap pix;
  QCString s;
  QBuffer buffer(s);

  // Silix
  if (img.width() <= maxPixImages_ && img.height() <= maxPixImages_)
    pix.convertFromImage(img);
  else {
    int newWidth, newHeight;
    if (img.width() < img.height()) {
      newHeight = maxPixImages_;
      newWidth = qRound(newHeight * img.width() / img.height());
    } else {
      newWidth = maxPixImages_;
      newHeight = qRound(newWidth * img.height() / img.width());
    }
    pix.convertFromImage(img.scale(newWidth, newHeight, QImage::ScaleMin));
  }

  QApplication::restoreOverrideCursor();

  if (pix.isNull())
    return;

  editorImg_->setPixmap(pix);

  QApplication::setOverrideCursor(waitCursor);

  buffer.open(IO_WriteOnly);
  pix.save(&buffer, "XPM");

  QApplication::restoreOverrideCursor();

  if (s.isEmpty())
    return;

  if (!QPixmapCache::find(s.left(100)))
    QPixmapCache::insert(s.left(100), pix);

  updateValue(QString(s));
}
"""

    """
  Carga una imagen en el campo de tipo pixmap con el ancho y alto preferido

  @param pixmap: pixmap a cargar en el campo
  @param w: ancho preferido de la imagen
  @param h: alto preferido de la imagen
  @author Silix
    """
    @decorators.NotImplementedWarn
    def setPixmapFromPixmap(self, pixmap, w = 0, h = 0):
"""
{
  if (pixmap.isNull())
    return;

  QApplication::setOverrideCursor(waitCursor);

  QPixmap pix;
  QCString s;
  QBuffer buffer(s);

  QImage img = pixmap.convertToImage();
  if (w != 0 && h != 0)
    pix.convertFromImage(img.scale(w, h, QImage::ScaleMin));
  else
    pix.convertFromImage(img);

  QApplication::restoreOverrideCursor();

  if (pix.isNull())
    return;

  editorImg_->setPixmap(pix);

  QApplication::setOverrideCursor(waitCursor);

  buffer.open(IO_WriteOnly);
  pix.save(&buffer, "XPM");

  QApplication::restoreOverrideCursor();

  if (s.isEmpty())
    return;

  if (!QPixmapCache::find(s.left(100)))
    QPixmapCache::insert(s.left(100), pix);

  updateValue(QString(s));
}
"""
    """
  Carga una imagen desde el portapapeles en el campo de tipo pixmap
  @author Silix
    """
    @decorators.NotImplementedWarn
    def setPixmapFromClipboard(self):
"""
{
  QImage img = QApplication::clipboard()->image();
  if (img.isNull())
    return;

  QApplication::setOverrideCursor(waitCursor);

  QPixmap pix;
  QCString s;
  QBuffer buffer(s);

  // Silix
  if (img.width() <= maxPixImages_ && img.height() <= maxPixImages_)
    pix.convertFromImage(img);
  else {
    int newWidth, newHeight;
    if (img.width() < img.height()) {
      newHeight = maxPixImages_;
      newWidth = qRound(newHeight * img.width() / img.height());
    } else {
      newWidth = maxPixImages_;
      newHeight = qRound(newWidth * img.height() / img.width());
    }
    pix.convertFromImage(img.scale(newWidth, newHeight, QImage::ScaleMin));
  }

  QApplication::restoreOverrideCursor();

  if (pix.isNull())
    return;

  editorImg_->setPixmap(pix);

  QApplication::setOverrideCursor(waitCursor);

  buffer.open(IO_WriteOnly);
  pix.save(&buffer, "XPM");

  QApplication::restoreOverrideCursor();

  if (s.isEmpty())
    return;

  if (!QPixmapCache::find(s.left(100)))
    QPixmapCache::insert(s.left(100), pix);

  updateValue(QString(s));
}
"""

    """
  Guarda imagen de campos tipo Pixmap en una ruta determinada.

  @param filename: Ruta al fichero donde se guardará la imagen
  @param fmt Indica el formato con el que guardar la imagen
  @author Silix
    """
    @decorators.NotImplementedWarn
    def savePixmap( filename, format):
"""
{
  if (editorImg_) {
    if (!filename.isEmpty()) {
      QPixmap pix;
      QApplication::setOverrideCursor(waitCursor);
      pix.loadFromData(value().toCString());
      if (!pix.isNull())
        if (!pix.save(filename, format))
          QMessageBox::warning(this, tr("Error"), tr("Error guardando fichero"));
      QApplication::restoreOverrideCursor();
    }
  }
}
"""
    """
  Devueve el objeto imagen asociado al campo

  @return imagen asociada al campo
  @author Silix
    """
    @decorators.NotImplementedWarn
    def pixmap(self):
"""
{
  QPixmap pix;
  pix.loadFromData(value().toCString());
  return pix;
}
"""

    """
  Emite la señal de foco perdido
    """
    @decorators.NotImplementedWarn
    def emitLostFocus(self):

    """
  Establece que el control no está mostrado
    """
    def setNoShowed(self):
        if not self.foreignField_.isEmpty() and not self.fieldRealtion_.isEmpty():
            self.showed_ = False
            if self.isvisible():
                self.showWidget()

    """
  Establece el valor de este campo según el resultado de la consulta
  cuya claúsula 'where' es;  nombre campo del objeto que envía la señal igual
  al valor que se indica como parámetro.

  Sólo se pueden conectar objetos tipo FLFielDB, y su uso normal es conectar
  la señal FLFieldDB::textChanged(cons QString&) a este slot.

  @param v Valor
    """
    @decorators.NotImplementedWarn
    def setMapValue(self, v):


    """
  Emite la señal de keyF2Pressed.

  La señal key_F2_Pressed del editor (sólo si el editor es FLLineEdit)
  está conectada a este slot.
   """
    @decorators.NotImplementedWarn
    def emitKeyF2Pressed(self):

    """
  Emite la señal de labelClicked. Se usa en los campos M1 para editar el formulario de edición del valor seleccionado.
    """
    @decorators.NotImplementedWarn
    def emitLabelClicked(self):

    """
  Emite la señal de textChanged.

  La señal textChanged del editor (sólo si el editor es FLLineEdit)
  está conectada a este slot.
    """
    @decorators.NotImplementedWarn
    def emitTextChanged(self, t):

    """
  Emite la señal activatedAccel( int )
    """
    @decorators.NotImplementedWarn
    def emitActivatedAccel(self, identifier):

    """
  Redefinida por conveniencia
    """
    @decorators.NotImplementedWarn
    def setEnabled(self , enable):

    #protected:

    """
  Filtro de eventos
    """
    @decorators.NotImplementedWarn
    def eventFilter(self, obj, ev):

    """
  Captura evento mostrar
    """
    @decorators.NotImplementedWarn
    def showEvent(self, e):

    #private:

    """
  Redefinida por conveniencia
    """
    @decorators.NotImplementedWarn
    def showWidget(self):

    """
  Inicializa un editor falso y no funcional.

  Esto se utiliza cuando se está editando el formulario con el diseñador y no
  se puede mostrar el editor real por no tener conexión a la base de datos.
  Crea una previsualización muy esquemática del editor, pero suficiente para
  ver la posisicón y el tamaño aproximado que tendrá el editor real.
    """
    @decorators.NotImplementedWarn
    def initFakeEditor(self):

    """
  Auxiliar para refrescar filtros utilizando fieldMapValue_ y mapValue_
    """
    @decorators.NotImplementedWarn
    def setMapValue(self):

 

    """
    Color de los campos obligatorios
    @author Aulla
    """
    @decorators.NotImplementedWarn
    def notNullColor(self):
        if not self.initNotNullColor_:
            self.initNotNullColor_ = True	
  	self.notNullColor_ = FLSettings.readEntry("ebcomportamiento/colorObligatorio","")
        if self.notNullColor_ == "":
            self.notNullColor_ = QColor(255, 233, 173)
        return self.notNullColor_
  	

    #signals
    @decorators.NotImplementedWarn
    def lostFocus(self): #Señal de foco perdido
    @decorators.NotImplementedWarn
    def keyF2Pressed(self): #Señal emitida si se pulsa la tecla F2 en el editor
    @decorators.NotImplementedWarn
    def labelClicked(self): #Señal emitida si se hace click en el label de un campo M1
    @decorators.NotImplementedWarn
    def textChanged(self, QString): #Señal emitida si se cambia el texto en el editor, sólo si es del tipo FLLineEdit
    @decorators.NotImplementedWarn
    def activatedAccel(self, int): #Cuando se pulsa una combinación de teclas de aceleración se emite esta señal indicando el identificador de la combinación de teclas pulsada
    @decorators.NotImplementedWarn
    def keyF4Pressed(self): #Señal emitida si se pulsa la tecla F4 en el editor
    @decorators.NotImplementedWarn
    def keyReturnPressed(self): #Señal emitida si se pulsa la tecla Return

class FLPixmapView(QScrollView, QFilePreview):

    pixmap_ = None
    pixmapView_ = None
    path_ = None
    autoScaled_ = None

  FLPixmapView(QWidget *parent = 0);
    @decorators.NotImplementedWarn
    def setPixmap(self, pix):
    @decorators.NotImplementedWarn
    def drawContents(self, p, int, int, int, int):
    @decorators.NotImplementedWarn
    def previewUrl(self, u):
    @decorators.NotImplementedWarn
    def clear(self):
    @decorators.NotImplementedWarn
    def pixmap(self):
    @decorators.NotImplementedWarn
    def setAutoScaled(self, autoScaled):


class FLLineEdit(QLineEdit):

    #FLLineEdit(QWidget *parent, const char *name = 0);

    
    type_ = None
    partDecimal = None
    autoSelect = None

    @decorators.NotImplementedWarn
    def text(self):
    
    #public slots:
    @decorators.NotImplementedWarn
    def setText(const QString &):

    #protected:
    @decorators.NotImplementedWarn
    def focusOutEvent(self, f):
    @decorators.NotImplementedWarn
    def focusInEvent(self, f):


class FLDoubleValidator: public QDoubleValidator

    #FLDoubleValidator(QObject *parent, const char *name = 0);
    #FLDoubleValidator(double bottom, double top, int decimals, QObject *parent, const char *name = 0);
    #QValidator::State validate(QString &input, int &) const;

class FLIntValidator: public QIntValidator

    #FLIntValidator(QObject *parent, const char *name = 0);
    #FLIntValidator(int minimum, int maximum, QObject *parent, const char *name = 0);
    #QValidator::State validate(QString &input, int &) const;


class FLUIntValidator(QIntValidator):

    #FLUIntValidator(QObject *parent, const char *name = 0);
    #FLUIntValidator(int minimum, int maximum, QObject *parent, const char *name = 0);
    #validate(QString &input, int &) const;


class FLSpinBox(QSpinBox):

    #FLSpinBox(QWidget *parent = 0, const char *name = 0) : QSpinBox(parent, name) {
    	#editor()setAlignment(Qt::AlignRight); }
    


class FLDateEdit(QDateEdit):
    
    #FLDateEdit(QWidget *parent = 0, const char *name = 0) : QDateEdit(parent, name) {}
    def fix(self):

class AQTextEditBar(QWidget):

    layout_ = None
    lb_ = None
    pbBold_ = None
    pbItal_ = None
    pbUnde_ = None
    pbColor_ = None
    comboFont_ = None
    comboSize_ = None
    ted_ = None

    #AQTextEditBar(QWidget *parent = 0, const char *name = 0, QLabel *lb = 0);
    @decorators.NotImplementedWarn
    def doConnections(self, e):

    #private slots:

    @decorators.NotImplementedWarn
    def textBold(self):
    @decorators.NotImplementedWarn
    def textItalic(self):
    @decorators.NotImplementedWarn
    def textUnderline(self):
    @decorators.NotImplementedWarn
    def textColor(self):
    @decorators.NotImplementedWarn
    def textFamily(self,f):
    @decorators.NotImplementedWarn
    def textSize(self, p):
    @decorators.NotImplementedWarn
    def fontChanged(self, f):
    @decorators.NotImplementedWarn
    def colorChanged(self, c):

