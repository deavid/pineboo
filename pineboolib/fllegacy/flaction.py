# -*- coding: utf-8 -*-
"""FLAction Module."""

from pineboolib.application.xmlaction import XMLAction
from typing import Union


class FLAction(object):
    """
    FLAction Class.

    This class contains information on actions to open forms.

    It is used to automatically link forms with your script,
    interface and source table.

    @author InfoSiAL S.L.
    """

    """
    Nombre de la accion
    """
    _name: str

    """
    Nombre del script asociado al formulario de edición de registros
    """
    _script_form_record: str

    """
    Nombre del script asociado al formulario maestro
    """
    _script_form: str

    """
    Nombre de la tabla origen para el formulario maestro
    """
    _table: str

    """
    Nombre del formulario maestro
    """
    _form: str

    """
    Nombre del formulario de edición de registros
    """
    _form_record: str

    """
    Texto para la barra de título del formulario maestro
    """
    _caption: str

    """
    Descripción
    """
    _description: str

    def __init__(self, action: Union[str, XMLAction]) -> None:
        """Initialize."""

        self._name = ""
        self._caption = ""
        self._description = ""
        self._form = ""
        self._form_record = ""
        self._script_form = ""
        self._script_form_record = ""
        self._table = ""

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
        """Return the values ​​in a text string."""

        return "<FLAction name=%r scriptForm=%r scriptFormRecord=%r form=%r formRecord=%r caption=%r>" % (
            self._name,
            self._script_form,
            self._script_form_record,
            self._form,
            self._form_record,
            self._caption,
        )

    def setName(self, n: str) -> None:
        """Set the name of the action."""

        self._name = n

    def setScriptFormRecord(self, s: str) -> None:
        """Set the name of the script associated with the record editing form."""

        self._script_form_record = "%s.qs" % s

    def setScriptForm(self, s: str) -> None:
        """Set the name of the script associated with the master form."""

        self._script_form = "%s.qs" % s

    def setTable(self, t: str) -> None:
        """Set the name of the source table of the master form."""

        self._table = t

    def setForm(self, f: str) -> None:
        """Set the name of the master form."""

        self._form = "%s.ui" % f

    def setFormRecord(self, f: str) -> None:
        """Set the name of the record editing form."""

        self._form_record = "%s.ui" % f

    def setCaption(self, c: str) -> None:
        """Set the text of the title bar of the master form."""

        self._caption = c

    def setDescription(self, d: str) -> None:
        """Set description."""

        self._description = d

    def name(self) -> str:
        """Get the name of the action."""

        return self._name

    def scriptFormRecord(self) -> str:
        """Get the name of the script associated with the record editing form."""

        return self._script_form_record

    def scriptForm(self) -> str:
        """Get the name of the script associated with the master form."""

        return self._script_form

    def table(self) -> str:
        """Get the table associated with the action."""

        return self._table

    def caption(self) -> str:
        """Get the text from the form's title bar."""

        return self._caption

    def description(self) -> str:
        """Get the description."""

        return self._description

    def form(self) -> str:
        """Get the name of the mestro form."""

        return self._form

    def formRecord(self) -> str:
        """Get the name of the record editing form."""

        return self._form_record
