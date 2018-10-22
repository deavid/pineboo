# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

from pineboolib.fllegacy.fltablemetadata import FLTableMetaData
from pineboolib.fllegacy.flaccesscontrol import FLAccessControl
from pineboolib.fllegacy.flutil import FLUtil
from pineboolib import decorators
import pineboolib


try:
    QString = unicode
except NameError:
    # Python 3
    QString = str


class FLAccessControlFactory(object):

    @decorators.BetaImplementation
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

    @decorators.BetaImplementation
    def type(self, obj):
        if not obj:
            print("NO OBJ")

        from pineboolib.fllegacy.FLFormDB import FLFormDB
        if isinstance(obj, QtWidgets.QMainWindow):
            return "mainwindow"
        if isinstance(obj, FLTableMetaData):
            return "table"
        if isinstance(obj, FLFormDB):
            return "form"

        return QString("")


class FLAccessControlMainWindow(FLAccessControl):

    acosPerms_ = None
    perm_ = None

    def __init__(self):
        super(FLAccessControlMainWindow, self).__init__()

    """
  Dado un objeto general (tipo QObject) de alto nivel, identifica si existe un controlador que puede controlar
  su acceso devolviendo en tal caso el nombre de tipo asignado.

  @param Objeto de alto nivel del cual se quiere conocer su tipo.
  @return Devuelve el nombre del tipo asociado al objeto de alto nivel dado, si existe controlador de acceso para él,
  en caso contrario devuelve una cadena vacía.
    """
    @decorators.BetaImplementation
    def type(self):
        return "mainwindow"

    @decorators.BetaImplementation
    def processObject(self, obj):
        mw = QtGui.QMainWindow(obj)
        if not mw or not self.acosPerms_:
            return

        if not self.perm_.isEmpty():
            l = QtCore.QObjectList(mw.queryList("QAction"))
            ito = QtCore.QObjectListIt(l)
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

    @decorators.BetaImplementation
    def setFromObject(self, object):
        print("FLAccessControlMainWindow::setFromObject %s" %
              FLUtil.translate(self, "app", "No implementado todavía."))


class FLAccessControlForm(FLAccessControl):

    pal = None
    acosPerms_ = None
    perm_ = None

    @decorators.BetaImplementation
    def __init__(self):
        super(FLAccessControlForm, self).__init__()
        if pineboolib.project._DGI.localDesktop():
            self.pal = QtGui.QPalette()
            # cg = QtGui.QPalette()
            from PyQt5.Qt import qApp
            bg = QtGui.QColor(qApp.palette().color(
                QtGui.QPalette.Active, QtGui.QPalette.Background))
            # cg.setColor(QtGui.QPalette.Foreground, bg)
            # cg.setColor(QtGui.QPalette.Text, bg)
            # cg.setColor(QtGui.QPalette.ButtonText, bg)
            # cg.setColor(QtGui.QPalette.Base, bg)
            # cg.setColor(QtGui.QPalette.Background, bg)
            # self.pal.setColor(QtGui.QPalette.Disabled, cg)
            self.pal.setColor(QtGui.QPalette.Foreground, bg)
            self.pal.setColor(QtGui.QPalette.Text, bg)
            self.pal.setColor(QtGui.QPalette.ButtonText, bg)
            self.pal.setColor(QtGui.QPalette.Base, bg)
            self.pal.setColor(QtGui.QPalette.Background, bg)
    """
  @return El tipo del que se encarga; "form".
    """
    @decorators.BetaImplementation
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
            w = fm.findChild(QtWidgets.QWidget, it)
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
                print(
                    "WARN: FLAccessControlFactory: No se encuentra el control %s para procesar ACLS." % it)

    @decorators.BetaImplementation
    def setFromObject(self, object):
        print("FLAccessControlform::setFromObject %s" %
              FLUtil.translate(self, "app", "No implementado todavía."))


class FLAccessControlTable(FLAccessControl):

    def __init__(self):
        super(FLAccessControlTable, self).__init__()

    def type(self):
        return "table"

    def processObject(self, obj):
        if not obj:
            return

        tm = obj

        maskPerm = 0
        hasAcos = True if self.acosPerms_ else False

        if self.perm_:
            if self.perm_[0] == "r":
                maskPerm = maskPerm + 2
            if self.perm_[1] == "w":
                maskPerm = maskPerm + 1
        elif hasAcos:
            maskPerm = 8
        else:
            return

        fieldPerm = ""
        maskFieldPerm = 0

        fL = tm.fieldList()
        if not fL:
            return

        field = None
        for it in fL:
            field = it
            maskFieldPerm = maskPerm
            if hasAcos and (field.name() in self.acosPerms_.keys()):
                fieldPerm = self.acosPerms_[field.name()]
                maskFieldPerm = 0
                if fieldPerm[0] == "r":
                    maskFieldPerm = maskFieldPerm + 2

                if fieldPerm[1] == "w":
                    maskFieldPerm = maskFieldPerm + 1

            if maskFieldPerm == 0:
                field.setVisible(False)
                field.setEditable(False)
            elif maskFieldPerm == 1:
                field.setVisible(False)
                field.setEditable(True)
            elif maskFieldPerm == 2:
                field.setVisible(True)
                field.setEditable(False)
            elif maskFieldPerm == 3:
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

        permW = None
        permR = None
        for it in fL:
            permR = '-'
            permW = '-'
            if it.visible():
                permR = 'r'
            if it.editable():
                permW = 'w'
            self.acosPerms_[it.name()] = "%s%s" % (permR, permW)
