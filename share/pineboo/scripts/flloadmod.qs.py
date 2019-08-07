# -*- coding: utf-8 -*-
from pineboolib.qsa import qsa
import os
import traceback


class FormInternalObj(qsa.FormDBWidget):
    def _class_init(self):
        self.util = qsa.FLUtil()

    def main(self):
        continuar = qsa.MessageBox.warning(
            util.translate(
                u"scripts",
                u"Antes de cargar un módulo asegúrese de tener una copia de seguridad de todos los datos,\ny de que no hay ningun otro usuario conectado a la base de datos mientras se realiza la carga.\n\n¿Desea continuar?",
            ),
            qsa.MessageBox.Yes,
            qsa.MessageBox.No,
        )
        if continuar == qsa.MessageBox.No:
            return
        nombreFichero = qsa.FileDialog.getOpenFileName(
            u"modfiles(*.mod)", util.translate(u"scripts", u"Elegir Fichero")
        )
        if nombreFichero:
            fichero = qsa.File(nombreFichero)
            if not qsa.from_project("formRecordflmodules").aceptarLicenciaDelModulo(
                qsa.ustr(fichero.path, u"/")
            ):
                qsa.MessageBox.critical(
                    util.translate(
                        u"scripts", u"Imposible cargar el módulo.\nLicencia del módulo no aceptada."
                    ),
                    qsa.MessageBox.Ok,
                )
                return
            modulo = None
            descripcion = None
            area = None
            desArea = None
            version = None
            nombreIcono = None
            versionMinimaFL = None
            dependencias = qsa.Array()
            fichero.open(qsa.File.ReadOnly)
            f = fichero.read()
            xmlModule = qsa.FLDomDocument()
            if xmlModule.setContent(f):
                nodeModule = xmlModule.namedItem(u"MODULE")
                if not nodeModule:
                    qsa.MessageBox.critical(
                        util.translate(u"scripts", u"Error en la carga del fichero xml .mod"),
                        qsa.MessageBox.Ok,
                        qsa.MessageBox.NoButton,
                    )
                modulo = nodeModule.namedItem(u"name").toElement().text()
                descripcion = nodeModule.namedItem(u"alias").toElement().text()
                area = nodeModule.namedItem(u"area").toElement().text()
                desArea = nodeModule.namedItem(u"areaname").toElement().text()
                version = nodeModule.namedItem(u"version").toElement().text()
                nombreIcono = nodeModule.namedItem(u"icon").toElement().text()
                if nodeModule.namedItem(u"flversion"):
                    versionMinimaFL = nodeModule.namedItem(u"flversion").toElement().text()
                if nodeModule.namedItem(u"dependencies"):
                    nodeDepend = xmlModule.elementsByTagName(u"dependency")
                    i = 0
                    while_pass = True
                    while i < len(nodeDepend):
                        if not while_pass:
                            i += 1
                            while_pass = True
                            continue
                        while_pass = False
                        dependencias[i] = nodeDepend.item(i).toElement().text()
                        i += 1
                        while_pass = True
                        try:
                            i < len(nodeDepend)
                        except Exception:
                            break

            else:
                aF = f.split(u"\n")
                modulo = dameValor(aF[0])
                descripcion = dameValor(aF[1])
                area = dameValor(aF[2])
                desArea = dameValor(aF[3])
                version = dameValor(aF[4])
                nombreIcono = dameValor(aF[5])
                if len(aF) > 6:
                    versionMinimaFL = dameValor(aF[6])
                if len(aF) > 7:
                    # DEBUG:: Argument 0 not understood
                    # DEBUG:: <Value><Constant><regexbody><regexchar
                    # arg00="LBRACKET"/><regexchar arg00="COMMA"/><regexchar
                    # arg00="SEMI"/><regexchar
                    # arg00="RBRACKET"/></regexbody></Constant></Value>
                    dependencias = dameValor(aF[7]).split(unknownarg)

            descripcion = traducirCadena(descripcion, fichero.path, modulo)
            desArea = traducirCadena(desArea, fichero.path, modulo)
            fichIcono = qsa.File(qsa.ustr(fichero.path, u"/", nombreIcono))
            fichIcono.open(qsa.File.ReadOnly)
            icono = fichIcono.read()

            # versionSys = sys.version().match("/ [ 0 - 9 ] + .[ 0 - 9 ] + /")
            # if compararVersiones(versionSys, versionMinimaFL) == 2:
            #    contVersion = MessageBox.warning(util.translate(u"scripts", u"Este módulo necesita la versión ") + versionMinimaFL + util.translate(u"scripts", u" o superior de la aplicación base,\nactualmente la versión instalada es la ") +
            #                                     sys.version() + util.translate(u"scripts", u".\nFacturaLUX puede fallar por esta causa.\n¿Desea continuar la carga?"), MessageBox.Yes, MessageBox.No)
            #    if contVersion == MessageBox.No:
            #        return
            if evaluarDependencias(dependencias) == False:
                return
            if not valorPorClave(u"flareas", u"idarea", ustr(u"idarea = '", area, u"'")):
                crearArea = qsa.MessageBox.warning(
                    util.translate(u"scripts", u"El área con el identificador ")
                    + area
                    + util.translate(u"scripts", u" no existe. ¿Desea crearla?"),
                    qsa.MessageBox.Yes,
                    qsa.MessageBox.No,
                )
                if crearArea == qsa.MessageBox.No:
                    return
                dialogo = qsa.Dialog()
                dialogo.width = 400
                dialogo.caption = qsa.ustr(util.translate(u"scripts", u"Crear área "), area, u":")
                dialogo.okButtonText = util.translate(u"scripts", u"Aceptar")
                dialogo.cancelButtonText = util.translate(u"scripts", u"Cancelar")
                leDesArea = qsa.LineEdit()
                leDesArea.text = desArea
                leDesArea.label = util.translate(u"scripts", u"Descripción: ")
                dialogo.add(leDesArea)
                if dialogo.exec_():
                    curArea = qsa.FLSqlCursor(u"flareas")
                    curArea.setModeAccess(curArea.Insert)
                    curArea.refreshBuffer()
                    curArea.setValueBuffer(u"idarea", area)
                    curArea.setValueBuffer(u"descripcion", leDesArea.text)
                    curArea.commitBuffer()

                else:
                    return

            recargar = None
            if valorPorClave(u"flmodules", u"idmodulo", ustr(u"idmodulo = '", modulo, u"'")):
                recargar = qsa.MessageBox.warning(
                    util.translate(u"scripts", u"El módulo ")
                    + modulo
                    + util.translate(u"scripts", u" ya existe. ¿Desea recargarlo?"),
                    qsa.MessageBox.Yes,
                    qsa.MessageBox.No,
                )
                if recargar == qsa.MessageBox.No:
                    return
            curModulo = qsa.FLSqlCursor(u"flmodules")
            if recargar == qsa.MessageBox.Yes:
                # WITH_START
                curModulo.select(ustr(u"idmodulo = '", modulo, u"'"))
                curModulo.first()
                curModulo.setModeAccess(curModulo.Edit)
                # WITH_END

            else:
                curModulo.setModeAccess(curModulo.Insert)

            # WITH_START
            curModulo.refreshBuffer()
            curModulo.setValueBuffer(u"idmodulo", modulo)
            curModulo.setValueBuffer(u"descripcion", descripcion)
            curModulo.setValueBuffer(u"idarea", area)
            curModulo.setValueBuffer(u"version", version)
            curModulo.setValueBuffer(u"icono", icono)
            curModulo.commitBuffer()
            # WITH_END
            curSeleccion = qsa.FLSqlCursor(u"flmodules")
            curModulo.setMainFilter(ustr(u"idmodulo = '", modulo, u"'"))
            curModulo.editRecord(False)
            qsa.from_project("formRecordflmodules").cargarDeDisco(
                qsa.ustr(fichero.path, u"/"), False
            )
            formRecordflmodules.accept()
            setting = "scripts/sys/modLastModule_%s" % qsa.sys.nameBD()
            nombreFichero = "%s" % os.path.abspath(nombreFichero)
            util.writeSettingEntry(setting, nombreFichero)
            qsa.aqApp.reinit()


def dameValor(self, linea=None):
    return linea


def valorPorClave(tabla=None, campo=None, where=None):
    valor = None
    query = qsa.FLSqlQuery()
    query.setTablesList(tabla)
    query.setSelect(campo)
    query.setFrom(tabla)
    query.setWhere(ustr(where, u";"))
    query.exec_()
    if query.next():
        valor = query.value(0)
    return valor


def compararVersiones(v1=None, v2=None):
    a1 = None
    a2 = None
    if v1 and v2:
        a1 = v1.split(u".")
        a2 = v2.split(u".")
        i = 0
        while_pass = True
        while i < len(a1):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            if qsa.parseInt(a1[i]) > qsa.parseInt(a2[i]):
                return 1
            if qsa.parseInt(a1[i]) < qsa.parseInt(a2[i]):
                return 2
            i += 1
            while_pass = True
            try:
                i < len(a1)
            except Exception:
                break

    return 0


def evaluarDependencias(dependencias=None):
    res = None
    if not dependencias:
        return True
    i = 0
    while_pass = True
    while i < len(dependencias):
        if not while_pass:
            i += 1
            while_pass = True
            continue
        while_pass = False
        if dependencias[i] == "":
            continue
        if qsa.sys.isLoadedModule(dependencias[i]) == False:
            res = qsa.MessageBox.warning(
                util.translate(u"scripts", u"Este módulo depende del módulo ")
                + dependencias[i]
                + util.translate(
                    u"scripts",
                    u", que no está instalado.\nFacturaLUX puede fallar por esta causa.\n¿Desea continuar la carga?",
                ),
                qsa.MessageBox.Yes,
                qsa.MessageBox.No,
            )
            if res == qsa.MessageBox.No:
                return False
        i += 1
        while_pass = True
        try:
            i < len(dependencias)
        except Exception:
            break

    return True


def traducirCadena(cadena=None, path=None, modulo=None):
    if cadena.find(u"QT_TRANSLATE_NOOP") == -1:
        return cadena
    cadena = qsa.QString(cadena).mid(41, len(cadena) - 43)
    nombreFichero = None
    try:
        nombreFichero = qsa.ustr(path, u"/translations/", modulo, u".", util.getIdioma(), u".ts")
    except Exception as e:
        e = traceback.format_exc()
        return cadena

    if not qsa.File.exists(nombreFichero):
        return cadena
    fichero = qsa.File(nombreFichero)
    fichero.open(qsa.File.ReadOnly)
    f = fichero.read()
    xmlTranslations = qsa.FLDomDocument()
    if xmlTranslations.setContent(f):
        nodeMess = xmlTranslations.elementsByTagName(u"message")
        i = 0
        while_pass = True
        while i < len(nodeMess):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            if nodeMess.item(i).namedItem(u"source").toElement().text() == cadena:
                traduccion = nodeMess.item(i).namedItem(u"translation").toElement().text()
                if traduccion:
                    cadena = traduccion
            i += 1
            while_pass = True
            try:
                i < len(nodeMess)
            except Exception:
                break

    return cadena


form = None
