# # -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore
from pineboolib.pncontrolsfactory import FLFieldDB, FLTableDB
import logging
import weakref
import sys


class FormDBWidget(QtWidgets.QWidget):
    closed = QtCore.pyqtSignal()
    cursor_ = None
    parent_ = None
    iface = None
    signal_test = QtCore.pyqtSignal(str, QtCore.QObject)

    logger = logging.getLogger("pnControlsFactory.FormDBWidget")

    def __init__(self, action=None, project=None, parent=None):
        if project is not None:

            super().__init__(parent)

            self._module = sys.modules[self.__module__]
            self._module.connect = self._connect
            self._module.disconnect = self._disconnect
            self._action = action
            self.cursor_ = None
            self.parent_ = parent or parent.parentWidget() if parent and hasattr(parent, "parentWidget") else parent

            import pineboolib

            if isinstance(self.parent(), pineboolib.pncontrolsfactory.FLFormDB):
                self.form = self.parent()

            self._formconnections = set([])

        self._class_init()

    def _connect(self, sender, signal, receiver, slot):
        # print(" > > > connect:", sender, " signal ", str(signal))
        from pineboolib.pncontrolsfactory import connect

        signal_slot = connect(sender, signal, receiver, slot, caller=self)
        if not signal_slot:
            return False

        self._formconnections.add(signal_slot)

    def _disconnect(self, sender, signal, receiver, slot):
        # print(" > > > disconnect:", self)
        from pineboolib.pncontrolsfactory import disconnect

        signal_slot = disconnect(sender, signal, receiver, slot, caller=self)
        if not signal_slot:
            return False

        for sl in self._formconnections:

            if sl[0].signal == signal_slot[0].signal and sl[1].__name__ == signal_slot[1].__name__:
                self._formconnections.remove(sl)
                break

    def obj(self):
        return self

    def parent(self):
        return self.parent_

    def _class_init(self):
        """Constructor de la clase QS (p.ej. interna(context))"""
        pass

    def init(self):
        """Evento init del motor. Llama a interna_init en el QS"""
        pass

    def closeEvent(self, event):
        if not self._action:
            self._action = getattr(self.parent(), "_action")
        self.logger.debug("closeEvent para accion %r", self._action.name)
        self.closed.emit()
        event.accept()  # let the window close
        self.doCleanUp()

    def doCleanUp(self):
        self.clear_connections()
        if getattr(self, "iface", None) is not None:
            from pineboolib.pncontrolsfactory import check_gc_referrers

            check_gc_referrers("FormDBWidget.iface:" + self.iface.__class__.__name__, weakref.ref(self.iface), self._action.name)
            del self.iface.ctx
            del self.iface
            self._action.formrecord_widget = None

    def clear_connections(self):
        # Limpiar todas las conexiones hechas en el script
        for signal, slot in self._formconnections:
            try:
                signal.disconnect(slot)
                self.logger.debug("Señal desconectada al limpiar: %s %s" % (signal, slot))
            except Exception:
                # self.logger.exception("Error al limpiar una señal: %s %s" % (signal, slot))
                pass
        self._formconnections.clear()

    def child(self, child_name):
        try:
            ret = self.findChild(QtWidgets.QWidget, child_name, QtCore.Qt.FindChildrenRecursively)
            if ret is None and self.parent():
                ret = getattr(self.parent(), child_name, None)

            if ret is not None:
                if isinstance(ret, (FLFieldDB, FLTableDB)) and hasattr(ret, "_loaded"):
                    if ret._loaded is False:
                        ret.load()
            else:
                self.logger.warning("WARN: No se encontro el control %s", child_name)
            return ret
        except Exception:
            return None

    def cursor(self):
        # if self.cursor_:
        #    return self.cursor_

        cursor = None
        parent = self

        while cursor is None and parent:
            parent = parent.parentWidget()
            cursor = getattr(parent, "cursor_", None)
        if cursor:
            self.cursor_ = cursor
        else:
            if not self.cursor_:
                from pineboolib.pncontrolsfactory import aqApp
                from pineboolib.fllegacy.flsqlcursor import FLSqlCursor

                action = aqApp.db().manager().action(self._action.name)
                self.cursor_ = FLSqlCursor(action.name())

        return self.cursor_

    def __getattr__(self, name):
        from pineboolib.pncontrolsfactory import aqApp

        ret_ = (
            getattr(self.cursor_, name, None)
            or getattr(aqApp, name, None)
            or getattr(self.parent(), name, None)
            or getattr(self.parent().script, name, None)
        )
        if ret_:
            return ret_

    def __iter__(self):
        self._iter_current = None
        return self

    def __next__(self):
        self._iter_current = 0 if self._iter_current is None else self._iter_current + 1

        list_ = [attr for attr in dir(self) if not attr[0] == "_"]
        if self._iter_current >= len(list_):
            raise StopIteration

        return list_[self._iter_current]
