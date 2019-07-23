# -*- coding: utf-8 -*-
from pineboolib.application.xmlaction import XMLAction
from typing import Union


class FLAction(object):

    """
    Esta clase contiene información de acciones para abrir formularios.

    Se utiliza para enlazar automáticamente formularios con su script,
    interfaz y tabla de origen.

    @author InfoSiAL S.L.
    """

    """
    Nombre de la accion
    """
    name_: str = ""

    """
    Nombre del script asociado al formulario de edición de registros
    """
    scriptFormRecord_: str = ""

    """
    Nombre del script asociado al formulario maestro
    """
    scriptForm_: str = ""

    """
    Nombre de la tabla origen para el formulario maestro
    """
    table_: str = ""

    """
    Nombre del formulario maestro
    """
    form_: str = ""

    """
    Nombre del formulario de edición de registros
    """
    formRecord_: str = ""

    """
    Texto para la barra de título del formulario maestro
    """
    caption_: str = ""

    """
    Descripción
    """
    description_: str = ""

    """
    constructor.
    """

    def __init__(self, action: Union[str, XMLAction] = None) -> None:
        super(FLAction, self).__init__()
        if action is None:
            return
        if isinstance(action, str):
            self.setName(action)
        elif isinstance(action, XMLAction):
            self.setName(action.name)
            if action.mainscript is not None:
                self.setScriptForm(action.mainscript)
            if action.scriptformrecord is not None:
                self.setScriptFormRecord(action.scriptformrecord)
            if action.mainform is not None:
                self.setForm(action.mainform)
            if action.form is not None:
                self.setFormRecord(action.form)
            if action.alias is not None:
                self.setCaption(action.alias)
        else:
            raise Exception("Unsupported action %r" % action)

    def __repr__(self):
        return "<FLAction name=%r scriptForm=%r scriptFormRecord=%r form=%r formRecord=%r caption=%r>" % (
            self.name_,
            self.scriptForm_,
            self.scriptFormRecord_,
            self.form_,
            self.formRecord_,
            self.caption_,
        )

    """
    Establece el nombre de la accion
    """

    def setName(self, n: str) -> None:
        self.name_ = n

    """
    Establece el nombre del script asociado al formulario de edición de registros
    """

    def setScriptFormRecord(self, s: str) -> None:
        self.scriptFormRecord_ = "%s.qs" % s

    """
    Establece el nombre del script asociado al formulario maestro
    """

    def setScriptForm(self, s: str) -> None:
        self.scriptForm_ = "%s.qs" % s

    """
    Establece el nombre de la tabla origen del formulario maestro
    """

    def setTable(self, t: str) -> None:
        self.table_ = t

    """
    Establece el nombre del formulario maestro
    """

    def setForm(self, f: str) -> None:
        self.form_ = "%s.ui" % f

    """
    Establece el nombre del formulario de edición de registros
    """

    def setFormRecord(self, f: str) -> None:
        self.formRecord_ = "%s.ui" % f

    """
    Establece el texto de la barra de título del formulario maestro
    """

    def setCaption(self, c: str) -> None:
        self.caption_ = c

    """
    Establece la descripción
    """

    def setDescription(self, d) -> None:
        self.description_ = d

    """
    Obtiene el nombre de la accion
    """

    def name(self) -> str:
        return self.name_

    """
    Obtiene el nombre del script asociado al formulario de edición de registros
    """

    def scriptFormRecord(self) -> str:
        return self.scriptFormRecord_

    """
    Obtiene el nombre del script asociado al formulario maestro
    """

    def scriptForm(self) -> str:
        return self.scriptForm_

    """
    Obtiene  la tabla asociada a la accion
    """

    def table(self) -> str:
        return self.table_

    """
    Obtiene el texto de la barra de título del formulario
    """

    def caption(self) -> str:
        return self.caption_

    """
    Obtiene la descripcion
    """

    def description(self) -> str:
        return self.description_

    """
    Obtiene el nombre del formulario mestro
    """

    def form(self) -> str:
        return self.form_

    """
    Obtiene el nombre del formulario de edición de registros
    """

    def formRecord(self) -> str:
        return self.formRecord_
