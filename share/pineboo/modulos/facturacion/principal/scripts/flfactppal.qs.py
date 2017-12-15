# -*- coding: utf-8 -*-
from pineboolib import qsatype
from pineboolib.qsaglobals import *
import traceback
sys = SysType()

class interna(object):
    ctx = qsatype.Object()
    def __init__(self, context = None):
        self.ctx = context
    
    def init(self):
        self.ctx.interna_init()
    
    def afterCommit_dirclientes(self, curDirCli = None):
        return self.ctx.interna_afterCommit_dirclientes(curDirCli)
    
    def afterCommit_dirproveedores(self, curDirProv = None):
        return self.ctx.interna_afterCommit_dirproveedores(curDirProv)
    
    def afterCommit_clientes(self, curCliente = None):
        return self.ctx.interna_afterCommit_clientes(curCliente)
    
    def beforeCommit_clientes(self, curCliente = None):
        return self.ctx.interna_beforeCommit_clientes(curCliente)
    
    def afterCommit_proveedores(self, curProveedor = None):
        return self.ctx.interna_afterCommit_proveedores(curProveedor)
    
    def beforeCommit_proveedores(self, curProveedor = None):
        return self.ctx.interna_beforeCommit_proveedores(curProveedor)
    
    def afterCommit_empresa(self, curEmpresa = None):
        return self.ctx.interna_afterCommit_empresa(curEmpresa)
    
    def beforeCommit_cuentasbcocli(self, curCuenta = None):
        return self.ctx.interna_beforeCommit_cuentasbcocli(curCuenta)
    

class oficial(interna):
    def __init__(self, context = None):
        super(oficial, self).__init__(context)
    
    def msgNoDisponible(self, nombreModulo = None):
        return self.ctx.oficial_msgNoDisponible(nombreModulo)
    
    def ejecutarQry(self, tabla = None, campos = None, where = None, listaTablas = None):
        return self.ctx.oficial_ejecutarQry(tabla, campos, where, listaTablas)
    
    def valorDefectoEmpresa(self, fN = None):
        return self.ctx.oficial_valorDefectoEmpresa(fN)
    
    def cerosIzquierda(self, numero = None, totalCifras = None):
        return self.ctx.oficial_cerosIzquierda(numero, totalCifras)
    
    def espaciosDerecha(self, texto = None, totalLongitud = None):
        return self.ctx.oficial_espaciosDerecha(texto, totalLongitud)
    
    def valoresIniciales(self):
        return self.ctx.oficial_valoresIniciales()
    
    def valorQuery(self, tablas = None, select = None, from_ = None, where = None):
        return self.ctx.oficial_valorQuery(tablas, select, from_, where)
    
    def crearSubcuenta(self, codSubcuenta = None, descripcion = None, idCuentaEsp = None, codEjercicio = None):
        return self.ctx.oficial_crearSubcuenta(codSubcuenta, descripcion, idCuentaEsp, codEjercicio)
    
    def borrarSubcuenta(self, idSubcuenta = None):
        return self.ctx.oficial_borrarSubcuenta(idSubcuenta)
    
    def ejercicioActual(self):
        return self.ctx.oficial_ejercicioActual()
    
    def cambiarEjercicioActual(self, codEjercicio = None):
        return self.ctx.oficial_cambiarEjercicioActual(codEjercicio)
    
    def datosCtaCliente(self, codCliente = None, valoresDefecto = None):
        return self.ctx.oficial_datosCtaCliente(codCliente, valoresDefecto)
    
    def datosCtaProveedor(self, codProveedor = None, valoresDefecto = None):
        return self.ctx.oficial_datosCtaProveedor(codProveedor, valoresDefecto)
    
    def calcularIntervalo(self, codIntervalo = None):
        return self.ctx.oficial_calcularIntervalo(codIntervalo)
    
    def crearSubcuentaCli(self, codSubcuenta = None, idSubcuenta = None, codCliente = None, codEjercicio = None):
        return self.ctx.oficial_crearSubcuentaCli(codSubcuenta, idSubcuenta, codCliente, codEjercicio)
    
    def rellenarSubcuentasCli(self, codCliente = None, codSubcuenta = None, nombre = None):
        return self.ctx.oficial_rellenarSubcuentasCli(codCliente, codSubcuenta, nombre)
    
    def crearSubcuentaProv(self, codSubcuenta = None, idSubcuenta = None, codProveedor = None, codEjercicio = None):
        return self.ctx.oficial_crearSubcuentaProv(codSubcuenta, idSubcuenta, codProveedor, codEjercicio)
    
    def rellenarSubcuentasProv(self, codProveedor = None, codSubcuenta = None, nombre = None):
        return self.ctx.oficial_rellenarSubcuentasProv(codProveedor, codSubcuenta, nombre)
    
    def automataActivado(self):
        return self.ctx.oficial_automataActivado()
    
    def clienteActivo(self, codCliente = None, fecha = None):
        return self.ctx.oficial_clienteActivo(codCliente, fecha)
    
    def obtenerProvincia(self, formulario = None, campoId = None, campoProvincia = None, campoPais = None):
        return self.ctx.oficial_obtenerProvincia(formulario, campoId, campoProvincia, campoPais)
    
    def actualizarContactos20070525(self):
        return self.ctx.oficial_actualizarContactos20070525()
    
    def lanzarEvento(self, cursor = None, evento = None):
        return self.ctx.oficial_lanzarEvento(cursor, evento)
    
    def actualizarContactosDeAgenda20070525(self, codCliente = None, codContacto = None, nombreCon = None, cargoCon = None, telefonoCon = None, faxCon = None, emailCon = None, idAgenda = None):
        return self.ctx.oficial_actualizarContactosDeAgenda20070525(codCliente, codContacto, nombreCon, cargoCon, telefonoCon, faxCon, emailCon, idAgenda)
    
    def actualizarContactosProv20070702(self):
        return self.ctx.oficial_actualizarContactosProv20070702()
    
    def actualizarContactosDeAgendaProv20070702(self, codProveedor = None, codContacto = None, nombreCon = None, cargoCon = None, telefonoCon = None, faxCon = None, emailCon = None, idAgenda = None):
        return self.ctx.oficial_actualizarContactosDeAgendaProv20070702(codProveedor, codContacto, nombreCon, cargoCon, telefonoCon, faxCon, emailCon, idAgenda)
    
    def elegirOpcion(self, opciones = None, titulo = None):
        return self.ctx.oficial_elegirOpcion(opciones, titulo)
    
    def crearProvinciasEsp(self, codPais = None):
        return self.ctx.oficial_crearProvinciasEsp(codPais)
    
    def textoFecha(self, fecha = None):
        return self.ctx.oficial_textoFecha(fecha)
    
    def validarNifIva(self, nifIva = None):
        return self.ctx.oficial_validarNifIva(nifIva)
    
    def ejecutarComandoAsincrono(self, comando = None):
        return self.ctx.oficial_ejecutarComandoAsincrono(comando)
    
    def globalInit(self):
        return self.ctx.oficial_globalInit()
    
    def existeEnvioMail(self):
        return self.ctx.oficial_existeEnvioMail()
    
    def validarProvincia(self, cursor = None, mtd = None):
        return self.ctx.oficial_validarProvincia(cursor, mtd)
    
    def simplify(self, str = None):
        return self.ctx.oficial_simplify(str)
    
    def escapeQuote(self, str = None):
        return self.ctx.oficial_escapeQuote(str)
    
    def calcularIBAN(self, cuenta = None, codPais = None):
        return self.ctx.oficial_calcularIBAN(cuenta, codPais)
    
    def digitoControlMod97(self, numero = None, codPais = None):
        return self.ctx.oficial_digitoControlMod97(numero, codPais)
    
    def moduloNumero(self, num = None, div = None):
        return self.ctx.oficial_moduloNumero(num, div)
    
    def calcularIdentificadorAcreedor(self, cifEmpresa = None, codCuenta = None):
        return self.ctx.oficial_calcularIdentificadorAcreedor(cifEmpresa, codCuenta)
    

class envioMail(oficial):
    def __init__(self, context = None):
        super(envioMail, self).__init__(context)
    
    def enviarCorreo(self, cuerpo = None, asunto = None, arrayDest = None, arrayAttach = None):
        return self.ctx.envioMail_enviarCorreo(cuerpo, asunto, arrayDest, arrayAttach)
    
    def componerCorreo(self, cuerpo = None, asunto = None, arrayDest = None, arrayAttach = None):
        return self.ctx.envioMail_componerCorreo(cuerpo, asunto, arrayDest, arrayAttach)
    
    def componerListaDestinatarios(self, codigo = None, tabla = None):
        return self.ctx.envioMail_componerListaDestinatarios(codigo, tabla)
    
    def existeEnvioMail(self):
        return self.ctx.envioMail_existeEnvioMail()
    

class dtoEsp(envioMail):
    def __init__(self, context = None):
        super(dtoEsp, self).__init__(context)
    
    def calcularLiquidacionAgente(self, codLiquidacion = None):
        return self.ctx.dtoEsp_calcularLiquidacionAgente(codLiquidacion)
    

class pubEnvioMail(dtoEsp):
    def __init__(self, context = None):
        super(pubEnvioMail, self).__init__(context)
    
    def pub_enviarCorreo(self, cuerpo = None, asunto = None, arrayDest = None, arrayAttach = None):
        return self.enviarCorreo(cuerpo, asunto, arrayDest, arrayAttach)
    
    def pub_componerListaDestinatarios(self, codigo = None, tabla = None):
        return self.componerListaDestinatarios(codigo, tabla)
    
    def pub_existeEnvioMail(self):
        return self.existeEnvioMail()
    

class head(pubEnvioMail):
    def __init__(self, context = None):
        super(head, self).__init__(context)
    

class ifaceCtx(head):
    def __init__(self, context = None):
        super(ifaceCtx, self).__init__(context)
    
    def pub_msgNoDisponible(self, modulo = None):
        return self.msgNoDisponible(modulo)
    
    def pub_ejecutarQry(self, tabla = None, campos = None, where = None, listaTablas = None):
        return self.ejecutarQry(tabla, campos, where, listaTablas)
    
    def pub_valorDefectoEmpresa(self, fN = None):
        return self.valorDefectoEmpresa(fN)
    
    def pub_valorQuery(self, tablas = None, select = None, from_ = None, where = None):
        return self.valorQuery(tablas, select, from_, where)
    
    def pub_cerosIzquierda(self, numero = None, totalCifras = None):
        return self.cerosIzquierda(numero, totalCifras)
    
    def pub_espaciosDerecha(self, texto = None, totalLongitud = None):
        return self.espaciosDerecha(texto, totalLongitud)
    
    def pub_ejercicioActual(self):
        return self.ejercicioActual()
    
    def pub_cambiarEjercicioActual(self, codEjercicio = None):
        return self.cambiarEjercicioActual(codEjercicio)
    
    def pub_datosCtaCliente(self, codCliente = None, valoresDefecto = None):
        return self.datosCtaCliente(codCliente, valoresDefecto)
    
    def pub_datosCtaProveedor(self, codProveedor = None, valoresDefecto = None):
        return self.datosCtaProveedor(codProveedor, valoresDefecto)
    
    def pub_calcularIntervalo(self, codIntervalo = None):
        return self.calcularIntervalo(codIntervalo)
    
    def pub_crearSubcuenta(self, codSubcuenta = None, descripcion = None, idCuentaEsp = None, codEjercicio = None):
        return self.crearSubcuenta(codSubcuenta, descripcion, idCuentaEsp, codEjercicio)
    
    def pub_crearSubcuentaCli(self, codSubcuenta = None, idSubcuenta = None, codCliente = None, codEjercicio = None):
        return self.crearSubcuentaCli(codSubcuenta, idSubcuenta, codCliente, codEjercicio)
    
    def pub_crearSubcuentaProv(self, codSubcuenta = None, idSubcuenta = None, codProveedor = None, codEjercicio = None):
        return self.crearSubcuentaProv(codSubcuenta, idSubcuenta, codProveedor, codEjercicio)
    
    def pub_rellenarSubcuentasCli(self, codCliente = None, codSubcuenta = None, nombre = None):
        return self.rellenarSubcuentasCli(codCliente, codSubcuenta, nombre)
    
    def pub_rellenarSubcuentasProv(self, codProveedor = None, codSubcuenta = None, nombre = None):
        return self.rellenarSubcuentasProv(codProveedor, codSubcuenta, nombre)
    
    def pub_automataActivado(self):
        return self.automataActivado()
    
    def pub_clienteActivo(self, codCliente = None, fecha = None):
        return self.clienteActivo(codCliente, fecha)
    
    def pub_obtenerProvincia(self, formulario = None, campoId = None, campoProvincia = None, campoPais = None):
        return self.obtenerProvincia(formulario, campoId, campoProvincia, campoPais)
    
    def pub_lanzarEvento(self, cursor = None, evento = None):
        return self.lanzarEvento(cursor, evento)
    
    def pub_elegirOpcion(self, opciones = None, titulo = None):
        return self.elegirOpcion(opciones, titulo)
    
    def pub_textoFecha(self, fecha = None):
        return self.textoFecha(fecha)
    
    def pub_validarNifIva(self, nifIva = None):
        return self.validarNifIva(nifIva)
    
    def pub_ejecutarComandoAsincrono(self, comando = None):
        return self.ejecutarComandoAsincrono(comando)
    
    def pub_globalInit(self):
        return self.globalInit()
    
    def pub_existeEnvioMail(self):
        return self.existeEnvioMail()
    
    def pub_crearProvinciasEsp(self, codPais = None):
        return self.crearProvinciasEsp(codPais)
    
    def pub_validarProvincia(self, cursor = None, mtd = None):
        return self.validarProvincia(cursor, mtd)
    
    def pub_simplify(self, str = None):
        return self.simplify(str)
    
    def pub_escapeQuote(self, str = None):
        return self.escapeQuote(str)
    
    def pub_calcularIBAN(self, cuenta = None, codPais = None):
        return self.calcularIBAN(cuenta, codPais)
    
    def pub_digitoControlMod97(self, numero = None, codPais = None):
        return self.digitoControlMod97(numero, codPais)
    
    def pub_moduloNumero(self, num = None, div = None):
        return self.moduloNumero(num, div)
    

class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)
    
    def interna_init(self):
        util = qsatype.FLUtil()
        condicion = util.sqlSelect(u"clientes", u"codcliente", u"(codcontacto = '' OR codcontacto IS NULL) AND (contacto <> '' AND contacto IS NOT NULL)")
        condicionProv = util.sqlSelect(u"proveedores", u"codproveedor", u"(codcontacto = '' OR codcontacto IS NULL) AND (contacto <> '' AND contacto IS NOT NULL)")
        if condicion:
            cursor = qsatype.FLSqlCursor(u"clientes")
            cursor.transaction(False)
            try:
                if self.iface.actualizarContactos20070525():
                    cursor.commit()
                else:
                    cursor.rollback()
                
            
            except Exception as e:
                e = traceback.format_exc()
                cursor.rollback()
                MessageBox.warning(util.translate(u"scripts", ustr( u"Hubo un error al actualizar los datos de contactos del módulo de Facturación:\n" , e )), MessageBox.Ok, MessageBox.NoButton)
            
        
        if condicionProv:
            cursor = qsatype.FLSqlCursor(u"proveedores")
            cursor.transaction(False)
            try:
                if self.iface.actualizarContactosProv20070702():
                    cursor.commit()
                else:
                    cursor.rollback()
                
            
            except Exception as e:
                e = traceback.format_exc()
                cursor.rollback()
                MessageBox.warning(util.translate(u"scripts", ustr( u"Hubo un error al actualizar los datos de contactos del módulo de Facturación:\n" , e )), MessageBox.Ok, MessageBox.NoButton)
            
        
        if util.sqlSelect(u"empresa", u"id", u"1 = 1"):
            return 
        cursor = qsatype.FLSqlCursor(u"empresa")
        cursor.select()
        if not cursor.first():
            MessageBox.information(util.translate(u"scripts", u"Se insertará una empresa por defecto y algunos valores iniciales para empezar a trabajar."), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton)
            self.iface.valoresIniciales()
            self.execMainScript(u"empresa")
    
    def interna_afterCommit_dirclientes(self, curDirCli = None):
        if curDirCli.modeAccess() == curDirCli.Del:
            domFact = curDirCli.valueBuffer(u"domfacturacion")
            domEnv = curDirCli.valueBuffer(u"domenvio")
            if domFact == True or domEnv == True:
                cursor = qsatype.FLSqlCursor(u"dirclientes")
                cursor.select(ustr( u"codcliente = '" , curDirCli.valueBuffer(u"codcliente") , u"' AND id <> " , curDirCli.valueBuffer(u"id") ))
                if cursor.first():
                    cursor.setModeAccess(cursor.Edit)
                    cursor.refreshBuffer()
                    if domFact == True:
                        cursor.setValueBuffer(u"domfacturacion", domFact)
                    if domEnv == True:
                        cursor.setValueBuffer(u"domenvio", domEnv)
                    cursor.commitBuffer()
        
        return True
    
    def interna_afterCommit_dirproveedores(self, curDirProv = None):
        if curDirProv.modeAccess() == curDirProv.Del:
            dirPpal = curDirProv.valueBuffer(u"direccionppal")
            if dirPpal == True:
                cursor = qsatype.FLSqlCursor(u"dirproveedores")
                cursor.select(ustr( u"codproveedor = '" , curDirProv.valueBuffer(u"codproveedor") , u"' AND id <> " , curDirProv.valueBuffer(u"id") ))
                if cursor.first():
                    cursor.setModeAccess(cursor.Edit)
                    cursor.refreshBuffer()
                    cursor.setValueBuffer(u"direccionppal", dirPpal)
                    cursor.commitBuffer()
        
        return True
    
    def interna_afterCommit_clientes(self, curCliente = None):
        util = qsatype.FLUtil()
        if not sys.isLoadedModule(u"flcontppal"):
            return True
        codSubcuenta = curCliente.valueBuffer(u"codsubcuenta")
        idSubcuenta = parseFloat(curCliente.valueBuffer(u"idsubcuenta"))
        codCliente = curCliente.valueBuffer(u"codcliente")
        idSubcuentaPrevia = parseFloat(curCliente.valueBufferCopy(u"idsubcuenta"))
        s21_when = curCliente.modeAccess()
        s21_do_work,s21_work_done = False,False
        if s21_when == curCliente.Insert: s21_do_work,s21_work_done = True,True
        if s21_do_work:
            if not self.iface.rellenarSubcuentasCli(codCliente, codSubcuenta, curCliente.valueBuffer(u"nombre")):
                return False
            s21_do_work = False # BREAK
        return True
    
    def interna_afterCommit_proveedores(self, curProveedor = None):
        util = qsatype.FLUtil()
        if not sys.isLoadedModule(u"flcontppal"):
            return True
        codSubcuenta = curProveedor.valueBuffer(u"codsubcuenta")
        idSubcuenta = parseFloat(curProveedor.valueBuffer(u"idsubcuenta"))
        codProveedor = curProveedor.valueBuffer(u"codproveedor")
        idSubcuentaPrevia = parseFloat(curProveedor.valueBufferCopy(u"idsubcuenta"))
        s9f_when = curProveedor.modeAccess()
        s9f_do_work,s9f_work_done = False,False
        if s9f_when == curProveedor.Insert: s9f_do_work,s9f_work_done = True,True
        if s9f_do_work:
            if not self.iface.rellenarSubcuentasProv(codProveedor, codSubcuenta, curProveedor.valueBuffer(u"nombre")):
                return False
            s9f_do_work = False # BREAK
        return True
    
    def interna_beforeCommit_proveedores(self, curProveedor = None):
        util = qsatype.FLUtil()
        if not sys.isLoadedModule(u"flcontppal"):
            return True
        s77_when = curProveedor.modeAccess()
        s77_do_work,s77_work_done = False,False
        if s77_when == curProveedor.Del: s77_do_work,s77_work_done = True,True
        if s77_do_work:
            qrySubcuentas = qsatype.FLSqlQuery()
            qrySubcuentas.setTablesList(u"co_subcuentasprov,co_subcuentas")
            qrySubcuentas.setSelect(u"s.codsubcuenta,s.descripcion,s.codejercicio,s.saldo,s.idsubcuenta")
            qrySubcuentas.setFrom(u"co_subcuentasprov sp INNER JOIN co_subcuentas s ON sp.idsubcuenta = s.idsubcuenta")
            qrySubcuentas.setWhere(ustr( u"sp.codproveedor = '" , curProveedor.valueBuffer(u"codproveedor") , u"'" ))
            try:
                qrySubcuentas.setForwardOnly(True)
            except Exception as e:
                e = traceback.format_exc()
            
            if not qrySubcuentas.exec_():
                return False
            idSubcuenta = ""
            while qrySubcuentas.next():
                idSubcuenta = qrySubcuentas.value(u"s.idsubcuenta")
                if parseFloat(qrySubcuentas.value(u"s.saldo")) != 0:
                    continue 
                if util.sqlSelect(u"co_partidas", u"idpartida", ustr( u"idsubcuenta = " , idSubcuenta )):
                    continue 
                if util.sqlSelect(u"co_subcuentasprov", u"idsubcuenta", ustr( u"idsubcuenta = " , idSubcuenta , u" AND codproveedor <> '" , curProveedor.valueBuffer(u"codproveedor") , u"'" )):
                    continue 
                if not util.sqlDelete(u"co_subcuentas", ustr( u"idsubcuenta = " , idSubcuenta )):
                    return False
        
        return True
    
    def interna_beforeCommit_clientes(self, curCliente = None):
        util = qsatype.FLUtil()
        if not sys.isLoadedModule(u"flcontppal"):
            return True
        se8_when = curCliente.modeAccess()
        se8_do_work,se8_work_done = False,False
        if se8_when == curCliente.Del: se8_do_work,se8_work_done = True,True
        if se8_do_work:
            qrySubcuentas = qsatype.FLSqlQuery()
            qrySubcuentas.setTablesList(u"co_subcuentascli,co_subcuentas")
            qrySubcuentas.setSelect(u"s.codsubcuenta,s.descripcion,s.codejercicio,s.saldo,s.idsubcuenta")
            qrySubcuentas.setFrom(u"co_subcuentascli sc INNER JOIN co_subcuentas s ON sc.idsubcuenta = s.idsubcuenta")
            qrySubcuentas.setWhere(ustr( u"sc.codcliente = '" , curCliente.valueBuffer(u"codcliente") , u"'" ))
            try:
                qrySubcuentas.setForwardOnly(True)
            except Exception as e:
                e = traceback.format_exc()
            
            if not qrySubcuentas.exec_():
                return False
            idSubcuenta = ""
            while qrySubcuentas.next():
                idSubcuenta = qrySubcuentas.value(u"s.idsubcuenta")
                if parseFloat(qrySubcuentas.value(u"s.saldo")) != 0:
                    continue 
                if util.sqlSelect(u"co_partidas", u"idpartida", ustr( u"idsubcuenta = " , idSubcuenta )):
                    continue 
                if util.sqlSelect(u"co_subcuentascli", u"idsubcuenta", ustr( u"idsubcuenta = " , idSubcuenta , u" AND codcliente <> '" , curCliente.valueBuffer(u"codcliente") , u"'" )):
                    continue 
                if not util.sqlDelete(u"co_subcuentas", ustr( u"idsubcuenta = " , idSubcuenta )):
                    return False
        
        return True
    
    def interna_afterCommit_empresa(self, curEmpresa = None):
        pass
    
    def interna_beforeCommit_cuentasbcocli(self, curCuenta = None):
        sbb_when = curCuenta.modeAccess()
        sbb_do_work,sbb_work_done = False,False
        if sbb_when == curCuenta.Del: sbb_do_work,sbb_work_done = True,True
        if sbb_do_work:
            util = qsatype.FLUtil()
            codRecibo = util.sqlSelect(u"reciboscli", u"codigo", ustr( u"codcliente = '" , curCuenta.valueBuffer(u"codcliente") , u"' AND codcuenta = '" , curCuenta.valueBuffer(u"codcuenta") , u"' AND estado <> 'Pagado'" ))
            if codRecibo and codRecibo != u"":
                MessageBox.warning(util.translate(u"scripts", u"No puede eliminar la cuenta del cliente porque hay al menos un recibo (%1) pendiente de pago asociado a esta cuenta.\nDebe cambiar la cuenta de los recibos pendientes de este cliente antes de borrarla.").arg(codRecibo), MessageBox.Ok, MessageBox.NoButton)
                return False
            sbb_do_work = False # BREAK
        
        return True
    
    def oficial_msgNoDisponible(self, nombreModulo = None):
        util = qsatype.FLUtil()
        MessageBox.information(util.translate(u"scripts", u"El módulo '") + nombreModulo + util.translate(u"scripts", u"' no está disponible."), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton)
    
    def oficial_ejecutarQry(self, tabla = None, campos = None, where = None, listaTablas = None):
        util = qsatype.FLUtil()
        campo = campos.split(u",")
        valor = qsatype.Array()
        valor[u"result"] = 1
        query = qsatype.FLSqlQuery()
        if listaTablas:
            query.setTablesList(listaTablas)
        else:
            query.setTablesList(tabla)
        
        try:
            query.setForwardOnly(True)
        except Exception as e:
            e = traceback.format_exc()
        
        query.setSelect(campo)
        query.setFrom(tabla)
        query.setWhere(where)
        if query.exec_():
            if query.next():
                i = 0
                while_pass = True
                while i < len(campo):
                    if not while_pass:
                        i += 1
                        while_pass = True
                        continue
                    while_pass = False
                    valor[campo[i]] = query.value(i)
                    i += 1
                    while_pass = True
                    try:
                        i < len(campo)
                    except: break
            
            else:
                valor.result = - 1
            
        
        else:
            MessageBox.critical(util.translate(u"scripts", u"Falló la consulta") + query.sql(), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton)
            valor.result = 0
        
        return valor
    
    def oficial_valorDefectoEmpresa(self, fN = None):
        query = qsatype.FLSqlQuery()
        query.setTablesList(u"empresa")
        try:
            query.setForwardOnly(True)
        except Exception as e:
            e = traceback.format_exc()
        
        query.setSelect(fN)
        query.setFrom(u"empresa")
        if query.exec_():
            if query.next():
                return query.value(0)
        return u""
    
    def oficial_ejercicioActual(self):
        util = qsatype.FLUtil()
        codEjercicio = ""
        try:
            settingKey = ustr( u"ejerUsr_" , sys.nameUser() )
            codEjercicio = util.readDBSettingEntry(settingKey)
        except Exception as e:
            e = traceback.format_exc()
        
        if not codEjercicio:
            codEjercicio = self.iface.valorDefectoEmpresa(u"codejercicio")
        return codEjercicio
    
    def oficial_cambiarEjercicioActual(self, codEjercicio = None):
        util = qsatype.FLUtil()
        ok = False
        try:
            settingKey = ustr( u"ejerUsr_" , sys.nameUser() )
            ok = util.writeDBSettingEntry(settingKey, codEjercicio)
        except Exception as e:
            e = traceback.format_exc()
        
        return ok
    
    def oficial_cerosIzquierda(self, numero = None, totalCifras = None):
        ret = parseString(numero)
        numCeros = totalCifras - len(ret)
        while_pass = True
        while numCeros > 0:
            if not while_pass:
                numCeros -= 1
                while_pass = True
                continue
            while_pass = False
            ret = ustr( u"0" , ret )
            numCeros -= 1
            while_pass = True
            try:
                numCeros > 0
            except: break
        
        return ret
    
    def oficial_espaciosDerecha(self, texto = None, totalLongitud = None):
        ret = parseString(texto)
        numEspacios = totalLongitud - len(ret)
        while_pass = True
        while numEspacios > 0:
            if not while_pass:
                numEspacios -= 1
                while_pass = True
                continue
            while_pass = False
            ret += u" "
            numEspacios -= 1
            while_pass = True
            try:
                numEspacios > 0
            except: break
        
        return ret
    
    def oficial_valoresIniciales(self):
        cursor = qsatype.FLSqlCursor(u"bancos")
        bancos = qsatype.Array([qsatype.Array([u"0030", u"BANESTO"]), qsatype.Array([u"0112", u"BANCO URQUIJO"]), qsatype.Array([u"2085", u"IBERCAJA"]), qsatype.Array([u"0093", u"BANCO DE VALENCIA"]), qsatype.Array([u"2059", u"CAIXA SABADELL"]), qsatype.Array([u"2073", u"CAIXA TARRAGONA"]), qsatype.Array([u"2038", u"CAJA MADRID"]), qsatype.Array([u"2091", u"CAIXA GALICIA"]), qsatype.Array([u"0019", u"DEUTSCHE BANK"]), qsatype.Array([u"0081", u"BANCO DE SABADELL"]), qsatype.Array([u"0049", u"BANCO SANTANDER CENTRAL HISPANO"]), qsatype.Array([u"0072", u"BANCO PASTOR"]), qsatype.Array([u"0075", u"BANCO POPULAR"]), qsatype.Array([u"0182", u"BANCO BILBAO VIZCAYA ARGENTARIA"]), qsatype.Array([u"0128", u"BANKINTER"]), qsatype.Array([u"2090", u"C.A.M."]), qsatype.Array([u"2100", u"LA CAIXA"]), qsatype.Array([u"2077", u"BANCAJA"]), qsatype.Array([u"0008", u"BANCO ATLANTICO"]), qsatype.Array([u"0061", u"BANCA MARCH"]), qsatype.Array([u"0065", u"BARCLAYS BANK"]), qsatype.Array([u"0073", u"PATAGON INTERNET BANK"]), qsatype.Array([u"0103", u"BANCO ZARAGOZANO"]), qsatype.Array([u"2013", u"CAIXA CATALUNYA"]), qsatype.Array([u"2043", u"CAJA MURCIA"]), qsatype.Array([u"2103", u"UNICAJA"]), qsatype.Array([u"2105", u"CAJA DE CASTILLA LA MANCHA"]), qsatype.Array([u"0042", u"BANCO GUIPUZCOANO"]), qsatype.Array([u"0138", u"BANKOA"]), qsatype.Array([u"3056", u"CAJA RURAL DE ALBACETE"])])
        i = 0
        while_pass = True
        while i < len(bancos):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
             #WITH_START
            cursor.setModeAccess(cursor.Insert)
            cursor.refreshBuffer()
            cursor.setValueBuffer(u"entidad", bancos[i][0])
            cursor.setValueBuffer(u"nombre", bancos[i][1])
            cursor.commitBuffer()
             #WITH_END
            i += 1
            while_pass = True
            try:
                i < len(bancos)
            except: break
        # EXPR??:: del
        # EXPR??:: cursor
        
        cursor = qsatype.FLSqlCursor(u"impuestos")
         #WITH_START
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"codimpuesto", u"GEN")
        cursor.setValueBuffer(u"descripcion", u"I.V.A. General")
        cursor.setValueBuffer(u"iva", u"21")
        cursor.setValueBuffer(u"recargo", u"5.2")
        cursor.commitBuffer()
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"codimpuesto", u"RED")
        cursor.setValueBuffer(u"descripcion", u"I.V.A. Reducido")
        cursor.setValueBuffer(u"iva", u"10")
        cursor.setValueBuffer(u"recargo", u"1.4")
        cursor.commitBuffer()
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"codimpuesto", u"SRED")
        cursor.setValueBuffer(u"descripcion", u"I.V.A. Superreducido")
        cursor.setValueBuffer(u"iva", u"4")
        cursor.setValueBuffer(u"recargo", u"0.5")
        cursor.commitBuffer()
         #WITH_END
        # EXPR??:: del
        # EXPR??:: cursor
        cursor = qsatype.FLSqlCursor(u"paises")
         #WITH_START
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"codpais", u"ES")
        cursor.setValueBuffer(u"nombre", u"ESPAÑA")
        cursor.setValueBuffer(u"bandera", u"/* XPM */\nstatic char * esp_xpm[] = {\n\"30 16 16 1\",\n\"  c #6C1E04\",\n\".	c #B78B19\",\n\"+	c #E4D31A\",\n\"@	c #8E4F09\",\n\"#	c #FBFC05\",\n\"$	c #EF0406\",\n\"%	c #F9978D\",\n\"&	c #FCFA36\",\n\"*	c #FC595C\",\n\"=	c #E1B025\",\n\"-	c #FB3634\",\n\";	c #E67559\",\n\">	c #A26E13\",\n\",	c #FCACAC\",\n\"'	c #B29F19\",\n\")	c #9D0204\",\n\",,%%%%%%%%%%%%%%%%%%%%%%%%%%;$\",\n\";;**************************$)\",\n\"--$$$$$$$$$$$$$$$$$$$$$$$$$$$)\",\n\"--$$$$$$$$$$$$$$$$$$$$$$$$$$$)\",\n\"&&####&#&++&################+'\",\"&&####&=.>..&###############+'\",\n\"&&####@=@@@=>=##############+'\",\n\"&&####='>;>%=+&#############+'\",\n\"&&####@@@ @>>.##############+'\",\n\"&&####.=>@;;#;##############+'\",\"&&+###>..>..>=##############+'\",\n\"&&####.+===+.+&#############+.\",\n\"--$$$$$$$$$$$$$$$$$$$$$$$$$$$)\",\n\"--$$$$$$$$$$$$$$$$$$$$$$$$$$$)\",\n\"$$$)$)$)$))$)$)$)$)$)$)$)$)$))\",\n\"))))))))))))))))))))))))))))))\"};\n")
        cursor.setValueBuffer(u"codiso", u"ES")
        cursor.commitBuffer()
         #WITH_END
        # EXPR??:: del
        # EXPR??:: cursor
        cursor = qsatype.FLSqlCursor(u"divisas")
         #WITH_START
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"coddivisa", u"EUR")
        cursor.setValueBuffer(u"descripcion", u"EUROS")
        cursor.setValueBuffer(u"tasaconv", u"1")
        cursor.setValueBuffer(u"codiso", u"978")
        cursor.commitBuffer()
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"coddivisa", u"USD")
        cursor.setValueBuffer(u"descripcion", u"DÓLARES USA")
        cursor.setValueBuffer(u"tasaconv", u"0.845")
        cursor.setValueBuffer(u"codiso", u"849")
        cursor.commitBuffer()
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"coddivisa", u"GBP")
        cursor.setValueBuffer(u"descripcion", u"LIBRAS ESTERLINAS")
        cursor.setValueBuffer(u"tasaconv", u"1.48")
        cursor.setValueBuffer(u"codiso", u"826")
        cursor.commitBuffer()
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"coddivisa", u"CHF")
        cursor.setValueBuffer(u"descripcion", u"FRANCOS SUIZOS")
        cursor.setValueBuffer(u"tasaconv", u"0.648")
        cursor.setValueBuffer(u"codiso", u"756")
        cursor.commitBuffer()
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"coddivisa", u"SEK")
        cursor.setValueBuffer(u"descripcion", u"CORONAS SUECAS")
        cursor.setValueBuffer(u"tasaconv", u"0.106")
        cursor.setValueBuffer(u"codiso", u"752")
        cursor.commitBuffer()
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"coddivisa", u"NOK")
        cursor.setValueBuffer(u"descripcion", u"CORONAS NORUEGAS")
        cursor.setValueBuffer(u"tasaconv", u"0.126")
        cursor.setValueBuffer(u"codiso", u"578")
        cursor.commitBuffer()
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"coddivisa", u"NZD")
        cursor.setValueBuffer(u"descripcion", u"DÓLARES NEOZELANDESES")
        cursor.setValueBuffer(u"tasaconv", u"0.608")
        cursor.setValueBuffer(u"codiso", u"554")
        cursor.commitBuffer()
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"coddivisa", u"JPY")
        cursor.setValueBuffer(u"descripcion", u"YENES JAPONESES")
        cursor.setValueBuffer(u"tasaconv", u"0.007")
        cursor.setValueBuffer(u"codiso", u"392")
        cursor.commitBuffer()
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"coddivisa", u"DKK")
        cursor.setValueBuffer(u"descripcion", u"CORONAS DANESAS")
        cursor.setValueBuffer(u"tasaconv", u"0.134")
        cursor.setValueBuffer(u"codiso", u"208")
        cursor.commitBuffer()
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"coddivisa", u"CAD")
        cursor.setValueBuffer(u"descripcion", u"DÓLARES CANADIENSES")
        cursor.setValueBuffer(u"tasaconv", u"0.735")
        cursor.setValueBuffer(u"codiso", u"124")
        cursor.commitBuffer()
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"coddivisa", u"AUD")
        cursor.setValueBuffer(u"descripcion", u"DÓLARES AUSTRALIANOS")
        cursor.setValueBuffer(u"tasaconv", u"0.639")
        cursor.setValueBuffer(u"codiso", u"036")
        cursor.commitBuffer()
         #WITH_END
        # EXPR??:: del
        # EXPR??:: cursor
        cursor = qsatype.FLSqlCursor(u"formaspago")
         #WITH_START
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"codpago", u"CONT")
        cursor.setValueBuffer(u"descripcion", u"CONTADO")
        cursor.commitBuffer()
         #WITH_END
        # EXPR??:: del
        # EXPR??:: cursor
        cursor = qsatype.FLSqlCursor(u"plazos")
         #WITH_START
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"codpago", u"CONT")
        cursor.setValueBuffer(u"dias", u"0")
        cursor.setValueBuffer(u"aplazado", u"100")
        cursor.commitBuffer()
         #WITH_END
        # EXPR??:: del
        # EXPR??:: cursor
        cursor = qsatype.FLSqlCursor(u"ejercicios")
        hoy = qsatype.Date()
        fechaInicio = qsatype.Date(hoy.getYear(), 1, 1)
        fechaFin = qsatype.Date(hoy.getYear(), 12, 31)
        codEjercicio = hoy.getYear()
         #WITH_START
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"codejercicio", codEjercicio)
        cursor.setValueBuffer(u"nombre", ustr( u"EJERCICIO " , codEjercicio ))
        cursor.setValueBuffer(u"fechainicio", fechaInicio)
        cursor.setValueBuffer(u"fechafin", fechaFin)
        cursor.setValueBuffer(u"estado", u"ABIERTO")
        cursor.commitBuffer()
         #WITH_END
        # EXPR??:: del
        # EXPR??:: cursor
        self.iface.cambiarEjercicioActual(codEjercicio)
        cursor = qsatype.FLSqlCursor(u"series")
         #WITH_START
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"codserie", u"A")
        cursor.setValueBuffer(u"descripcion", u"SERIE A")
        cursor.commitBuffer()
         #WITH_END
        # EXPR??:: del
        # EXPR??:: cursor
        cursor = qsatype.FLSqlCursor(u"secuenciasejercicios")
        idSec = 0
         #WITH_START
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"codserie", u"A")
        cursor.setValueBuffer(u"codejercicio", codEjercicio)
        idSec = valueBuffer(u"id")
        cursor.commitBuffer()
         #WITH_END
        # EXPR??:: del
        # EXPR??:: cursor
        cursor = qsatype.FLSqlCursor(u"secuencias")
         #WITH_START
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"id", idSec)
        cursor.setValueBuffer(u"nombre", u"nfacturacli")
        cursor.setValueBuffer(u"valor", 1)
        cursor.commitBuffer()
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"id", idSec)
        cursor.setValueBuffer(u"nombre", u"nfacturaprov")
        cursor.setValueBuffer(u"valor", 1)
        cursor.commitBuffer()
         #WITH_END
        # EXPR??:: del
        # EXPR??:: cursor
        cursor = qsatype.FLSqlCursor(u"empresa")
        cursor.setActivatedCheckIntegrity(False)
        milogo = u""
        milogo += u'/* XPM */\n'
        milogo += u'static char * logo_xpm[] = {\n'
        milogo += u'"50 16 7 1",\n'
        milogo += u'" 	c #1E00FF",\n'
        milogo += u'".	c #FF0000",\n'
        milogo += u'"+	c #FF00FF",\n'
        milogo += u'"@	c #18FF00",\n'
        milogo += u'"#	c #33FFFF",\n'
        milogo += u'"$	c #FFFF00",\n'
        milogo += u'"%	c #FFFFFF",\n'
        milogo += u'"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",\n'
        milogo += u'"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",\n'
        milogo += u'"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",\n'
        milogo += u'"%%$%%%%%%%%%%%%%%%%%%%%%%%%%% %%% %%%%%%%%%%%%%%%%",\n'
        milogo += u'"%%.%%%%%%%%%%%%%%%%%%%%%%%%%% %%%%%%%%%%%%%%%%%%%%",\n'
        milogo += u'"%%.%%%%%%@@@%%%@@@@@%%%   %%    % %%   ++%%%...%%%",\n'
        milogo += u'"%%.%%%%%$%%%@%%@%%%@%%#%%% %% %%% %% %%%+%%.%%%.%%",\n'
        milogo += u'"%%.%%%%%$%%%@%%@%%%@%%#%%% %% %%% %% %%% %%+%%%.%%",\n'
        milogo += u'"%%.%%%%%$%%%@%%@%%%@%%@%%%#%% %%% %% %%% %%+%%%.%%",\n'
        milogo += u'"%%.%%%%%.%%%$%%@%%%@%%@%%%#%%#%%% %% %%% %% %%%+%%",\n'
        milogo += u'"%%.....%%.$$%%%%@@@@%%%@@@%%%## % %%     %%%  +%%%",\n'
        milogo += u'"%%%%%%%%%%%%%%%%%%%@%%%%%%%%%%%%%%%% %%%%%%%%%%%%%",\n'
        milogo += u'"%%%%%%%%%%%%%%%$$$$%%%%%%%%%%%%%%%%% %%%%%%%%%%%%%",\n'
        milogo += u'"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",\n'
        milogo += u'"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",\n'
        milogo += u'"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"};\n'
         #WITH_START
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"nombre", u"Empresa por defecto")
        cursor.setValueBuffer(u"cifnif", u"Z99999999")
        cursor.setValueBuffer(u"administrador", u"ANONIMO")
        cursor.setValueBuffer(u"direccion", u"C/ CALLE 999")
        cursor.setValueBuffer(u"codejercicio", codEjercicio)
        cursor.setValueBuffer(u"coddivisa", u"EUR")
        cursor.setValueBuffer(u"codpago", u"CONT")
        cursor.setValueBuffer(u"codserie", u"A")
        cursor.setValueBuffer(u"codpostal", u"00000")
        cursor.setValueBuffer(u"ciudad", u"MADRID")
        cursor.setValueBuffer(u"provincia", u"MADRID")
        cursor.setValueBuffer(u"telefono", u"96 111 22 33")
        cursor.setValueBuffer(u"email", u"email@example.com")
        cursor.setValueBuffer(u"codpais", u"ES")
        cursor.setValueBuffer(u"logo", milogo)
        cursor.commitBuffer()
         #WITH_END
        self.iface.crearProvinciasEsp()
    
    def oficial_crearProvinciasEsp(self, codPais = None):
        util = qsatype.FLUtil()
        cursor = qsatype.FLSqlCursor(u"provincias")
        provincias = qsatype.Array([qsatype.Array([u"ALAVA", u"ES", u"01"]), qsatype.Array([u"ALBACETE", u"ES", u"02"]), qsatype.Array([u"ALICANTE", u"ES", u"03"]), qsatype.Array([u"ALMERIA", u"ES", u"04"]), qsatype.Array([u"ASTURIAS", u"ES", u"33"]), qsatype.Array([u"AVILA", u"ES", u"05"]), qsatype.Array([u"BADAJOZ", u"ES", u"06"]), qsatype.Array([u"BALEARES", u"ES", u"07"]), qsatype.Array([u"BARCELONA", u"ES", u"08"]), qsatype.Array([u"BURGOS", u"ES", u"09"]), qsatype.Array([u"CACERES", u"ES", u"10"]), qsatype.Array([u"CADIZ", u"ES", u"11"]), qsatype.Array([u"CANTABRIA", u"ES", u"39"]), qsatype.Array([u"CASTELLON", u"ES", u"12"]), qsatype.Array([u"CIUDAD REAL", u"ES", u"12"]), qsatype.Array([u"CIUDAD REAL", u"ES", u"13"]), qsatype.Array([u"CORDOBA", u"ES", u"14"]), qsatype.Array([u"LA CORUÑA", u"ES", u"15"]), qsatype.Array([u"CUENCA", u"ES", u"16"]), qsatype.Array([u"GERONA", u"ES", u"17"]), qsatype.Array([u"GRANADA", u"ES", u"18"]), qsatype.Array([u"GUADALAJARA", u"ES", u"19"]), qsatype.Array([u"GUIPUZCOA", u"ES", u"20"]), qsatype.Array([u"HUELVA", u"ES", u"21"]), qsatype.Array([u"HUESCA", u"ES", u"22"]), qsatype.Array([u"JAEN", u"ES", u"23"]), qsatype.Array([u"LEON", u"ES", u"24"]), qsatype.Array([u"LERIDA", u"ES", u"25"]), qsatype.Array([u"LUGO", u"ES", u"27"]), qsatype.Array([u"MADRID", u"ES", u"28"]), qsatype.Array([u"MALAGA", u"ES", u"29"]), qsatype.Array([u"MURCIA", u"ES", u"30"]), qsatype.Array([u"NAVARRA", u"ES", u"31"]), qsatype.Array([u"ORENSE", u"ES", u"32"]), qsatype.Array([u"PALENCIA", u"ES", u"34"]), qsatype.Array([u"LAS PALMAS", u"ES", u"35"]), qsatype.Array([u"PONTEVEDRA", u"ES", u"36"]), qsatype.Array([u"LA RIOJA", u"ES", u"26"]), qsatype.Array([u"SALAMANCA", u"ES", u"37"]), qsatype.Array([u"SEGOVIA", u"ES", u"40"]), qsatype.Array([u"SEVILLA", u"ES", u"41"]), qsatype.Array([u"SORIA", u"ES", u"42"]), qsatype.Array([u"TARRAGONA", u"ES", u"43"]), qsatype.Array([u"SANTA CRUZ DE TENERIFE", u"ES", u"38"]), qsatype.Array([u"TERUEL", u"ES", u"44"]), qsatype.Array([u"TOLEDO", u"ES", u"45"]), qsatype.Array([u"VALENCIA", u"ES", u"46"]), qsatype.Array([u"VALLADOLID", u"ES", u"47"]), qsatype.Array([u"VIZCAYA", u"ES", u"48"]), qsatype.Array([u"ZAMORA", u"ES", u"49"]), qsatype.Array([u"ZARAGOZA", u"ES", u"50"])])
        codPaisProvincia = ""
        i = 0
        while_pass = True
        while i < len(provincias):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            codPaisProvincia = ( ( codPais if codPais else provincias[i][1] ) )
            if util.sqlSelect(u"provincias", u"idprovincia", ustr( u"codpais = '" , codPaisProvincia , u"' AND (UPPER(provincia) = '" , provincias[i][0] , u"' OR codigo = '" , provincias[i][2] , u"')" )):
                continue 
             #WITH_START
            cursor.setModeAccess(cursor.Insert)
            cursor.refreshBuffer()
            cursor.setValueBuffer(u"provincia", provincias[i][0])
            cursor.setValueBuffer(u"codpais", codPaisProvincia)
            cursor.setValueBuffer(u"codigo", provincias[i][2])
            cursor.commitBuffer()
             #WITH_END
            i += 1
            while_pass = True
            try:
                i < len(provincias)
            except: break
    
    def oficial_valorQuery(self, tablas = None, select = None, from_ = None, where = None):
        qry = qsatype.FLSqlQuery()
        try:
            qry.setForwardOnly(True)
        except Exception as e:
            e = traceback.format_exc()
        
        qry.setTablesList(tablas)
        qry.setSelect(select)
        qry.setFrom(from_)
        qry.setWhere(where)
        qry.exec_()
        if qry.next():
            return qry.value(0)
        else:
            return u""
        
    
    def oficial_crearSubcuenta(self, codSubcuenta = None, descripcion = None, idCuentaEsp = None, codEjercicio = None):
        util = qsatype.FLUtil()
        datosEmpresa = qsatype.Array()
        if not codEjercicio:
            datosEmpresa[u"codejercicio"] = self.iface.ejercicioActual()
        else:
            datosEmpresa[u"codejercicio"] = codEjercicio
        
        datosEmpresa[u"coddivisa"] = self.iface.valorDefectoEmpresa(u"coddivisa")
        idSubcuenta = util.sqlSelect(u"co_subcuentas", u"idsubcuenta", ustr( u"codsubcuenta = '" , codSubcuenta , u"' AND codejercicio = '" , datosEmpresa.codejercicio , u"'" ))
        if idSubcuenta:
            return idSubcuenta
        codCuenta3 = codSubcuenta[0:3]
        codCuenta4 = codSubcuenta[0:4]
        datosCuenta = self.iface.ejecutarQry(u"co_cuentas", u"codcuenta,idcuenta", ustr( u"idcuentaesp = '" , idCuentaEsp , u"'" , u" AND codcuenta = '" , codCuenta4 , u"'" , u" AND codejercicio = '" , datosEmpresa.codejercicio , u"' ORDER BY codcuenta" ))
        if datosCuenta.result == - 1:
            datosCuenta = self.iface.ejecutarQry(u"co_cuentas", u"codcuenta,idcuenta", ustr( u"idcuentaesp = '" , idCuentaEsp , u"'" , u" AND codcuenta = '" , codCuenta3 , u"'" , u" AND codejercicio = '" , datosEmpresa.codejercicio , u"' ORDER BY codcuenta" ))
            if datosCuenta.result == - 1:
                return True
        curSubcuenta = qsatype.FLSqlCursor(u"co_subcuentas")
         #WITH_START
        curSubcuenta.setModeAccess(curSubcuenta.Insert)
        curSubcuenta.refreshBuffer()
        curSubcuenta.setValueBuffer(u"codsubcuenta", codSubcuenta)
        curSubcuenta.setValueBuffer(u"descripcion", descripcion)
        curSubcuenta.setValueBuffer(u"idcuenta", datosCuenta.idcuenta)
        curSubcuenta.setValueBuffer(u"codcuenta", datosCuenta.codcuenta)
        curSubcuenta.setValueBuffer(u"coddivisa", datosEmpresa.coddivisa)
        curSubcuenta.setValueBuffer(u"codejercicio", datosEmpresa.codejercicio)
         #WITH_END
        if not curSubcuenta.commitBuffer():
            return False
        return curSubcuenta.valueBuffer(u"idsubcuenta")
    
    def oficial_borrarSubcuenta(self, idSubcuenta = None):
        util = qsatype.FLUtil()
        if not util.sqlSelect(u"co_partidas", u"idpartida", ustr( u"idsubcuenta = " , idSubcuenta )):
            curSubcuenta = qsatype.FLSqlCursor(u"co_subcuentas")
            curSubcuenta.select(ustr( u"idsubcuenta = " , idSubcuenta ))
            curSubcuenta.first()
            curSubcuenta.setModeAccess(curSubcuenta.Del)
            curSubcuenta.refreshBuffer()
            if not curSubcuenta.commitBuffer():
                return False
        
        return True
    
    def oficial_datosCtaCliente(self, codCliente = None, valoresDefecto = None):
        if not codCliente or codCliente == u"":
            return flfacturac.iface.pub_datosCtaEspecial(u"CLIENT", valoresDefecto.codejercicio)
        util = qsatype.FLUtil()
        ctaCliente = qsatype.Array()
        ctaCliente[u"codsubcuenta"] = u""
        ctaCliente[u"idsubcuenta"] = u""
        if not parseString(codCliente) == None:
            qrySubcuenta = qsatype.FLSqlQuery()
            try:
                qrySubcuenta.setForwardOnly(True)
            except Exception as e:
                e = traceback.format_exc()
            
            qrySubcuenta.setTablesList(u"co_subcuentascli")
            qrySubcuenta.setSelect(u"idsubcuenta, codsubcuenta")
            qrySubcuenta.setFrom(u"co_subcuentascli")
            qrySubcuenta.setWhere(ustr( u"codcliente = '" , codCliente , u"' AND codejercicio = '" , valoresDefecto.codejercicio , u"'" ))
            if not qrySubcuenta.exec_():
                ctaCliente.error = 2
                return ctaCliente
            if not qrySubcuenta.first():
                MessageBox.critical(ustr( util.translate(u"scripts", u"No hay ninguna subcuenta asociada al cliente ") , codCliente , util.translate(u"scripts", u" para el ejercicio ") , valoresDefecto.codejercicio , u".\n" , util.translate(u"scripts", u"Debe crear la subcuenta en el formulario de clientes.") ), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton)
                ctaCliente.error = 1
                return ctaCliente
            ctaCliente.idsubcuenta = qrySubcuenta.value(0)
            ctaCliente.codsubcuenta = qrySubcuenta.value(1)
        
        ctaCliente.error = 0
        return ctaCliente
    
    def oficial_datosCtaProveedor(self, codProveedor = None, valoresDefecto = None):
        if not codProveedor or codProveedor == u"":
            return flfacturac.iface.pub_datosCtaEspecial(u"PROVEE", valoresDefecto.codejercicio)
        util = qsatype.FLUtil()
        ctaProveedor = qsatype.Array()
        ctaProveedor[u"codsubcuenta"] = u""
        ctaProveedor[u"idsubcuenta"] = u""
        if not parseString(codProveedor) == None:
            qrySubcuenta = qsatype.FLSqlQuery()
            qrySubcuenta.setTablesList(u"co_subcuentasprov")
            qrySubcuenta.setSelect(u"idsubcuenta, codsubcuenta")
            qrySubcuenta.setFrom(u"co_subcuentasprov")
            qrySubcuenta.setWhere(ustr( u"codproveedor = '" , codProveedor , u"' AND codejercicio = '" , valoresDefecto.codejercicio , u"'" ))
            if not qrySubcuenta.exec_():
                ctaProveedor.error = 1
                return ctaProveedor
            if not qrySubcuenta.first():
                MessageBox.critical(ustr( util.translate(u"scripts", u"No hay ninguna subcuenta asociada al proveedor ") , codProveedor , util.translate(u"scripts", u" para el ejercicio ") , valoresDefecto.codejercicio , u".\n" , util.translate(u"scripts", u"Debe crear la subcuenta en el formulario de proveedores.") ), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton)
                ctaProveedor.error = 1
                return ctaProveedor
            ctaProveedor.idsubcuenta = qrySubcuenta.value(0)
            ctaProveedor.codsubcuenta = qrySubcuenta.value(1)
        
        ctaProveedor.error = 0
        return ctaProveedor
    
    def oficial_calcularIntervalo(self, codIntervalo = None):
        util = qsatype.FLUtil()
        intervalo = qsatype.Array()
        textoFun = util.sqlSelect(u"intervalos", u"funcionintervalo", ustr( u"codigo = '" , codIntervalo , u"'" ))
        funcionVal = qsatype.Function(textoFun)
        resultado = funcionVal()
        if resultado:
            return resultado
        intervalo[u"desde"] = False
        intervalo[u"hasta"] = False
        fechaDesde = qsatype.Date()
        fechaHasta = qsatype.Date()
        mes = 0
        anio = 0
        s2a_when = codIntervalo
        s2a_do_work,s2a_work_done = False,False
        if s2a_when == u"000001": s2a_do_work,s2a_work_done = True,True
        if s2a_do_work:
            intervalo.desde = fechaDesde
            intervalo.hasta = fechaHasta
            s2a_do_work = False # BREAK
        if s2a_when == u"000002": s2a_do_work,s2a_work_done = True,True
        if s2a_do_work:
            intervalo.desde = util.addDays(fechaDesde, - 1)
            intervalo.hasta = util.addDays(fechaHasta, - 1)
            s2a_do_work = False # BREAK
        if s2a_when == u"000003": s2a_do_work,s2a_work_done = True,True
        if s2a_do_work:
            dias = fechaDesde.getDay() - 1
            dias = dias * - 1
            intervalo.desde = util.addDays(fechaDesde, dias)
            intervalo.hasta = util.addDays(intervalo.desde, 6)
            s2a_do_work = False # BREAK
        
        if s2a_when == u"000004": s2a_do_work,s2a_work_done = True,True
        if s2a_do_work:
            dias = fechaHasta.getDay() - 1
            dias = dias * - 1
            intervalo.hasta = util.addDays(fechaHasta, dias - 1)
            intervalo.desde = util.addDays(intervalo.hasta, - 6)
            s2a_do_work = False # BREAK
        
        if s2a_when == u"000005": s2a_do_work,s2a_work_done = True,True
        if s2a_do_work:
            mes = fechaDesde.getMonth()
            fechaDesde.setDate(1)
            intervalo.desde = fechaDesde
            fechaHasta.setDate(1)
            fechaHasta = util.addMonths(fechaHasta, 1)
            fechaHasta = util.addDays(fechaHasta, - 1)
            intervalo.hasta = fechaHasta
            s2a_do_work = False # BREAK
        
        if s2a_when == u"000006": s2a_do_work,s2a_work_done = True,True
        if s2a_do_work:
            fechaDesde.setDate(1)
            fechaDesde = util.addMonths(fechaDesde, - 1)
            intervalo.desde = fechaDesde
            fechaHasta.setDate(1)
            fechaHasta = util.addDays(fechaHasta, - 1)
            intervalo.hasta = fechaHasta
            s2a_do_work = False # BREAK
        
        if s2a_when == u"000007": s2a_do_work,s2a_work_done = True,True
        if s2a_do_work:
            fechaDesde.setDate(1)
            fechaDesde.setMonth(1)
            intervalo.desde = fechaDesde
            fechaHasta.setMonth(12)
            fechaHasta.setDate(31)
            intervalo.hasta = fechaHasta
            s2a_do_work = False # BREAK
        
        if s2a_when == u"000008": s2a_do_work,s2a_work_done = True,True
        if s2a_do_work:
            anio = fechaDesde.getYear() - 1
            fechaDesde.setDate(1)
            fechaDesde.setMonth(1)
            fechaDesde.setYear(anio)
            intervalo.desde = fechaDesde
            fechaHasta.setMonth(12)
            fechaHasta.setDate(31)
            fechaHasta.setYear(anio)
            intervalo.hasta = fechaHasta
            s2a_do_work = False # BREAK
        
        if s2a_when == u"000009": s2a_do_work,s2a_work_done = True,True
        if s2a_do_work:
            intervalo.desde = u"1970-01-01"
            intervalo.hasta = u"3000-01-01"
            s2a_do_work = False # BREAK
        if s2a_when == u"000010": s2a_do_work,s2a_work_done = True,True
        if s2a_do_work:
            intervalo.desde = u"1970-01-01"
            intervalo.hasta = fechaHasta
            s2a_do_work = False # BREAK
        return intervalo
    
    def oficial_crearSubcuentaCli(self, codSubcuenta = None, idSubcuenta = None, codCliente = None, codEjercicio = None):
        curSubcuentaCli = qsatype.FLSqlCursor(u"co_subcuentascli")
         #WITH_START
        curSubcuentaCli.setModeAccess(curSubcuentaCli.Insert)
        curSubcuentaCli.refreshBuffer()
        curSubcuentaCli.setValueBuffer(u"codsubcuenta", codSubcuenta)
        curSubcuentaCli.setValueBuffer(u"idSubcuenta", idSubcuenta)
        curSubcuentaCli.setValueBuffer(u"codcliente", codCliente)
        curSubcuentaCli.setValueBuffer(u"codejercicio", codEjercicio)
         #WITH_END
        if not curSubcuentaCli.commitBuffer():
            return False
        return True
    
    def oficial_crearSubcuentaProv(self, codSubcuenta = None, idSubcuenta = None, codProveedor = None, codEjercicio = None):
        curSubcuentaProv = qsatype.FLSqlCursor(u"co_subcuentasprov")
         #WITH_START
        curSubcuentaProv.setModeAccess(curSubcuentaProv.Insert)
        curSubcuentaProv.refreshBuffer()
        curSubcuentaProv.setValueBuffer(u"codsubcuenta", codSubcuenta)
        curSubcuentaProv.setValueBuffer(u"idSubcuenta", idSubcuenta)
        curSubcuentaProv.setValueBuffer(u"codproveedor", codProveedor)
        curSubcuentaProv.setValueBuffer(u"codejercicio", codEjercicio)
         #WITH_END
        if not curSubcuentaProv.commitBuffer():
            return False
        return True
    
    def oficial_rellenarSubcuentasCli(self, codCliente = None, codSubcuenta = None, nombre = None):
        if not sys.isLoadedModule(u"flcontppal"):
            return True
        if not codSubcuenta:
            return True
        util = qsatype.FLUtil()
        qry = qsatype.FLSqlQuery()
        qry.setTablesList(u"ejercicios,co_subcuentascli")
        qry.setSelect(u"e.codejercicio")
        qry.setFrom(ustr( u"ejercicios e LEFT OUTER JOIN co_subcuentascli s ON e.codejercicio = s.codejercicio AND s.codcliente = '" , codCliente , u"'" ))
        qry.setWhere(u"s.id IS NULL AND e.estado = 'ABIERTO' AND e.fechafin >= CURRENT_DATE")
        if not qry.exec_():
            return False
        idSubcuenta = 0
        codEjercicio = ""
        while qry.next():
            codEjercicio = qry.value(0)
            if not util.sqlSelect(u"co_epigrafes", u"codepigrafe", ustr( u"codejercicio = '" , codEjercicio , u"'" )):
                continue 
            idSubcuenta = self.iface.crearSubcuenta(codSubcuenta, nombre, u"CLIENT", codEjercicio)
            if not idSubcuenta:
                return False
            if idSubcuenta == True:
                continue 
            if not self.iface.crearSubcuentaCli(codSubcuenta, idSubcuenta, codCliente, codEjercicio):
                return False
        
        return True
    
    def oficial_rellenarSubcuentasProv(self, codProveedor = None, codSubcuenta = None, nombre = None):
        if not sys.isLoadedModule(u"flcontppal"):
            return 
        util = qsatype.FLUtil()
        qry = qsatype.FLSqlQuery()
        qry.setTablesList(u"ejercicios,co_subcuentasprov")
        qry.setSelect(u"e.codejercicio")
        qry.setFrom(ustr( u"ejercicios e LEFT OUTER JOIN co_subcuentasprov s ON e.codejercicio = s.codejercicio AND s.codproveedor = '" , codProveedor , u"'" ))
        qry.setWhere(u"s.id IS NULL AND e.estado = 'ABIERTO' AND e.fechafin >= CURRENT_DATE")
        if not qry.exec_():
            return False
        idSubcuenta = 0
        codEjercicio = ""
        while qry.next():
            codEjercicio = qry.value(0)
            if not util.sqlSelect(u"co_epigrafes", u"codepigrafe", ustr( u"codejercicio = '" , codEjercicio , u"'" )):
                continue 
            idSubcuenta = self.iface.crearSubcuenta(codSubcuenta, nombre, u"PROVEE", codEjercicio)
            if not idSubcuenta:
                return False
            if idSubcuenta == True:
                continue 
            if not self.iface.crearSubcuentaProv(codSubcuenta, idSubcuenta, codProveedor, codEjercicio):
                return False
        
        return True
    
    def oficial_automataActivado(self):
        if not sys.isLoadedModule(u"flautomata"):
            return False
        if formau_automata.iface.pub_activado():
            return True
        return False
    
    def oficial_clienteActivo(self, codCliente = None, fecha = None):
        util = qsatype.FLUtil()
        if not codCliente or codCliente == u"":
            return True
        qryBaja = qsatype.FLSqlQuery()
        qryBaja.setTablesList(u"clientes")
        qryBaja.setSelect(u"debaja, fechabaja")
        qryBaja.setFrom(u"clientes")
        qryBaja.setWhere(ustr( u"codcliente = '" , codCliente , u"'" ))
        qryBaja.setForwardOnly(True)
        if not qryBaja.exec_():
            return False
        if not qryBaja.first():
            return False
        if not qryBaja.value(u"debaja"):
            return True
        if util.daysTo(fecha, qryBaja.value(u"fechabaja")) <= 0:
            if not self.iface.automataActivado():
                fechaDdMmAaaa = util.dateAMDtoDMA(fecha)
                MessageBox.warning(util.translate(u"scripts", u"El cliente está de baja para la fecha especificada (%1)").arg(fechaDdMmAaaa), MessageBox.Ok, MessageBox.NoButton)
            return False
        
        return True
    
    def oficial_obtenerProvincia(self, formulario = None, campoId = None, campoProvincia = None, campoPais = None):
        util = qsatype.FLUtil()
        if not campoId:
            campoId = u"idprovincia"
        if not campoProvincia:
            campoProvincia = u"provincia"
        if not campoPais:
            campoPais = u"codpais"
        provincia = formulario.cursor().valueBuffer(campoProvincia)
        if not provincia or provincia == u"":
            return 
        if provincia.endswith(u"."):
            formulario.cursor().setNull(campoId)
            provincia = provincia[0:len(provincia) - 1]
            provincia = provincia.toUpperCase()
            where = ustr( u"UPPER(provincia) LIKE '" , provincia , u"%'" )
            codPais = formulario.cursor().valueBuffer(campoPais)
            if codPais and codPais != u"":
                where += ustr( u" AND codpais = '" , codPais , u"'" )
            qryProvincia = qsatype.FLSqlQuery()
             #WITH_START
            qryProvincia.setTablesList(u"provincias")
            qryProvincia.setSelect(u"idprovincia")
            qryProvincia.setFrom(u"provincias")
            qryProvincia.setForwardOnly(True)
             #WITH_END
            qryProvincia.setWhere(where)
            if not qryProvincia.exec_():
                return False
            sc0_when = qryProvincia.size()
            sc0_do_work,sc0_work_done = False,False
            if sc0_when == 0: sc0_do_work,sc0_work_done = True,True
            if sc0_do_work:
                return 
            if sc0_when == 1: sc0_do_work,sc0_work_done = True,True
            if sc0_do_work:
                if not qryProvincia.first():
                    return False
                formulario.cursor().setValueBuffer(campoId, qryProvincia.value(u"idprovincia"))
                sc0_do_work = False # BREAK
            
            if not sc0_work_done: sc0_do_work,sc0_work_done = True,True
            if sc0_do_work:
                listaProvincias = u""
                while qryProvincia.next():
                    if listaProvincias != u"":
                        listaProvincias += u", "
                    listaProvincias += qryProvincia.value(u"idprovincia")
                f = qsatype.FLFormSearchDB(u"provincias")
                curProvincias = f.cursor()
                curProvincias.setMainFilter(ustr( u"idprovincia IN (" , listaProvincias , u")" ))
                f.setMainWidget()
                idProvincia = f.exec_(u"idprovincia")
                if idProvincia:
                    formulario.cursor().setValueBuffer(campoId, idProvincia)
                sc0_do_work = False # BREAK
    
    def oficial_actualizarContactos20070525(self):
        util = qsatype.FLUtil()
        qryClientes = qsatype.FLSqlQuery()
        qryClientes.setTablesList(u"clientes")
        qryClientes.setFrom(u"clientes")
        qryClientes.setSelect(u"codcliente,codcontacto,contacto")
        qryClientes.setWhere(u"")
        if not qryClientes.exec_():
            return False
        util.createProgressDialog(util.translate(u"scripts", u"Reorganizando Contactos"), qryClientes.size())
        util.setProgress(0)
        cont = 1
        while qryClientes.next():
            util.setProgress(cont)
            cont += 1
            codCliente = qryClientes.value(u"codcliente")
            if not codCliente:
                util.destroyProgressDialog()
                return False
            qryAgenda = qsatype.FLSqlQuery()
            qryAgenda.setTablesList(u"contactosclientes")
            qryAgenda.setFrom(u"contactosclientes")
            qryAgenda.setSelect(u"contacto,cargo,telefono,fax,email,id,codcliente")
            qryAgenda.setWhere(ustr( u"codcliente = '" , codCliente , u"'" ))
            if not qryAgenda.exec_():
                util.destroyProgressDialog()
                return False
            if sys.isLoadedModule(u"flcrm_ppal"):
                qryClientesContactos = qsatype.FLSqlQuery()
                qryClientesContactos.setTablesList(u"crm_clientescontactos")
                qryClientesContactos.setFrom(u"crm_clientescontactos")
                qryClientesContactos.setSelect(u"codcontacto")
                qryClientesContactos.setWhere(ustr( u"codcliente = '" , codCliente , u"' AND codcontacto NOT IN(SELECT codcontacto FROM contactosclientes WHERE codcliente = '" , codCliente , u"')" ))
                if not qryClientesContactos.exec_():
                    util.destroyProgressDialog()
                    return False
                while qryClientesContactos.next():
                    self.iface.actualizarContactosDeAgenda20070525(codCliente, qryClientesContactos.value(u"codcontacto"))
            
            while qryAgenda.next():
                nombreCon = qryAgenda.value(u"contacto")
                cargoCon = qryAgenda.value(u"cargo")
                telefonoCon = qryAgenda.value(u"telefono")
                faxCon = qryAgenda.value(u"fax")
                emailCon = qryAgenda.value(u"email")
                idAgenda = qryAgenda.value(u"id")
                if not idAgenda or idAgenda == 0:
                    util.destroyProgressDialog()
                    return False
                qryContactos = qsatype.FLSqlQuery()
                qryContactos.setTablesList(u"crm_contactos,contactosclientes")
                qryContactos.setFrom(u"crm_contactos INNER JOIN contactosclientes ON crm_contactos.codcontacto = contactosclientes.codcontacto")
                qryContactos.setSelect(u"crm_contactos.codcontacto")
                qryContactos.setWhere(ustr( u"crm_contactos.nombre = '" , nombreCon , u"' AND (contactosclientes.codcliente = '" , codCliente , u"' AND (crm_contactos.email = '" , emailCon , u"' AND crm_contactos.telefono1 = '" , telefonoCon , u"'))" ))
                if not qryContactos.exec_():
                    util.destroyProgressDialog()
                    return False
                codContacto = u""
                if qryContactos.first():
                    codContacto = qryContactos.value(u"crm_contactos.codcontacto")
                if not self.iface.actualizarContactosDeAgenda20070525(codCliente, codContacto, nombreCon, cargoCon, telefonoCon, faxCon, emailCon, idAgenda):
                    util.destroyProgressDialog()
                    return False
            
            if ( qryClientes.value(u"contacto") and qryClientes.value(u"contacto") != u"" ) and ( not qryClientes.value(u"codcontacto") or qryClientes.value(u"codcontacto") == u"" ):
                codContacto = util.sqlSelect(u"crm_contactos", u"codcontacto", ustr( u"nombre = '" , self.iface.escapeQuote(qryClientes.value(u"contacto")) , u"'" ))
                if codContacto:
                    self.iface.actualizarContactosDeAgenda20070525(codCliente, codContacto, qryClientes.value(u"contacto"))
                else:
                    codContacto = self.iface.actualizarContactosDeAgenda20070525(codCliente, u"", qryClientes.value(u"contacto"))
                
                if not codContacto:
                    util.destroyProgressDialog()
                    return False
                curCliente = qsatype.FLSqlCursor(u"clientes")
                curCliente.select(ustr( u"codcliente = '" , codCliente , u"'" ))
                curCliente.setModeAccess(curCliente.Edit)
                if not curCliente.first():
                    util.destroyProgressDialog()
                    return False
                curCliente.refreshBuffer()
                curCliente.setValueBuffer(u"codcontacto", codContacto)
                if not curCliente.commitBuffer():
                    util.destroyProgressDialog()
                    return False
        
        util.setProgress(qryClientes.size())
        util.destroyProgressDialog()
        return True
    
    def oficial_actualizarContactosProv20070702(self):
        util = qsatype.FLUtil()
        qryProveedores = qsatype.FLSqlQuery()
        qryProveedores.setTablesList(u"proveedores")
        qryProveedores.setFrom(u"proveedores")
        qryProveedores.setSelect(u"codproveedor,codcontacto,contacto")
        qryProveedores.setWhere(u"")
        if not qryProveedores.exec_():
            return False
        util.createProgressDialog(util.translate(u"scripts", u"Reorganizando Contactos"), qryProveedores.size())
        util.setProgress(0)
        cont = 1
        while qryProveedores.next():
            util.setProgress(cont)
            cont += 1
            codProveedor = qryProveedores.value(u"codproveedor")
            if not codProveedor:
                util.destroyProgressDialog()
                return False
            qryAgenda = qsatype.FLSqlQuery()
            qryAgenda.setTablesList(u"contactosproveedores")
            qryAgenda.setFrom(u"contactosproveedores")
            qryAgenda.setSelect(u"contacto,cargo,telefono,fax,email,id,codproveedor")
            qryAgenda.setWhere(ustr( u"codproveedor = '" , codProveedor , u"'" ))
            if not qryAgenda.exec_():
                util.destroyProgressDialog()
                return False
            while qryAgenda.next():
                nombreCon = qryAgenda.value(u"contacto")
                cargoCon = qryAgenda.value(u"cargo")
                telefonoCon = qryAgenda.value(u"telefono")
                faxCon = qryAgenda.value(u"fax")
                emailCon = qryAgenda.value(u"email")
                idAgenda = qryAgenda.value(u"id")
                if not idAgenda or idAgenda == 0:
                    util.destroyProgressDialog()
                    return False
                qryContactos = qsatype.FLSqlQuery()
                qryContactos.setTablesList(u"crm_contactos,contactosproveedores")
                qryContactos.setFrom(u"crm_contactos INNER JOIN contactosproveedores ON crm_contactos.codcontacto = contactosproveedores.codcontacto")
                qryContactos.setSelect(u"crm_contactos.codcontacto")
                qryContactos.setWhere(ustr( u"crm_contactos.nombre = '" , nombreCon , u"' AND (contactosproveedores.codproveedor = '" , codProveedor , u"' AND (crm_contactos.email = '" , emailCon , u"' AND crm_contactos.telefono1 = '" , telefonoCon , u"'))" ))
                if not qryContactos.exec_():
                    util.destroyProgressDialog()
                    return False
                codContacto = u""
                if qryContactos.first():
                    codContacto = qryContactos.value(u"crm_contactos.codcontacto")
                if not self.iface.actualizarContactosDeAgendaProv20070702(codProveedor, codContacto, nombreCon, cargoCon, telefonoCon, faxCon, emailCon, idAgenda):
                    util.destroyProgressDialog()
                    return False
            
            if ( qryProveedores.value(u"contacto") and qryProveedores.value(u"contacto") != u"" ) and ( not qryProveedores.value(u"codcontacto") or qryProveedores.value(u"codcontacto") == u"" ):
                codContacto = util.sqlSelect(u"crm_contactos", u"codcontacto", ustr( u"nombre = '" , qryProveedores.value(u"contacto") , u"'" ))
                if codContacto:
                    self.iface.actualizarContactosDeAgendaProv20070702(codProveedor, codContacto, qryProveedores.value(u"contacto"))
                else:
                    codContacto = self.iface.actualizarContactosDeAgendaProv20070702(codProveedor, u"", qryProveedores.value(u"contacto"))
                
                if not codContacto:
                    util.destroyProgressDialog()
                    return False
                curProveedor = qsatype.FLSqlCursor(u"proveedores")
                curProveedor.select(ustr( u"codproveedor = '" , codProveedor , u"'" ))
                curProveedor.setModeAccess(curProveedor.Edit)
                if not curProveedor.first():
                    util.destroyProgressDialog()
                    return False
                curProveedor.refreshBuffer()
                curProveedor.setValueBuffer(u"codcontacto", codContacto)
                if not curProveedor.commitBuffer():
                    util.destroyProgressDialog()
                    return False
        
        util.setProgress(qryProveedores.size())
        util.destroyProgressDialog()
        return True
    
    def oficial_actualizarContactosDeAgenda20070525(self, codCliente = None, codContacto = None, nombreCon = None, cargoCon = None, telefonoCon = None, faxCon = None, emailCon = None, idAgenda = None):
        util = qsatype.FLUtil()
        curContactos = qsatype.FLSqlCursor(u"crm_contactos")
        curAgenda = qsatype.FLSqlCursor(u"contactosclientes")
        if codContacto and codContacto != u"":
            curContactos.select(ustr( u"codcontacto = '" , codContacto , u"'" ))
            if not curContactos.first():
                return False
            curContactos.setModeAccess(curContactos.Edit)
            curContactos.refreshBuffer()
            if not curContactos.valueBuffer(u"cargo") or curContactos.valueBuffer(u"cargo") == u"":
                curContactos.setValueBuffer(u"cargo", cargoCon)
            if not curContactos.valueBuffer(u"telefono1") or curContactos.valueBuffer(u"telefono1") == u"":
                curContactos.setValueBuffer(u"telefono1", telefonoCon)
            else:
                if not curContactos.valueBuffer(u"telefono2") or curContactos.valueBuffer(u"telefono2") == u"":
                    curContactos.setValueBuffer(u"telefono2", telefonoCon)
            
            if not curContactos.valueBuffer(u"fax") or curContactos.valueBuffer(u"fax") == u"":
                curContactos.setValueBuffer(u"fax", faxCon)
            if not curContactos.valueBuffer(u"email") or curContactos.valueBuffer(u"email") == u"":
                curContactos.setValueBuffer(u"email", emailCon)
        
        else:
             #WITH_START
            curContactos.setModeAccess(Insert)
            curContactos.refreshBuffer()
            curContactos.setValueBuffer(u"codcontacto", util.nextCounter(u"codcontacto", self))
            curContactos.setValueBuffer(u"nombre", nombreCon)
            curContactos.setValueBuffer(u"email", emailCon)
            curContactos.setValueBuffer(u"telefono1", telefonoCon)
            curContactos.setValueBuffer(u"cargo", cargoCon)
            curContactos.setValueBuffer(u"fax", faxCon)
             #WITH_END
            if not curContactos.commitBuffer():
                return False
            codContacto = curContactos.valueBuffer(u"codcontacto")
            if not codContacto:
                return False
        
        if not idAgenda or idAgenda == 0:
            if not util.sqlSelect(u"contactosclientes", u"id", ustr( u"codcontacto = '" , codContacto , u"' AND codcliente = '" , codCliente , u"'" )):
                curAgenda.setModeAccess(curAgenda.Insert)
                curAgenda.refreshBuffer()
                curAgenda.setValueBuffer(u"codcliente", codCliente)
                curAgenda.setValueBuffer(u"codcontacto", codContacto)
                if not curAgenda.commitBuffer():
                    return False
        
        else:
            curAgenda.select(ustr( u"id = " , idAgenda ))
            if not curAgenda.first():
                return False
            curAgenda.setModeAccess(curAgenda.Edit)
            curAgenda.refreshBuffer()
            curAgenda.setValueBuffer(u"codcontacto", codContacto)
            if not curAgenda.commitBuffer():
                return False
        
        return codContacto
    
    def oficial_lanzarEvento(self, cursor = None, evento = None):
        datosEvento = qsatype.Array()
        datosEvento[u"tipoobjeto"] = cursor.table()
        datosEvento[u"idobjeto"] = cursor.valueBuffer(cursor.primaryKey())
        datosEvento[u"evento"] = evento
        if not flcolaproc.iface.pub_procesarEvento(datosEvento):
            return False
        return True
    
    def oficial_actualizarContactosDeAgendaProv20070702(self, codProveedor = None, codContacto = None, nombreCon = None, cargoCon = None, telefonoCon = None, faxCon = None, emailCon = None, idAgenda = None):
        util = qsatype.FLUtil()
        curContactos = qsatype.FLSqlCursor(u"crm_contactos")
        curAgenda = qsatype.FLSqlCursor(u"contactosproveedores")
        if codContacto and codContacto != u"":
            curContactos.select(ustr( u"codcontacto = '" , codContacto , u"'" ))
            if not curContactos.first():
                return False
            curContactos.setModeAccess(curContactos.Edit)
            curContactos.refreshBuffer()
            if not curContactos.valueBuffer(u"cargo") or curContactos.valueBuffer(u"cargo") == u"":
                curContactos.setValueBuffer(u"cargo", cargoCon)
            if not curContactos.valueBuffer(u"telefono1") or curContactos.valueBuffer(u"telefono1") == u"":
                curContactos.setValueBuffer(u"telefono1", telefonoCon)
            else:
                if not curContactos.valueBuffer(u"telefono2") or curContactos.valueBuffer(u"telefono2") == u"":
                    curContactos.setValueBuffer(u"telefono2", telefonoCon)
            
            if not curContactos.valueBuffer(u"fax") or curContactos.valueBuffer(u"fax") == u"":
                curContactos.setValueBuffer(u"fax", faxCon)
            if not curContactos.valueBuffer(u"email") or curContactos.valueBuffer(u"email") == u"":
                curContactos.setValueBuffer(u"email", emailCon)
        
        else:
             #WITH_START
            curContactos.setModeAccess(Insert)
            curContactos.refreshBuffer()
            curContactos.setValueBuffer(u"codcontacto", util.nextCounter(u"codcontacto", self))
            curContactos.setValueBuffer(u"nombre", nombreCon)
            curContactos.setValueBuffer(u"email", emailCon)
            curContactos.setValueBuffer(u"telefono1", telefonoCon)
            curContactos.setValueBuffer(u"cargo", cargoCon)
            curContactos.setValueBuffer(u"fax", faxCon)
             #WITH_END
            if not curContactos.commitBuffer():
                return False
            codContacto = curContactos.valueBuffer(u"codcontacto")
            if not codContacto:
                return False
        
        if not idAgenda or idAgenda == 0:
            if not util.sqlSelect(u"contactosproveedores", u"id", ustr( u"codcontacto = '" , codContacto , u"' AND codproveedor = '" , codProveedor , u"'" )):
                curAgenda.setModeAccess(curAgenda.Insert)
                curAgenda.refreshBuffer()
                curAgenda.setValueBuffer(u"codproveedor", codProveedor)
                curAgenda.setValueBuffer(u"codcontacto", codContacto)
                if not curAgenda.commitBuffer():
                    return False
        
        else:
            curAgenda.select(ustr( u"id = " , idAgenda ))
            if not curAgenda.first():
                return False
            curAgenda.setModeAccess(curAgenda.Edit)
            curAgenda.refreshBuffer()
            curAgenda.setValueBuffer(u"codcontacto", codContacto)
            if not curAgenda.commitBuffer():
                return False
        
        return codContacto
    
    def oficial_elegirOpcion(self, opciones = None, titulo = None):
        util = qsatype.FLUtil()
        dialog = qsatype.Dialog()
        dialog.okButtonText = util.translate(u"scripts", u"Aceptar")
        dialog.cancelButtonText = util.translate(u"scripts", u"Cancelar")
        dialog.title = titulo
        bgroup = qsatype.GroupBox()
        dialog.add(bgroup)
        rB = qsatype.Array()
        i = 0
        while_pass = True
        while i < len(opciones):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            rB[i] = qsatype.RadioButton()
            bgroup.add(rB[i])
            rB[i].text = opciones[i]
            if i == 0:
                rB[i].checked = True
            else:
                rB[i].checked = False
            
            if ( i + 1 ) % 25 == 0:
                bgroup.newColumn()
            i += 1
            while_pass = True
            try:
                i < len(opciones)
            except: break
        
        if dialog.exec_():
            i = 0
            while_pass = True
            while i < len(opciones):
                if not while_pass:
                    i += 1
                    while_pass = True
                    continue
                while_pass = False
                if rB[i].checked == True:
                    return i
                i += 1
                while_pass = True
                try:
                    i < len(opciones)
                except: break
        
        else:
            return - 1
        
    
    def oficial_textoFecha(self, fecha = None):
        util = qsatype.FLUtil()
        if not fecha or fecha == u"":
            return u""
        mes = fecha[5:5 +  2]
        textoMes = ""
        sd4_when = mes
        sd4_do_work,sd4_work_done = False,False
        if sd4_when == u"01": sd4_do_work,sd4_work_done = True,True
        if sd4_do_work:
            textoMes = util.translate(u"scripts", u"Enero")
            sd4_do_work = False # BREAK
        if sd4_when == u"02": sd4_do_work,sd4_work_done = True,True
        if sd4_do_work:
            textoMes = util.translate(u"scripts", u"Febrero")
            sd4_do_work = False # BREAK
        if sd4_when == u"03": sd4_do_work,sd4_work_done = True,True
        if sd4_do_work:
            textoMes = util.translate(u"scripts", u"Marzo")
            sd4_do_work = False # BREAK
        if sd4_when == u"04": sd4_do_work,sd4_work_done = True,True
        if sd4_do_work:
            textoMes = util.translate(u"scripts", u"Abril")
            sd4_do_work = False # BREAK
        if sd4_when == u"05": sd4_do_work,sd4_work_done = True,True
        if sd4_do_work:
            textoMes = util.translate(u"scripts", u"Mayo")
            sd4_do_work = False # BREAK
        if sd4_when == u"06": sd4_do_work,sd4_work_done = True,True
        if sd4_do_work:
            textoMes = util.translate(u"scripts", u"Junio")
            sd4_do_work = False # BREAK
        if sd4_when == u"07": sd4_do_work,sd4_work_done = True,True
        if sd4_do_work:
            textoMes = util.translate(u"scripts", u"Julio")
            sd4_do_work = False # BREAK
        if sd4_when == u"08": sd4_do_work,sd4_work_done = True,True
        if sd4_do_work:
            textoMes = util.translate(u"scripts", u"Agosto")
            sd4_do_work = False # BREAK
        if sd4_when == u"09": sd4_do_work,sd4_work_done = True,True
        if sd4_do_work:
            textoMes = util.translate(u"scripts", u"Septiembre")
            sd4_do_work = False # BREAK
        if sd4_when == u"10": sd4_do_work,sd4_work_done = True,True
        if sd4_do_work:
            textoMes = util.translate(u"scripts", u"Octubre")
            sd4_do_work = False # BREAK
        if sd4_when == u"11": sd4_do_work,sd4_work_done = True,True
        if sd4_do_work:
            textoMes = util.translate(u"scripts", u"Noviembre")
            sd4_do_work = False # BREAK
        if sd4_when == u"12": sd4_do_work,sd4_work_done = True,True
        if sd4_do_work:
            textoMes = util.translate(u"scripts", u"Diciembre")
            sd4_do_work = False # BREAK
        dia = parseInt(fecha[8:8 +  2])
        ano = parseInt(fecha[0:0 +  4])
        texto = util.translate(u"scripts", u"%1 de %2 de %3").arg(parseString(dia)).arg(textoMes).arg(ano)
        return texto
    
    def oficial_validarNifIva(self, nifIva = None):
        util = qsatype.FLUtil()
        error = ""
        if not nifIva or nifIva == u"":
            error = util.translate(u"scripts", u"No se ha establecido el NIF/IVA")
            return error
        codPais = nifIva[0:2]
        pais = ""
        longPosibles = qsatype.Array()
        s4c_when = codPais
        s4c_do_work,s4c_work_done = False,False
        if s4c_when == u"DE": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([9])
            pais = util.translate(u"scripts", u"Alemania")
            s4c_do_work = False # BREAK
        if s4c_when == u"AT": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([9])
            pais = util.translate(u"scripts", u"Austria")
            s4c_do_work = False # BREAK
        if s4c_when == u"BE": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([9, 10])
            pais = util.translate(u"scripts", u"Bélgica")
            s4c_do_work = False # BREAK
        if s4c_when == u"BG": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([9, 10])
            pais = util.translate(u"scripts", u"Bulgaria")
            s4c_do_work = False # BREAK
        if s4c_when == u"CY": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([9])
            pais = util.translate(u"scripts", u"Chipre")
            s4c_do_work = False # BREAK
        if s4c_when == u"CZ": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([9])
            pais = util.translate(u"scripts", u"Chequia")
            s4c_do_work = False # BREAK
        if s4c_when == u"DK": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([8])
            pais = util.translate(u"scripts", u"Dinamarca")
            s4c_do_work = False # BREAK
        if s4c_when == u"EE": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([9])
            pais = util.translate(u"scripts", u"Estonia")
            s4c_do_work = False # BREAK
        if s4c_when == u"FI": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([8])
            pais = util.translate(u"scripts", u"Finlandia")
            s4c_do_work = False # BREAK
        if s4c_when == u"FR": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([11])
            pais = util.translate(u"scripts", u"Francia")
            s4c_do_work = False # BREAK
        if s4c_when == u"EL": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([9])
            pais = util.translate(u"scripts", u"Grecia")
            s4c_do_work = False # BREAK
        if s4c_when == u"GB": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([5, 9, 12])
            pais = util.translate(u"scripts", u"Gran Bretaña")
            s4c_do_work = False # BREAK
        if s4c_when == u"NL": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([12])
            pais = util.translate(u"scripts", u"Holanda")
            s4c_do_work = False # BREAK
        if s4c_when == u"HU": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([8])
            pais = util.translate(u"scripts", u"Hungría")
            s4c_do_work = False # BREAK
        if s4c_when == u"IT": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([11])
            pais = util.translate(u"scripts", u"Gran Bretaña")
            s4c_do_work = False # BREAK
        if s4c_when == u"IE": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([8])
            pais = util.translate(u"scripts", u"Irlanda")
            s4c_do_work = False # BREAK
        if s4c_when == u"LT": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([9, 12])
            pais = util.translate(u"scripts", u"Lituania")
            s4c_do_work = False # BREAK
        if s4c_when == u"LU": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([8])
            pais = util.translate(u"scripts", u"Luxemburgo")
            s4c_do_work = False # BREAK
        if s4c_when == u"PL": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([10])
            pais = util.translate(u"scripts", u"Polonia")
            s4c_do_work = False # BREAK
        if s4c_when == u"PT": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([9])
            pais = util.translate(u"scripts", u"Portugal")
            s4c_do_work = False # BREAK
        if s4c_when == u"RO": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([2, 3, 4, 5, 6, 7, 8, 9, 10])
            pais = util.translate(u"scripts", u"Rumanía")
            s4c_do_work = False # BREAK
        if s4c_when == u"SE": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([12])
            pais = util.translate(u"scripts", u"Suecia")
            s4c_do_work = False # BREAK
        if s4c_when == u"SI": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([8])
            pais = util.translate(u"scripts", u"Eslovenia")
            s4c_do_work = False # BREAK
        if s4c_when == u"SK": s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            longPosibles = qsatype.Array([10])
            pais = util.translate(u"scripts", u"Eslovaquia")
            s4c_do_work = False # BREAK
        if not s4c_work_done: s4c_do_work,s4c_work_done = True,True
        if s4c_do_work:
            error = util.translate(u"scripts", u"El código de país %1 no es correcto").arg(codPais)
            return error
        longOk = False
        longitud = len(nifIva) - 2
        i = 0
        while_pass = True
        while i < len(longPosibles):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            if longitud == longPosibles[i]:
                longOk = True
            i += 1
            while_pass = True
            try:
                i < len(longPosibles)
            except: break
        
        if not longOk:
            longTotales = qsatype.Array(len(longPosibles))
            i = 0
            while_pass = True
            while i < len(longPosibles):
                if not while_pass:
                    i += 1
                    while_pass = True
                    continue
                while_pass = False
                longTotales[i] = longPosibles[i] + 2
                i += 1
                while_pass = True
                try:
                    i < len(longPosibles)
                except: break
            
            error = util.translate(u"scripts", u"Error en la validación del NIF/IVA %1 para el país %2:\nLas longitudes admitidas son: %3").arg(nifIva).arg(pais).arg(longTotales.join(u", "))
            return error
        
        return u"OK"
    
    def oficial_ejecutarComandoAsincrono(self, comando = None):
        res = qsatype.Array()
        qsatype.Process.execute(comando)
        if qsatype.Process.stderr != u"":
            res[u"ok"] = False
            res[u"salida"] = qsatype.Process.stderr
        else:
            res[u"ok"] = True
            res[u"salida"] = qsatype.Process.stdout
        
        return res
    
    def oficial_globalInit(self):
        if sys.isLoadedModule(u"flcolaproc"):
            try:
                flcolaproc.iface.pub_globalInit()
            except Exception as e:
                e = traceback.format_exc()
            
        
        if sys.isLoadedModule(u"flcolamens"):
            try:
                flcolamens.iface.pub_globalInit()
            except Exception as e:
                e = traceback.format_exc()
            
    
    def oficial_existeEnvioMail(self):
        return False
    
    def oficial_validarProvincia(self, cursor = None, mtd = None):
        util = qsatype.FLUtil()
        if not mtd:
            mtd = []
            mtd[u"idprovincia"] = u"idprovincia"
            mtd[u"provincia"] = u"provincia"
            mtd[u"codpais"] = u"codpais"
        
        idProvincia = cursor.valueBuffer(mtd[u"idprovincia"])
        provincia = cursor.valueBuffer(mtd[u"provincia"])
        codPais = cursor.valueBuffer(mtd[u"codpais"])
        if util.sqlSelect(u"paises", u"validarprov", ustr( u"codpais = '" , codPais , u"'" )):
            if not idProvincia or idProvincia == u"":
                idProvincia = False
                if provincia and provincia != u"" and provincia != None:
                    idProvincia = util.sqlSelect(u"provincias", u"idprovincia", ustr( u"UPPER(provincia) = '" , provincia.toUpperCase() , u"' AND codpais = '" , codPais , u"'" ))
                    if idProvincia:
                        cursor.setValueBuffer(mtd[u"idprovincia"], idProvincia)
                if not idProvincia:
                    MessageBox.warning(util.translate(u"scripts", u"La provincia %1 no pertenece al país %2").arg(provincia).arg(codPais), MessageBox.Ok, MessageBox.NoButton)
                    return False
            
            else:
                idProvTabla = util.sqlSelect(u"provincias", u"idprovincia", ustr( u"UPPER(provincia) = '" , provincia.toUpperCase() , u"' AND codpais = '" , codPais , u"' AND idprovincia = " , idProvincia ))
                if not idProvTabla:
                    MessageBox.warning(util.translate(u"scripts", u"La provincia %1 no pertenece al país %2").arg(provincia).arg(codPais), MessageBox.Ok, MessageBox.NoButton)
                    return False
            
        
        return True
    
    def oficial_simplify(self, str = None):
        regExp = qsatype.RegExp(u"( |\n|\r|\t|\f)")
        regExp.global_ = True
        str = str.replace(regExp, u"")
        return str
    
    def oficial_escapeQuote(self, str = None):
        regExp = qsatype.RegExp(u"'")
        regExp.global_ = True
        str = str.replace(regExp, u"''")
        return str
    
    def oficial_calcularIBAN(self, cuenta = None, codPais = None):
        _i = self.iface
        IBAN = u""
        if not cuenta or cuenta == u"":
            return u""
        codIso = None
        if codPais and codPais != u"":
            codIso = AQUtil.sqlSelect(u"paises", u"codiso", ustr( u"codpais = '" , codPais , u"'" ))
            codIso = ( u"ES" if ( not codIso or codIso == u"" ) else codIso )
        else:
            codIso = u"ES"
        
        digControl = _i.digitoControlMod97(cuenta, codIso)
        IBAN += codIso + digControl + cuenta
        return IBAN
    
    def oficial_moduloNumero(self, num = None, div = None):
        d = None
        i = 0
        a = 1
        parcial = 0
        i = len(num) - 1
        while_pass = True
        while i >= 0:
            if not while_pass:
                i -= 1
                while_pass = True
                continue
            while_pass = False
            d = parseInt(num[i])
            parcial += ( d * a )
            a = ( a * 10 ) % div
            i -= 1
            while_pass = True
            try:
                i >= 0
            except: break
        
        return parcial % div
    
    def oficial_digitoControlMod97(self, numero = None, codPais = None):
        _i = self.iface
        cadena = u""
        cadena += ustr( parseString(numero) , codPais.toUpperCase() , u"00" )
        i = 0
        while_pass = True
        while i < len(cadena):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            if isNaN(cadena[i]):
                trans = cadena.charCodeAt(i) - 55
                cadena = cadena.replace(cadena[i], trans)
            i += 1
            while_pass = True
            try:
                i < len(cadena)
            except: break
        
        digControl = _i.moduloNumero(cadena, 97)
        digControl = 98 - digControl
        digControl = flfactppal.iface.pub_cerosIzquierda(digControl, 2)
        return digControl
    
    def oficial_calcularIdentificadorAcreedor(self, cifEmpresa = None, codCuenta = None):
        _i = self.iface
        codPais = AQUtil.sqlSelect(u"empresa INNER JOIN paises ON empresa.codpais = paises.codpais", u"paises.codiso", ustr( u"empresa.cifnif = '" , cifEmpresa , u"'" ), u"empresa,paises")
        if not codPais:
            sys.warnMsgBox(sys.translate(u"No se ha podido obtener el código ISO del país asociado a la empresa"))
            return False
        codComercial = AQUtil.sqlSelect(u"cuentasbanco", u"sufijo", ustr( u"codcuenta = '" , codCuenta , u"'" ))
        numControl = u""
        cifEmpresa = cifEmpresa.toUpperCase()
        carValido = u"1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        i = 0
        while_pass = True
        while i < len(cifEmpresa):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            if carValido.find(cifEmpresa[i]) >= 0:
                numControl += cifEmpresa[i]
            i += 1
            while_pass = True
            try:
                i < len(cifEmpresa)
            except: break
        
        digControl = _i.digitoControlMod97(numControl, codPais)
        identificador = codPais + digControl + codComercial + cifEmpresa
        return identificador
    
    def envioMail_componerListaDestinatarios(self, codigo = None, tabla = None):
        debug(tabla)
        util = qsatype.FLUtil()
        arrayMails = qsatype.Array()
        listaDestinatarios = ""
        emailPrincipal = ""
        nombrePrincipal = ""
        dialog = None
        q = qsatype.FLSqlQuery()
        s15_when = tabla
        s15_do_work,s15_work_done = False,False
        if s15_when == u"clientes": s15_do_work,s15_work_done = True,True
        if s15_do_work:
            emailPrincipal = util.sqlSelect(u"clientes", u"email", ustr( u"codcliente = '" , codigo , u"'" ))
            nombrePrincipal = util.sqlSelect(u"clientes", u"nombre", ustr( u"codcliente = '" , codigo , u"'" ))
            q.setTablesList(u"contactosclientes,crm_contactos")
            q.setFrom(u"contactosclientes INNER JOIN crm_contactos ON contactosclientes.codcontacto = crm_contactos.codcontacto")
            q.setSelect(u"crm_contactos.email,crm_contactos.nombre")
            q.setWhere(ustr( u"contactosclientes.codcliente = '" , codigo , u"' AND (crm_contactos.email <> '' AND crm_contactos.email IS NOT NULL)" ))
            if not q.exec_():
                return False
            dialog = qsatype.Dialog(util.translate(u"scripts", u"Contactos del cliente"), 0)
            s15_do_work = False # BREAK
        
        if s15_when == u"proveedores": s15_do_work,s15_work_done = True,True
        if s15_do_work:
            emailPrincipal = util.sqlSelect(u"proveedores", u"email", ustr( u"codproveedor = '" , codigo , u"'" ))
            nombrePrincipal = util.sqlSelect(u"proveedores", u"nombre", ustr( u"codproveedor = '" , codigo , u"'" ))
            q.setTablesList(u"contactosproveedores,crm_contactos")
            q.setFrom(u"contactosproveedores INNER JOIN crm_contactos ON contactosproveedores.codcontacto = crm_contactos.codcontacto")
            q.setSelect(u"crm_contactos.email,crm_contactos.nombre")
            q.setWhere(ustr( u"contactosproveedores.codproveedor = '" , codigo , u"' AND (crm_contactos.email <> '' AND crm_contactos.email IS NOT NULL)" ))
            if not q.exec_():
                return False
            dialog = qsatype.Dialog(util.translate(u"scripts", u"Contactos del proveedor"), 0)
            s15_do_work = False # BREAK
        
        debug(ustr( u"emailPrincipal " , emailPrincipal ))
        dialog.caption = u"Selecciona el destinatario"
        dialog.OKButtonText = util.translate(u"scripts", u"Aceptar")
        dialog.cancelButtonText = util.translate(u"scripts", u"Cancelar")
        bgroup = qsatype.GroupBox()
        dialog.add(bgroup)
        cB = qsatype.Array()
        nEmails = 0
        cB[nEmails] = qsatype.CheckBox()
        cB[nEmails].text = util.translate(u"scripts", ustr( nombrePrincipal , u" (" , emailPrincipal , u")" ))
        arrayMails[nEmails] = emailPrincipal
        cB[nEmails].checked = True
        bgroup.add(cB[nEmails])
        nEmails += 1
        while q.next():
            cB[nEmails] = qsatype.CheckBox()
            cB[nEmails].text = util.translate(u"scripts", ustr( q.value(1) , u" (" , q.value(0) , u")" ))
            arrayMails[nEmails] = q.value(0)
            cB[nEmails].checked = False
            bgroup.add(cB[nEmails])
            nEmails += 1
        
        debug(ustr( u"nEmails " , nEmails ))
        if nEmails > 1:
            nEmails -= 1
            lista = u""
            if dialog.exec_():
                i = 0
                while_pass = True
                while i <= nEmails:
                    if not while_pass:
                        i += 1
                        while_pass = True
                        continue
                    while_pass = False
                    if cB[i].checked == True:
                        debug(ustr( u"arrayMails[i] " , arrayMails[i] ))
                        lista += ustr( arrayMails[i] , u"," )
                    i += 1
                    while_pass = True
                    try:
                        i <= nEmails
                    except: break
            
            else:
                return 
            
            lista = lista[0:len(lista) - 1]
            if lista == u"":
                return 
            listaDestinatarios = lista
        
        else:
            listaDestinatarios = emailPrincipal
        
        debug(ustr( u"listaDestinatarios " , listaDestinatarios ))
        return listaDestinatarios
    
    def envioMail_enviarCorreo(self, cuerpo = None, asunto = None, arrayDest = None, arrayAttach = None):
        util = qsatype.FLUtil()
        comando = self.iface.componerCorreo(cuerpo, asunto, arrayDest, arrayAttach)
        if not comando:
            return False
        res = self.iface.ejecutarComandoAsincrono(comando)
        return True
    
    def envioMail_componerCorreo(self, cuerpo = None, asunto = None, arrayDest = None, arrayAttach = None):
        util = qsatype.FLUtil()
        clienteCorreo = util.readSettingEntry(u"scripts/flfactinfo/clientecorreo")
        if not clienteCorreo or clienteCorreo == u"":
            MessageBox.warning(util.translate(u"scripts", u"No tiene establecido el tipo de cliente de correo.\nDebe establecer este valor en la pestaÃ±a Correo del formulario de empresa"), MessageBox.Ok, MessageBox.NoButton)
            return False
        nombreCorreo = util.readSettingEntry(u"scripts/flfactinfo/nombrecorreo")
        if not nombreCorreo or nombreCorreo == u"":
            MessageBox.warning(util.translate(u"scripts", u"No tiene establecido el nombre del ejecutable del programa de correo.\nDebe establecer este valor en la pestaÃ±a Correo del formulario de empresa"), MessageBox.Ok, MessageBox.NoButton)
            return False
        destinatarios = u""
        i = 0
        while_pass = True
        while i < len(arrayDest):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            if i > 0:
                destinatarios += u" "
            destinatarios += arrayDest[i][u"direccion"]
            i += 1
            while_pass = True
            try:
                i < len(arrayDest)
            except: break
        
        documentos = u""
        if arrayAttach:
            documentos = arrayAttach.join(u" ")
        comando = qsatype.Array()
        sc1_when = clienteCorreo
        sc1_do_work,sc1_work_done = False,False
        if sc1_when == u"Thunderbird": sc1_do_work,sc1_work_done = True,True
        if sc1_do_work:
            if documentos != u"":
                comando = qsatype.Array([nombreCorreo, u"-compose", ustr( u"to='" , destinatarios , u"',subject=" ), asunto, u",body=", cuerpo, ustr( u",attachment=file://" , documentos )])
            else:
                comando = qsatype.Array([nombreCorreo, u"-compose", ustr( u"to='" , destinatarios , u"',subject=" ), asunto, u",body=", cuerpo])
            
            sc1_do_work = False # BREAK
        
        if sc1_when == u"Outlook": sc1_do_work,sc1_work_done = True,True
        if sc1_do_work:
            if documentos != u"":
                documentos = qsatype.Dir.convertSeparators(documentos)
                comando = qsatype.Array([ustr( u"\"" , nombreCorreo , u"\" /c" ), u"ipm.note", u"/m", destinatarios, u"/a", documentos])
            else:
                comando = qsatype.Array([ustr( u"\"" , nombreCorreo , u"\" /c" ), u"ipm.note", u"/m", destinatarios])
            
            sc1_do_work = False # BREAK
        
        if sc1_when == u"KMail": sc1_do_work,sc1_work_done = True,True
        if sc1_do_work:
            if documentos != u"":
                comando = qsatype.Array([nombreCorreo, destinatarios, u"-s", asunto, u"--body", cuerpo, documentos])
            else:
                comando = qsatype.Array([nombreCorreo, destinatarios, u"-s", asunto, u"--body", cuerpo])
            
            sc1_do_work = False # BREAK
        
        if not sc1_work_done: sc1_do_work,sc1_work_done = True,True
        if sc1_do_work:
            pass
        return comando
    
    def envioMail_existeEnvioMail(self):
        return True
    
    def dtoEsp_calcularLiquidacionAgente(self, codLiquidacion = None):
        util = qsatype.FLUtil()
        qryFacturas = qsatype.FLSqlQuery()
        qryFacturas.setTablesList(u"facturascli,lineasfacturascli")
        qryFacturas.setSelect(u"coddivisa, tasaconv, facturascli.porcomision, lineasfacturascli.porcomision, neto, facturascli.idfactura, lineasfacturascli.pvptotal, facturascli.pordtoesp")
        qryFacturas.setFrom(u"facturascli INNER JOIN lineasfacturascli ON facturascli.idfactura = lineasfacturascli.idfactura")
        qryFacturas.setWhere(ustr( u"codliquidacion = '" , codLiquidacion , u"'" ))
        if not qryFacturas.exec_():
            return False
        total = 0
        comision = 0
        descuento = 0
        tasaconv = 0
        divisaEmpresa = util.sqlSelect(u"empresa", u"coddivisa", u"1=1")
        idfactura = 0
        comisionFactura = False
        while qryFacturas.next():
            if not idfactura or idfactura != qryFacturas.value(u"facturascli.idfactura"):
                idfactura = qryFacturas.value(u"facturascli.idfactura")
                if parseFloat(qryFacturas.value(u"facturascli.porcomision")):
                    comisionFactura = True
                    comision = parseFloat(qryFacturas.value(u"facturascli.porcomision")) * parseFloat(qryFacturas.value(u"neto")) / 100
                    tasaconv = parseFloat(qryFacturas.value(u"tasaconv"))
                    if qryFacturas.value(u"coddivisa") == divisaEmpresa:
                        total += comision
                    else:
                        total += comision * tasaconv
                    
                
                else:
                    comisionFactura = False
                
            
            if not comisionFactura:
                descuento = parseFloat(qryFacturas.value(u"facturascli.pordtoesp"))
                descuento = ( ( 0 if isNaN(descuento) else descuento ) )
                comision = parseFloat(qryFacturas.value(u"lineasfacturascli.porcomision")) * parseFloat(qryFacturas.value(u"lineasfacturascli.pvptotal") * ( 100 - descuento ) / 100) / 100
                tasaconv = parseFloat(qryFacturas.value(u"tasaconv"))
                if qryFacturas.value(u"coddivisa") == divisaEmpresa:
                    total += comision
                else:
                    total += comision * tasaconv
                
        
        return total
    


form = None
