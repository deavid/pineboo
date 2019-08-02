# -*- coding: utf-8 -*-
from pineboolib.core.utils import logging
from pineboolib.core.utils.utils_base import ustr
from pineboolib.qt3_widgets.formdbwidget import FormDBWidget
from pineboolib.fllegacy.systype import SysType
from pineboolib.fllegacy.flutil import FLUtil
from pineboolib.fllegacy.aqsobjects.aqsettings import AQSettings
from pineboolib.fllegacy.aqsobjects.aqutil import AQUtil
from pineboolib.application.qsadictmodules import QSADictModules

logger = logging.getLogger("sys.qs")


class FormInternalObj(FormDBWidget):
    def _class_init(self):
        self.form = self
        self.iface = self

    def init(self):
        from pineboolib.fllegacy.flapplication import aqApp

        settings = AQSettings()
        flfactppal = QSADictModules.from_project("flfactppal")
        if flfactppal is not None:
            try:
                codEjercicio = flfactppal.iface.pub_ejercicioActual()
            except Exception as e:
                logger.error("Module flfactppal was loaded but not able to execute <flfactppal.iface.pub_ejercicioActual()>")
                logger.error("... this usually means that flfactppal has failed translation to python")
                logger.exception(e)
                codEjercicio = None
            if codEjercicio:
                util = FLUtil()
                nombreEjercicio = util.sqlSelect(u"ejercicios", u"nombre", ustr(u"codejercicio='", codEjercicio, u"'"))
                if AQUtil.sqlSelect(u"flsettings", u"valor", u"flkey='PosInfo'") == "True":
                    texto = ""
                    if nombreEjercicio:
                        texto = ustr(u"[ ", nombreEjercicio, u" ]")
                    texto = ustr(
                        texto,
                        u" [ ",
                        aqApp.db().driverNameToDriverAlias(aqApp.db().driverName()),
                        u" ] * [ ",
                        SysType.nameBD(),
                        u" ] * [ ",
                        SysType.nameUser(),
                        u" ] ",
                    )
                    aqApp.setCaptionMainWidget(texto)

                else:
                    if nombreEjercicio:
                        aqApp.setCaptionMainWidget(nombreEjercicio)

                oldApi = settings.readBoolEntry(u"application/oldApi")
                if not oldApi:
                    valor = util.readSettingEntry(u"ebcomportamiento/ebCallFunction")
                    if valor:
                        funcion = Function(valor)
                        try:
                            funcion()
                        except Exception:
                            debug(traceback.format_exc())

        if settings.readBoolEntry("ebcomportamiento/git_updates_enabled", False):
            SysType.AQTimer.singleShot(2000, SysType.search_git_updates)


def afterCommit_flfiles(curFiles=None):
    if curFiles.modeAccess() != curFiles.Browse:
        qry = FLSqlQuery()
        qry.setTablesList(u"flserial")
        qry.setSelect(u"sha")
        qry.setFrom(u"flfiles")
        qry.setForwardOnly(True)
        if qry.exec_():
            if qry.first():
                util = FLUtil()
                v = util.sha1(qry.value(0))
                while qry.next():
                    if qry.value(0) is not None:
                        v = util.sha1(v + qry.value(0))
                curSerial = FLSqlCursor(u"flserial")
                curSerial.select()
                if not curSerial.first():
                    curSerial.setModeAccess(curSerial.Insert)
                else:
                    curSerial.setModeAccess(curSerial.Edit)

                curSerial.refreshBuffer()
                curSerial.setValueBuffer(u"sha", v)
                curSerial.commitBuffer()

        else:
            curSerial = FLSqlCursor(u"flserial")
            curSerial.select()
            if not curSerial.first():
                curSerial.setModeAccess(curSerial.Insert)
            else:
                curSerial.setModeAccess(curSerial.Edit)

            curSerial.refreshBuffer()
            curSerial.setValueBuffer(u"sha", curFiles.valueBuffer(u"sha"))
            curSerial.commitBuffer()

    return True


form = None
