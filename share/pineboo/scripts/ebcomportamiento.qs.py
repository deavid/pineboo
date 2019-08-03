# -*- coding: utf-8 -*-

from pineboolib.qsa import *
from pineboolib.core.utils.utils_base import filedir
from pineboolib.fllegacy.aqsobjects.aqsettings import AQSettings
from PyQt5 import QtCore  # type: ignore
from pineboolib.qt3_widgets.formdbwidget import FormDBWidget
import os

settings = AQSettings()


class FormInternalObj(FormDBWidget):
    def _class_init(self):
        pass

    def main(self):
        mng = qsa.aqApp.db().managerModules()
        self.w_ = qsa.QWidget(qsa.aqApp.mainWidget(), QtCore.Qt.Dialog)
        self.w_ = mng.createUI(u"ebcomportamiento.ui", None, self.w_)
        w = self.w_
        botonAceptar = w.child(u"pbnAceptar")
        boton_aceptar_kugar = w.child(u"pbn_kut")
        botonCancelar = w.child(u"pbnCancelar")
        botonCambiarColor = w.child(u"pbnCO")
        connect(botonAceptar, u"clicked()", self, u"guardar_clicked")
        connect(boton_aceptar_kugar, u"clicked()", self, u"cambiar_kugar_clicked")
        connect(botonCancelar, u"clicked()", self, u"cerrar_clicked")
        connect(botonCambiarColor, u"clicked()", self, u"seleccionarColor_clicked")
        self.cargarConfiguracion()
        self.initEventFilter()
        w.show()

    def cargarConfiguracion(self):
        w = self.w_
        from pineboolib.application import project

        w.child(u"cbFLTableDC").checked = self.leerValorLocal("FLTableDoubleClick")
        w.child(u"cbFLTableSC").checked = self.leerValorLocal("FLTableShortCut")
        w.child(u"cbFLTableCalc").checked = self.leerValorLocal("FLTableExport2Calc")
        w.child(u"cbDebuggerMode").checked = self.leerValorLocal("isDebuggerMode")
        w.child(u"cbSLConsola").checked = self.leerValorLocal("SLConsola")
        w.child(u"cbSLInterface").checked = self.leerValorLocal("SLInterface")
        w.child(u"leCallFunction").text = self.leerValorLocal("ebCallFunction")
        w.child(u"leMaxPixImages").text = self.leerValorLocal("maxPixImages")
        w.child(u"leNombreVertical").text = self.leerValorGlobal("verticalName")
        w.child(u"cbFLLarge").checked = self.leerValorGlobal("FLLargeMode") == "True"
        w.child(u"cbPosInfo").checked = self.leerValorGlobal("PosInfo") == "True"
        w.child(u"cbMobile").checked = self.leerValorLocal("mobileMode")
        w.child(u"cbDeleteCache").checked = self.leerValorLocal("deleteCache")
        w.child(u"cbParseProject").checked = self.leerValorLocal("parseProject")
        w.child(u"cbActionsMenuRed").checked = self.leerValorLocal("ActionsMenuRed")
        w.child(u"cbSpacerLegacy").checked = self.leerValorLocal("spacerLegacy")
        w.child(u"cbParseModulesOnLoad").checked = self.leerValorLocal("parseModulesOnLoad")
        w.child(u"cb_traducciones").checked = self.leerValorLocal("translations_from_qm")
        w.child("le_kut_temporales").text = self.leerValorLocal("kugar_temp_dir")
        w.child("cb_kut_debug").checked = self.leerValorLocal("kugar_debug_mode")
        w.child("cb_no_borrar_cache").checked = self.leerValorLocal("keep_general_cache")
        w.child("cb_snapshot").checked = self.leerValorLocal("show_snaptshop_button")
        w.child("cb_mdi").checked = self.leerValorLocal("mdi_mode")
        w.child("cb_imagenes").checked = self.leerValorLocal("no_img_cached")
        w.child("cb_dbadmin").checked = self.leerValorLocal("dbadmin_enabled")
        w.child("cb_std_query").checked = self.leerValorLocal("std_query")
        w.child("cb_disable_mtdparser").checked = self.leerValorLocal("orm_parser_disabled")
        w.child("cb_disable_orm_load").checked = self.leerValorLocal("orm_load_disabled")
        autoComp = self.leerValorLocal("autoComp")
        if not autoComp or autoComp == "OnDemandF4":
            autoComp = "Bajo Demanda (F4)"
        elif autoComp == "NeverAuto":
            autoComp = "Nunca"
        else:
            autoComp = "Siempre"
        w.child(u"cbAutoComp").setCurrentText = autoComp

        w.child(u"leCO").hide()
        self.colorActual_ = self.leerValorLocal("colorObligatorio")
        if not self.colorActual_:
            self.colorActual_ = "#FFE9AD"

        w.child(u"leCO").setStyleSheet("background-color:" + self.colorActual_)

        # Actualizaciones.

        if os.path.exists(filedir("../.git")):
            w.child("cb_git_activar").checked = self.leerValorLocal("git_updates_enabled")
            ruta = self.leerValorLocal("git_updates_repo")
            if ruta is False:
                ruta = "https://github.com/Aulla/pineboo.git"
            w.child("le_git_ruta").text = ruta
            connect(w.child("pb_git_test"), u"clicked()", self, "search_git_updates")
        else:
            w.child("tbwLocales").setTabEnabled("tab_updates", False)

        w.child(u"leCO").show()

    def search_git_updates(self):
        url = self.w_.child("le_git_ruta").text
        qsa.sys.search_git_updates(url)

    def leerValorGlobal(self, valor_name=None):
        util = qsa.FLUtil()
        value = util.sqlSelect("flsettings", "valor", "flkey='%s'" % valor_name)

        if value is None:
            value = ""

        return value

    def grabarValorGlobal(self, valor_name=None, value=None):
        util = qsa.FLUtil()
        if not util.sqlSelect("flsettings", "flkey", "flkey='%s'" % valor_name):
            util.sqlInsert("flsettings", "flkey,valor", "%s,%s" % (valor_name, value))
        else:
            util.sqlUpdate("flsettings", u"valor", value, "flkey = '%s'" % valor_name)

    def leerValorLocal(self, valor_name):
        from pineboolib.core.settings import config

        if valor_name in ("isDebuggerMode", "dbadmin_enabled"):
            valor = config.value("application/%s" % valor_name, False)
        else:
            if valor_name in ("ebCallFunction", "maxPixImages", "kugarParser", "colorObligatorio", "kugar_temp_dir", "git_updates_repo"):
                valor = config.value("ebcomportamiento/%s" % valor_name, "")
                if valor_name == "kugar_temp_dir" and valor == "":
                    from pineboolib.application import project

                    valor = project.tmpdir

            else:
                valor = config.value("ebcomportamiento/%s" % valor_name, False)
        return valor

    def grabarValorLocal(self, valor_name=None, value=None):
        from pineboolib.core.settings import config

        if valor_name in ("isDebuggerMode", "dbadmin_enabled"):
            config.set_value("application/%s" % valor_name, value)
        else:
            if valor_name == "maxPixImages" and value is None:
                value = 600
            config.set_value("ebcomportamiento/%s" % valor_name, value)

    def initEventFilter(self):
        w = self.w_
        w.eventFilterFunction = qsa.ustr(w.objectName, u".eventFilter")
        w.allowedEvents = qsa.Array([qsa.AQS.Close])
        w.installEventFilter(w)

    def eventFilter(self, o=None, e=None):
        if e.type == qsa.AQS.Close:
            self.cerrar_clicked()

    def cerrar_clicked(self):
        self.w_.close()

    def guardar_clicked(self):
        w = self.w_
        self.grabarValorGlobal("verticalName", w.child(u"leNombreVertical").text)
        self.grabarValorLocal("FLTableDoubleClick", w.child(u"cbFLTableDC").checked)
        self.grabarValorLocal("FLTableShortCut", w.child(u"cbFLTableSC").checked)
        self.grabarValorLocal("FLTableExport2Calc", w.child(u"cbFLTableCalc").checked)
        self.grabarValorLocal("isDebuggerMode", w.child(u"cbDebuggerMode").checked)
        self.grabarValorLocal("SLConsola", w.child(u"cbSLConsola").checked)
        self.grabarValorLocal("SLInterface", w.child(u"cbSLInterface").checked)
        self.grabarValorLocal("ebCallFunction", w.child(u"leCallFunction").text)
        self.grabarValorLocal("maxPixImages", w.child(u"leMaxPixImages").text)
        self.grabarValorLocal("colorObligatorio", self.colorActual_)
        self.grabarValorLocal("ActionsMenuRed", w.child(u"cbActionsMenuRed").checked)
        self.grabarValorGlobal("FLLargeMode", w.child(u"cbFLLarge").checked)
        self.grabarValorGlobal("PosInfo", w.child(u"cbPosInfo").checked)
        self.grabarValorLocal("deleteCache", w.child(u"cbDeleteCache").checked)
        self.grabarValorLocal("parseProject", w.child(u"cbParseProject").checked)
        self.grabarValorLocal("mobileMode", w.child(u"cbMobile").checked)
        self.grabarValorLocal("spacerLegacy", w.child(u"cbSpacerLegacy").checked)
        self.grabarValorLocal("parseModulesOnLoad", w.child(u"cbParseModulesOnLoad").checked)
        self.grabarValorLocal("translations_from_qm", w.child(u"cb_traducciones").checked)
        self.grabarValorLocal("kugar_temp_dir", w.child("le_kut_temporales").text)
        self.grabarValorLocal("kugar_debug_mode", w.child("cb_kut_debug").checked)
        self.grabarValorLocal("keep_general_cache", w.child("cb_no_borrar_cache").checked)
        self.grabarValorLocal("git_updates_enabled", w.child("cb_git_activar").checked)
        self.grabarValorLocal("git_updates_repo", w.child("le_git_ruta").text)
        self.grabarValorLocal("show_snaptshop_button", w.child("cb_snapshot").checked)
        self.grabarValorLocal("mdi_mode", w.child("cb_mdi").checked)
        self.grabarValorLocal("no_img_cached", w.child("cb_imagenes").checked)
        self.grabarValorLocal("dbadmin_enabled", w.child("cb_dbadmin").checked)
        self.grabarValorLocal("std_query", w.child("cb_std_query").checked)
        self.grabarValorLocal("orm_parser_disabled", w.child("cb_disable_mtdparser").checked)
        self.grabarValorLocal("orm_load_disabled", w.child("cb_disable_orm_load").checked)

        autoComp = w.child(u"cbAutoComp").currentText
        if autoComp == "Nunca":
            autoComp = "NeverAuto"
        elif autoComp == "Bajo Demanda (F4)":
            autoComp = "OnDemandF4"
        else:
            autoComp = "AlwaysAuto"
        self.grabarValorLocal("autoComp", autoComp)
        self.cerrar_clicked()

    def seleccionarColor_clicked(self):
        self.colorActual_ = qsa.AQS.ColorDialog_getColor(self.colorActual_, self.w_).name()
        self.w_.child(u"leCO").setStyleSheet("background-color:" + self.colorActual_)

    def cambiar_kugar_clicked(self):
        old_dir = self.w_.child("le_kut_temporales").text
        old_dir = self.fixPath(old_dir)
        new_dir = qsa.FileDialog.getExistingDirectory(old_dir)
        if new_dir and new_dir is not old_dir:
            self.w_.child("le_kut_temporales").text = new_dir
            project.tmpdir = new_dir

    def fixPath(self, ruta=None):
        rutaFixed = ""
        if qsa.sys.osName() == u"WIN32":
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
