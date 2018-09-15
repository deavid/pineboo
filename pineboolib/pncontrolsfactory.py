# -*- coding: utf-8 -*-
import re
import os
from PyQt5 import QtCore

import pineboolib
import logging
import weakref

from pineboolib import decorators
from PyQt5.QtCore import QObject, Qt
from pineboolib.fllegacy.FLApplication import FLApplication

logger = logging.getLogger("PNControlsFactory")

"""
Conjunto de controles usados en Pineboo. Estos son cargados desde el DGI seleccionado en el proyecto
"""

"""
Devuelve un objecto a partir de su nombre
@param name, Nombre del objecto a buscar
@return objecto o None si no existe el objeto buscado
"""


def resolveObject(name):
    obj_ = getattr(pineboolib._DGI, name, None)
    if obj_:
        return obj_

    logger.warn("%s.resolveSDIObject no puede encontra el objeto %s en %s",
                __name__, name, pineboolib._DGI.alias())


# Clases Qt
QComboBox = resolveObject("QComboBox")
QTable = resolveObject("QTable")
QLayoutWidget = resolveObject("QLayoutWidget")
QToolButton = resolveObject("QToolButton")
QTabWidget = resolveObject("QTabWidget")
QLabel = resolveObject("QLabel")
QGroupBox = resolveObject("QGroupBox")
QListView = resolveObject("QListView")
QPushButton = resolveObject("QPushButton")
QTextEdit = resolveObject("QTextEdit")
QLineEdit = resolveObject("QLineEdit")
QDateEdit = resolveObject("QDateEdit")
QCheckBox = resolveObject("QCheckBox")
QWidget = resolveObject("QWidget")
QtWidgets = resolveObject("QtWidgets")
QColor = resolveObject("QColor")
QMessageBox = resolveObject("QMessageBox")
QButtonGroup = resolveObject("QButtonGroup")
QDialog = resolveObject("QDialog")
QVBoxLayout = resolveObject("QVBoxLayout")
QHBoxLayout = resolveObject("QHBoxLayout")
QFrame = resolveObject("QFrame")
QMainWindow = resolveObject("QMainWindow")
QSignalMapper = resolveObject("QSignalMapper")
QDomDocument = resolveObject("QDomDocument")
QMenu = resolveObject("QMenu")
QToolBar = resolveObject("QToolBar")
QListWidgetItem = resolveObject("QListWidgetItem")
QListViewWidget = resolveObject("QListViewWidget")
QPixmap = resolveObject("QPixmap")
QImage = resolveObject("QImage")
QIcon = resolveObject("QIcon")
QAction = resolveObject("QAction")
QActionGroup = resolveObject("QActionGroup")
QTreeWidget = resolveObject("QTreeWidget")
QTreeWidgetItem = resolveObject("QTreeWidgetItem")
QTreeWidgetItemIterator = resolveObject("QTreeWidgetItemIterator")
"""
QIconSet = resolveObject("QIconSet")
"""
# Clases FL
FLLineEdit = resolveObject("FLLineEdit")
FLTimeEdit = resolveObject("FLTimeEdit")
FLDateEdit = resolveObject("FLDateEdit")
FLPixmapView = resolveObject("FLPixmapView")
FLDomDocument = resolveObject("FLDomDocument")
FLListViewItem = resolveObject("FLListViewItem")
FLTable = resolveObject("FLTable")
FLDataTable = resolveObject("FLDataTable")
FLCheckBox = resolveObject("FLCheckBox")
FLTextEditOutput = resolveObject("FLTextEditOutput")
# Clases QSA
CheckBox = resolveObject("CheckBox")
TextEdit = QTextEdit
LineEdit = resolveObject("LineEdit")
FileDialog = resolveObject("FileDialog")
MessageBox = resolveObject("MessageBox")
RadioButton = resolveObject("RadioButton")
Color = QColor
Dialog = resolveObject("Dialog")
GroupBox = resolveObject("GroupBox")


class SysType(object):
    def __init__(self):
        self._name_user = None

    def nameUser(self):
        return pineboolib.project.conn.user()

    def interactiveGUI(self):
        return "Pineboo"

    def isLoadedModule(self, modulename):
        return modulename in pineboolib.project.conn.managerModules().listAllIdModules()

    def translate(self, text):
        return text

    def osName(self):
        from pineboolib.fllegacy.FLUtil import FLUtil
        util = FLUtil()
        return util.getOS()

    def nameBD(self):
        return pineboolib.project.conn.DBName()

    def toUnicode(self, text, format):
        return "%s" % text.encode(format).decode("utf-8")

    def Mr_Proper(self):
        pineboolib.project.conn.Mr_Proper()

    def installPrefix(self):
        return filedir("..")

    def __getattr__(self, fun_):
        return pineboolib.project.call("sys.iface.%s()" % fun_, [], None, True)

    def installACL(self, idacl):
        acl_ = pineboolib.project.acl()
        if acl_:
            acl_.installACL(idacl)

    def version(self):
        return pineboolib.project.version

    def processEvents(self):
        QtWidgets.qApp.processEvents()

    def write(self, encode_, dir_, contenido):
        f = codecs.open(dir_, encoding=encode_, mode="w+")
        f.write(contenido)
        f.seek(0)
        f.close()

    def cleanupMetaData(self, connName="default"):
        pineboolib.project.conn.database(connName).manager().cleanupMetaData()

    def updateAreas(self):
        pineboolib.project.initToolBox()

    def isDebuggerMode(self):
        from pineboolib.fllegacy.FLSettings import FLSettings
        return FLSettings().readBoolEntry("application/isDebuggerMode")

    def isNebulaBuild(self):
        return False

    def setCaptionMainWidget(self, t):
        aqApp.setCaptionMainWidget(t)

    def isQuickBuild(self):
        return False

    def isDebuggerEnabled(self):
        return True

    def isUserBuild(self):
        return False

    def nameDriver(self, connName="default"):
        return pineboolib.project.conn.database(connName).driverName()

    def addDatabase(self, connName="default"):
        return pineboolib.project.conn.useConn(connName)()

    def removeDatabase(self, connName="default"):
        return pineboolib.project.conn.removeConn(connName)

    def runTransaction(self, f, oParam):

        curT = FLSqlCursor("flfiles")
        curT.transaction(False)
        # gui = self.interactiveGUI()
        # if gui:
        #   AQS.Application_setOverrideCursor(AQS.WaitCursor);

        errorMsg = None
        try:
            valor = f(oParam)
            errorMsg = getattr(oParam, "errorMsg", None)
            if valor:
                curT.commit()
            else:
                curT.rollback()
                # if gui:
                #   AQS.Application_restoreOverrideCursor();
                if errorMsg is None:
                    self.warnMsgBox(self.translate(u"Error al ejecutar la función"))
                else:
                    self.warnMsgBox(errorMsg)
                return False

        except Exception:
            curT.rollback()
            # if gui:
            #   AQS.Application_restoreOverrideCursor();
            if errorMsg is None:
                self.warnMsgBox(self.translate(u"Error al ejecutar la función"))
            else:
                self.warnMsgBox(errorMsg)
            return False

        # if gui:
        #   AQS.Application_restoreOverrideCursor();
        return valor

    def infoMsgBox(self, msg):

        if not isinstance(msg, str):
            return
        msg += "\n"
        if self.interactiveGUI():
            MessageBox.information(msg, MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton, "Pineboo")
        else:
            print("INFO ", msg)

    def warnMsgBox(self, msg):

        if not isinstance(msg, str):
            return
        msg += "\n"
        if self.interactiveGUI():
            MessageBox.warning(msg, MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton, "Pineboo")
        else:
            print("WARN ", msg)

    def errorMsgBox(self, msg):

        if not isinstance(msg, str):
            return
        msg += "\n"
        if self.interactiveGUI():
            MessageBox.critical(msg, MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton, "Pineboo")
        else:
            print("ERROR ", msg)


class System(object):

    def setenv(name, val):
        os.environ[name] = val

    def getenv(self, name):
        return os.environ(name)


class ProxySlot:
    PROXY_FUNCTIONS = {}

    def __init__(self, remote_fn, receiver, slot):
        self.key = "%r.%r->%r" % (remote_fn, receiver, slot)
        if self.key not in self.PROXY_FUNCTIONS:
            weak_fn = weakref.WeakMethod(remote_fn)
            weak_receiver = weakref.ref(receiver)
            self.PROXY_FUNCTIONS[self.key] = proxy_fn(weak_fn, weak_receiver, slot)
        self.proxy_function = self.PROXY_FUNCTIONS[self.key]

    def getProxyFn(self):
        return self.proxy_function


def proxy_fn(wf, wr, slot):
    def fn(*args, **kwargs):
        f = wf()
        if not f:
            return None
        r = wr()
        if not r:
            return None

        # Apaño para conectar los clicked()
        if args == (False,):
            return f()

        return f(*args, **kwargs)
    return fn


def connect(sender, signal, receiver, slot, caller=None):
    if caller is not None:
        logger.debug("* * * Connect:: %s %s %s %s %s", caller, sender, signal, receiver, slot)
    else:
        logger.debug("? ? ? Connect:: %s %s %s %s", sender, signal, receiver, slot)
    signal_slot = solve_connection(sender, signal, receiver, slot)
    if not signal_slot:
        return False
    # http://pyqt.sourceforge.net/Docs/PyQt4/qt.html#ConnectionType-enum
    conntype = QtCore.Qt.QueuedConnection | QtCore.Qt.UniqueConnection
    signal, slot = signal_slot

    try:
        signal.connect(slot, type=conntype)
    except Exception:
        logger.exception("ERROR Connecting: %s %s %s %s", sender, signal, receiver, slot)
        return False

    return signal_slot


def disconnect(sender, signal, receiver, slot, caller=None):
    signal_slot = solve_connection(sender, signal, receiver, slot)
    if not signal_slot:
        return False
    signal, slot = signal_slot
    try:
        signal.disconnect(slot)
    except Exception:
        pass

    return signal_slot


def solve_connection(sender, signal, receiver, slot):
    if sender is None:
        logger.error("Connect Error:: %s %s %s %s", sender, signal, receiver, slot)
        return False

    m = re.search(r"^(\w+)\.(\w+)(\(.*\))?", slot)
    if slot.endswith("()"):
        slot = slot[:-2]

    if isinstance(sender, QDateEdit):
        if "valueChanged" in signal:
            signal = signal.replace("valueChanged", "dateChanged")

    if receiver.__class__.__name__ == "FormInternalObj" and slot == "accept":
        receiver = receiver.parent()

    remote_fn = getattr(receiver, slot, None)

    sg_name = re.sub(' *\(.*\)', '', signal)
    oSignal = getattr(sender, sg_name, None)
    if not oSignal and sender.__class__.__name__ == "FormInternalObj":
        oSignal = getattr(sender.parent(), sg_name, None)
    if not oSignal:
        logger.error("ERROR: No existe la señal %s para la clase %s", signal, sender.__class__.__name__)
        return

    if remote_fn:
        if receiver.__class__.__name__ == "FLFormSearchDB" and slot == "accept":
            return oSignal, remote_fn

        pS = ProxySlot(remote_fn, receiver, slot)
        proxyfn = pS.getProxyFn()
        return oSignal, proxyfn
    elif m:
        remote_obj = getattr(receiver, m.group(1), None)
        if remote_obj is None:
            raise AttributeError("Object %s not found on %s" %
                                 (remote_obj, str(receiver)))
        remote_fn = getattr(remote_obj, m.group(2), None)
        if remote_fn is None:
            raise AttributeError("Object %s not found on %s" %
                                 (remote_fn, remote_obj))
        return oSignal, remote_fn

    elif isinstance(receiver, QtCore.QObject):
        if isinstance(slot, str):
            oSlot = getattr(receiver, slot, None)
            if not oSlot:
                return False
        return oSignal, oSlot
    else:
        logger.error(
            "Al realizar connect %s:%s -> %s:%s ; "
            "el slot no se reconoce y el receptor no es QObject.",
            sender, signal, receiver, slot)
    return False


aqApp = FLApplication()


class FormDBWidget(QWidget):
    closed = QtCore.pyqtSignal()
    cursor_ = None
    parent_ = None
    iface = None

    logger = logging.getLogger("pnControlsFactory.FormDBWidget")

    def __init__(self, action, project, parent=None):
        import pineboolib
        if not pineboolib.project._DGI.useDesktop():
            self._class_init()
            return

        if pineboolib.project._DGI.localDesktop():
            self.remote_widgets = {}

        super(FormDBWidget, self).__init__(parent)
        import sys
        self._module = sys.modules[self.__module__]
        self._module.connect = self._connect
        self._module.disconnect = self._disconnect
        self._action = action
        self.cursor_ = None
        self.parent_ = parent or parent.parentWidget()

        self._formconnections = set([])
        try:
            self._class_init()

        except Exception as e:
            self.logger.exception("Error al inicializar la clase iface de QS:")

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
        try:
            self._formconnections.remove(signal_slot)
        except KeyError:
            self.logger.exception("Error al eliminar una señal que no se encuentra")

    # def __del__(self):
    #    self.doCleanUp()
    #    print("FormDBWidget: Borrando form para accion %r %s %s" % (self._action.name, self.iface, self))

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
        can_exit = True
        if not self._action:
            self._action = getattr(self.parent(), "_action")
        self.logger.debug("closeEvent para accion %r", self._action.name)
        check_gc_referrers("FormDBWidget:" + self.__class__.__name__,
                           weakref.ref(self), self._action.name)
        if can_exit:
            self.closed.emit()
            event.accept()  # let the window close
            self.doCleanUp()
        else:
            event.ignore()
            return

    def doCleanUp(self):
        # Limpiar todas las conexiones hechas en el script
        for signal, slot in self._formconnections:
            try:
                signal.disconnect(slot)
                self.logger.debug("Señal desconectada al limpiar: %s %s" % (signal, slot))
            except Exception:
                self.logger.exception("Error al limpiar una señal: %s %s" % (signal, slot))
        self._formconnections.clear()

        if getattr(self, 'iface', None) is not None:
            check_gc_referrers("FormDBWidget.iface:" + self.iface.__class__.__name__,
                               weakref.ref(self.iface), self._action.name)
            del self.iface.ctx
            del self.iface
            self._action.formrecord_widget = None
            del self

    def child(self, childName):
        try:
            parent = self
            ret = None
            while parent and not ret:
                ret = parent.findChild(QtWidgets.QWidget, childName)
                if not ret:
                    parent = parent.parentWidget()

                loaded = getattr(ret, "_loaded", None)
                if loaded is False:
                    ret.load()

        except RuntimeError as rte:
            # FIXME: A veces intentan buscar un control que ya está siendo eliminado.
            # ... por lo que parece, al hacer el close del formulario no se desconectan sus señales.
            print("ERROR: Al buscar el control %r encontramos el error %r" %
                  (childName, rte))
            print_stack(8)
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
                self.logger.warn("WARN: No se encontro el control %s", childName)

        # Para inicializar los controles si se llaman desde qsa antes de
        # mostrar el formulario.
        #from pineboolib.fllegacy.FLFieldDB import FLFieldDB
        # if isinstance(ret, FLFieldDB):
        #    if not ret.cursor():
        #        ret.initCursor()
        #    if not ret.editor_ and not ret.editorImg_:
        #        ret.initEditor()

        #from pineboolib.fllegacy.FLTableDB import FLTableDB
        # if isinstance(ret, FLTableDB):
        #    if not ret.tableRecords_ and self.cursor_:
        #        ret.tableRecords()
        #        ret.setTableRecordsCursor()

        # else:
        #    print("DEBUG: Encontrado el control %r: %r" % (childName, ret))
        return ret

    def cursor(self):
        # if self.cursor_:
        #    return self.cursor_

        cursor = None
        parent = self

        while not cursor and parent:
            parent = parent.parentWidget()
            cursor = getattr(parent, "cursor_", None)
        if cursor:
            self.cursor_ = cursor
        else:
            if not self.cursor_:
                from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
                self.cursor_ = FLSqlCursor(self._action)

        return self.cursor_

    def __getattr__(self, name):
        ret_ = getattr(self.cursor_, name, None) or getattr(aqApp, name, None)
        if ret_:
            return ret_


def check_gc_referrers(typename, w_obj, name):
    import threading
    import time

    def checkfn():
        import gc
        time.sleep(2)
        gc.collect()
        obj = w_obj()
        if not obj:
            return
        # TODO: Si ves el mensaje a continuación significa que "algo" ha dejado
        # ..... alguna referencia a un formulario (o similar) que impide que se destruya
        # ..... cuando se deja de usar. Causando que los connects no se destruyan tampoco
        # ..... y que se llamen referenciando al código antiguo y fallando.
        # print("HINT: Objetos referenciando %r::%r (%r) :" % (typename, obj, name))
        for ref in gc.get_referrers(obj):
            if isinstance(ref, dict):
                x = []
                for k, v in ref.items():
                    if v is obj:
                        k = "(**)" + k
                        x.insert(0, k)
                # print(" - dict:", repr(x), gc.get_referrers(ref))
            else:
                if "<frame" in str(repr(ref)):
                    continue
                # print(" - obj:", repr(ref), [x for x in dir(ref) if getattr(ref, x) is obj])

    threading.Thread(target=checkfn).start()


def print_stack(maxsize=1):
    for tb in traceback.format_list(traceback.extract_stack())[1:-2][-maxsize:]:
        print(tb.rstrip())
