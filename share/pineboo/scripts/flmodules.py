# -*- coding: utf-8 -*-

from pineboolib import qsatype
from pineboolib.qsaglobals import *
import traceback

class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        self.util = qsatype.FLUtil()
    
    def init(self):
        botonCargar = self.child(u"botonCargar")
        botonExportar = self.child(u"botonExportar")
        connect(botonCargar, u"clicked()", self, u"botonCargar_clicked")
        connect(botonExportar, u"clicked()", self, u"botonExportar_clicked")
        cursor = self.cursor()
        if cursor.modeAccess() == cursor.Browse:
            botonCargar.setEnabled(False)
            botonExportar.setEnabled(False)
    
    def cargarFicheroEnBD(self, nombre = None, contenido = None, log = None, directorio = None):
        if not util.isFLDefFile(contenido) and not nombre.endsWith(u".qs") and not nombre.endsWith(u".ar"):
            return 
        cursorFicheros = qsatype.FLSqlCursor(u"flfiles")
        cursor = self.cursor()
        cursorFicheros.select(ustr( u"nombre = '" , nombre , u"'" ))
        if not cursorFicheros.first():
            if nombre.endsWith(u".ar"):
                if not cargarAr(nombre, contenido, log, directorio):
                    return 
            log.append(util.translate(u"scripts", u"- Cargando :: ") + nombre)
            cursorFicheros.setModeAccess(cursorFicheros.Insert)
            cursorFicheros.refreshBuffer()
            cursorFicheros.setValueBuffer(u"nombre", nombre)
            cursorFicheros.setValueBuffer(u"idmodulo", cursor.valueBuffer(u"idmodulo"))
            cursorFicheros.setValueBuffer(u"sha", util.sha1(contenido))
            cursorFicheros.setValueBuffer(u"contenido", contenido)
            cursorFicheros.commitBuffer()
    
    def cargarAr(self, nombre = None, contenido = None, log = None, directorio = None):
        if not sys.isLoadedModule(u"eneboodev"):
            return False
        if util.readSettingEntry(u"scripts/sys/conversionAr") != u"true":
            return False
        log.append(util.translate(u"scripts", u"Convirtiendo %0 a kut").arg(nombre))
        contenido = sys.toUnicode(contenido, u"UTF-8")
        contenido = eneboodev.iface.pub_ar2kut(contenido)
        nombre = ustr( nombre.toString().left(qsa(nombre).length - 3) , u".kut" )
        if contenido:
            localEnc = util.readSettingEntry(u"scripts/sys/conversionArENC")
            if not localEnc:
                localEnc = u"ISO-8859-15"
            contenido = sys.fromUnicode(contenido, localEnc)
            self.cargarFicheroEnBD(nombre, contenido, log, directorio)
            log.append(util.translate(u"scripts", u"Volcando a disco ") + nombre)
            File.write(Dir.cleanDirPath(ustr( directorio , u"/" , nombre )), contenido)
        
        return True
    
    def cargarFicheros(self, directorio = None, extension = None):
        dir = qsatype.Dir(directorio)
        ficheros = dir.entryList(extension, Dir.Files)
        log = self.child(u"log")
        i = 0
        while i < qsa(ficheros).length:
            self.cargarFicheroEnBD(ficheros[i], File.read(Dir.cleanDirPath(ustr( directorio , u"/" , ficheros[i] ))), log, directorio)
            sys.processEvents()
            i += 1
    
    def botonCargar_clicked(self):
        directorio = FileDialog.getExistingDirectory(u"", util.translate(u"scripts", u"Elegir Directorio"))
        self.cargarDeDisco(directorio, True)
    
    def botonExportar_clicked(self):
        directorio = FileDialog.getExistingDirectory(u"", util.translate(u"scripts", u"Elegir Directorio"))
        self.exportarADisco(directorio)
    
    def aceptarLicenciaDelModulo(self, directorio = None):
        licencia = Dir.cleanDirPath(ustr( directorio , u"/COPYING" ))
        if not File.exists(licencia):
            MessageBox.critical(util.translate(u"scripts", ustr( u"El fichero " , licencia , u" con la licencia del módulo no existe.\nEste fichero debe existir para poder aceptar la licencia que contiene." )), MessageBox.Ok)
            return False
        licencia = File.read(licencia)
        dialog = qsatype.Dialog()
        dialog.width = 600
        dialog.caption = util.translate(u"scripts", u"Acuerdo de Licencia.")
        dialog.newTab(util.translate(u"scripts", u"Acuerdo de Licencia."))
        texto = qsatype.TextEdit()
        qsa(texto).text = licencia
        dialog.add(texto)
        dialog.okButtonText = util.translate(u"scripts", u"Sí, acepto este acuerdo de licencia.")
        dialog.cancelButtonText = util.translate(u"scripts", u"No, no acepto este acuerdo de licencia.")
        if dialog.exec_():
            return True
    
    def cargarDeDisco(self, directorio = None, comprobarLicencia = None):
        if directorio:
            if comprobarLicencia:
                if not aceptarLicenciaDelModulo(directorio):
                    MessageBox.critical(util.translate(u"scripts", u"Imposible cargar el módulo.\nLicencia del módulo no aceptada."), MessageBox.Ok)
                    return 
            sys.cleanupMetaData()
            if self.cursor().commitBuffer():
                self.child(u"idMod").setDisabled(True)
                log = self.child(u"log")
                qsa(log).text = u""
                sys.processEvents()
                self.setDisabled(True)
                self.cargarFicheros(ustr( directorio , u"/" ), u"*.xml")
                self.cargarFicheros(ustr( directorio , u"/forms/" ), u"*.ui")
                self.cargarFicheros(ustr( directorio , u"/tables/" ), u"*.mtd")
                self.cargarFicheros(ustr( directorio , u"/scripts/" ), u"*.qs")
                self.cargarFicheros(ustr( directorio , u"/queries/" ), u"*.qry")
                self.cargarFicheros(ustr( directorio , u"/reports/" ), u"*.kut")
                self.cargarFicheros(ustr( directorio , u"/reports/" ), u"*.ar")
                self.cargarFicheros(ustr( directorio , u"/translations/" ), u"*.ts")
                self.setDisabled(False)
                log.append(util.translate(u"scripts", u"* Carga finalizada."))
                self.child(u"lineas").refresh()
    
    def tipoDeFichero(self, nombre = None):
        posPunto = nombre.lastIndexOf(u".")
        return nombre.right(qsa(nombre).length - posPunto)
    
    def exportarADisco(self, directorio = None):
        if directorio:
            curFiles = self.child(u"lineas").cursor()
            cursorModules = qsatype.FLSqlCursor(u"flmodules")
            cursorAreas = qsatype.FLSqlCursor(u"flareas")
            if curFiles.size() != 0:
                dir = qsatype.Dir()
                idModulo = self.cursor().valueBuffer(u"idmodulo")
                log = self.child(u"log")
                qsa(log).text = u""
                directorio = Dir.cleanDirPath(ustr( directorio , u"/" , idModulo ))
                if not dir.fileExists(directorio):
                    dir.mkdir(directorio)
                if not dir.fileExists(ustr( directorio , u"/forms" )):
                    dir.mkdir(ustr( directorio , u"/forms" ))
                if not dir.fileExists(ustr( directorio , u"/scripts" )):
                    dir.mkdir(ustr( directorio , u"/scripts" ))
                if not dir.fileExists(ustr( directorio , u"/queries" )):
                    dir.mkdir(ustr( directorio , u"/queries" ))
                if not dir.fileExists(ustr( directorio , u"/tables" )):
                    dir.mkdir(ustr( directorio , u"/tables" ))
                if not dir.fileExists(ustr( directorio , u"/reports" )):
                    dir.mkdir(ustr( directorio , u"/reports" ))
                if not dir.fileExists(ustr( directorio , u"/translations" )):
                    dir.mkdir(ustr( directorio , u"/translations" ))
                curFiles.first()
                file = None
                tipo = None
                contenido = ""
                self.setDisabled(True)
                # DEBUG:: * not-known-seq * <DoWhile><Source><InstructionUpdate><Identifier name="file"/><OpUpdate type="EQUALS"/><Value><Member><Identifier name="curFiles"/><FunctionCall name="valueBuffer"><CallArguments><Value><Constant delim="&quot;" type="String" value="nombre"/></Value></CallArguments></FunctionCall></Member></Value></InstructionUpdate><InstructionUpdate><Identifier name="tipo"/><OpUpdate type="EQUALS"/><Value><FunctionCall name="tipoDeFichero"><CallArguments><Value><Identifier name="file"/></Value></CallArguments></FunctionCall></Value></InstructionUpdate><InstructionUpdate><Identifier name="contenido"/><OpUpdate type="EQUALS"/><Value><Member><Identifier name="curFiles"/><FunctionCall name="valueBuffer"><CallArguments><Value><Constant delim="&quot;" type="String" value="contenido"/></Value></CallArguments></FunctionCall></Member></Value></InstructionUpdate><If><Condition><Value><OpUnary type="LNOT"><Member><Identifier name="contenido"/><FunctionCall name="isEmpty"/></Member></OpUnary></Value></Condition><Source><Switch><Condition><Value><Identifier name="tipo"/></Value></Condition><Case><Value><Constant delim="&quot;" type="String" value=".xml"/></Value><Source><InstructionCall><Member><Identifier name="sys"/><FunctionCall name="write"><CallArguments><Value><Constant delim="&quot;" type="String" value="ISO-8859-1"/></Value><Expression><Identifier name="directorio"/><OpMath type="PLUS"/><Constant delim="&quot;" type="String" value="/"/><OpMath type="PLUS"/><Identifier name="file"/></Expression><Value><Identifier name="contenido"/></Value></CallArguments></FunctionCall></Member></InstructionCall><InstructionCall><Member><Identifier name="log"/><FunctionCall name="append"><CallArguments><Value><Member><Identifier name="util"/><FunctionCall name="translate"><CallArguments><Value><Constant delim="&quot;" type="String" value="scripts"/></Value><Expression><Constant delim="&quot;" type="String" value="* Exportando "/><OpMath type="PLUS"/><Identifier name="file"/><OpMath type="PLUS"/><Constant delim="&quot;" type="String" value="."/></Expression></CallArguments></FunctionCall></Member></Value></CallArguments></FunctionCall></Member></InstructionCall><InstructionFlow type="BREAK"/></Source></Case><Case><Value><Constant delim="&quot;" type="String" value=".ui"/></Value><Source><InstructionCall><Member><Identifier name="sys"/><FunctionCall name="write"><CallArguments><Value><Constant delim="&quot;" type="String" value="ISO-8859-1"/></Value><Expression><Identifier name="directorio"/><OpMath type="PLUS"/><Constant delim="&quot;" type="String" value="/forms/"/><OpMath type="PLUS"/><Identifier name="file"/></Expression><Value><Identifier name="contenido"/></Value></CallArguments></FunctionCall></Member></InstructionCall><InstructionCall><Member><Identifier name="log"/><FunctionCall name="append"><CallArguments><Value><Member><Identifier name="util"/><FunctionCall name="translate"><CallArguments><Value><Constant delim="&quot;" type="String" value="scripts"/></Value><Expression><Constant delim="&quot;" type="String" value="* Exportando "/><OpMath type="PLUS"/><Identifier name="file"/><OpMath type="PLUS"/><Constant delim="&quot;" type="String" value="."/></Expression></CallArguments></FunctionCall></Member></Value></CallArguments></FunctionCall></Member></InstructionCall><InstructionFlow type="BREAK"/></Source></Case><Case><Value><Constant delim="&quot;" type="String" value=".qs"/></Value><Source><InstructionCall><Member><Identifier name="sys"/><FunctionCall name="write"><CallArguments><Value><Constant delim="&quot;" type="String" value="ISO-8859-1"/></Value><Expression><Identifier name="directorio"/><OpMath type="PLUS"/><Constant delim="&quot;" type="String" value="/scripts/"/><OpMath type="PLUS"/><Identifier name="file"/></Expression><Value><Identifier name="contenido"/></Value></CallArguments></FunctionCall></Member></InstructionCall><InstructionCall><Member><Identifier name="log"/><FunctionCall name="append"><CallArguments><Value><Member><Identifier name="util"/><FunctionCall name="translate"><CallArguments><Value><Constant delim="&quot;" type="String" value="scripts"/></Value><Expression><Constant delim="&quot;" type="String" value="* Exportando "/><OpMath type="PLUS"/><Identifier name="file"/><OpMath type="PLUS"/><Constant delim="&quot;" type="String" value="."/></Expression></CallArguments></FunctionCall></Member></Value></CallArguments></FunctionCall></Member></InstructionCall><InstructionFlow type="BREAK"/></Source></Case><Case><Value><Constant delim="&quot;" type="String" value=".qry"/></Value><Source><InstructionCall><Member><Identifier name="sys"/><FunctionCall name="write"><CallArguments><Value><Constant delim="&quot;" type="String" value="ISO-8859-1"/></Value><Expression><Identifier name="directorio"/><OpMath type="PLUS"/><Constant delim="&quot;" type="String" value="/queries/"/><OpMath type="PLUS"/><Identifier name="file"/></Expression><Value><Identifier name="contenido"/></Value></CallArguments></FunctionCall></Member></InstructionCall><InstructionCall><Member><Identifier name="log"/><FunctionCall name="append"><CallArguments><Value><Member><Identifier name="util"/><FunctionCall name="translate"><CallArguments><Value><Constant delim="&quot;" type="String" value="scripts"/></Value><Expression><Constant delim="&quot;" type="String" value="* Exportando "/><OpMath type="PLUS"/><Identifier name="file"/><OpMath type="PLUS"/><Constant delim="&quot;" type="String" value="."/></Expression></CallArguments></FunctionCall></Member></Value></CallArguments></FunctionCall></Member></InstructionCall><InstructionFlow type="BREAK"/></Source></Case><Case><Value><Constant delim="&quot;" type="String" value=".mtd"/></Value><Source><InstructionCall><Member><Identifier name="sys"/><FunctionCall name="write"><CallArguments><Value><Constant delim="&quot;" type="String" value="ISO-8859-1"/></Value><Expression><Identifier name="directorio"/><OpMath type="PLUS"/><Constant delim="&quot;" type="String" value="/tables/"/><OpMath type="PLUS"/><Identifier name="file"/></Expression><Value><Identifier name="contenido"/></Value></CallArguments></FunctionCall></Member></InstructionCall><InstructionCall><Member><Identifier name="log"/><FunctionCall name="append"><CallArguments><Value><Member><Identifier name="util"/><FunctionCall name="translate"><CallArguments><Value><Constant delim="&quot;" type="String" value="scripts"/></Value><Expression><Constant delim="&quot;" type="String" value="* Exportando "/><OpMath type="PLUS"/><Identifier name="file"/><OpMath type="PLUS"/><Constant delim="&quot;" type="String" value="."/></Expression></CallArguments></FunctionCall></Member></Value></CallArguments></FunctionCall></Member></InstructionCall><InstructionFlow type="BREAK"/></Source></Case><Case><Value><Constant delim="&quot;" type="String" value=".kut"/></Value><Source><InstructionCall><Member><Identifier name="sys"/><FunctionCall name="write"><CallArguments><Value><Constant delim="&quot;" type="String" value="ISO-8859-1"/></Value><Expression><Identifier name="directorio"/><OpMath type="PLUS"/><Constant delim="&quot;" type="String" value="/reports/"/><OpMath type="PLUS"/><Identifier name="file"/></Expression><Value><Identifier name="contenido"/></Value></CallArguments></FunctionCall></Member></InstructionCall><InstructionCall><Member><Identifier name="log"/><FunctionCall name="append"><CallArguments><Value><Member><Identifier name="util"/><FunctionCall name="translate"><CallArguments><Value><Constant delim="&quot;" type="String" value="scripts"/></Value><Expression><Constant delim="&quot;" type="String" value="* Exportando "/><OpMath type="PLUS"/><Identifier name="file"/><OpMath type="PLUS"/><Constant delim="&quot;" type="String" value="."/></Expression></CallArguments></FunctionCall></Member></Value></CallArguments></FunctionCall></Member></InstructionCall><InstructionFlow type="BREAK"/></Source></Case><Case><Value><Constant delim="&quot;" type="String" value=".ts"/></Value><Source><InstructionCall><Member><Identifier name="sys"/><FunctionCall name="write"><CallArguments><Value><Constant delim="&quot;" type="String" value="ISO-8859-1"/></Value><Expression><Identifier name="directorio"/><OpMath type="PLUS"/><Constant delim="&quot;" type="String" value="/translations/"/><OpMath type="PLUS"/><Identifier name="file"/></Expression><Value><Identifier name="contenido"/></Value></CallArguments></FunctionCall></Member></InstructionCall><InstructionCall><Member><Identifier name="log"/><FunctionCall name="append"><CallArguments><Value><Member><Identifier name="util"/><FunctionCall name="translate"><CallArguments><Value><Constant delim="&quot;" type="String" value="scripts"/></Value><Expression><Constant delim="&quot;" type="String" value="* Exportando "/><OpMath type="PLUS"/><Identifier name="file"/><OpMath type="PLUS"/><Constant delim="&quot;" type="String" value="."/></Expression></CallArguments></FunctionCall></Member></Value></CallArguments></FunctionCall></Member></InstructionCall><InstructionFlow type="BREAK"/></Source></Case><CaseDefault><Source><InstructionCall><Member><Identifier name="log"/><FunctionCall name="append"><CallArguments><Value><Member><Identifier name="util"/><FunctionCall name="translate"><CallArguments><Value><Constant delim="&quot;" type="String" value="scripts"/></Value><Expression><Constant delim="&quot;" type="String" value="* Omitiendo "/><OpMath type="PLUS"/><Identifier name="file"/><OpMath type="PLUS"/><Constant delim="&quot;" type="String" value="."/></Expression></CallArguments></FunctionCall></Member></Value></CallArguments></FunctionCall></Member></InstructionCall></Source></CaseDefault></Switch></Source></If><InstructionCall><Member><Identifier name="sys"/><FunctionCall name="processEvents"/></Member></InstructionCall></Source><Condition><Value><Member><Identifier name="curFiles"/><FunctionCall name="next"/></Member></Value></Condition></DoWhile>
                cursorModules.select(ustr( u"idmodulo = '" , idModulo , u"'" ))
                if cursorModules.first():
                    cursorAreas.select(ustr( u"idarea = '" , cursorModules.valueBuffer(u"idarea") , u"'" ))
                    cursorAreas.first()
                    areaName = cursorAreas.valueBuffer(u"descripcion")
                    sys.write(u"ISO-8859-1", ustr( directorio , u"/" , cursorModules.valueBuffer(u"idmodulo") , u".xpm" ), cursorModules.valueBuffer(u"icono"))
                    log.append(util.translate(u"scripts", ustr( u"* Exportando " , cursorModules.valueBuffer(u"idmodulo") , u".xpm ." )))
                    contenido = ustr( u'<!DOCTYPE MODULE>\n<MODULE>\n<name>' , cursorModules.valueBuffer(u"idmodulo") , u'</name>\n<alias>QT_TRANSLATE_NOOP("FLWidgetApplication","' , cursorModules.valueBuffer(u"descripcion") , u'")</alias>\n<area>' , cursorModules.valueBuffer(u"idarea") , u'</area>\n<areaname>QT_TRANSLATE_NOOP("FLWidgetApplication","' , areaName , u'")</areaname>\n<version>' , cursorModules.valueBuffer(u"version") , u'</version>\n<icon>' , cursorModules.valueBuffer(u"idmodulo") , u'.xpm</icon>\n<flversion>' , cursorModules.valueBuffer(u"version") , u'</flversion>\n<description>' , cursorModules.valueBuffer(u"idmodulo") , u'</description>\n</MODULE>' )
                    sys.write(u"ISO-8859-1", ustr( directorio , u"/" , cursorModules.valueBuffer(u"idmodulo") , u".mod" ), contenido)
                    log.append(util.translate(u"scripts", ustr( u"* Generando " , cursorModules.valueBuffer(u"idmodulo") , u".mod ." )))
                
                self.setDisabled(False)
                log.append(util.translate(u"scripts", u"* Exportación finalizada."))
    


form = None
