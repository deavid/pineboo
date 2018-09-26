# -*- coding: utf-8 -*-
from pineboolib.qsa import *
import traceback
sys = SysType()


class FormInternalObj(FormDBWidget):
    def _class_init(self):
        pass

    def init(self):
        self.child(u"contenido").text = self.cursor().valueBuffer(u"contenido")
        botonEditar = self.child(u"botonEditar")
        pbXMLEditor = self.child(u"pbXMLEditor")
        cursor = self.cursor()
        if cursor.modeAccess() == cursor.Browse:
            botonEditar.setEnabled(False)
            pbXMLEditor.setEnabled(False)
        else:
            connect(botonEditar, u"clicked()", self, u"editarFichero")
            nombre = cursor.valueBuffer(u"nombre")
            tipo = self.tipoDeFichero(nombre)
            if tipo == u".ui" or tipo == u".ts" or tipo == u".qs":
                pbXMLEditor.setEnabled(False)
            else:
                connect(pbXMLEditor, u"clicked()", self, u"editarFicheroXML")

    def acceptedForm(self):
        self.cursor().setValueBuffer(u"contenido", self.child(u"contenido").text)

    def tipoDeFichero(self, nombre=None):
        posPunto = nombre.rfind(u".")
        return nombre[(len(nombre) - (len(nombre) - posPunto)):]

    def editarFichero(self):
        cursor = self.cursor()
        util = FLUtil()
        if cursor.checkIntegrity():
            self.child(u"nombre").setDisabled(True)
            nombre = cursor.valueBuffer(u"nombre")
            tipo = self.tipoDeFichero(nombre)
            temporal = System.getenv(u"TMP")
            if temporal == '':
                temporal = System.getenv(u"TMPDIR")
            if temporal == '':
                temporal = System.getenv(u"HOME")
            if temporal == '':
                temporal = ustr(sys.installPrefix(), u"/share/facturalux/tmp")
            temporal = ustr(temporal, u"/", cursor.valueBuffer(u"nombre"))
            contenido = self.child(u"contenido").text
            comando = ""
            s01_when = tipo
            s01_do_work, s01_work_done = False, False
            if s01_when == u".ui":
                s01_do_work, s01_work_done = True, True
            if s01_do_work:
                if util.getOS() == u"MACX":
                    File.write(temporal, ustr(contenido, u"\n\n\n\n\n\n\n\n\n\n\n\n\n\n"))
                    comando = ustr(sys.installPrefix(), u"/bin/designer.app/Contents/MacOS/designer")
                else:
                    File.write(temporal, contenido)
                    comando = ustr(sys.installPrefix(), u"/bin/designer")

                self.setDisabled(True)
                Process.execute(Array([comando, temporal]))
                self.child(u"contenido").text = File.read(temporal)
                self.setDisabled(False)
                s01_do_work = False  # BREAK

            if s01_when == u".ts":
                s01_do_work, s01_work_done = True, True
            if s01_do_work:
                if util.getOS() == u"MACX":
                    File.write(temporal, ustr(contenido, u"\n\n\n\n\n\n\n\n\n\n\n\n\n\n"))
                    comando = ustr(sys.installPrefix(), u"/bin/linguist.app/Contents/MacOS/linguist")
                else:
                    File.write(temporal, contenido)
                    comando = ustr(sys.installPrefix(), u"/bin/linguist")

                self.setDisabled(True)
                Process.execute(Array([comando, temporal]))
                self.child(u"contenido").text = File.read(temporal)
                self.setDisabled(False)
                s01_do_work = False  # BREAK

            if s01_when == u".kut":
                s01_do_work, s01_work_done = True, True
            if s01_do_work:
                if util.getOS() == u"MACX":
                    File.write(temporal, ustr(contenido, u"\n\n\n\n\n\n\n\n\n\n\n\n\n\n"))
                    comando = ustr(sys.installPrefix(), u"/bin/kudesigner.app/Contents/MacOS/kudesigner")
                else:
                    File.write(temporal, contenido)
                    comando = ustr(sys.installPrefix(), u"/bin/kudesigner")

                self.setDisabled(True)
                Process.execute(Array([comando, temporal]))
                self.child(u"contenido").text = File.read(temporal)
                self.setDisabled(False)
                s01_do_work = False  # BREAK

            if s01_when == u".qs":
                s01_do_work, s01_work_done = True, True
            if s01_do_work:
                self.setDisabled(True)
                editor = FLScriptEditor(nombre)
                editor.exec_()
                self.child(u"contenido").text = editor.code()
                self.setDisabled(False)
                s01_do_work = False  # BREAK

            if not s01_work_done:
                s01_do_work, s01_work_done = True, True
            if s01_do_work:
                self.setDisabled(True)
                dialog = Dialog()
                dialog.width = 600
                dialog.cancelButtonText = u""
                editor = TextEdit()
                editor.textFormat = editor.PlainText
                editor.text = contenido
                dialog.add(editor)
                dialog.exec_()
                self.child(u"contenido").text = editor.text
                self.setDisabled(False)

    def editarFicheroXML(self):
        cursor = self.cursor()
        util = FLUtil()
        if cursor.checkIntegrity():
            temporal = System.getenv(u"TMP")
            if temporal == '':
                temporal = System.getenv(u"TMPDIR")
            if temporal == '':
                temporal = System.getenv(u"HOME")
            if temporal == '':
                temporal = ustr(sys.installPrefix(), u"/share/facturalux/tmp")
            temporal = ustr(temporal, u"/", cursor.valueBuffer(u"nombre"))
            comando = ""
            contenido = self.child(u"contenido").text
            if util.getOS() == u"MACX":
                File.write(temporal, ustr(contenido, u"\n\n\n\n\n\n\n\n\n\n\n\n\n\n"))
                comando = ustr(sys.installPrefix(), u"/bin/teddy.app/Contents/MacOS/teddy")
            else:
                File.write(temporal, contenido)
                comando = ustr(sys.installPrefix(), u"/bin/teddy")

            self.setDisabled(True)
            Process.execute(Array([comando, temporal]))
            self.child(u"contenido").text = File.read(temporal)
            self.setDisabled(False)

    def calculateField(self, fN=None):
        if fN == u"sha":
            util = FLUtil()
            return util.sha1(self.cursor().valueBuffer(u"contenido"))


form = None
