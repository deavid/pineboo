# -*- coding: utf-8 -*-
from pineboolib.qsa import qsa
import traceback


class interna(object):
    ctx = qsa.Object()

    def __init__(self, context=None):
        self.ctx = context

    def main(self):
        self.ctx.interna_main()

    def init(self):
        self.ctx.interna_init()


class oficial(interna):
    pathLocal = ""
    idFuncional = ""
    bloqueo = qsa.Boolean()

    def __init__(self, context=None):
        super(oficial, self).__init__(context)

    def cargarModulo(self, nombreFichero=None):
        return self.ctx.oficial_cargarModulo(nombreFichero)

    def compararVersiones(self, v1=None, v2=None):
        return self.ctx.oficial_compararVersiones(v1, v2)

    def traducirCadena(self, cadena=None, path=None, modulo=None):
        return self.ctx.oficial_traducirCadena(cadena, path, modulo)


class head(oficial):
    def __init__(self, context=None):
        super(head, self).__init__(context)


class ifaceCtx(head):
    def __init__(self, context=None):
        super(ifaceCtx, self).__init__(context)


class FormInternalObj(qsa.FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)

    def interna_init(self):
        pass

    def interna_main(self):
        util = qsa.FLUtil()
        setting = "scripts/sys/modLastModule_%s" % qsa.sys.nameBD()
        fichMod = util.readSettingEntry(setting)
        if not fichMod:
            fichMod = qsa.FileDialog.getOpenFileName(
                util.translate(u"scripts", u"Módulo a cargar (*.mod)"),
                util.translate(u"scripts", u"Módulo a cargar"),
            )
            if not fichMod:
                return
            util.writeSettingEntry(setting, fichMod)

        qsa.sys.processEvents()
        self.iface.cargarModulo(fichMod)
        qsa.sys.reinit()

    def oficial_cargarModulo(self, nombreFichero=None):
        util = qsa.FLUtil()
        fichero = qsa.File(nombreFichero)
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

        descripcion = self.iface.traducirCadena(descripcion, fichero.path, modulo)
        desArea = self.iface.traducirCadena(desArea, fichero.path, modulo)
        fichIcono = qsa.File(ustr(fichero.path, u"/", nombreIcono))
        fichIcono.open(qsa.File.ReadOnly)
        icono = fichIcono.read()
        # DEBUG:: Argument 0 not understood
        # DEBUG:: <Value><Constant><regexbody><regexchar
        # arg00="LBRACKET"/><regexchar arg00="ICONST:'0'"/><regexchar
        # arg00="MINUS"/><regexchar arg00="ICONST:'9'"/><regexchar
        # arg00="RBRACKET"/><regexchar arg00="PLUS"/><regexchar
        # arg00="PERIOD"/><regexchar arg00="LBRACKET"/><regexchar
        # arg00="ICONST:'0'"/><regexchar arg00="MINUS"/><regexchar
        # arg00="ICONST:'9'"/><regexchar arg00="RBRACKET"/><regexchar
        # arg00="PLUS"/></regexbody></Constant></Value>
        # versionSys = sys.version().match(unknownarg)
        # if self.iface.compararVersiones(versionSys, versionMinimaFL) == 2:
        #    contVersion = MessageBox.warning(util.translate(u"scripts", u"Este módulo necesita la versión ") + versionMinimaFL + util.translate(u"scripts", u" o superior de la aplicación base,\nactualmente la versión instalada es la ") +
        #                                     sys.version() + util.translate(u"scripts", u".\nFacturaLUX puede fallar por esta causa.\n¿Desea continuar la carga?"), MessageBox.Yes, MessageBox.No)
        #    if contVersion == MessageBox.No:
        #        return
        if not util.sqlSelect(u"flareas", u"idarea", ustr(u"idarea = '", area, u"'")):
            if not util.sqlInsert(u"flareas", u"idarea,descripcion", ustr(area, u",", desArea)):
                qsa.MessageBox.warning(
                    util.translate(u"scripts", u"Error al crear el área:\n") + area,
                    qsa.MessageBox.Ok,
                    qsa.MessageBox.NoButton,
                )
                return False
        recargar = util.sqlSelect(u"flmodules", u"idmodulo", ustr(u"idmodulo = '", modulo, u"'"))
        curModulo = qsa.FLSqlCursor(u"flmodules")
        if recargar:
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
        qsa.from_project("formRecordflmodules").cargarDeDisco(ustr(fichero.path, u"/"), False)
        qsa.from_project("formRecordflmodules").accept()
        return True

    def oficial_compararVersiones(self, v1=None, v2=None):
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

    def oficial_traducirCadena(self, cadena=None, path=None, modulo=None):
        util = qsa.FLUtil()
        if cadena.find(u"QT_TRANSLATE_NOOP") == -1:
            return cadena
        cadena = qsa.QString(cadena).mid(41, len(cadena) - 43)
        nombreFichero = None
        try:
            nombreFichero = qsa.ustr(
                path, u"/translations/", modulo, u".", util.getIdioma(), u".ts"
            )
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
