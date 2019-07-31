# -*- coding: utf-8 -*-
"""
FLAccessControlFactory Module.

Manage ACLs between different application objects.
"""
from PyQt5 import QtWidgets  # type: ignore

from pineboolib.application.metadata.pntablemetadata import PNTableMetaData
from pineboolib.fllegacy.flaccesscontrol import FLAccessControl

from pineboolib.application import project
from typing import Dict, Any

import logging

logger = logging.getLogger("FLAccessControlFactory")


class FLAccessControlMainWindow(FLAccessControl):
    """FLAccessControlMainWindow Class."""

    def __init__(self) -> None:
        """Inicialize."""

        super(FLAccessControlMainWindow, self).__init__()

    def type(self) -> str:
        """Return target type."""

        return "mainwindow"

    def processObject(self, obj: QtWidgets.QWidget) -> None:
        """Process the object."""

        from pineboolib import pncontrolsfactory

        mw = pncontrolsfactory.QMainWindow(obj)
        if not mw or not self._acos_perms:
            return

        a: QtWidgets.QAction
        list1 = mw.queryList("QAction")
        actions_idx = {a.name(): a for a in list1}
        if not self._perm:
            for a in list1:
                if self._acos_perms[a.name()]:
                    continue
                if self._perm == "-w" or self._perm == "--":
                    a.setVisible(False)

        for a_name, perm in self._acos_perms.items():
            if a_name in actions_idx:
                a = actions_idx[a_name]
                if perm in ("-w", "--"):
                    a.setVisible(False)

    def setFromObject(self, object: Any) -> None:
        """Not implemented jet."""
        logger.warning("FLAccessControlMainWindow::setFromObject %s", "No implementado todavía.")


class FLAccessControlForm(FLAccessControl):
    """FLAccessControlForm Class."""

    def __init__(self) -> None:
        """Inicialize."""

        super().__init__()
        if project.DGI.localDesktop():
            from PyQt5.Qt import qApp  # type: ignore
            from PyQt5 import QtGui  # type: ignore

            self.pal = QtGui.QPalette()
            bg = QtGui.QColor(qApp.palette().color(QtGui.QPalette.Active, QtGui.QPalette.Background))

            self.pal.setColor(QtGui.QPalette.Foreground, bg)
            self.pal.setColor(QtGui.QPalette.Text, bg)
            self.pal.setColor(QtGui.QPalette.ButtonText, bg)
            self.pal.setColor(QtGui.QPalette.Base, bg)
            self.pal.setColor(QtGui.QPalette.Background, bg)

    def type(self) -> str:
        """Return target type."""
        return "form"

    def processObject(self, obj) -> None:
        """
        Process objects that are of the FLFormDB class.

        Only control the children of the object that are of the QWidget class, and only
        allows to make them not visible or not editable. Actually do them
        not visible means that they are not editable and modifying the palette to
        that the entire region of the component be shown in black. The permits
        which accepts are:

        - "-w" or "--" (no_read / write or no_read / no_write) -> not visible
        - "r-" (read / no_write) -> not editable

        This allows any component of an AbanQ form (FLFormDB,
        FLFormRecordDB and FLFormSearchDB) can be made not visible or not editable for convenience.
        """

        fm = obj
        if not fm or not self._acos_perms:
            return

        if self._perm:
            list_ = fm.children()

            for w in list_:
                if self._acos_perms[w.name()]:
                    continue

                if self._perm in ("-w", "--"):
                    w.setPalette(self.pal)
                    w.setDisabled(True)
                    w.hide()
                    continue

                if self._perm == "r-":
                    w.setDisabled(True)

        for it in self._acos_perms.keys():
            from pineboolib import pncontrolsfactory

            w = fm.findChild(pncontrolsfactory.QWidget, it)
            if w:
                perm = self._acos_perms[it]
                if perm in ("-w", "--"):
                    if project.DGI.localDesktop():
                        w.setPalette(self.pal)
                    w.setDisabled(True)
                    w.hide()
                    continue

                if perm == "r-":
                    w.setDisabled(True)

            else:
                print("WARN: FLAccessControlFactory: No se encuentra el control %s para procesar ACLS." % it)

    def setFromObject(self, object) -> None:
        """Not implemented jet."""
        logger.warning("FLAccessControlForm::setFromObject %s", "No implementado todavía.")


class FLAccessControlTable(FLAccessControl):
    """FLAccessControlTable Class."""

    def __init__(self) -> None:
        """Inicialize."""

        super().__init__()
        self._acos_perms: Dict[str, str] = {}

    def type(self) -> str:
        """Return target type."""

        return "table"

    def processObject(self, obj: "PNTableMetaData") -> None:
        """Process PNTableMetaData belonging to a table."""

        if not obj:
            return

        tm = obj

        mask_perm = 0
        has_acos = True if self._acos_perms else False

        if self._perm:
            if self._perm[0] == "r":
                mask_perm = mask_perm + 2
            if self._perm[1] == "w":
                mask_perm = mask_perm + 1
        elif has_acos:
            mask_perm = 3
        else:
            return

        field_perm = ""
        mask_field_perm = 0

        fL = tm.fieldList()
        if not fL:
            return

        for it in fL:
            field = it
            mask_field_perm = mask_perm
            if has_acos and (field.name() in self._acos_perms.keys()):
                field_perm = self._acos_perms[field.name()]
                mask_field_perm = 0
                if field_perm[0] == "r":
                    mask_field_perm = mask_field_perm + 2

                if field_perm[1] == "w":
                    mask_field_perm = mask_field_perm + 1

            if mask_field_perm == 0:
                field.setVisible(False)
                field.setEditable(False)
            elif mask_field_perm == 1:
                field.setVisible(False)
                field.setEditable(True)
            elif mask_field_perm == 2:
                field.setVisible(True)
                field.setEditable(False)
            elif mask_field_perm == 3:
                field.setVisible(True)
                field.setEditable(True)

    def setFromObject(self, obj: "PNTableMetaData") -> None:
        """Apply permissions from a PNTableMetaData."""

        tm = obj
        if not tm:
            return

        if self._acos_perms:
            self._acos_perms.clear()
            del self._acos_perms

        self._acos_perms = {}
        # self._acos_perms.setAutoDelete(True)

        fL = tm.fieldList()
        if not fL:
            return

        permW = ""
        permR = ""
        for it in fL:
            permR = "-"
            permW = "-"
            if it.visible():
                permR = "r"
            if it.editable():
                permW = "w"
            self._acos_perms[it.name()] = "%s%s" % (permR, permW)


class FLAccessControlFactory(object):
    """FLAccessControlFactory Class."""

    def create(self, type_: str) -> "FLAccessControl":
        """Create a control instance according to the type that we pass."""

        if type_ is None:
            raise ValueError("type_ must be set")

        if type_ == "mainwindow":
            return FLAccessControlMainWindow()
        elif type_ == "form":
            return FLAccessControlForm()
        elif type_ == "table":
            return FLAccessControlTable()

        raise ValueError("type_ %r unknown" % type_)

    def type(self, obj: Any) -> str:
        """Return the type of instance target."""

        if obj is None:
            logger.warning("NO OBJ")

        ret_ = ""
        from pineboolib import pncontrolsfactory

        if isinstance(obj, pncontrolsfactory.QMainWindow):
            ret_ = "mainwindow"
        elif isinstance(obj, PNTableMetaData):
            ret_ = "table"
        elif isinstance(obj, pncontrolsfactory.FLFormDB):
            ret_ = "form"

        return ret_
