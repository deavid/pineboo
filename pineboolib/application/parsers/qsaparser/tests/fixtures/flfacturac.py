# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING
from pineboolib.qsa import qsa

# /** @file */


# /** @class_declaration interna */
class interna(object):
    ctx = qsa.Object()

    def __init__(self, context=None):
        self.ctx = context

    def beforeCommit_presupuestoscli(self, curPresupuesto=None):
        return self.ctx.interna_beforeCommit_presupuestoscli(curPresupuesto)

    def beforeCommit_pedidoscli(self, curPedido=None):
        return self.ctx.interna_beforeCommit_pedidoscli(curPedido)

    def beforeCommit_pedidosprov(self, curPedido=None):
        return self.ctx.interna_beforeCommit_pedidosprov(curPedido)

    def beforeCommit_albaranescli(self, curAlbaran=None):
        return self.ctx.interna_beforeCommit_albaranescli(curAlbaran)

    def beforeCommit_albaranesprov(self, curAlbaran=None):
        return self.ctx.interna_beforeCommit_albaranesprov(curAlbaran)

    def beforeCommit_facturascli(self, curFactura=None):
        return self.ctx.interna_beforeCommit_facturascli(curFactura)

    def beforeCommit_facturasprov(self, curFactura=None):
        return self.ctx.interna_beforeCommit_facturasprov(curFactura)

    def afterCommit_pedidoscli(self, curPedido=None):
        return self.ctx.interna_afterCommit_pedidoscli(curPedido)

    def afterCommit_albaranescli(self, curAlbaran=None):
        return self.ctx.interna_afterCommit_albaranescli(curAlbaran)

    def afterCommit_albaranesprov(self, curAlbaran=None):
        return self.ctx.interna_afterCommit_albaranesprov(curAlbaran)

    def afterCommit_facturascli(self, curFactura=None):
        return self.ctx.interna_afterCommit_facturascli(curFactura)

    def afterCommit_facturasprov(self, curFactura=None):
        return self.ctx.interna_afterCommit_facturasprov(curFactura)

    def afterCommit_lineasalbaranesprov(self, curLA=None):
        return self.ctx.interna_afterCommit_lineasalbaranesprov(curLA)

    def afterCommit_lineasfacturasprov(self, curLF=None):
        return self.ctx.interna_afterCommit_lineasfacturasprov(curLF)

    def afterCommit_lineaspedidoscli(self, curLA=None):
        return self.ctx.interna_afterCommit_lineaspedidoscli(curLA)

    def afterCommit_lineaspedidosprov(self, curLA=None):
        return self.ctx.interna_afterCommit_lineaspedidosprov(curLA)

    def afterCommit_lineasalbaranescli(self, curLA=None):
        return self.ctx.interna_afterCommit_lineasalbaranescli(curLA)

    def afterCommit_lineasfacturascli(self, curLF=None):
        return self.ctx.interna_afterCommit_lineasfacturascli(curLF)


# /** @class_declaration oficial */
class oficial(interna):
    curAsiento_ = None

    def __init__(self, context=None):
        super(oficial, self).__init__(context)

    def obtenerHueco(self, codSerie=None, codEjercicio=None, tipo=None):
        return self.ctx.oficial_obtenerHueco(codSerie, codEjercicio, tipo)

    def establecerNumeroSecuencia(self, fN=None, value=None):
        return self.ctx.oficial_establecerNumeroSecuencia(fN, value)

    def cerosIzquierda(self, numero=None, totalCifras=None):
        return self.ctx.oficial_cerosIzquierda(numero, totalCifras)

    def construirCodigo(self, codSerie=None, codEjercicio=None, numero=None):
        return self.ctx.oficial_construirCodigo(codSerie, codEjercicio, numero)

    def siguienteNumero(self, codSerie=None, codEjercicio=None, fN=None):
        return self.ctx.oficial_siguienteNumero(codSerie, codEjercicio, fN)

    def agregarHueco(self, serie=None, ejercicio=None, numero=None, fN=None):
        return self.ctx.oficial_agregarHueco(serie, ejercicio, numero, fN)

    def asientoBorrable(self, idAsiento=None):
        return self.ctx.oficial_asientoBorrable(idAsiento)

    def generarAsientoFacturaCli(self, curFactura=None):
        return self.ctx.oficial_generarAsientoFacturaCli(curFactura)

    def generarPartidasVenta(self, curFactura=None, idAsiento=None, valoresDefecto=None):
        return self.ctx.oficial_generarPartidasVenta(curFactura, idAsiento, valoresDefecto)

    def generarPartidasIVACli(self, curFactura=None, idAsiento=None, valoresDefecto=None, ctaCliente=None):
        return self.ctx.oficial_generarPartidasIVACli(curFactura, idAsiento, valoresDefecto, ctaCliente)

    def generarPartidasIRPF(self, curFactura=None, idAsiento=None, valoresDefecto=None):
        return self.ctx.oficial_generarPartidasIRPF(curFactura, idAsiento, valoresDefecto)

    def generarPartidasRecFinCli(self, curFactura=None, idAsiento=None, valoresDefecto=None):
        return self.ctx.oficial_generarPartidasRecFinCli(curFactura, idAsiento, valoresDefecto)

    def generarPartidasIRPFProv(self, curFactura=None, idAsiento=None, valoresDefecto=None):
        return self.ctx.oficial_generarPartidasIRPFProv(curFactura, idAsiento, valoresDefecto)

    def generarPartidasRecFinProv(self, curFactura=None, idAsiento=None, valoresDefecto=None):
        return self.ctx.oficial_generarPartidasRecFinProv(curFactura, idAsiento, valoresDefecto)

    def generarPartidasCliente(self, curFactura=None, idAsiento=None, valoresDefecto=None, ctaCliente=None):
        return self.ctx.oficial_generarPartidasCliente(curFactura, idAsiento, valoresDefecto, ctaCliente)

    def regenerarAsiento(self, cur=None, valoresDefecto=None):
        return self.ctx.oficial_regenerarAsiento(cur, valoresDefecto)

    def datosAsientoRegenerado(self, cur=None, valoresDefecto=None):
        return self.ctx.oficial_datosAsientoRegenerado(cur, valoresDefecto)

    def generarAsientoFacturaProv(self, curFactura=None):
        return self.ctx.oficial_generarAsientoFacturaProv(curFactura)

    def generarPartidasCompra(self, curFactura=None, idAsiento=None, valoresDefecto=None, concepto=None):
        return self.ctx.oficial_generarPartidasCompra(curFactura, idAsiento, valoresDefecto, concepto)

    def generarPartidasIVAProv(
        self, curFactura=None, idAsiento=None, valoresDefecto=None, ctaProveedor=None, concepto=None
    ):
        return self.ctx.oficial_generarPartidasIVAProv(curFactura, idAsiento, valoresDefecto, ctaProveedor, concepto)

    def generarPartidasProveedor(
        self, curFactura=None, idAsiento=None, valoresDefecto=None, ctaProveedor=None, concepto=None, sinIVA=None
    ):
        return self.ctx.oficial_generarPartidasProveedor(
            curFactura, idAsiento, valoresDefecto, ctaProveedor, concepto, sinIVA
        )

    def datosCtaEspecial(self, ctaEsp=None, codEjercicio=None):
        return self.ctx.oficial_datosCtaEspecial(ctaEsp, codEjercicio)

    def datosCtaIVA(self, tipo=None, codEjercicio=None, codImpuesto=None):
        return self.ctx.oficial_datosCtaIVA(tipo, codEjercicio, codImpuesto)

    def datosCtaVentas(self, codEjercicio=None, codSerie=None):
        return self.ctx.oficial_datosCtaVentas(codEjercicio, codSerie)

    def datosCtaCliente(self, curFactura=None, valoresDefecto=None):
        return self.ctx.oficial_datosCtaCliente(curFactura, valoresDefecto)

    def datosCtaProveedor(self, curFactura=None, valoresDefecto=None):
        return self.ctx.oficial_datosCtaProveedor(curFactura, valoresDefecto)

    def asientoFacturaAbonoCli(self, curFactura=None, valoresDefecto=None):
        return self.ctx.oficial_asientoFacturaAbonoCli(curFactura, valoresDefecto)

    def asientoFacturaAbonoProv(self, curFactura=None, valoresDefecto=None):
        return self.ctx.oficial_asientoFacturaAbonoProv(curFactura, valoresDefecto)

    def datosDocFacturacion(self, fecha=None, codEjercicio=None, tipoDoc=None):
        return self.ctx.oficial_datosDocFacturacion(fecha, codEjercicio, tipoDoc)

    def tieneIvaDocCliente(self, codSerie=None, codCliente=None, codEjercicio=None):
        return self.ctx.oficial_tieneIvaDocCliente(codSerie, codCliente, codEjercicio)

    def tieneIvaDocProveedor(self, codSerie=None, codProveedor=None, codEjercicio=None):
        return self.ctx.oficial_tieneIvaDocProveedor(codSerie, codProveedor, codEjercicio)

    def automataActivado(self):
        return self.ctx.oficial_automataActivado()

    def comprobarRegularizacion(self, curFactura=None):
        return self.ctx.oficial_comprobarRegularizacion(curFactura)

    def recalcularHuecos(self, serie=None, ejercicio=None, fN=None):
        return self.ctx.oficial_recalcularHuecos(serie, ejercicio, fN)

    def mostrarTraza(self, codigo=None, tipo=None):
        return self.ctx.oficial_mostrarTraza(codigo, tipo)

    def datosPartidaFactura(self, curPartida=None, curFactura=None, tipo=None, concepto=None):
        return self.ctx.oficial_datosPartidaFactura(curPartida, curFactura, tipo, concepto)

    def eliminarAsiento(self, idAsiento=None):
        return self.ctx.oficial_eliminarAsiento(idAsiento)

    def siGenerarRecibosCli(self, curFactura=None, masCampos=None):
        return self.ctx.oficial_siGenerarRecibosCli(curFactura, masCampos)

    def validarIvaRecargoCliente(self, codCliente=None, id=None, tabla=None, identificador=None):
        return self.ctx.oficial_validarIvaRecargoCliente(codCliente, id, tabla, identificador)

    def validarIvaRecargoProveedor(self, codProveedor=None, id=None, tabla=None, identificador=None):
        return self.ctx.oficial_validarIvaRecargoProveedor(codProveedor, id, tabla, identificador)

    def comprobarFacturaAbonoCli(self, curFactura=None):
        return self.ctx.oficial_comprobarFacturaAbonoCli(curFactura)

    def consultarCtaEspecial(self, ctaEsp=None, codEjercicio=None):
        return self.ctx.oficial_consultarCtaEspecial(ctaEsp, codEjercicio)

    def crearCtaEspecial(self, codCtaEspecial=None, tipo=None, codEjercicio=None, desCta=None):
        return self.ctx.oficial_crearCtaEspecial(codCtaEspecial, tipo, codEjercicio, desCta)

    def comprobarCambioSerie(self, cursor=None):
        return self.ctx.oficial_comprobarCambioSerie(cursor)

    def netoVentasFacturaCli(self, curFactura=None):
        return self.ctx.oficial_netoVentasFacturaCli(curFactura)

    def netoComprasFacturaProv(self, curFactura=None):
        return self.ctx.oficial_netoComprasFacturaProv(curFactura)

    def datosConceptoAsiento(self, cur=None):
        return self.ctx.oficial_datosConceptoAsiento(cur)

    def subcuentaVentas(self, referencia=None, codEjercicio=None):
        return self.ctx.oficial_subcuentaVentas(referencia, codEjercicio)

    def regimenIVACliente(self, curDocCliente=None):
        return self.ctx.oficial_regimenIVACliente(curDocCliente)

    def restarCantidadCli(self, idLineaPedido=None, idLineaAlbaran=None):
        return self.ctx.oficial_restarCantidadCli(idLineaPedido, idLineaAlbaran)

    def restarCantidadProv(self, idLineaPedido=None, idLineaAlbaran=None):
        return self.ctx.oficial_restarCantidadProv(idLineaPedido, idLineaAlbaran)

    def actualizarPedidosCli(self, curAlbaran=None):
        return self.ctx.oficial_actualizarPedidosCli(curAlbaran)

    def actualizarPedidosProv(self, curAlbaran=None):
        return self.ctx.oficial_actualizarPedidosProv(curAlbaran)

    def actualizarLineaPedidoProv(
        self, idLineaPedido=None, idPedido=None, referencia=None, idAlbaran=None, cantidadLineaAlbaran=None
    ):
        return self.ctx.oficial_actualizarLineaPedidoProv(
            idLineaPedido, idPedido, referencia, idAlbaran, cantidadLineaAlbaran
        )

    def actualizarEstadoPedidoProv(self, idPedido=None, curAlbaran=None):
        return self.ctx.oficial_actualizarEstadoPedidoProv(idPedido, curAlbaran)

    def obtenerEstadoPedidoProv(self, idPedido=None):
        return self.ctx.oficial_obtenerEstadoPedidoProv(idPedido)

    def actualizarLineaPedidoCli(
        self, idLineaPedido=None, idPedido=None, referencia=None, idAlbaran=None, cantidadLineaAlbaran=None
    ):
        return self.ctx.oficial_actualizarLineaPedidoCli(
            idLineaPedido, idPedido, referencia, idAlbaran, cantidadLineaAlbaran
        )

    def actualizarEstadoPedidoCli(self, idPedido=None, curAlbaran=None):
        return self.ctx.oficial_actualizarEstadoPedidoCli(idPedido, curAlbaran)

    def obtenerEstadoPedidoCli(self, idPedido=None):
        return self.ctx.oficial_obtenerEstadoPedidoCli(idPedido)

    def liberarAlbaranesCli(self, idFactura=None):
        return self.ctx.oficial_liberarAlbaranesCli(idFactura)

    def liberarAlbaranCli(self, idAlbaran=None):
        return self.ctx.oficial_liberarAlbaranCli(idAlbaran)

    def liberarAlbaranesProv(self, idFactura=None):
        return self.ctx.oficial_liberarAlbaranesProv(idFactura)

    def liberarAlbaranProv(self, idAlbaran=None):
        return self.ctx.oficial_liberarAlbaranProv(idAlbaran)

    def liberarPresupuestoCli(self, idPresupuesto=None):
        return self.ctx.oficial_liberarPresupuestoCli(idPresupuesto)

    def actualizarPedidosLineaAlbaranCli(self, curLA=None):
        return self.ctx.oficial_actualizarPedidosLineaAlbaranCli(curLA)

    def actualizarPedidosLineaAlbaranProv(self, curLA=None):
        return self.ctx.oficial_actualizarPedidosLineaAlbaranProv(curLA)

    def aplicarComisionLineas(self, codAgente=None, tblHija=None, where=None):
        return self.ctx.oficial_aplicarComisionLineas(codAgente, tblHija, where)

    def calcularComisionLinea(self, codAgente=None, referencia=None):
        return self.ctx.oficial_calcularComisionLinea(codAgente, referencia)

    def arrayCostesAfectados(self, arrayInicial=None, arrayFinal=None):
        return self.ctx.oficial_arrayCostesAfectados(arrayInicial, arrayFinal)

    def compararArrayCoste(self, a=None, b=None):
        return self.ctx.oficial_compararArrayCoste(a, b)

    def esSubcuentaEspecial(self, codSubcuenta=None, codEjercicio=None, idTipoEsp=None):
        return self.ctx.oficial_esSubcuentaEspecial(codSubcuenta, codEjercicio, idTipoEsp)

    def campoImpuesto(self, campo=None, codImpuesto=None, fecha=None):
        return self.ctx.oficial_campoImpuesto(campo, codImpuesto, fecha)

    def datosImpuesto(self, codImpuesto=None, fecha=None):
        return self.ctx.oficial_datosImpuesto(codImpuesto, fecha)

    def valorDefecto(self, fN=None):
        return self.ctx.oficial_valorDefecto(fN)

    def formateaCadena(self, cIn=None):
        return self.ctx.oficial_formateaCadena(cIn)


# /** @class_declaration head */
class head(oficial):
    def __init__(self, context=None):
        super(head, self).__init__(context)


# /** @class_declaration ifaceCtx */
class ifaceCtx(head):
    def __init__(self, context=None):
        super(ifaceCtx, self).__init__(context)

    def pub_cerosIzquierda(self, numero=None, totalCifras=None):
        return self.cerosIzquierda(numero, totalCifras)

    def pub_asientoBorrable(self, idAsiento=None):
        return self.asientoBorrable(idAsiento)

    def pub_regenerarAsiento(self, cur=None, valoresDefecto=None):
        return self.regenerarAsiento(cur, valoresDefecto)

    def pub_datosCtaEspecial(self, ctaEsp=None, codEjercicio=None):
        return self.datosCtaEspecial(ctaEsp, codEjercicio)

    def pub_siguienteNumero(self, codSerie=None, codEjercicio=None, fN=None):
        return self.siguienteNumero(codSerie, codEjercicio, fN)

    def pub_construirCodigo(self, codSerie=None, codEjercicio=None, numero=None):
        return self.construirCodigo(codSerie, codEjercicio, numero)

    def pub_agregarHueco(self, serie=None, ejercicio=None, numero=None, fN=None):
        return self.agregarHueco(serie, ejercicio, numero, fN)

    def pub_datosDocFacturacion(self, fecha=None, codEjercicio=None, tipoDoc=None):
        return self.datosDocFacturacion(fecha, codEjercicio, tipoDoc)

    def pub_tieneIvaDocCliente(self, codSerie=None, codCliente=None, codEjercicio=None):
        return self.tieneIvaDocCliente(codSerie, codCliente, codEjercicio)

    def pub_tieneIvaDocProveedor(self, codSerie=None, codProveedor=None, codEjercicio=None):
        return self.tieneIvaDocProveedor(codSerie, codProveedor, codEjercicio)

    def pub_automataActivado(self):
        return self.automataActivado()

    def pub_generarAsientoFacturaCli(self, curFactura=None):
        return self.generarAsientoFacturaCli(curFactura)

    def pub_generarAsientoFacturaProv(self, curFactura=None):
        return self.generarAsientoFacturaProv(curFactura)

    def pub_mostrarTraza(self, codigo=None, tipo=None):
        return self.mostrarTraza(codigo, tipo)

    def pub_eliminarAsiento(self, idAsiento=None):
        return self.eliminarAsiento(idAsiento)

    def pub_validarIvaRecargoCliente(self, codCliente=None, id=None, tabla=None, identificador=None):
        return self.validarIvaRecargoCliente(codCliente, id, tabla, identificador)

    def pub_validarIvaRecargoProveedor(self, codProveedor=None, id=None, tabla=None, identificador=None):
        return self.validarIvaRecargoProveedor(codProveedor, id, tabla, identificador)

    def pub_subcuentaVentas(self, referencia=None, codEjercicio=None):
        return self.subcuentaVentas(referencia, codEjercicio)

    def pub_regimenIVACliente(self, curDocCliente=None):
        return self.regimenIVACliente(curDocCliente)

    def pub_actualizarEstadoPedidoCli(self, idPedido=None, curAlbaran=None):
        return self.actualizarEstadoPedidoCli(idPedido, curAlbaran)

    def pub_actualizarEstadoPedidoProv(self, idPedido=None, curAlbaran=None):
        return self.actualizarEstadoPedidoProv(idPedido, curAlbaran)

    def pub_aplicarComisionLineas(self, codAgente=None, tblHija=None, where=None):
        return self.aplicarComisionLineas(codAgente, tblHija, where)

    def pub_calcularComisionLinea(self, codAgente=None, referencia=None):
        return self.calcularComisionLinea(codAgente, referencia)

    def pub_arrayCostesAfectados(self, arrayInicial=None, arrayFinal=None):
        return self.arrayCostesAfectados(arrayInicial, arrayFinal)

    def pub_campoImpuesto(self, campo=None, codImpuesto=None, fecha=None):
        return self.campoImpuesto(campo, codImpuesto, fecha)

    def pub_datosImpuesto(self, codImpuesto=None, fecha=None):
        return self.datosImpuesto(codImpuesto, fecha)

    def pub_formateaCadena(self, cIn=None):
        return self.formateaCadena(cIn)


# /** @class_declaration FormInternalObj */
class FormInternalObj(qsa.FormDBWidget):
    iface: ifaceCtx

    # /** @class_definition FormInternalObj */
    def _class_init(self):
        self.iface = ifaceCtx(self)

    # /** @class_definition interna */
    def interna_beforeCommit_pedidoscli(self, curPedido=None):
        util = qsa.FLUtil()
        numero = ""
        for case in qsa.switch(curPedido.modeAccess()):
            if case(curPedido.Insert):
                if not qsa.from_project("flfactppal").iface.pub_clienteActivo(
                    curPedido.valueBuffer("codcliente"), curPedido.valueBuffer("fecha")
                ):
                    return False
                if curPedido.valueBuffer("numero") == 0:
                    numero = self.iface.siguienteNumero(
                        curPedido.valueBuffer("codserie"), curPedido.valueBuffer("codejercicio"), "npedidocli"
                    )
                    if not numero:
                        return False
                    curPedido.setValueBuffer("numero", numero)
                    curPedido.setValueBuffer(
                        "codigo", qsa.from_project("formpedidoscli").iface.pub_commonCalculateField("codigo", curPedido)
                    )

                break

            if case(curPedido.Edit):
                if not self.iface.comprobarCambioSerie(curPedido):
                    return False
                if not qsa.from_project("flfactppal").iface.pub_clienteActivo(
                    curPedido.valueBuffer("codcliente"), curPedido.valueBuffer("fecha")
                ):
                    return False
                if curPedido.valueBuffer("servido") == "Parcial":
                    estado = self.iface.obtenerEstadoPedidoCli(curPedido.valueBuffer("idpedido"))
                    if estado == "Sí":
                        curPedido.setValueBuffer("servido", estado)
                        curPedido.setValueBuffer("editable", False)

                break

            if case(curPedido.Del):
                if curPedido.valueBuffer("servido") == "Parcial":
                    qsa.MessageBox.warning(
                        util.translate(
                            "scripts",
                            "No se puede eliminar un pedido servido parcialmente.\nDebe borrar antes el albarán relacionado.",
                        ),
                        qsa.MessageBox.Ok,
                        qsa.MessageBox.NoButton,
                        qsa.MessageBox.NoButton,
                    )
                    return False
                break

        return True

    def interna_beforeCommit_lineasalbaranescli(self, curLinea=None):
        util = qsa.FLUtil()
        for case in qsa.switch(curLinea.modeAccess()):
            if case(curLinea.Del):
                break
        return True

    def interna_beforeCommit_pedidosprov(self, curPedido=None):
        util = qsa.FLUtil()
        numero = ""
        for case in qsa.switch(curPedido.modeAccess()):
            if case(curPedido.Insert):
                if curPedido.valueBuffer("numero") == 0:
                    numero = self.iface.siguienteNumero(
                        curPedido.valueBuffer("codserie"), curPedido.valueBuffer("codejercicio"), "npedidoprov"
                    )
                    if not numero:
                        return False
                    curPedido.setValueBuffer("numero", numero)
                    curPedido.setValueBuffer(
                        "codigo",
                        qsa.from_project("formpedidosprov").iface.pub_commonCalculateField("codigo", curPedido),
                    )

                break

            if case(curPedido.Edit):
                if not self.iface.comprobarCambioSerie(curPedido):
                    return False
                if curPedido.valueBuffer("servido") == "Parcial":
                    estado = self.iface.obtenerEstadoPedidoProv(curPedido.valueBuffer("idpedido"))
                    if estado == "Sí":
                        curPedido.setValueBuffer("servido", estado)
                        curPedido.setValueBuffer("editable", False)
                        if qsa.sys.isLoadedModule("flcolaproc"):
                            if not qsa.from_project("flfactppal").iface.pub_lanzarEvento(
                                curPedido, "pedidoProvAlbaranado"
                            ):
                                return False

                break

            if case(curPedido.Del):
                if curPedido.valueBuffer("servido") == "Parcial":
                    qsa.MessageBox.warning(
                        util.translate(
                            "scripts",
                            "No se puede eliminar un pedido servido parcialmente.\nDebe borrar antes el albarán relacionado.",
                        ),
                        qsa.MessageBox.Ok,
                        qsa.MessageBox.NoButton,
                        qsa.MessageBox.NoButton,
                    )
                    return False
                break

        return True

    def interna_beforeCommit_facturascli(self, curFactura=None):
        util = qsa.FLUtil()
        numero = ""
        if curFactura.modeAccess() == curFactura.Insert or curFactura.modeAccess() == curFactura.Edit:
            if not self.iface.comprobarFacturaAbonoCli(curFactura):
                return False
        for case in qsa.switch(curFactura.modeAccess()):
            if case(curFactura.Insert):
                if not qsa.from_project("flfactppal").iface.pub_clienteActivo(
                    curFactura.valueBuffer("codcliente"), curFactura.valueBuffer("fecha")
                ):
                    return False
                if curFactura.valueBuffer("numero") == 0:
                    self.iface.recalcularHuecos(
                        curFactura.valueBuffer("codserie"), curFactura.valueBuffer("codejercicio"), "nfacturacli"
                    )
                    numero = self.iface.siguienteNumero(
                        curFactura.valueBuffer("codserie"), curFactura.valueBuffer("codejercicio"), "nfacturacli"
                    )
                    if not numero:
                        return False
                    curFactura.setValueBuffer("numero", numero)
                    curFactura.setValueBuffer(
                        "codigo",
                        qsa.from_project("formfacturascli").iface.pub_commonCalculateField("codigo", curFactura),
                    )

                break

            if case(curFactura.Edit):
                if not self.iface.comprobarCambioSerie(curFactura):
                    return False
                if not qsa.from_project("flfactppal").iface.pub_clienteActivo(
                    curFactura.valueBuffer("codcliente"), curFactura.valueBuffer("fecha")
                ):
                    return False
                break

        if curFactura.modeAccess() == curFactura.Insert or curFactura.modeAccess() == curFactura.Edit:
            if util.sqlSelect(
                "facturascli",
                "idfactura",
                qsa.ustr(
                    "codejercicio = '",
                    curFactura.valueBuffer("codejercicio"),
                    "' AND codserie = '",
                    curFactura.valueBuffer("codserie"),
                    "' AND numero = '",
                    curFactura.valueBuffer("numero"),
                    "' AND idfactura <> ",
                    curFactura.valueBuffer("idfactura"),
                ),
            ):
                numero = self.iface.siguienteNumero(
                    curFactura.valueBuffer("codserie"), curFactura.valueBuffer("codejercicio"), "nfacturacli"
                )
                if not numero:
                    return False
                curFactura.setValueBuffer("numero", numero)
                curFactura.setValueBuffer(
                    "codigo", qsa.from_project("formfacturascli").iface.pub_commonCalculateField("codigo", curFactura)
                )

        if curFactura.modeAccess() == curFactura.Edit:
            if not qsa.from_project("formRecordfacturascli").iface.pub_actualizarLineasIva(curFactura):
                return False
        if curFactura.modeAccess() == curFactura.Insert or curFactura.modeAccess() == curFactura.Edit:
            if qsa.sys.isLoadedModule("flcontppal") and qsa.from_project("flfactppal").iface.pub_valorDefectoEmpresa(
                "contintegrada"
            ):
                if not self.iface.generarAsientoFacturaCli(curFactura):
                    return False
        return True

    def interna_beforeCommit_facturasprov(self, curFactura=None):
        util = qsa.FLUtil()
        numero = ""
        if curFactura.valueBuffer("deabono"):
            if not curFactura.valueBuffer("idfacturarect"):
                qsa.MessageBox.warning(
                    util.translate("scripts", "Debe seleccionar la factura que desea abonar"),
                    qsa.MessageBox.Ok,
                    qsa.MessageBox.NoButton,
                    qsa.MessageBox.NoButton,
                )
                return False
            if util.sqlSelect(
                "facturasprov",
                "idfacturarect",
                qsa.ustr(
                    "idfacturarect = ",
                    curFactura.valueBuffer("idfacturarect"),
                    " AND idfactura <> ",
                    curFactura.valueBuffer("idfactura"),
                ),
            ):
                qsa.MessageBox.warning(
                    util.translate("scripts", "La factura ")
                    + util.sqlSelect(
                        "facturasprov", "codigo", qsa.ustr("idfactura = ", curFactura.valueBuffer("idFacturarect"))
                    )
                    + util.translate("scripts", " ya está abonada"),
                    qsa.MessageBox.Ok,
                    qsa.MessageBox.NoButton,
                )
                return False

        if curFactura.modeAccess() == curFactura.Edit:
            if not self.iface.comprobarCambioSerie(curFactura):
                return False
        if curFactura.modeAccess() == curFactura.Insert:
            if curFactura.valueBuffer("numero") == 0:
                self.iface.recalcularHuecos(
                    curFactura.valueBuffer("codserie"), curFactura.valueBuffer("codejercicio"), "nfacturaprov"
                )
                numero = self.iface.siguienteNumero(
                    curFactura.valueBuffer("codserie"), curFactura.valueBuffer("codejercicio"), "nfacturaprov"
                )
                if not numero:
                    return False
                curFactura.setValueBuffer("numero", numero)
                curFactura.setValueBuffer(
                    "codigo", qsa.from_project("formfacturasprov").iface.pub_commonCalculateField("codigo", curFactura)
                )

        if curFactura.modeAccess() == curFactura.Insert or curFactura.modeAccess() == curFactura.Edit:
            if util.sqlSelect(
                "facturasprov",
                "idfactura",
                qsa.ustr(
                    "codejercicio = '",
                    curFactura.valueBuffer("codejercicio"),
                    "' AND codserie = '",
                    curFactura.valueBuffer("codserie"),
                    "' AND numero = '",
                    curFactura.valueBuffer("numero"),
                    "' AND idfactura <> ",
                    curFactura.valueBuffer("idfactura"),
                ),
            ):
                numero = self.iface.siguienteNumero(
                    curFactura.valueBuffer("codserie"), curFactura.valueBuffer("codejercicio"), "nfacturaprov"
                )
                if not numero:
                    return False
                curFactura.setValueBuffer("numero", numero)
                curFactura.setValueBuffer(
                    "codigo", qsa.from_project("formfacturasprov").iface.pub_commonCalculateField("codigo", curFactura)
                )

        if curFactura.modeAccess() == curFactura.Edit:
            if not qsa.from_project("formRecordfacturasprov").iface.pub_actualizarLineasIva(curFactura):
                return False
        if curFactura.modeAccess() == curFactura.Insert or curFactura.modeAccess() == curFactura.Edit:
            if qsa.sys.isLoadedModule("flcontppal") and qsa.from_project("flfactppal").iface.pub_valorDefectoEmpresa(
                "contintegrada"
            ):
                if not self.iface.generarAsientoFacturaProv(curFactura):
                    return False
        return True

    def interna_beforeCommit_albaranescli(self, curAlbaran=None):
        util = qsa.FLUtil()
        numero = ""
        for case in qsa.switch(curAlbaran.modeAccess()):
            if case(curAlbaran.Insert):
                if not qsa.from_project("flfactppal").iface.pub_clienteActivo(
                    curAlbaran.valueBuffer("codcliente"), curAlbaran.valueBuffer("fecha")
                ):
                    return False
                if curAlbaran.valueBuffer("numero") == 0:
                    numero = self.iface.siguienteNumero(
                        curAlbaran.valueBuffer("codserie"), curAlbaran.valueBuffer("codejercicio"), "nalbarancli"
                    )
                    if not numero:
                        return False
                    curAlbaran.setValueBuffer("numero", numero)
                    curAlbaran.setValueBuffer(
                        "codigo",
                        qsa.from_project("formalbaranescli").iface.pub_commonCalculateField("codigo", curAlbaran),
                    )

                break

            if case(curAlbaran.Edit):
                if not self.iface.comprobarCambioSerie(curAlbaran):
                    return False
                if not qsa.from_project("flfactppal").iface.pub_clienteActivo(
                    curAlbaran.valueBuffer("codcliente"), curAlbaran.valueBuffer("fecha")
                ):
                    return False
                break

            if case(curAlbaran.Del):
                break

        return True

    def interna_afterCommit_albaranescli(self, curAlbaran=None):
        for case in qsa.switch(curAlbaran.modeAccess()):
            if case(curAlbaran.Del):
                break
        return True

    def interna_afterCommit_albaranesprov(self, curAlbaran=None):
        for case in qsa.switch(curAlbaran.modeAccess()):
            if case(curAlbaran.Del):
                break
        return True

    def interna_beforeCommit_albaranesprov(self, curAlbaran=None):
        util = qsa.FLUtil()
        numero = ""
        for case in qsa.switch(curAlbaran.modeAccess()):
            if case(curAlbaran.Insert):
                if curAlbaran.valueBuffer("numero") == 0:
                    numero = self.iface.siguienteNumero(
                        curAlbaran.valueBuffer("codserie"), curAlbaran.valueBuffer("codejercicio"), "nalbaranprov"
                    )
                    if not numero:
                        return False
                    curAlbaran.setValueBuffer("numero", numero)
                    curAlbaran.setValueBuffer(
                        "codigo",
                        qsa.from_project("formalbaranesprov").iface.pub_commonCalculateField("codigo", curAlbaran),
                    )

                break

            if case(curAlbaran.Edit):
                if not self.iface.comprobarCambioSerie(curAlbaran):
                    return False
                break

        return True

    def interna_beforeCommit_presupuestoscli(self, curPresupuesto=None):
        util = qsa.FLUtil()
        numero = ""
        for case in qsa.switch(curPresupuesto.modeAccess()):
            if case(curPresupuesto.Insert):
                if not qsa.from_project("flfactppal").iface.pub_clienteActivo(
                    curPresupuesto.valueBuffer("codcliente"), curPresupuesto.valueBuffer("fecha")
                ):
                    return False
                if curPresupuesto.valueBuffer("numero") == 0:
                    numero = self.iface.siguienteNumero(
                        curPresupuesto.valueBuffer("codserie"),
                        curPresupuesto.valueBuffer("codejercicio"),
                        "npresupuestocli",
                    )
                    if not numero:
                        return False
                    curPresupuesto.setValueBuffer("numero", numero)
                    curPresupuesto.setValueBuffer(
                        "codigo",
                        qsa.from_project("formpresupuestoscli").iface.pub_commonCalculateField(
                            "codigo", curPresupuesto
                        ),
                    )

                break

            if case(curPresupuesto.Edit):
                if not self.iface.comprobarCambioSerie(curPresupuesto):
                    return False
                if not qsa.from_project("flfactppal").iface.pub_clienteActivo(
                    curPresupuesto.valueBuffer("codcliente"), curPresupuesto.valueBuffer("fecha")
                ):
                    return False
                break

        return True

    def interna_afterCommit_pedidoscli(self, curPedido=None):
        for case in qsa.switch(curPedido.modeAccess()):
            if case(curPedido.Del):
                if not self.iface.liberarPresupuestoCli(curPedido.valueBuffer("idpresupuesto")):
                    return False
                break

        return True

    def interna_afterCommit_facturascli(self, curFactura=None):
        for case in qsa.switch(curFactura.modeAccess()):
            if case(curFactura.Del):
                if not self.iface.agregarHueco(
                    curFactura.valueBuffer("codserie"),
                    curFactura.valueBuffer("codejercicio"),
                    curFactura.valueBuffer("numero"),
                    "nfacturacli",
                ):
                    return False
                if not self.iface.liberarAlbaranesCli(curFactura.valueBuffer("idfactura")):
                    return False
                break

        util = qsa.FLUtil()
        if qsa.sys.isLoadedModule("flfactteso") and curFactura.valueBuffer("tpv") == False:
            if curFactura.modeAccess() == curFactura.Insert or curFactura.modeAccess() == curFactura.Edit:
                if self.iface.siGenerarRecibosCli(curFactura):
                    if not qsa.from_project("flfactteso").iface.pub_regenerarRecibosCli(curFactura):
                        return False
            if curFactura.modeAccess() == curFactura.Del:
                qsa.from_project("flfactteso").iface.pub_actualizarRiesgoCliente(curFactura.valueBuffer("codcliente"))

        if qsa.sys.isLoadedModule("flcontppal") and qsa.from_project("flfactppal").iface.pub_valorDefectoEmpresa(
            "contintegrada"
        ):
            for case in qsa.switch(curFactura.modeAccess()):
                if case(curFactura.Edit):
                    if curFactura.valueBuffer("nogenerarasiento"):
                        idAsientoAnterior = curFactura.valueBufferCopy("idasiento")
                        if idAsientoAnterior and idAsientoAnterior != "":
                            if not self.iface.eliminarAsiento(idAsientoAnterior):
                                return False

                    break

                if case(curFactura.Del):
                    if not self.iface.eliminarAsiento(curFactura.valueBuffer("idasiento")):
                        return False
                    break

        return True

    def interna_afterCommit_facturasprov(self, curFactura=None):
        util = qsa.FLUtil()
        if qsa.sys.isLoadedModule("flfactteso"):
            if curFactura.modeAccess() == curFactura.Insert or curFactura.modeAccess() == curFactura.Edit:
                if (
                    curFactura.valueBuffer("total") != curFactura.valueBufferCopy("total")
                    or curFactura.valueBuffer("codproveedor") != curFactura.valueBufferCopy("codproveedor")
                    or curFactura.valueBuffer("codpago") != curFactura.valueBufferCopy("codpago")
                    or curFactura.valueBuffer("fecha") != curFactura.valueBufferCopy("fecha")
                ):
                    if not qsa.from_project("flfactteso").iface.pub_regenerarRecibosProv(curFactura):
                        return False

        for case in qsa.switch(curFactura.modeAccess()):
            if case(curFactura.Del):
                if not self.iface.liberarAlbaranesProv(curFactura.valueBuffer("idfactura")):
                    return False
                break

        if qsa.sys.isLoadedModule("flcontppal") and qsa.from_project("flfactppal").iface.pub_valorDefectoEmpresa(
            "contintegrada"
        ):
            for case in qsa.switch(curFactura.modeAccess()):
                if case(curFactura.Edit):
                    if curFactura.valueBuffer("nogenerarasiento"):
                        idAsientoAnterior = curFactura.valueBufferCopy("idasiento")
                        if idAsientoAnterior and idAsientoAnterior != "":
                            if not self.iface.eliminarAsiento(idAsientoAnterior):
                                return False

                    break

                if case(curFactura.Del):
                    if not self.iface.eliminarAsiento(curFactura.valueBuffer("idasiento")):
                        return False
                    break

        return True

    def interna_afterCommit_lineasalbaranesprov(self, curLA=None):
        if not self.iface.actualizarPedidosLineaAlbaranProv(curLA):
            return False
        if qsa.sys.isLoadedModule("flfactalma"):
            if not qsa.from_project("flfactalma").iface.pub_controlStockAlbaranesProv(curLA):
                return False
        return True

    def interna_afterCommit_lineasfacturasprov(self, curLF=None):
        util = qsa.FLUtil()
        if qsa.sys.isLoadedModule("flfactalma"):
            if not qsa.from_project("flfactalma").iface.pub_controlStockFacturasProv(curLF):
                return False
        return True

    def interna_afterCommit_lineaspedidoscli(self, curLP=None):
        if qsa.sys.isLoadedModule("flfactalma"):
            if not qsa.from_project("flfactalma").iface.pub_controlStockPedidosCli(curLP):
                return False
        return True

    def interna_afterCommit_lineaspedidosprov(self, curLP=None):
        if qsa.sys.isLoadedModule("flfactalma"):
            if not qsa.from_project("flfactalma").iface.pub_controlStockPedidosProv(curLP):
                return False
        return True

    def interna_afterCommit_lineasalbaranescli(self, curLA=None):
        if not self.iface.actualizarPedidosLineaAlbaranCli(curLA):
            return False
        if qsa.sys.isLoadedModule("flfactalma"):
            if not qsa.from_project("flfactalma").iface.pub_controlStockAlbaranesCli(curLA):
                return False
        return True

    def interna_afterCommit_lineasfacturascli(self, curLF=None):
        if qsa.sys.isLoadedModule("flfactalma"):
            if not qsa.from_project("flfactalma").iface.pub_controlStockFacturasCli(curLF):
                return False
        return True

    # /** @class_definition oficial */
    def oficial_actualizarPedidosLineaAlbaranCli(self, curLA=None):
        util = qsa.FLUtil()
        idLineaPedido = qsa.parseFloat(curLA.valueBuffer("idlineapedido"))
        if idLineaPedido == 0:
            return True
        for case in qsa.switch(curLA.modeAccess()):
            if case(curLA.Insert):
                if not self.iface.actualizarLineaPedidoCli(
                    curLA.valueBuffer("idlineapedido"),
                    curLA.valueBuffer("idpedido"),
                    curLA.valueBuffer("referencia"),
                    curLA.valueBuffer("idalbaran"),
                    curLA.valueBuffer("cantidad"),
                ):
                    return False
                if not self.iface.actualizarEstadoPedidoCli(curLA.valueBuffer("idpedido"), curLA):
                    return False
                break

            if case(curLA.Edit):
                if curLA.valueBuffer("cantidad") != curLA.valueBufferCopy("cantidad"):
                    if not self.iface.actualizarLineaPedidoCli(
                        curLA.valueBuffer("idlineapedido"),
                        curLA.valueBuffer("idpedido"),
                        curLA.valueBuffer("referencia"),
                        curLA.valueBuffer("idalbaran"),
                        curLA.valueBuffer("cantidad"),
                    ):
                        return False
                    if not self.iface.actualizarEstadoPedidoCli(curLA.valueBuffer("idpedido"), curLA):
                        return False

                break

            if case(curLA.Del):
                idPedido = curLA.valueBuffer("idpedido")
                idLineaAlbaran = curLA.valueBuffer("idlinea")
                if not self.iface.restarCantidadCli(idLineaPedido, idLineaAlbaran):
                    return False
                self.iface.actualizarEstadoPedidoCli(idPedido)
                break

        return True

    def oficial_actualizarPedidosLineaAlbaranProv(self, curLA=None):
        util = qsa.FLUtil()
        idLineaPedido = qsa.parseFloat(curLA.valueBuffer("idlineapedido"))
        if idLineaPedido == 0:
            return True
        for case in qsa.switch(curLA.modeAccess()):
            if case(curLA.Insert):
                if not self.iface.actualizarLineaPedidoProv(
                    curLA.valueBuffer("idlineapedido"),
                    curLA.valueBuffer("idpedido"),
                    curLA.valueBuffer("referencia"),
                    curLA.valueBuffer("idalbaran"),
                    curLA.valueBuffer("cantidad"),
                ):
                    return False
                if not self.iface.actualizarEstadoPedidoProv(curLA.valueBuffer("idpedido"), curLA):
                    return False
                break

            if case(curLA.Edit):
                if curLA.valueBuffer("cantidad") != curLA.valueBufferCopy("cantidad"):
                    if not self.iface.actualizarLineaPedidoProv(
                        curLA.valueBuffer("idlineapedido"),
                        curLA.valueBuffer("idpedido"),
                        curLA.valueBuffer("referencia"),
                        curLA.valueBuffer("idalbaran"),
                        curLA.valueBuffer("cantidad"),
                    ):
                        return False
                    if not self.iface.actualizarEstadoPedidoProv(curLA.valueBuffer("idpedido"), curLA):
                        return False

                break

            if case(curLA.Del):
                idPedido = curLA.valueBuffer("idpedido")
                idLineaAlbaran = curLA.valueBuffer("idlinea")
                if not self.iface.restarCantidadProv(idLineaPedido, idLineaAlbaran):
                    return False
                self.iface.actualizarEstadoPedidoProv(idPedido)
                break

        return True

    def oficial_obtenerHueco(self, codSerie=None, codEjercicio=None, tipo=None):
        cursorHuecos = qsa.FLSqlCursor("huecos")
        numHueco = 0
        cursorHuecos.select(
            qsa.ustr(
                "upper(codserie)='",
                codSerie,
                "' AND upper(codejercicio)='",
                codEjercicio,
                "' AND upper(tipo)='",
                tipo,
                "' ORDER BY numero;",
            )
        )
        if cursorHuecos.next():
            numHueco = cursorHuecos.valueBuffer("numero")
            cursorHuecos.setActivatedCheckIntegrity(False)
            cursorHuecos.setModeAccess(cursorHuecos.Del)
            cursorHuecos.refreshBuffer()
            cursorHuecos.commitBuffer()

        return numHueco

    def oficial_establecerNumeroSecuencia(self, fN=None, value=None):
        return qsa.parseFloat(value) + 1

    def oficial_cerosIzquierda(self, numero=None, totalCifras=None):
        ret = qsa.parseString(numero)
        numCeros = totalCifras - qsa.length(ret)
        while_pass = True
        while numCeros > 0:
            if not while_pass:
                numCeros -= 1
                while_pass = True
                continue
            while_pass = False
            ret = qsa.ustr("0", ret)
            numCeros -= 1
            while_pass = True
            try:
                numCeros > 0
            except Exception:
                break

        return ret

    def oficial_construirCodigo(self, codSerie=None, codEjercicio=None, numero=None):
        return (
            self.iface.cerosIzquierda(codEjercicio, 4)
            + self.iface.cerosIzquierda(codSerie, 2)
            + self.iface.cerosIzquierda(numero, 6)
        )

    def oficial_siguienteNumero(self, codSerie=None, codEjercicio=None, fN=None):
        numero = 0
        util = qsa.FLUtil()
        cursorSecuencias = qsa.FLSqlCursor("secuenciasejercicios")
        cursorSecuencias.setContext(self)
        cursorSecuencias.setActivatedCheckIntegrity(False)
        cursorSecuencias.select(
            qsa.ustr("upper(codserie)='", codSerie, "' AND upper(codejercicio)='", codEjercicio, "';")
        )
        if cursorSecuencias.next():
            if fN == "nfacturaprov":
                numeroHueco = self.iface.obtenerHueco(codSerie, codEjercicio, "FP")
                if numeroHueco != 0:
                    cursorSecuencias.setActivatedCheckIntegrity(True)
                    return numeroHueco

            if fN == "nfacturacli":
                numeroHueco = self.iface.obtenerHueco(codSerie, codEjercicio, "FC")
                if numeroHueco != 0:
                    cursorSecuencias.setActivatedCheckIntegrity(True)
                    return numeroHueco

            cursorSecs = qsa.FLSqlCursor("secuencias")
            cursorSecs.setContext(self)
            cursorSecs.setActivatedCheckIntegrity(False)
            idSec = cursorSecuencias.valueBuffer("id")
            cursorSecs.select(qsa.ustr("id=", idSec, " AND nombre='", fN, "'"))
            if not cursorSecs.next():
                numero = cursorSecuencias.valueBuffer(fN)
                if not numero or qsa.isNaN(numero):
                    numero = 1
                cursorSecs.setModeAccess(cursorSecs.Insert)
                cursorSecs.refreshBuffer()
                cursorSecs.setValueBuffer("id", idSec)
                cursorSecs.setValueBuffer("nombre", fN)
                cursorSecs.setValueBuffer("valor", self.iface.establecerNumeroSecuencia(fN, numero))
                cursorSecs.commitBuffer()

            else:
                cursorSecs.setModeAccess(cursorSecs.Edit)
                cursorSecs.refreshBuffer()
                if not cursorSecs.isNull("valorout"):
                    numero = cursorSecs.valueBuffer("valorout")
                else:
                    numero = cursorSecs.valueBuffer("valor")

                cursorSecs.setValueBuffer("valorout", self.iface.establecerNumeroSecuencia(fN, numero))
                cursorSecs.commitBuffer()

            cursorSecs.setActivatedCheckIntegrity(True)

        else:
            res = qsa.MessageBox.warning(
                util.translate("scripts", "La serie ")
                + codSerie
                + util.translate("scripts", " no existe para el ejercicio ")
                + codEjercicio
                + util.translate("scripts", ".\n¿Desea crearla?"),
                qsa.MessageBox.Yes,
                qsa.MessageBox.No,
            )
            if res != qsa.MessageBox.Yes:
                cursorSecuencias.setActivatedCheckIntegrity(True)
                return False
            cursorSecuencias.setModeAccess(cursorSecuencias.Insert)
            cursorSecuencias.refreshBuffer()
            cursorSecuencias.setValueBuffer("codserie", codSerie)
            cursorSecuencias.setValueBuffer("codejercicio", codEjercicio)
            numero = "1"
            cursorSecuencias.setValueBuffer(fN, "2")
            if not cursorSecuencias.commitBuffer():
                cursorSecuencias.setActivatedCheckIntegrity(True)
                return False

        cursorSecuencias.setActivatedCheckIntegrity(True)
        return numero

    def oficial_agregarHueco(self, serie=None, ejercicio=None, numero=None, fN=None):
        return self.iface.recalcularHuecos(serie, ejercicio, fN)

    def oficial_asientoBorrable(self, idAsiento=None):
        util = qsa.FLUtil()
        qryEjerAsiento = qsa.FLSqlQuery()
        qryEjerAsiento.setTablesList("ejercicios,co_asientos")
        qryEjerAsiento.setSelect("e.estado")
        qryEjerAsiento.setFrom(qsa.ustr("co_asientos a INNER JOIN ejercicios e", " ON a.codejercicio = e.codejercicio"))
        qryEjerAsiento.setWhere(qsa.ustr("a.idasiento = ", idAsiento))
        try:
            qryEjerAsiento.setForwardOnly(True)
        except Exception:
            e = qsa.format_exc()

        if not qryEjerAsiento.exec_():
            return False
        if not qryEjerAsiento.next():
            return True
        if qryEjerAsiento.value(0) != "ABIERTO":
            qsa.MessageBox.critical(
                util.translate(
                    "scripts",
                    "No puede realizarse la modificación porque el asiento contable correspondiente pertenece a un ejercicio cerrado",
                ),
                qsa.MessageBox.Ok,
                qsa.MessageBox.NoButton,
                qsa.MessageBox.NoButton,
            )
            return False
        return True

    def oficial_generarAsientoFacturaCli(self, curFactura=None):
        if curFactura.modeAccess() != curFactura.Insert and curFactura.modeAccess() != curFactura.Edit:
            return True
        util = qsa.FLUtil()
        if curFactura.valueBuffer("nogenerarasiento"):
            curFactura.setNull("idasiento")
            return True
        if not self.iface.comprobarRegularizacion(curFactura):
            return False
        datosAsiento = qsa.Array()
        valoresDefecto = qsa.Array()
        valoresDefecto["codejercicio"] = curFactura.valueBuffer("codejercicio")
        valoresDefecto["coddivisa"] = qsa.from_project("flfactppal").iface.pub_valorDefectoEmpresa("coddivisa")
        curTransaccion = qsa.FLSqlCursor("facturascli")
        curTransaccion.transaction(False)
        try:
            datosAsiento = self.iface.regenerarAsiento(curFactura, valoresDefecto)
            if datosAsiento.error:
                raise Exception(util.translate("scripts", "Error al regenerar el asiento"))
            ctaCliente = self.iface.datosCtaCliente(curFactura, valoresDefecto)
            if ctaCliente.error != 0:
                raise Exception(util.translate("scripts", "Error al leer los datos de subcuenta de cliente"))
            if not self.iface.generarPartidasCliente(curFactura, datosAsiento.idasiento, valoresDefecto, ctaCliente):
                raise Exception(util.translate("scripts", "Error al generar las partidas de cliente"))
            if not self.iface.generarPartidasIRPF(curFactura, datosAsiento.idasiento, valoresDefecto):
                raise Exception(util.translate("scripts", "Error al generar las partidas de IRPF"))
            if not self.iface.generarPartidasIVACli(curFactura, datosAsiento.idasiento, valoresDefecto, ctaCliente):
                raise Exception(util.translate("scripts", "Error al generar las partidas de IVA"))
            if not self.iface.generarPartidasRecFinCli(curFactura, datosAsiento.idasiento, valoresDefecto):
                raise Exception(util.translate("scripts", "Error al generar las partidas de recargo financiero"))
            if not self.iface.generarPartidasVenta(curFactura, datosAsiento.idasiento, valoresDefecto):
                raise Exception(util.translate("scripts", "Error al generar las partidas de venta"))
            curFactura.setValueBuffer("idasiento", datosAsiento.idasiento)
            if curFactura.valueBuffer("deabono"):
                if not self.iface.asientoFacturaAbonoCli(curFactura, valoresDefecto):
                    raise Exception(
                        util.translate("scripts", "Error al generar el asiento correspondiente a la factura de abono")
                    )
            if not qsa.from_project("flcontppal").iface.pub_comprobarAsiento(datosAsiento.idasiento):
                raise Exception(util.translate("scripts", "Error al comprobar el asiento"))

        except Exception:
            e = qsa.format_exc()
            curTransaccion.rollback()
            qsa.MessageBox.warning(
                qsa.ustr(
                    util.translate("scripts", "Error al generar el asiento correspondiente a la factura %s:")
                    % (str(curFactura.valueBuffer("codigo"))),
                    "\n",
                    e,
                ),
                qsa.MessageBox.Ok,
                qsa.MessageBox.NoButton,
            )
            return False

        curTransaccion.commit()
        return True

    def oficial_generarPartidasVenta(self, curFactura=None, idAsiento=None, valoresDefecto=None):
        util = qsa.FLUtil()
        ctaVentas = self.iface.datosCtaVentas(valoresDefecto.codejercicio, curFactura.valueBuffer("codserie"))
        if ctaVentas.error != 0:
            qsa.MessageBox.warning(
                util.translate("scripts", "No se ha encontrado una subcuenta de ventas para esta factura."),
                qsa.MessageBox.Ok,
                qsa.MessageBox.NoButton,
            )
            return False
        haber = 0
        haberME = 0
        monedaSistema = valoresDefecto.coddivisa == curFactura.valueBuffer("coddivisa")
        if monedaSistema:
            haber = self.iface.netoVentasFacturaCli(curFactura)
            haberME = 0
        else:
            haber = qsa.parseFloat(
                util.sqlSelect("co_partidas", "SUM(debe - haber)", qsa.ustr("idasiento = ", idAsiento))
            )
            haberME = self.iface.netoVentasFacturaCli(curFactura)

        haber = util.roundFieldValue(haber, "co_partidas", "haber")
        haberME = util.roundFieldValue(haberME, "co_partidas", "haberme")
        curPartida = qsa.FLSqlCursor("co_partidas")
        # WITH_START
        curPartida.setModeAccess(curPartida.Insert)
        curPartida.refreshBuffer()
        curPartida.setValueBuffer("idsubcuenta", ctaVentas.idsubcuenta)
        curPartida.setValueBuffer("codsubcuenta", ctaVentas.codsubcuenta)
        curPartida.setValueBuffer("idasiento", idAsiento)
        curPartida.setValueBuffer("debe", 0)
        curPartida.setValueBuffer("haber", haber)
        curPartida.setValueBuffer("coddivisa", curFactura.valueBuffer("coddivisa"))
        curPartida.setValueBuffer("tasaconv", curFactura.valueBuffer("tasaconv"))
        curPartida.setValueBuffer("debeME", 0)
        curPartida.setValueBuffer("haberME", haberME)
        # WITH_END
        self.iface.datosPartidaFactura(curPartida, curFactura, "cliente")
        if not curPartida.commitBuffer():
            return False
        return True

    def oficial_netoVentasFacturaCli(self, curFactura=None):
        return qsa.parseFloat(curFactura.valueBuffer("neto"))

    def oficial_netoComprasFacturaProv(self, curFactura=None):
        return qsa.parseFloat(curFactura.valueBuffer("neto"))

    def oficial_generarPartidasIVACli(self, curFactura=None, idAsiento=None, valoresDefecto=None, ctaCliente=None):
        util = qsa.FLUtil()
        haber = 0
        haberME = 0
        baseImponible = 0
        recargo = 0
        iva = 0
        regimenIVA = self.iface.regimenIVACliente(curFactura)
        if not regimenIVA:
            qsa.MessageBox.warning(
                util.translate(
                    "scripts",
                    "Error al obtener el régimen de IVA asociado a la factura %s.\nCompruebe que el cliente tiene un régimen de IVA establecido",
                )
                % (str(curFactura.valueBuffer("codigo"))),
                qsa.MessageBox.Ok,
                qsa.MessageBox.NoButton,
            )
            return False
        monedaSistema = valoresDefecto.coddivisa == curFactura.valueBuffer("coddivisa")
        qryIva = qsa.FLSqlQuery()
        qryIva.setTablesList("lineasivafactcli")
        qryIva.setSelect("neto, iva, totaliva, recargo, totalrecargo, codimpuesto")
        qryIva.setFrom("lineasivafactcli")
        qryIva.setWhere(qsa.ustr("idfactura = ", curFactura.valueBuffer("idfactura")))
        try:
            qryIva.setForwardOnly(True)
        except Exception:
            e = qsa.format_exc()

        if not qryIva.exec_():
            return False
        while qryIva.next():
            iva = qsa.parseFloat(qryIva.value("iva"))
            if qsa.isNaN(iva):
                iva = 0
            recargo = qsa.parseFloat(qryIva.value("recargo"))
            if qsa.isNaN(recargo):
                recargo = 0
            if monedaSistema:
                haber = qsa.parseFloat(qryIva.value(2))
                haberME = 0
                baseImponible = qsa.parseFloat(qryIva.value(0))
            else:
                haber = qsa.parseFloat(qryIva.value(2)) * qsa.parseFloat(curFactura.valueBuffer("tasaconv"))
                haberME = qsa.parseFloat(qryIva.value(2))
                baseImponible = qsa.parseFloat(qryIva.value(0)) * qsa.parseFloat(curFactura.valueBuffer("tasaconv"))

            haber = util.roundFieldValue(haber, "co_partidas", "haber")
            haberME = util.roundFieldValue(haberME, "co_partidas", "haberme")
            baseImponible = util.roundFieldValue(baseImponible, "co_partidas", "baseimponible")
            ctaIvaRep = qsa.Array()
            textoError = ""
            for case in qsa.switch(regimenIVA):
                if case("U.E."):
                    ctaIvaRep = self.iface.datosCtaIVA("IVAEUE", valoresDefecto.codejercicio, qryIva.value(5))
                    textoError = util.translate("scripts", "I.V.A. entregas intracomunitarias (IVAEUE)")
                    break
                if case("Exento"):
                    ctaIvaRep = self.iface.datosCtaIVA("IVAREX", valoresDefecto.codejercicio, qryIva.value(5))
                    textoError = util.translate("scripts", "I.V.A. repercutido exento (IVAREX)")
                    break
                if case("Exportaciones"):
                    ctaIvaRep = self.iface.datosCtaIVA("IVARXP", valoresDefecto.codejercicio, qryIva.value(5))
                    textoError = util.translate("scripts", "I.V.A. repercutido exportaciones (IVARXP)")
                    break
                if case():
                    ctaIvaRep = self.iface.datosCtaIVA("IVAREP", valoresDefecto.codejercicio, qryIva.value(5))
                    textoError = util.translate("scripts", "I.V.A. repercutido R. General(IVAREP)")

            if ctaIvaRep.error != 0:
                qsa.MessageBox.information(
                    util.translate(
                        "scripts",
                        "La cuenta especial de %s no tiene asignada subcuenta.\nDebe asociarla en el módulo Principal del área Financiera",
                    )
                    % (str(textoError)),
                    qsa.MessageBox.Ok,
                    qsa.MessageBox.NoButton,
                )
                return False
            curPartida = qsa.FLSqlCursor("co_partidas")
            # WITH_START
            curPartida.setModeAccess(curPartida.Insert)
            curPartida.refreshBuffer()
            curPartida.setValueBuffer("idsubcuenta", ctaIvaRep.idsubcuenta)
            curPartida.setValueBuffer("codsubcuenta", ctaIvaRep.codsubcuenta)
            curPartida.setValueBuffer("idasiento", idAsiento)
            curPartida.setValueBuffer("debe", 0)
            curPartida.setValueBuffer("haber", haber)
            curPartida.setValueBuffer("baseimponible", baseImponible)
            curPartida.setValueBuffer("iva", iva)
            curPartida.setValueBuffer("recargo", recargo)
            curPartida.setValueBuffer("coddivisa", curFactura.valueBuffer("coddivisa"))
            curPartida.setValueBuffer("tasaconv", curFactura.valueBuffer("tasaconv"))
            curPartida.setValueBuffer("idcontrapartida", ctaCliente.idsubcuenta)
            curPartida.setValueBuffer("codcontrapartida", ctaCliente.codsubcuenta)
            curPartida.setValueBuffer("debeME", 0)
            curPartida.setValueBuffer("haberME", haberME)
            curPartida.setValueBuffer("codserie", curFactura.valueBuffer("codserie"))
            curPartida.setValueBuffer("cifnif", curFactura.valueBuffer("cifnif"))
            # WITH_END
            self.iface.datosPartidaFactura(curPartida, curFactura, "cliente")
            if not curPartida.commitBuffer():
                return False
            if monedaSistema:
                haber = qsa.parseFloat(qryIva.value(4))
                haberME = 0
            else:
                haber = qsa.parseFloat(qryIva.value(4)) * qsa.parseFloat(curFactura.valueBuffer("tasaconv"))
                haberME = qsa.parseFloat(qryIva.value(4))

            haber = util.roundFieldValue(haber, "co_partidas", "haber")
            haberME = util.roundFieldValue(haberME, "co_partidas", "haberme")
            if qsa.parseFloat(haber) != 0:
                ctaRecargo = self.iface.datosCtaIVA("IVARRE", valoresDefecto.codejercicio, qryIva.value(5))
                if ctaRecargo.error != 0:
                    qsa.MessageBox.warning(
                        util.translate(
                            "scripts",
                            "No tiene definida cuál es la subcuenta  asociada al recargo de equivalencia en ventas.\nPara definirla vaya a Facturación->Principal->Impuestos e indíquela en el/los impuestos correspondientes",
                        ),
                        qsa.MessageBox.Ok,
                        qsa.MessageBox.NoButton,
                    )
                    return False
                curPartida = qsa.FLSqlCursor("co_partidas")
                # WITH_START
                curPartida.setModeAccess(curPartida.Insert)
                curPartida.refreshBuffer()
                curPartida.setValueBuffer("idsubcuenta", ctaRecargo.idsubcuenta)
                curPartida.setValueBuffer("codsubcuenta", ctaRecargo.codsubcuenta)
                curPartida.setValueBuffer("idasiento", idAsiento)
                curPartida.setValueBuffer("debe", 0)
                curPartida.setValueBuffer("haber", haber)
                curPartida.setValueBuffer("baseimponible", baseImponible)
                curPartida.setValueBuffer("iva", iva)
                curPartida.setValueBuffer("recargo", recargo)
                curPartida.setValueBuffer("coddivisa", curFactura.valueBuffer("coddivisa"))
                curPartida.setValueBuffer("tasaconv", curFactura.valueBuffer("tasaconv"))
                curPartida.setValueBuffer("idcontrapartida", ctaCliente.idsubcuenta)
                curPartida.setValueBuffer("codcontrapartida", ctaCliente.codsubcuenta)
                curPartida.setValueBuffer("debeME", 0)
                curPartida.setValueBuffer("haberME", haberME)
                curPartida.setValueBuffer("codserie", curFactura.valueBuffer("codserie"))
                curPartida.setValueBuffer("cifnif", curFactura.valueBuffer("cifnif"))
                # WITH_END
                self.iface.datosPartidaFactura(curPartida, curFactura, "cliente")
                if not curPartida.commitBuffer():
                    return False

        return True

    def oficial_regimenIVACliente(self, curDocCliente=None):
        util = qsa.FLUtil()
        regimen = ""
        codCliente = curDocCliente.valueBuffer("codcliente")
        if codCliente and codCliente != "":
            regimen = util.sqlSelect("clientes", "regimeniva", qsa.ustr("codcliente = '", codCliente, "'"))
        else:
            regimen = "General"

        return regimen

    def oficial_generarPartidasIRPF(self, curFactura=None, idAsiento=None, valoresDefecto=None):
        util = qsa.FLUtil()
        irpf = qsa.parseFloat(curFactura.valueBuffer("totalirpf"))
        if irpf == 0:
            return True
        debe = 0
        debeME = 0
        ctaIrpf = self.iface.datosCtaEspecial("IRPF", valoresDefecto.codejercicio)
        if ctaIrpf.error != 0:
            qsa.MessageBox.warning(
                util.translate(
                    "scripts",
                    "No tiene ninguna cuenta contable marcada como cuenta especial\nIRPF (IRPF para clientes).\nDebe asociar la cuenta a la cuenta especial en el módulo Principal del área Financiera",
                ),
                qsa.MessageBox.Ok,
                qsa.MessageBox.NoButton,
                qsa.MessageBox.NoButton,
            )
            return False
        monedaSistema = valoresDefecto.coddivisa == curFactura.valueBuffer("coddivisa")
        if monedaSistema:
            debe = irpf
            debeME = 0
        else:
            debe = irpf * qsa.parseFloat(curFactura.valueBuffer("tasaconv"))
            debeME = irpf

        debe = util.roundFieldValue(debe, "co_partidas", "debe")
        debeME = util.roundFieldValue(debeME, "co_partidas", "debeme")
        curPartida = qsa.FLSqlCursor("co_partidas")
        # WITH_START
        curPartida.setModeAccess(curPartida.Insert)
        curPartida.refreshBuffer()
        curPartida.setValueBuffer("idsubcuenta", ctaIrpf.idsubcuenta)
        curPartida.setValueBuffer("codsubcuenta", ctaIrpf.codsubcuenta)
        curPartida.setValueBuffer("idasiento", idAsiento)
        curPartida.setValueBuffer("debe", debe)
        curPartida.setValueBuffer("haber", 0)
        curPartida.setValueBuffer("coddivisa", curFactura.valueBuffer("coddivisa"))
        curPartida.setValueBuffer("tasaconv", curFactura.valueBuffer("tasaconv"))
        curPartida.setValueBuffer("debeME", debeME)
        curPartida.setValueBuffer("haberME", 0)
        # WITH_END
        self.iface.datosPartidaFactura(curPartida, curFactura, "cliente")
        if not curPartida.commitBuffer():
            return False
        return True

    def oficial_generarPartidasRecFinCli(self, curFactura=None, idAsiento=None, valoresDefecto=None):
        util = qsa.FLUtil()
        recFinanciero = qsa.parseFloat(curFactura.valueBuffer("recfinanciero") * curFactura.valueBuffer("neto") / 100)
        if not recFinanciero:
            return True
        haber = 0
        haberME = 0
        ctaRecfin = qsa.Array()
        ctaRecfin = self.iface.datosCtaEspecial("INGRF", valoresDefecto.codejercicio)
        if ctaRecfin.error != 0:
            qsa.MessageBox.warning(
                util.translate(
                    "scripts",
                    "No tiene ninguna cuenta contable marcada como cuenta especial\nINGRF (recargo financiero en ingresos) \nDebe asociar una cuenta contable a esta cuenta especial en el módulo Principal del área Financiera",
                ),
                qsa.MessageBox.Ok,
                qsa.MessageBox.NoButton,
                qsa.MessageBox.NoButton,
            )
            return False
        monedaSistema = valoresDefecto.coddivisa == curFactura.valueBuffer("coddivisa")
        if monedaSistema:
            haber = recFinanciero
            haberME = 0
        else:
            haber = recFinanciero * qsa.parseFloat(curFactura.valueBuffer("tasaconv"))
            haberME = recFinanciero

        haber = util.roundFieldValue(haber, "co_partidas", "haber")
        haberME = util.roundFieldValue(haberME, "co_partidas", "haberme")
        curPartida = qsa.FLSqlCursor("co_partidas")
        # WITH_START
        curPartida.setModeAccess(curPartida.Insert)
        curPartida.refreshBuffer()
        curPartida.setValueBuffer("idsubcuenta", ctaRecfin.idsubcuenta)
        curPartida.setValueBuffer("codsubcuenta", ctaRecfin.codsubcuenta)
        curPartida.setValueBuffer("idasiento", idAsiento)
        curPartida.setValueBuffer("haber", haber)
        curPartida.setValueBuffer("debe", 0)
        curPartida.setValueBuffer("coddivisa", curFactura.valueBuffer("coddivisa"))
        curPartida.setValueBuffer("tasaconv", curFactura.valueBuffer("tasaconv"))
        curPartida.setValueBuffer("haberME", haberME)
        curPartida.setValueBuffer("debeME", 0)
        # WITH_END
        self.iface.datosPartidaFactura(curPartida, curFactura, "cliente")
        if not curPartida.commitBuffer():
            return False
        return True

    def oficial_generarPartidasIRPFProv(self, curFactura=None, idAsiento=None, valoresDefecto=None):
        util = qsa.FLUtil()
        irpf = qsa.parseFloat(curFactura.valueBuffer("totalirpf"))
        if irpf == 0:
            return True
        haber = 0
        haberME = 0
        ctaIrpf = qsa.Array()
        ctaIrpf.codsubcuenta = util.sqlSelect(
            "lineasfacturasprov lf INNER JOIN articulos a ON lf.referencia = a.referencia",
            "a.codsubcuentairpfcom",
            qsa.ustr("lf.idfactura = ", curFactura.valueBuffer("idfactura"), " AND a.codsubcuentairpfcom IS NOT NULL"),
            "lineasfacturasprov,articulos",
        )
        if ctaIrpf.codsubcuenta:
            hayDistintasSubcuentas = util.sqlSelect(
                "lineasfacturasprov lf INNER JOIN articulos a ON lf.referencia = a.referencia",
                "a.referencia",
                qsa.ustr(
                    "lf.idfactura = ",
                    curFactura.valueBuffer("idfactura"),
                    " AND (a.codsubcuentairpfcom <> '",
                    ctaIrpf.codsubcuenta,
                    "' OR a.codsubcuentairpfcom  IS NULL)",
                ),
                "lineasfacturasprov,articulos",
            )
            if hayDistintasSubcuentas:
                qsa.MessageBox.warning(
                    util.translate(
                        "scripts",
                        "No es posible generar el asiento contable de una factura que tiene artículos asignados a distintas subcuentas de IRPF.\nDebe corregir la asociación de las subcuentas de IRPF a los artículos o bien crear distintas facturas para cada subcuenta.",
                    ),
                    qsa.MessageBox.Ok,
                    qsa.MessageBox.NoButton,
                    qsa.MessageBox.NoButton,
                )
                return False
            ctaIrpf.idsubcuenta = util.sqlSelect(
                "co_subcuentas",
                "idsubcuenta",
                qsa.ustr(
                    "codsubcuenta = '", ctaIrpf.codsubcuenta, "' AND codejercicio = '", valoresDefecto.codejercicio, "'"
                ),
            )
            if not ctaIrpf.idsubcuenta:
                qsa.MessageBox.warning(
                    util.translate(
                        "scripts",
                        "No existe la subcuenta de IRPF %s para el ejercicio %s.\nAntes de generar el asiento debe crear esta subcuenta.",
                    )
                    % (str(ctaIrpf.codsubcuenta), str(valoresDefecto.codejercicio)),
                    qsa.MessageBox.Ok,
                    qsa.MessageBox.NoButton,
                    qsa.MessageBox.NoButton,
                )
                return False

        else:
            ctaIrpf = self.iface.datosCtaEspecial("IRPFPR", valoresDefecto.codejercicio)
            if ctaIrpf.error != 0:
                qsa.MessageBox.warning(
                    util.translate(
                        "scripts",
                        "No tiene ninguna cuenta contable marcada como cuenta especial\nIRPFPR (IRPF para proveedores / acreedores).\nDebe asociar la cuenta a la cuenta especial en el módulo Principal del área Financiera",
                    ),
                    qsa.MessageBox.Ok,
                    qsa.MessageBox.NoButton,
                    qsa.MessageBox.NoButton,
                )
                return False

        monedaSistema = valoresDefecto.coddivisa == curFactura.valueBuffer("coddivisa")
        if monedaSistema:
            haber = irpf
            haberME = 0
        else:
            haber = irpf * qsa.parseFloat(curFactura.valueBuffer("tasaconv"))
            haberME = irpf

        haber = util.roundFieldValue(haber, "co_partidas", "haber")
        haberME = util.roundFieldValue(haberME, "co_partidas", "haberme")
        curPartida = qsa.FLSqlCursor("co_partidas")
        # WITH_START
        curPartida.setModeAccess(curPartida.Insert)
        curPartida.refreshBuffer()
        curPartida.setValueBuffer("idsubcuenta", ctaIrpf.idsubcuenta)
        curPartida.setValueBuffer("codsubcuenta", ctaIrpf.codsubcuenta)
        curPartida.setValueBuffer("idasiento", idAsiento)
        curPartida.setValueBuffer("debe", 0)
        curPartida.setValueBuffer("haber", haber)
        curPartida.setValueBuffer("coddivisa", curFactura.valueBuffer("coddivisa"))
        curPartida.setValueBuffer("tasaconv", curFactura.valueBuffer("tasaconv"))
        curPartida.setValueBuffer("debeME", 0)
        curPartida.setValueBuffer("haberME", haberME)
        # WITH_END
        self.iface.datosPartidaFactura(curPartida, curFactura, "proveedor")
        if not curPartida.commitBuffer():
            return False
        return True

    def oficial_generarPartidasCliente(self, curFactura=None, idAsiento=None, valoresDefecto=None, ctaCliente=None):
        util = qsa.FLUtil()
        debe = 0
        debeME = 0
        monedaSistema = valoresDefecto.coddivisa == curFactura.valueBuffer("coddivisa")
        if monedaSistema:
            debe = qsa.parseFloat(curFactura.valueBuffer("total"))
            debeME = 0
        else:
            debe = qsa.parseFloat(curFactura.valueBuffer("total")) * qsa.parseFloat(curFactura.valueBuffer("tasaconv"))
            debeME = qsa.parseFloat(curFactura.valueBuffer("total"))

        debe = util.roundFieldValue(debe, "co_partidas", "debe")
        debeME = util.roundFieldValue(debeME, "co_partidas", "debeme")
        curPartida = qsa.FLSqlCursor("co_partidas")
        # WITH_START
        curPartida.setModeAccess(curPartida.Insert)
        curPartida.refreshBuffer()
        curPartida.setValueBuffer("idsubcuenta", ctaCliente.idsubcuenta)
        curPartida.setValueBuffer("codsubcuenta", ctaCliente.codsubcuenta)
        curPartida.setValueBuffer("idasiento", idAsiento)
        curPartida.setValueBuffer("debe", debe)
        curPartida.setValueBuffer("haber", 0)
        curPartida.setValueBuffer("coddivisa", curFactura.valueBuffer("coddivisa"))
        curPartida.setValueBuffer("tasaconv", curFactura.valueBuffer("tasaconv"))
        curPartida.setValueBuffer("debeME", debeME)
        curPartida.setValueBuffer("haberME", 0)
        # WITH_END
        self.iface.datosPartidaFactura(curPartida, curFactura, "cliente")
        if not curPartida.commitBuffer():
            return False
        return True

    def oficial_regenerarAsiento(self, cur=None, valoresDefecto=None):
        util = qsa.FLUtil()
        asiento = qsa.Array()
        idAsiento = cur.valueBuffer("idasiento")
        if cur.isNull("idasiento"):
            datosAsiento = self.iface.datosConceptoAsiento(cur)
            if not self.iface.curAsiento_:
                self.iface.curAsiento_ = qsa.FLSqlCursor("co_asientos")
            self.iface.curAsiento_.setModeAccess(self.iface.curAsiento_.Insert)
            self.iface.curAsiento_.refreshBuffer()
            self.iface.curAsiento_.setValueBuffer("numero", 0)
            self.iface.curAsiento_.setValueBuffer("fecha", cur.valueBuffer("fecha"))
            self.iface.curAsiento_.setValueBuffer("codejercicio", valoresDefecto.codejercicio)
            self.iface.curAsiento_.setValueBuffer("concepto", datosAsiento.concepto)
            self.iface.curAsiento_.setValueBuffer("tipodocumento", datosAsiento.tipoDocumento)
            self.iface.curAsiento_.setValueBuffer("documento", datosAsiento.documento)
            if not self.iface.datosAsientoRegenerado(cur, valoresDefecto):
                asiento.error = True
                return asiento
            if not self.iface.curAsiento_.commitBuffer():
                asiento.error = True
                return asiento
            asiento.idasiento = self.iface.curAsiento_.valueBuffer("idasiento")
            asiento.numero = self.iface.curAsiento_.valueBuffer("numero")
            asiento.fecha = self.iface.curAsiento_.valueBuffer("fecha")
            asiento.concepto = self.iface.curAsiento_.valueBuffer("concepto")
            asiento.tipodocumento = self.iface.curAsiento_.valueBuffer("tipodocumento")
            asiento.documento = self.iface.curAsiento_.valueBuffer("documento")
            self.iface.curAsiento_.select(qsa.ustr("idasiento = ", asiento.idasiento))
            self.iface.curAsiento_.first()
            self.iface.curAsiento_.setUnLock("editable", False)

        else:
            datosAsiento = self.iface.datosConceptoAsiento(cur)
            if not self.iface.asientoBorrable(idAsiento):
                asiento.error = True
                return asiento
            if not self.iface.curAsiento_:
                self.iface.curAsiento_ = qsa.FLSqlCursor("co_asientos")
            self.iface.curAsiento_.select(qsa.ustr("idasiento = ", idAsiento))
            if not self.iface.curAsiento_.first():
                asiento.error = True
                return asiento
            self.iface.curAsiento_.setUnLock("editable", True)
            self.iface.curAsiento_.select(qsa.ustr("idasiento = ", idAsiento))
            if not self.iface.curAsiento_.first():
                asiento.error = True
                return asiento
            self.iface.curAsiento_.setModeAccess(self.iface.curAsiento_.Edit)
            self.iface.curAsiento_.refreshBuffer()
            self.iface.curAsiento_.setValueBuffer("fecha", cur.valueBuffer("fecha"))
            self.iface.curAsiento_.setValueBuffer("concepto", datosAsiento.concepto)
            self.iface.curAsiento_.setValueBuffer("tipodocumento", datosAsiento.tipoDocumento)
            self.iface.curAsiento_.setValueBuffer("documento", datosAsiento.documento)
            if not self.iface.datosAsientoRegenerado(cur, valoresDefecto):
                asiento.error = True
                return asiento
            if not self.iface.curAsiento_.commitBuffer():
                asiento.error = True
                return asiento
            self.iface.curAsiento_.select(qsa.ustr("idasiento = ", idAsiento))
            if not self.iface.curAsiento_.first():
                asiento.error = True
                return asiento
            self.iface.curAsiento_.setUnLock("editable", False)
            asiento = qsa.from_project("flfactppal").iface.pub_ejecutarQry(
                "co_asientos",
                "idasiento,numero,fecha,codejercicio,concepto,tipodocumento,documento",
                qsa.ustr("idasiento = '", idAsiento, "'"),
            )
            if asiento.codejercicio != valoresDefecto.codejercicio:
                qsa.MessageBox.warning(
                    util.translate(
                        "scripts",
                        "Está intentando regenerar un asiento del ejercicio %s en el ejercicio %s.\nVerifique que su ejercicio actual es correcto. Si lo es y está actualizando un pago, bórrelo y vuélvalo a crear.",
                    )
                    % (str(asiento.codejercicio), str(valoresDefecto.codejercicio)),
                    qsa.MessageBox.Ok,
                    qsa.MessageBox.NoButton,
                )
                asiento.error = True
                return asiento
            curPartidas = qsa.FLSqlCursor("co_partidas")
            curPartidas.select(qsa.ustr("idasiento = ", idAsiento))
            idP = 0
            while curPartidas.next():
                curPartidas.setModeAccess(curPartidas.Del)
                curPartidas.refreshBuffer()
                if not curPartidas.commitBuffer():
                    asiento.error = True
                    return asiento

        asiento.error = False
        return asiento

    def oficial_datosAsientoRegenerado(self, cur=None, valoresDefecto=None):
        return True

    def oficial_datosConceptoAsiento(self, cur=None):
        util = qsa.FLUtil()
        datosAsiento = qsa.Array()
        for case in qsa.switch(cur.table()):
            if case("facturascli"):
                datosAsiento.concepto = qsa.ustr(
                    "Nuestra factura ", cur.valueBuffer("codigo"), " - ", cur.valueBuffer("nombrecliente")
                )
                datosAsiento.documento = cur.valueBuffer("codigo")
                datosAsiento.tipoDocumento = "Factura de cliente"
                break

            if case("facturasprov"):
                numProveedor = cur.valueBuffer("numproveedor")
                if numProveedor and numProveedor != "":
                    numProveedor = qsa.ustr(numProveedor, " / ")
                datosAsiento.concepto = qsa.ustr(
                    "Su factura ", numProveedor, cur.valueBuffer("codigo"), " - ", cur.valueBuffer("nombre")
                )
                datosAsiento.documento = cur.valueBuffer("codigo")
                datosAsiento.tipoDocumento = "Factura de proveedor"
                break

            if case("pagosdevolcli"):
                codRecibo = util.sqlSelect("reciboscli", "codigo", qsa.ustr("idrecibo = ", cur.valueBuffer("idrecibo")))
                nombreCli = util.sqlSelect(
                    "reciboscli", "nombrecliente", qsa.ustr("idrecibo = ", cur.valueBuffer("idrecibo"))
                )
                if cur.valueBuffer("tipo") == "Pago":
                    datosAsiento.concepto = qsa.ustr("Pago recibo ", codRecibo, " - ", nombreCli)
                else:
                    datosAsiento.concepto = qsa.ustr("Devolución recibo ", codRecibo)

                datosAsiento.tipoDocumento = "Recibo"
                datosAsiento.documento = ""
                break

            if case("pagosdevolrem"):
                if cur.valueBuffer("tipo") == "Pago":
                    datosAsiento.concepto = qsa.ustr(
                        cur.valueBuffer("tipo"), " ", "remesa", " ", cur.valueBuffer("idremesa")
                    )
                datosAsiento.tipoDocumento = ""
                datosAsiento.documento = ""
                break

            if case("co_dotaciones"):
                datosAsiento.concepto = qsa.ustr(
                    "Dotación de ",
                    util.sqlSelect(
                        "co_amortizaciones",
                        "elemento",
                        qsa.ustr("codamortizacion = '", cur.valueBuffer("codamortizacion"), "'"),
                    ),
                    " - ",
                    util.dateAMDtoDMA(cur.valueBuffer("fecha")),
                )
                datosAsiento.documento = ""
                datosAsiento.tipoDocumento = ""
                break

            if case():
                datosAsiento.concepto = ""
                datosAsiento.documento = ""
                datosAsiento.tipoDocumento = ""

        return datosAsiento

    def oficial_eliminarAsiento(self, idAsiento=None):
        util = qsa.FLUtil()
        if not idAsiento or idAsiento == "":
            return True
        if not self.iface.asientoBorrable(idAsiento):
            return False
        curAsiento = qsa.FLSqlCursor("co_asientos")
        curAsiento.select(qsa.ustr("idasiento = ", idAsiento))
        if not curAsiento.first():
            return False
        curAsiento.setUnLock("editable", True)
        if not util.sqlDelete("co_asientos", qsa.ustr("idasiento = ", idAsiento)):
            curAsiento.setValueBuffer("idasiento", idAsiento)
            return False
        return True

    def oficial_generarAsientoFacturaProv(self, curFactura=None):
        if curFactura.modeAccess() != curFactura.Insert and curFactura.modeAccess() != curFactura.Edit:
            return True
        util = qsa.FLUtil()
        if curFactura.valueBuffer("nogenerarasiento"):
            curFactura.setNull("idasiento")
            return True
        if not self.iface.comprobarRegularizacion(curFactura):
            return False
        util = qsa.FLUtil()
        datosAsiento = qsa.Array()
        valoresDefecto = qsa.Array()
        valoresDefecto["codejercicio"] = curFactura.valueBuffer("codejercicio")
        valoresDefecto["coddivisa"] = qsa.from_project("flfactppal").iface.pub_valorDefectoEmpresa("coddivisa")
        curTransaccion = qsa.FLSqlCursor("facturascli")
        curTransaccion.transaction(False)
        try:
            datosAsiento = self.iface.regenerarAsiento(curFactura, valoresDefecto)
            if datosAsiento.error:
                raise Exception(util.translate("scripts", "Error al regenerar el asiento"))
            numProveedor = curFactura.valueBuffer("numproveedor")
            concepto = ""
            if not numProveedor or numProveedor == "":
                concepto = util.translate("scripts", "Su factura ") + curFactura.valueBuffer("codigo")
            else:
                concepto = util.translate("scripts", "Su factura ") + numProveedor

            concepto += qsa.ustr(" - ", curFactura.valueBuffer("nombre"))
            ctaProveedor = self.iface.datosCtaProveedor(curFactura, valoresDefecto)
            if ctaProveedor.error != 0:
                raise Exception(util.translate("scripts", "Error al obtener la subcuenta del proveedor"))
            regimenIVA = util.sqlSelect(
                "proveedores", "regimeniva", qsa.ustr("codproveedor = '", curFactura.valueBuffer("codproveedor"), "'")
            )
            for case in qsa.switch(regimenIVA):
                if case("UE"):
                    if not self.iface.generarPartidasProveedor(
                        curFactura, datosAsiento.idasiento, valoresDefecto, ctaProveedor, concepto, True
                    ):
                        raise Exception(util.translate("scripts", "Error al generar la partida de proveedor"))
                    if not self.iface.generarPartidasIRPFProv(curFactura, datosAsiento.idasiento, valoresDefecto):
                        raise Exception(util.translate("scripts", "Error al generar la partida de IRPF"))
                    if not self.iface.generarPartidasRecFinProv(curFactura, datosAsiento.idasiento, valoresDefecto):
                        raise Exception(util.translate("scripts", "Error al generar la partida recargo financiero"))
                    if not self.iface.generarPartidasIVAProv(
                        curFactura, datosAsiento.idasiento, valoresDefecto, ctaProveedor, concepto
                    ):
                        raise Exception(util.translate("scripts", "Error al generar la partida de IVA"))
                    if not self.iface.generarPartidasCompra(
                        curFactura, datosAsiento.idasiento, valoresDefecto, concepto
                    ):
                        raise Exception(util.translate("scripts", "Error al generar la partida de compras"))
                    break

                if case("Exento"):
                    if not self.iface.generarPartidasProveedor(
                        curFactura, datosAsiento.idasiento, valoresDefecto, ctaProveedor, concepto, True
                    ):
                        raise Exception(util.translate("scripts", "Error al generar la partida de proveedor"))
                    if not self.iface.generarPartidasRecFinProv(curFactura, datosAsiento.idasiento, valoresDefecto):
                        raise Exception(util.translate("scripts", "Error al generar la partida de recargo financiero"))
                    if not self.iface.generarPartidasIRPFProv(curFactura, datosAsiento.idasiento, valoresDefecto):
                        raise Exception(util.translate("scripts", "Error al generar la partida de IRPF"))
                    if not self.iface.generarPartidasIVAProv(
                        curFactura, datosAsiento.idasiento, valoresDefecto, ctaProveedor, concepto
                    ):
                        raise Exception(util.translate("scripts", "Error al generar la partida de IVA"))
                    if not self.iface.generarPartidasCompra(
                        curFactura, datosAsiento.idasiento, valoresDefecto, concepto
                    ):
                        raise Exception(util.translate("scripts", "Error al generar la partida de compras"))
                    break

                if case():
                    if not self.iface.generarPartidasProveedor(
                        curFactura, datosAsiento.idasiento, valoresDefecto, ctaProveedor, concepto
                    ):
                        raise Exception(util.translate("scripts", "Error al generar la partida de proveedor"))
                    if not self.iface.generarPartidasIRPFProv(curFactura, datosAsiento.idasiento, valoresDefecto):
                        raise Exception(util.translate("scripts", "Error al generar la partida de IRPF"))
                    if not self.iface.generarPartidasRecFinProv(curFactura, datosAsiento.idasiento, valoresDefecto):
                        raise Exception(util.translate("scripts", "Error al generar la partida de recargo financiero"))
                    if not self.iface.generarPartidasIVAProv(
                        curFactura, datosAsiento.idasiento, valoresDefecto, ctaProveedor, concepto
                    ):
                        raise Exception(util.translate("scripts", "Error al generar la partida de IVA"))
                    if not self.iface.generarPartidasCompra(
                        curFactura, datosAsiento.idasiento, valoresDefecto, concepto
                    ):
                        raise Exception(util.translate("scripts", "Error al generar la partida de compra"))

            curFactura.setValueBuffer("idasiento", datosAsiento.idasiento)
            if curFactura.valueBuffer("deabono"):
                if not self.iface.asientoFacturaAbonoProv(curFactura, valoresDefecto):
                    raise Exception(util.translate("scripts", "Error al modificar el asiento de abono"))
            if not qsa.from_project("flcontppal").iface.pub_comprobarAsiento(datosAsiento.idasiento):
                raise Exception(util.translate("scripts", "Error al comprobar el asiento"))

        except Exception:
            e = qsa.format_exc()
            curTransaccion.rollback()
            qsa.MessageBox.warning(
                qsa.ustr(
                    util.translate("scripts", "Error al generar el asiento correspondiente a la factura %s:")
                    % (str(curFactura.valueBuffer("codigo"))),
                    "\n",
                    e,
                ),
                qsa.MessageBox.Ok,
                qsa.MessageBox.NoButton,
            )
            return False

        curTransaccion.commit()
        return True

    def oficial_generarPartidasCompra(self, curFactura=None, idAsiento=None, valoresDefecto=None, concepto=None):
        ctaCompras = qsa.Array()
        util = qsa.FLUtil()
        monedaSistema = valoresDefecto.coddivisa == curFactura.valueBuffer("coddivisa")
        debe = 0
        debeME = 0
        idUltimaPartida = 0
        qrySubcuentas = qsa.FLSqlQuery()
        # WITH_START
        qrySubcuentas.setTablesList("lineasfacturasprov")
        qrySubcuentas.setSelect("codsubcuenta, SUM(pvptotal)")
        qrySubcuentas.setFrom("lineasfacturasprov")
        qrySubcuentas.setWhere(qsa.ustr("idfactura = ", curFactura.valueBuffer("idfactura"), " GROUP BY codsubcuenta"))
        # WITH_END
        try:
            qrySubcuentas.setForwardOnly(True)
        except Exception:
            e = qsa.format_exc()

        if not qrySubcuentas.exec_():
            return False
        if qrySubcuentas.size() == 0:
            ctaCompras = self.iface.datosCtaEspecial("COMPRA", valoresDefecto.codejercicio)
            if ctaCompras.error != 0:
                qsa.MessageBox.warning(
                    util.translate(
                        "scripts", "No existe ninguna subcuenta marcada como cuenta especial de COMPRA para %s"
                    )
                    % (str(valoresDefecto.codejercicio)),
                    qsa.MessageBox.Ok,
                    qsa.MessageBox.NoButton,
                )
                return False
            if monedaSistema:
                debe = self.iface.netoComprasFacturaProv(curFactura)
                debeME = 0
            else:
                debe = qsa.parseFloat(curFactura.valueBuffer("neto")) * qsa.parseFloat(
                    curFactura.valueBuffer("tasaconv")
                )
                debeME = self.iface.netoComprasFacturaProv(curFactura)

            debe = util.roundFieldValue(debe, "co_partidas", "debe")
            debeME = util.roundFieldValue(debeME, "co_partidas", "debeme")
            curPartida = qsa.FLSqlCursor("co_partidas")
            # WITH_START
            curPartida.setModeAccess(curPartida.Insert)
            curPartida.refreshBuffer()
            curPartida.setValueBuffer("idsubcuenta", ctaCompras.idsubcuenta)
            curPartida.setValueBuffer("codsubcuenta", ctaCompras.codsubcuenta)
            curPartida.setValueBuffer("idasiento", idAsiento)
            curPartida.setValueBuffer("debe", debe)
            curPartida.setValueBuffer("haber", 0)
            curPartida.setValueBuffer("coddivisa", curFactura.valueBuffer("coddivisa"))
            curPartida.setValueBuffer("tasaconv", curFactura.valueBuffer("tasaconv"))
            curPartida.setValueBuffer("debeME", debeME)
            curPartida.setValueBuffer("haberME", 0)
            # WITH_END
            self.iface.datosPartidaFactura(curPartida, curFactura, "proveedor", concepto)
            if not curPartida.commitBuffer():
                return False
            idUltimaPartida = curPartida.valueBuffer("idpartida")

        else:
            while qrySubcuentas.next():
                if qrySubcuentas.value(0) == "" or not qrySubcuentas.value(0):
                    ctaCompras = self.iface.datosCtaEspecial("COMPRA", valoresDefecto.codejercicio)
                    if ctaCompras.error != 0:
                        return False
                else:
                    ctaCompras.codsubcuenta = qrySubcuentas.value(0)
                    ctaCompras.idsubcuenta = util.sqlSelect(
                        "co_subcuentas",
                        "idsubcuenta",
                        qsa.ustr(
                            "codsubcuenta = '",
                            qrySubcuentas.value(0),
                            "' AND codejercicio = '",
                            valoresDefecto.codejercicio,
                            "'",
                        ),
                    )
                    if not ctaCompras.idsubcuenta:
                        qsa.MessageBox.warning(
                            util.translate("scripts", "No existe la subcuenta ")
                            + ctaCompras.codsubcuenta
                            + util.translate("scripts", " correspondiente al ejercicio ")
                            + valoresDefecto.codejercicio
                            + util.translate(
                                "scripts", ".\nPara poder crear la factura debe crear antes esta subcuenta"
                            ),
                            qsa.MessageBox.Ok,
                            qsa.MessageBox.NoButton,
                        )
                        return False

                if monedaSistema:
                    debe = qsa.parseFloat(qrySubcuentas.value(1))
                    debeME = 0
                else:
                    debe = qsa.parseFloat(qrySubcuentas.value(1)) * qsa.parseFloat(curFactura.valueBuffer("tasaconv"))
                    debeME = qsa.parseFloat(qrySubcuentas.value(1))

                debe = util.roundFieldValue(debe, "co_partidas", "debe")
                debeME = util.roundFieldValue(debeME, "co_partidas", "debeme")
                curPartida = qsa.FLSqlCursor("co_partidas")
                # WITH_START
                curPartida.setModeAccess(curPartida.Insert)
                curPartida.refreshBuffer()
                curPartida.setValueBuffer("idsubcuenta", ctaCompras.idsubcuenta)
                curPartida.setValueBuffer("codsubcuenta", ctaCompras.codsubcuenta)
                curPartida.setValueBuffer("idasiento", idAsiento)
                curPartida.setValueBuffer("debe", debe)
                curPartida.setValueBuffer("haber", 0)
                curPartida.setValueBuffer("coddivisa", curFactura.valueBuffer("coddivisa"))
                curPartida.setValueBuffer("tasaconv", curFactura.valueBuffer("tasaconv"))
                curPartida.setValueBuffer("debeME", debeME)
                curPartida.setValueBuffer("haberME", 0)
                # WITH_END
                self.iface.datosPartidaFactura(curPartida, curFactura, "proveedor", concepto)
                if not curPartida.commitBuffer():
                    return False
                idUltimaPartida = curPartida.valueBuffer("idpartida")

        if not monedaSistema:
            debe = qsa.parseFloat(
                util.sqlSelect(
                    "co_partidas",
                    "SUM(haber - debe)",
                    qsa.ustr("idasiento = ", idAsiento, " AND idpartida <> ", idUltimaPartida),
                )
            )
            if debe and not qsa.isNaN(debe) and debe != 0:
                debe = qsa.parseFloat(util.roundFieldValue(debe, "co_partidas", "debe"))
                if not util.sqlUpdate("co_partidas", "debe", debe, qsa.ustr("idpartida = ", idUltimaPartida)):
                    return False

        return True

    def oficial_generarPartidasIVAProv(
        self, curFactura=None, idAsiento=None, valoresDefecto=None, ctaProveedor=None, concepto=None
    ):
        util = qsa.FLUtil()
        haber = 0
        haberME = 0
        baseImponible = 0
        monedaSistema = valoresDefecto.coddivisa == curFactura.valueBuffer("coddivisa")
        recargo = 0
        iva = 0
        regimenIVA = util.sqlSelect(
            "proveedores", "regimeniva", qsa.ustr("codproveedor = '", curFactura.valueBuffer("codproveedor"), "'")
        )
        codCuentaEspIVA = ""
        qryIva = qsa.FLSqlQuery()
        qryIva.setTablesList("lineasivafactprov")
        if regimenIVA == "UE":
            qryIva.setSelect("neto, iva, neto*iva/100, recargo, neto*recargo/100, codimpuesto")
        else:
            qryIva.setSelect("neto, iva, totaliva, recargo, totalrecargo, codimpuesto")

        qryIva.setFrom("lineasivafactprov")
        qryIva.setWhere(qsa.ustr("idfactura = ", curFactura.valueBuffer("idfactura")))
        try:
            qryIva.setForwardOnly(True)
        except Exception:
            e = qsa.format_exc()

        if not qryIva.exec_():
            return False
        while qryIva.next():
            iva = qsa.parseFloat(qryIva.value("iva"))
            if qsa.isNaN(iva):
                iva = 0
            recargo = qsa.parseFloat(qryIva.value("recargo"))
            if qsa.isNaN(recargo):
                recargo = 0
            if monedaSistema:
                debe = qsa.parseFloat(qryIva.value(2))
                debeME = 0
                baseImponible = qsa.parseFloat(qryIva.value(0))
            else:
                debe = qsa.parseFloat(qryIva.value(2)) * qsa.parseFloat(curFactura.valueBuffer("tasaconv"))
                debeME = qsa.parseFloat(qryIva.value(2))
                baseImponible = qsa.parseFloat(qryIva.value(0)) * qsa.parseFloat(curFactura.valueBuffer("tasaconv"))

            debe = util.roundFieldValue(debe, "co_partidas", "debe")
            debeME = util.roundFieldValue(debeME, "co_partidas", "debeme")
            baseImponible = util.roundFieldValue(baseImponible, "co_partidas", "baseimponible")
            for case in qsa.switch(regimenIVA):
                if case("UE"):
                    codCuentaEspIVA = "IVASUE"
                    break
                if case("General"):
                    codCuentaEspIVA = "IVASOP"
                    break
                if case("Exento"):
                    codCuentaEspIVA = "IVASEX"
                    break
                if case("Importaciones"):
                    return True
                    break
                if case("Agrario"):
                    codCuentaEspIVA = "IVASRA"
                    break
                if case():
                    codCuentaEspIVA = "IVASOP"

            ctaIvaSop = self.iface.datosCtaIVA(codCuentaEspIVA, valoresDefecto.codejercicio, qryIva.value(5))
            if ctaIvaSop.error != 0:
                qsa.MessageBox.warning(
                    util.translate(
                        "scripts",
                        "Esta factura pertenece al régimen IVA tipo %s.\nNo existe ninguna cuenta contable marcada como tipo especial %s\n\nDebe asociar una cuenta contable a dicho tipo especial en el módulo Principal del área Financiera",
                    )
                    % (str(regimenIVA), str(codCuentaEspIVA)),
                    qsa.MessageBox.Ok,
                    qsa.MessageBox.NoButton,
                    qsa.MessageBox.NoButton,
                )
                return False
            curPartida = qsa.FLSqlCursor("co_partidas")
            # WITH_START
            curPartida.setModeAccess(curPartida.Insert)
            curPartida.refreshBuffer()
            curPartida.setValueBuffer("idsubcuenta", ctaIvaSop.idsubcuenta)
            curPartida.setValueBuffer("codsubcuenta", ctaIvaSop.codsubcuenta)
            curPartida.setValueBuffer("idasiento", idAsiento)
            curPartida.setValueBuffer("debe", debe)
            curPartida.setValueBuffer("haber", 0)
            curPartida.setValueBuffer("baseimponible", baseImponible)
            curPartida.setValueBuffer("iva", iva)
            curPartida.setValueBuffer("recargo", recargo)
            curPartida.setValueBuffer("coddivisa", curFactura.valueBuffer("coddivisa"))
            curPartida.setValueBuffer("tasaconv", curFactura.valueBuffer("tasaconv"))
            curPartida.setValueBuffer("idcontrapartida", ctaProveedor.idsubcuenta)
            curPartida.setValueBuffer("codcontrapartida", ctaProveedor.codsubcuenta)
            curPartida.setValueBuffer("debeME", debeME)
            curPartida.setValueBuffer("haberME", 0)
            curPartida.setValueBuffer("codserie", curFactura.valueBuffer("codserie"))
            curPartida.setValueBuffer("cifnif", curFactura.valueBuffer("cifnif"))
            # WITH_END
            self.iface.datosPartidaFactura(curPartida, curFactura, "proveedor")
            if not curPartida.commitBuffer():
                return False
            if regimenIVA == "UE":
                haber = debe
                haberME = debeME
                codCuentaEspIVA = "IVARUE"
                ctaIvaSop = self.iface.datosCtaIVA("IVARUE", valoresDefecto.codejercicio, qryIva.value(5))
                if ctaIvaSop.error != 0:
                    return False
                curPartida = qsa.FLSqlCursor("co_partidas")
                # WITH_START
                curPartida.setModeAccess(curPartida.Insert)
                curPartida.refreshBuffer()
                curPartida.setValueBuffer("idsubcuenta", ctaIvaSop.idsubcuenta)
                curPartida.setValueBuffer("codsubcuenta", ctaIvaSop.codsubcuenta)
                curPartida.setValueBuffer("idasiento", idAsiento)
                curPartida.setValueBuffer("debe", 0)
                curPartida.setValueBuffer("haber", haber)
                curPartida.setValueBuffer("baseimponible", baseImponible)
                curPartida.setValueBuffer("iva", iva)
                curPartida.setValueBuffer("recargo", recargo)
                curPartida.setValueBuffer("coddivisa", curFactura.valueBuffer("coddivisa"))
                curPartida.setValueBuffer("tasaconv", curFactura.valueBuffer("tasaconv"))
                curPartida.setValueBuffer("idcontrapartida", ctaProveedor.idsubcuenta)
                curPartida.setValueBuffer("codcontrapartida", ctaProveedor.codsubcuenta)
                curPartida.setValueBuffer("debeME", 0)
                curPartida.setValueBuffer("haberME", haberME)
                curPartida.setValueBuffer("codserie", curFactura.valueBuffer("codserie"))
                curPartida.setValueBuffer("cifnif", curFactura.valueBuffer("cifnif"))
                # WITH_END
                self.iface.datosPartidaFactura(curPartida, curFactura, "proveedor", concepto)
                if not curPartida.commitBuffer():
                    return False

            if monedaSistema:
                debe = qsa.parseFloat(qryIva.value(4))
                debeME = 0
            else:
                debe = qsa.parseFloat(qryIva.value(4)) * qsa.parseFloat(curFactura.valueBuffer("tasaconv"))
                debeME = qsa.parseFloat(qryIva.value(4))

            debe = util.roundFieldValue(debe, "co_partidas", "debe")
            debeME = util.roundFieldValue(debeME, "co_partidas", "debeme")
            if qsa.parseFloat(debe) != 0:
                ctaRecargo = self.iface.datosCtaIVA("IVADEU", valoresDefecto.codejercicio, qryIva.value(5))
                if ctaRecargo.error != 0:
                    return False
                curPartida = qsa.FLSqlCursor("co_partidas")
                # WITH_START
                curPartida.setModeAccess(curPartida.Insert)
                curPartida.refreshBuffer()
                curPartida.setValueBuffer("idsubcuenta", ctaRecargo.idsubcuenta)
                curPartida.setValueBuffer("codsubcuenta", ctaRecargo.codsubcuenta)
                curPartida.setValueBuffer("idasiento", idAsiento)
                curPartida.setValueBuffer("debe", debe)
                curPartida.setValueBuffer("haber", 0)
                curPartida.setValueBuffer("baseimponible", baseImponible)
                curPartida.setValueBuffer("iva", iva)
                curPartida.setValueBuffer("recargo", recargo)
                curPartida.setValueBuffer("coddivisa", curFactura.valueBuffer("coddivisa"))
                curPartida.setValueBuffer("tasaconv", curFactura.valueBuffer("tasaconv"))
                curPartida.setValueBuffer("idcontrapartida", ctaProveedor.idsubcuenta)
                curPartida.setValueBuffer("codcontrapartida", ctaProveedor.codsubcuenta)
                curPartida.setValueBuffer("debeME", debeME)
                curPartida.setValueBuffer("haberME", 0)
                curPartida.setValueBuffer("codserie", curFactura.valueBuffer("codserie"))
                curPartida.setValueBuffer("cifnif", curFactura.valueBuffer("cifnif"))
                # WITH_END
                self.iface.datosPartidaFactura(curPartida, curFactura, "proveedor", concepto)
                if not curPartida.commitBuffer():
                    return False

        return True

    def oficial_generarPartidasProveedor(
        self, curFactura=None, idAsiento=None, valoresDefecto=None, ctaProveedor=None, concepto=None, sinIVA=None
    ):
        util = qsa.FLUtil()
        haber = 0
        haberME = 0
        totalIVA = 0
        if sinIVA:
            totalIVA = qsa.parseFloat(curFactura.valueBuffer("totaliva"))
        monedaSistema = valoresDefecto.coddivisa == curFactura.valueBuffer("coddivisa")
        if monedaSistema:
            haber = qsa.parseFloat(curFactura.valueBuffer("total"))
            haber -= totalIVA
            haberME = 0
        else:
            haber = (qsa.parseFloat(curFactura.valueBuffer("total")) - totalIVA) * qsa.parseFloat(
                curFactura.valueBuffer("tasaconv")
            )
            haberME = qsa.parseFloat(curFactura.valueBuffer("total"))

        haber = util.roundFieldValue(haber, "co_partidas", "haber")
        haberME = util.roundFieldValue(haberME, "co_partidas", "haberme")
        curPartida = qsa.FLSqlCursor("co_partidas")
        # WITH_START
        curPartida.setModeAccess(curPartida.Insert)
        curPartida.refreshBuffer()
        curPartida.setValueBuffer("idsubcuenta", ctaProveedor.idsubcuenta)
        curPartida.setValueBuffer("codsubcuenta", ctaProveedor.codsubcuenta)
        curPartida.setValueBuffer("idasiento", idAsiento)
        curPartida.setValueBuffer("debe", 0)
        curPartida.setValueBuffer("haber", haber)
        curPartida.setValueBuffer("coddivisa", curFactura.valueBuffer("coddivisa"))
        curPartida.setValueBuffer("tasaconv", curFactura.valueBuffer("tasaconv"))
        curPartida.setValueBuffer("debeME", 0)
        curPartida.setValueBuffer("haberME", haberME)
        # WITH_END
        self.iface.datosPartidaFactura(curPartida, curFactura, "proveedor", concepto)
        if not curPartida.commitBuffer():
            return False
        return True

    def oficial_generarPartidasRecFinProv(self, curFactura=None, idAsiento=None, valoresDefecto=None):
        util = qsa.FLUtil()
        recFinanciero = qsa.parseFloat(curFactura.valueBuffer("recfinanciero") * curFactura.valueBuffer("neto") / 100)
        if not recFinanciero:
            return True
        debe = 0
        debeME = 0
        ctaRecfin = qsa.Array()
        ctaRecfin = self.iface.datosCtaEspecial("GTORF", valoresDefecto.codejercicio)
        if ctaRecfin.error != 0:
            qsa.MessageBox.warning(
                util.translate(
                    "scripts",
                    "No tiene ninguna cuenta contable marcada como cuenta especial\nGTORF (recargo financiero en gastos).\nDebe asociar una cuenta contable a esta cuenta especial en el módulo Principal del área Financiera",
                ),
                qsa.MessageBox.Ok,
                qsa.MessageBox.NoButton,
                qsa.MessageBox.NoButton,
            )
            return False
        monedaSistema = valoresDefecto.coddivisa == curFactura.valueBuffer("coddivisa")
        if monedaSistema:
            debe = recFinanciero
            debeME = 0
        else:
            debe = recFinanciero * qsa.parseFloat(curFactura.valueBuffer("tasaconv"))
            debeME = recFinanciero

        debe = util.roundFieldValue(debe, "co_partidas", "debe")
        debeME = util.roundFieldValue(debeME, "co_partidas", "debeme")
        curPartida = qsa.FLSqlCursor("co_partidas")
        # WITH_START
        curPartida.setModeAccess(curPartida.Insert)
        curPartida.refreshBuffer()
        curPartida.setValueBuffer("idsubcuenta", ctaRecfin.idsubcuenta)
        curPartida.setValueBuffer("codsubcuenta", ctaRecfin.codsubcuenta)
        curPartida.setValueBuffer("idasiento", idAsiento)
        curPartida.setValueBuffer("debe", debe)
        curPartida.setValueBuffer("haber", 0)
        curPartida.setValueBuffer("coddivisa", curFactura.valueBuffer("coddivisa"))
        curPartida.setValueBuffer("tasaconv", curFactura.valueBuffer("tasaconv"))
        curPartida.setValueBuffer("debeME", debeME)
        curPartida.setValueBuffer("haberME", 0)
        # WITH_END
        self.iface.datosPartidaFactura(curPartida, curFactura, "proveedor")
        if not curPartida.commitBuffer():
            return False
        return True

    def oficial_datosCtaEspecial(self, ctaEsp=None, codEjercicio=None):
        datos = qsa.Array()
        q = qsa.FLSqlQuery()
        # WITH_START
        q.setTablesList("co_subcuentas,co_cuentasesp")
        q.setSelect("s.idsubcuenta, s.codsubcuenta")
        q.setFrom("co_cuentasesp ce INNER JOIN co_subcuentas s ON ce.codsubcuenta = s.codsubcuenta")
        q.setWhere(
            qsa.ustr(
                "ce.idcuentaesp = '", ctaEsp, "' AND s.codejercicio = '", codEjercicio, "'  ORDER BY s.codsubcuenta"
            )
        )
        # WITH_END
        try:
            q.setForwardOnly(True)
        except Exception:
            e = qsa.format_exc()

        if not q.exec_():
            datos["error"] = 2
            return datos
        if q.next():
            datos["error"] = 0
            datos["idsubcuenta"] = q.value(0)
            datos["codsubcuenta"] = q.value(1)
            return datos

        # WITH_START
        q.setTablesList("co_cuentas,co_subcuentas,co_cuentasesp")
        q.setSelect("s.idsubcuenta, s.codsubcuenta")
        q.setFrom(
            "co_cuentasesp ce INNER JOIN co_cuentas c ON ce.codcuenta = c.codcuenta INNER JOIN co_subcuentas s ON c.idcuenta = s.idcuenta"
        )
        q.setWhere(
            qsa.ustr(
                "ce.idcuentaesp = '", ctaEsp, "' AND c.codejercicio = '", codEjercicio, "' ORDER BY s.codsubcuenta"
            )
        )
        # WITH_END
        try:
            q.setForwardOnly(True)
        except Exception:
            e = qsa.format_exc()

        if not q.exec_():
            datos["error"] = 2
            return datos
        if q.next():
            datos["error"] = 0
            datos["idsubcuenta"] = q.value(0)
            datos["codsubcuenta"] = q.value(1)
            return datos

        # WITH_START
        q.setTablesList("co_cuentas,co_subcuentas")
        q.setSelect("s.idsubcuenta, s.codsubcuenta")
        q.setFrom("co_cuentas c INNER JOIN co_subcuentas s ON c.idcuenta = s.idcuenta")
        q.setWhere(
            qsa.ustr("c.idcuentaesp = '", ctaEsp, "' AND c.codejercicio = '", codEjercicio, "' ORDER BY s.codsubcuenta")
        )
        # WITH_END
        try:
            q.setForwardOnly(True)
        except Exception:
            e = qsa.format_exc()

        if not q.exec_():
            datos["error"] = 2
            return datos
        if not q.next():
            if self.iface.consultarCtaEspecial(ctaEsp, codEjercicio):
                return self.iface.datosCtaEspecial(ctaEsp, codEjercicio)
            else:
                datos["error"] = 1
                return datos

        datos["error"] = 0
        datos["idsubcuenta"] = q.value(0)
        datos["codsubcuenta"] = q.value(1)
        return datos

    def oficial_consultarCtaEspecial(self, ctaEsp=None, codEjercicio=None):
        util = qsa.FLUtil()
        for case in qsa.switch(ctaEsp):
            if case("IVASUE"):
                res = qsa.MessageBox.warning(
                    util.translate(
                        "scripts",
                        "No tiene establecida la subcuenta de IVA soportado para adquisiciones intracomunitaras (IVASUE).\nEsta subcuenta es necesaria para almacenar información útil para informes como el de facturas emitidas o el modelo 300.\n¿Desea indicar cuál es esta subcuenta ahora?",
                    ),
                    qsa.MessageBox.Yes,
                    qsa.MessageBox.No,
                )
                if res != qsa.MessageBox.Yes:
                    return False
                return self.iface.crearCtaEspecial(
                    "IVASUE",
                    "subcuenta",
                    codEjercicio,
                    util.translate("scripts", "IVA soportado en adquisiciones intracomunitarias U.E."),
                )
                break

            if case("IVARUE"):
                res = qsa.MessageBox.warning(
                    util.translate(
                        "scripts",
                        "No tiene establecida la subcuenta de IVA repercutido para adquisiciones intracomunitaras (IVARUE).\nEsta subcuenta es necesaria para almacenar información útil para informes como el de facturas emitidas o el modelo 300.\n¿Desea indicar cuál es esta subcuenta ahora?",
                    ),
                    qsa.MessageBox.Yes,
                    qsa.MessageBox.No,
                )
                if res != qsa.MessageBox.Yes:
                    return False
                return self.iface.crearCtaEspecial(
                    "IVARUE",
                    "subcuenta",
                    codEjercicio,
                    util.translate("scripts", "IVA repercutido en adquisiciones intracomunitarias U.E."),
                )
                break

            if case("IVAEUE"):
                res = qsa.MessageBox.warning(
                    util.translate(
                        "scripts",
                        "No tiene establecida la subcuenta de IVA para entregas intracomunitaras (IVAEUE).\nEsta subcuenta es necesaria para almacenar información útil para informes como el de facturas emitidas o el modelo 300.\n¿Desea indicar cuál es esta subcuenta ahora?",
                    ),
                    qsa.MessageBox.Yes,
                    qsa.MessageBox.No,
                )
                if res != qsa.MessageBox.Yes:
                    return False
                return self.iface.crearCtaEspecial(
                    "IVAEUE",
                    "subcuenta",
                    codEjercicio,
                    util.translate("scripts", "IVA en entregas intracomunitarias U.E."),
                )
                break

            if case():
                return False

        return False

    def oficial_datosCtaIVA(self, tipo=None, codEjercicio=None, codImpuesto=None):
        util = qsa.FLUtil()
        datos = qsa.Array()
        codSubcuenta = ""
        if not codImpuesto or codImpuesto == "":
            codSubcuenta = util.sqlSelect(
                "co_subcuentas",
                "codsubcuenta",
                qsa.ustr("idcuentaesp = '", tipo, "' AND codejercicio = '", codEjercicio, "' ORDER BY codsubcuenta"),
            )
            if not codSubcuenta or codSubcuenta == "":
                return self.iface.datosCtaEspecial(tipo, codEjercicio)
        if tipo == "IVAREP":
            codSubcuenta = util.sqlSelect("impuestos", "codsubcuentarep", qsa.ustr("codimpuesto = '", codImpuesto, "'"))
        if tipo == "IVASOP":
            codSubcuenta = util.sqlSelect("impuestos", "codsubcuentasop", qsa.ustr("codimpuesto = '", codImpuesto, "'"))
        if tipo == "IVAACR":
            codSubcuenta = util.sqlSelect("impuestos", "codsubcuentaacr", qsa.ustr("codimpuesto = '", codImpuesto, "'"))
        if tipo == "IVARRE":
            codSubcuenta = False
            curPrueba = qsa.FLSqlCursor("impuestos")
            if curPrueba.fieldType("codsubcuentaivarepre") != 0:
                codSubcuenta = util.sqlSelect(
                    "impuestos", "codsubcuentaivarepre", qsa.ustr("codimpuesto = '", codImpuesto, "'")
                )
            if not codSubcuenta:
                codSubcuenta = util.sqlSelect(
                    "impuestos", "codsubcuentaacr", qsa.ustr("codimpuesto = '", codImpuesto, "'")
                )

        if tipo == "IVADEU":
            codSubcuenta = util.sqlSelect("impuestos", "codsubcuentadeu", qsa.ustr("codimpuesto = '", codImpuesto, "'"))
        if tipo == "IVARUE":
            codSubcuenta = util.sqlSelect(
                "impuestos", "codsubcuentaivadevadue", qsa.ustr("codimpuesto = '", codImpuesto, "'")
            )
        if tipo == "IVASUE":
            codSubcuenta = util.sqlSelect(
                "impuestos", "codsubcuentaivadedadue", qsa.ustr("codimpuesto = '", codImpuesto, "'")
            )
        if tipo == "IVAEUE":
            codSubcuenta = util.sqlSelect(
                "impuestos", "codsubcuentaivadeventue", qsa.ustr("codimpuesto = '", codImpuesto, "'")
            )
        if tipo == "IVASIM":
            curPrueba = qsa.FLSqlCursor("impuestos")
            if curPrueba.fieldType("codsubcuentaivasopimp") != 0:
                codSubcuenta = util.sqlSelect(
                    "impuestos", "codsubcuentaivasopimp", qsa.ustr("codimpuesto = '", codImpuesto, "'")
                )
            else:
                tipo = "IVASOP"

        if tipo == "IVARXP":
            curPrueba = qsa.FLSqlCursor("impuestos")
            if curPrueba.fieldType("codsubcuentaivarepexp") != 0:
                codSubcuenta = util.sqlSelect(
                    "impuestos", "codsubcuentaivarepexp", qsa.ustr("codimpuesto = '", codImpuesto, "'")
                )
            else:
                tipo = "IVARXP"

        if tipo == "IVAREX":
            curPrueba = qsa.FLSqlCursor("impuestos")
            if curPrueba.fieldType("codsubcuentaivarepexe") != 0:
                codSubcuenta = util.sqlSelect(
                    "impuestos", "codsubcuentaivarepexe", qsa.ustr("codimpuesto = '", codImpuesto, "'")
                )
            else:
                tipo = "IVAREX"

        if tipo == "IVASEX":
            curPrueba = qsa.FLSqlCursor("impuestos")
            if curPrueba.fieldType("codsubcuentaivasopexe") != 0:
                codSubcuenta = util.sqlSelect(
                    "impuestos", "codsubcuentaivasopexe", qsa.ustr("codimpuesto = '", codImpuesto, "'")
                )
            else:
                tipo = "IVASEX"

        if not codSubcuenta or codSubcuenta == "":
            codSubcuenta = util.sqlSelect(
                "co_subcuentas",
                "codsubcuenta",
                qsa.ustr("idcuentaesp = '", tipo, "' AND codejercicio = '", codEjercicio, "' ORDER BY codsubcuenta"),
            )
            if not codSubcuenta or codSubcuenta == "":
                return self.iface.datosCtaEspecial(tipo, codEjercicio)
        q = qsa.FLSqlQuery()
        # WITH_START
        q.setTablesList("co_subcuentas")
        q.setSelect("idsubcuenta, codsubcuenta")
        q.setFrom("co_subcuentas")
        q.setWhere(qsa.ustr("codsubcuenta = '", codSubcuenta, "' AND codejercicio = '", codEjercicio, "'"))
        # WITH_END
        try:
            q.setForwardOnly(True)
        except Exception:
            e = qsa.format_exc()

        if not q.exec_():
            datos["error"] = 2
            return datos
        if not q.next():
            return self.iface.datosCtaEspecial(tipo, codEjercicio)
        datos["error"] = 0
        datos["idsubcuenta"] = q.value(0)
        datos["codsubcuenta"] = q.value(1)
        return datos

    def oficial_datosCtaVentas(self, codEjercicio=None, codSerie=None):
        util = qsa.FLUtil()
        datos = qsa.Array()
        codCuenta = util.sqlSelect("series", "codcuenta", qsa.ustr("codserie = '", codSerie, "'"))
        if qsa.parseString(codCuenta) == "":
            return self.iface.datosCtaEspecial("VENTAS", codEjercicio)
        q = qsa.FLSqlQuery()
        # WITH_START
        q.setTablesList("co_cuentas,co_subcuentas")
        q.setSelect("idsubcuenta, codsubcuenta")
        q.setFrom("co_cuentas c INNER JOIN co_subcuentas s ON c.idcuenta = s.idcuenta")
        q.setWhere(
            qsa.ustr("c.codcuenta = '", codCuenta, "' AND c.codejercicio = '", codEjercicio, "' ORDER BY codsubcuenta")
        )
        # WITH_END
        try:
            q.setForwardOnly(True)
        except Exception:
            e = qsa.format_exc()

        if not q.exec_():
            datos["error"] = 2
            return datos
        if not q.next():
            datos["error"] = 1
            return datos
        datos["error"] = 0
        datos["idsubcuenta"] = q.value(0)
        datos["codsubcuenta"] = q.value(1)
        return datos

    def oficial_datosCtaCliente(self, curFactura=None, valoresDefecto=None):
        return qsa.from_project("flfactppal").iface.pub_datosCtaCliente(
            curFactura.valueBuffer("codcliente"), valoresDefecto
        )

    def oficial_datosCtaProveedor(self, curFactura=None, valoresDefecto=None):
        return qsa.from_project("flfactppal").iface.pub_datosCtaProveedor(
            curFactura.valueBuffer("codproveedor"), valoresDefecto
        )

    def oficial_asientoFacturaAbonoCli(self, curFactura=None, valoresDefecto=None):
        idAsiento = qsa.parseString(curFactura.valueBuffer("idasiento"))
        idFactura = curFactura.valueBuffer("idfactura")
        curPartidas = qsa.FLSqlCursor("co_partidas")
        debe = 0
        haber = 0
        debeME = 0
        haberME = 0
        aux = 0
        util = qsa.FLUtil()
        curPartidas.select(qsa.ustr("idasiento = '", idAsiento, "'"))
        while curPartidas.next():
            curPartidas.setModeAccess(curPartidas.Edit)
            curPartidas.refreshBuffer()
            debe = qsa.parseFloat(curPartidas.valueBuffer("debe"))
            haber = qsa.parseFloat(curPartidas.valueBuffer("haber"))
            debeME = qsa.parseFloat(curPartidas.valueBuffer("debeme"))
            haberME = qsa.parseFloat(curPartidas.valueBuffer("haberme"))
            aux = debe
            debe = haber * -1
            haber = aux * -1
            aux = debeME
            debeME = haberME * -1
            haberME = aux * -1
            debe = util.roundFieldValue(debe, "co_partidas", "debe")
            haber = util.roundFieldValue(haber, "co_partidas", "haber")
            debeME = util.roundFieldValue(debeME, "co_partidas", "debeme")
            haberME = util.roundFieldValue(haberME, "co_partidas", "haberme")
            curPartidas.setValueBuffer("debe", debe)
            curPartidas.setValueBuffer("haber", haber)
            curPartidas.setValueBuffer("debeme", debeME)
            curPartidas.setValueBuffer("haberme", haberME)
            if not curPartidas.commitBuffer():
                return False

        qryPartidasVenta = qsa.FLSqlQuery()
        qryPartidasVenta.setTablesList("co_partidas,co_subcuentas,co_cuentas")
        qryPartidasVenta.setSelect("p.idsubcuenta, p.codsubcuenta")
        qryPartidasVenta.setFrom(
            "co_partidas p INNER JOIN co_subcuentas s ON s.idsubcuenta = p.idsubcuenta INNER JOIN co_cuentas c ON c.idcuenta = s.idcuenta "
        )
        qryPartidasVenta.setWhere(qsa.ustr("c.idcuentaesp = 'VENTAS' AND idasiento = ", idAsiento))
        try:
            qryPartidasVenta.setForwardOnly(True)
        except Exception:
            e = qsa.format_exc()

        if not qryPartidasVenta.exec_():
            return False
        if qryPartidasVenta.size == 0:
            return True
        curPartidasVenta = qsa.FLSqlCursor("co_partidas")
        ctaDevolVentas = False
        codSubcuentaDev = ""
        while qryPartidasVenta.next():
            codSubcuentaDev = qryPartidasVenta.value("p.codsubcuenta")
            if not self.iface.esSubcuentaEspecial(codSubcuentaDev, valoresDefecto.codejercicio, "VENTAS"):
                continue
            if not ctaDevolVentas:
                ctaDevolVentas = self.iface.datosCtaEspecial("DEVVEN", valoresDefecto.codejercicio)
                if ctaDevolVentas.error == 1:
                    qsa.MessageBox.warning(
                        util.translate(
                            "scripts",
                            "No tiene definida una subcuenta especial de devoluciones de ventas.\nEl asiento asociado a la factura no puede ser creado",
                        ),
                        qsa.MessageBox.Ok,
                        qsa.MessageBox.NoButton,
                        qsa.MessageBox.NoButton,
                    )
                    return False
                if ctaDevolVentas.error == 2:
                    return False

            curPartidasVenta.select(
                qsa.ustr("idasiento = ", idAsiento, " AND idsubcuenta = ", qryPartidasVenta.value(0))
            )
            curPartidasVenta.first()
            curPartidasVenta.setModeAccess(curPartidasVenta.Edit)
            curPartidasVenta.refreshBuffer()
            curPartidasVenta.setValueBuffer("idsubcuenta", ctaDevolVentas.idsubcuenta)
            curPartidasVenta.setValueBuffer("codsubcuenta", ctaDevolVentas.codsubcuenta)
            if not curPartidasVenta.commitBuffer():
                return False

        return True

    def oficial_asientoFacturaAbonoProv(self, curFactura=None, valoresDefecto=None):
        idAsiento = qsa.parseString(curFactura.valueBuffer("idasiento"))
        idFactura = curFactura.valueBuffer("idfactura")
        curPartidas = qsa.FLSqlCursor("co_partidas")
        debe = 0
        haber = 0
        debeME = 0
        haberME = 0
        aux = 0
        util = qsa.FLUtil()
        curPartidas.select(qsa.ustr("idasiento = '", idAsiento, "'"))
        while curPartidas.next():
            curPartidas.setModeAccess(curPartidas.Edit)
            curPartidas.refreshBuffer()
            debe = qsa.parseFloat(curPartidas.valueBuffer("debe"))
            haber = qsa.parseFloat(curPartidas.valueBuffer("haber"))
            debeME = qsa.parseFloat(curPartidas.valueBuffer("debeme"))
            haberME = qsa.parseFloat(curPartidas.valueBuffer("haberme"))
            aux = debe
            debe = haber * -1
            haber = aux * -1
            aux = debeME
            debeME = haberME * -1
            haberME = aux * -1
            debe = util.roundFieldValue(debe, "co_partidas", "debe")
            haber = util.roundFieldValue(haber, "co_partidas", "haber")
            debeME = util.roundFieldValue(debeME, "co_partidas", "debeme")
            haberME = util.roundFieldValue(haberME, "co_partidas", "haberme")
            curPartidas.setValueBuffer("debe", debe)
            curPartidas.setValueBuffer("haber", haber)
            curPartidas.setValueBuffer("debeme", debeME)
            curPartidas.setValueBuffer("haberme", haberME)
            if not curPartidas.commitBuffer():
                return False

        qryPartidasCompra = qsa.FLSqlQuery()
        qryPartidasCompra.setTablesList("co_partidas,co_subcuentas,co_cuentas")
        qryPartidasCompra.setSelect("p.idsubcuenta,p.codsubcuenta")
        qryPartidasCompra.setFrom(
            "co_partidas p INNER JOIN co_subcuentas s ON s.idsubcuenta = p.idsubcuenta INNER JOIN co_cuentas c ON c.idcuenta = s.idcuenta "
        )
        qryPartidasCompra.setWhere(qsa.ustr("c.idcuentaesp = 'COMPRA' AND idasiento = ", idAsiento))
        try:
            qryPartidasCompra.setForwardOnly(True)
        except Exception:
            e = qsa.format_exc()

        if not qryPartidasCompra.exec_():
            return False
        if qryPartidasCompra.size() == 0:
            return True
        curPartidasCompra = qsa.FLSqlCursor("co_partidas")
        ctaDevolCompra = False
        codSubcuentaDev = ""
        while qryPartidasCompra.next():
            codSubcuentaDev = qryPartidasCompra.value("p.codsubcuenta")
            if not self.iface.esSubcuentaEspecial(codSubcuentaDev, valoresDefecto.codejercicio, "COMPRA"):
                continue
            if not ctaDevolCompra:
                ctaDevolCompra = self.iface.datosCtaEspecial("DEVCOM", valoresDefecto.codejercicio)
                if ctaDevolCompra.error == 1:
                    qsa.MessageBox.warning(
                        util.translate(
                            "scripts",
                            "No tiene definida una subcuenta especial de devoluciones de compras.\nEl asiento asociado a la factura no puede ser creado",
                        ),
                        qsa.MessageBox.Ok,
                        qsa.MessageBox.NoButton,
                        qsa.MessageBox.NoButton,
                    )
                    return False
                if ctaDevolCompra.error == 2:
                    return False

            curPartidasCompra.select(
                qsa.ustr("idasiento = ", idAsiento, " AND idsubcuenta = ", qryPartidasCompra.value(0))
            )
            curPartidasCompra.first()
            curPartidasCompra.setModeAccess(curPartidasCompra.Edit)
            curPartidasCompra.refreshBuffer()
            curPartidasCompra.setValueBuffer("idsubcuenta", ctaDevolCompra.idsubcuenta)
            curPartidasCompra.setValueBuffer("codsubcuenta", ctaDevolCompra.codsubcuenta)
            if not curPartidasCompra.commitBuffer():
                return False

        return True

    def oficial_esSubcuentaEspecial(self, codSubcuenta=None, codEjercicio=None, idTipoEsp=None):
        qsa.debug(qsa.ustr("oficial_esSubcuentaEspecial para ", codSubcuenta, " ", codEjercicio, " ", idTipoEsp))
        util = qsa.FLUtil()
        if not codEjercicio:
            codEjercicio = qsa.from_project("flfactppal").iface.pub_ejercicioActual()
        qrySubcuenta = qsa.FLSqlQuery()
        qrySubcuenta.setTablesList("co_subcuentas,co_cuentas")
        qrySubcuenta.setSelect("s.idcuentaesp, c.codcuenta, c.idcuentaesp")
        qrySubcuenta.setFrom("co_subcuentas s INNER JOIN co_cuentas c ON s.idcuenta = c.idcuenta")
        qrySubcuenta.setWhere(
            qsa.ustr("s.codsubcuenta = '", codSubcuenta, "' AND s.codejercicio = '", codEjercicio, "'")
        )
        qrySubcuenta.setForwardOnly(True)
        qsa.debug(qrySubcuenta.sql())
        if not qrySubcuenta.exec_():
            qsa.debug(1)
            return False
        if not qrySubcuenta.first():
            qsa.debug(2)
            return False
        if qrySubcuenta.value("s.idcuenaesp") == idTipoEsp or qrySubcuenta.value("c.idcuentaesp") == idTipoEsp:
            qsa.debug(4)
            return True
        codCuenta = qrySubcuenta.value("c.codcuenta")
        qryTipoEsp = qsa.FLSqlQuery()
        qryTipoEsp.setTablesList("co_cuentasesp")
        qryTipoEsp.setSelect("codcuenta, codsubcuenta")
        qryTipoEsp.setFrom("co_cuentasesp")
        qryTipoEsp.setWhere(qsa.ustr("idcuentaesp = '", __undef__idCuentaEsp, "'"))
        qryTipoEsp.setForwardOnly(True)
        if not qryTipoEsp.exec_():
            qsa.debug(5)
            return False
        if not qryTipoEsp.first():
            qsa.debug(6)
            return False
        if qryTipoEsp.value("codsubcuenta") == codSubcuenta or qryTipoEsp.value("codcuenta") == codCuenta:
            qsa.debug(8)
            return True
        qsa.debug(9)
        return False

    def oficial_datosDocFacturacion(self, fecha=None, codEjercicio=None, tipoDoc=None):
        res = qsa.Array()
        res["ok"] = True
        res["modificaciones"] = False
        util = qsa.FLUtil()
        if util.sqlSelect(
            "ejercicios",
            "codejercicio",
            qsa.ustr("codejercicio = '", codEjercicio, "' AND '", fecha, "' BETWEEN fechainicio AND fechafin"),
        ):
            return res
        f = qsa.FLFormSearchDB("fechaejercicio")
        cursor = f.cursor()
        cursor.select()
        if not cursor.first():
            cursor.setModeAccess(cursor.Insert)
        else:
            cursor.setModeAccess(cursor.Edit)

        cursor.refreshBuffer()
        cursor.refreshBuffer()
        cursor.setValueBuffer("fecha", fecha)
        cursor.setValueBuffer("codejercicio", codEjercicio)
        cursor.setValueBuffer("label", tipoDoc)
        cursor.commitBuffer()
        cursor.select()
        if not cursor.first():
            res["ok"] = False
            return res
        cursor.setModeAccess(cursor.Edit)
        cursor.refreshBuffer()
        f.setMainWidget()
        acpt = f.exec_("codejercicio")
        if not acpt:
            res["ok"] = False
            return res
        res["modificaciones"] = True
        res["fecha"] = cursor.valueBuffer("fecha")
        res["codEjercicio"] = cursor.valueBuffer("codejercicio")
        if res.codEjercicio != qsa.from_project("flfactppal").iface.pub_ejercicioActual():
            if tipoDoc != "pagosdevolcli" and tipoDoc != "pagosdevolprov":
                qsa.MessageBox.information(
                    util.translate(
                        "scripts",
                        "Ha seleccionado un ejercicio distinto del actual.\nPara visualizar los documentos generados debe cambiar el ejercicio actual en la ventana\nde empresa y volver a abrir el formulario maestro correspondiente a los documentos generados",
                    ),
                    qsa.MessageBox.Ok,
                    qsa.MessageBox.NoButton,
                )
        return res

    def oficial_tieneIvaDocCliente(self, codSerie=None, codCliente=None, codEjercicio=None):
        util = qsa.FLUtil()
        conIva = True
        if util.sqlSelect("series", "siniva", qsa.ustr("codserie = '", codSerie, "'")):
            return 0
        else:
            regIva = util.sqlSelect("clientes", "regimeniva", qsa.ustr("codcliente = '", codCliente, "'"))
            if regIva == "Exento":
                return 0
            else:
                if not util.sqlSelect("clientes", "recargo", qsa.ustr("codcliente = '", codCliente, "'")):
                    return 1

        return 2

    def oficial_tieneIvaDocProveedor(self, codSerie=None, codProveedor=None, codEjercicio=None):
        util = qsa.FLUtil()
        tieneIva = 0
        if util.sqlSelect("series", "siniva", qsa.ustr("codserie = '", codSerie, "'")):
            tieneIva = 0
        else:
            regIva = util.sqlSelect("proveedores", "regimeniva", qsa.ustr("codproveedor = '", codProveedor, "'"))
            if regIva == "Exento":
                tieneIva = 0
            else:
                if qsa.from_project("flfactppal").iface.pub_valorDefectoEmpresa("recequivalencia"):
                    tieneIva = 2
                else:
                    tieneIva = 1

        return tieneIva

    def oficial_automataActivado(self):
        if not qsa.sys.isLoadedModule("flautomata"):
            return False
        if qsa.from_project("formau_automata").iface.pub_activado():
            return True
        return False

    def oficial_comprobarRegularizacion(self, curFactura=None):
        util = qsa.FLUtil()
        fecha = curFactura.valueBuffer("fecha")
        if util.sqlSelect(
            "co_regiva",
            "idregiva",
            qsa.ustr(
                "fechainicio <= '",
                fecha,
                "' AND fechafin >= '",
                fecha,
                "' AND codejercicio = '",
                curFactura.valueBuffer("codejercicio"),
                "'",
            ),
        ):
            qsa.MessageBox.warning(
                util.translate(
                    "scripts", "No puede incluirse el asiento de la factura en un período de I.V.A. ya regularizado"
                ),
                qsa.MessageBox.Ok,
                qsa.MessageBox.NoButton,
            )
            return False
        return True

    def oficial_recalcularHuecos(self, serie=None, ejercicio=None, fN=None):
        util = qsa.FLUtil()
        tipo = ""
        tabla = ""
        if fN == "nfacturaprov":
            tipo = "FP"
            tabla = "facturasprov"
        else:
            if fN == "nfacturacli":
                tipo = "FC"
                tabla = "facturascli"

        idSec = util.sqlSelect(
            "secuenciasejercicios", "id", qsa.ustr("codserie = '", serie, "' AND codejercicio = '", ejercicio, "'")
        )
        if idSec:
            nHuecos = qsa.parseInt(
                util.sqlSelect(
                    "huecos",
                    "count(*)",
                    qsa.ustr("codserie = '", serie, "' AND codejercicio = '", ejercicio, "' AND tipo = '", tipo, "'"),
                )
            )
            nFacturas = qsa.parseInt(
                util.sqlSelect(
                    tabla, "count(*)", qsa.ustr("codserie = '", serie, "' AND codejercicio = '", ejercicio, "'")
                )
            )
            maxFactura = (
                qsa.parseInt(
                    util.sqlSelect("secuencias", "valorout", qsa.ustr("id = ", idSec, " AND nombre='", fN, "'"))
                )
                - 1
            )
            if qsa.isNaN(maxFactura):
                maxFactura = 0
            if maxFactura - nFacturas != nHuecos:
                nSec = util.sqlSelect("secuencias", "valorinicial", qsa.ustr("id = ", idSec, " AND nombre='", fN, "'"))
                if not nSec:
                    nSec = 0
                nFac = 0
                ultFac = -1
                cursorHuecos = qsa.FLSqlCursor("huecos")
                qryFac = qsa.FLSqlQuery()
                util.createProgressDialog(
                    util.translate("scripts", "Calculando huecos en la numeración..."), maxFactura
                )
                qryFac.setTablesList(tabla)
                qryFac.setSelect("numero")
                qryFac.setFrom(tabla)
                qryFac.setWhere(qsa.ustr("codserie = '", serie, "' AND codejercicio = '", ejercicio, "'"))
                qryFac.setOrderBy("codigo asc")
                qryFac.setForwardOnly(True)
                if not qryFac.exec_():
                    return True
                util.sqlDelete(
                    "huecos",
                    qsa.ustr(
                        "codserie = '",
                        serie,
                        "' AND codejercicio = '",
                        ejercicio,
                        "' AND (tipo = 'XX' OR tipo = '",
                        tipo,
                        "')",
                    ),
                )
                while qryFac.next():
                    nFac = qryFac.value(0)
                    if ultFac == nFac:
                        continue
                    ultFac = nFac
                    nSec += 1
                    util.setProgress(nSec)
                    while nSec < nFac:
                        cursorHuecos.setModeAccess(cursorHuecos.Insert)
                        cursorHuecos.refreshBuffer()
                        cursorHuecos.setValueBuffer("tipo", tipo)
                        cursorHuecos.setValueBuffer("codserie", serie)
                        cursorHuecos.setValueBuffer("codejercicio", ejercicio)
                        cursorHuecos.setValueBuffer("numero", nSec)
                        cursorHuecos.commitBuffer()
                        nSec += 1
                        util.setProgress(nSec)

                nSec += 1
                util.setProgress(nSec)
                util.sqlUpdate("secuencias", "valorout", nSec, qsa.ustr("id = ", idSec, " AND nombre='", fN, "'"))
                util.setProgress(maxFactura)
                util.destroyProgressDialog()

        return True

    def oficial_mostrarTraza(self, codigo=None, tipo=None):
        util = qsa.FLUtil()
        util.sqlDelete("trazadoc", qsa.ustr("usuario = '", qsa.sys.nameUser(), "'"))
        f = qsa.FLFormSearchDB("trazadoc")
        curTraza = f.cursor()
        curTraza.setModeAccess(curTraza.Insert)
        curTraza.refreshBuffer()
        curTraza.setValueBuffer("usuario", qsa.sys.nameUser())
        curTraza.setValueBuffer("codigo", codigo)
        curTraza.setValueBuffer("tipo", tipo)
        if not curTraza.commitBuffer():
            return False
        curTraza.select(qsa.ustr("usuario = '", qsa.sys.nameUser(), "'"))
        if not curTraza.first():
            return False
        curTraza.setModeAccess(curTraza.Browse)
        f.setMainWidget()
        curTraza.refreshBuffer()
        acpt = f.exec_("usuario")

    def oficial_datosPartidaFactura(self, curPartida=None, curFactura=None, tipo=None, concepto=None):
        util = qsa.FLUtil()
        if tipo == "cliente":
            if concepto:
                curPartida.setValueBuffer("concepto", concepto)
            else:
                curPartida.setValueBuffer(
                    "concepto",
                    qsa.ustr(
                        util.translate("scripts", "Nuestra factura"),
                        " ",
                        curFactura.valueBuffer("codigo"),
                        " - ",
                        curFactura.valueBuffer("nombrecliente"),
                    ),
                )

            if curPartida.valueBuffer("cifnif"):
                curPartida.setValueBuffer("tipodocumento", "Factura de cliente")

        else:
            if concepto:
                curPartida.setValueBuffer("concepto", concepto)
            else:
                numFactura = curFactura.valueBuffer("numproveedor")
                if numFactura == "":
                    numFactura = curFactura.valueBuffer("codigo")
                curPartida.setValueBuffer(
                    "concepto",
                    qsa.ustr(
                        util.translate("scripts", "Su factura"),
                        " ",
                        numFactura,
                        " - ",
                        curFactura.valueBuffer("nombre"),
                    ),
                )

            if curPartida.valueBuffer("cifnif"):
                curPartida.setValueBuffer("tipodocumento", "Factura de proveedor")

        if curPartida.valueBuffer("cifnif"):
            curPartida.setValueBuffer("documento", curFactura.valueBuffer("codigo"))
            curPartida.setValueBuffer("factura", curFactura.valueBuffer("numero"))

    def oficial_siGenerarRecibosCli(self, curFactura=None, masCampos=None):
        camposAcomprobar = qsa.Array("codcliente", "total", "codpago", "fecha")
        i = 0
        while_pass = True
        while i < qsa.length(camposAcomprobar):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            if curFactura.valueBuffer(camposAcomprobar[i]) != curFactura.valueBufferCopy(camposAcomprobar[i]):
                return True
            i += 1
            while_pass = True
            try:
                i < qsa.length(camposAcomprobar)
            except Exception:
                break

        if masCampos:
            i = 0
            while_pass = True
            while i < qsa.length(masCampos):
                if not while_pass:
                    i += 1
                    while_pass = True
                    continue
                while_pass = False
                if curFactura.valueBuffer(masCampos[i]) != curFactura.valueBufferCopy(masCampos[i]):
                    return True
                i += 1
                while_pass = True
                try:
                    i < qsa.length(masCampos)
                except Exception:
                    break

        return False

    def oficial_validarIvaRecargoCliente(self, codCliente=None, id=None, tabla=None, identificador=None):
        util = qsa.FLUtil()
        if not codCliente:
            return True
        regimenIva = util.sqlSelect("clientes", "regimeniva", qsa.ustr("codcliente = '", codCliente, "'"))
        aplicarRecargo = util.sqlSelect("clientes", "recargo", qsa.ustr("codcliente = '", codCliente, "'"))
        q = qsa.FLSqlQuery()
        q.setTablesList(tabla)
        q.setSelect("iva,recargo")
        q.setFrom(tabla)
        q.setWhere(qsa.ustr(identificador, " = ", id))
        if not q.exec_():
            return False
        preguntadoIva = False
        preguntadoRecargo = False
        while q.next() and (not preguntadoIva or not preguntadoRecargo):
            iva = qsa.parseFloat(q.value("iva"))
            if not iva:
                iva = 0
            recargo = qsa.parseFloat(q.value("recargo"))
            if not recargo:
                recargo = 0
            if not preguntadoIva:
                for case in qsa.switch(regimenIva):
                    if case("General"):
                        if iva == 0:
                            res = qsa.MessageBox.warning(
                                util.translate(
                                    "scripts",
                                    "El cliente %s tiene establecido un régimen de I.V.A. %s\ny en alguna o varias de las lineas no hay establecido un % de I.V.A.\n¿Desea continuar de todas formas?",
                                )
                                % (str(codCliente), str(regimenIva)),
                                qsa.MessageBox.Yes,
                                qsa.MessageBox.No,
                            )
                            preguntadoIva = True
                            if res != qsa.MessageBox.Yes:
                                return False

                        break

                    if case("Exento"):
                        if iva != 0:
                            res = qsa.MessageBox.warning(
                                util.translate(
                                    "scripts",
                                    "El cliente %s tiene establecido un régimen de I.V.A. %s\ny en alguna o varias de las lineas hay establecido un % de I.V.A.\n¿Desea continuar de todas formas?",
                                )
                                % (str(codCliente), str(regimenIva)),
                                qsa.MessageBox.Yes,
                                qsa.MessageBox.No,
                            )
                            preguntadoIva = True
                            if res != qsa.MessageBox.Yes:
                                return False

                        break

            if not preguntadoRecargo:
                if aplicarRecargo and recargo == 0:
                    res = qsa.MessageBox.warning(
                        util.translate(
                            "scripts",
                            "Al cliente %s se le debe aplicar Recargo de Equivalencia\ny en alguna o varias de las lineas no hay establecido un % de R. Equivalencia.\n¿Desea continuar de todas formas?",
                        )
                        % (str(codCliente)),
                        qsa.MessageBox.Yes,
                        qsa.MessageBox.No,
                    )
                    preguntadoRecargo = True
                    if res != qsa.MessageBox.Yes:
                        return False

                if not aplicarRecargo and recargo != 0:
                    res = qsa.MessageBox.warning(
                        util.translate(
                            "scripts",
                            "Al cliente %s no se le debe aplicar Recargo de Equivalencia\ny en alguna o varias de las lineas hay establecido un % de R. Equivalencia.\n¿Desea continuar de todas formas?",
                        )
                        % (str(codCliente)),
                        qsa.MessageBox.Yes,
                        qsa.MessageBox.No,
                    )
                    preguntadoRecargo = True
                    if res != qsa.MessageBox.Yes:
                        return False

        return True

    def oficial_validarIvaRecargoProveedor(self, codProveedor=None, id=None, tabla=None, identificador=None):
        util = qsa.FLUtil()
        if not codProveedor:
            return True
        regimenIva = util.sqlSelect("proveedores", "regimeniva", qsa.ustr("codproveedor = '", codProveedor, "'"))
        aplicarRecargo = util.sqlSelect("empresa", "recequivalencia", "1 = 1")
        q = qsa.FLSqlQuery()
        q.setTablesList(tabla)
        q.setSelect("iva,recargo")
        q.setFrom(tabla)
        q.setWhere(qsa.ustr(identificador, " = ", id))
        if not q.exec_():
            return False
        preguntadoIva = False
        preguntadoRecargo = False
        while q.next() and (not preguntadoIva or not preguntadoRecargo):
            iva = qsa.parseFloat(q.value("iva"))
            if not iva:
                iva = 0
            recargo = qsa.parseFloat(q.value("recargo"))
            if not recargo:
                recargo = 0
            if not preguntadoIva:
                for case in qsa.switch(regimenIva):
                    if case("General"):
                        pass
                    if case("U.E."):
                        if iva == 0:
                            res = qsa.MessageBox.warning(
                                util.translate(
                                    "scripts",
                                    "El proveedor %s tiene establecido un régimen de I.V.A. %s\ny en alguna o varias de las lineas no hay establecido un % de I.V.A.\n¿Desea continuar de todas formas?",
                                )
                                % (str(codProveedor), str(regimenIva)),
                                qsa.MessageBox.Yes,
                                qsa.MessageBox.No,
                            )
                            preguntadoIva = True
                            if res != qsa.MessageBox.Yes:
                                return False

                        break

                    if case("Exento"):
                        if iva != 0:
                            res = qsa.MessageBox.warning(
                                util.translate(
                                    "scripts",
                                    "El proveedor %s tiene establecido un régimen de I.V.A. %s\ny en alguna o varias de las lineas hay establecido un % de I.V.A.\n¿Desea continuar de todas formas?",
                                )
                                % (str(codProveedor), str(regimenIva)),
                                qsa.MessageBox.Yes,
                                qsa.MessageBox.No,
                            )
                            preguntadoIva = True
                            if res != qsa.MessageBox.Yes:
                                return False

                        break

            if not preguntadoRecargo:
                if aplicarRecargo and recargo == 0:
                    res = qsa.MessageBox.warning(
                        util.translate(
                            "scripts",
                            "En los datos de empresa está activa al opción Aplicar Recargo de Equivalencia\ny en alguna o varias de las lineas no hay establecido un % de R. Equivalencia.\n¿Desea continuar de todas formas?",
                        ),
                        qsa.MessageBox.Yes,
                        qsa.MessageBox.No,
                    )
                    preguntadoRecargo = True
                    if res != qsa.MessageBox.Yes:
                        return False

                if not aplicarRecargo and recargo != 0:
                    res = qsa.MessageBox.warning(
                        util.translate(
                            "scripts",
                            "En los datos de empresa no está activa al opción Aplicar Recargo de Equivalencia\ny en alguna o varias de las lineas hay establecido un % de R. Equivalencia.\n¿Desea continuar de todas formas?",
                        ),
                        qsa.MessageBox.Yes,
                        qsa.MessageBox.No,
                    )
                    preguntadoRecargo = True
                    if res != qsa.MessageBox.Yes:
                        return False

        return True

    def oficial_comprobarFacturaAbonoCli(self, curFactura=None):
        util = qsa.FLUtil()
        if curFactura.valueBuffer("deabono"):
            if not curFactura.valueBuffer("idfacturarect"):
                res = qsa.MessageBox.warning(
                    util.translate("scripts", "No ha indicado la factura que desea abonar.\n¿Desea continuar?"),
                    qsa.MessageBox.No,
                    qsa.MessageBox.Yes,
                )
                if res != qsa.MessageBox.Yes:
                    return False
            else:
                if util.sqlSelect(
                    "facturascli",
                    "idfacturarect",
                    qsa.ustr(
                        "idfacturarect = ",
                        curFactura.valueBuffer("idfacturarect"),
                        " AND idfactura <> ",
                        curFactura.valueBuffer("idfactura"),
                    ),
                ):
                    qsa.MessageBox.warning(
                        util.translate("scripts", "La factura ")
                        + util.sqlSelect(
                            "facturascli", "codigo", qsa.ustr("idfactura = ", curFactura.valueBuffer("idfacturarect"))
                        )
                        + util.translate("scripts", " ya está abonada"),
                        qsa.MessageBox.Ok,
                        qsa.MessageBox.NoButton,
                        qsa.MessageBox.NoButton,
                    )
                    return False

        return True

    def oficial_crearCtaEspecial(self, codCtaEspecial=None, tipo=None, codEjercicio=None, desCta=None):
        util = qsa.FLUtil()
        codSubcuenta = ""
        if tipo == "subcuenta":
            f = qsa.FLFormSearchDB("co_subcuentas")
            curSubcuenta = f.cursor()
            curSubcuenta.setMainFilter(qsa.ustr("codejercicio = '", codEjercicio, "'"))
            f.setMainWidget()
            codSubcuenta = f.exec_("codsubcuenta")
            if not codSubcuenta:
                return False

        curCtaEspecial = qsa.FLSqlCursor("co_cuentasesp")
        curCtaEspecial.select(qsa.ustr("idcuentaesp = '", codCtaEspecial, "'"))
        if curCtaEspecial.first():
            curCtaEspecial.setModeAccess(curCtaEspecial.Edit)
            curCtaEspecial.refreshBuffer()
        else:
            curCtaEspecial.setModeAccess(curCtaEspecial.Insert)
            curCtaEspecial.refreshBuffer()
            curCtaEspecial.setValueBuffer("idcuentaesp", codCtaEspecial)
            curCtaEspecial.setValueBuffer("descripcion", desCta)

        if codSubcuenta and codSubcuenta != "":
            curCtaEspecial.setValueBuffer("codsubcuenta", codSubcuenta)
        if not curCtaEspecial.commitBuffer():
            return False
        return True

    def oficial_comprobarCambioSerie(self, cursor=None):
        util = qsa.FLUtil()
        if (
            not cursor.valueBuffer("codserie")
            or cursor.valueBuffer("codserie") == ""
            or not cursor.valueBufferCopy("codserie")
            or cursor.valueBufferCopy("codserie") == ""
        ):
            return True
        if cursor.valueBuffer("codserie") != cursor.valueBufferCopy("codserie"):
            util = qsa.FLUtil()
            qsa.MessageBox.warning(
                util.translate("scripts", "No se puede modificar la serie.\nSerie anterior:%s - Serie actual:%s")
                % (str(cursor.valueBufferCopy("codserie")), str(cursor.valueBuffer("codserie"))),
                qsa.MessageBox.Ok,
                qsa.MessageBox.NoButton,
                qsa.MessageBox.NoButton,
            )
            return False
        return True

    def oficial_subcuentaVentas(self, referencia=None, codEjercicio=None):
        return False

    def oficial_restarCantidadCli(self, idLineaPedido=None, idLineaAlbaran=None):
        util = qsa.FLUtil()
        cantidad = qsa.parseFloat(
            util.sqlSelect(
                "lineasalbaranescli",
                "SUM(cantidad)",
                qsa.ustr("idlineapedido = ", idLineaPedido, " AND idlinea <> ", idLineaAlbaran),
            )
        )
        if qsa.isNaN(cantidad):
            cantidad = 0
        curLineaPedido = qsa.FLSqlCursor("lineaspedidoscli")
        curLineaPedido.select(qsa.ustr("idlinea = ", idLineaPedido))
        if curLineaPedido.first():
            curLineaPedido.setModeAccess(curLineaPedido.Edit)
            curLineaPedido.refreshBuffer()
            curLineaPedido.setValueBuffer("totalenalbaran", cantidad)
            if not curLineaPedido.commitBuffer():
                return False

        return True

    def oficial_restarCantidadProv(self, idLineaPedido=None, idLineaAlbaran=None):
        util = qsa.FLUtil()
        cantidad = qsa.parseFloat(
            util.sqlSelect(
                "lineasalbaranesprov",
                "SUM(cantidad)",
                qsa.ustr("idlineapedido = ", idLineaPedido, " AND idlinea <> ", idLineaAlbaran),
            )
        )
        if qsa.isNaN(cantidad):
            cantidad = 0
        curLineaPedido = qsa.FLSqlCursor("lineaspedidosprov")
        curLineaPedido.select(qsa.ustr("idlinea = ", idLineaPedido))
        if curLineaPedido.first():
            curLineaPedido.setModeAccess(curLineaPedido.Edit)
            curLineaPedido.refreshBuffer()
            curLineaPedido.setValueBuffer("totalenalbaran", cantidad)
            if not curLineaPedido.commitBuffer():
                return False

        return True

    def oficial_actualizarPedidosCli(self, curAlbaran=None):
        return True

    def oficial_actualizarPedidosProv(self, curAlbaran=None):
        return True

    def oficial_actualizarLineaPedidoProv(
        self, idLineaPedido=None, idPedido=None, referencia=None, idAlbaran=None, cantidadLineaAlbaran=None
    ):
        if idLineaPedido == 0:
            return True
        cantidadServida = 0
        curLineaPedido = qsa.FLSqlCursor("lineaspedidosprov")
        curLineaPedido.select(qsa.ustr("idlinea = ", idLineaPedido))
        curLineaPedido.setModeAccess(curLineaPedido.Edit)
        if not curLineaPedido.first():
            return True
        cantidadPedido = qsa.parseFloat(curLineaPedido.valueBuffer("cantidad"))
        query = qsa.FLSqlQuery()
        query.setTablesList("lineasalbaranesprov")
        query.setSelect("SUM(cantidad)")
        query.setFrom("lineasalbaranesprov")
        query.setWhere(qsa.ustr("idlineapedido = ", idLineaPedido, " AND idalbaran <> ", idAlbaran))
        if not query.exec_():
            return False
        if query.next():
            canOtros = qsa.parseFloat(query.value("SUM(cantidad)"))
            if qsa.isNaN(canOtros):
                canOtros = 0
            cantidadServida = canOtros + qsa.parseFloat(cantidadLineaAlbaran)

        if cantidadServida > cantidadPedido:
            cantidadServida = cantidadPedido
        curLineaPedido.setValueBuffer("totalenalbaran", cantidadServida)
        if not curLineaPedido.commitBuffer():
            return False
        return True

    def oficial_actualizarEstadoPedidoProv(self, idPedido=None, curAlbaran=None):
        estado = self.iface.obtenerEstadoPedidoProv(idPedido)
        if not estado:
            return False
        curPedido = qsa.FLSqlCursor("pedidosprov")
        curPedido.select(qsa.ustr("idpedido = ", idPedido))
        if curPedido.first():
            if estado == curPedido.valueBuffer("servido"):
                return True
            curPedido.setUnLock("editable", True)
        curPedido.select(qsa.ustr("idpedido = ", idPedido))
        curPedido.setModeAccess(curPedido.Edit)
        if curPedido.first():
            curPedido.setValueBuffer("servido", estado)
            if estado == "Sí":
                curPedido.setValueBuffer("editable", False)
                if qsa.sys.isLoadedModule("flcolaproc"):
                    if not qsa.from_project("flfactppal").iface.pub_lanzarEvento(curPedido, "pedidoProvAlbaranado"):
                        return False

            if not curPedido.commitBuffer():
                return False

        return True

    def oficial_obtenerEstadoPedidoProv(self, idPedido=None):
        query = qsa.FLSqlQuery()
        query.setTablesList("lineaspedidosprov")
        query.setSelect("cantidad, totalenalbaran, cerrada")
        query.setFrom("lineaspedidosprov")
        query.setWhere(qsa.ustr("idpedido = ", idPedido))
        if not query.exec_():
            return False
        estado = ""
        totalServidas = 0
        parcial = False
        totalLineas = query.size()
        totalCerradas = 0
        if totalLineas == 0:
            return "No"
        cantidad = 0
        cantidadServida = 0
        cerrada = qsa.Boolean()
        while query.next():
            cantidad = qsa.parseFloat(query.value("cantidad"))
            cantidadServida = qsa.parseFloat(query.value("totalenalbaran"))
            cerrada = query.value("cerrada")
            if cerrada:
                totalCerradas += 1
            else:
                if cantidad == cantidadServida:
                    totalServidas += 1
                else:
                    if cantidad > cantidadServida and cantidadServida != 0:
                        parcial = True

        totalAServir = totalLineas - totalCerradas
        if parcial:
            estado = "Parcial"
        else:
            if totalServidas == 0 and totalCerradas == 0:
                estado = "No"
            else:
                if totalServidas >= totalAServir:
                    estado = "Sí"
                else:
                    estado = "Parcial"

        return estado

    def oficial_actualizarLineaPedidoCli(
        self, idLineaPedido=None, idPedido=None, referencia=None, idAlbaran=None, cantidadLineaAlbaran=None
    ):
        if idLineaPedido == 0:
            return True
        cantidadServida = 0
        curLineaPedido = qsa.FLSqlCursor("lineaspedidoscli")
        curLineaPedido.select(qsa.ustr("idlinea = ", idLineaPedido))
        curLineaPedido.setModeAccess(curLineaPedido.Edit)
        if not curLineaPedido.first():
            return True
        cantidadPedido = qsa.parseFloat(curLineaPedido.valueBuffer("cantidad"))
        query = qsa.FLSqlQuery()
        query.setTablesList("lineasalbaranescli")
        query.setSelect("SUM(cantidad)")
        query.setFrom("lineasalbaranescli")
        query.setWhere(qsa.ustr("idlineapedido = ", idLineaPedido, " AND idalbaran <> ", idAlbaran))
        if not query.exec_():
            return False
        if query.next():
            canOtros = qsa.parseFloat(query.value("SUM(cantidad)"))
            if qsa.isNaN(canOtros):
                canOtros = 0
            cantidadServida = canOtros + qsa.parseFloat(cantidadLineaAlbaran)

        if cantidadServida > cantidadPedido:
            cantidadServida = cantidadPedido
        curLineaPedido.setValueBuffer("totalenalbaran", cantidadServida)
        if not curLineaPedido.commitBuffer():
            return False
        return True

    def oficial_actualizarEstadoPedidoCli(self, idPedido=None, curAlbaran=None):
        estado = self.iface.obtenerEstadoPedidoCli(idPedido)
        if not estado:
            return False
        curPedido = qsa.FLSqlCursor("pedidoscli")
        curPedido.select(qsa.ustr("idpedido = ", idPedido))
        if curPedido.first():
            if estado == curPedido.valueBuffer("servido"):
                return True
            curPedido.setUnLock("editable", True)
        curPedido.select(qsa.ustr("idpedido = ", idPedido))
        curPedido.setModeAccess(curPedido.Edit)
        if curPedido.first():
            curPedido.setValueBuffer("servido", estado)
            if estado == "Sí":
                curPedido.setValueBuffer("editable", False)
            if not curPedido.commitBuffer():
                return False

        return True

    def oficial_obtenerEstadoPedidoCli(self, idPedido=None):
        query = qsa.FLSqlQuery()
        query.setTablesList("lineaspedidoscli")
        query.setSelect("cantidad, totalenalbaran, cerrada")
        query.setFrom("lineaspedidoscli")
        query.setWhere(qsa.ustr("idpedido = ", idPedido))
        if not query.exec_():
            return False
        estado = ""
        totalServidas = 0
        parcial = False
        totalLineas = query.size()
        totalCerradas = 0
        if totalLineas == 0:
            return "No"
        cantidad = 0
        cantidadServida = 0
        cerrada = qsa.Boolean()
        while query.next():
            cantidad = qsa.parseFloat(query.value("cantidad"))
            cantidadServida = qsa.parseFloat(query.value("totalenalbaran"))
            cerrada = query.value("cerrada")
            if cerrada:
                totalCerradas += 1
            else:
                if cantidad == cantidadServida:
                    totalServidas += 1
                else:
                    if cantidad > cantidadServida and cantidadServida != 0:
                        parcial = True

        totalAServir = totalLineas - totalCerradas
        if parcial:
            estado = "Parcial"
        else:
            if totalServidas == 0 and totalCerradas == 0:
                estado = "No"
            else:
                if totalServidas >= totalAServir:
                    estado = "Sí"
                else:
                    estado = "Parcial"

        return estado

    def oficial_liberarAlbaranesCli(self, idFactura=None):
        curAlbaranes = qsa.FLSqlCursor("albaranescli")
        curAlbaranes.select(qsa.ustr("idfactura = ", idFactura))
        while curAlbaranes.next():
            if not self.iface.liberarAlbaranCli(curAlbaranes.valueBuffer("idalbaran")):
                return False
        return True

    def oficial_liberarAlbaranCli(self, idAlbaran=None):
        curAlbaran = qsa.FLSqlCursor("albaranescli")
        # WITH_START
        curAlbaran.select(qsa.ustr("idalbaran = ", idAlbaran))
        curAlbaran.first()
        curAlbaran.setUnLock("ptefactura", True)
        curAlbaran.setModeAccess(curAlbaran.Edit)
        curAlbaran.refreshBuffer()
        curAlbaran.setValueBuffer("idfactura", "0")
        # WITH_END
        if not curAlbaran.commitBuffer():
            return False
        return True

    def oficial_liberarAlbaranesProv(self, idFactura=None):
        curAlbaranes = qsa.FLSqlCursor("albaranesprov")
        curAlbaranes.select(qsa.ustr("idfactura = ", idFactura))
        while curAlbaranes.next():
            if not self.iface.liberarAlbaranProv(curAlbaranes.valueBuffer("idalbaran")):
                return False
        return True

    def oficial_liberarAlbaranProv(self, idAlbaran=None):
        curAlbaran = qsa.FLSqlCursor("albaranesprov")
        # WITH_START
        curAlbaran.select(qsa.ustr("idalbaran = ", idAlbaran))
        curAlbaran.first()
        curAlbaran.setUnLock("ptefactura", True)
        curAlbaran.setModeAccess(curAlbaran.Edit)
        curAlbaran.refreshBuffer()
        curAlbaran.setValueBuffer("idfactura", "0")
        # WITH_END
        if not curAlbaran.commitBuffer():
            return False
        return True

    def oficial_liberarPresupuestoCli(self, idPresupuesto=None):
        if idPresupuesto:
            curPresupuesto = qsa.FLSqlCursor("presupuestoscli")
            curPresupuesto.select(qsa.ustr("idpresupuesto = ", idPresupuesto))
            if not curPresupuesto.first():
                return False
            # WITH_START
            curPresupuesto.setUnLock("editable", True)
            # WITH_END

        return True

    def oficial_aplicarComisionLineas(self, codAgente=None, tblHija=None, where=None):
        util = qsa.FLUtil()
        numLineas = util.sqlSelect(tblHija, "count(idlinea)", where)
        if not numLineas:
            return True
        referencia = ""
        comision = 0
        if not codAgente or codAgente == "":
            return False
        curLineas = qsa.FLSqlCursor(tblHija)
        curLineas.select(where)
        util.createProgressDialog(util.translate("scripts", "Actualizando comisión ..."), numLineas)
        i = 0
        while curLineas.next():
            util.setProgress(i)
            i += 1
            curLineas.setActivatedCommitActions(False)
            curLineas.setModeAccess(curLineas.Edit)
            curLineas.refreshBuffer()
            referencia = curLineas.valueBuffer("referencia")
            comision = self.iface.calcularComisionLinea(codAgente, referencia)
            comision = util.roundFieldValue(comision, tblHija, "porcomision")
            curLineas.setValueBuffer("porcomision", comision)
            if not curLineas.commitBuffer():
                util.destroyProgressDialog()
                return False

        util.setProgress(numLineas)
        util.destroyProgressDialog()
        return True

    def oficial_calcularComisionLinea(self, codAgente=None, referencia=None):
        util = qsa.FLUtil()
        valor = -1
        if referencia and referencia != "":
            id = util.sqlSelect(
                "articulosagen", "id", qsa.ustr("referencia = '", referencia, "' AND codagente = '", codAgente, "'")
            )
            if id:
                valor = qsa.parseFloat(util.sqlSelect("articulosagen", "comision", qsa.ustr("id = ", id)))
        if valor == -1:
            valor = qsa.parseFloat(util.sqlSelect("agentes", "porcomision", qsa.ustr("codagente = '", codAgente, "'")))
        valor = util.roundFieldValue(valor, "agentes", "porcomision")
        return valor

    def oficial_arrayCostesAfectados(self, arrayInicial=None, arrayFinal=None):
        arrayAfectados = qsa.Array()
        iAA = 0
        iAI = 0
        iAF = 0
        longAI = qsa.length(arrayInicial)
        longAF = qsa.length(arrayFinal)
        arrayInicial.sort(self.iface.compararArrayCoste)
        arrayFinal.sort(self.iface.compararArrayCoste)
        comparacion = 0
        while iAI < longAI or iAF < longAF:
            if iAI < longAI and iAF < longAF:
                comparacion = self.iface.compararArrayCoste(arrayInicial[iAI], arrayFinal[iAF])
            else:
                if iAF < longAF:
                    comparacion = 1
                else:
                    if iAI < longAI:
                        comparacion = -1

            for case in qsa.switch(comparacion):
                if case(1):
                    arrayAfectados[iAA] = qsa.Array()
                    arrayAfectados[iAA]["idarticulo"] = arrayFinal[iAF]["idarticulo"]
                    iAF += 1
                    iAA += 1
                    break

                if case(-1):
                    arrayAfectados[iAA] = qsa.Array()
                    arrayAfectados[iAA]["idarticulo"] = arrayInicial[iAI]["idarticulo"]
                    iAI += 1
                    iAA += 1
                    break

                if case(0):
                    if (arrayInicial[iAI]["cantidad"] != arrayFinal[iAF]["cantidad"]) or (
                        arrayInicial[iAI]["pvptotal"] != arrayFinal[iAF]["pvptotal"]
                    ):
                        arrayAfectados[iAA] = qsa.Array()
                        arrayAfectados[iAA]["idarticulo"] = arrayFinal[iAI]["idarticulo"]
                        iAA += 1
                    iAI += 1
                    iAF += 1
                    break

        return arrayAfectados

    def oficial_compararArrayCoste(self, a=None, b=None):
        resultado = 0
        if a["idarticulo"] > b["idarticulo"]:
            resultado = 1
        else:
            if a["idarticulo"] < b["idarticulo"]:
                resultado = -1

        return resultado

    def oficial_campoImpuesto(self, campo=None, codImpuesto=None, fecha=None):
        util = qsa.FLUtil()
        return qsa.parseFloat(util.sqlSelect("impuestos", campo, qsa.ustr("codimpuesto = '", codImpuesto, "'")))

    def oficial_datosImpuesto(self, codImpuesto=None, fecha=None):
        datosImpuesto = qsa.Array()
        qryImpuesto = qsa.FLSqlQuery()
        qryImpuesto.setTablesList("impuestos")
        qryImpuesto.setSelect("iva, recargo")
        qryImpuesto.setFrom("impuestos")
        qryImpuesto.setWhere(qsa.ustr("codimpuesto = '", codImpuesto, "'"))
        try:
            qryImpuesto.setForwardOnly(True)
        except Exception:
            e = qsa.format_exc()

        if not qryImpuesto.exec_():
            return False
        if not qryImpuesto.first():
            return False
        datosImpuesto.iva = qryImpuesto.value("iva")
        datosImpuesto.recargo = qryImpuesto.value("recargo")
        return datosImpuesto

    def oficial_valorDefecto(self, fN=None):
        util = qsa.FLUtil()
        valor = util.sqlSelect("facturac_general", fN, "1 = 1")
        if not valor:
            return ""
        return valor

    def oficial_formateaCadena(self, cIn=None):
        cOut = ""
        equivA = "ÑñÇçÁáÉéÍíÓóÚúÀàÈèÌìÒòÙùÂâÊêÎîÔôÛûÄäËëÏïÖöÜüº"
        equivB = "NnCcAaEeIiOoUuAaEeIiOoUuAaEeIiOoUuAaEeIiOoUu "
        validos = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ /-?+:,.'()"
        iEq = None
        i = 0
        while_pass = True
        while i < qsa.length(cIn):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            iEq = equivA.find(cIn[i])
            if iEq >= 0:
                cOut += equivB[iEq]
            else:
                if validos.find(cIn[i]) >= 0:
                    cOut += cIn[i]

            i += 1
            while_pass = True
            try:
                i < qsa.length(cIn)
            except Exception:
                break

        return cOut


if TYPE_CHECKING:
    form: FormInternalObj = FormInternalObj()
    iface = form.iface
else:
    form = None
