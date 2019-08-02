# # -*- coding: utf-8 -*-
from PyQt5 import QtCore  # type: ignore
from typing import Set, Tuple, Any, Dict
import sys
import weakref


class FormDBWidget(QtCore.QObject):
    """description of class"""

    closed = QtCore.pyqtSignal()
    cursor_ = None
    parent_ = None
    iface = None
    signal_test = QtCore.pyqtSignal(str, QtCore.QObject)
    _loaded = None

    _cursors: Dict[str, Any]

    def __init__(self, action=None, project=None, parent=None):
        if project is None:
            parent = QtCore.QObject()

        super().__init__(parent)

        self._module = sys.modules[self.__module__]
        self._module.connect = self._connect
        self._module.disconnect = self._disconnect
        self._action = action
        self.cursor_ = None
        self._loaded = None

        self.parent_ = parent
        self._cursors = {}

        # import pineboolib
        # if isinstance(self.parent(), pineboolib.pncontrolsfactory.FLFormDB):
        #    self.form = self.parent()

        self._formconnections: Set[Tuple] = set([])
        self._class_init()

    def _connect(self, sender, signal, receiver, slot):
        # print(" > > > connect:", sender, " signal ", str(signal))
        from pineboolib.application import connections

        signal_slot = connections.connect(sender, signal, receiver, slot, caller=self)
        if not signal_slot:
            return False
        self._formconnections.add(signal_slot)

    def _disconnect(self, sender, signal, receiver, slot):
        # print(" > > > disconnect:", self)
        from pineboolib.application import connections

        signal_slot = connections.disconnect(sender, signal, receiver, slot, caller=self)
        if not signal_slot:
            return False

        if signal_slot in self._formconnections:
            self._formconnections.remove(signal_slot)
        else:
            self.logger.warning("Error al eliminar una señal que no se encuentra")

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
            from pineboolib.core.garbage_collector import check_gc_referrers

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
        pass
        """
        try:
            parent = self
            ret = None
            while parent and not ret:
                ret = parent.findChild(QtWidgets.QWidget, child_name)
                if not ret:
                    parent = parent.parentWidget()

            loaded = getattr(ret, "_loaded", None)
            if loaded is False:
                ret.load()

        except RuntimeError as rte:
            # FIXME: A veces intentan buscar un control que ya está siendo eliminado.
            # ... por lo que parece, al hacer el close del formulario no se desconectan sus señales.
            print("ERROR: Al buscar el control %r encontramos el error %r" %
                  (child_name, rte))

            from pineboolib import pncontrolsfactory
            pncontrolsfacotry.print_stack(8)
            import gc
            gc.collect()
            print("HINT: Objetos referenciando FormDBWidget::%r (%r) : %r" %
                  (self, self._action.name, gc.get_referrers(self)))
            if hasattr(self, 'iface'):
                print("HINT: Objetos referenciando FormDBWidget.iface::%r : %r" % (
                    self.iface, gc.get_referrers(self.iface)))
            ret = None
        else:
            if ret is None:
                self.logger.warning("WARN: No se encontro el control %s", child_name)
        return ret
        """

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
                from pineboolib.fllegacy.flsqlcursor import FLSqlCursor

                self.cursor_ = FLSqlCursor(self._action)

        return self.cursor_

    def parentWidget(self):
        return self.parent_

    def __getattr__(self, name):
        from pineboolib.fllegacy.flapplication import aqApp

        ret_ = (
            getattr(self.cursor_, name, None)
            or getattr(aqApp, name, None)
            or getattr(self.parent(), name, None)
            or getattr(self._action.script, name, None)
        )
        if ret_:
            return ret_
        # else:
        #    return getattr(self.iface, name, None)

    def __iter__(self):
        self._iter_current = None
        return self

    def __next__(self):
        self._iter_current = 0 if self._iter_current is None else self._iter_current + 1

        list_ = [attr for attr in dir(self) if not attr[0] == "_"]
        if self._iter_current >= len(list_):
            raise StopIteration

        return list_[self._iter_current]
