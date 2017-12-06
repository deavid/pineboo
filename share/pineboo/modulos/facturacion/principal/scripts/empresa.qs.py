# -*- coding: utf-8 -*-
from pineboolib import qsatype
from pineboolib.qsaglobals import *
import traceback
sys = SysType()

class interna(object):
    ctx = qsatype.Object()
    def __init__(self, context = None):
        self.ctx = context
    
    def main(self):
        self.ctx.interna_main()
    
    def init(self):
        self.ctx.interna_init()
    
    def validateForm(self):
        return self.ctx.interna_validateForm()
    

class oficial(interna):
    pbnCambiarEjercicioActual = qsatype.Object()
    bloqueoProvincia = qsatype.Boolean()
    def __init__(self, context = None):
        super(oficial, self).__init__(context)
    
    def pbnCambiarEjercicioActual_clicked(self):
        return self.ctx.oficial_pbnCambiarEjercicioActual_clicked()
    
    def mostrarEjercicioActual(self):
        return self.ctx.oficial_mostrarEjercicioActual()
    
    def cambiarEjercicioActual(self):
        return self.ctx.oficial_cambiarEjercicioActual()
    
    def bufferChanged(self, fN = None):
        return self.ctx.oficial_bufferChanged(fN)
    

class navegador(oficial):
    def __init__(self, context = None):
        super(navegador, self).__init__(context)
    
    def init(self):
        return self.ctx.navegador_init()
    
    def cambiarNavegador(self):
        return self.ctx.navegador_cambiarNavegador()
    

class envioMail(navegador):
    def __init__(self, context = None):
        super(envioMail, self).__init__(context)
    
    def init(self):
        return self.ctx.envioMail_init()
    
    def cambiarClienteCorreo(self):
        return self.ctx.envioMail_cambiarClienteCorreo()
    
    def cambiarNombreCorreo(self):
        return self.ctx.envioMail_cambiarNombreCorreo()
    
    def cambiarDirIntermedia(self):
        return self.ctx.envioMail_cambiarDirIntermedia()
    

class head(envioMail):
    def __init__(self, context = None):
        super(head, self).__init__(context)
    

class ifaceCtx(head):
    def __init__(self, context = None):
        super(ifaceCtx, self).__init__(context)
    
    def pub_cambiarEjercicioActual(self):
        return self.cambiarEjercicioActual()
    

class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)
    
    def interna_init(self):
        cursor = self.cursor()
        self.iface.pbnCambiarEjercicioActual = self.child(u"pbnCambiarEjercicioActual")
        self.iface.bloqueoProvincia = False
        connect(self.iface.pbnCambiarEjercicioActual, u"clicked()", self, u"iface.pbnCambiarEjercicioActual_clicked")
        connect(cursor, u"bufferChanged(QString)", self, u"iface.bufferChanged")
        if not flfactppal.iface.pub_ejercicioActual():
            flfactppal.iface.pub_cambiarEjercicioActual(self.cursor().valueBuffer(u"codejercicio"))
        self.child(u"fdbCodEjercicio").close()
        self.child(u"fdbNombreEjercicio").close()
        self.iface.mostrarEjercicioActual()
    
    def interna_main(self):
        f = qsatype.FLFormSearchDB(u"empresa")
        cursor = f.cursor()
        cursor.select()
        if not cursor.first():
            cursor.setModeAccess(cursor.Insert)
        else:
            cursor.setModeAccess(cursor.Edit)
        
        f.setMainWidget()
        if cursor.modeAccess() == cursor.Insert:
            f.child(u"pushButtonCancel").setDisabled(True)
        cursor.refreshBuffer()
        commitOk = False
        acpt = qsatype.Boolean()
        cursor.transaction(False)
        while not commitOk:
            acpt = False
            f.exec_(u"nombre")
            acpt = f.accepted()
            if not acpt:
                if cursor.rollback():
                    commitOk = True
            else:
                if cursor.commitBuffer():
                    cursor.commit()
                    commitOk = True
            
    
    def interna_validateForm(self):
        util = qsatype.FLUtil()
        if not sys.isLoadedModule(u"flcontppal") and self.cursor().valueBuffer(u"contintegrada") == True:
            MessageBox.warning(util.translate(u"scripts", u"No puede activarse la contabilidad integrada si no está cargado el módulo principal de Contabilidad"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton)
            return False
        return True
    
    def oficial_pbnCambiarEjercicioActual_clicked(self):
        if not self.iface.cambiarEjercicioActual():
            return 
        self.iface.mostrarEjercicioActual()
    
    def oficial_cambiarEjercicioActual(self):
        f = qsatype.FLFormSearchDB(u"ejercicios")
        f.setMainWidget()
        codEjercicio = f.exec_(u"codejercicio")
        if not codEjercicio:
            return False
        ok = flfactppal.iface.pub_cambiarEjercicioActual(codEjercicio)
        return ok
    
    def oficial_mostrarEjercicioActual(self):
        util = qsatype.FLUtil()
        codEjercicio = flfactppal.iface.pub_ejercicioActual()
        nombreEjercicio = util.sqlSelect(u"ejercicios", u"nombre", ustr( u"codejercicio='" , codEjercicio , u"'" ))
        try:
            sys.setCaptionMainWidget(nombreEjercicio)
            self.child(u"lblValEjercicioActual").text = ustr( codEjercicio , u" - " , nombreEjercicio )
            self.child(u"lblEjercicioActual").text = ustr( util.translate(u"scripts", u"Ejercicio actual para ") , sys.nameUser() , u":" )
        except Exception as e:
            e = traceback.format_exc()
        
    
    def oficial_bufferChanged(self, fN = None):
        util = qsatype.FLUtil()
        cursor = self.cursor()
        sb2_when = fN
        sb2_do_work,sb2_work_done = False,False
        if sb2_when == u"provincia": sb2_do_work,sb2_work_done = True,True
        if sb2_do_work:
            if not self.iface.bloqueoProvincia:
                self.iface.bloqueoProvincia = True
                flfactppal.iface.pub_obtenerProvincia(self)
                self.iface.bloqueoProvincia = False
            sb2_do_work = False # BREAK
    
    def navegador_init(self):
        super(navegador, self.iface).init()
        util = qsatype.FLUtil()
        self.child(u"lblNombreNavegador").text = util.readSettingEntry(u"scripts/flfactinfo/nombrenavegador")
        connect(self.child(u"pbnCambiarNavegador"), u"clicked()", self, u"iface.cambiarNavegador")
    
    def navegador_cambiarNavegador(self):
        util = qsatype.FLUtil()
        nombreNavegador = Input.getText(util.translate(u"scripts", u"Nombre del navegador o ruta de acceso:"))
        if not nombreNavegador:
            return 
        self.child(u"lblNombreNavegador").text = nombreNavegador
        util.writeSettingEntry(u"scripts/flfactinfo/nombrenavegador", nombreNavegador)
    
    def envioMail_init(self):
        super(envioMail, self.iface).init()
        util = qsatype.FLUtil()
        self.child(u"lblClienteCorreo").text = util.readSettingEntry(u"scripts/flfactinfo/clientecorreo")
        self.child(u"lblNombreCorreo").text = util.readSettingEntry(u"scripts/flfactinfo/nombrecorreo")
        self.child(u"lblDirIntermedia").text = util.readSettingEntry(u"scripts/flfactinfo/dirCorreo")
        connect(self.child(u"pbnCambiarClienteCorreo"), u"clicked()", self, u"iface.cambiarClienteCorreo")
        connect(self.child(u"pbnCambiarNombreCorreo"), u"clicked()", self, u"iface.cambiarNombreCorreo")
        connect(self.child(u"pbnCambiarDirIntermedia"), u"clicked()", self, u"iface.cambiarDirIntermedia")
    
    def envioMail_cambiarClienteCorreo(self):
        util = qsatype.FLUtil()
        opciones = qsatype.Array([u"KMail", u"Thunderbird", u"Outlook"])
        codClienteCorreo = Input.getItem(util.translate(u"scripts", u"Cliente de correo:"), opciones, u"KMail", False)
        if not codClienteCorreo:
            return 
        self.child(u"lblClienteCorreo").text = codClienteCorreo
        util.writeSettingEntry(u"scripts/flfactinfo/clientecorreo", codClienteCorreo)
        nombreCorreo = u""
        s3d_when = codClienteCorreo
        s3d_do_work,s3d_work_done = False,False
        if s3d_when == u"KMail": s3d_do_work,s3d_work_done = True,True
        if s3d_do_work:
            nombreCorreo = u"kmail"
            s3d_do_work = False # BREAK
        if s3d_when == u"Thunderbird": s3d_do_work,s3d_work_done = True,True
        if s3d_do_work:
            nombreCorreo = u"thunderbird"
            s3d_do_work = False # BREAK
        if s3d_when == u"Outlook": s3d_do_work,s3d_work_done = True,True
        if s3d_do_work:
            nombreCorreo = u"outlook.exe"
            s3d_do_work = False # BREAK
        if nombreCorreo != u"":
            self.child(u"lblNombreCorreo").text = nombreCorreo
            util.writeSettingEntry(u"scripts/flfactinfo/nombrecorreo", nombreCorreo)
    
    def envioMail_cambiarNombreCorreo(self):
        util = qsatype.FLUtil()
        nombreCorreo = Input.getText(util.translate(u"scripts", u"Ejecutable para correo:"))
        if not nombreCorreo:
            return 
        self.child(u"lblNombreCorreo").text = nombreCorreo
        util.writeSettingEntry(u"scripts/flfactinfo/nombrecorreo", nombreCorreo)
    
    def envioMail_cambiarDirIntermedia(self):
        util = qsatype.FLUtil()
        ruta = FileDialog.getExistingDirectory(util.translate(u"scripts", u""), util.translate(u"scripts", u"RUTA INTERMEDIA"))
        if not qsatype.File.isDir(ruta):
            MessageBox.information(util.translate(u"scripts", u"Ruta errÃ³nea"), MessageBox.Ok, MessageBox.NoButton)
            return 
        self.child(u"lblDirIntermedia").text = ruta
        util.writeSettingEntry(u"scripts/flfactinfo/dirCorreo", ruta)
    


form = None
