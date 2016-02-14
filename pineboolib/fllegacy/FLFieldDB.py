# encoding: UTF-8
from PyQt4 import QtCore,QtGui

from pineboolib import decorators

class FLFieldDB(QtGui.QWidget):
    
    editor_ = None #Editor para el contenido del campo que representa el componente
    fieldName_ = None #Nombre del campo de la tabla al que esta asociado este componente
    tableName_ = None #Nombre de la tabla fóranea
    actionName_ = None #Nombre de la accion
    foreignField_ = None #Nombre del campo foráneo
    fieldRelation_ = None #Nombre del campo de la relación
    filter_ = None #Nombre del campo de la relación
    cursor_ = None #Cursor con los datos de la tabla origen para el componente
    cursorAux = None #  Cursor auxiliar de uso interno para almacenar los registros de la tabla relacionada con la de origen
    cursorInit = None #Indica que si ya se ha inicializado el cursor
    cursorAuxInit = None #Indica que si ya se ha inicializado el cursor auxiliar
    topWidget_ = None #Ventana superior
    showed = None #Indica que el componete ya ha sido mostrado una vez
    cursorBackup_ = None #Backup del cursor por defecto para acceder al modo tabla externa
    showAlias_ = None #Variable que almacena el estado de la propiead showAlias
    """
    Seleccionador de fechas.
    """
    datePopup_ = None
    dateFrame_ = None
    datePickerOn_ = None

    accel_ = None #Aceleradores de combinaciones de teclas
    keepDisabled_ = None #Indica que el componente permanezca deshabilitado evitando que vuelva a habilitarse en sucesivos refrescos. Ver FLFieldDB::refresh().
    editorImg_ = None #Editor para imagenes
    pbAux_ = None #Boton auxiliar multifunción
    pbAux2_ = None #Boton auxiliar multifunción
    pbAux3_ = None #Boton auxiliar multifunción
    pbAux4_ = None #Boton auxiliar multifunción
    fieldAlias_ = None #Almacena el alias del campo que será mostrado en el formulario
    showEditor_ = None #Almacena el valor de la propiedad showEditor
    partDecimal_= None #Valor de cifras decimales en caso de ser distinto del definido en los metadatos del campo

    """
    Tamaños maximo y minimos iniciales
    """
    initMaxSize_ = None
    initMinSize_ = None

    """
    Para asistente de completado automático.
    """
    autoComPopup_= None
    autoComFrame_= None
    autoComFieldName_= None
    autoComFieldRelation_ = None
    autoCompMode_ = None
    timerAutoComp_ = None

    """
    Auxiliares para poder repetir llamada a setMapValue y refrescar filtros
    """
    fieldMapValue_ = None
    mapValue_ = None

    maxPixImages_ = None #Tamaño máximo de las imágenes en los campos pixmaps (en píxeles) @author Silix
    notNullColor_ = None #Color de los campos obligatorios @author Aulla
    initNotNullColor_ = False #Colorear campos obligatorios @author Aulla
  
  
  
  /**
  El formato del texto
  */
  Qt::TextFormat textFormat_;

    def __init__(self, parent, *args):
        super(FLFieldDB,self).__init__(parent,*args)


    
    def __getattr__(self, name): return DefFun(self, name)

    """
  Para obtener el nombre de la accion.

  @return Nombre de la accion
    """  
    @decorators.NotImplementedWarn
    def actionName(self):
        return self.actionName_
            

    """
  Para establecer el nombre de la accion.

  @param aN Nombre de la accion
    """  
    @decorators.NotImplementedWarn
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
    @decorators.NotImplementedWarn
    def fieldName(self):
        return self.fieldName_

    """
  Para añadir un filtro al cursor.

    """
    @decorators.NotImplementedWarn
    def setFilter(self, f):
        if not self.filter_ == f:
            self.filter_ = f
            self.setMaValue()

    """
  Para obtener el filtro del cursor.

    """
    @decorators.NotImplementedWarn
    self.filter(self):
        return self.fliter_


    """
  Para establecer el nombre del campo.

  @param fN Nombre del campo
    """
    @decorators.NotImplementedWarn
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
    @decorators.NotImplementedWarn
    def tableName(self):
        return self.tableName_
    """
  Para establecer el nombre de la tabla foránea.

  @param fT Nombre de la tabla
    """
    @decorators.NotImplementedWarn
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
    @decorators.NotImplementedWarn
    def foreignField(self):
        return self.foreingField_

    """
  Para establecer el nombre del campo foráneo.

  @param fN Nombre del campo
    """
    @decorators.NotImplementedWarn
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
    @decorators.NotImplementedWarn
    def fieldRelation(self):
        return self.fieldRelation_

    """
  @return Alias del campo, es el valor mostrado en la etiqueta
    """
    @decorators.NotImplementedWarn
    def fieldAlias(self):
        return self.fieldAlias_

    """    
  Para obtener el widget editor.

  @return Objeto con el editor del campo
    """
    @decorators.NotImplementedWarn
    def editor(self):
        return self.editor_

    """
  Para establecer el nombre del campo relacionado.

  @param fN Nombre del campo
    """
    @decorators.NotImplementedWarn
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
    @decorators.NotImplementedWarn
    def setFieldAlias(self, alias):
        if alias:
            self.filedAlias_ = alias
            if self.showAlias_:
                self.textLabelDB.setText(self.fieldAlias_)

    """
  Establece el formato del texto

  @param f Formato del campo
    """
    @decorators.NotImplementedWarn
    def setTextFormat(self, f):
        self.textFormat_ = f
        ted = self.editor_
        if ted:
            ted.setTextFormat(self.textFormat_)

    """
  @return El formato del texto
    """
    @decorators.NotImplementedWarn
    def textFormat(self):
        ted = self.editor_
        if ted:
            return ted.textFormat()
        return self.textFormat_

    """
  Establece el modo de "echo"

  @param m Modo (Normal, NoEcho, Password)
    """
    @decorators.NotImplementedWarn
    def setEchoMode(self, m):
        led = self.editor_
        if led:
            led.setEchoMode(m.echoMode())


    """
  @return El mode de "echo" (Normal, NoEcho, Password)
    """
    @decorators.NotImplementedWarn
    def echoMode(self):
        led = self.editor_
        if led:
            return led.echoMode()
        return Qtgui.QlineEdit.Normal
    """
  Establece el valor contenido en elcampo.

  @param v Valor a establecer
    """
    @decorators.NotImplementedWarn
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

        cv = QVariant(v)
        if field.hasOptionsList(): #{
            idxItem = -1
            if v.type() == QVariant.String:
                idxItem = field.optionsList().findIndex(v.toString())
            if idxItem == -1:
                idxItem = v.toInt()
            self.editor_.setCurrentItem(idxItem)
            #updateValue(::qt_cast<QComboBox *>(editor_)->currentText()); #FIXME
        return
        #}

        type_ = field.type()
        fltype = FLFieldMetaData.flDecodeType(type_)
        if v.type() == QVariant.Bool and not fltype == QVariant.Bool:# {
            if type_ == QVariant.Double or type_ == QVariant.Int or type_ == QVariant.UInt:
                v = 0
            else:
                v.clear()
        #}
        if v.type() == QVariant.String and not v.toString(): # .isEmpty()
            if type_ == QVariant.Double and type_ == QVariant.Int ans type_ == QVariant.UInt:
                v.clear()

        isNull = bool(not v.isValid() and v.isNull())
        if isNull and not field.allowNull():# {
            defVal = QVariant(field.defaultValue())
            if defVal.isValid() and not defVal.isNull(): #{
                v = defVal
                isNull = false
    #}
  #}

        v.cast(fltype)

        if type_ == QVariant.UInt or type_ == QVariant.Int or type_ == QVariant.String:
            if self.editor_:
                #bool doHome = (::qt_cast<FLLineEdit *>(editor_)->text().isEmpty()); #FIXME
                #::qt_cast<FLLineEdit *>(editor_)->setText(isNull ? QString() : v.toString()); #FIXME
                if doHome:
                    ::qt_cast<FLLineEdit *>(editor_)->home(false); #FIXME
        if type_ == QVariant.StringList:
            if not self.editor_:
                return
            #::qt_cast<QTextEdit *>(editor_)->setText(isNull ? QString() : v.toString()); #FIXME
      
        if type_ == QVariant.Double:
            if not self.editor_:
                s= None
                if not isNull:
                    s.setNum(v.toDouble(), 'f', self.partDecimal_ != -1 ? self.partDecimal_ : field.partDecimal()) #FIXME??
                #::qt_cast<FLLineEdit *>(editor_)->setText(s); #FIXME

        if type_ == FLFieldMetaData.Serial:

            if self.editor_:
                #::qt_cast<FLSpinBox *>(editor_)->setValue(isNull ? 0 : v.toUInt()); #FIXME
    
        if type_ == QVariant.Pixmap:
            if self.editorImg_: #{
                cs= None
                if not isNull:
                    cs = v.toCString()
                if cs.isEmpty(): # {
                    self.editorImg_->clear()
                    return
                #}
                pix = QPixmap 
                if not QPixmapCache::find(cs.left(100), pix): # { #FIXME
                    pix.loadFromData(cs)
                    QPixmapCache.insert(cs.left(100), pix) #FIXME
                    # }
                if not pix.isNull():
                    self.editorImg_.setPixmap(pix)
                else:
                    self.editorImg_.clear()
        #}
        if type_ == QVariant.Date:
            if (self.editor_):
                #::qt_cast<FLDateEdit *>(editor_)->setDate(isNull ? QDate() : v.toDate()); #FIXME

        if type_ == QVariant.Time:
            if self.editor_:
                #::qt_cast<QTimeEdit *>(editor_)->setTime(isNull ? QTime() : v.toTime()); #FIXME
        if type_ == QVariant.Bool:
            if self.editor_ and not isNull:
                #::qt_cast<QCheckBox *>(editor_)->setChecked(v.toBool()); #FIXME


    """
  Obtiene el valor contenido en el campo.
    """
    @decorators.NotImplementedWarn
    def value(self):

    """
  Marca como seleccionado el contenido del campo.
    """
    @decorators.NotImplementedWarn
    def selectAll(self):

    """
  Devuelve el cursor de donde se obtienen los datos. Muy util
  para ser usado en el modo de tabla externa (fieldName y tableName
  definidos, foreingField y fieldRelation en blanco).
    """
    @decorators.NotImplementedWarn
    def cursor(self):

    """
  Devuelve el valor de la propiedad showAlias. Esta propiedad es
  usada para saber si hay que mostrar el alias cuando se está
  en modo de cursor relacionado.
    """
    @decorators.NotImplementedWarn
    def showAlias(self):

    """
  Establece el estado de la propiedad showAlias.
    """
    @decorators.NotImplementedWarn
    def setShowAlias(self, value):

    """
  Inserta como acelerador de teclado una combinación de teclas, devociendo su identificador

  @param key Cadena de texto que representa la combinación de teclas (p.e. "Ctrl+Shift+O")
  @return El identificador asociado internamente a la combinación de teclas aceleración insertada
    """
    @decorators.NotImplementedWarn
    def insertAccel(self, key):
        return 

    """
  Elimina, desactiva, una combinación de teclas de aceleración según su identificador.

  @param identifier Identificador de la combinación de teclas de aceleración
    """
    @decorators.NotImplementedWarn
    def removeAccel(self, identifier):


    """
  Establece la capacidad de mantener el componente deshabilitado ignorando posibles
  habilitaciones por refrescos. Ver FLFieldDB::keepDisabled_ .

  @param keep TRUE para activar el mantenerse deshabilitado y FALSE para desactivar
    """
    @decorators.NotImplementedWarn
    def setKeepDisabled(self, keep):

    """
  Devuelve el valor de la propiedad showEditor.
    """
    @decorators.NotImplementedWarn
    def showEditor(self):

    """
  Establece el valor de la propiedad showEditor.
    """
    @decorators.NotImplementedWarn
    def setShowEditor(self, show):

    """
  Establece el número de decimales
    """
    @decorators.NotImplementedWarn
    def setPartDecimal(self, d):

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


    """
  Refresco rápido
    """
    @decorators.NotImplementedWarn
    def refreshQuick(self fN = None):


    """
  Inicia el cursor segun este campo sea de la tabla origen o de
  una tabla relacionada
    """
    @decorators.NotImplementedWarn
    def initCursor(self):


    """
  Crea e inicia el editor apropiado para editar el tipo de datos
  contenido en el campo (p.e: si el campo contiene una fecha crea
  e inicia un QDataEdit)
    """
    @decorators.NotImplementedWarn
    def initEditor(self):


    """
  Actualiza el valor del campo con una cadena de texto.

  @param t Cadena de texto para actualizar el campo
    """
    @decorators.NotImplementedWarn
    def updateValue(self, t):

    """
  Actualiza el valor del campo con una fecha.

  @param d Fecha para actualizar el campo
    """
    @decorators.NotImplementedWarn
    def updateValue(self, d):

    """
  Actualiza el valor del campo con una hora.

  @param t Hora para actualizar el campo
    """
    @decorators.NotImplementedWarn
    def updateValue(self, t):

    """
  Actualiza el valor del campo con un valor logico.

  @param b Valor logico para actualizar el campo
    """
    @decorators.NotImplementedWarn
    def updateValue(self, b):

    """
  Actualiza el valor del campo con un texto, si el componente
  es del tipo QTextEdit
    """
    @decorators.NotImplementedWarn
    def updateValue(self):

    """
  Muestra/Oculta el seleccionador de fechas.
    """
    @decorators.NotImplementedWarn
    def toggleDatePicker(self):

    """
  Borra imagen en campos tipo Pixmap.
    """
    @decorators.NotImplementedWarn
    def clearPixmap(self):

    """
  Guarda imagen en campos tipo Pixmap.

  @param fmt Indica el formato con el que guardar la imagen
    """
    @decorators.NotImplementedWarn
    self savePixmap(self, f):

    """
  Muestra/Oculta el asistente de completado automático.
    """
    @decorators.NotImplementedWarn
    self toggleAutoCompletion(self):

    """
  Actualiza el valor del campo a partir del contenido que
  ofrece el asistente de completado automático.
    """
    @decorators.NotImplementedWarn
    self autoCompletionUpdateValue(self):

    #public slots:

    """
  Abre un formulario de edición para el valor seleccionado en su acción correspondiente
    """
    @decorators.NotImplementedWarn
    def openFormRecordRelation(self):

    """
  Abre un dialogo para buscar en la tabla relacionada
    """
    @decorators.NotImplementedWarn
    def searchValue(self):

    """
  Abre un dialogo para buscar un fichero de imagen.

  Si el campo no es de tipo Pixmap no hace nada
    """
    @decorators.NotImplementedWarn
    def searchPixmap(self):

    """
  Carga una imagen en el campo de tipo pixmap
  @param filename: Ruta al fichero que contiene la imagen
    """
    @decorators.NotImplementedWarn
    def setPixmap(self, filename):

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
  Carga una imagen desde el portapapeles en el campo de tipo pixmap
  @author Silix
    """
    @decorators.NotImplementedWarn
    def setPixmapFromClipboard(self):

    """
  Guarda imagen de campos tipo Pixmap en una ruta determinada.

  @param filename: Ruta al fichero donde se guardará la imagen
  @param fmt Indica el formato con el que guardar la imagen
  @author Silix
    """
    @decorators.NotImplementedWarn
    def savePixmap( filename, format):

    """
  Devueve el objeto imagen asociado al campo

  @return imagen asociada al campo
  @author Silix
    """
    @decorators.NotImplementedWarn
    def pixmap(self):

    """
  Emite la señal de foco perdido
    """
    def emitLostFocus(self):

    """
  Establece que el control no está mostrado
    """
    def setNoShowed(self):

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

