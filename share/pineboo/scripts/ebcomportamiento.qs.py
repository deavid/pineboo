# -*- coding: utf-8 -*-
from pineboolib import qsatype
from pineboolib.qsaglobals import *
import traceback
from PyQt5.QtWidgets import QWidget
sys = SysType()


class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        pass

    def main(self):
        mng = aqApp.db().managerModules()
        self.w_ = QWidget()
        self.w_ = mng.createUI(u"ebcomportamiento.ui", None,  self.w_)
        w = self.w_
        botonAceptar = w.child(u"pbnAceptar")
        botonCancelar = w.child(u"pbnCancelar")
        botonCambiarColor = w.child(u"pbnCO")
        connect(botonAceptar, u"clicked()", self, u"guardar_clicked")
        connect(botonCancelar, u"clicked()", self, u"cerrar_clicked")
        connect(botonCambiarColor, u"clicked()", self, u"seleccionarColor_clicked")
        self.cargarConfiguracion()
        self.initEventFilter()
        w_.show()

    def cargarConfiguracion(self):
        w = self.w_
        w.child(u"leNombreVertical").text = leerValorGlobal(u"verticalName")
        w.child(u"cbFLTableDC").checked = leerValorLocal(u"FLTableDoubleClick")
        w.child(u"cbFLTableSC").checked = leerValorLocal(u"FLTableShortCut")
        w.child(u"cbFLTableCalc").checked = leerValorLocal(u"FLTableExport2Calc")
        w.child(u"cbDebuggerMode").checked = leerValorLocal(u"isDebuggerMode")
        w.child(u"cbSLConsola").checked = leerValorLocal(u"SLConsola")
        w.child(u"cbSLInterface").checked = leerValorLocal(u"SLInterface")
        w.child(u"leCallFunction").text = leerValorLocal(u"ebCallFunction")
        w.child(u"leMaxPixImages").text = leerValorLocal(u"maxPixImages")
        w.child(u"cbFLLarge").checked = leerValorGlobal(u"FLLargeMode")
        w.child(u"cbPosInfo").checked = leerValorGlobal(u"PosInfo")
        w.child(u"leCO").hide()
        if leerValorLocal(u"colorObligatorio") == u"":
            w.child(u"leCO").paletteBackgroundColor = u"#FFE9AD"
        else:
            w.child(u"leCO").paletteBackgroundColor = leerValorLocal(u"colorObligatorio")

        w.child(u"leCO").show()
        w.child(u"cbActionsMenuRed").checked = leerValorLocal(u"ActionsMenuRed")

    def leerValorGlobal(self, valorName=None):
        util = qsatype.FLUtil()
        valor = u""
        if not util.sqlSelect(u"flsettings", u"valor", ustr(u"flkey='", valorName, u"'")):
            valor = u""
        else:
            valor = util.sqlSelect(u"flsettings", u"valor", ustr(u"flkey='", valorName, u"'"))

        return valor

    def grabarValorGlobal(self, valorName=None, value=None):
        util = qsatype.FLUtil()
        if not util.sqlSelect(u"flsettings", u"flkey", ustr(u"flkey='", valorName, u"'")):
            util.sqlInsert(u"flsettings", u"flkey,valor", ustr(valorName, u",", value))
        else:
            util.sqlUpdate(u"flsettings", u"valor", value, ustr(u"flkey = '", valorName, u"'"))

    def leerValorLocal(self, valorName=None):
        util = qsatype.FLUtil()
        valor = ""
        s01_when = valorName
        s01_do_work, s01_work_done = False, False
        if s01_when == u"isDebuggerMode":
            s01_do_work, s01_work_done = True, True
        if s01_do_work:
            settings = qsatype.AQSettings()
            valor = settings.readBoolEntry(ustr(u"application/", valorName))
            s01_do_work = False  # BREAK
        if s01_when == u"SLInterface":
            s01_do_work, s01_work_done = True, True
        if s01_do_work:
            pass
        if s01_when == u"SLConsola":
            s01_do_work, s01_work_done = True, True
        if s01_do_work:
            pass
        if s01_when == u"FLTableDoubleClick":
            s01_do_work, s01_work_done = True, True
        if s01_do_work:
            pass
        if s01_when == u"FLTableShortCut":
            s01_do_work, s01_work_done = True, True
        if s01_do_work:
            pass
        if s01_when == u"FLTableExport2Calc":
            s01_do_work, s01_work_done = True, True
        if s01_do_work:
            pass
        if not s01_work_done:
            s01_do_work, s01_work_done = True, True
        if s01_do_work:
            valor = util.readSettingEntry(ustr(u"ebcomportamiento/", valorName), u"")
            s01_do_work = False  # BREAK
        return valor

    def grabarValorLocal(self, valorName=None, value=None):
        if valorName == u"maxPixImages" and value < 1:
            value = 600
        s02_when = valorName
        s02_do_work, s02_work_done = False, False
        if s02_when == u"isDebuggerMode":
            s02_do_work, s02_work_done = True, True
        if s02_do_work:
            settings = qsatype.AQSettings()
            settings.writeEntry(ustr(u"application/", valorName), value)
            s02_do_work = False  # BREAK
        if not s02_work_done:
            s02_do_work, s02_work_done = True, True
        if s02_do_work:
            settings = qsatype.AQSettings()
            settings.writeEntry(ustr(u"ebcomportamiento/", valorName), value)
            s02_do_work = False  # BREAK

    def initEventFilter(self):
        w = self.w_
        w.eventFilterFunction = ustr(self.name, u".eventFilter")
        w.allowedEvents = qsatype.Array([AQS.Close])
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
        self.grabarValorLocal(u"colorObligatorio", ustr(w.child(u"leCO").paletteBackgroundColor, u""))
        self.grabarValorLocal(u"ActionsMenuRed", w.child(u"cbActionsMenuRed").checked)
        self.grabarValorGlobal(u"FLLargeMode", w.child(u"cbFLLarge").checked)
        self.grabarValorGlobal(u"PosInfo", w.child(u"cbPosInfo").checked)
        self.cerrar_clicked()

    def seleccionarColor_clicked(self):
        w = self.w_
        colorActual = w.child(u"leCO").paletteBackgroundColor
        w.child(u"leCO").hide()
        w.child(u"leCO").paletteBackgroundColor = AQS.ColorDialog_getColor(colorActual)
        w_.hide()
        w_.show()
        if w.child(u"leCO").paletteBackgroundColor == u"#000000":
            w.child(u"leCO").paletteBackgroundColor = colorActual
        w.child(u"leCO").show()

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
