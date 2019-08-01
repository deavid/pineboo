import platform
import traceback
import os
import re


from typing import Callable, Any

from PyQt5 import QtCore

from PyQt5.QtXml import QDomDocument
from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QFileDialog

from pineboolib.core.settings import config
from pineboolib.core import decorators
from pineboolib.core.utils.utils_base import ustr, filedir
from pineboolib.core.system import System
from pineboolib.core.utils import logging

from pineboolib.application import project
from pineboolib.application.types import Array, Date, File, Dir, Object
from pineboolib.application.packager.aqunpacker import AQUnpacker
from pineboolib.application import connections
from pineboolib.application.qsatypes.sysbasetype import SysBaseType
from pineboolib.application.database.pnsqlcursor import PNSqlCursor

from pineboolib.fllegacy.flapplication import aqApp
from pineboolib.fllegacy.aqsobjects.aqs import AQS
from pineboolib.fllegacy.aqsobjects.aqsql import AQSql as AQSql_class

from pineboolib.fllegacy.aqsobjects.aqsqlquery import AQSqlQuery as AQSqlQuery_class
from pineboolib.fllegacy.aqsobjects.aqsettings import AQSettings


from pineboolib.qt3_widgets.dialog import Dialog
from pineboolib.qt3_widgets.qbytearray import QByteArray
from pineboolib.qt3_widgets.process import Process
from pineboolib.qt3_widgets.messagebox import MessageBox
from pineboolib.qt3_widgets.qtextedit import QTextEdit
from pineboolib.qt3_widgets.qlabel import QLabel
from pineboolib.qt3_widgets.qdialog import QDialog
from pineboolib.qt3_widgets.qvboxlayout import QVBoxLayout
from pineboolib.qt3_widgets.qhboxlayout import QHBoxLayout
from pineboolib.qt3_widgets.qpushbutton import QPushButton
from pineboolib.qt3_widgets.qdateedit import QDateEdit


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
        from pineboolib.qsa import debug, File, Function

        file = File(fileQSA)
        try:
            file.open(File.ReadOnly)
        except Exception:
            e = traceback.format_exc()
            logger.warning(e)
            return

        fn = Function(str(file.read()))
        fn(args)

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
        util = FLUtil()
        diag = Dialog()
        txtEdit = TextEdit()
        diag.caption = util.translate(u"scripts", u"Bloqueos de la base de datos")
        diag.width = 500
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
            headRecord = ustr(u'<table border="1"><tr><td><b>', util.translate(u"scripts", u"Registro bloqueado"), u"</b></td></tr>")
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
        strXml = AQUtil.sqlSelect(u"flupdates", u"modulesdef", u"actual='true'")
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
        qry = AQSqlQuery()
        qry.setSelect(u"sha")
        qry.setFrom(u"flfiles")
        if qry.exec_() and qry.first():
            v = AQUtil.sha1(parseString(qry.value(0)))
            while qry.next():
                v = AQUtil.sha1(v + str(qry.value(0)))
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
        shaGlobal = calculateShaGlobal()
        AQSql.update(u"flupdates", Array([u"actual"]), Array([False]))
        AQSql.insert(
            u"flupdates",
            Array([u"fecha", u"hora", u"nombre", u"modulesdef", u"filesdef", u"shaglobal"]),
            Array([now, parseString(now)[(len(parseString(now)) - (8)) :], fileName, modulesDef, filesDef, shaGlobal]),
        )

    @classmethod
    def warnLocalChanges(self, changes=None):
        if changes is None:
            changes = localChanges()
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
        lay.margin = 6
        lay.spacing = 6
        lbl = QLabel(diag)
        lbl.text = txt
        lbl.alignment = AQS.AlignTop or AQS.WordBreak
        lay.addWidget(lbl)
        ted = QTextEdit(diag)
        ted.textFormat = TextEdit.LogText
        ted.alignment = AQS.AlignHCenter or AQS.AlignVCenter
        ted.append(reportChanges(changes))
        lay.addWidget(ted)
        lbl2 = QLabel(diag)
        lbl2.text = self.translate("¿Que desea hacer?")
        lbl2.alignment = AQS.AlignTop or AQS.WordBreak
        lay.addWidget(lbl2)
        lay2 = QHBoxLayout()
        lay2.margin = 6
        lay2.spacing = 6
        lay.addLayout(lay2)
        pbCancel = QPushButton(diag)
        pbCancel.text = self.translate(u"Cancelar")
        pbAccept = QPushButton(diag)
        pbAccept.text = self.translate(u"continue")
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
        qry = AQSqlQuery()
        qry.setSelect(u"idmodulo,nombre,contenido")
        qry.setFrom(u"flfiles")
        if not qry.exec_():
            return doc
        shaSum = u""
        shaSumTxt = u""
        shaSumBin = u""
        while qry.next():
            idMod = parseString(qry.value(0))
            if idMod == u"sys":
                continue
            fName = parseString(qry.value(1))
            ba = QByteArray()
            ba.string = self.fromUnicode(parseString(qry.value(2)), u"iso-8859-15")
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
            if textPacking(fName):
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
                if binaryPacking(fName):
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

        qry = AQSqlQuery()
        qry.setSelect(u"idmodulo,icono")
        qry.setFrom(u"flmodules")
        if qry.exec_():
            while qry.next():
                idMod = parseString(qry.value(0))
                if idMod == u"sys":
                    continue
                fName = ustr(idMod, u".xpm")
                ba = QByteArray()
                ba.string = parseString(qry.value(1))
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
                if textPacking(fName):
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
            dir_ = Dir(ustr(installPrefix(), u"/share/eneboo/packages"))
            dir_.setCurrent()
            input_ = FileDialog.getOpenFileName(
                u"Eneboo/AbanQ Packages", AQUtil.translate(u"scripts", u"Seleccionar Fichero"), "*.eneboopkg"
            )
        if warnBackup is None:
            warnBackup = True
        if input_:
            try:
                loadAbanQPackage(input_, warnBackup)
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
            changes = localChanges()
            if changes["size"] != 0:
                if not warnLocalChanges(changes):
                    return
            if ok:
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
                    ok = False

                unpacker.jump()
                unpacker.jump()
                unpacker.jump()
                if ok:
                    ok = loadModulesDef(unpacker)
                if ok:
                    ok = loadFilesDef(unpacker)

            if not ok:
                self.errorMsgBox(self.translate(u"No se ha podido realizar la carga de los módulos."))
            else:
                registerUpdate(input_)
                self.infoMsgBox(self.translate(u"La carga de módulos se ha realizado con éxito."))
                AQTimer.singleShot(0, reinit)
                tmpVar = FLVar()
                tmpVar.set(u"mrproper", u"dirty")

    @classmethod
    def loadFilesDef(self, un=None):
        filesDef = self.toUnicode(un.getText(), u"utf8")
        doc = QDomDocument()
        if not doc.setContent(filesDef):
            self.errorMsgBox(self.translate(u"Error XML al intentar cargar la definición de los ficheros."))
            return False
        ok = True
        root = doc.firstChild()
        files = root.childNodes()
        AQUtil.createProgressDialog(self.translate(u"Registrando ficheros"), len(files))
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
            AQUtil.setProgress(i)
            AQUtil.setLabelText(ustr(self.translate(u"Registrando fichero"), u" ", fil["id"]))
            if len(fil["id"]) == 0 or fil["skip"] == u"true":
                continue
            if not registerFile(fil, un):
                self.errorMsgBox(ustr(self.translate(u"Error registrando el fichero"), u" ", fil["id"]))
                ok = False
                break
            i += 1
            while_pass = True
            try:
                i < len(files)
            except Exception:
                break

        AQUtil.destroyProgressDialog()
        return ok

    @classmethod
    def registerFile(self, fil=None, un=None):
        if fil["id"].endswith(u".xpm"):
            cur = AQSqlCursor(u"flmodules")
            if not cur.select(ustr(u"idmodulo='", fil["module"], u"'")):
                return False
            if not cur.first():
                return False
            cur.setModeAccess(AQSql.Edit)
            cur.refreshBuffer()
            cur.setValueBuffer(u"icono", un.getText())
            return cur.commitBuffer()

        cur = AQSqlCursor(u"flfiles")
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
        dbProName = AQUtil.readDBSettingEntry(u"projectname")
        if not dbProName:
            dbProName = u""
        if proName == dbProName:
            return True
        if not proName == "" and dbProName == "":
            return AQUtil.writeDBSettingEntry(u"projectname", proName)
        txt = u""
        txt += self.translate(u"¡¡ CUIDADO !! POSIBLE INCOHERENCIA EN LOS MÓDULOS\n\n")
        txt += self.translate(u"Está intentando cargar un proyecto o rama de módulos cuyo\n")
        txt += self.translate(u"nombre difiere del instalado actualmente en la base de datos.\n")
        txt += self.translate(u"Es posible que la estructura de los módulos que quiere cargar\n")
        txt += self.translate(u"sea completamente distinta a la instalada actualmente, y si continua\n")
        txt += self.translate(u"podría dañar el código, datos y la estructura de tablas de Eneboo.\n\n")
        txt += self.translate(u"- Nombre del proyecto instalado: %s\n") % (str(dbProName))
        txt += self.translate(u"- Nombre del proyecto a cargar: %s\n\n") % (str(proName))
        txt += u"\n\n"
        if not self.interactiveGUI():
            logger.warning(txt)
            return False
        txt += self.translate(u"¿Desea continuar?")
        return MessageBox.Yes == MessageBox.warning(txt, MessageBox.No, MessageBox.Yes, MessageBox.NoButton, u"AbanQ")

    @classmethod
    def loadModulesDef(self, un=None):
        modulesDef = self.toUnicode(un.getText(), u"utf8")
        doc = QDomDocument()
        if not doc.setContent(modulesDef):
            self.errorMsgBox(translate(u"Error XML al intentar cargar la definición de los módulos."))
            return False
        root = doc.firstChild()
        if not checkProjectName(root.toElement().attribute(u"projectname", u"")):
            return False
        ok = True
        modules = root.childNodes()
        AQUtil.createProgressDialog(translate(u"Registrando módulos"), len(modules))
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
            AQUtil.setProgress(i)
            AQUtil.setLabelText(ustr(translate(u"Registrando módulo"), u" ", mod["id"]))
            if not registerArea(mod) or not registerModule(mod):
                self.errorMsgBox(ustr(translate(u"Error registrando el módulo"), u" ", mod["id"]))
                ok = False
                break
            i += 1
            while_pass = True
            try:
                i < len(modules)
            except Exception:
                break

        AQUtil.destroyProgressDialog()
        return ok

    @classmethod
    def registerArea(self, mod=None):
        cur = AQSqlCursor(u"flareas")
        if not cur.select(ustr(u"idarea='", mod["area"], u"'")):
            return False
        cur.setModeAccess((AQSql.Edit if cur.first() else AQSql.Insert))
        cur.refreshBuffer()
        cur.setValueBuffer(u"idarea", mod["area"])
        cur.setValueBuffer(u"descripcion", mod["areaname"])
        return cur.commitBuffer()

    @classmethod
    def registerModule(self, mod=None):
        cur = AQSqlCursor(u"flmodules")
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
    def questionMsgBox(self, msg=None, keyRemember=None, txtRemember=None, forceShow=None, txtCaption=None, txtYes=None, txtNo=None):
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
        lay.margin = 6
        lay.spacing = 6
        lay2 = QHBoxLayout(lay)
        lay2.margin = 6
        lay2.spacing = 6
        lblPix = QLabel(diag)
        lblPix.pixmap = AQS.Pixmap_fromMimeSource(u"help_index.png")
        lblPix.alignment = AQS.AlignTop
        lay2.addWidget(lblPix)
        lbl = QLabel(diag)
        lbl.text = msg
        lbl.alignment = AQS.AlignTop or AQS.WordBreak
        lay2.addWidget(lbl)
        lay3 = QHBoxLayout(lay)
        lay3.margin = 6
        lay3.spacing = 6
        pbYes = QPushButton(diag)
        pbYes.text = txtYes if txtYes else self.translate(u"Sí")
        pbNo = QPushButton(diag)
        pbNo.text = txtNo if txtNo else self.translate(u"No")
        lay3.addWidget(pbYes)
        lay3.addWidget(pbNo)
        connections.connect(pbYes, u"clicked()", diag, u"accept()")
        connections.connect(pbNo, u"clicked()", diag, u"reject()")
        chkRemember = None
        if keyRemember and txtRemember:
            chkRemember = QCheckBox(txtRemember, diag)
            chkRemember.checked = valRemember
            lay.addWidget(chkRemember)
        ret = MessageBox.No if (diag.exec_() == 0) else MessageBox.Yes
        if chkRemember is not None:
            settings.writeEntry(key + keyRemember, chkRemember.checked)
        return ret

    @classmethod
    def decryptFromBase64(self, str_=None):
        ba = QByteArray()
        ba.string = str_
        return parseString(AQS.decryptInternal(AQS.fromBase64(ba)))

    @classmethod
    def exportModules(self):
        dirBasePath = FileDialog.getExistingDirectory(Dir.home)
        if not dirBasePath:
            return
        dataBaseName = aqApp.db().database()
        dirBasePath = Dir.cleanDirPath(ustr(dirBasePath, u"/modulos_exportados_", QString(dataBaseName).mid(dataBaseName.rfind(u"/") + 1)))
        dir = Dir()
        if not dir.fileExists(dirBasePath):
            try:
                dir.mkdir(dirBasePath)
            except Exception:
                e = traceback.format_exc()
                self.errorMsgBox(ustr(u"", e))
                return

        else:
            self.warnMsgBox(dirBasePath + self.translate(u" ya existe,\ndebe borrarlo antes de continuar"))
            return

        qry = AQSqlQuery()
        qry.setSelect(u"idmodulo")
        qry.setFrom(u"flmodules")
        if not qry.exec_() or qry.size() == 0:
            return
        p = 0
        AQUtil.createProgressDialog(translate(u"Exportando módulos"), qry.size() - 1)
        while qry.next():
            idMod = qry.value(0)
            if idMod == u"sys":
                continue
            AQUtil.setLabelText(String(u"%s") % (str(idMod)))
            p += 1
            AQUtil.setProgress(p)
            try:
                exportModule(idMod, dirBasePath)
            except Exception:
                e = traceback.format_exc()
                AQUtil.destroyProgressDialog()
                self.errorMsgBox(ustr(u"", e))
                return

        dbProName = AQUtil.readDBSettingEntry(u"projectname")
        if not dbProName:
            dbProName = u""
        if not dbProName == "":
            doc = QDomDocument()
            tag = doc.createElement(u"mvproject")
            tag.toElement().setAttribute(u"name", dbProName)
            doc.appendChild(tag)
            try:
                File.write(ustr(dirBasePath, u"/mvproject.xml"), doc.toString(2))
            except Exception:
                e = traceback.format_exc()
                AQUtil.destroyProgressDialog()
                self.errorMsgBox(ustr(u"", e))
                return

        AQUtil.destroyProgressDialog()
        self.infoMsgBox(translate(u"Módulos exportados en:\n") + dirBasePath)

    @classmethod
    def xmlModule(self, idMod=None):
        qry = AQSqlQuery()
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
        areaName = AQUtil.sqlSelect(u"flareas", u"descripcion", ustr(u"idarea='", idArea, u"'"))
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
    def fileWriteIso(self, fileName=None, content=None):
        fileISO = QFile(fileName)
        if not fileISO.open(File.WriteOnly):
            logger.warning(ustr(u"Error abriendo fichero ", fileName, u" para escritura"))
            return False
        tsISO = QTextStream(fileISO.ioDevice())
        tsISO.setCodec(AQS.TextCodec_codecForName(u"ISO8859-15"))
        tsISO.opIn(content)
        fileISO.close()

    @classmethod
    def fileWriteUtf8(self, fileName=None, content=None):
        fileUTF = QFile(fileName)
        if not fileUTF.open(File.WriteOnly):
            logger.warning(ustr(u"Error abriendo fichero ", fileName, u" para escritura"))
            return False
        tsUTF = QTextStream(fileUTF.ioDevice())
        tsUTF.setCodec(AQS.TextCodec_codecForName(u"utf8"))
        tsUTF.opIn(content)
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
        xmlMod = xmlModule(idMod)
        self.fileWriteIso(ustr(dirPath, u"/", idMod, u".mod"), xmlMod.toString(2))
        xpmMod = AQUtil.sqlSelect(u"flmodules", u"icono", ustr(u"idmodulo='", idMod, u"'"))
        self.fileWriteIso(ustr(dirPath, u"/", idMod, u".xpm"), xpmMod)
        qry = AQSqlQuery()
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

        key = ustr(u"scripts/sys/modLastDirModules_", nameBD())
        dirAnt = AQUtil.readSettingEntry(key)
        dirMods = FileDialog.getExistingDirectory((dirAnt if dirAnt else False), self.translate(u"Directorio de Módulos"))
        if not dirMods:
            return
        dirMods = Dir.cleanDirPath(dirMods)
        dirMods = Dir.convertSeparators(dirMods)
        Dir.current = dirMods
        listFilesMod = selectModsDialog(AQUtil.findFiles(Array([dirMods]), u"*.mod", False))
        AQUtil.createProgressDialog(translate(u"Importando"), len(listFilesMod))
        AQUtil.setProgress(1)
        i = 0
        while_pass = True
        while i < len(listFilesMod):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            AQUtil.setLabelText(listFilesMod[i])
            AQUtil.setProgress(i)
            if not importModule(listFilesMod[i]):
                self.errorMsgBox(translate(u"Error al cargar el módulo:\n") + listFilesMod[i])
                break
            i += 1
            while_pass = True
            try:
                i < len(listFilesMod)
            except Exception:
                break

        AQUtil.destroyProgressDialog()
        AQUtil.writeSettingEntry(key, dirMods)
        self.infoMsgBox(translate(u"Importación de módulos finalizada."))
        AQTimer.singleShot(0, reinit)

    @classmethod
    def selectModsDialog(self, listFilesMod=None):
        dialog = Dialog()
        dialog.okButtonText = self.translate(u"Aceptar")
        dialog.cancelButtonText = self.translate(u"Cancelar")
        bgroup = GroupBox()
        bgroup.title = self.translate(u"Seleccione módulos a importar")
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
            cB[i] = CheckBox()
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
        fileMod = File(modPath)
        contentMod = u""
        try:
            fileMod.open(File.ReadOnly)
            contentMod = fileMod.read()
        except Exception:
            e = traceback.format_exc()
            self.errorMsgBox(ustr(translate(u"Error leyendo fichero."), u"\n", e))
            return False

        mod = None
        xmlMod = QDomDocument()
        if xmlMod.setContent(contentMod):
            nodeMod = xmlMod.namedItem(u"MODULE")
            if not nodeMod:
                self.errorMsgBox(translate(u"Error en la carga del fichero xml .mod"))
                return False
            mod = {
                "id": (nodeMod.namedItem(u"name").toElement().text()),
                "alias": (self.trTagText(nodeMod.namedItem(u"alias").toElement().text())),
                "area": (nodeMod.namedItem(u"area").toElement().text()),
                "areaname": (self.trTagText(nodeMod.namedItem(u"areaname").toElement().text())),
                "version": (nodeMod.namedItem(u"version").toElement().text()),
            }
            if not registerArea(mod) or not registerModule(mod):
                self.errorMsgBox(ustr(translate(u"Error registrando el módulo"), u" ", mod["id"]))
                return False
            if not self.importFiles(fileMod.path, u"*.xml", mod["id"]):
                return False
            if not self.importFiles(fileMod.path, u"*.ui", mod["id"]):
                return False
            if not self.importFiles(fileMod.path, u"*.qs", mod["id"]):
                return False
            if not self.importFiles(fileMod.path, u"*.qry", mod["id"]):
                return False
            if not self.importFiles(fileMod.path, u"*.mtd", mod["id"]):
                return False
            if not self.importFiles(fileMod.path, u"*.kut", mod["id"]):
                return False
            if not self.importFiles(fileMod.path, u"*.ar", mod["id"]):
                return False
            if not self.importFiles(fileMod.path, u"*.jrxml", mod["id"]):
                return False
            if not self.importFiles(fileMod.path, u"*.svg", mod["id"]):
                return False
            if not self.importFiles(fileMod.path, u"*.ts", mod["id"]):
                return False

        else:
            self.errorMsgBox(translate(u"Error en la carga del fichero xml .mod"))
            return False

        return True

    @classmethod
    def importFiles(self, dirPath=None, ext=None, idMod=None):
        ok = True
        listFiles = AQUtil.findFiles(Array([dirPath]), ext, False)
        AQUtil.createProgressDialog(translate(u"Importando"), len(listFiles))
        AQUtil.setProgress(1)
        i = 0
        while_pass = True
        while i < len(listFiles):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            AQUtil.setLabelText(listFiles[i])
            AQUtil.setProgress(i)
            if not self.importFile(listFiles[i], idMod):
                self.errorMsgBox(translate(u"Error al cargar :\n") + listFiles[i])
                ok = False
                break
            i += 1
            while_pass = True
            try:
                i < len(listFiles)
            except Exception:
                break

        AQUtil.destroyProgressDialog()
        return ok

    @classmethod
    def importFile(self, filePath=None, idMod=None):
        file = File(filePath)
        content = u""
        try:
            file.open(File.ReadOnly)
            content = file.read()
        except Exception:
            e = traceback.format_exc()
            self.errorMsgBox(ustr(translate(u"Error leyendo fichero."), u"\n", e))
            return False

        ok = True
        name = file.name
        if (
            not AQUtil.isFLDefFile(content) and not name.endswith(u".qs") and not name.endswith(u".ar") and not name.endswith(u".svg")
        ) or name.endswith(u"untranslated.ts"):
            return ok
        cur = AQSqlCursor(u"flfiles")
        cur.select(ustr(u"nombre = '", name, u"'"))
        if not cur.first():
            if name.endswith(u".ar"):
                if not importReportAr(filePath, idMod, content):
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
                cur.setValueBuffer(u"nombre", name + parseString(d))
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
                    if not importReportAr(filePath, idMod, content):
                        return True

        return ok

    @classmethod
    def importReportAr(self, filePath=None, idMod=None, content=None):
        if not self.isLoadedModule(u"flar2kut"):
            return False
        if AQUtil.readSettingEntry(u"scripts/sys/conversionAr") != u"true":
            return False
        content = self.toUnicode(content, u"UTF-8")
        content = qsa.flar2kut.iface.pub_ar2kut(content)
        filePath = ustr(filePath[0 : len(filePath) - 3], u".kut")
        if content:
            localEnc = util.readSettingEntry(u"scripts/sys/conversionArENC")
            if not localEnc:
                localEnc = u"ISO-8859-15"
            content = self.fromUnicode(content, localEnc)
            try:
                File.write(filePath, content)
            except Exception:
                e = traceback.format_exc()
                self.errorMsgBox(ustr(translate(u"Error escribiendo fichero."), u"\n", e))
                return False

            return self.importFile(filePath, idMod)

        return False

    @decorators.WorkingOnThis
    @classmethod
    def runTransaction(self, f=None, oParam=None):
        curT = PNSqlCursor(u"flfiles")
        curT.transaction(False)
        valor = None
        errorMsg = None
        gui = self.interactiveGUI()
        if gui:
            try:
                AQS.Application_setOverrideCursor(AQS.WaitCursor)
            except Exception:
                e = traceback.format_exc()

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
                    self.warnMsgBox(translate(u"Error al ejecutar la función"))

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
                self.warnMsgBox(ustr(errorMsg, u": ", parseString(e)))
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
            url = settings.readEntry("ebcomportamiento/git_updates_repo", "https://github.com/Aulla/pineboo.git")

        command = "git status %s" % url

        pro = Process
        pro.execute(command)

        # print("***", pro.stdout)

        if pro.stdout.find("git pull") > -1:
            if MessageBox.Yes != MessageBox.warning(
                "Hay nuevas actualizaciones disponibles para Pineboo. ¿Desea actualizar?", MessageBox.No, MessageBox.Yes
            ):
                return

            pro.execute("git pull %s" % url)

            MessageBox.information("Pineboo se va a reiniciar ahora", MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton, u"Eneboo")
            # os.execl(executable, os.path.abspath(__file__)) #FIXME

    @classmethod
    def qsaExceptions(self):
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
        strXmlUpt = AQUtil.sqlSelect("flupdates", "filesdef", "actual='true'")
        if not strXmlUpt:
            return ret
        docUpt = QDomDocument()
        if not docUpt.setContent(strXmlUpt):
            self.errorMsgBox(translate(u"Error XML al intentar cargar la definición de los ficheros."))
            return ret
        docBd = self.xmlFilesDefBd()
        ret = self.diffXmlFilesDef(docBd, docUpt)
        return ret

    @classmethod
    def interactiveGUI(self):
        return aqApp.db().self.interactiveGUI()


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
        self.db_ = aqApp.db() if db is None else db
        self.showGui_ = True if showGui is None else showGui
        self.dirBase_ = Dir.home if dirBase is None else dirBase
        self.funLog_ = self.addLog if funLog is None else funLog
        self.fileName_ = self.genFileName()
        self.encoding = sys.getfilesystemencoding()

    def init(self):
        if self.showGui_:
            self.buildGui()
            self.w_.exec_()

    def buildGui(self):
        self.w_ = QDialog()
        self.w_.caption = qsa_sys.translate(u"Copias de seguridad")
        self.w_.modal = True
        self.w_.resize(800, 600)
        # lay = QVBoxLayout(self.w_, 6, 6)
        lay = QVBoxLayout(self.w_)
        frm = QFrame(self.w_)
        frm.frameShape = AQS.Box
        frm.lineWidth = 1
        frm.frameShadow = AQS.Plain
        # layFrm = QVBoxLayout(frm, 6, 6)
        layFrm = QVBoxLayout(frm)
        lbl = QLabel(frm)
        lbl.text = qsa_sys.translate(u"Driver: %s") % (str(self.db_.driverNameToDriverAlias(self.db_.driverName())))
        lbl.alignment = AQS.AlignTop
        layFrm.addWidget(lbl)
        lbl = QLabel(frm)
        lbl.text = qsa_sys.translate(u"Base de datos: %s") % (str(self.db_.database()))
        lbl.alignment = AQS.AlignTop
        layFrm.addWidget(lbl)
        lbl = QLabel(frm)
        lbl.text = qsa_sys.translate(u"Host: %s") % (str(self.db_.host()))
        lbl.alignment = AQS.AlignTop
        layFrm.addWidget(lbl)
        lbl = QLabel(frm)
        lbl.text = qsa_sys.translate(u"Puerto: %s") % (str(self.db_.port()))
        lbl.alignment = AQS.AlignTop
        layFrm.addWidget(lbl)
        lbl = QLabel(frm)
        lbl.text = qsa_sys.translate(u"Usuario: %s") % (str(self.db_.user()))
        lbl.alignment = AQS.AlignTop
        layFrm.addWidget(lbl)
        layAux = QHBoxLayout()
        layFrm.addLayout(layAux)
        self.lblDirBase_ = QLabel(frm)
        self.lblDirBase_.text = qsa_sys.translate(u"Directorio Destino: %s") % (str(self.dirBase_))
        self.lblDirBase_.alignment = AQS.AlignVCenter
        layAux.addWidget(self.lblDirBase_)
        self.pbChangeDir_ = QPushButton(qsa_sys.translate(u"Cambiar"), frm)
        self.pbChangeDir_.setSizePolicy(AQS.Maximum, AQS.Preferred)
        connections.connect(self.pbChangeDir_, u"clicked()", self, u"changeDirBase()")
        layAux.addWidget(self.pbChangeDir_)
        lay.addWidget(frm)
        self.pbInitDump_ = QPushButton(qsa_sys.translate(u"INICIAR COPIA"), self.w_)
        connections.connect(self.pbInitDump_, u"clicked()", self, u"initDump()")
        lay.addWidget(self.pbInitDump_)
        lbl = QLabel(self.w_)
        lbl.text = u"Log:"
        lay.addWidget(lbl)
        self.tedLog_ = QTextEdit(self.w_)
        self.tedLog_.textFormat = TextEdit.LogText
        self.tedLog_.alignment = AQS.AlignHCenter or AQS.AlignVCenter
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
                qsa_sys.infoMsgBox(self.state_.msg)
            self.w_.close()
        else:
            if gui:
                qsa_sys.self.errorMsgBox(self.state_.msg)

    def genFileName(self):
        now = Date()
        timeStamp = parseString(now)
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
            dirBasePath = FileDialog.getExistingDirectory(self.dirBase_)
            if not dirBasePath:
                return
        self.dirBase_ = dirBasePath
        if self.showGui_ and self.lblDirBase_ is not None:
            self.lblDirBase_.text = qsa_sys.translate(u"Directorio Destino: %s") % (str(self.dirBase_))
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
        self.proc_.readyReadStandardOutput.connect(self.readFromStdout)
        self.proc_.readyReadStandardError.connect(self.readFromStderr)
        self.proc_.start()

        while self.proc_.running:
            qsa_sys.processEvents()

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
            self.setState(False, qsa_sys.translate(u"Este tipo de base de datos no soporta el volcado a disco."))
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
            self.setState(False, qsa_sys.translate(u"No se ha podido realizar la copia de seguridad."))
            self.funLog_(self.state_.msg)
        else:
            self.setState(True, qsa_sys.translate(u"Copia de seguridad realizada con éxito en:\n%s") % (str(self.fileName_)))
            self.funLog_(self.state_.msg)

        return ok

    def dumpPostgreSQL(self):
        pgDump = u"pg_dump"
        command = None
        fileName = ustr(self.fileName_, u".sql")
        db = self.db_
        if qsa_sys.osName() == u"WIN32":
            pgDump += u".exe"
            System.setenv(u"PGPASSWORD", db.password())
            command = [pgDump, u"-f", fileName, u"-h", db.host(), u"-p", db.port(), u"-U", db.user(), db.database()]
        else:
            System.setenv(u"PGPASSWORD", db.password())
            command = [pgDump, u"-v", u"-f", fileName, u"-h", db.host(), u"-p", db.port(), u"-U", db.user(), db.database()]

        if not self.launchProc(command):
            self.setState(
                False,
                qsa_sys.translate(u"No se ha podido volcar la base de datos a disco.\n")
                + qsa_sys.translate(u"Es posible que no tenga instalada la herramienta ")
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
        if qsa_sys.osName() == u"WIN32":
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
                qsa_sys.translate(u"No se ha podido volcar la base de datos a disco.\n")
                + qsa_sys.translate(u"Es posible que no tenga instalada la herramienta ")
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
        qry = AQSqlQuery()
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
        AQUtil.createProgressDialog(qsa_sys.translate(u"Haciendo copia en CSV de ") + table, qry.size())
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
                rec += parseString(qry.value(i))
                i += 1
                while_pass = True
                try:
                    i < len(fieldNames)
                except Exception:
                    break

            ts.opIn(ustr(rec, u"\n"))
            p += 1
            AQUtil.setProgress(p)

        file.close()
        AQUtil.destroyProgressDialog()
        return True

    def dumpAllTablesToCsv(self):
        fileName = self.fileName_
        db = self.db_
        tables = db.tables(AQSql.Tables)
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

        connections.connect(sigMap, u"mapped(QString)", qsa_sys.AQGlobalFunctions, u"exec()")
        sigMap.setMapping(obj, functionName)
        connections.connect(obj, signal, sigMap, u"map()")
