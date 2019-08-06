import traceback
import os
import os.path
import sys
from typing import cast

from PyQt5 import QtCore
from PyQt5.QtXml import QDomDocument
from PyQt5.QtCore import QProcess, QFile, QTextStream
from PyQt5.QtCore import Qt, QDir, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QApplication, QGroupBox, QCheckBox
from PyQt5.QtWidgets import QFrame

from pineboolib.core.settings import settings
from pineboolib.core import decorators
from pineboolib.core.utils.utils_base import ustr, filedir, sha1
from pineboolib.core.system import System
from pineboolib.core.utils import logging
from pineboolib.core.error_manager import error_manager

from pineboolib.application import project
from pineboolib.application.types import Array, Date, File, Dir, Object, FileStatic
from pineboolib.application.packager.aqunpacker import AQUnpacker
from pineboolib.application import connections
from pineboolib.application.qsatypes.sysbasetype import SysBaseType
from pineboolib.application.database.pnsqlcursor import PNSqlCursor
from pineboolib.application.database.pnsqlquery import PNSqlQuery
from pineboolib.application.database.utils import sqlSelect
from pineboolib.application.process import Process

# from pineboolib.fllegacy.flapplication import aqApp  # avoid importing at root.
from pineboolib.fllegacy.aqsobjects.aqs import AQS
from pineboolib.fllegacy.aqsobjects.aqsql import AQSql
from pineboolib.fllegacy.aqsobjects.aqsettings import AQSettings
from pineboolib.fllegacy.flvar import FLVar
from pineboolib.fllegacy.flutil import FLUtil

from pineboolib.qt3_widgets.dialog import Dialog
from pineboolib.qt3_widgets.qbytearray import QByteArray
from pineboolib.qt3_widgets.messagebox import MessageBox
from pineboolib.qt3_widgets.qtextedit import QTextEdit
from pineboolib.qt3_widgets.qlabel import QLabel
from pineboolib.qt3_widgets.qdialog import QDialog
from pineboolib.qt3_widgets.qvboxlayout import QVBoxLayout
from pineboolib.qt3_widgets.qhboxlayout import QHBoxLayout
from pineboolib.qt3_widgets.qpushbutton import QPushButton


logger = logging.getLogger("fllegacy.systype")


class SysType(SysBaseType):
    time_user_ = QtCore.QDateTime.currentDateTime()

    @classmethod
    def translate(self, *args) -> str:
        from pineboolib.fllegacy.fltranslations import FLTranslate

        group = args[0] if len(args) == 2 else "scripts"
        text = args[1] if len(args) == 2 else args[0]

        if text == "MetaData":
            group, text = text, group

        text = text.replace(" % ", " %% ")

        return str(FLTranslate(group, text))

    @classmethod
    def installACL(self, idacl) -> None:
        # FIXME: Add ACL later
        # acl_ = project.acl()
        # acl_ = None
        # if acl_:
        #     acl_.installACL(idacl)
        pass

    @classmethod
    def updateAreas(self) -> None:
        from pineboolib.fllegacy.flapplication import aqApp

        aqApp.initToolBox()

    @classmethod
    def reinit(self) -> None:
        from pineboolib.fllegacy.flapplication import aqApp

        aqApp.reinit()

    @classmethod
    def setCaptionMainWidget(self, t) -> None:
        from pineboolib.fllegacy.flapplication import aqApp

        aqApp.setCaptionMainWidget(t)

    @staticmethod
    def execQSA(fileQSA=None, args=None):
        """
            Execute a QS file.
        """
        from pineboolib.application.types import Function

        try:
            with open(fileQSA, "r") as file:
                fn = Function(file.read())
                fn(args)
        except Exception:
            e = traceback.format_exc()
            logger.warning(e)
            return

    @staticmethod
    def dumpDatabase(self):
        aqDumper = AbanQDbDumper()
        aqDumper.init()

    @staticmethod
    def terminateChecksLocks(self, sqlCursor: "PNSqlCursor" = None):
        if sqlCursor is not None:
            sqlCursor.checkRisksLocks(True)

    @classmethod
    def statusDbLocksDialog(self, locks=None):
        diag = Dialog()
        txtEdit = QTextEdit()
        diag.caption = self.translate(u"scripts", u"Bloqueos de la base de datos")
        diag.setWidth(500)
        html = u'<html><table border="1">'
        if locks is not None and len(locks):
            j = 0
            item = u""
            fields = locks[0].split(u"@")
            closeInfo = False
            closeRecord = False
            headInfo = u'<table border="1"><tr>'
            i = 0
            while_pass = True
            while i < len(fields):
                if not while_pass:
                    i += 1
                    while_pass = True
                    continue
                while_pass = False
                headInfo += ustr(u"<td><b>", fields[i], u"</b></td>")
                i += 1
                while_pass = True
                try:
                    i < len(fields)
                except Exception:
                    break

            headInfo += u"</tr>"
            headRecord = ustr(
                u'<table border="1"><tr><td><b>',
                self.translate(u"scripts", u"Registro bloqueado"),
                u"</b></td></tr>",
            )
            i = 1
            while_pass = True
            while i < len(locks):
                if not while_pass:
                    i += 1
                    while_pass = True
                    continue
                while_pass = False
                item = locks[i]
                if item[0:2] == u"##":
                    if closeInfo:
                        html += u"</table>"
                    if not closeRecord:
                        html += headRecord
                    html += ustr(u"<tr><td>", item[(len(item) - (len(item) - 2)) :], u"</td></tr>")
                    closeRecord = True
                    closeInfo = False

                else:
                    if closeRecord:
                        html += u"</table>"
                    if not closeInfo:
                        html += headInfo
                    html += u"<tr>"
                    fields = item.split(u"@")
                    j = 0
                    while_pass = True
                    while j < len(fields):
                        if not while_pass:
                            j += 1
                            while_pass = True
                            continue
                        while_pass = False
                        html += ustr(u"<td>", fields[j], u"</td>")
                        j += 1
                        while_pass = True
                        try:
                            j < len(fields)
                        except Exception:
                            break

                    html += u"</tr>"
                    closeRecord = False
                    closeInfo = True

                i += 1
                while_pass = True
                try:
                    i < len(locks)
                except Exception:
                    break

        html += u"</table></table></html>"
        txtEdit.text = html
        diag.add(txtEdit)
        diag.exec_()

    @classmethod
    def mvProjectXml(self):
        docRet = QDomDocument()
        strXml = sqlSelect(u"flupdates", u"modulesdef", u"actual='true'")
        if not strXml:
            return docRet
        doc = QDomDocument()
        if not doc.setContent(strXml):
            return docRet
        strXml = u""
        nodes = doc.childNodes()
        i = 0
        while_pass = True
        while i < len(nodes):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            it = nodes.item(i)
            if it.isComment():
                data = it.toComment().data()
                if not data == "" and data.startswith(u"<mvproject "):
                    strXml = data
                    break

            i += 1
            while_pass = True
            try:
                i < len(nodes)
            except Exception:
                break

        if strXml == "":
            return docRet
        docRet.setContent(strXml)
        return docRet

    @classmethod
    def mvProjectModules(self):
        ret = Array()
        doc = self.mvProjectXml()
        mods = doc.elementsByTagName(u"module")
        i = 0
        while_pass = True
        while i < len(mods):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            it = mods.item(i).toElement()
            mod = {"name": (it.attribute(u"name")), "version": (it.attribute(u"version"))}
            if len(mod["name"]) == 0:
                continue
            ret[mod["name"]] = mod
            i += 1
            while_pass = True
            try:
                i < len(mods)
            except Exception:
                break

        return ret

    @classmethod
    def mvProjectExtensions(self):
        ret = Array()
        doc = self.mvProjectXml()
        exts = doc.elementsByTagName(u"extension")
        i = 0
        while_pass = True
        while i < len(exts):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            it = exts.item(i).toElement()
            ext = {"name": (it.attribute(u"name")), "version": (it.attribute(u"version"))}
            if len(ext["name"]) == 0:
                continue
            ret[ext["name"]] = ext
            i += 1
            while_pass = True
            try:
                i < len(exts)
            except Exception:
                break

        return ret

    @classmethod
    def calculateShaGlobal(self):
        v = u""
        qry = PNSqlQuery()
        qry.setSelect(u"sha")
        qry.setFrom(u"flfiles")
        if qry.exec_() and qry.first():
            v = sha1(str(qry.value(0)))
            while qry.next():
                v = sha1(v + str(qry.value(0)))
        return v

    @classmethod
    def registerUpdate(self, input_=None):
        if not input_:
            return
        unpacker = AQUnpacker(input_)
        errors = unpacker.errorMessages()
        if len(errors) != 0:
            msg = self.translate(u"Hubo los siguientes errores al intentar cargar los módulos:")
            msg += u"\n"
            i = 0
            while_pass = True
            while i < len(errors):
                if not while_pass:
                    i += 1
                    while_pass = True
                    continue
                while_pass = False
                msg += ustr(errors[i], u"\n")
                i += 1
                while_pass = True
                try:
                    i < len(errors)
                except Exception:
                    break

            self.errorMsgBox(msg)
            return

        unpacker.jump()
        unpacker.jump()
        unpacker.jump()
        now = Date()
        file = File(input_)
        fileName = file.name
        modulesDef = self.toUnicode(unpacker.getText(), u"utf8")
        filesDef = self.toUnicode(unpacker.getText(), u"utf8")
        shaGlobal = self.calculateShaGlobal()
        AQSql.update(u"flupdates", [u"actual"], [False])
        AQSql.insert(
            u"flupdates",
            [u"fecha", u"hora", u"nombre", u"modulesdef", u"filesdef", u"shaglobal"],
            [now, str(now)[(len(str(now)) - (8)) :], fileName, modulesDef, filesDef, shaGlobal],
        )

    @classmethod
    def warnLocalChanges(self, changes=None):
        if changes is None:
            changes = self.localChanges()
        if changes["size"] == 0:
            return True
        diag = QDialog()
        diag.caption = self.translate(u"Detectados cambios locales")
        diag.modal = True
        txt = u""
        txt += self.translate(u"¡¡ CUIDADO !! DETECTADOS CAMBIOS LOCALES\n\n")
        txt += self.translate(u"Se han detectado cambios locales en los módulos desde\n")
        txt += self.translate(u"la última actualización/instalación de un paquete de módulos.\n")
        txt += self.translate(u"Si continua es posible que estos cambios sean sobreescritos por\n")
        txt += self.translate(u"los cambios que incluye el paquete que quiere cargar.\n\n")
        txt += u"\n\n"
        txt += self.translate(u"Registro de cambios")
        lay = QVBoxLayout(diag)
        lay.setMargin(6)
        lay.setSpacing(6)
        lbl = QLabel(diag)
        lbl.setText(txt)
        lbl.setAlignment(cast(Qt.Alignment, Qt.AlignTop | Qt.WordBreak))
        lay.addWidget(lbl)
        ted = QTextEdit(diag)
        ted.setTextFormat(QTextEdit.LogText)
        ted.setAlignment(cast(Qt.Alignment, Qt.AlignHCenter | Qt.AlignVCenter))
        ted.append(self.reportChanges(changes))
        lay.addWidget(ted)
        lbl2 = QLabel(diag)
        lbl2.setText(self.translate("¿Que desea hacer?"))
        lbl2.setAlignment(cast(Qt.Alignment, Qt.AlignTop | Qt.WordBreak))
        lay.addWidget(lbl2)
        lay2 = QHBoxLayout()
        lay2.setMargin(6)
        lay2.setSpacing(6)
        lay.addLayout(lay2)
        pbCancel = QPushButton(diag)
        pbCancel.setText(self.translate(u"Cancelar"))
        pbAccept = QPushButton(diag)
        pbAccept.setText(self.translate(u"continue"))
        lay2.addWidget(pbCancel)
        lay2.addWidget(pbAccept)
        connections.connect(pbAccept, "clicked()", diag, "accept()")
        connections.connect(pbCancel, "clicked()", diag, "reject()")
        return False if (diag.exec_() == 0) else True

    @classmethod
    def xmlFilesDefBd(self):
        doc = QDomDocument(u"files_def")
        root = doc.createElement(u"files")
        doc.appendChild(root)
        qry = PNSqlQuery()
        qry.setSelect(u"idmodulo,nombre,contenido")
        qry.setFrom(u"flfiles")
        if not qry.exec_():
            return doc
        shaSum = u""
        shaSumTxt = u""
        shaSumBin = u""
        while qry.next():
            idMod = str(qry.value(0))
            if idMod == u"sys":
                continue
            fName = str(qry.value(1))
            ba = QByteArray()
            ba.string = self.fromUnicode(str(qry.value(2)), u"iso-8859-15")
            sha = ba.sha1()
            nf = doc.createElement(u"file")
            root.appendChild(nf)
            ne = doc.createElement(u"module")
            nf.appendChild(ne)
            nt = doc.createTextNode(idMod)
            ne.appendChild(nt)
            ne = doc.createElement(u"name")
            nf.appendChild(ne)
            nt = doc.createTextNode(fName)
            ne.appendChild(nt)
            if self.textPacking(fName):
                ne = doc.createElement(u"text")
                nf.appendChild(ne)
                nt = doc.createTextNode(fName)
                ne.appendChild(nt)
                ne = doc.createElement(u"shatext")
                nf.appendChild(ne)
                nt = doc.createTextNode(sha)
                ne.appendChild(nt)
                ba = QByteArray()
                ba.string = shaSum + sha
                shaSum = ba.sha1()
                ba = QByteArray()
                ba.string = shaSumTxt + sha
                shaSumTxt = ba.sha1()

            try:
                if self.binaryPacking(fName):
                    ne = doc.createElement(u"binary")
                    nf.appendChild(ne)
                    nt = doc.createTextNode(ustr(fName, u".qso"))
                    ne.appendChild(nt)
                    sha = AQS.sha1(qry.value(3))
                    ne = doc.createElement(u"shabinary")
                    nf.appendChild(ne)
                    nt = doc.createTextNode(sha)
                    ne.appendChild(nt)
                    ba = QByteArray()
                    ba.string = shaSum + sha
                    shaSum = ba.sha1()
                    ba = QByteArray()
                    ba.string = shaSumBin + sha
                    shaSumBin = ba.sha1()

            except Exception:
                e = traceback.format_exc()
                logger.error(e)

        qry = PNSqlQuery()
        qry.setSelect(u"idmodulo,icono")
        qry.setFrom(u"flmodules")
        if qry.exec_():
            while qry.next():
                idMod = str(qry.value(0))
                if idMod == u"sys":
                    continue
                fName = ustr(idMod, u".xpm")
                ba = QByteArray()
                ba.string = str(qry.value(1))
                sha = ba.sha1()
                nf = doc.createElement(u"file")
                root.appendChild(nf)
                ne = doc.createElement(u"module")
                nf.appendChild(ne)
                nt = doc.createTextNode(idMod)
                ne.appendChild(nt)
                ne = doc.createElement(u"name")
                nf.appendChild(ne)
                nt = doc.createTextNode(fName)
                ne.appendChild(nt)
                if self.textPacking(fName):
                    ne = doc.createElement(u"text")
                    nf.appendChild(ne)
                    nt = doc.createTextNode(fName)
                    ne.appendChild(nt)
                    ne = doc.createElement(u"shatext")
                    nf.appendChild(ne)
                    nt = doc.createTextNode(sha)
                    ne.appendChild(nt)
                    ba = QByteArray()
                    ba.string = shaSum + sha
                    shaSum = ba.sha1()
                    ba = QByteArray()
                    ba.string = shaSumTxt + sha
                    shaSumTxt = ba.sha1()

        ns = doc.createElement(u"shasum")
        ns.appendChild(doc.createTextNode(shaSum))
        root.appendChild(ns)
        ns = doc.createElement(u"shasumtxt")
        ns.appendChild(doc.createTextNode(shaSumTxt))
        root.appendChild(ns)
        ns = doc.createElement(u"shasumbin")
        ns.appendChild(doc.createTextNode(shaSumBin))
        root.appendChild(ns)
        return doc

    @classmethod
    def loadModules(self, input_=None, warnBackup=None):
        if input_ is None:
            dir_ = Dir(ustr(self.installPrefix(), u"/share/eneboo/packages"))
            dir_.setCurrent()
            input_ = QFileDialog.getOpenFileName(
                QApplication.focusWidget(),
                u"Eneboo/AbanQ Packages",
                self.translate(u"scripts", u"Seleccionar Fichero"),
                "*.eneboopkg",
            )
        if warnBackup is None:
            warnBackup = True
        if input_:
            try:
                self.loadAbanQPackage(input_, warnBackup)
            except Exception:
                logger.warn("*******", traceback.format_exc())

    @classmethod
    def loadAbanQPackage(self, input_=None, warnBackup=None):
        if warnBackup and self.interactiveGUI():
            txt = u""
            txt += self.translate(u"Asegúrese de tener una copia de seguridad de todos los datos\n")
            txt += self.translate(u"y de que  no hay ningun otro  usuario conectado a la base de\n")
            txt += self.translate(u"datos mientras se realiza la carga.\n\n")
            txt += u"\n\n"
            txt += self.translate(u"¿Desea continuar?")
            if MessageBox.Yes != MessageBox.warning(txt, MessageBox.No, MessageBox.Yes):
                return

        if input_:
            ok = True
            changes = self.localChanges()
            if changes["size"] != 0:
                if not self.warnLocalChanges(changes):
                    return
            if ok:
                unpacker = AQUnpacker(input_)
                errors = unpacker.errorMessages()
                if len(errors) != 0:
                    msg = self.translate(
                        u"Hubo los siguientes errores al intentar cargar los módulos:"
                    )
                    msg += u"\n"
                    i = 0
                    while_pass = True
                    while i < len(errors):
                        if not while_pass:
                            i += 1
                            while_pass = True
                            continue
                        while_pass = False
                        msg += ustr(errors[i], u"\n")
                        i += 1
                        while_pass = True
                        try:
                            i < len(errors)
                        except Exception:
                            break

                    self.errorMsgBox(msg)
                    ok = False

                unpacker.jump()
                unpacker.jump()
                unpacker.jump()
                if ok:
                    ok = self.loadModulesDef(unpacker)
                if ok:
                    ok = self.loadFilesDef(unpacker)

            if not ok:
                self.errorMsgBox(
                    self.translate(u"No se ha podido realizar la carga de los módulos.")
                )
            else:
                self.registerUpdate(input_)
                self.infoMsgBox(self.translate(u"La carga de módulos se ha realizado con éxito."))
                AQTimer.singleShot(0, self.reinit)
                tmpVar = FLVar()
                tmpVar.set(u"mrproper", u"dirty")

    @classmethod
    def loadFilesDef(self, un=None):
        filesDef = self.toUnicode(un.getText(), u"utf8")
        doc = QDomDocument()
        if not doc.setContent(filesDef):
            self.errorMsgBox(
                self.translate(u"Error XML al intentar cargar la definición de los ficheros.")
            )
            return False
        ok = True
        root = doc.firstChild()
        files = root.childNodes()
        FLUtil.createProgressDialog(self.translate(u"Registrando ficheros"), len(files))
        i = 0
        while_pass = True
        while i < len(files):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            it = files.item(i)
            fil = {
                "id": it.namedItem(u"name").toElement().text(),
                "skip": it.namedItem(u"skip").toElement().text(),
                "module": it.namedItem(u"module").toElement().text(),
                "text": it.namedItem(u"text").toElement().text(),
                "shatext": it.namedItem(u"shatext").toElement().text(),
                "binary": it.namedItem(u"binary").toElement().text(),
                "shabinary": it.namedItem(u"shabinary").toElement().text(),
            }
            FLUtil.setProgress(i)
            FLUtil.setLabelText(ustr(self.translate(u"Registrando fichero"), u" ", fil["id"]))
            if len(fil["id"]) == 0 or fil["skip"] == u"true":
                continue
            if not self.registerFile(fil, un):
                self.errorMsgBox(
                    ustr(self.translate(u"Error registrando el fichero"), u" ", fil["id"])
                )
                ok = False
                break
            i += 1
            while_pass = True
            try:
                i < len(files)
            except Exception:
                break

        FLUtil.destroyProgressDialog()
        return ok

    @classmethod
    def registerFile(self, fil=None, un=None):
        if fil["id"].endswith(u".xpm"):
            cur = PNSqlCursor(u"flmodules")
            if not cur.select(ustr(u"idmodulo='", fil["module"], u"'")):
                return False
            if not cur.first():
                return False
            cur.setModeAccess(AQSql.Edit)
            cur.refreshBuffer()
            cur.setValueBuffer(u"icono", un.getText())
            return cur.commitBuffer()

        cur = PNSqlCursor(u"flfiles")
        if not cur.select(ustr(u"nombre='", fil["id"], u"'")):
            return False
        cur.setModeAccess((AQSql.Edit if cur.first() else AQSql.Insert))
        cur.refreshBuffer()
        cur.setValueBuffer(u"nombre", fil["id"])
        cur.setValueBuffer(u"idmodulo", fil["module"])
        cur.setValueBuffer(u"sha", fil["shatext"])
        if len(fil["text"]) > 0:
            if fil["id"].endswith(u".qs"):
                cur.setValueBuffer(u"contenido", self.toUnicode(un.getText(), u"iso-8859-15"))
            else:
                cur.setValueBuffer(u"contenido", un.getText())

        if len(fil["binary"]) > 0:
            un.getBinary()
        return cur.commitBuffer()

    @classmethod
    def checkProjectName(self, proName=None):
        if not proName or proName is None:
            proName = u""
        dbProName = FLUtil.readDBSettingEntry(u"projectname")
        if not dbProName:
            dbProName = u""
        if proName == dbProName:
            return True
        if not proName == "" and dbProName == "":
            return FLUtil.writeDBSettingEntry(u"projectname", proName)
        txt = u""
        txt += self.translate(u"¡¡ CUIDADO !! POSIBLE INCOHERENCIA EN LOS MÓDULOS\n\n")
        txt += self.translate(u"Está intentando cargar un proyecto o rama de módulos cuyo\n")
        txt += self.translate(u"nombre difiere del instalado actualmente en la base de datos.\n")
        txt += self.translate(u"Es posible que la estructura de los módulos que quiere cargar\n")
        txt += self.translate(
            u"sea completamente distinta a la instalada actualmente, y si continua\n"
        )
        txt += self.translate(
            u"podría dañar el código, datos y la estructura de tablas de Eneboo.\n\n"
        )
        txt += self.translate(u"- Nombre del proyecto instalado: %s\n") % (str(dbProName))
        txt += self.translate(u"- Nombre del proyecto a cargar: %s\n\n") % (str(proName))
        txt += u"\n\n"
        if not self.interactiveGUI():
            logger.warning(txt)
            return False
        txt += self.translate(u"¿Desea continuar?")
        return MessageBox.Yes == MessageBox.warning(
            txt, MessageBox.No, MessageBox.Yes, MessageBox.NoButton, u"AbanQ"
        )

    @classmethod
    def loadModulesDef(self, un=None):
        modulesDef = self.toUnicode(un.getText(), u"utf8")
        doc = QDomDocument()
        if not doc.setContent(modulesDef):
            self.errorMsgBox(
                self.translate(u"Error XML al intentar cargar la definición de los módulos.")
            )
            return False
        root = doc.firstChild()
        if not self.checkProjectName(root.toElement().attribute(u"projectname", u"")):
            return False
        ok = True
        modules = root.childNodes()
        FLUtil.createProgressDialog(self.translate(u"Registrando módulos"), len(modules))
        i = 0
        while_pass = True
        while i < len(modules):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            it = modules.item(i)
            mod = {
                "id": it.namedItem(u"name").toElement().text(),
                "alias": self.trTagText(it.namedItem(u"alias").toElement().text()),
                "area": it.namedItem(u"area").toElement().text(),
                "areaname": self.trTagText(it.namedItem(u"areaname").toElement().text()),
                "version": it.namedItem(u"version").toElement().text(),
            }
            FLUtil.setProgress(i)
            FLUtil.setLabelText(ustr(self.translate(u"Registrando módulo"), u" ", mod["id"]))
            if not self.registerArea(mod) or not self.registerModule(mod):
                self.errorMsgBox(
                    ustr(self.translate(u"Error registrando el módulo"), u" ", mod["id"])
                )
                ok = False
                break
            i += 1
            while_pass = True
            try:
                i < len(modules)
            except Exception:
                break

        FLUtil.destroyProgressDialog()
        return ok

    @classmethod
    def registerArea(self, mod=None):
        cur = PNSqlCursor(u"flareas")
        if not cur.select(ustr(u"idarea='", mod["area"], u"'")):
            return False
        cur.setModeAccess((AQSql.Edit if cur.first() else AQSql.Insert))
        cur.refreshBuffer()
        cur.setValueBuffer(u"idarea", mod["area"])
        cur.setValueBuffer(u"descripcion", mod["areaname"])
        return cur.commitBuffer()

    @classmethod
    def registerModule(self, mod=None):
        cur = PNSqlCursor(u"flmodules")
        if not cur.select(ustr(u"idmodulo='", mod["id"], u"'")):
            return False
        cur.setModeAccess((AQSql.Edit if cur.first() else AQSql.Insert))
        cur.refreshBuffer()
        cur.setValueBuffer(u"idmodulo", mod["id"])
        cur.setValueBuffer(u"idarea", mod["area"])
        cur.setValueBuffer(u"descripcion", mod["alias"])
        cur.setValueBuffer(u"version", mod["version"])
        return cur.commitBuffer()

    @classmethod
    def questionMsgBox(
        self,
        msg=None,
        keyRemember=None,
        txtRemember=None,
        forceShow=None,
        txtCaption=None,
        txtYes=None,
        txtNo=None,
    ):
        settings = AQSettings()
        key = u"QuestionMsgBox/"
        valRemember = False
        if keyRemember:
            valRemember = settings.readBoolEntry(key + keyRemember)
            if valRemember and not forceShow:
                return MessageBox.Yes
        if not self.interactiveGUI():
            return True
        diag = QDialog()
        diag.caption = txtCaption if txtCaption else u"Eneboo"
        diag.modal = True
        lay = QVBoxLayout(diag)
        lay.setMargin(6)
        lay.setSpacing(6)
        lay2 = QHBoxLayout(lay)
        lay2.setMargin(6)
        lay2.setSpacing(6)
        lblPix = QLabel(diag)
        pixmap = AQS.pixmap_fromMimeSource(u"help_index.png")
        if pixmap:
            lblPix.setPixmap(pixmap)
            lblPix.setAlignment(AQS.AlignTop)
        lay2.addWidget(lblPix)
        lbl = QLabel(diag)
        lbl.setText(msg)
        lbl.setAlignment(cast(Qt.Alignment, AQS.AlignTop | AQS.WordBreak))
        lay2.addWidget(lbl)
        lay3 = QHBoxLayout(lay)
        lay3.setMargin(6)
        lay3.setSpacing(6)
        pbYes = QPushButton(diag)
        pbYes.setText(txtYes if txtYes else self.translate(u"Sí"))
        pbNo = QPushButton(diag)
        pbNo.setText(txtNo if txtNo else self.translate(u"No"))
        lay3.addWidget(pbYes)
        lay3.addWidget(pbNo)
        connections.connect(pbYes, u"clicked()", diag, u"accept()")
        connections.connect(pbNo, u"clicked()", diag, u"reject()")
        chkRemember = None
        if keyRemember and txtRemember:
            # from pineboolib.qt3_widgets.qcheckbox import QCheckBox

            chkRemember = QCheckBox(txtRemember, diag)
            chkRemember.setChecked(valRemember)
            lay.addWidget(chkRemember)
        ret = MessageBox.No if (diag.exec_() == 0) else MessageBox.Yes
        if chkRemember is not None:
            settings.writeEntry(key + keyRemember, chkRemember.checked)
        return ret

    @classmethod
    def exportModules(self):
        from pineboolib.qt3_widgets.filedialog import FileDialog

        dirBasePath = FileDialog.getExistingDirectory(Dir.home)
        if not dirBasePath:
            return
        dataBaseName = project.conn.db_name
        dirBasePath = Dir.cleanDirPath(
            ustr(dirBasePath, u"/modulos_exportados_", dataBaseName[dataBaseName.rfind(u"/") + 1 :])
        )
        dir = Dir()
        if not dir.fileExists(dirBasePath):
            try:
                dir.mkdir(dirBasePath)
            except Exception:
                e = traceback.format_exc()
                self.errorMsgBox(ustr(u"", e))
                return

        else:
            self.warnMsgBox(
                dirBasePath + self.translate(u" ya existe,\ndebe borrarlo antes de continuar")
            )
            return

        qry = PNSqlQuery()
        qry.setSelect(u"idmodulo")
        qry.setFrom(u"flmodules")
        if not qry.exec_() or qry.size() == 0:
            return
        p = 0
        FLUtil.createProgressDialog(self.translate(u"Exportando módulos"), qry.size() - 1)
        while qry.next():
            idMod = qry.value(0)
            if idMod == u"sys":
                continue
            FLUtil.setLabelText(idMod)
            p += 1
            FLUtil.setProgress(p)
            try:
                self.exportModule(idMod, dirBasePath)
            except Exception:
                e = traceback.format_exc()
                FLUtil.destroyProgressDialog()
                self.errorMsgBox(ustr(u"", e))
                return

        dbProName = FLUtil.readDBSettingEntry(u"projectname")
        if not dbProName:
            dbProName = u""
        if not dbProName == "":
            doc = QDomDocument()
            tag = doc.createElement(u"mvproject")
            tag.toElement().setAttribute(u"name", dbProName)
            doc.appendChild(tag)
            try:
                FileStatic.write(ustr(dirBasePath, u"/mvproject.xml"), doc.toString(2))
            except Exception:
                e = traceback.format_exc()
                FLUtil.destroyProgressDialog()
                self.errorMsgBox(ustr(u"", e))
                return

        FLUtil.destroyProgressDialog()
        self.infoMsgBox(self.translate(u"Módulos exportados en:\n") + dirBasePath)

    @classmethod
    def xmlModule(self, idMod=None):
        qry = PNSqlQuery()
        qry.setSelect(u"descripcion,idarea,version")
        qry.setFrom(u"flmodules")
        qry.setWhere(ustr(u"idmodulo='", idMod, u"'"))
        if not qry.exec_() or not qry.next():
            return
        doc = QDomDocument(u"MODULE")
        tagMod = doc.createElement(u"MODULE")
        doc.appendChild(tagMod)
        tag = doc.createElement(u"name")
        tag.appendChild(doc.createTextNode(idMod))
        tagMod.appendChild(tag)
        trNoop = u'QT_TRANSLATE_NOOP("Eneboo","%s")'
        tag = doc.createElement(u"alias")
        tag.appendChild(doc.createTextNode(trNoop % qry.value(0)))
        tagMod.appendChild(tag)
        idArea = qry.value(1)
        tag = doc.createElement(u"area")
        tag.appendChild(doc.createTextNode(idArea))
        tagMod.appendChild(tag)
        areaName = sqlSelect(u"flareas", u"descripcion", ustr(u"idarea='", idArea, u"'"))
        tag = doc.createElement(u"areaname")
        tag.appendChild(doc.createTextNode(trNoop % areaName))
        tagMod.appendChild(tag)
        tag = doc.createElement(u"entryclass")
        tag.appendChild(doc.createTextNode(idMod))
        tagMod.appendChild(tag)
        tag = doc.createElement(u"version")
        tag.appendChild(doc.createTextNode(qry.value(2)))
        tagMod.appendChild(tag)
        tag = doc.createElement(u"icon")
        tag.appendChild(doc.createTextNode(ustr(idMod, u".xpm")))
        tagMod.appendChild(tag)
        return doc

    @classmethod
    def fileWriteIso(self, file_name=None, content=None):
        from pineboolib.application.types import File

        # from PyQt5.QtCore import QTextStream

        fileISO = File(file_name, "ISO8859-15")
        fileISO.write(content)
        # if not fileISO.open(File.WriteOnly):
        #    logger.warning(ustr(u"Error abriendo fichero ", fileName, u" para escritura"))
        #    return False
        # tsISO = QTextStream(fileISO)
        # tsISO.setCodec(AQS.TextCodec_codecForName(u"ISO8859-15"))
        # tsISO.opIn(content)
        fileISO.close()

    @classmethod
    def fileWriteUtf8(self, file_name=None, content=None):
        from pineboolib.application.types import File

        # from PyQt5.QtCore import QTextStream

        fileUTF = File(file_name, "UTF-8")
        fileUTF.write(content)
        # if not fileUTF.open(File.WriteOnly):
        #    logger.warning(ustr(u"Error abriendo fichero ", fileName, u" para escritura"))
        #    return False
        # tsUTF = QTextStream(fileUTF.ioDevice)
        # tsUTF.setCodec(AQS.TextCodec_codecForName(u"utf8"))
        # tsUTF.opIn(content)
        fileUTF.close()

    @classmethod
    def exportModule(self, idMod=None, dirBasePath=None):
        dir = Dir()
        dirPath = Dir.cleanDirPath(ustr(dirBasePath, u"/", idMod))
        if not dir.fileExists(dirPath):
            dir.mkdir(dirPath)
        if not dir.fileExists(ustr(dirPath, u"/forms")):
            dir.mkdir(ustr(dirPath, u"/forms"))
        if not dir.fileExists(ustr(dirPath, u"/scripts")):
            dir.mkdir(ustr(dirPath, u"/scripts"))
        if not dir.fileExists(ustr(dirPath, u"/queries")):
            dir.mkdir(ustr(dirPath, u"/queries"))
        if not dir.fileExists(ustr(dirPath, u"/tables")):
            dir.mkdir(ustr(dirPath, u"/tables"))
        if not dir.fileExists(ustr(dirPath, u"/reports")):
            dir.mkdir(ustr(dirPath, u"/reports"))
        if not dir.fileExists(ustr(dirPath, u"/translations")):
            dir.mkdir(ustr(dirPath, u"/translations"))
        xmlMod = self.xmlModule(idMod)
        self.fileWriteIso(ustr(dirPath, u"/", idMod, u".mod"), xmlMod.toString(2))
        xpmMod = sqlSelect(u"flmodules", u"icono", ustr(u"idmodulo='", idMod, u"'"))
        self.fileWriteIso(ustr(dirPath, u"/", idMod, u".xpm"), xpmMod)
        qry = PNSqlQuery()
        qry.setSelect(u"nombre,contenido")
        qry.setFrom(u"flfiles")
        qry.setWhere(ustr(u"idmodulo='", idMod, u"'"))
        if not qry.exec_() or qry.size() == 0:
            return
        while qry.next():
            name = qry.value(0)
            content = qry.value(1)
            type = name[(len(name) - (len(name) - name.rfind(u"."))) :]
            if content == "":
                continue
            s02_when = type
            s02_do_work, s02_work_done = False, False
            if s02_when == u".xml":
                s02_do_work, s02_work_done = True, True
            if s02_do_work:
                self.fileWriteIso(ustr(dirPath, u"/", name), content)
                s02_do_work = False  # BREAK
            if s02_when == u".ui":
                s02_do_work, s02_work_done = True, True
            if s02_do_work:
                self.fileWriteIso(ustr(dirPath, u"/forms/", name), content)
                s02_do_work = False  # BREAK
            if s02_when == u".qs":
                s02_do_work, s02_work_done = True, True
            if s02_do_work:
                self.fileWriteIso(ustr(dirPath, u"/scripts/", name), content)
                s02_do_work = False  # BREAK
            if s02_when == u".qry":
                s02_do_work, s02_work_done = True, True
            if s02_do_work:
                self.fileWriteIso(ustr(dirPath, u"/queries/", name), content)
                s02_do_work = False  # BREAK
            if s02_when == u".mtd":
                s02_do_work, s02_work_done = True, True
            if s02_do_work:
                self.fileWriteIso(ustr(dirPath, u"/tables/", name), content)
                s02_do_work = False  # BREAK
            if s02_when == u".kut":
                s02_do_work, s02_work_done = True, True
            if s02_do_work:
                pass
            if s02_when == u".ar":
                s02_do_work, s02_work_done = True, True
            if s02_do_work:
                pass
            if s02_when == u".jrxml":
                s02_do_work, s02_work_done = True, True
            if s02_do_work:
                pass
            if s02_when == u".svg":
                s02_do_work, s02_work_done = True, True
            if s02_do_work:
                self.fileWriteIso(ustr(dirPath, u"/reports/", name), content)
                s02_do_work = False  # BREAK
            if s02_when == u".ts":
                s02_do_work, s02_work_done = True, True  # noqa
            if s02_do_work:
                self.fileWriteIso(ustr(dirPath, u"/translations/", name), content)
                s02_do_work = False  # BREAK

    @classmethod
    def importModules(self, warnBackup=None):
        if warnBackup is None:
            warnBackup = True
        if warnBackup and self.interactiveGUI():
            txt = u""
            txt += self.translate(u"Asegúrese de tener una copia de seguridad de todos los datos\n")
            txt += self.translate(u"y de que  no hay ningun otro  usuario conectado a la base de\n")
            txt += self.translate(u"datos mientras se realiza la importación.\n\n")
            txt += self.translate(u"Obtenga soporte en")
            txt += u" http://www.infosial.com\n(c) InfoSiAL S.L."
            txt += u"\n\n"
            txt += self.translate(u"¿Desea continuar?")
            if MessageBox.Yes != MessageBox.warning(txt, MessageBox.No, MessageBox.Yes):
                return

        key = ustr(u"scripts/sys/modLastDirModules_", SysBaseType.nameBD())
        dirAnt = settings.value(key)
        from pineboolib.qt3_widgets.filedialog import FileDialog

        dirMods = FileDialog.getExistingDirectory(
            str(dirAnt) if dirAnt else None, self.translate(u"Directorio de Módulos")
        )
        if not dirMods:
            return
        dirMods = Dir.cleanDirPath(dirMods)
        dirMods = Dir.convertSeparators(dirMods)
        QDir.setCurrent(dirMods)  # change current directory
        listFilesMod = self.selectModsDialog(FLUtil.findFiles(dirMods, u"*.mod", False))
        FLUtil.createProgressDialog(self.translate(u"Importando"), len(listFilesMod))
        FLUtil.setProgress(1)
        i = 0
        while_pass = True
        while i < len(listFilesMod):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            FLUtil.setLabelText(listFilesMod[i])
            FLUtil.setProgress(i)
            if not self.importModule(listFilesMod[i]):
                self.errorMsgBox(self.translate(u"Error al cargar el módulo:\n") + listFilesMod[i])
                break
            i += 1
            while_pass = True
            try:
                i < len(listFilesMod)
            except Exception:
                break

        FLUtil.destroyProgressDialog()
        FLUtil.writeSettingEntry(key, dirMods)
        self.infoMsgBox(self.translate(u"Importación de módulos finalizada."))
        AQTimer.singleShot(0, self.reinit)

    @classmethod
    def selectModsDialog(self, listFilesMod=None):
        dialog = Dialog()
        dialog.okButtonText = self.translate(u"Aceptar")
        dialog.cancelButtonText = self.translate(u"Cancelar")
        bgroup = QGroupBox()
        bgroup.setTitle(self.translate(u"Seleccione módulos a importar"))
        dialog.add(bgroup)
        res = Array()
        cB = Array()
        i = 0
        while_pass = True
        while i < len(listFilesMod):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            cB[i] = QCheckBox()
            bgroup.add(cB[i])
            cB[i].text = listFilesMod[i]
            cB[i].checked = True
            i += 1
            while_pass = True
            try:
                i < len(listFilesMod)
            except Exception:
                break

        idx = 0
        if dialog.exec_():
            i = 0
            while_pass = True
            while i < len(listFilesMod):
                if not while_pass:
                    i += 1
                    while_pass = True
                    continue
                while_pass = False
                if cB[i].checked:
                    res[idx] = listFilesMod[i]
                    idx += 1
                i += 1
                while_pass = True
                try:
                    i < len(listFilesMod)
                except Exception:
                    break

        return res

    @classmethod
    def importModule(self, modPath=None):
        try:
            with open(modPath, "r") as fileMod:
                contentMod = fileMod.read()
        except Exception:
            e = traceback.format_exc()
            self.errorMsgBox(ustr(self.translate(u"Error leyendo fichero."), u"\n", e))
            return False
        mod_folder = os.path.dirname(modPath)
        mod = None
        xmlMod = QDomDocument()
        if xmlMod.setContent(contentMod):
            nodeMod = xmlMod.namedItem(u"MODULE")
            if not nodeMod:
                self.errorMsgBox(self.translate(u"Error en la carga del fichero xml .mod"))
                return False
            mod = {
                "id": (nodeMod.namedItem(u"name").toElement().text()),
                "alias": (self.trTagText(nodeMod.namedItem(u"alias").toElement().text())),
                "area": (nodeMod.namedItem(u"area").toElement().text()),
                "areaname": (self.trTagText(nodeMod.namedItem(u"areaname").toElement().text())),
                "version": (nodeMod.namedItem(u"version").toElement().text()),
            }
            if not self.registerArea(mod) or not self.registerModule(mod):
                self.errorMsgBox(
                    ustr(self.translate(u"Error registrando el módulo"), u" ", mod["id"])
                )
                return False
            if not self.importFiles(mod_folder, u"*.xml", mod["id"]):
                return False
            if not self.importFiles(mod_folder, u"*.ui", mod["id"]):
                return False
            if not self.importFiles(mod_folder, u"*.qs", mod["id"]):
                return False
            if not self.importFiles(mod_folder, u"*.qry", mod["id"]):
                return False
            if not self.importFiles(mod_folder, u"*.mtd", mod["id"]):
                return False
            if not self.importFiles(mod_folder, u"*.kut", mod["id"]):
                return False
            if not self.importFiles(mod_folder, u"*.ar", mod["id"]):
                return False
            if not self.importFiles(mod_folder, u"*.jrxml", mod["id"]):
                return False
            if not self.importFiles(mod_folder, u"*.svg", mod["id"]):
                return False
            if not self.importFiles(mod_folder, u"*.ts", mod["id"]):
                return False

        else:
            self.errorMsgBox(self.translate(u"Error en la carga del fichero xml .mod"))
            return False

        return True

    @classmethod
    def importFiles(self, dirPath=None, ext=None, idMod=None):
        ok = True
        listFiles = FLUtil.findFiles(dirPath, ext, False)
        FLUtil.createProgressDialog(self.translate(u"Importando"), len(listFiles))
        FLUtil.setProgress(1)
        i = 0
        while_pass = True
        while i < len(listFiles):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            FLUtil.setLabelText(listFiles[i])
            FLUtil.setProgress(i)
            if not self.importFile(listFiles[i], idMod):
                self.errorMsgBox(self.translate(u"Error al cargar :\n") + listFiles[i])
                ok = False
                break
            i += 1
            while_pass = True
            try:
                i < len(listFiles)
            except Exception:
                break

        FLUtil.destroyProgressDialog()
        return ok

    @classmethod
    def importFile(self, filePath=None, idMod=None):
        file = File(filePath)
        content = u""
        try:
            file.open(File.ReadOnly)
            content = str(file.read())
        except Exception:
            e = traceback.format_exc()
            self.errorMsgBox(ustr(self.translate(u"Error leyendo fichero."), u"\n", e))
            return False

        ok = True
        name = file.name
        if (
            not FLUtil.isFLDefFile(content)
            and not name.endswith(u".qs")
            and not name.endswith(u".ar")
            and not name.endswith(u".svg")
        ) or name.endswith(u"untranslated.ts"):
            return ok
        cur = PNSqlCursor(u"flfiles")
        cur.select(ustr(u"nombre = '", name, u"'"))
        if not cur.first():
            if name.endswith(u".ar"):
                if not self.importReportAr(filePath, idMod, content):
                    return True
            cur.setModeAccess(AQSql.Insert)
            cur.refreshBuffer()
            cur.setValueBuffer(u"nombre", name)
            cur.setValueBuffer(u"idmodulo", idMod)
            ba = QByteArray()
            ba.string = content
            cur.setValueBuffer(u"sha", ba.sha1())
            cur.setValueBuffer(u"contenido", content)
            ok = cur.commitBuffer()

        else:
            cur.setModeAccess(AQSql.Edit)
            cur.refreshBuffer()
            ba = QByteArray()
            ba.string = content
            shaCnt = ba.sha1()
            if cur.valueBuffer(u"sha") != shaCnt:
                contenidoCopia = cur.valueBuffer(u"contenido")
                cur.setModeAccess(AQSql.Insert)
                cur.refreshBuffer()
                d = Date()
                cur.setValueBuffer(u"nombre", name + str(d))
                cur.setValueBuffer(u"idmodulo", idMod)
                cur.setValueBuffer(u"contenido", contenidoCopia)
                cur.commitBuffer()
                cur.select(ustr(u"nombre = '", name, u"'"))
                cur.first()
                cur.setModeAccess(AQSql.Edit)
                cur.refreshBuffer()
                cur.setValueBuffer(u"idmodulo", idMod)
                cur.setValueBuffer(u"sha", shaCnt)
                cur.setValueBuffer(u"contenido", content)
                ok = cur.commitBuffer()
                if name.endswith(u".ar"):
                    if not self.importReportAr(filePath, idMod, content):
                        return True

        return ok

    @classmethod
    def importReportAr(self, filePath=None, idMod=None, content=None):
        from pineboolib.application.safeqsa import SafeQSA

        if not self.isLoadedModule(u"flar2kut"):
            return False
        if settings.value(u"scripts/sys/conversionAr") != u"true":
            return False
        content = self.toUnicode(content, u"UTF-8")
        content = SafeQSA.root_module("flar2kut").iface.pub_ar2kut(content)
        filePath = ustr(filePath[0 : len(filePath) - 3], u".kut")
        if content:
            localEnc = settings.value(u"scripts/sys/conversionArENC")
            if not localEnc:
                localEnc = u"ISO-8859-15"
            content = self.fromUnicode(content, localEnc)
            try:
                File.write(filePath, content)
            except Exception:
                e = traceback.format_exc()
                self.errorMsgBox(ustr(self.translate(u"Error escribiendo fichero."), u"\n", e))
                return False

            return self.importFile(filePath, idMod)

        return False

    @classmethod
    @decorators.WorkingOnThis
    def runTransaction(self, f=None, oParam=None):
        curT = PNSqlCursor(u"flfiles")
        curT.transaction(False)
        valor = None
        errorMsg = None
        gui = self.interactiveGUI()
        # FIXME: setOverrideCursor expects a QCursor, not a flag.
        # if gui:
        #     try:
        #         AQS.Application_setOverrideCursor(Qt.WaitCursor)
        #     except Exception:
        #         e = traceback.format_exc()

        try:
            valor = f(oParam)
            if "errorMsg" in oParam:
                errorMsg = oParam["errorMsg"]

            if valor:
                curT.commit()
            else:
                curT.rollback()
                if gui:
                    try:
                        AQS.Application_restoreOverrideCursor()
                    except Exception:
                        e = traceback.format_exc()

                if errorMsg:
                    self.warnMsgBox(errorMsg)
                else:
                    self.warnMsgBox(self.translate(u"Error al ejecutar la función"))

                return False

        except Exception:
            e = traceback.format_exc(limit=-6, chain=False)
            curT.rollback()
            if gui:
                try:
                    AQS.Application_restoreOverrideCursor()
                except Exception:
                    e = traceback.format_exc()

            if errorMsg:
                self.warnMsgBox(ustr(errorMsg, u": ", str(e)))
            else:
                self.warnMsgBox(error_manager(e))

            return False

        if gui:
            try:
                AQS.Application_restoreOverrideCursor()
            except Exception:
                e = traceback.format_exc()
                logger.error(e)

        return valor

    @classmethod
    def search_git_updates(self, url=None):

        if not os.path.exists(filedir("../.git")):
            return

        settings = AQSettings()
        if not url:
            url = settings.readEntry(
                "ebcomportamiento/git_updates_repo", "https://github.com/Aulla/pineboo.git"
            )

        command = "git status %s" % url

        pro = Process()
        pro.execute(command)
        if pro.stdout is None:
            return
        # print("***", pro.stdout)

        if pro.stdout.find("git pull") > -1:
            if MessageBox.Yes != MessageBox.warning(
                "Hay nuevas actualizaciones disponibles para Pineboo. ¿Desea actualizar?",
                MessageBox.No,
                MessageBox.Yes,
            ):
                return

            pro.execute("git pull %s" % url)

            MessageBox.information(
                "Pineboo se va a reiniciar ahora",
                MessageBox.Ok,
                MessageBox.NoButton,
                MessageBox.NoButton,
                u"Eneboo",
            )
            # os.execl(executable, os.path.abspath(__file__)) #FIXME

    @classmethod
    def qsaExceptions(self):
        from pineboolib.fllegacy.flapplication import aqApp

        return aqApp.db().qsaExceptions()

    @classmethod
    def serverTime(self):
        # FIXME: QSqlSelectCursor is not defined. Was an internal of Qt3.3
        return None
        # db = aqApp.db().db()
        # sql = u"select current_time"
        # ahora = None
        # q = QSqlSelectCursor(sql, db)
        # if q.isActive() and q.next():
        #     ahora = q.value(0)
        # return ahora

    @classmethod
    def localChanges(self):
        ret = {}
        ret[u"size"] = 0
        strXmlUpt = sqlSelect("flupdates", "filesdef", "actual='true'")
        if not strXmlUpt:
            return ret
        docUpt = QDomDocument()
        if not docUpt.setContent(strXmlUpt):
            self.errorMsgBox(
                self.translate(u"Error XML al intentar cargar la definición de los ficheros.")
            )
            return ret
        docBd = self.xmlFilesDefBd()
        ret = self.diffXmlFilesDef(docBd, docUpt)
        return ret

    @classmethod
    def interactiveGUI(self):
        from pineboolib.fllegacy.flapplication import aqApp

        return aqApp.db().interactiveGUI()


class AbanQDbDumper(object):
    SEP_CSV = u"\u00b6"
    db_ = None
    showGui_ = None
    dirBase_ = None
    fileName_ = None
    w_ = None
    lblDirBase_ = None
    pbChangeDir_ = None
    tedLog_ = None
    pbInitDump_ = None
    state_ = Object()
    funLog_ = None
    proc_ = None

    def __init__(self, db=None, dirBase=None, showGui=None, funLog=None):
        from pineboolib.fllegacy.flapplication import aqApp

        self.db_ = aqApp.db() if db is None else db
        self.showGui_ = True if showGui is None else showGui
        self.dirBase_ = Dir.home if dirBase is None else dirBase
        self.funLog_ = self.addLog if funLog is None else funLog
        self.fileName_ = self.genFileName()
        self.encoding = sys.getdefaultencoding()

    def init(self):
        if self.showGui_:
            self.buildGui()
            self.w_.exec_()

    def buildGui(self):
        self.w_ = QDialog()
        self.w_.caption = SysType.translate(u"Copias de seguridad")
        self.w_.modal = True
        self.w_.resize(800, 600)
        # lay = QVBoxLayout(self.w_, 6, 6)
        lay = QVBoxLayout(self.w_)
        frm = QFrame(self.w_)
        frm.setFrameShape(Qt.Box)
        frm.setLineWidth(1)
        frm.setFrameShadow(Qt.Plain)

        # layFrm = QVBoxLayout(frm, 6, 6)
        layFrm = QVBoxLayout(frm)
        lbl = QLabel(frm)
        lbl.setText(
            SysType.translate(u"Driver: %s")
            % (str(self.db_.driverNameToDriverAlias(self.db_.driverName())))
        )
        lbl.setAlignment(Qt.AlignTop)
        layFrm.addWidget(lbl)
        lbl = QLabel(frm)
        lbl.setText(SysType.translate(u"Base de datos: %s") % (str(self.db_.database())))
        lbl.setAlignment(Qt.AlignTop)
        layFrm.addWidget(lbl)
        lbl = QLabel(frm)
        lbl.setText(SysType.translate(u"Host: %s") % (str(self.db_.host())))
        lbl.setAlignment(Qt.AlignTop)
        layFrm.addWidget(lbl)
        lbl = QLabel(frm)
        lbl.setText(SysType.translate(u"Puerto: %s") % (str(self.db_.port())))
        lbl.setAlignment(Qt.AlignTop)
        layFrm.addWidget(lbl)
        lbl = QLabel(frm)
        lbl.setText(SysType.translate(u"Usuario: %s") % (str(self.db_.user())))
        lbl.setAlignment(Qt.AlignTop)
        layFrm.addWidget(lbl)
        layAux = QHBoxLayout()
        layFrm.addLayout(layAux)
        self.lblDirBase_ = QLabel(frm)
        self.lblDirBase_.setText(
            SysType.translate(u"Directorio Destino: %s") % (str(self.dirBase_))
        )
        self.lblDirBase_.setAlignment(Qt.AlignVCenter)
        layAux.addWidget(self.lblDirBase_)
        self.pbChangeDir_ = QPushButton(SysType.translate(u"Cambiar"), frm)
        self.pbChangeDir_.setSizePolicy(Qt.Maximum, Qt.Preferred)
        connections.connect(self.pbChangeDir_, u"clicked()", self, u"changeDirBase()")
        layAux.addWidget(self.pbChangeDir_)
        lay.addWidget(frm)
        self.pbInitDump_ = QPushButton(SysType.translate(u"INICIAR COPIA"), self.w_)
        connections.connect(self.pbInitDump_, u"clicked()", self, u"initDump()")
        lay.addWidget(self.pbInitDump_)
        lbl = QLabel(self.w_)
        lbl.setText("Log:")
        lay.addWidget(lbl)
        self.tedLog_ = QTextEdit(self.w_)
        self.tedLog_.setTextFormat(QTextEdit.LogText)
        self.tedLog_.setAlignment(cast(Qt.Alignment, Qt.AlignHCenter | Qt.AlignVCenter))
        lay.addWidget(self.tedLog_)

    def initDump(self):
        gui = self.showGui_ and self.w_ is not None
        if gui:
            self.w_.enabled = False
        self.dumpDatabase()
        if gui:
            self.w_.enabled = True
        if self.state_.ok:
            if gui:
                SysType.infoMsgBox(self.state_.msg)
            self.w_.close()
        else:
            if gui:
                SysType.errorMsgBox(self.state_.msg)

    def genFileName(self):
        now = Date()
        timeStamp = str(now)
        regExp = ["-", ":"]
        # regExp.global_ = True
        for rE in regExp:
            timeStamp = timeStamp.replace(rE, u"")

        fileName = ustr(self.dirBase_, u"/dump_", self.db_.database(), u"_", timeStamp)
        fileName = Dir.cleanDirPath(fileName)
        fileName = Dir.convertSeparators(fileName)
        return fileName

    def changeDirBase(self, dir_=None):
        dirBasePath = dir_
        if not dirBasePath:
            dirBasePath = QFileDialog.getExistingDirectory(self.dirBase_)
            if not dirBasePath:
                return
        self.dirBase_ = dirBasePath
        if self.showGui_ and self.lblDirBase_ is not None:
            self.lblDirBase_.text = SysType.translate(u"Directorio Destino: %s") % (
                str(self.dirBase_)
            )
        self.fileName_ = self.genFileName()

    def addLog(self, msg=None):
        if self.showGui_ and self.tedLog_ is not None:
            self.tedLog_.append(msg)
        else:
            logger.warning(msg)

    def setState(self, ok=None, msg=None):
        self.state_.ok = ok
        self.state_.msg = msg

    def state(self):
        return self.state_

    def launchProc(self, command):
        self.proc_ = QProcess()
        self.proc_.setProgram(command[0])
        self.proc_.setArguments(command[1:])
        # FIXME: Mejorar lectura linea a linea
        cast(pyqtSignal, self.proc_.readyReadStandardOutput).connect(self.readFromStdout)
        cast(pyqtSignal, self.proc_.readyReadStandardError).connect(self.readFromStderr)
        self.proc_.start()

        while self.proc_.running:
            SysType.processEvents()

        return self.proc_.exitcode() == self.proc_.normalExit

    def readFromStdout(self):
        t = self.proc_.readLine().data().decode(self.encoding)
        if t not in (None, ""):
            self.funLog_(t)

    def readFromStderr(self):
        t = self.proc_.readLine().data().decode(self.encoding)
        if t not in (None, ""):
            self.funLog_(t)

    def dumpDatabase(self):
        driver = self.db_.driverName()
        typeBd = 0
        if driver.find("PSQL") > -1:
            typeBd = 1
        else:
            if driver.find("MYSQL") > -1:
                typeBd = 2

        if typeBd == 0:
            self.setState(
                False,
                SysType.translate(u"Este tipo de base de datos no soporta el volcado a disco."),
            )
            self.funLog_(self.state_.msg)
            self.dumpAllTablesToCsv()
            return False
        file = File(self.fileName_)  # noqa
        try:
            if not os.path.exists(self.fileName_):
                dir_ = Dir(self.fileName_)  # noqa

        except Exception:
            e = traceback.format_exc()
            self.setState(False, ustr(u"", e))
            self.funLog_(self.state_.msg)
            return False

        ok = True
        if typeBd == 1:
            ok = self.dumpPostgreSQL()

        if typeBd == 2:
            ok = self.dumpMySQL()

        if not ok:
            self.dumpAllTablesToCsv()
        if not ok:
            self.setState(
                False, SysType.translate(u"No se ha podido realizar la copia de seguridad.")
            )
            self.funLog_(self.state_.msg)
        else:
            self.setState(
                True,
                SysType.translate(u"Copia de seguridad realizada con éxito en:\n%s")
                % (str(self.fileName_)),
            )
            self.funLog_(self.state_.msg)

        return ok

    def dumpPostgreSQL(self):
        pgDump = u"pg_dump"
        command = None
        fileName = ustr(self.fileName_, u".sql")
        db = self.db_
        if SysType.osName() == u"WIN32":
            pgDump += u".exe"
            System.setenv(u"PGPASSWORD", db.password())
            command = [
                pgDump,
                u"-f",
                fileName,
                u"-h",
                db.host(),
                u"-p",
                db.port(),
                u"-U",
                db.user(),
                db.database(),
            ]
        else:
            System.setenv(u"PGPASSWORD", db.password())
            command = [
                pgDump,
                u"-v",
                u"-f",
                fileName,
                u"-h",
                db.host(),
                u"-p",
                db.port(),
                u"-U",
                db.user(),
                db.database(),
            ]

        if not self.launchProc(command):
            self.setState(
                False,
                SysType.translate(u"No se ha podido volcar la base de datos a disco.\n")
                + SysType.translate(u"Es posible que no tenga instalada la herramienta ")
                + pgDump,
            )
            self.funLog_(self.state_["msg"])
            return False
        self.setState(True, u"")
        return True

    def dumpMySQL(self):
        myDump = u"mysqldump"
        command = None
        fileName = ustr(self.fileName_, u".sql")
        db = self.db_
        if SysType.osName() == u"WIN32":
            myDump += u".exe"
            command = [
                myDump,
                u"-v",
                ustr(u"--result-file=", fileName),
                ustr(u"--host=", db.host()),
                ustr(u"--port=", db.port()),
                ustr(u"--password=", db.password()),
                ustr(u"--user=", db.user()),
                db.database(),
            ]
        else:
            command = [
                myDump,
                u"-v",
                ustr(u"--result-file=", fileName),
                ustr(u"--host=", db.host()),
                ustr(u"--port=", db.port()),
                ustr(u"--password=", db.password()),
                ustr(u"--user=", db.user()),
                db.database(),
            ]

        if not self.launchProc(command):
            self.setState(
                False,
                SysType.translate(u"No se ha podido volcar la base de datos a disco.\n")
                + SysType.translate(u"Es posible que no tenga instalada la herramienta ")
                + myDump,
            )
            self.funLog_(self.state_.msg)
            return False
        self.setState(True, u"")
        return True

    def dumpTableToCsv(self, table=None, dirBase=None):
        fileName = ustr(dirBase, table, u".csv")
        file = QFile(fileName)
        if not file.open(File.WriteOnly):
            return False
        ts = QTextStream(file.ioDevice())
        ts.setCodec(AQS.TextCodec_codecForName(u"utf8"))
        qry = PNSqlQuery()
        qry.setSelect(ustr(table, u".*"))
        qry.setFrom(table)
        if not qry.exec_():
            return False
        rec = u""
        fieldNames = qry.fieldList()
        i = 0
        while_pass = True
        while i < len(fieldNames):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            if i > 0:
                rec += self.SEP_CSV
            rec += fieldNames[i]
            i += 1
            while_pass = True
            try:
                i < len(fieldNames)
            except Exception:
                break

        ts.opIn(ustr(rec, u"\n"))
        FLUtil.createProgressDialog(
            SysType.translate(u"Haciendo copia en CSV de ") + table, qry.size()
        )
        p = 0
        while qry.next():
            rec = u""
            i = 0
            while_pass = True
            while i < len(fieldNames):
                if not while_pass:
                    i += 1
                    while_pass = True
                    continue
                while_pass = False
                if i > 0:
                    rec += self.SEP_CSV
                rec += str(qry.value(i))
                i += 1
                while_pass = True
                try:
                    i < len(fieldNames)
                except Exception:
                    break

            ts.opIn(ustr(rec, u"\n"))
            p += 1
            FLUtil.setProgress(p)

        file.close()
        FLUtil.destroyProgressDialog()
        return True

    def dumpAllTablesToCsv(self):
        fileName = self.fileName_
        db = self.db_
        tables = db.tables(AQSql.TableType.Tables)
        dir_ = Dir(fileName)
        dir_.mkdir()
        dirBase = Dir.convertSeparators(ustr(fileName, u"/"))
        # i = 0
        # while_pass = True
        for table_ in tables:
            self.dumpTableToCsv(table_, dirBase)
        return True


class AQTimer(QtCore.QTimer):
    pass


class AQGlobalFunctions(object):
    functions_ = Array()
    mappers_ = Array()
    count_ = 0

    def set(self, functionName=None, globalFunction=None):
        self.functions_[functionName] = globalFunction

    def get(self, functionName=None):
        return self.functions_[functionName]

    def exec_(self, functionName=None):
        fn = self.functions_[functionName]
        if fn is not None:
            fn()

    def mapConnect(self, obj=None, signal=None, functionName=None):
        c = self.count_ % 100
        sigMap = QtCore.QSignalMapper(obj)
        self.mappers_[c] = sigMap

        def _():
            self.mappers_[c] = None

        connections.connect(sigMap, u"mapped(QString)", self, u"exec()")
        sigMap.setMapping(obj, functionName)
        connections.connect(obj, signal, sigMap, u"map()")
