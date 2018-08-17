# -*- coding: utf-8 -*-
from pineboolib.qsa import *
import traceback
from PyQt5.QtGui import QPalette
import pineboolib
sys = SysType()


class FormInternalObj(FormDBWidget):
    def _class_init(self):
        pass

    def main(self):
        mng = aqApp.db().managerModules()
        self.w_ = QWidget()
        self.w_ = mng.createUI(u"ebcomportamiento.ui", None, self.w_)
        w = self.w_
        botonAceptar = w.child(u"pbnAceptar")
        botonCancelar = w.child(u"pbnCancelar")
        botonCambiarColor = w.child(u"pbnCO")
        connect(botonAceptar, u"clicked()", self, u"guardar_clicked")
        connect(botonCancelar, u"clicked()", self, u"cerrar_clicked")
        connect(botonCambiarColor, u"clicked()", self, u"seleccionarColor_clicked")
        self.cargarConfiguracion()
        self.initEventFilter()
        w.show()

    def cargarConfiguracion(self):
        w = self.w_
        w.child(u"leNombreVertical").text = self.leerValorGlobal(u"verticalName")
        w.child(u"cbFLTableDC").checked = self.leerValorLocal(u"FLTableDoubleClick")
        w.child(u"cbFLTableSC").checked = self.leerValorLocal(u"FLTableShortCut")
        w.child(u"cbFLTableCalc").checked = self.leerValorLocal(u"FLTableExport2Calc")
        w.child(u"cbDebuggerMode").checked = self.leerValorLocal(u"isDebuggerMode")
        w.child(u"cbSLConsola").checked = self.leerValorLocal(u"SLConsola")
        w.child(u"cbSLInterface").checked = self.leerValorLocal(u"SLInterface")
        w.child(u"leCallFunction").text = self.leerValorLocal(u"ebCallFunction")
        w.child(u"leMaxPixImages").text = self.leerValorLocal(u"maxPixImages")
        w.child(u"cbFLLarge").checked = (self.leerValorGlobal(u"FLLargeMode") == 'True')
        w.child(u"cbPosInfo").checked = (self.leerValorGlobal(u"PosInfo") == 'True')
        w.child(u"cbMobile").checked = self.leerValorLocal(u"mobileMode")
        w.child(u"cbDeleteCache").checked = self.leerValorLocal("deleteCache")
        w.child(u"cbParseProject").checked = self.leerValorLocal("parseProject")
        w.child(u"cbActionsMenuRed").checked = self.leerValorLocal(u"ActionsMenuRed")
        w.child(u"cbKugarParser").addItems(pineboolib.project.kugarPlugin.listAvalibles())
        w.child(u"cbKugarParser").setCurrentText(pineboolib.project.kugarPlugin.defaultParser())

        autoComp = self.leerValorLocal("autoComp")
        if not autoComp or autoComp == "OnDemandF4":
            autoComp = "Bajo Demanda (F4)"
        elif autoComp == "NeverAuto":
            autoComp = "Nunca"
        else:
            autoComp = "Siempre"
        w.child(u"cbAutoComp").setCurrentText(autoComp)

        w.child(u"leCO").hide()
        self.colorActual_ = self.leerValorLocal(u"colorObligatorio")
        if self.colorActual_ is "":
            self.colorActual_ = "#FFE9AD"

        w.child(u"leCO").setStyleSheet('background-color:' + self.colorActual_)
        w.child(u"leCO").show()

    def leerValorGlobal(self, valorName=None):
        util = FLUtil()
        valor = util.sqlSelect(u"flsettings", u"valor", ustr(u"flkey='", valorName, u"'"))
        if valor is None:
            valor = ""

        return valor

    def grabarValorGlobal(self, valorName=None, value=None):
        util = FLUtil()
        if not util.sqlSelect(u"flsettings", u"flkey", ustr(u"flkey='", valorName, u"'")):
            util.sqlInsert(u"flsettings", u"flkey,valor", ustr(valorName, u",", value))
        else:
            util.sqlUpdate(u"flsettings", u"valor", value, ustr(u"flkey = '", valorName, u"'"))

    def leerValorLocal(self, valorName=None):
        util = FLUtil()
        settings = AQSettings()
        if valorName == u"isDebuggerMode":
            valor = settings.readBoolEntry(ustr(u"application/", valorName))
        else:
            valor = util.readSettingEntry(ustr(u"ebcomportamiento/", valorName), u"")
        return valor

    def grabarValorLocal(self, valorName=None, value=None):
        settings = AQSettings()
        if valorName == "maxPixImages" and value is None:
            value = 600

        if valorName == "isDebuggerMode":
            settings.writeEntry(ustr(u"application/", valorName), value)
        else:
            settings.writeEntry(ustr(u"ebcomportamiento/", valorName), value)

    def initEventFilter(self):
        w = self.w_
        w.eventFilterFunction = ustr(w.objectName, u".eventFilter")
        w.allowedEvents = Array([AQS.Close])
        w.installEventFilter(w)

    def eventFilter(self, o=None, e=None):
        s03_when = e.type
        s03_do_work, s03_work_done = False, False
        if s03_when == AQS.Close:
            s03_do_work, s03_work_done = True, True
        if s03_do_work:
            self.cerrar_clicked()
            s03_do_work = False  # BREAK

    def cerrar_clicked(self):
        self.w_.close()

    def guardar_clicked(self):
        w = self.w_
        self.grabarValorGlobal(u"verticalName", w.child(u"leNombreVertical").text)
        self.grabarValorLocal(u"FLTableDoubleClick", w.child(u"cbFLTableDC").checked)
        self.grabarValorLocal(u"FLTableShortCut", w.child(u"cbFLTableSC").checked)
        self.grabarValorLocal(u"FLTableExport2Calc", w.child(u"cbFLTableCalc").checked)
        self.grabarValorLocal(u"isDebuggerMode", w.child(u"cbDebuggerMode").checked)
        self.grabarValorLocal(u"SLConsola", w.child(u"cbSLConsola").checked)
        self.grabarValorLocal(u"SLInterface", w.child(u"cbSLInterface").checked)
        self.grabarValorLocal(u"ebCallFunction", w.child(u"leCallFunction").text)
        self.grabarValorLocal(u"maxPixImages", w.child(u"leMaxPixImages").text)
        self.grabarValorLocal(u"colorObligatorio", self.colorActual_)
        self.grabarValorLocal(u"ActionsMenuRed", w.child(u"cbActionsMenuRed").checked)
        self.grabarValorGlobal(u"FLLargeMode", w.child(u"cbFLLarge").checked)
        self.grabarValorGlobal(u"PosInfo", w.child(u"cbPosInfo").checked)
        self.grabarValorLocal(u"deleteCache", w.child(u"cbDeleteCache").checked)
        self.grabarValorLocal(u"parseProject", w.child(u"cbParseProject").checked)
        self.grabarValorLocal(u"mobileMode", w.child(u"cbMobile").checked)
        self.grabarValorLocal(u"kugarParser", w.child(u"cbKugarParser").currentText())
        autoComp = w.child(u"cbAutoComp").currentText()
        if autoComp == "Nunca":
            autoComp = "NeverAuto"
        elif autoComp == "Bajo Demanda (F4)":
            autoComp = "OnDemandF4"
        else:
            autoComp = "AlwaysAuto"
        self.grabarValorLocal("autoComp", autoComp)
        self.cerrar_clicked()

    def seleccionarColor_clicked(self):
        self.colorActual_ = AQS.ColorDialog_getColor(self.colorActual_, self.w_).name()
        self.w_.child(u"leCO").setStyleSheet('background-color:' + self.colorActual_)

    def fixPath(self, ruta=None):
        rutaFixed = ""
        if sys.osName() == u"WIN32":
            barra = u"\\"
            while ruta != rutaFixed:
                rutaFixed = ruta
                ruta = ruta.replace(u"/", barra)
            if not rutaFixed.endswith(barra):
                rutaFixed += u"\\"

        else:
            rutaFixed = ruta

        return rutaFixed


form = None
