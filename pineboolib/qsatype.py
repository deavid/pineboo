# -*- coding: utf-8 -*-
import logging
import os
import fnmatch
import weakref
import re
import codecs
import traceback

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QTabWidget, QTextEdit, QWidget, QIODevice
from PyQt5.QtXml import QDomDocument
from PyQt5.QtWidgets import QApplication

# AQSObjects
from pineboolib.fllegacy.aqsobjects.AQSettings import AQSettings
from pineboolib.fllegacy.aqsobjects.AQUtil import AQUtil as AQUtil_Legacy
from pineboolib.fllegacy.aqsobjects.AQSql import AQSql as AQSql_Legacy

from pineboolib.fllegacy.FLPosPrinter import FLPosPrinter as FLPosPrinter_Legacy

from pineboolib.fllegacy.FLFormSearchDB import FLFormSearchDB
from pineboolib.fllegacy import FLSqlQuery as FLSqlQuery_Legacy
from pineboolib.fllegacy import FLSqlCursor as FLSqlCursor_Legacy
from pineboolib.fllegacy import FLTableDB as FLTableDB_Legacy
from pineboolib.fllegacy import FLFieldDB as FLFieldDB_Legacy
from pineboolib.fllegacy import FLUtil as FLUtil_Legacy
from pineboolib.fllegacy import FLReportViewer as FLReportViewer_Legacy

from pineboolib.utils import filedir

from pineboolib import decorators

import pineboolib

util = FLUtil_Legacy.FLUtil()  # <- para cuando QS erróneo usa util sin definirla
AQUtil = AQUtil_Legacy


logger = logging.getLogger(__name__)


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
        util = FLUtil()
        return util.getOS()

    def nameBD(self):
        return pineboolib.project.conn.DBName()

    def setCaptionMainWidget(self, value):
        self.mainWidget().setWindowTitle("Pineboo - %s" % value)
        pass

    def toUnicode(self, text, format):
        return u"%s" % text

    def mainWidget(self):
        if pineboolib.project._DGI.localDesktop():
            return pineboolib.project.main_window.ui_
        else:
            return None

    def Mr_Proper(self):
        pineboolib.project.conn.Mr_Proper()

    def installPrefix(self):
        return filedir("..")

    def __getattr__(self, fun_):
        ret_ = eval(fun_, pineboolib.qsatype.__dict__)
        if ret_ is not None:
            return ret_

    def installACL(self, idacl):
        acl_ = pineboolib.project.acl()
        if acl_:
            acl_.installACL(idacl)

    def version(self):
        return pineboolib.project.version

    def processEvents(self):
        QApplication.processEvents()

    @decorators.BetaImplementation
    def reinit(self):
        self.processEvents()
        pineboolib.project.main_window.saveState()
        pineboolib.project.run()
        pineboolib.project.main_window.areas = []
        # FIXME: Limpiar el ui para no duplicar controles
        pineboolib.project.main_window.load()
        pineboolib.project.main_window.show()
        pineboolib.project.call("sys.iface._class_init()", [], None, True)

    def write(self, encode_, dir_, contenido):
        f = codecs.open(dir_, encoding=encode_, mode="w+")
        f.write(contenido)
        f.seek(0)
        f.close()

    def cleanupMetaData(self, connName="default"):
        pineboolib.project.conn.database(connName).manager().cleanupMetaData()

    def updateAreas(self):
        pineboolib.project.initToolBox()

    @decorators.NotImplementedWarn
    def isDebuggerMode(self):
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


sys = SysType()


class StructMyDict(dict):

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, name, value):
        self[name] = value


def Function(args, source):
    # Leer código QS embebido en Source
    # asumir que es una funcion anónima, tal que:
    #  -> function($args) { source }
    # compilar la funcion y devolver el puntero
    qs_source = """
function anon(%s) {
    %s
} """ % (args, source)
    print("Compilando QS en línea: ", qs_source)
    from pineboolib.flparser import flscriptparse
    from pineboolib.flparser import postparse
    from pineboolib.flparser.pytnyzer import write_python_file, string_template
    import io
    prog = flscriptparse.parse(qs_source)
    tree_data = flscriptparse.calctree(prog, alias_mode=0)
    ast = postparse.post_parse(tree_data)
    tpl = string_template

    f1 = io.StringIO()

    write_python_file(f1, ast, tpl)
    pyprog = f1.getvalue()
    print("Resultado: ", pyprog)
    glob = {}
    loc = {}
    exec(pyprog, glob, loc)
    # ... y lo peor es que funciona. W-T-F.

    # return loc["anon"]
    return getattr(loc["FormInternalObj"], "anon")


def Object(x=None):
    if x is None:
        x = {}
    return StructMyDict(x)

# def Array(x=None):
    # try:
    # if x is None: return {}
    # else: return list(x)
    # except TypeError:
    # return [x]


class Array(object):

    dict_ = None
    key_ = None
    names_ = None

    def __init__(self, *args):
        self.names_ = []
        self.dict_ = {}

        if not len(args):
            return
        elif isinstance(args[0], int) and len(args) == 1:
            return
        elif isinstance(args[0], list):
            for field in args[0]:
                self.names_.append(field)
                self.dict_[field] = field

        elif isinstance(args[0], str):
            for f in args:
                self.__setitem__(f, f)
        else:
            self.dict_ = args

    def __setitem__(self, key, value):
        # if isinstance(key, int):
        #   key = str(key)
        if key not in self.names_:
            self.names_.append(key)

        self.dict_[key] = value

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.dict_[self.names_[key]]
        else:
            # print("QSATYPE.DEBUG: Array.getItem() " ,key,  self.dict_[key])
            return self.dict_[key]

    def __getattr__(self, k):
        if k == 'length':
            return len(self.dict_)
        else:
            return self.dict_[k]

    def __len__(self):
        len_ = 0

        for l in self.dict_:
            len_ = len_ + 1

        return len_


class FileDialog(QtWidgets.QFileDialog):

    def getOpenFileName(*args):
        obj = None
        parent = QtWidgets.QApplication.activeModalWidget()
        if len(args) == 1:
            obj = QtWidgets.QFileDialog.getOpenFileName(parent, str(args[0]))
        elif len(args) == 2:
            obj = QtWidgets.QFileDialog.getOpenFileName(parent, str(args[0]), str(args[1]))
        elif len(args) == 3:
            obj = QtWidgets.QFileDialog.getOpenFileName(parent, str(args[0]), str(args[1]), str(args[2]))
        elif len(args) == 4:
            obj = QtWidgets.QFileDialog.getOpenFileName(parent, str(args[0]), str(args[1]), str(args[2]), str(args[3]))

        if obj is None:
            return None

        return obj[0]

    def getExistingDirectory(basedir=None, caption=None):
        if not basedir:
            basedir = filedir("..")

        if pineboolib.project._DGI.localDesktop():
            parent = pineboolib.project.main_window.ui_
            ret = QtWidgets.QFileDialog.getExistingDirectory(parent, caption, basedir, QtWidgets.QFileDialog.ShowDirsOnly)
            if ret:
                ret = ret + "/"

            return ret


def Boolean(x=False):
    return bool(x)


class Math(object):

    def abs(x):
        return math.fabs(x)

    def ceil(x):
        return math.ceil(x)

    def floor(x):
        return math.floor(x)

    def pow(x, y):
        return math.pow(x, y)


def parseFloat(x):
    if x is None:
        return 0
    return float(x)


def parseString(objeto):
    try:
        return objeto.toString()
    except Exception:
        return str(objeto)


def parseInt(x):
    if x is None:
        return 0
    return int(x)


def isNaN(x):
    if not x:
        return True

    try:
        float(x)
        return False
    except ValueError:
        return True


def ustr(*t1):

    return "".join([ustr1(t) for t in t1])


def ustr1(t):
    if isinstance(t, str):
        return t

    if isinstance(t, float):
        try:
            t = int(t)
        except Exception:
            pass

    # if isinstance(t, QtCore.QString): return str(t)
    if isinstance(t, str):
        return str(t, "UTF-8")
    try:
        return str(t)
    except Exception as e:
        logger.exception("ERROR Coercing to string: %s", repr(t))
        return None


class Date(object):

    @classmethod
    def parse(cls, value):
        return QtCore.QDate.fromString(value)


QMessageBox = QtWidgets.QMessageBox


class MessageBox(QMessageBox):
    @classmethod
    def msgbox(cls, typename, text, button0, button1=None, button2=None, title=None, form=None):
        if title or form:
            logger.warn("MessageBox: Se intentó usar título y/o form, y no está implementado.")
        icon = QMessageBox.NoIcon
        title = "Message"
        if typename == "question":
            icon = QMessageBox.Question
            title = "Question"
        elif typename == "information":
            icon = QMessageBox.Information
            title = "Information"
        elif typename == "warning":
            icon = QMessageBox.Warning
            title = "Warning"
        elif typename == "critical":
            icon = QMessageBox.Critical
            title = "Critical"
        # title = unicode(title,"UTF-8")
        # text = unicode(text,"UTF-8")
        msg = QMessageBox(icon, str(title), str(text))
        msg.addButton(button0)
        if button1:
            msg.addButton(button1)
        if button2:
            msg.addButton(button2)
        return msg.exec_()

    @classmethod
    def question(cls, *args):
        return cls.msgbox("question", *args)

    @classmethod
    def information(cls, *args):
        return cls.msgbox("question", *args)

    @classmethod
    def warning(cls, *args):
        return cls.msgbox("warning", *args)

    @classmethod
    def critical(cls, *args):
        return cls.msgbox("critical", *args)


class Input(object):
    @classmethod
    def getText(cls, question, prevtxt, title):
        text, ok = QtWidgets.QInputDialog.getText(None, title,
                                                  question, QtWidgets.QLineEdit.Normal, prevtxt)
        if not ok:
            return None
        return text


def qsa_length(obj):
    lfn = getattr(obj, "length", None)
    if lfn:
        return lfn()
    return len(lfn)


def qsa_text(obj):
    try:
        return obj.text()
    except Exception:
        return obj.text


def FLSqlQuery(*args):
    # if not args: return None
    query_ = FLSqlQuery_Legacy.FLSqlQuery(*args)

    return query_


def FLUtil(*args):
    return FLUtil_Legacy.FLUtil(*args)


def FLSqlCursor(action=None, cN=None):
    if action is None:
        return None
    return FLSqlCursor_Legacy.FLSqlCursor(action, True, cN)


def FLTableDB(*args):
    if not args:
        return None
    return FLTableDB_Legacy.FLTableDB(*args)


FLListViewItem = QtWidgets.QListView
FLDomDocument = QDomDocument
Color = QtGui.QColor
QColor = QtGui.QColor
QDateEdit = QtWidgets.QDateEdit


def FLPosPrinter(*args, **kwargs):
    return FLPosPrinter_Legacy()


@decorators.BetaImplementation
def FLReportViewer():
    return FLReportViewer_Legacy.FLReportViewer()


"""
class FLDomDocument(object):

    parser = None
    tree = None
    root_ = None
    string_ = None

    def __init__(self):
        self.parser = etree.XMLParser(recover=True, encoding='utf-8')
        self.string_ = None


    def setContent(self, value):
        try:
            self.string_ = value
            if value.startswith('<?'):
                value = re.sub(r'^\<\?.*?\?\>','', value, flags=re.DOTALL)
            self.tree = etree.fromstring(value, self.parser)
            #self.root_ = self.tree.getroot()
            return True
        except:
            return False

    def namedItem(self, name):
        return u"<%s" % name in self.string_

    def toString(self, value = None):
        return self.string_
"""


def FLCodBar(*args):
    from pineboolib.fllegacy.FLCodBar import FLCodBar as FLCodBar_Legacy
    return FLCodBar_Legacy(*args)


def FLNetwork(*args):
    from pineboolib.fllegacy.FLNetwork import FLNetwork as FLNetwork_Legacy
    return FLNetwork_Legacy(*args)


def print_stack(maxsize=1):
    for tb in traceback.format_list(traceback.extract_stack())[1:-2][-maxsize:]:
        print(tb.rstrip())


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


class FormDBWidget(QtWidgets.QWidget):
    closed = QtCore.pyqtSignal()
    cursor_ = None
    parent_ = None
    iface = None

    logger = logging.getLogger("qsatype.FormDBWidget")

    def __init__(self, action, project, parent=None):
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
        self.parent_ = parent
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

    def __del__(self):
        # self.doCleanUp()
        print("FormDBWidget: Borrando form para accion %r" % self._action.name)

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
        print("FormDBWidget: closeEvent para accion %r" % self._action.name)
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
                self.logger.info("Señal desconectada al limpiar: %s %s" % (signal, slot))
            except Exception:
                self.logger.exception("Error al limpiar una señal: %s %s" % (signal, slot))
        self._formconnections.clear()

        if hasattr(self, 'iface'):
            check_gc_referrers("FormDBWidget.iface:" + self.iface.__class__.__name__,
                               weakref.ref(self.iface), self._action.name)
            del self.iface.ctx
            del self.iface

    def child(self, childName):
        try:
            parent = self
            ret = None
            while parent and not ret:
                ret = parent.findChild(QtWidgets.QWidget, childName)
                if not ret:
                    parent = parent.parentWidget()

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
                qWarning("WARN: No se encontro el control %s" % childName)

        # Para inicializar los controles si se llaman desde qsa antes de
        # mostrar el formulario.
        if isinstance(ret, FLFieldDB_Legacy.FLFieldDB):
            if not ret.cursor():
                ret.initCursor()
            if not ret.editor_ and not ret.editorImg_:
                ret.initEditor()

        if isinstance(ret, FLTableDB_Legacy.FLTableDB):
            if not ret.tableRecords_:
                ret.tableRecords()
                ret.setTableRecordsCursor()

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
                self.cursor_ = FLSqlCursor(self._action.table)

        return self.cursor_

    """
    FIX: Cuando usamos this como cursor o execMainscript... todo esto tiene que buscarse en cursor o action ... (dentro de un __getattr__)
    """
    """
    def valueBuffer(self, name):
        return self.cursor().valueBuffer(name)

    def isNull(self, name):
        return self.cursor().isNull(name)

    def table(self):
        return self.cursor().table()

    def cursorRelation(self):
        return self.cursor().cursorRelation()

    def execMainScript(self, name):
        self._action.execMainScript(name)
    
    """

    def __getattr__(self, name):
        ret_ = getattr([self._action, self.cursor_], name, None)
        if ret_ is not None:
            print(name, type(ret_))
            print("Retornando", tpye(ret_))
            return ret_


def RegExp(strRE):
    if strRE[-2:] == "/g":
        strRE = strRE[:-2]

    if strRE[:1] == "/":
        strRE = strRE[1:]

    return qsaRegExp(strRE)


class qsaRegExp(object):

    strRE_ = None
    result_ = None

    def __init__(self, strRE):
        print("Nuevo Objeto RegExp de " + strRE)
        self.strRE_ = strRE

    def search(self, text):
        print("Buscando " + self.strRE_ + " en " + text)
        self.result_ = re.search(self.strRE_, text)

    def cap(self, i):
        if self.result_ is None:
            return None

        try:
            return self.result_.group(i)
        except Exception:
            return None


class Date(object):

    date_ = None
    time_ = None

    def __init__(self, *args):
        super(Date, self).__init__()
        if len(args) == 1:
            date_ = args[0]
            self.date_ = QtCore.QDate(date_)
            self.time_ = QtCore.QTime(0, 0)
        elif not args:
            self.date_ = QtCore.QDate.currentDate()
            self.time_ = QtCore.QTime.currentTime()
        else:
            self.date_ = QtCore.QDate(args[0], args[1], args[2])
            self.time_ = QtCore.QTime(0, 0)

    def toString(self, *args, **kwargs):
        texto = "%s-%s-%sT%s:%s:%s" % (self.date_.toString("dd"), self.date_.toString("MM"), self.date_.toString(
            "yyyy"), self.time_.toString("hh"), self.time_.toString("mm"), self.time_.toString("ss"))
        return texto

    def getYear(self):
        return self.date_.year()

    def getMonth(self):
        return self.date_.month()

    def getDay(self):
        return self.date_.day()

    def getHours(self):
        return self.time_.hour()

    def getMinutes(self):
        return self.time_.minute()

    def getSeconds(self):
        return self.time_.second()

    def getMilliseconds(self):
        return self.time_.msec()


class Process(QtCore.QProcess):

    running = None
    stderr = None
    stdout = None

    def __init__(self, *args):
        super(Process, self).__init__()
        self.readyReadStandardOutput.connect(self.stdoutReady)
        self.readyReadStandardError.connect(self.stderrReady)
        self.stderr = None
        if args:
            self.runing = False
            self.setProgram(args[0])
            argumentos = args[1:]
            self.setArguments(argumentos)

    def start(self):
        self.running = True
        super(Process, self).start()

    def stop(self):
        self.running = False
        super(Process, self).stop()

    def writeToStdin(self, stdin_):
        stdin_as_bytes = stdin_.encode('utf-8')
        self.writeData(stdin_as_bytes)
        # self.closeWriteChannel()

    def stdoutReady(self):
        self.stdout = str(self.readAllStandardOutput())

    def stderrReady(self):
        self.stderr = str(self.readAllStandardError())

    def __setattr__(self, name, value):
        if name == "workingDirectory":
            self.setWorkingDirectory(value)
        else:
            super(Process, self).__setattr__(name, value)

    def execute(comando):

        pro = QtCore.QProcess()
        array = comando.split(" ")
        programa = array[0]
        argumentos = array[1:]
        pro.setProgram(programa)
        pro.setArguments(argumentos)
        pro.start()
        pro.waitForFinished(30000)
        Process.stdout = pro.readAllStandardOutput().data().decode()
        Process.stderr = pro.readAllStandardError().data().decode()


class RadioButton(QtWidgets.QRadioButton):

    def __ini__(self):
        super(RadioButton, self).__init__()
        self.setChecked(False)

    def __setattr__(self, name, value):
        if name == "text":
            self.setText(value)
        elif name == "checked":
            self.setChecked(value)
        else:
            super(RadioButton, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name == "checked":
            return self.isChecked()


class Dialog(QtWidgets.QDialog):
    _layout = None
    buttonBox = None
    okButtonText = None
    cancelButtonText = None
    okButton = None
    cancelButton = None
    _tab = None

    def __init__(self, title=None, f=None, desc=None):
        # FIXME: f no lo uso , es qt.windowsflg
        super(Dialog, self).__init__()
        if title:
            self.setWindowTitle(str(title))

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.okButton = QtWidgets.QPushButton("&Aceptar")
        self.cancelButton = QtWidgets.QPushButton("&Cancelar")
        self.buttonBox.addButton(
            self.okButton, QtWidgets.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(
            self.cancelButton, QtWidgets.QDialogButtonBox.RejectRole)
        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
        self._tab = QTabWidget()
        self._tab.hide()
        self._layout.addWidget(self._tab)
        self.oKButtonText = None
        self.cancelButtonText = None

    def add(self, _object):
        self._layout.addWidget(_object)

    def exec_(self):
        if self.okButtonText:
            self.okButton.setText(str(self.okButtonText))
        if (self.cancelButtonText):
            self.cancelButton.setText(str(self.cancelButtonText))
        self._layout.addWidget(self.buttonBox)

        return super(Dialog, self).exec_()

    def newTab(self, name):
        if self._tab.isHidden():
            self._tab.show()
        self._tab.addTab(QtWidgets.QWidget(), str(name))

    def __getattr__(self, name):
        if name == "caption":
            name = self.setWindowTitle

        return getattr(super(Dialog, self), name)


class GroupBox(QtWidgets.QGroupBox):
    def __init__(self):
        super(GroupBox, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)

    def add(self, _object):
        self._layout.addWidget(_object)

    def __setattr__(self, name, value):
        if name == "title":
            self.setTitle(str(value))
        else:
            super(GroupBox, self).__setattr__(name, value)


class CheckBox(QWidget):
    _label = None
    _cb = None

    def __init__(self):
        super(CheckBox, self).__init__()

        self._label = QtWidgets.QLabel(self)
        self._cb = QtWidgets.QCheckBox(self)
        spacer = QtWidgets.QSpacerItem(
            1, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        _lay = QtWidgets.QHBoxLayout()
        _lay.addWidget(self._cb)
        _lay.addWidget(self._label)
        _lay.addSpacerItem(spacer)
        self.setLayout(_lay)

    def __setattr__(self, name, value):
        if name == "text":
            self._label.setText(str(value))
        elif name == "checked":
            self._cb.setChecked(value)
        else:
            super(CheckBox, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name == "checked":
            return self._cb.isChecked()
        else:
            return super(CheckBox, self).__getattr__(name)


class QComboBox(QWidget):

    _label = None
    _combo = None

    def __init__(self):
        super(QComboBox, self).__init__()

        self._label = QtWidgets.QLabel(self)
        self._combo = QtWidgets.QComboBox(self)
        self._combo.setMinimumHeight(25)
        _lay = QtWidgets.QHBoxLayout()
        _lay.addWidget(self._label)
        _lay.addWidget(self._combo)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(True)
        self._combo.setSizePolicy(sizePolicy)

        self.setLayout(_lay)

    def __setattr__(self, name, value):
        if name == "label":
            self._label.setText(str(value))
        elif name == "itemList":
            self._combo.insertItems(len(value), value)
        elif name == "currentItem":
            self._combo.setCurrentText(str(value))
        else:
            super(QComboBox, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name == "currentItem":
            return self._combo.currentText()
        else:
            return super(QComboBox, self).__getattr__(name)


class LineEdit(QWidget):
    _label = None
    _line = None

    def __init__(self):
        super(LineEdit, self).__init__()

        self._label = QtWidgets.QLabel(self)
        self._line = QtWidgets.QLineEdit(self)
        _lay = QtWidgets.QHBoxLayout()
        _lay.addWidget(self._label)
        _lay.addWidget(self._line)
        self.setLayout(_lay)

    def __setattr__(self, name, value):
        if name == "label":
            self._label.setText(str(value))
        elif name == "text":
            self._line.setText(str(value))
        else:
            super(LineEdit, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name == "text":
            return self._line.text()
        else:
            return super(LineEdit, self).__getattr__(name)


class Dir_Class(object):
    path_ = None
    home = None
    Files = "*.*"

    def __init__(self, path=None):
        self.path_ = path
        self.home = filedir("..")

    def entryList(self, patron, type_=None):
        # p = os.walk(self.path_)
        retorno = []
        try:
            for file in os.listdir(self.path_):
                if fnmatch.fnmatch(file, patron):
                    retorno.append(file)
        except Exception as e:
            print("Dir_Class.entryList:", e)

        return retorno

    def fileExists(self, name):
        return os.path.exists(name)

    def cleanDirPath(name):
        return str(name)

    def setCurrent(self, val=None):
        if val is None:
            val = filedir(".")
        os.chdir(val)

    def mkdir(self, name=None):
        if name is None:
            name = self.path_
        try:
            os.stat(name)
        except:
            os.mkdir(name)


Dir = Dir_Class


class TextEdit(QTextEdit):
    pass


class File(QtCore.QFile):
    fichero = None
    mode = None
    path = None

    ReadOnly = QIODevice.ReadOnly
    WriteOnly = QIODevice.WriteOnly
    ReadWrite = QIODevice.ReadWrite
    encode_ = None

    def __init__(self, rutaFichero, encode=None):
        self.encode_ = "iso-8859-15"
        if isinstance(rutaFichero, tuple):
            rutaFichero = rutaFichero[0]
        self.fichero = str(rutaFichero)
        super(File, self).__init__(rutaFichero)
        self.path = os.path.dirname(self.fichero)

        if encode is not None:
            self.encode_ = encode

    # def open(self, mode):
    #    super(File, self).open(self.fichero, mode)

    def read(self):

        if isinstance(self, str):
            file_ = self
            encode = "iso-8859-15"
        else:
            file_ = self.fichero
            encode = self.encode_

        f = codecs.open(file_, encoding=encode)
        ret = ""
        for l in f:
            ret = ret + l

        f.close()
        return ret
        # if isinstance(self, str):
        #    f = File(self)
        #    f.open(File.ReadOnly)
        #    return f.read()

        #in_ = QTextStream(self)
        # return in_.readAll()

    def write(self, text):
        f = codecs.open(self.fichero, encoding=self.encode_, mode="w+")
        f.write(text)
        f.seek(0)
        f.close()

    def exists(name):
        return os.path.isfile(name)


class QString(str):
    def mid(self, start, length=None):
        if length is None:
            return self[start:]
        else:
            return self[start:start + length]


class QWidget(QWidget):

    def child(self, name):
        return self.findChild(QtWidgets.QWidget, name)


def ustr(*t1):

    return "".join([ustr1(t) for t in t1])


def ustr1(t):
    if isinstance(t, str):
        return t

    if isinstance(t, float):
        try:
            t = int(t)
        except Exception:
            pass

    # if isinstance(t, QtCore.QString): return str(t)
    if isinstance(t, str):
        return str(t, "UTF-8")
    try:
        return str(t)
    except Exception as e:
        logger.exception("ERROR Coercing to string: %s", repr(t))
        return None


def debug(txt):
    logger.message("---> " + ustr(txt))


class aqApp(object):

    def db():
        return pineboolib.project.conn
