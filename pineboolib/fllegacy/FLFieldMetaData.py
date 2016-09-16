# -*- coding: utf-8 -*-

#Completa Si

from pineboolib.fllegacy.FLRelationMetaDataList import FLRelationMetaDataList
from pineboolib import decorators
from pineboolib.fllegacy.FLRelationMetaData import FLRelationMetaData


from PyQt4.QtCore import QVariant, QString
from PyQt4 import QtCore, QtGui
from pineboolib.utils import aqtt



class FLFieldMetaData():
    """
  @param n Nombre del campo
  @param a Alias del campo, utilizado en etiquetas de los formularios
  @param aN TRUE si permite nulos (NULL), FALSE si los permite (NOT NULL)
  @param _isPrimaryKey TRUE si es clave primaria, FALSE si no es clave primaria, ser
        clave primaria implica ser Indice y Único
  @param t Tipo del campo
  @param l Longitud del campo en caracteres, siempre que se de tipo cadena
       de caracteres
  @param c Indica si el campo es calculado
  @param v Indica si el campo es visible
  @param ed Indica si el campo es editable
  @param pI Indica el número de dígitos de la parte entera
  @param pD Indica el número de decimales
  @param iNX TRUE si el campo es índice
  @param uNI TRUE si el campo determina registros únicos
  @param coun Indica si es un contador. Para referencias automáticas
  @param defValue Valor por defecto para el campo
  @param oT Indica si las modificaciones en el campo son fuera de transaccion
  @param rX Expresion regular utilizada como mascara de validacion
  @param vG Indica si el campo es visible en la rejilla de la tabla
  @param gen Indica si el campo es generado.
  @param iCK Indica si es clave compuesta
    """  

    Serial = "serial"
    Unlock = "unlock"
    Check = "bool"
    count_ = 0


    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            self.inicializeFLFieldMetaData(args[0])
        else:
            self.inicializeNewFLFieldMetaData( *args, **kwargs)    
        ++self.count_
            
            
    
    def inicializeFLFieldMetaData(self, other):
        self.d = FLFieldMetaDataPrivate()
        self.copy(other)
        
                                           
    def inicializeNewFLFieldMetaData(self, n, a, aN, isPrimaryKey, t, l=0, c=False, v=True, ed=True, pI=4, pD=0, iNX=False, uNI=False,coun=False,defValue=None,oT=False, rX=None, vG=True,gen=True,iCK=False):  
        self.d = FLFieldMetaDataPrivate(n, a, aN, isPrimaryKey, t, l, c, v, ed, pI, pD, iNX, uNI, coun, defValue, oT, rX, vG, gen, iCK)
    
    """
    desctructor
    """
    def __del__(self):
        del self.d
        --self.count_
        
 
        
    """
    Obtiene el nombre del campo.

    @return Nombre del campo
    """
    def name(self):
        return self.d.fieldName_


    """
    Establece el nombre para el campo

    @param n Nombre del campo
    """
    @decorators.BetaImplementation
    def setName(self, n):
        self.d.fieldName_ = n 
        
    """
    Obtiene el alias del campo.

    @return Alias del campo
    """
    def alias(self):
        return aqtt(self.d.alias_)

    """
    Obtiene si permite nulos.

    @return TRUE si permite nulos, FALSE en caso contrario
    """
    def allowNull(self):
        return self.d.allowNull_

    """
    Obtiene si es clave primaria.

    @return TRUE si es clave primaria, FALSE en caso contrario
    """

    def isPrimaryKey(self):
        return self.d.isPrimaryKey_
    
    def setIsPrimaryKey(self, b):
        self.d.isPrimaryKey_ = b
    """
    Obtiene si es clave compuesta.

    @return TRUE si es clave compuesta, FALSE en caso contrario
    """
    def isCompoundKey(self):
        return self.d.isCompoundKey_

    """
    Obtiene el tipo del campo.

    @return El tipo del campo
    """
    def type(self):
        return str(self.d.type_)

    """
    Obtiene la longitud del campo.

    @return La longitud del campo
    """
    def length(self):
        return self.d.length_

    """
    Obtiene si el campo es calculado.

    @return TRUE si el campo es calculado, FALSE en caso contrario
    """
    def calculated(self):
        return self.d.calculated_

    """
    Establece si el campo es calculado.

    @param c Valor TRUE si se quiere poner el campo como calculado, FALSE en caso contrario
    """
    def setCalculated(self, c):
        self.d.calculated_ = c

    """
    Obtiene si el campo es editable.

    @return TRUE si el campo es editable, FALSE en caso contrario
    """
    def editable(self):
        return self.d.editable_

    """
    Establece si el campo es editable.

    @param ed Valor TRUE si se quiere que el campo sea editable, FALSE
          en caso contrario
    """
    def setEditable(self, ed):
        self.d.editable_ = ed

    """
    Obtiene si el campo es visible.

    @return TRUE si el campo es visible, FALSE en caso contrario
    """
    def visible(self):
        return self.d.visible_

    """
    Obtiene si el campo es visible en la rejilla de la tabla.

    @return TRUE si el campo es visible en la rejilla de la tabla, FALSE en caso contrario
    """
    def visibleGrid(self):
        return self.d.visibleGrid_


    """
    @return TRUE si el campo es generado, es decir, se incluye en las consultas
    """
    def generated(self):
        return self.d.generated_

    """
    Establece si el campo es visible.

    @param v Valor TRUE si se quiere poner el campo como visible, FALSE
         en caso contrario
    """
    def setVisible(self, v):
        self.d.visible_ = v

    """
    Establece si el campo es visible en la rejilla de la tabla.

    @param v Valor TRUE si se quiere poner el campo como visible, FALSE
         en caso contrario
    """
    def setVisibleGrid(self, v):
        self.d.visibleGrid_ = v

    """
    Obtiene el número de dígitos de la parte entera.

    @return El número de dígitos de la parte entera del campo
    """
    def partInteger(self):
        return self.d.partInteger_

    """
    Obtiene el número de dígitos de la parte decimal.

    @return El número de dígitos de la parte decimal del campo
    """
    def partDecimal(self):
        return self.d.partDecimal_
    """
    Obtiene si el campo es contador.

    @return TRUE si el campo es una referencia con contador
    """
    @decorators.BetaImplementation
    def isCounter(self):
        return self.d.contador_


    """
    Obtiene si el campo es índice.

    @return TRUE si el campo es índice, FALSE en caso contrario
    """
    @decorators.BetaImplementation
    def isIndex(self):
        return self.d.isIndex_

    """
    Obtiene si el campo determina registros únicos.

    @return TRUE si el campo determina registros únicos, FALSE en caso contrario
    """
    @decorators.BetaImplementation
    def isUnique(self):
        return self.d.isUnique_

    """
    Tipo de datos lista de relaciones
    """
    #typedef QPtrList<FLRelationMetaData> FLRelationMetaDataList; // FLRelationMetaDataList.py

    """
    Añade una relacion con otra tabla para este campo.

    Añade un nuevo objeto FLRelationMetaData, a la lista
    de relaciones para este campo.

    Hay que notar que para un campo solo puede existir una
    sola relacion del tipo M1 (muchos a uno), por lo que en
    el caso de que se quieran añadir varias relaciones de
    este tipo para el campo solo se tendrá en cuenta la primera.
    Relaciones del tipo 1M (uno a muchos) pueden existir todas
    las que sean necesarias. Ver FLRelationMetaData::Cardinality.

    @param r Objeto FlRelationMetaData con la definicion de la
         relacion a añadir """
         
    def addRelationMD(self, r):
        
        isRelM1 = False
        #print("FLFieldMetadata(%s).addRelationMD(card %s)" % (self.name(), r.cardinality()))
        if r.cardinality() == FLRelationMetaData.RELATION_M1:
            isRelM1 = True
        if isRelM1 and self.d.relationM1_:
            print("FLFieldMetaData: Se ha intentado crear más de una relación muchos a uno para el mismo campo")
            return
        
        
        r.setField(self.d.fieldName_)
        if isRelM1:
            self.d.relationM1_ = r 
            return
        
        if not self.d.relationList_:
            self.d.relationList_ = []
        
        self.d.relationList_.append(r)
        
    """
    Para obtener la lista de definiciones de las relaciones.

     No incluye la relacion M1

    @return Objeto con la lista de deficiones de la relaciones del campo
    """
    def relationList(self):
        return self.d.relationList_

    """
    Para obtener la relacion muchos a uno para este campo.

       No incluida en relationList()

    @return Objeto FLRelationMetaData con la descripcion de la relacion
        muchos a uno para este campo
    """
    def relationM1(self):
        return self.d.relationM1_
             
    """
    Establece un campo asociado para este campo, y el nombre
    del campo de la tabla foránea que se debe utilizar para filtrar según
    el valor del campo asociado.

    Ver FLFieldMetaData::associatedField_
    Ver FLFieldMetaData::associatedFieldFilterTo_

    @param r Objeto FLFieldMetaData que define el campo que se quiere asociar a este
    @param f Nombre del campo a aplicar el filtro
    """
    #def setAssociatedField(self, *r, f):
    #    self.d.associatedField_ = r
    #    self.d.associatedFieldFilterTo_ = f

    """
    Sobrecargada por conveniencia

    @param r Nombre del campo que se quiere asociar a este
    @param f Nombre del campo a aplicar el filtro
    """
    #def setAssociatedField(self, rName, f):
    #    self.d.associatedFieldName_ = rName
    #    self.d.associatedFieldFilterTo_ = f
    
    
    def setAssociatedField(self, rName, f ):
        if isinstance(rName, FLFieldMetaData):
            self.d.associatedField_ = rName
        else:      
            self.d.associatedFieldName_ = rName
            
        self.d.associatedFieldFilterTo_ = f

    """
    Devuelve el campo asociado para este campo.

    Ver FLFieldMetaData::associatedField_

    @return Objeto FLFieldMetaData que define el campo asociado a este, o 0
      si no hay campo asociado
    """
    def associatedField(self):
        return self.d.associatedField_


    """
    Devuelve el nombre del campo que hay que filtrar según el campo asociado.

    Ver FLFieldMetaData::associatedFieldFilterTo_

    @return Nombre del campo de la tabla foránea M-1, al que hay que aplicar el filtro
      según el valor del campo asociado
    """
    @decorators.BetaImplementation
    def associatedFieldFilterTo(self):
        return self.d.associatedFieldFilterTo_

    """
    Devuelve el nombre del campo asociado este.

    Ver FLFieldMetaData::associatedField_

    @return Nombre del campo asociado
    """
    @decorators.BetaImplementation
    def associatedFieldName(self):
        return self.d.associatedFieldName_


    """
    Devuelve el valor por defecto para el campo.

    @return Valor que se asigna por defecto al campo
    """
    @decorators.BetaImplementation
    def defaultValue(self):
        return self.d.defaultValue_

    """
    Devuelve si el campo se modifica fuera de transaccion,
    ver FLFieldMetaData::outTransaction_.

    @return TRUE si el campo se modifica fuera de transaccion, FALSE en caso contrario
    """
    def outTransaction(self):
        return self.d.outTransaction_

    """
    Devuelve la expresion regular que sirve como mascara de validacion para el campo.

    @return Cadena de caracteres que contiene una expresion regular, utilizada como
        mascara para validar los valores introducidos en el campo
    """
    @decorators.BetaImplementation
    def regExpValidator(self):
        return self.d.regExpValidator_

    """
    Devuelve la lista de opciones para el campo

    @return Lista de opciones del campo
    """
    def optionsList(self):
        return self.d.optionsList_

    """
    Devuelve el index de un campo determinado

    @return Lista de opciones del campo
    """    
    def getIndexOptionsList(self, name):
        i = 0
        for option in self.d.optionsList_:
            if option == str(name):
                return i 
            
            i = i + 1
            
        return None
        
    """
    Establece la lista de opciones para el campo

    @param ol Cadena de texto con la opciones para el campo
          separada por comas, p.e. "opcion1,opcion2,opcion3"
    """
    def setOptionsList(self, ol):
        self.d.optionsList_ = []
        if ol.find("QT_TRANSLATE") != -1:
            for componente in ol.split(";"):
                self.d.optionsList_.append(aqtt(componente))
        else:
            for componente in ol.split(","):
                self.d.optionsList_.append(aqtt(componente))
                      
        if len(self.d.optionsList_) > 0:
            self.d.hasOptionsList_ = True
        else:
            self.d.hasOptionList_ = False 
    """
    Obtiene si el campo es de tipo Check
    """
    def isCheck(self):
        if self.d.type_ == self.Check:
            return True
        else:
            return False

    """
    Obtiene si el campo tiene lista de opciones
    """
    def hasOptionsList(self):
        return self.d.hasOptionsList_

    """
    Ver FLFieldMetaData::fullyCaclulated_
    """
    @decorators.BetaImplementation
    def fullyCalculated(self):
        return self.d.fullyCalculated_
  
    @decorators.BetaImplementation
    def setFullyCalculated(self, c):
        self.d.fullyCalculated_ = c
        if c:
            self.d.generated_ = True

    """
    Ver FLFieldMetaData::trimmed_
    """
    @decorators.BetaImplementation
    def trimed(self):
        return self.d.trimmed_
    
    @decorators.BetaImplementation
    def setTrimed(self, t):
        self.d.trimmed_ = t


    """
    Establece el objeto FLTableMetaData al que pertenece
    """
    def setMetadata(self, mtd):
        self.d.mtd_ = mtd


    """
    Obtiene el objeto FLTableMetaData al que pertenece
    """
    def metadata(self):
        return self.d.mtd_

    """
    Obtiene el tipo del campo convertido a un tipo equivalente de la clase QVariant
    """
    def flDecodeType(self, fltype):
        
        _type = None
        #print("Decode", fltype)
        
        if fltype == "int":
            _type = QVariant.Int
        elif fltype == "serial" or fltype == "uint":
            _type = QVariant.UInt
        elif fltype == "bool" or fltype == "unlock":
            _type = QVariant.Bool
        elif fltype == "double":
            _type = QVariant.Double
        elif fltype ==  "time":
            _type = QVariant.Time
        elif fltype == "date":
            _type = QVariant.Date
        elif fltype == "string" or fltype == "pixmap" or fltype == "stringList":
            _type = QVariant.String
        elif fltype == "bytearray":
            _type = QVariant.ByteArray
        
        #print("Return", _type)
        return _type
    """
    Devuelve diferentes opciones de búsqueda para este campo.

    @return lista de las distintas opciones
    """
    @decorators.BetaImplementation
    def searchOptions(self):
        return self.d.searchOptions_
    """
    Establece la lista de opciones para el campo

    @param ol Cadena de texto con la opciones para el campo
          separada por comas, p.e. "opcion1,opcion2,opcion3"
    """
    @decorators.BetaImplementation
    def setSearchOptions(self, ol):
        self.d.searchOptions_ = []
        for dato in ol.split(","):
            self.d.searchOptions_.append(dato)
  
  
    def copy(self, other):
        if other == self:
            return
        
        self = other
        """
        od = other.d
        if od.relationM1_:
            self.d.relationM1_ = od.relationM1_
        
        self.d.clearRelationList()
        
        if od.relationList_:
            self.d.relationList_ = od.relationList_
        
        self.d.fieldName_ = od.fieldName_
        self.d.alias_ = od.alias_
        self.d.allowNull_ = od.allowNull_
        self.d.isPrimaryKey_ = od.isPrimaryKey_
        self.d.type_ = od.type_
        self.d.length_ = od.length_
        self.d.calculated_ = od.calculated_
        self.d.fullyCalculated_ = od.fullyCalculated_
        self.d.trimmed_ = od.trimmed_
        self.d.visible_ = od.visible_
        self.d.editable_ = od.editable_
        self.d.partInteger_ = od.partInteger_
        self.d.partDecimal_ = od.partDecimal_
        self.d.isIndex_ = od.isIndex_
        self.d.isUnique_ = od.isUnique_
        self.d.contador_ = od.contador_
        self.d.associatedField_ = od.associatedField_
        self.d.associatedFieldName_ = od.associatedFieldName_
        self.d.associatedFieldFilterTo_ = od.associatedFieldFilterTo_
        self.d.defaultValue_ = od.defaultValue_
        self.d.optionsList_ = od.optionsList_
        self.d.outTransaction_ = od.outTransaction_
        self.d.regExpValidator_ = od.regExpValidator_
        self.d.visibleGrid_ = od.visibleGrid_
        self.d.generated_ = od.generated_
        self.d.isCompoundKey_ = od.isCompoundKey_
        self.d.hasOptionsList_ = od.hasOptionsList_    
        """
    
    def formatAssignValue(self,fieldName , value, upper):
        if self.type() == ("", None) or fieldName.isEmpty():
            return "1 = 1"
        
        isText = False
        if value.type() == "string" or value.type() == "stringlist":
            isText = True
        
        formatV = QString()
        if value.type() == "int" or value.type() == "uint" or value.type() == "double":
            formatV = value.toString()
        else: 
            formatV = "'" + value.toString() + "'"
        
        #print("FORMATV es %s, %s y value era %s" % (formatV, type(formatV), value.toString()))
                 
        if formatV.isEmpty():
            return "1 = 1"
        
        if upper and isText:
            fName = QString("upper(" + fieldName + ")")
        else:
            fName = QString(fieldName)
        
        return QString(fName + " = " + formatV)
        
        
        
                
               
    
class FLFieldMetaDataPrivate():
    """
    Nombre del campo en la tabla
    """
    fieldName_ = None

    """
    Alias o mote para el campo, usado como
    etiqueta de campos en los formularios
    """
    alias_ = None

    """
    Almacena si el campo permite ser nulo
    """
    allowNull_ = None

    """
    Almacena si el campo es clave primaria
    """
    isPrimaryKey_ = None

    """
    Tipo del campo
    """
    type_ = None

    """
    Longitud del campo
    """
    length_ = None

    """
    Indica si el campo es calculado de forma diferida.
    Esto indica que el campo se calcula al editar o insertar un registro, en el commit.
    """
    calculated_ = None

    """
    Indica si el campo es totalmente calculado.
    Esto indica que el valor campo del campo es dinámico y se calcula en cada refresco.
    Un campo totalmente calculado implica que es generado.
    """
    fullyCalculated_ = None

    """
    Indica que al leer el campo de la base de datos los espacios mas a la derecha
    son eliminados.
    """
    trimmed_ = None

    """
    Indica si el campo es visible
    """
    visible_ = None

    """
    Indica si el campo es editable
    """
    editable_ = None

    """
    Indica el número de dígitos de la parte entera
    """
    partInteger_ = None

    """
    Indica el númeor de dígitos de la parte decimal
    """
    partDecimal_ = None

    """
    Indica si el campo es índice
    """
    isIndex_ = None

    """
    Indica si el campo es único
    """
    isUnique_ = None

    """
    Indica si el campo es un contador de referencia y abanq en el
    momento de insertar un registro debe intentar calcular cual sería el
    siguiente numero.

    @author Andrés Otón Urbano (andresoton@eresmas.com)
    """
    contador_ = None

    """
    Lista de relaciones para este campo
    """
    relationList_ = None

    """
    Mantiene, si procede, la relación M1 (muchos a uno)
    para el campo (solo puede haber una relacion de este tipo para un campo)
    """
    relationM1_ = None

    """
    Asocia este campo con otro, para efectuar filtros en búsquedas.

    El campo que se asocia a este debe tener una relación M-1.
    Este campo también debe tener una relación M-1. Al asociar un campo a este,
    las búsquedas mediante los botones de búsqueda en los formularios de edición
    de registros vendrán condicionadas por el valor del campo asociado en el
    momento de realizar dicha búsqueda. Cuando se realiza una búsqueda para
    este campo la tabla relacionada con él (M-1) será mostrada para elegir un
    registro de todos los posibles, en el caso normal se muestran todos los registros,
    pero cuando se asocia un campo sólo se muestran aquellos registros que satisfagan el
    valor del campo asociado. Ejemplo : En la tabla albaranes asociamos el campo
    'codemporig' al campo 'codalmorig' (NO es lo mismo que asociar 'codalmorig'
    a 'codemporig') cuando abrimos el formulario de albaranes elegimos una empresa
    origen (codemporig), cuando vayamos a elegir un almacen origen (codalmorig) sólo
    se podrá elegir entre los almacenes que son de la empresa origen , ya que el formulario
    de búsqueda sólo se mostrarán los almacenes cuyo código de empresa
    (ver FLFieldMetaData::associatedFieldFilterTo_) sea igual al valor de la empresa origen
    elegida (codemporig)
    """
    associatedField_ = None
    associatedFieldName_ = None

    """
    Nombre del campo que se debe filtra según el campo asociado.

    Esta propiedad sólo tiene sentido cuando hay un campo asociado a este,
    ver FLFieldMetaData ::associatedField_ , y si ese campo tiene una relacion M-1. Indica
    el nombre del campo de la tabla foránea en la relación M-1, que se debe utilizar para filtrar
    los registros según el valor del campo asociado. Ejemplo : En la tabla albaranes asociamos el campo
    'codemporig' al campo 'codalmorig' (NO es lo mismo que asociar 'codalmorig'
    a 'codemporig'), e indicamos que el campo de filtro es 'codempresa' de la tabla relacionada M-1 con el
    campo 'codalmorig' (Almacenes) . Cuando abrimos el formulario de albaranes elegimos una empresa
    origen (codemporig), cuando vayamos a elegir un almacen origen (codalmorig) sólo se podrá elegir
    entre los almacenes que son de la empresa origen, ya que el formulario de búsqueda sólo se mostrarán
    los almacenes cuyo código de empresa (el campo indicado de filtro ) sea igual al valor de la empresa
    origen elegida (codemporig)
    """
    associatedFieldFilterTo_ = None

    """
    Valor por defecto para el campo
    """
    defaultValue_ = None

    """
    Lista de opciones para el campo
    """
    optionsList_ = None

    """
    Indica si las modificaciones del campo se hacen fuera de cualquier transaccion.

    Al estar activado este flag, todos los cambios en el valor de este campo se
    realizan fuera de la transaccion y de forma exclusiva. Es decir los cambios
    realizados en el campo son inmediatamente reflejados en la tabla sin esperar a
    que se termine transaccion, y de forma exclusiva (bloqueando el registro al que
    pertenece el campo mientras se modifica). Esto permite en el acto hacer visibles
    para todas las demas conexiones de la base de datos los cambios realizados en un campo.
    Hay que tener en cuenta que al tener el campo esta caracteristica especial de modificarse
    fuera de la transaccion, el "rollback" no tendra efecto sobre los cambios realizados
    en el y siempre permanecera en la base de datos la ultima modificacion efectuada en
    el campo.
    """
    outTransaction_ = None

    """
    Almacena la expresion regular que sirve como mascara de validacion para el campo.
    """
    regExpValidator_ = None
  
    """
    Indica si el campo debe ser visible en la rejilla de la tabla.
    """
    visibleGrid_ = None

    """
    Indica si el campo es generado, es decir, se incluye en las consultas
    """
    generated_ = False

    """
    Almacena si el campo es clave compuesta
    """
    isCompoundKey_ = None
  
    """
    Indica si el campo toma su valor de una lista de opciones
    """
    hasOptionsList_ = None

    """
    Contiene las distintas opciones de búsqueda
    """
    searchOptions_ = None
  
    """
    Objeto FLTableMetaData al que pertenece
    """
    mtd_ = None
    

    def __init__(self, *args, **kwargs):
        
        self.regExpValidator_ = QString()
        
        if len(args) == 0:
            self.inicializeEmpty()
        else:
            self.inicialize(*args, **kwargs)
        
 
    def inicializeEmpty(self):
        self.relationList_ = None
        self.relationM1_ = None
        self.associatedField_ = None
        self.mtd_ = None
        

    def inicialize(self, n, a, aN, iPK, t, l , c, v, ed, pI, pD, iNX, uNI, coun, defValue, oT, rX, vG, gen, iCK):
        self.fieldName_ = n.lower()
        self.alias_ = a
        if c:
            self.allowNull_ = True
        else:
            self.allowNull_ = aN 
        self.isPrimaryKey_ = iPK
        self.type_ = t
        self.length_ = l
        self.calculated_ = c
        self.visible_ = v 
        self.editable_ = ed
        self.partInteger_ = pI
        self.partDecimal_ = pD
        self.isIndex_ = iNX
        self.isUnique_ = uNI
        self.contador_ = coun
        self.relationList_ = None
        self.relationM1_ = None
        self.associatedField_ = None
        self.defaultValue_ = defValue
        self.outTransaction_ = oT
        self.regExpValidator_ = rX
        self.visibleGrid_ = vG
        self.generated_ = gen
        self.isCompoundKey_ = iCK
        self.hasOptionsList_ = False
        self.mtd_ = None
        self.fullyCalculated_ = False
        self.trimmed_ = False
        
        if int(l) < 0:
            self.length_ = 0
        if int(pI) < 0:
            self.partInteger_ = 0
        if int(pD) < 0:
            self.partDecimal_ = 0
        
        #print("Tipo ", t)
        
        if not t == "string" and not int(l) == 0: 
            self.length_ = 0
        
        
        if not t == "int" and not t == "uint" and t == "double" and not int(pI) == 0: 
            self.partInteger_ = 0
        
        if t == "double" and not int(pD) == 0: 
            self.partDecimal_ = 0

    @decorators.BetaImplementation
    def __del_(self):
        self.clearRelationList()
        if self.relationM1_ and self.relationM1_.deref():
            self.relationM1_ = None
        

    """
    Limpia la lista de definiciones de relaciones
    """
    def clearRelationList(self):
        self.relationList_ = []
        

