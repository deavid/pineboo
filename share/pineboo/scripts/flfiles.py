# -*- coding: utf-8 -*-
from pineboolib import qsatype
from pineboolib.qsaglobals import *
import traceback

class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        pass
    
    def init(self):
        qsa(self.child(u"contenido")).text = self.cursor().valueBuffer(u"contenido")
        botonEditar = self.child(u"botonEditar")
        pbXMLEditor = self.child(u"pbXMLEditor")
        cursor = self.cursor()
        if cursor.modeAccess() == cursor.Browse:
            botonEditar.setEnabled(False)
            pbXMLEditor.setEnabled(False)
    
    def acceptedForm(self):
        self.cursor().setValueBuffer(u"contenido", qsa(self.child(u"contenido")).text)
    
    def tipoDeFichero(self, nombre = None):
        posPunto = nombre.lastIndexOf(u".")
        return nombre.right(qsa(nombre).length - posPunto)
    
    def editarFichero(self):
        cursor = self.cursor()
        if cursor.checkIntegrity():
            self.child(u"nombre").setDisabled(True)
            nombre = cursor.valueBuffer(u"nombre")
            tipo = tipoDeFichero(nombre)
            temporal = System.getenv(u"TMP")
            if temporal.isEmpty():
                temporal = System.getenv(u"TMPDIR")
            if temporal.isEmpty():
                temporal = System.getenv(u"HOME")
            if temporal.isEmpty():
                temporal = ustr( sys.installPrefix() , u"/share/facturalux/tmp" )
            temporal = ustr( temporal , u"/" , cursor.valueBuffer(u"nombre") )
            contenido = qsa(self.child(u"contenido")).text
            s51_when = tipo
            s51_do_work,s51_work_done = False,False
            if s51_when == u".ui": s51_do_work,s51_work_done = True,True
            if s51_do_work:
                File.write(temporal, contenido)
                comando = ustr( sys.installPrefix() , u"/bin/designer" )
                self.setDisabled(True)
                Process.execute(qsatype.Array([comando, temporal]))
                qsa(self.child(u"contenido")).text = File.read(temporal)
                self.setDisabled(False)
                s51_do_work = False # BREAK
            
            if s51_when == u".ts": s51_do_work,s51_work_done = True,True
            if s51_do_work:
                File.write(temporal, contenido)
                comando = ustr( sys.installPrefix() , u"/bin/linguist" )
                self.setDisabled(True)
                Process.execute(qsatype.Array([comando, temporal]))
                qsa(self.child(u"contenido")).text = File.read(temporal)
                self.setDisabled(False)
                s51_do_work = False # BREAK
            
            if s51_when == u".kut": s51_do_work,s51_work_done = True,True
            if s51_do_work:
                File.write(temporal, contenido)
                comando = ustr( sys.installPrefix() , u"/bin/kudesigner" )
                self.setDisabled(True)
                Process.execute(qsatype.Array([comando, temporal]))
                qsa(self.child(u"contenido")).text = File.read(temporal)
                self.setDisabled(False)
                s51_do_work = False # BREAK
            
            if s51_when == u".qs": s51_do_work,s51_work_done = True,True
            if s51_do_work:
                self.setDisabled(True)
                editor = qsatype.FLScriptEditor(nombre)
                editor.exec_()
                qsa(self.child(u"contenido")).text = editor.code()
                self.setDisabled(False)
                s51_do_work = False # BREAK
            
            if not s51_work_done: s51_do_work,s51_work_done = True,True
            if s51_do_work:
                self.setDisabled(True)
                dialog = qsatype.Dialog()
                dialog.width = 600
                dialog.cancelButtonText = u""
                editor = qsatype.TextEdit()
                editor.textFormat = editor.PlainText
                qsa(editor).text = contenido
                dialog.add(editor)
                dialog.exec_()
                qsa(self.child(u"contenido")).text = qsa(editor).text
                self.setDisabled(False)
    
    def editarFicheroXML(self):
        cursor = self.cursor()
        if cursor.checkIntegrity():
            temporal = System.getenv(u"TMP")
            if temporal.isEmpty():
                temporal = System.getenv(u"TMPDIR")
            if temporal.isEmpty():
                temporal = System.getenv(u"HOME")
            if temporal.isEmpty():
                temporal = ustr( sys.installPrefix() , u"/share/facturalux/tmp" )
            temporal = ustr( temporal , u"/" , cursor.valueBuffer(u"nombre") )
            contenido = qsa(self.child(u"contenido")).text
            File.write(temporal, contenido)
            comando = ustr( sys.installPrefix() , u"/bin/teddy" )
            self.setDisabled(True)
            Process.execute(qsatype.Array([comando, temporal]))
            qsa(self.child(u"contenido")).text = File.read(temporal)
            self.setDisabled(False)
    
    def calculateField(self, fN = None):
        if fN == u"sha":
            util = qsatype.FLUtil()
            return util.sha1(self.cursor().valueBuffer(u"contenido"))
    


form = None
