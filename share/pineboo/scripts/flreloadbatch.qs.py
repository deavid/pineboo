# -*- coding: utf-8 -*-
from pineboolib.qsa import *


class interna(object):
    ctx = Object()

    def __init__(self, context=None):
        self.ctx = context

    def main(self):
        self.ctx.interna_main()

    def init(self):
        self.ctx.interna_init()


class oficial(interna):
    pathLocal = ""
    idFuncional = ""
    bloqueo = Boolean()

    def __init__(self, context=None):
        super(oficial, self).__init__(context)

    def cargarModulo(self, nombreFichero=None):
        return self.ctx.oficial_cargarModulo(nombreFichero)

    def compararVersiones(self, v1=None, v2=None):
        return self.ctx.oficial_compararVersiones(v1, v2)

    def traducirCadena(self, cadena=None, path=None, modulo=None):
        return self.ctx.oficial_traducirCadena(cadena, path, modulo)

    def ejecutarComando(self, comando=None):
        return self.ctx.oficial_ejecutarComando(comando)

    def elegirOpcion(self, opciones=None):
        return self.ctx.oficial_elegirOpcion(opciones)


class head(oficial):
    def __init__(self, context=None):
        super(head, self).__init__(context)


class ifaceCtx(head):
    def __init__(self, context=None):
        super(ifaceCtx, self).__init__(context)

    def pub_cargarModulo(self, nombreFichero=None):
        return self.cargarModulo(nombreFichero)


class FormInternalObj(FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)

    def interna_init(self):
        pass

    def interna_main(self):
        util = FLUtil()
        setting = "scripts/sys/modLastDirModules_%s" % sys.nameBD()
        dirAnt = util.readSettingEntry(setting)
        dirMods = FileDialog.getExistingDirectory(dirAnt, util.translate(u"scripts", u"Directorio de Módulos"))

        if not dirMods:
            return
        Dir().setCurrent(dirMods)

        resComando = Array()
        if util.getOS() == u"WIN32":
            resComando = self.iface.ejecutarComando(u"cmd.exe \/C dir \/B \/S *.mod")
        else:
            resComando = self.iface.ejecutarComando(u"find . -name *.mod")

        if resComando.ok == False:
            MessageBox.warning(
                util.translate(u"scripts", u"Error al buscar los módulos en el directorio:\n") + dirMods,
                MessageBox.Ok,
                MessageBox.NoButton,
                MessageBox.NoButton,
            )
            return

        opciones = resComando.salida.split(u"\n")
        opciones.pop()
        modulos = self.iface.elegirOpcion(opciones)
        if modulos == -1 or modulos == -2:
            return
        i = 0
        while_pass = True
        while i < len(modulos):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            sys.processEvents()
            if not self.iface.cargarModulo(modulos[i]):
                MessageBox.warning(
                    util.translate(u"scripts", u"Error al cargar el módulo:\n") + modulos[i],
                    MessageBox.Ok,
                    MessageBox.NoButton,
                    MessageBox.NoButton,
                )
                return
            i += 1
            while_pass = True
            try:
                i < len(modulos)
            except Exception:
                break

        util.writeSettingEntry(setting, dirMods)
        aqApp.reinit()

    def oficial_ejecutarComando(self, comando=None):
        res = Array()
        Process.execute(comando)
        if Process.stderr != u"":
            res[u"ok"] = False
            res[u"salida"] = Process.stderr
            if self.iface.pub_log:
                self.iface.pub_log.child(u"log").append(ustr(u"Error al ejecutar el comando: ", comando, u"\n", Process.stderr))
                self.iface.pub_log.child(u"log").append(res.salida)

        else:
            res[u"ok"] = True
            res[u"salida"] = Process.stdout

        return res

    def oficial_cargarModulo(self, nombreFichero=None):
        util = FLUtil()
        if util.getOS() == u"WIN32":
            nombreFichero = nombreFichero[0 : len(nombreFichero) - 1]

        if not isinstance(nombreFichero, str):
            nombreFichero = nombreFichero.data().decode("utf-8")

        fichero = File(nombreFichero, "iso-8859-15")
        modulo = None
        descripcion = None
        area = None
        desArea = None
        version = None
        nombreIcono = None
        versionMinimaFL = None
        dependencias = Array()
        fichero.open(File.ReadOnly)
        f = fichero.read()
        xmlModule = FLDomDocument()
        if xmlModule.setContent(f):
            nodeModule = xmlModule.namedItem(u"MODULE")
            if not nodeModule:
                MessageBox.critical(
                    util.translate(u"scripts", u"Error en la carga del fichero xml .mod"), MessageBox.Ok, MessageBox.NoButton
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
            modulo = self.iface.dameValor(aF[0])
            descripcion = self.iface.dameValor(aF[1])
            area = self.iface.dameValor(aF[2])
            desArea = self.iface.dameValor(aF[3])
            version = self.iface.dameValor(aF[4])
            nombreIcono = self.iface.dameValor(aF[5])
            if len(aF) > 6:
                versionMinimaFL = self.iface.dameValor(aF[6])
            if len(aF) > 7:
                # DEBUG:: Argument 0 not understood
                # DEBUG:: <Value><Constant><regexbody><regexchar
                # arg00="LBRACKET"/><regexchar arg00="COMMA"/><regexchar
                # arg00="SEMI"/><regexchar
                # arg00="RBRACKET"/></regexbody></Constant></Value>
                dependencias = self.ifacedameValor(aF[7]).split(unknownarg)

        descripcion = self.iface.traducirCadena(descripcion, fichero.path, modulo)
        desArea = self.iface.traducirCadena(desArea, fichero.path, modulo)
        fichIcono = File(ustr(fichero.path, u"/", nombreIcono))
        fichIcono.open(File.ReadOnly)
        icono = fichIcono.read()

        # DEBUG:: Argument 0 not understood
        # DEBUG:: <Value><Constant><regexbody><regexchar arg00="LBRACKET"/><regexchar arg00="ICONST:'0'"/><regexchar arg00="MINUS"/><regexchar arg00="ICONST:'9'"/><regexchar arg00="RBRACKET"/><regexchar arg00="PLUS"/><regexchar arg00="PERIOD"/><regexchar arg00="LBRACKET"/><regexchar arg00="ICONST:'0'"/><regexchar arg00="MINUS"/><regexchar arg00="ICONST:'9'"/><regexchar arg00="RBRACKET"/><regexchar arg00="PLUS"/></regexbody></Constant></Value>
        # versionSys = sys.version().match(unknownarg)
        # if self.iface.compararVersiones(versionSys, versionMinimaFL) == 2:
        #    contVersion = MessageBox.warning(util.translate(u"scripts", u"Este módulo necesita la versión ") + versionMinimaFL + util.translate(u"scripts", u" o superior de la aplicación base,\nactualmente la versión instalada es la ") + sys.version() + util.translate(u"scripts", u".\nFacturaLUX puede fallar por esta causa.\n¿Desea continuar la carga?"), MessageBox.Yes, MessageBox.No)
        #    if contVersion == MessageBox.No:
        #        return
        if not util.sqlSelect(u"flareas", u"idarea", ustr(u"idarea = '", area, u"'")):
            if not util.sqlInsert(u"flareas", u"idarea,descripcion", ustr(area, u",", desArea)):
                MessageBox.warning(util.translate(u"scripts", u"Error al crear el área:\n") + area, MessageBox.Ok, MessageBox.NoButton)
                return False
        recargar = util.sqlSelect(u"flmodules", u"idmodulo", ustr(u"idmodulo = '", modulo, u"'"))
        curModulo = FLSqlCursor(u"flmodules")
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
        curSeleccion = FLSqlCursor(u"flmodules")
        curModulo.setMainFilter(ustr(u"idmodulo = '", modulo, u"'"))
        curModulo.editRecord(False)
        formRecordflmodules.cargarDeDisco(u"%s/" % fichero.path, False)
        formRecordflmodules.accept()
        setting = "scripts/sys/modLastModule_%s" % sys.nameBD()
        nombreFichero = "%s" % os.path.abspath(nombreFichero)
        util.writeSettingEntry(setting, nombreFichero)
        sys.processEvents()
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
                if parseInt(a1[i]) > parseInt(a2[i]):
                    return 1
                if parseInt(a1[i]) < parseInt(a2[i]):
                    return 2
                i += 1
                while_pass = True
                try:
                    i < len(a1)
                except Exception:
                    break

        return 0

    def oficial_traducirCadena(self, cadena=None, path=None, modulo=None):
        util = FLUtil()
        if cadena.find(u"QT_TRANSLATE_NOOP") == -1:
            return cadena
        cadena2 = cadena
        cadena = QString(cadena).mid(41, len(cadena) - 43)
        nombreFichero = None
        try:
            nombreFichero = ustr(path, u"/translations/", modulo, u".", util.getIdioma(), u".ts")
        except Exception as e:
            e = traceback.format_exc()
            return cadena

        if not File.exists(nombreFichero):
            return cadena
        fichero = File(nombreFichero)
        fichero.open(File.ReadOnly)
        f = fichero.read()
        xmlTranslations = FLDomDocument()
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

    def oficial_elegirOpcion(self, opciones=None):
        util = FLUtil()
        dialog = Dialog()
        dialog.okButtonText = util.translate(u"scripts", u"Aceptar")
        dialog.cancelButtonText = util.translate(u"scripts", u"Cancelar")
        bgroup = GroupBox()
        bgroup.title = util.translate(u"scripts", u"Seleccione módulos a cargar")
        dialog.add(bgroup)
        resultado = Array()
        cB = Array()
        i = 0
        while_pass = True
        while i < len(opciones):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            cB[i] = CheckBox()
            bgroup.add(cB[i])
            cB[i].text = opciones[i]
            cB[i].checked = True
            i += 1
            while_pass = True
            try:
                i < len(opciones)
            except Exception:
                break

        indice = 0
        if dialog.exec_():
            i = 0
            while_pass = True
            while i < len(opciones):
                if not while_pass:
                    i += 1
                    while_pass = True
                    continue
                while_pass = False
                if cB[i].checked == True:
                    resultado[indice] = opciones[i]
                    indice += 1
                i += 1
                while_pass = True
                try:
                    i < len(opciones)
                except Exception:
                    break

        else:
            return -1

        if len(resultado) == 0:
            return -1
        return resultado


form = None
