# -*- coding: utf-8 -*-

from pineboolib.fllegacy.FLFormDB_old import FLFormDB
from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
from pineboolib import decorators
from pineboolib.utils import DefFun
from pineboolib import project
from PyQt4 import QtCore, QtGui, Qt
from pineboolib.utils import filedir

class FLFormSearchDB( FLFormDB ):
    _accepted = None
    _cursor = None

    formReady = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        parent = None
        name = None

        if isinstance(args[0], str):
            name = args[0]
            self._cursor= FLSqlCursor(name)
            action = self._cursor.action()
            self._accepted = False

        elif isinstance(args[0], FLSqlCursor):
            self.cursor_ = args[0]
            action = args[1]
            parent = args[2]

        super(FLFormSearchDB,self).__init__(parent ,action)


    def __delattr__(self, *args, **kwargs):
        if self.cursor_:
            self.cursor_.restoreEditionFlag(self)
            self.cursor_.restoreBrowseFlag(self)

        FLFormDB.__delattr__(self, *args, **kwargs)

    def __getattr__(self, name): return DefFun(self, name)

    def setFilter(self, f):

        if not self.cursor_:
            return
        previousF = self.cursor_.mainFilter()
        newF = None
        if not previousF:
            newF = f
        elif previousF.contains(f):
            return
        else:
            newF = "%s AND %s" % (previousF, f)
        self.cursor_.setMainFilter(newF)


    def setCursor(self, cursor):
        print("Definiendo cursor")
        self._cursor = cursor

    @decorators.Incomplete
    def setMainWidget(self, w = None):
        if not self._cursor or not w:
            print("Creamos la ventana (ignorado)")
            return
        print("Creamos la ventana")

        if self.showed:
            if self.mainWidget_ and not self.mainWidget_ == w:
                self.initMainWidget(w)
        else:
            w.hide()

        if self.layoutButtons:
            del self.layoutButtons

        if self.layout:
            del self.layout


        w.setFont(QtGui.qApp.font())
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(w)
        self.layoutButtons = QtGui.QHBoxLayout()

        #pbSize = Qt.QSize(22,22)

        wt = QtGui.QToolButton.whatsThis()
        wt.setIcon(QtGui.QIcon(filedir("icons","gtk-find.png")))
        self.layoutButtons.addWidget(wt)
        wt.show()

        self.mainWidget_ = w

        self._cursor.setEdition(False)
        self._cursor.setBrowse(False)
        self._cursor.recordChoosed.emit(self.acepted)







    def exec_(self, valor):
        print("  <<<< EXEC BEGIN ")
        print("Ejecutamos la ventana y esperamos respuesta, introducimos desde y hasta en cursor")
        self._cursor.setFilter("1=1")
        self.load()
        self.show()
        # Hay que intentar retener la ejecución aquí, hasta confirmación.
        # ... para eso es interesante QDialog, pero hay que ver si se puede integrar.
        for i in range(100):
            QtCore.QCoreApplication.processEvents() # No funciona, pero se ve la idea.

        print("  >>>> EXEC END")


    def accepted(self):
        return self._accepted
