# -*- coding: utf-8 -*-
import os

from PyQt5 import QtWidgets, Qt, QtCore  # type: ignore

from pineboolib import logging
from pineboolib.core import decorators
from pineboolib import pncontrolsfactory

from pineboolib.core.settings import config
from pineboolib.fllegacy.flutil import FLUtil
from pineboolib.fllegacy.flapplication import aqApp
from typing import Any, List, Optional, cast, TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.application.database.pnconnection import PNConnection

logger = logging.getLogger(__name__)


class AQStaticDirInfo(object):

    active_: bool
    path_: str

    def __init__(self, *args) -> None:

        if len(args) == 1:
            self.active_ = args[0]
            self.path_ = ""
        else:
            self.active_ = args[0]
            self.path_ = args[1]


class AQStaticBdInfo(object):

    enabled_: bool
    dirs_: List[AQStaticDirInfo]
    key_ = None

    def __init__(self, database: "PNConnection") -> None:
        self.db_ = database.DBName()
        self.dirs_ = []
        self.key_ = "StaticLoader/%s/" % self.db_
        self.enabled_ = config.value("%senabled" % self.key_, False)

    def findPath(self, p: str) -> Optional[AQStaticDirInfo]:

        for info in self.dirs_:
            if info.path_ == p:
                return info

        return None

    def readSettings(self) -> None:
        self.enabled_ = config.value("%senabled" % self.key_, False)
        self.dirs_.clear()
        dirs = config.value("%sdirs" % self.key_, [])
        i = 0

        while i < len(dirs):
            active_ = dirs[i]
            i += 1
            path_ = dirs[i]
            i += 1
            self.dirs_.append(AQStaticDirInfo(active_, path_))

    def writeSettings(self) -> None:

        config.set_value("%senabled" % self.key_, self.enabled_)
        dirs = []
        active_dirs = []

        for info in self.dirs_:
            dirs.append(str(info.active_))
            dirs.append(info.path_)
            if info.active_:
                active_dirs.append(info.path_)

        config.set_value("%sdirs" % self.key_, dirs)
        config.set_value("%sactiveDirs" % self.key_, ",".join(active_dirs))


class FLStaticLoaderWarning(QtCore.QObject):

    warns_: List[str]
    paths_: List[Any]

    def __init__(self) -> None:
        super().__init__()
        self.warns_ = []
        self.paths_ = []

    def popupWarnings(self) -> None:
        if not self.warns_:
            return

        msg = '<p><img source="about.png" align="right"><b><u>CARGA ESTATICA ACTIVADA</u></b><br><br><font face="Monospace">'

        for it in self.warns_:
            msg += "%s<br>" % it

        msg += "</font><br></p>"
        self.warns_.clear()

        aqApp.popupWarn(msg)

    @decorators.NotImplementedWarn
    def scriptBaseFileName(self, name: str):

        scripts = aqApp.project().scripts()
        for it in scripts:
            if it.baseFileName() == name:
                return it

        return None

    def updateScripts(self) -> None:
        if not self.paths_:
            return

        suf_mn = "::Main"
        suf_fm = "::Form"
        suf_fr = "::FormRecod"

        for it in self.paths_:
            n = it.section(":", 0, 0)
            if not n.endswith(".qs") or not n.endswith(".qs.py"):
                continue

            src = self.scriptBaseFileName(n + suf_mn)
            if src:
                src.__setFilename(it.section(":", 1, 1) + n)

            src = self.scriptBaseFileName(n + suf_fm)
            if src:
                src.__setFilename(it.section(":", 1, 1) + n)

            src = self.scriptBaseFileName(n + suf_fr)
            if src:
                src.__setFilename(it.section(":", 1, 1) + n)

        self.paths_.clear()


warn_: Optional[FLStaticLoaderWarning] = None


class FLStaticLoader(QtCore.QObject):
    def __init__(self, b, ui) -> None:

        super(FLStaticLoader, self).__init__()

        self.ui_ = ui
        self.b_ = b
        self.pixOn.setVisible(False)
        self.tblDirs.verticalHeader().setVisible(False)
        self.tblDirs.setLeftMargin(0)
        self.tblDirs.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.tblDirs.horizontalHeader().setSectionsClickable(False)
        self.tblDirs.setColumnStrechable(0, True)
        self.tblDirs.adjustColumn(1)
        self.tblDirs.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.load()

        self.pbAddDir.clicked.connect(self.addDir)
        self.pbModDir.clicked.connect(self.modDir)
        self.pbDelDir.clicked.connect(self.delDir)
        self.chkEnabled.toggled.connect(self.setEnabled)

    @decorators.pyqtSlot()
    def load(self) -> None:
        self.b_.readSettings()
        self.lblBdTop.setText(self.b_.db_)
        self.chkEnabled.setChecked(self.b_.enabled_)

        if self.b_.dirs_:
            n_rows = self.tblDirs.numRows()
            if n_rows > 0:
                rows = []
                for row in range(n_rows):
                    rows.append(row)

                self.tblDirs.removeRows(rows)

            n_rows = len(self.b_.dirs_)
            self.tblDirs.setNumRows(n_rows)
            row = 0

            for info in self.b_.dirs_:
                self.tblDirs.setText(row, 0, info.path_)

                chk = pncontrolsfactory.FLCheckBox(self.tblDirs, row)
                chk.setChecked(info.active_ == "True")
                chk.toggled.connect(self.setChecked)
                self.tblDirs.setCellWidget(row, 1, chk)
                row += 1

            self.tblDirs.setCurrentCell(n_rows, 0)

    @QtCore.pyqtSlot(bool)
    def addDir(self) -> None:

        cur_row = self.tblDirs.currentRow()
        dir_init = self.tblDirs.text(cur_row, 0) if cur_row > -1 else ""

        dir = Qt.QFileDialog.getExistingDirectory(None, self.tr("Selecciones el directorio a insertar"), dir_init)

        if dir:

            n_rows = self.tblDirs.numRows()
            self.tblDirs.setNumRows(n_rows + 1)
            self.tblDirs.setText(n_rows, 0, dir)

            chk = pncontrolsfactory.FLCheckBox(self.tblDirs, n_rows)
            chk.setChecked(True)
            chk.toggled.connect(self.setChecked)

            self.tblDirs.setCellWidget(n_rows, 1, chk)
            self.tblDirs.setCurrentCell(n_rows, 0)

            self.b_.dirs_.append(AQStaticDirInfo(True, dir))

    @decorators.pyqtSlot()
    def modDir(self) -> None:

        cur_row = self.tblDirs.currentRow()
        if cur_row == -1:
            return

        dir_init = self.tblDirs.text(cur_row, 0) if cur_row > -1 else ""

        dir = Qt.QFileDialog.getExistingDirectory(None, self.tr("Selecciones el directorio a modificar"), dir_init)

        if dir:
            info = self.b_.findPath(self.tblDirs.text(cur_row, 0))
            if info:
                info.path_ = dir

            self.tblDirs.setText(cur_row, 0, dir)

    @decorators.pyqtSlot()
    def delDir(self) -> None:

        cur_row = self.tblDirs.currentRow()
        if cur_row == -1:
            return

        if QtWidgets.QMessageBox.No == QtWidgets.QMessageBox.warning(
            QtWidgets.QWidget(),
            self.tr("Borrar registro"),
            self.tr("El registro activo será borrado. ¿ Está seguro ?"),
            cast(QtWidgets.QMessageBox, QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.No),
        ):
            return

        info = self.b_.findPath(self.tblDirs.text(cur_row, 0))
        if info:
            self.b_.dirs_.remove(info)

        self.tblDirs.removeRow(cur_row)

    @QtCore.pyqtSlot(bool)
    def setEnabled(self, on: bool) -> None:
        self.b_.enabled_ = on

    @QtCore.pyqtSlot(bool)
    def setChecked(self, on: bool) -> None:

        chk = self.sender()
        if not chk:
            return

        rows = self.tblDirs.rowCount()

        info = None
        for r in range(rows):
            if self.tblDirs.cellWidget(r, 1) is chk:
                info = self.b_.findPath(self.tblDirs.text(r, 0))

        if info:
            info.active_ = on

    @staticmethod
    def setup(b, ui: Any) -> None:
        diag_setup = FLStaticLoader(b, ui)
        if QtWidgets.QDialog.Accepted == diag_setup.ui_.exec_():
            b.writeSettings()

    @staticmethod
    def content(n, b: Any, only_path=False) -> Any:
        global warn_
        b.readSettings()
        util = FLUtil()
        separator = "\\" if util.getOS().find("WIN") > -1 else "/"
        for info in b.dirs_:
            content_path = info.path_ + separator + n
            if info.active_ and os.path.exists(content_path):
                if not warn_:
                    warn_ = FLStaticLoaderWarning()

                timer = QtCore.QTimer
                if not warn_.warns_ and config.value("ebcomportamiento/SLInterface", True):
                    timer.singleShot(500, warn_.popupWarnings)

                if not warn_.paths_:
                    timer.singleShot(1500, warn_.updateScripts)

                msg = "%s -> ...%s" % (n, info.path_[0:40])

                if msg not in warn_.warns_:
                    warn_.warns_.append(msg)
                    warn_.paths_.append("%s:%s" % (n, info.path_))
                    if config.value("ebcomportamiento/SLConsola", False):
                        logger.warning("CARGA ESTATICA ACTIVADA:%s -> %s", n, info.path_)

                if only_path:
                    return content_path
                else:
                    from pineboolib.application import project

                    if project.conn is None:
                        raise Exception("Project is not connected yet")

                    return project.conn.managerModules().contentFS(info.path_ + separator + n)

        return None

    def __getattr__(self, name) -> Any:
        return self.ui_.findChild(QtWidgets.QWidget, name)
