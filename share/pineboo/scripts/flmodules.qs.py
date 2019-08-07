# -*- coding: utf-8 -*-
from pineboolib.qsa import qsa


class FormInternalObj(qsa.FormDBWidget):
    def _class_init(self):
        pass

    def init(self):
        botonCargar = self.child(u"botonCargar")
        botonExportar = self.child(u"botonExportar")
        connect(botonCargar, u"clicked()", self, u"botonCargar_clicked")
        connect(botonExportar, u"clicked()", self, u"botonExportar_clicked")
        cursor = self.cursor()
        if cursor.modeAccess() == cursor.Browse:
            botonCargar.setEnabled(False)
            botonExportar.setEnabled(False)

    def cargarFicheroEnBD(self, nombre=None, contenido=None, log=None, directorio=None):
        if (
            not qsa.util.isFLDefFile(contenido)
            and not nombre.endswith(u".mod")
            and not nombre.endswith(u".xpm")
            and not nombre.endswith(u".signatures")
            and not nombre.endswith(u".checksum")
            and not nombre.endswith(u".certificates")
            and not nombre.endswith(u".qs")
            and not nombre.endswith(u".ar")
            and not nombre.endswith(u".qs.py")
            and not nombre.endswith(u".kut")
        ):
            return
        cursorFicheros = qsa.FLSqlCursor(u"flfiles")
        cursor = self.cursor()
        cursorFicheros.select(ustr(u"nombre = '", nombre, u"'"))
        if not cursorFicheros.first():
            if nombre.endswith(u".ar"):
                if not self.cargarAr(nombre, contenido, log, directorio):
                    return
            log.append(util.translate(u"scripts", u"- Cargando :: ") + nombre)
            cursorFicheros.setModeAccess(cursorFicheros.Insert)
            cursorFicheros.refreshBuffer()
            cursorFicheros.setValueBuffer(u"nombre", nombre)
            cursorFicheros.setValueBuffer(u"idmodulo", cursor.valueBuffer(u"idmodulo"))
            cursorFicheros.setValueBuffer(u"sha", qsa.util.sha1(contenido))
            cursorFicheros.setValueBuffer(u"contenido", contenido)
            cursorFicheros.commitBuffer()

        else:
            cursorFicheros.setModeAccess(cursorFicheros.Edit)
            cursorFicheros.refreshBuffer()
            contenidoCopia = cursorFicheros.valueBuffer(u"contenido")
            if contenidoCopia != contenido:
                log.append(util.translate(u"scripts", u"- Actualizando :: ") + nombre)
                cursorFicheros.setModeAccess(cursorFicheros.Insert)
                cursorFicheros.refreshBuffer()
                d = qsa.Date()
                cursorFicheros.setValueBuffer(u"nombre", nombre + qsa.parseString(d))
                cursorFicheros.setValueBuffer(u"idmodulo", cursor.valueBuffer(u"idmodulo"))
                cursorFicheros.setValueBuffer(u"contenido", contenidoCopia)
                cursorFicheros.commitBuffer()
                log.append(
                    util.translate(u"scripts", u"- Backup :: ") + nombre + qsa.parseString(d)
                )
                cursorFicheros.select(ustr(u"nombre = '", nombre, u"'"))
                cursorFicheros.first()
                cursorFicheros.setModeAccess(cursorFicheros.Edit)
                cursorFicheros.refreshBuffer()
                cursorFicheros.setValueBuffer(u"idmodulo", cursor.valueBuffer(u"idmodulo"))
                cursorFicheros.setValueBuffer(u"sha", util.sha1(contenido))
                cursorFicheros.setValueBuffer(u"contenido", contenido)
                cursorFicheros.commitBuffer()
                if nombre.endswith(u".ar"):
                    self.cargarAr(nombre, contenido, log, directorio)

    def cargarAr(self, nombre=None, contenido=None, log=None, directorio=None):
        if not qsa.sys.isLoadedModule(u"flar2kut"):
            return False
        if qsa.util.readSettingEntry(u"scripts/sys/conversionAr") != u"true":
            return False
        log.append(util.translate(u"scripts", u"Convirtiendo %s a kut") % (str(nombre)))
        contenido = qsa.sys.toUnicode(contenido, u"UTF-8")
        contenido = qsa.from_project("flar2kut").iface.pub_ar2kut(contenido)
        nombre = qsa.ustr(qsa.parseString(nombre)[0 : len(nombre) - 3], u".kut")
        if contenido:
            localEnc = qsa.util.readSettingEntry(u"scripts/sys/conversionArENC")
            if not localEnc:
                localEnc = u"ISO-8859-15"
            contenido = qsa.sys.fromUnicode(contenido, localEnc)
            self.cargarFicheroEnBD(nombre, contenido, log, directorio)
            log.append(util.translate(u"scripts", u"Volcando a disco ") + nombre)
            qsa.File.write(qsa.Dir.cleanDirPath(ustr(directorio, u"/", nombre)), contenido)

        else:
            log.append(qsa.util.translate(u"scripts", u"Error de conversión"))
            return False

        return True

    def cargarFicheros(self, directorio=None, extension=None):
        dir = qsa.Dir(directorio)
        ficheros = dir.entryList(extension, qsa.Dir.Files)
        log = self.child(u"log")
        i = 0
        from pineboolib.fllegacy.flsettings import FLSettings
        from pineboolib.application.parsers.qsaparser import postparse
        import os

        settings = qsa.FLSettings()
        while_pass = True
        while i < len(ficheros):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            path_ = qsa.Dir.cleanDirPath(ustr(directorio, u"/", ficheros[i]))
            if settings.readBoolEntry("ebcomportamiento/parseModulesOnLoad", False):
                file_py_path_ = "%s.py" % path_
                if os.path.exists(file_py_path_):
                    os.remove(file_py_path_)
                if path_.endswith(".qs"):
                    postparse.pythonify([path_])
                if os.path.exists(file_py_path_):
                    value_py = File(file_py_path_).read()
                    self.cargarFicheroEnBD("%s.py" % ficheros[i], value_py, log, directorio)

            value = qsa.File(path_).read()
            self.cargarFicheroEnBD(ficheros[i], value, log, directorio)
            qsa.sys.processEvents()
            i += 1
            while_pass = True
            try:
                i < len(ficheros)
            except Exception:
                break

    def botonCargar_clicked(self):
        directorio = qsa.FileDialog.getExistingDirectory(
            u"", qsa.util.translate(u"scripts", u"Elegir Directorio")
        )
        self.cargarDeDisco(directorio, True)

    def botonExportar_clicked(self):
        directorio = qsa.FileDialog.getExistingDirectory(
            u"", qsa.util.translate(u"scripts", u"Elegir Directorio")
        )
        self.exportarADisco(directorio)

    def aceptarLicenciaDelModulo(self, directorio=None):
        licencia = qsa.Dir.cleanDirPath(qsa.ustr(directorio, u"/COPYING"))
        if not qsa.File.exists(licencia):
            qsa.MessageBox.critical(
                util.translate(
                    u"scripts",
                    qsa.ustr(
                        u"El fichero ",
                        licencia,
                        u" con la licencia del módulo no existe.\nEste fichero debe existir para poder aceptar la licencia que contiene.",
                    ),
                ),
                qsa.MessageBox.Ok,
            )
            return False
        licencia = qsa.File.read(licencia)
        dialog = qsa.Dialog()
        dialog.width = 600
        dialog.caption = qsa.util.translate(u"scripts", u"Acuerdo de Licencia.")
        dialog.newTab(qsa.util.translate(u"scripts", u"Acuerdo de Licencia."))
        texto = qsa.TextEdit()
        texto.text = licencia
        dialog.add(texto)
        dialog.okButtonText = qsa.util.translate(
            u"scripts", u"Sí, acepto este acuerdo de licencia."
        )
        dialog.cancelButtonText = qsa.util.translate(
            u"scripts", u"No, no acepto este acuerdo de licencia."
        )
        if dialog.exec_():
            return True
        else:
            return False

    def cargarDeDisco(self, directorio=None, comprobarLicencia=None):
        if directorio:
            if comprobarLicencia:
                if not self.aceptarLicenciaDelModulo(directorio):
                    MessageBox.critical(
                        util.translate(
                            u"scripts",
                            u"Imposible cargar el módulo.\nLicencia del módulo no aceptada.",
                        ),
                        qsa.MessageBox.Ok,
                    )
                    return
            qsa.sys.cleanupMetaData()
            qsa.sys.processEvents()
            if self.cursor().commitBuffer():
                self.child(u"idMod").setDisabled(True)
                log = self.child(u"log")
                log.text = u""
                self.setDisabled(True)
                self.cargarFicheros(ustr(directorio, u"/"), u"*.xml")
                self.cargarFicheros(ustr(directorio, u"/"), u"*.mod")
                self.cargarFicheros(ustr(directorio, u"/"), u"*.xpm")
                self.cargarFicheros(ustr(directorio, u"/"), u"*.signatures")
                self.cargarFicheros(ustr(directorio, u"/"), u"*.certificates")
                self.cargarFicheros(ustr(directorio, u"/"), u"*.checksum")
                self.cargarFicheros(ustr(directorio, u"/forms/"), u"*.ui")
                self.cargarFicheros(ustr(directorio, u"/tables/"), u"*.mtd")
                self.cargarFicheros(ustr(directorio, u"/scripts/"), u"*.qs")
                self.cargarFicheros(ustr(directorio, u"/scripts/"), u"*.qs.py")
                self.cargarFicheros(ustr(directorio, u"/queries/"), u"*.qry")
                self.cargarFicheros(ustr(directorio, u"/reports/"), u"*.kut")
                self.cargarFicheros(ustr(directorio, u"/reports/"), u"*.ar")
                self.cargarFicheros(ustr(directorio, u"/translations/"), u"*.ts")
                self.setDisabled(False)
                log.append(qsa.util.translate(u"scripts", u"* Carga finalizada."))
                self.child(u"lineas").refresh()

    def tipoDeFichero(self, nombre=None):
        posPunto = nombre.rfind(u".")
        return nombre[posPunto:]

    def exportarADisco(self, directorio=None):
        if directorio:
            curFiles = self.child(u"lineas").cursor()
            cursorModules = qsa.FLSqlCursor(u"flmodules")
            cursorAreas = qsa.FLSqlCursor(u"flareas")
            if curFiles.size() != 0:
                dir = qsa.Dir()
                idModulo = self.cursor().valueBuffer(u"idmodulo")
                log = self.child(u"log")
                log.text = u""
                directorio = qsa.Dir.cleanDirPath(qsa.ustr(directorio, u"/", idModulo))
                if not dir.fileExists(directorio):
                    dir.mkdir(directorio)
                if not dir.fileExists(qsa.ustr(directorio, u"/forms")):
                    dir.mkdir(qsa.ustr(directorio, u"/forms"))
                if not dir.fileExists(ustr(directorio, u"/scripts")):
                    dir.mkdir(qsa.ustr(directorio, u"/scripts"))
                if not dir.fileExists(ustr(directorio, u"/queries")):
                    dir.mkdir(qsa.ustr(directorio, u"/queries"))
                if not dir.fileExists(ustr(directorio, u"/tables")):
                    dir.mkdir(qsa.ustr(directorio, u"/tables"))
                if not dir.fileExists(ustr(directorio, u"/reports")):
                    dir.mkdir(qsa.ustr(directorio, u"/reports"))
                if not dir.fileExists(ustr(directorio, u"/translations")):
                    dir.mkdir(qsa.ustr(directorio, u"/translations"))
                curFiles.first()
                file = None
                tipo = None
                contenido = ""
                self.setDisabled(True)
                s01_dowhile_1stloop = True
                while s01_dowhile_1stloop or curFiles.next():
                    s01_dowhile_1stloop = False
                    file = curFiles.valueBuffer(u"nombre")
                    tipo = self.tipoDeFichero(file)
                    contenido = curFiles.valueBuffer(u"contenido")
                    if not contenido == "":
                        s01_when = tipo
                        s01_do_work, s01_work_done = False, False
                        if s01_when == u".xml":
                            s01_do_work, s01_work_done = True, True
                        if s01_do_work:
                            qsa.sys.write(
                                u"ISO-8859-1", qsa.ustr(directorio, u"/", file), contenido
                            )
                            log.append(
                                qsa.util.translate(
                                    u"scripts", qsa.ustr(u"* Exportando ", file, u".")
                                )
                            )
                            s01_do_work = False  # BREAK
                        if s01_when == u".mod":
                            s01_do_work, s01_work_done = True, True
                        if s01_do_work:
                            qsa.sys.write(
                                u"ISO-8859-1", qsa.ustr(directorio, u"/", file), contenido
                            )
                            log.append(
                                qsa.util.translate(
                                    u"scripts", qsa.ustr(u"* Exportando ", file, u".")
                                )
                            )
                            s01_do_work = False  # BREAK
                        if s01_when == u".xpm":
                            s01_do_work, s01_work_done = True, True
                        if s01_do_work:
                            qsa.sys.write(
                                u"ISO-8859-1", qsa.ustr(directorio, u"/", file), contenido
                            )
                            log.append(
                                qsa.util.translate(
                                    u"scripts", qsa.ustr(u"* Exportando ", file, u".")
                                )
                            )
                            s01_do_work = False  # BREAK
                        if s01_when == u".signatures":
                            s01_do_work, s01_work_done = True, True
                        if s01_do_work:
                            qsa.sys.write(
                                u"ISO-8859-1", qsa.ustr(directorio, u"/", file), contenido
                            )
                            log.append(
                                qsa.util.translate(
                                    u"scripts", qsa.ustr(u"* Exportando ", file, u".")
                                )
                            )
                            s01_do_work = False  # BREAK
                        if s01_when == u".certificates":
                            s01_do_work, s01_work_done = True, True
                        if s01_do_work:
                            qsa.sys.write(
                                u"ISO-8859-1", qsa.ustr(directorio, u"/", file), contenido
                            )
                            log.append(
                                qsa.util.translate(
                                    u"scripts", qsa.ustr(u"* Exportando ", file, u".")
                                )
                            )
                            s01_do_work = False  # BREAK
                        if s01_when == u".checksum":
                            s01_do_work, s01_work_done = True, True
                        if s01_do_work:
                            qsa.sys.write(
                                u"ISO-8859-1", qsa.ustr(directorio, u"/", file), contenido
                            )
                            log.append(
                                qsa.util.translate(
                                    u"scripts", qsa.ustr(u"* Exportando ", file, u".")
                                )
                            )
                            s01_do_work = False  # BREAK
                        if s01_when == u".ui":
                            s01_do_work, s01_work_done = True, True
                        if s01_do_work:
                            qsa.sys.write(
                                u"ISO-8859-1", qsa.ustr(directorio, u"/forms/", file), contenido
                            )
                            log.append(
                                qsa.util.translate(
                                    u"scripts", qsa.ustr(u"* Exportando ", file, u".")
                                )
                            )
                            s01_do_work = False  # BREAK
                        if s01_when == u".qs":
                            s01_do_work, s01_work_done = True, True
                        if s01_do_work:
                            qsa.sys.write(
                                u"ISO-8859-1", qsa.ustr(directorio, u"/scripts/", file), contenido
                            )
                            log.append(
                                qsa.util.translate(
                                    u"scripts", qsa.ustr(u"* Exportando ", file, u".")
                                )
                            )
                            s01_do_work = False  # BREAK
                        if s01_when == u".py":
                            s01_do_work, s01_work_done = True, True
                        if s01_do_work:
                            qsa.sys.write(
                                u"UTF-8", qsa.ustr(directorio, u"/scripts/", file), contenido
                            )
                            log.append(
                                qsa.util.translate(
                                    u"scripts", qsa.ustr(u"* Exportando ", file, u".")
                                )
                            )
                            s01_do_work = False  # BREAK

                        if s01_when == u".qry":
                            s01_do_work, s01_work_done = True, True
                        if s01_do_work:
                            qsa.sys.write(
                                u"ISO-8859-1", qsa.ustr(directorio, u"/queries/", file), contenido
                            )
                            log.append(
                                qsa.util.translate(
                                    u"scripts", qsa.ustr(u"* Exportando ", file, u".")
                                )
                            )
                            s01_do_work = False  # BREAK
                        if s01_when == u".mtd":
                            s01_do_work, s01_work_done = True, True
                        if s01_do_work:
                            qsa.sys.write(
                                u"ISO-8859-1", qsa.ustr(directorio, u"/tables/", file), contenido
                            )
                            log.append(
                                qsa.util.translate(
                                    u"scripts", qsa.ustr(u"* Exportando ", file, u".")
                                )
                            )
                            s01_do_work = False  # BREAK
                        if s01_when == u".kut":
                            s01_do_work, s01_work_done = True, True
                        if s01_do_work:
                            qsa.sys.write(
                                u"ISO-8859-1", qsa.ustr(directorio, u"/reports/", file), contenido
                            )
                            log.append(
                                qsa.util.translate(
                                    u"scripts", qsa.ustr(u"* Exportando ", file, u".")
                                )
                            )
                            s01_do_work = False  # BREAK
                        if s01_when == u".ts":
                            s01_do_work, s01_work_done = True, True
                        if s01_do_work:
                            qsa.sys.write(
                                u"ISO-8859-1",
                                qsa.ustr(directorio, u"/translations/", file),
                                contenido,
                            )
                            log.append(
                                qsa.util.translate(
                                    u"scripts", qsa.ustr(u"* Exportando ", file, u".")
                                )
                            )
                            s01_do_work = False  # BREAK
                        if not s01_work_done:
                            s01_do_work, s01_work_done = True, True
                        if s01_do_work:
                            log.append(
                                qsa.util.translate(
                                    u"scripts", qsa.ustr(u"* Omitiendo ", file, u".")
                                )
                            )

                    qsa.sys.processEvents()

                cursorModules.select(ustr(u"idmodulo = '", idModulo, u"'"))
                if cursorModules.first():
                    cursorAreas.select(
                        qsa.ustr(u"idarea = '", cursorModules.valueBuffer(u"idarea"), u"'")
                    )
                    cursorAreas.first()
                    areaName = cursorAreas.valueBuffer(u"descripcion")
                    if not qsa.File.exists(
                        qsa.ustr(directorio, u"/", cursorModules.valueBuffer(u"idmodulo"), u".xpm")
                    ):
                        qsa.sys.write(
                            u"ISO-8859-1",
                            qsa.ustr(
                                directorio, u"/", cursorModules.valueBuffer(u"idmodulo"), u".xpm"
                            ),
                            cursorModules.valueBuffer(u"icono"),
                        )
                        log.append(
                            qsa.util.translate(
                                u"scripts",
                                qsa.ustr(
                                    u"* Exportando ",
                                    cursorModules.valueBuffer(u"idmodulo"),
                                    u".xpm (Regenerado).",
                                ),
                            )
                        )
                    if not qsa.File.exists(
                        qsa.ustr(directorio, u"/", cursorModules.valueBuffer(u"idmodulo"), u".mod")
                    ):
                        contenido = ustr(
                            u"<!DOCTYPE MODULE>\n<MODULE>\n<name>",
                            cursorModules.valueBuffer(u"idmodulo"),
                            u'</name>\n<alias>QT_TRANSLATE_NOOP("FLWidgetApplication","',
                            cursorModules.valueBuffer(u"descripcion"),
                            u'")</alias>\n<area>',
                            cursorModules.valueBuffer(u"idarea"),
                            u'</area>\n<areaname>QT_TRANSLATE_NOOP("FLWidgetApplication","',
                            areaName,
                            u'")</areaname>\n<version>',
                            cursorModules.valueBuffer(u"version"),
                            u"</version>\n<icon>",
                            cursorModules.valueBuffer(u"idmodulo"),
                            u".xpm</icon>\n<flversion>",
                            cursorModules.valueBuffer(u"version"),
                            u"</flversion>\n<description>",
                            cursorModules.valueBuffer(u"idmodulo"),
                            u"</description>\n</MODULE>",
                        )
                        qsa.sys.write(
                            u"ISO-8859-1",
                            qsa.ustr(
                                directorio, u"/", cursorModules.valueBuffer(u"idmodulo"), u".mod"
                            ),
                            contenido,
                        )
                        log.append(
                            qsa.util.translate(
                                u"scripts",
                                qsa.ustr(
                                    u"* Generando ",
                                    cursorModules.valueBuffer(u"idmodulo"),
                                    u".mod (Regenerado).",
                                ),
                            )
                        )

                self.setDisabled(False)
                log.append(qsa.util.translate(u"scripts", u"* Exportación finalizada."))


form = None
