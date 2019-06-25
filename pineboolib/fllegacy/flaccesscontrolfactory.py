# -*- coding: utf-8 -*-

from PyQt5 import QtCore

from pineboolib.fllegacy.fltablemetadata import FLTableMetaData
from pineboolib.fllegacy.flaccesscontrol import FLAccessControl

import pineboolib


class FLAccessControlFactory(object):
    def create(self, type_):
        if type_ is None:
            return False

        if type_ == "mainwindow":
            return FLAccessControlMainWindow()
        elif type_ == "form":
            return FLAccessControlForm()
        elif type_ == "table":
            return FLAccessControlTable()

        return False

    def type(self, obj):
        if obj is None:
            print("NO OBJ")

        ret_ = ""
        from pineboolib.pncontrolsfactory import FLFormDB, QMainWindow

        if isinstance(obj, QMainWindow):
            ret_ = "mainwindow"
        elif isinstance(obj, FLTableMetaData):
            ret_ = "table"
        elif isinstance(obj, FLFormDB):
            ret_ = "form"

        return ret_


class FLAccessControlMainWindow(FLAccessControl):
    def __init__(self):
        super(FLAccessControlMainWindow, self).__init__()

    """
  Dado un objeto general (tipo QObject) de alto nivel, identifica si existe un controlador que puede controlar
  su acceso devolviendo en tal caso el nombre de tipo asignado.

  @param Objeto de alto nivel del cual se quiere conocer su tipo.
  @return Devuelve el nombre del tipo asociado al objeto de alto nivel dado, si existe controlador de acceso para él,
  en caso contrario devuelve una cadena vacía.
    """

    def type(self):
        return "mainwindow"

    def processObject(self, obj):
        from pineboolib.pncontrolsfactory import QMainWindow

        mw = QMainWindow(obj)
        if not mw or not self.acosPerms_:
            return

        if not self.perm_:
            list1 = QtCore.QObjectList(mw.queryList("QAction"))
            ito = QtCore.QObjectListIt(list1)
            a = QtCore.QAction

            while not ito.current() == 0:
                a = ito.current()
                ++ito
                if self.acosPerm_[a.name()]:
                    continue
                if self.perm_ == "-w" or self.perm_ == "--":
                    a.setVisible(False)

            del l

        it = QtCore.QDictIterator(self.acosPerms_)
        for i in range(len(it.current())):
            a = mw.child(it.currentKey(), "QAction")
            if a:
                perm = it
                if perm in ("-w", "--"):
                    a.setVisible(False)

    def setFromObject(self, object):
        from pineboolib.fllegacy.flutil import FLUtil

        print("FLAccessControlMainWindow::setFromObject %s" % FLUtil.translate(self, "app", "No implementado todavía."))


class FLAccessControlForm(FLAccessControl):
    def __init__(self):
        super(FLAccessControlForm, self).__init__()
        if pineboolib.project._DGI.localDesktop():
            from PyQt5.Qt import qApp
            from PyQt5 import QtGui

            self.pal = QtGui.QPalette()
            bg = QtGui.QColor(qApp.palette().color(QtGui.QPalette.Active, QtGui.QPalette.Background))

            self.pal.setColor(QtGui.QPalette.Foreground, bg)
            self.pal.setColor(QtGui.QPalette.Text, bg)
            self.pal.setColor(QtGui.QPalette.ButtonText, bg)
            self.pal.setColor(QtGui.QPalette.Base, bg)
            self.pal.setColor(QtGui.QPalette.Background, bg)

    """
  @return El tipo del que se encarga; "form".
    """

    def type(self):
        return "form"

    """
  Procesa objetos que son de la clase FLFormDB.

  Sólo controla los hijos del objeto que son de la clase QWidget,y sólo
  permite hacerlos no visibles o no editables. En realidad hacerlos
  no visibles significa que sean no editables y modficando la paleta para
  que toda la región del componente sea mostrada en color negro. Los permisos
  que acepta son :

  - "-w" o "--" (no_lectura/escritura o no_lectura/no_escritura) -> no visible
  - "r-" (lectura/no_escritura) -> no editable

  Esto permite que cualquier componente de un formulario de AbanQ ( FLFormDB,
  FLFormRecordDB y FLFormSearchDB) se pueda hacer no visible o no editable a conveniencia.
    """

    def processObject(self, obj):
        fm = obj
        if not fm or not self.acosPerms_:
            return

        if self.perm_:
            list_ = fm.children()

            for w in list_:
                if self.acosPerms_[w.name()]:
                    continue

                if self.perm_ in ("-w", "--"):
                    w.setPalette(self.pal)
                    w.setDisabled(True)
                    w.hide()
                    continue

                if self.perm_ == "r-":
                    w.setDisabled(True)

        for it in self.acosPerms_.keys():
            from pineboolib.pncontrolsfactory import QWidget

            w = fm.findChild(QWidget, it)
            if w:
                perm = self.acosPerms_[it]
                if perm in ("-w", "--"):
                    if pineboolib.project._DGI.localDesktop():
                        w.setPalette(self.pal)
                    w.setDisabled(True)
                    w.hide()
                    continue

                if perm == "r-":
                    w.setDisabled(True)

            else:
                print("WARN: FLAccessControlFactory: No se encuentra el control %s para procesar ACLS." % it)

    def setFromObject(self, object):
        print("FLAccessControlform::setFromObject: No implementado todavía.")


class FLAccessControlTable(FLAccessControl):
    def __init__(self):
        super(FLAccessControlTable, self).__init__()

    def type(self):
        return "table"

    def processObject(self, obj):
        if not obj:
            return

        tm = obj

        mask_perm = 0
        has_acos = True if self.acosPerms_ else False

        if self.perm_:
            if self.perm_[0] == "r":
                mask_perm = mask_perm + 2
            if self.perm_[1] == "w":
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
            if has_acos and (field.name() in self.acosPerms_.keys()):
                field_perm = self.acosPerms_[field.name()]
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

    def setFromObject(self, obj):
        tm = obj
        if not tm:
            return

        if self.acosPerms_:
            self.acosPerms_.clear()
            del self.acosPerms_

        self.acosPerms_ = {}
        # self.acosPerms_.setAutoDelete(True)

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
            self.acosPerms_[it.name()] = "%s%s" % (permR, permW)
