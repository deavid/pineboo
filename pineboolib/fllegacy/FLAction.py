# -*- coding: utf-8 -*-

from pineboolib import decorators


class FLAction():

    """
    Esta clase contiene información de acciones para abrir formularios.

    Se utiliza para enlazar automáticamente formularios con su script,
    interfaz y tabla de origen.

    @author InfoSiAL S.L.
    """

    """
    Nombre de la accion
    """
    name_ = None

    """
    Nombre del script asociado al formulario de edición de registros
    """
    scriptFormRecord_ = None

    """
    Nombre del script asociado al formulario maestro
    """
    scriptForm_ = None

    """
    Nombre de la tabla origen para el formulario maestro
    """
    table_ = None

    """
    Nombre del formulario maestro
    """
    form_ = None

    """
    Nombre del formulario de edición de registros
    """
    formRecord_ = None

    """
    Texto para la barra de título del formulario maestro
    """
    caption_ = None
  
    """
    Descripción
    """
    description_ = None
 
    
    
    
    """
    constructor.
    """
    def __init__(self):
        print("Init FLAction")
        
    """
    Establece el nombre de la accion
    """
    def setName(self, n):
        self.name_ = n

    """
    Establece el nombre del script asociado al formulario de edición de registros
    """
    def setScriptFormRecord(self, s):
        self.scriptFormRecord_ = s + ".qs"

    """
    Establece el nombre del script asociado al formulario maestro
    """
    def setScriptForm(self, s):
        self.scriptForm_ = s + ".qs"
    
    """
    Establece el nombre de la tabla origen del formulario maestro
    """
    def setTable(self, t):
        self.table_ = t

    """
    Establece el nombre del formulario maestro
    """
    def setForm(self, f):
        self.form_ = f + ".ui"

    """
    Establece el nombre del formulario de edición de registros
    """
    def setFormRecord(self, f):
        self.formRecord_ = f + ".ui"
    """
    Establece el texto de la barra de título del formulario maestro
    """
    @decorators.NotImplementedWarn
    def setCaption(self, c):
        self.caption_ = c

    """
    Establece la descripción
    """
    def setDescription(self, d):
        self.description_ = d

    """
    Obtiene el nombre de la accion
    """
    def name(self):
        return self.name_
    
    """
    Obtiene el nombre del script asociado al formulario de edición de registros
    """
    def scriptFormRecord(self):
        return self.scriptFormRecord_

    """
    Obtiene el nombre del script asociado al formulario maestro
    """
    def scriptForm(self):
        return self.scriptForm_

    """
    Obtiene  la tabla asociada a la accion
    """
    def table(self):
        return self.table_
    
    """
    Obtiene el texto de la barra de título del formulario
    """
    def caption(self):
        return self.caption_

    """
    Obtiene la descripcion
    """
    def description(self):
        return self.description_
    
    """
    Obtiene el nombre del formulario mestro
    """
    def form(self):
        return self.form_
    """
    Obtiene el nombre del formulario de edición de registros
    """
    def formRecord(self):
        return self.formRecord_

