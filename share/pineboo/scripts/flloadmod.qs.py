util = qsatype.FLUtil()
def main():
    continuar = MessageBox.warning(util.translate(u"scripts", u"Antes de cargar un módulo asegúrese de tener una copia de seguridad de todos los datos,\ny de que no hay ningun otro usuario conectado a la base de datos mientras se realiza la carga.\n\n¿Desea continuar?"), MessageBox.Yes, MessageBox.No)
    if continuar == MessageBox.No:
        return 
    nombreFichero = FileDialog.getOpenFileName(u"modfiles(*.mod)", util.translate(u"scripts", u"Elegir Fichero"))
    if nombreFichero:
        fichero = qsatype.File(nombreFichero)
        if not formRecordflmodules.aceptarLicenciaDelModulo(ustr( fichero.path , u"/" )):
            MessageBox.critical(util.translate(u"scripts", u"Imposible cargar el módulo.\nLicencia del módulo no aceptada."), MessageBox.Ok)
            return 
        modulo = None
        descripcion = None
        area = None
        desArea = None
        version = None
        nombreIcono = None
        versionMinimaFL = None
        dependencias = []
        fichero.open(File.ReadOnly)
        f = fichero.read()
        xmlModule = qsatype.FLDomDocument()
        if xmlModule.setContent(f):
            nodeModule = xmlModule.namedItem(u"MODULE")
            if not nodeModule:
                MessageBox.critical(util.translate(u"scripts", u"Error en la carga del fichero xml .mod"), MessageBox.Ok, MessageBox.NoButton)
            modulo = qsa(nodeModule.namedItem(u"name").toElement()).text()
            descripcion = qsa(nodeModule.namedItem(u"alias").toElement()).text()
            area = qsa(nodeModule.namedItem(u"area").toElement()).text()
            desArea = qsa(nodeModule.namedItem(u"areaname").toElement()).text()
            version = qsa(nodeModule.namedItem(u"version").toElement()).text()
            nombreIcono = qsa(nodeModule.namedItem(u"icon").toElement()).text()
            if nodeModule.namedItem(u"flversion"):
                versionMinimaFL = qsa(nodeModule.namedItem(u"flversion").toElement()).text()
            if nodeModule.namedItem(u"dependencies"):
                nodeDepend = xmlModule.elementsByTagName(u"dependency")
                i = 0
                while i < qsa(nodeDepend).length():
                    dependencias[i] = qsa(nodeDepend.item(i).toElement()).text()
                    i += 1
        
        else:
            aF = f.split(u"\n")
            modulo = dameValor(aF[0])
            descripcion = dameValor(aF[1])
            area = dameValor(aF[2])
            desArea = dameValor(aF[3])
            version = dameValor(aF[4])
            nombreIcono = dameValor(aF[5])
            if qsa(aF).length > 6:
                versionMinimaFL = dameValor(aF[6])
            if qsa(aF).length > 7:
                # DEBUG:: Argument 0 not understood
                # DEBUG:: <Value><Constant><regexbody><regexchar arg00="LBRACKET"/><regexchar arg00="COMMA"/><regexchar arg00="RBRACKET"/></regexbody></Constant></Value>
                dependencias = dameValor(aF[7]).split(unknownarg)
        
        descripcion = traducirCadena(descripcion, fichero.path, modulo)
        desArea = traducirCadena(desArea, fichero.path, modulo)
        fichIcono = qsatype.File(ustr( fichero.path , u"/" , nombreIcono ))
        fichIcono.open(File.ReadOnly)
        icono = fichIcono.read()
        # DEBUG:: Argument 0 not understood
        # DEBUG:: <Value><Constant><regexbody><regexchar arg00="LBRACKET"/><regexchar arg00="ICONST:'0'"/><regexchar arg00="MINUS"/><regexchar arg00="ICONST:'9'"/><regexchar arg00="RBRACKET"/><regexchar arg00="PLUS"/><regexchar arg00="PERIOD"/><regexchar arg00="LBRACKET"/><regexchar arg00="ICONST:'0'"/><regexchar arg00="MINUS"/><regexchar arg00="ICONST:'9'"/><regexchar arg00="RBRACKET"/><regexchar arg00="PLUS"/></regexbody></Constant></Value>
        versionSys = sys.version().match(unknownarg)
        if compararVersiones(versionSys, versionMinimaFL) == 2:
            contVersion = MessageBox.warning(util.translate(u"scripts", u"Este módulo necesita la versión ") + versionMinimaFL + util.translate(u"scripts", u" o superior de la aplicación base,\nactualmente la versión instalada es la ") + sys.version() + util.translate(u"scripts", u".\nFacturaLUX puede fallar por esta causa.\n¿Desea continuar la carga?"), MessageBox.Yes, MessageBox.No)
            if contVersion == MessageBox.No:
                return 
        if evaluarDependencias(dependencias) == False:
            return 
        if not valorPorClave(u"flareas", u"idarea", ustr( u"idarea = '" , area , u"'" )):
            crearArea = MessageBox.warning(util.translate(u"scripts", u"El área con el identificador ") + area + util.translate(u"scripts", u" no existe. ¿Desea crearla?"), MessageBox.Yes, MessageBox.No)
            if crearArea == MessageBox.No:
                return 
            dialogo = qsatype.Dialog()
            dialogo.width = 400
            dialogo.caption = ustr( util.translate(u"scripts", u"Crear área ") , area , u":" )
            dialogo.okButtonText = util.translate(u"scripts", u"Aceptar")
            dialogo.cancelButtonText = util.translate(u"scripts", u"Cancelar")
            leDesArea = qsatype.LineEdit()
            qsa(leDesArea).text = desArea
            leDesArea.label = util.translate(u"scripts", u"Descripción: ")
            dialogo.add(leDesArea)
            if dialogo.exec_():
                curArea = qsatype.FLSqlCursor(u"flareas")
                curArea.setModeAccess(curArea.Insert)
                curArea.refreshBuffer()
                curArea.setValueBuffer(u"idarea", area)
                curArea.setValueBuffer(u"descripcion", qsa(leDesArea).text)
                curArea.commitBuffer()
            
            else:
                return 
            
        
        recargar = None
        if valorPorClave(u"flmodules", u"idmodulo", ustr( u"idmodulo = '" , modulo , u"'" )):
            recargar = MessageBox.warning(util.translate(u"scripts", u"El módulo ") + modulo + util.translate(u"scripts", u" ya existe. ¿Desea recargarlo?"), MessageBox.Yes, MessageBox.No)
            if recargar == MessageBox.No:
                return 
        curModulo = qsatype.FLSqlCursor(u"flmodules")
        if recargar == MessageBox.Yes:
            w0d_obj = curModulo
            select(ustr( u"idmodulo = '" , modulo , u"'" ))
            first()
            setModeAccess(curModulo.Edit)
            del w0d_obj
        
        else:
            curModulo.setModeAccess(curModulo.Insert)
        
        wb8_obj = curModulo
        refreshBuffer()
        setValueBuffer(u"idmodulo", modulo)
        setValueBuffer(u"descripcion", descripcion)
        setValueBuffer(u"idarea", area)
        setValueBuffer(u"version", version)
        setValueBuffer(u"icono", icono)
        commitBuffer()
        del wb8_obj
        curSeleccion = qsatype.FLSqlCursor(u"flmodules")
        curModulo.setMainFilter(ustr( u"idmodulo = '" , modulo , u"'" ))
        curModulo.editRecord()
        formRecordflmodules.cargarDeDisco(ustr( fichero.path , u"/" ), False)
        formRecordflmodules.accept()
        setting = ustr( u"scripts/sys/modLastModule_" , sys.nameBD() )
        util.writeSettingEntry(setting, nombreFichero)

def dameValor(linea = None):
    return linea

def valorPorClave(tabla = None, campo = None, where = None):
    valor = None
    query = qsatype.FLSqlQuery()
    query.setTablesList(tabla)
    query.setSelect(campo)
    query.setFrom(tabla)
    query.setWhere(ustr( where , u";" ))
    query.exec_()
    if query.next():
        valor = query.value(0)
    return valor

def compararVersiones(v1 = None, v2 = None):
    a1 = None
    a2 = None
    if v1 and v2:
        a1 = v1.split(u".")
        a2 = v2.split(u".")
        i = 0
        while i < qsa(a1).length:
            if parseInt(a1[i]) > parseInt(a2[i]):
                return 1
            if parseInt(a1[i]) < parseInt(a2[i]):
                return 2
            i += 1
    
    return 0

def evaluarDependencias(dependencias = None):
    res = None
    if not dependencias:
        return True
    i = 0
    while i < qsa(dependencias).length:
        if dependencias[i].isEmpty():
            continue 
        if sys.isLoadedModule(dependencias[i]) == False:
            res = MessageBox.warning(util.translate(u"scripts", u"Este módulo depende del módulo ") + dependencias[i] + util.translate(u"scripts", u", que no está instalado.\nFacturaLUX puede fallar por esta causa.\n¿Desea continuar la carga?"), MessageBox.Yes, MessageBox.No)
            if res == MessageBox.No:
                return False
        i += 1
    
    return True

def traducirCadena(cadena = None, path = None, modulo = None):
    if cadena.find(u"QT_TRANSLATE_NOOP") == - 1:
        return cadena
    cadena = cadena.mid(41, qsa(cadena).length - 43)
    nombreFichero = None
    try:
        nombreFichero = ustr( path , u"/translations/" , modulo , u"." , util.getIdioma() , u".ts" )
    except Exception as e:
        e = traceback.format_exc()
        return cadena
    
    if not File.exists(nombreFichero):
        return cadena
    fichero = qsatype.File(nombreFichero)
    fichero.open(File.ReadOnly)
    f = fichero.read()
    xmlTranslations = qsatype.FLDomDocument()
    if xmlTranslations.setContent(f):
        nodeMess = xmlTranslations.elementsByTagName(u"message")
        i = 0
        while i < qsa(nodeMess).length():
            if qsa(nodeMess.item(i).namedItem(u"source").toElement()).text() == cadena:
                traduccion = qsa(nodeMess.item(i).namedItem(u"translation").toElement()).text()
                if traduccion:
                    cadena = traduccion
            i += 1
    
    return cadena

