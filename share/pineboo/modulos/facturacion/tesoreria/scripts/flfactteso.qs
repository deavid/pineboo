/***************************************************************************
                 flfactteso.qs  -  description
                             -------------------
    begin                : lun abr 26 2004
    copyright            : (C) 2004 by InfoSiAL S.L.
    email                : mail@infosial.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

/** @file */

/** @class_declaration interna */
////////////////////////////////////////////////////////////////////////////
//// DECLARACION ///////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////
//// INTERNA /////////////////////////////////////////////////////
class interna {
    var ctx:Object;
    function interna( context ) { this.ctx = context; }
        function init() { this.ctx.interna_init(); }
    function afterCommit_pagosdevolcli(curPD:FLSqlCursor):Boolean {
                return this.ctx.interna_afterCommit_pagosdevolcli(curPD);
        }
        function beforeCommit_pagosdevolcli(curPD:FLSqlCursor):Boolean {
                return this.ctx.interna_beforeCommit_pagosdevolcli(curPD);
        }
        function afterCommit_reciboscli(curR:FLSqlCursor):Boolean {
                return this.ctx.interna_afterCommit_reciboscli(curR);
        }
        function afterCommit_pagosdevolprov(curPD:FLSqlCursor):Boolean {
                return this.ctx.interna_afterCommit_pagosdevolprov(curPD);
        }
        function beforeCommit_pagosdevolprov(curPD:FLSqlCursor):Boolean {
                return this.ctx.interna_beforeCommit_pagosdevolprov(curPD);
        }
        function beforeCommit_remesas(curRemesa:FLSqlCursor):Boolean {
                return this.ctx.interna_beforeCommit_remesas(curRemesa);
        }
        function beforeCommit_pagosdevolrem(curPR:FLSqlCursor):Boolean {
                return this.ctx.interna_beforeCommit_pagosdevolrem(curPR);
        }
        function afterCommit_pagosdevolrem(curPD:FLSqlCursor):Boolean {
                return this.ctx.interna_afterCommit_pagosdevolrem(curPD);
        }
}
//// INTERNA /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
class oficial extends interna {
        var curReciboCli:FLSqlCursor;

    function oficial( context ) { interna( context ); }
        function actualizarRiesgoCliente(codCliente:String) {
                return this.ctx.oficial_actualizarRiesgoCliente(codCliente);
        }
        function tienePagosDevCli(idRecibo:Number):Boolean {
                return this.ctx.oficial_tienePagosDevCli(idRecibo);
        }
        function regenerarRecibosCli(cursor:FLSqlCursor, emitirComo:String):Boolean {
                return this.ctx.oficial_regenerarRecibosCli(cursor, emitirComo);
        }
        function generarReciboCli(curFactura:FLSqlCursor, numRecibo:String, importe:Number, fechaVto:String, emitirComo:String, datosCuentaDom:Array, datosCuentaEmp:Array, datosSubcuentaEmp:Array):Boolean {
                return this.ctx.oficial_generarReciboCli(curFactura, numRecibo, importe, fechaVto, emitirComo, datosCuentaDom, datosCuentaEmp, datosSubcuentaEmp);
        }
        function obtenerDatosCuentaDom(codCliente:String):Array {
                return this.ctx.oficial_obtenerDatosCuentaDom(codCliente);
        }
        function obtenerDatosCuentaEmp(codCliente:String, codPago:String):Array {
                return this.ctx.oficial_obtenerDatosCuentaEmp(codCliente, codPago);
        }
        function obtenerDatosSubcuentaEmp(datosCuentaEmp:Array):Array {
                return this.ctx.oficial_obtenerDatosSubcuentaEmp(datosCuentaEmp);
        }
        function borrarRecibosCli(idFactura:Number):Boolean {
                return this.ctx.oficial_borrarRecibosCli(idFactura);
        }
        function calcFechaVencimientoCli(curFactura:FLSqlCursor, numPlazo:Number, diasAplazado:Number):String {
                return this.ctx.oficial_calcFechaVencimientoCli(curFactura, numPlazo, diasAplazado);
        }
        function regenerarRecibosProv(cursor:FLSqlCursor, emitirComo:String):Boolean {
                return this.ctx.oficial_regenerarRecibosProv(cursor, emitirComo);
        }
        function datosReciboCli(curFactura:FLSqlCursor):Boolean {
                return this.ctx.oficial_datosReciboCli(curFactura);
        }
        function calcularEstadoFacturaCli(idRecibo:String, idFactura:String):Boolean {
                return this.ctx.oficial_calcularEstadoFacturaCli(idRecibo, idFactura);
        }
        function cambiaUltimoPagoCli(idRecibo:String, idPagoDevol:String, unlock:Boolean):Boolean {
                return this.ctx.oficial_cambiaUltimoPagoCli(idRecibo, idPagoDevol, unlock);
        }
        function generarAsientoPagoDevolCli(curPD:FLSqlCursor) {
                return this.ctx.oficial_generarAsientoPagoDevolCli(curPD);
        }
        function generarPartidasCli(curPD:FLSqlCursor, valoresDefecto:Array, datosAsiento:Array, recibo:Array):Boolean {
                return this.ctx.oficial_generarPartidasCli(curPD, valoresDefecto, datosAsiento, recibo);
        }
        function generarPartidasBanco(curPD:FLSqlCursor, valoresDefecto:Array, datosAsiento:Array, recibo:Array):Boolean {
                return this.ctx.oficial_generarPartidasBanco(curPD, valoresDefecto, datosAsiento, recibo);
        }
        function generarPartidasCambio(curPD:FLSqlCursor, valoresDefecto:Array, datosAsiento:Array, recibo:Array):Boolean {
                return this.ctx.oficial_generarPartidasCambio(curPD, valoresDefecto, datosAsiento, recibo);
        }
        function comprobarCuentasDom(idRemesa:String):Boolean {
                return this.ctx.oficial_comprobarCuentasDom(idRemesa);
        }
        function automataActivado():Boolean {
                return this.ctx.oficial_automataActivado();
        }
        function generarAsientoPagoRemesa(curPR:FLSqlCursor):Boolean {
                return this.ctx.oficial_generarAsientoPagoRemesa(curPR);
        }
        function generarPartidasEFCOGC(curPR:FLSqlCursor, valoresDefecto:Array, datosAsiento:Array, remesa:Array):Boolean {
                return this.ctx.oficial_generarPartidasEFCOGC(curPR, valoresDefecto, datosAsiento, remesa);
        }
        function generarPartidasBancoRem(curPR:FLSqlCursor, valoresDefecto:Array, datosAsiento:Array, remesa:Array):Boolean {
                return this.ctx.oficial_generarPartidasBancoRem(curPR, valoresDefecto, datosAsiento, remesa);
        }
        function esPagoEstePagoDevol(curPD:FLSqlCursor):Boolean {
                return this.ctx.oficial_esPagoEstePagoDevol(curPD);
        }
        function generarAsientoInverso(idAsientoDestino:Number, idAsientoOrigen:Number, concepto:String, codEjercicio:String):Boolean {
                return this.ctx.oficial_generarAsientoInverso(idAsientoDestino, idAsientoOrigen, concepto, codEjercicio);
        }
}
//// OFICIAL /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration proveed */
//////////////////////////////////////////////////////////////////
//// PROVEED /////////////////////////////////////////////////////
class proveed extends oficial /** %from: oficial */ {
    var curReciboProv:FLSqlCursor;

	function proveed( context ) { oficial( context ); }
	function tienePagosDevProv(idRecibo:Number):Boolean {
		return this.ctx.proveed_tienePagosDevProv(idRecibo);
	}
	function regenerarRecibosProv(cursor:FLSqlCursor, forzarEmitirComo:String):Boolean {
		return this.ctx.proveed_regenerarRecibosProv(cursor, forzarEmitirComo);
	}
	function afterCommit_pagosdevolprov(curPD:FLSqlCursor):Boolean {
		return this.ctx.proveed_afterCommit_pagosdevolprov(curPD);
	}
	function beforeCommit_pagosdevolprov(curPD:FLSqlCursor):Boolean {
		return this.ctx.proveed_beforeCommit_pagosdevolprov(curPD);
	}
	function calcFechaVencimientoProv(curFactura:FLSqlCursor, numPlazo:Number, diasAplazado:Number):String {
		return this.ctx.proveed_calcFechaVencimientoProv(curFactura, numPlazo, diasAplazado);
	}
	function datosReciboProv():Boolean {
		return this.ctx.proveed_datosReciboProv();
	}
	function cambiaUltimoPagoProv(idRecibo:String, idPagoDevol:String, unlock:Boolean):Boolean {
		return this.ctx.proveed_cambiaUltimoPagoProv(idRecibo, idPagoDevol, unlock);
	}
	function calcularEstadoFacturaProv(idRecibo:String, idFactura:String):Boolean {
		return this.ctx.proveed_calcularEstadoFacturaProv(idRecibo, idFactura);
	}
	function borrarRecibosProv(idFactura:Number):Boolean {
		return this.ctx.proveed_borrarRecibosProv(idFactura);
	}
	function generarPartidasProv(curPD:FLSqlCursor, valoresDefecto:Array, datosAsiento:Array, recibo:Array):Boolean {
		return this.ctx.proveed_generarPartidasProv(curPD, valoresDefecto, datosAsiento, recibo);
	}
	function generarPartidasBancoProv(curPD:FLSqlCursor, valoresDefecto:Array, datosAsiento:Array, recibo:Array):Boolean {
		return this.ctx.proveed_generarPartidasBancoProv(curPD, valoresDefecto, datosAsiento, recibo);
	}
	function generarPartidasCambioProv(curPD:FLSqlCursor, valoresDefecto:Array, datosAsiento:Array, recibo:Array):Boolean {
		return this.ctx.proveed_generarPartidasCambioProv(curPD, valoresDefecto, datosAsiento, recibo);
	}
	function generarAsientoPagoDevolProv(curPD:FLSqlCursor):Boolean {
		return this.ctx.proveed_generarAsientoPagoDevolProv(curPD);
	}
	function codCuentaPagoProv(curFactura:FLSqlCursor):String {
		return this.ctx.proveed_codCuentaPagoProv(curFactura);
	}
	function siGenerarRecibosProv(curFactura:FLSqlCursor, masCampos:Array):Boolean {
		return this.ctx.proveed_siGenerarRecibosProv(curFactura, masCampos);
	}
	function obtenerDatosCuentaDomProv(codProveedor:String):Array {
		return this.ctx.proveed_obtenerDatosCuentaDomProv(codProveedor);
	}
}
//// PROVEED /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration diasPagoProv */
/////////////////////////////////////////////////////////////////
//// DIAS_PAGO_PROV /////////////////////////////////////////////
class diasPagoProv extends proveed /** %from: oficial */ {
    function diasPagoProv( context ) { proveed ( context ); }
	function calcFechaVencimientoProv(curFactura:FLSqlCursor, numPlazo:Number, diasAplazado:Number):String {
		return this.ctx.diasPagoProv_calcFechaVencimientoProv(curFactura, numPlazo, diasAplazado);
	}
	function procesarDiasPagoProv(fechaV:String, diasPago:Array):String {
		return this.ctx.diasPagoProv_procesarDiasPagoProv(fechaV, diasPago);
	}
	function procesarDiasPagoProvAnt(fechaV:String, diasPago:Array):String {
		return this.ctx.diasPagoProv_procesarDiasPagoProvAnt(fechaV, diasPago);
	}
}
//// DIAS_PAGO_PROV //////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration remesaProv */
/////////////////////////////////////////////////////////////////
//// REMESAS DE RECIBOS DE PROVEEDOR ////////////////////////////
class remesaProv extends diasPagoProv /** %from: proveed */ {
    function remesaProv( context ) { diasPagoProv ( context ); }
	function beforeCommit_remesasprov(curRemesa:FLSqlCursor):Boolean {
		return this.ctx.remesaProv_beforeCommit_remesasprov(curRemesa);
	}
	function generarPartidasEFCOGP(curPR:FLSqlCursor, valoresDefecto:Array, datosAsiento:Array, remesa:Array):Boolean {
		return this.ctx.remesaProv_generarPartidasEFCOGP(curPR, valoresDefecto, datosAsiento, remesa);
	}
	function generarAsientoPagoRemesaProv(curPR:FLSqlCursor):Boolean {
		return this.ctx.remesaProv_generarAsientoPagoRemesaProv(curPR);
	}
	function generarPartidasBancoRemProv(curPR:FLSqlCursor, valoresDefecto:Array, datosAsiento:Array, remesa:Array):Boolean {
		return this.ctx.remesaProv_generarPartidasBancoRemProv(curPR, valoresDefecto, datosAsiento, remesa);
	}
	function beforeCommit_pagosdevolremprov(curPR:FLSqlCursor):Boolean {
		return this.ctx.remesaProv_beforeCommit_pagosdevolremprov(curPR);
	}
	function afterCommit_pagosdevolremprov(curPD:FLSqlCursor):Boolean {
		return this.ctx.remesaProv_afterCommit_pagosdevolremprov(curPD);
	}
}
//// REMESAS DE RECIBOS DE PROVEEDOR ////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration modelo340 */
       /////////////////////////////////////////////////////////////////
       //// MODELO 340 /////////////////////////////////////////////////
       class modelo340 extends remesaProv /** %from: proveed */
{
  function modelo340(context)
  {
    remesaProv(context);
  }
  function beforeCommit_pagosdevolprov(curPD)
  {
    return this.ctx.modelo340_beforeCommit_pagosdevolprov(curPD);
  }
  function afterCommit_pagosdevolprov(curPD)
  {
    return this.ctx.modelo340_afterCommit_pagosdevolprov(curPD);
  }
  function marcarPrimerPago(idRecibo)
  {
    return this.ctx.modelo340_marcarPrimerPago(idRecibo);
  }
}

//// MODELO 340 /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////
class head extends modelo340 {
    function head( context ) { modelo340 ( context ); }
}
//// DESARROLLO /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration ifaceCtx */
/////////////////////////////////////////////////////////////////
//// INTERFACE  /////////////////////////////////////////////////
class ifaceCtx extends head {
    function ifaceCtx( context ) { head( context ); }
        function pub_actualizarRiesgoCliente(codCliente:String) {
                return this.actualizarRiesgoCliente(codCliente);
        }
        function pub_regenerarRecibosCli(cursor:FLSqlCursor, emitirComo:String):Boolean {
                return this.regenerarRecibosCli(cursor, emitirComo);
        }
        function pub_regenerarRecibosProv(cursor:FLSqlCursor, emitirComo:String):Boolean {
                return this.regenerarRecibosProv(cursor, emitirComo);
        }
        function pub_calcularEstadoFacturaCli(idRecibo:String, idFactura:String):Boolean {
                return this.calcularEstadoFacturaCli(idRecibo, idFactura);
        }
        function pub_comprobarCuentasDom(idRemesa:String):Boolean {
                return this.comprobarCuentasDom(idRemesa);
        }
        function pub_automataActivado():Boolean {
                return this.automataActivado();
        }
}


//// INTERFACE  /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

const iface = new pubProveed( this );

/** @class_declaration pubProveed */
/////////////////////////////////////////////////////////////////
//// PUB PROVEEDORES ////////////////////////////////////////////
class pubProveed extends ifaceCtx /** %from: ifaceCtx */ {
	function pubProveed( context ) { ifaceCtx( context ); }
	function pub_calcularEstadoFacturaProv(idRecibo:String, idFactura:String):Boolean {
		return this.calcularEstadoFacturaProv(idRecibo, idFactura);
	}
}
//// PUB PROVEEDORES ////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition interna */
////////////////////////////////////////////////////////////////////////////
//// DEFINICION ////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////
//// INTERNA /////////////////////////////////////////////////////
/** \D Se actualiza el campo idremesa de los pagos con el valor del campo idremesa del recibo
\end */
function interna_init()
{
        var util:FLUtil;
        if (!util.sqlSelect("remesas", "idremesa", "1 = 1"))
                return;
        if (util.sqlSelect("pagosdevolcli", "idremesa", "idremesa IS NOT NULL AND idremesa <> 0"))
                return;
        var qryRecibos:FLSqlQuery = new FLSqlQuery;
        qryRecibos.setTablesList("reciboscli,pagosdevolcli");
        qryRecibos.setSelect("pd.idpagodevol, r.idremesa, MAX(pd.fecha)")
        qryRecibos.setFrom("reciboscli r INNER JOIN pagosdevolcli pd ON r.idrecibo = pd.idrecibo")
        qryRecibos.setWhere("r.idremesa IS NOT NULL AND r.idremesa <> 0 AND pd.tipo = 'Pago' AND (pd.idremesa IS NULL OR pd.idremesa = 0) GROUP BY pd.idpagodevol, r.idremesa");
        qryRecibos.setForwardOnly(true);
        if (!qryRecibos.exec())
                return;
        var editable:Boolean;
        var paso:Number = 0;
        var curPD:FLSqlCursor = new FLSqlCursor("pagosdevolcli");
        curPD.setActivatedCommitActions(false);
        curPD.transaction(false);
        try {
                util.createProgressDialog(util.translate("scripts", "Actualizando pagos de recibos remesados"), qryRecibos.size());
                while (qryRecibos.next()) {
                        util.setProgress(paso)
                        curPD.select("idpagodevol = " + qryRecibos.value("pd.idpagodevol"))
                        if (!curPD.first()) {
                                curPD.rollback();
                                util.destroyProgressDialog();
                                break;
                        }
                        editable = curPD.valueBuffer("editable");
                        if (!editable) {
                                curPD.setUnLock("editable", true);
                                curPD.select("idpagodevol = " + qryRecibos.value("pd.idpagodevol"));
                                curPD.first();
                        }
                        curPD.setModeAccess(curPD.Edit);
                        curPD.refreshBuffer();
                        curPD.setValueBuffer("idremesa", qryRecibos.value("r.idremesa"));
                        if (!curPD.commitBuffer()) {
                                curPD.rollback();
                                util.destroyProgressDialog();
                                break;
                        }
                        if (!editable) {
                                curPD.select("idpagodevol = " + qryRecibos.value("pd.idpagodevol"));
                                curPD.first();
                                curPD.setUnLock("editable", false);
                        }
                        paso++;
                }
        } catch (e) {
                util.destroyProgressDialog();
                curPD.rollback();
        }
        curPD.setActivatedCommitActions(true);
        util.destroyProgressDialog();
        if (paso == qryRecibos.size()) {
                debug("Commit");
                curPD.commit();
        } else
                curPD.rollback();
}

/** \C Se elimina, si es posible, el asiento contable asociado al pago o devolución
\end */
function interna_afterCommit_pagosdevolcli(curPD:FLSqlCursor):Boolean
{
        var idRecibo:String = curPD.valueBuffer("idrecibo");
        /** \C Se cambia el pago anterior al actual para que sólo el último sea editable
        \end */
        switch (curPD.modeAccess()) {
                case curPD.Insert:
                case curPD.Edit: {
                        if (!this.iface.cambiaUltimoPagoCli(idRecibo, curPD.valueBuffer("idpagodevol"), false))
                                return false;
                        break;
                }
                case curPD.Del: {
                        if (!this.iface.cambiaUltimoPagoCli(idRecibo, curPD.valueBuffer("idpagodevol"), true))
                                return false;
                        break;
                }
        }

        if (!this.iface.calcularEstadoFacturaCli(idRecibo))
                return false;


        var util:FLUtil = new FLUtil();
        if (sys.isLoadedModule("flcontppal") == false || util.sqlSelect("empresa", "contintegrada", "1 = 1") == false)
                return true;

        switch (curPD.modeAccess()) {
                case curPD.Del: {
                        if (curPD.isNull("idasiento"))
                                return true;

                        var idAsiento:Number = curPD.valueBuffer("idasiento");
                        if (flfacturac.iface.pub_asientoBorrable(idAsiento) == false)
                                return false;

                        var curAsiento:FLSqlCursor = new FLSqlCursor("co_asientos");
                        curAsiento.select("idasiento = " + idAsiento);
                        if (curAsiento.first()) {
                                curAsiento.setUnLock("editable", true);
                                curAsiento.setModeAccess(curAsiento.Del);
                                curAsiento.refreshBuffer();
                                if (!curAsiento.commitBuffer())
                                        return false;
                        }
                        break;
                }
                case curPD.Edit: {
                        if (curPD.valueBuffer("nogenerarasiento")) {
                                var idAsientoAnterior:String = curPD.valueBufferCopy("idasiento");
                                if (idAsientoAnterior && idAsientoAnterior != "") {
                                        if (!flfacturac.iface.pub_eliminarAsiento(idAsientoAnterior))
                                                return false;
                                }
                        }
                        break;
                }
        }

        return true;
}

/** \C Se regenera, si es posible, el asiento contable asociado al pago o devolución
\end */
function interna_beforeCommit_pagosdevolcli(curPD:FLSqlCursor):Boolean
{
        var util:FLUtil = new FLUtil();
        if (sys.isLoadedModule("flcontppal") && flfactppal.iface.pub_valorDefectoEmpresa("contintegrada") && !curPD.valueBuffer("nogenerarasiento")) {
                if (!this.iface.generarAsientoPagoDevolCli(curPD)) {
                        return false;
                }
        }

        return true;
}

/** \C Se recalcula el riesgo alcanzado
\end */
function interna_afterCommit_reciboscli(curR:FLSqlCursor):Boolean
{
        if (curR.valueBuffer("codcliente"))
                this.iface.actualizarRiesgoCliente(curR.valueBuffer("codcliente"));

        return true;
}


/** \C Funcionalidad no implementada para la versión oficial
\end */
function interna_afterCommit_pagosdevolprov(curPD:FLSqlCursor):Boolean
{
        return true;
}

/** \C Funcionalidad no implementada para la versión oficial
\end */
function interna_beforeCommit_pagosdevolprov(curPD:FLSqlCursor):Boolean
{
        return true;
}

function interna_beforeCommit_remesas(curRemesa:FLSqlCursor):Boolean
{

        switch (curRemesa.modeAccess()) {
                /** \C La remesa puede borrarse si todos los pagos asociados pueden ser excluidos
                \end */
                case curRemesa.Del: {
                        var idRemesa:Number = curRemesa.valueBuffer("idremesa");
                        var qryRecibos:FLSqlQuery = new FLSqlQuery;
                        qryRecibos.setTablesList("pagosdevolcli");
                        qryRecibos.setSelect("DISTINCT(idrecibo)");
                        qryRecibos.setFrom("pagosdevolcli");
                        qryRecibos.setWhere("idremesa = " + idRemesa);
                        qryRecibos.setForwardOnly(true);
                        if (!qryRecibos.exec())
                                return false;
                        while (qryRecibos.next()) {
                                if (!formRecordremesas.iface.pub_excluirReciboRemesa(qryRecibos.value(0), idRemesa))
                                        return false;
                        }
                }
        }
        return true;
}

/** \C Se regenera, si es posible, el asiento contable asociado al pago de una remesa
\end */
function interna_beforeCommit_pagosdevolrem(curPR:FLSqlCursor):Boolean
{
        var util:FLUtil = new FLUtil();
        if (sys.isLoadedModule("flcontppal") && flfactppal.iface.pub_valorDefectoEmpresa("contintegrada") && !curPR.valueBuffer("nogenerarasiento")) {
                if (!this.iface.generarAsientoPagoRemesa(curPR))
                        return false;
        }

        return true;
}

/** \C Se elimina, si es posible, el asiento contable asociado al pago o devolución
\end */
function interna_afterCommit_pagosdevolrem(curPD:FLSqlCursor):Boolean
{
        var util:FLUtil = new FLUtil();
        if (sys.isLoadedModule("flcontppal") == false || util.sqlSelect("empresa", "contintegrada", "1 = 1") == false)
                return true;

        switch (curPD.modeAccess()) {
                case curPD.Del: {
                        if (curPD.isNull("idasiento"))
                                return true;

                        var idAsiento:Number = curPD.valueBuffer("idasiento");
                        if (flfacturac.iface.pub_asientoBorrable(idAsiento) == false)
                                return false;

                        var curAsiento:FLSqlCursor = new FLSqlCursor("co_asientos");
                        curAsiento.select("idasiento = " + idAsiento);
                        if (curAsiento.first()) {
                                curAsiento.setUnLock("editable", true);
                                curAsiento.setModeAccess(curAsiento.Del);
                                curAsiento.refreshBuffer();
                                if (!curAsiento.commitBuffer())
                                        return false;
                        }
                        break;
                }
                case curPD.Edit: {
                        if (curPD.valueBuffer("nogenerarasiento")) {
                                var idAsientoAnterior:String = curPD.valueBufferCopy("idasiento");
                                if (idAsientoAnterior && idAsientoAnterior != "") {
                                        if (!flfacturac.iface.pub_eliminarAsiento(idAsientoAnterior))
                                                return false;
                                }
                        }
                        break;
                }
        }

        return true;
}
//// INTERNA /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
/** \D Actualiza el valor del riesgo alcanzado para un cliente. El valor se calcula como la suma de importes de: recibos emitidos - recibos pagados + recibos devueltos
@param codCliente: Código del cliente
\end */
function oficial_actualizarRiesgoCliente(codCliente:String)
{
        var util:FLUtil = new FLUtil();
        var riesgo:Number = parseFloat( util.sqlSelect( "reciboscli", "SUM(importe)", "estado <> 'Pagado' AND codcliente='" + codCliente + "'" ) );
        if (!riesgo || isNaN(riesgo))
                riesgo = 0;

        util.sqlUpdate( "clientes", "riesgoalcanzado", riesgo, "codcliente = '" + codCliente + "'" );

        if ( !flfactteso.iface.pub_automataActivado() ) {
                var riesgoMax:Number = parseFloat( util.sqlSelect( "clientes", "riesgomax", "codcliente = '" + codCliente + "'" ) );
                if ( riesgo >= riesgoMax && riesgoMax > 0 ) {
                        MessageBox.warning(util.translate("scripts", "El cliente ") + codCliente + util.translate("scripts", " ha superado el riesgo máximo"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
                }
        }
}

/** \D Genera las partidas inversas correspondientes a un asiento, asociándolas a otro.
@param idAsientoDestino Asiento de destino para la partida
@param idAsientoOrigen Asiento de origen para la partida
@param concepto Concepto de la partida inversa
\end */
/// Llamada por recibos_prov
function oficial_generarAsientoInverso(idAsientoDestino:Number, idAsientoOrigen:Number, concepto:String, codEjercicio:String):Boolean
{
        var util:FLUtil = new FLUtil;
        var curPartida:FLSqlCursor = new FLSqlCursor("co_partidas");
        curPartida.select("idasiento = " + idAsientoDestino);
        qryPartidaOriginal = new FLSqlQuery();
        with(qryPartidaOriginal) {
                setTablesList("co_partidas");
                setSelect("codsubcuenta, debe, haber, coddivisa, tasaconv, debeME, haberME");
                setFrom("co_partidas");
                setWhere("idasiento = " + idAsientoOrigen);
        }
        try { qryPartidaOriginal.setForwardOnly( true ); } catch (e) {}
        if (!qryPartidaOriginal.exec())
                return false;

        while (qryPartidaOriginal.next()) {
                var idSubcuenta:Number = util.sqlSelect("co_subcuentas", "idsubcuenta", "codsubcuenta = '" + qryPartidaOriginal.value(0) + "' AND codejercicio = '" + codEjercicio + "'");
                if (!idSubcuenta) {
                        MessageBox.warning(util.translate("scripts", "No existe la subcuenta ")  + qryPartidaOriginal.value(0) + util.translate("scripts", " correspondiente al ejercicio ") + codEjercicio + util.translate("scripts", ".\nPara poder realizar el asiento debe crear antes esta subcuenta"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
                        return false;
                }
                with(curPartida) {
                        setModeAccess(curPartida.Insert);
                        refreshBuffer();
                        setValueBuffer("concepto", concepto);
                        setValueBuffer("idsubcuenta", idSubcuenta);
                        setValueBuffer("codsubcuenta", qryPartidaOriginal.value(0));
                        setValueBuffer("idasiento", idAsientoDestino);
                        setValueBuffer("debe", qryPartidaOriginal.value(2));
                        setValueBuffer("haber", qryPartidaOriginal.value(1));
                        setValueBuffer("coddivisa", qryPartidaOriginal.value(3));
                        setValueBuffer("tasaconv", qryPartidaOriginal.value(4));
                        setValueBuffer("debeME", qryPartidaOriginal.value(6));
                        setValueBuffer("haberME", qryPartidaOriginal.value(5));
                }
                if (!curPartida.commitBuffer())
                        return false;
        }
        return true;
}

/* \D Indica si un determinado recibo tiene pagos y/o devoluciones asociadas.
@param idRecibo: Identificador del recibo
@return True: Tiene, False: No tiene
\end */
function oficial_tienePagosDevCli(idRecibo:Number):Boolean
{
        var curPagosDev:FLSqlCursor = new FLSqlCursor("pagosdevolcli");
        curPagosDev.select("idrecibo = " + idRecibo);
        return curPagosDev.next();
}

/* \D Calcula la fecha de vencimiento de un recibo, como la fecha de facturación más los días del plazo correspondiente
@param curFactura: Cursor posicionado en el registro de facturas correspondiente a la factura
@param numPlazo: Número del plazo actual
@param diasAplazado: Días de aplazamiento del pago
@return Fecha de vencimiento
\end */
function oficial_calcFechaVencimientoCli(curFactura:FLSqlCursor, numPlazo:Number, diasAplazado:Number):String
{
        var util:FLUtil = new FLUtil;
        return util.addDays(curFactura.valueBuffer("fecha"), diasAplazado);
}

/* \D Regenera los recibos asociados a una factura a cliente.
Si la contabilidad está activada, genera los correspondientes asientos de pago y devolución.

@param cursor: Cursor posicionado en el registro de facturascli correspondiente a la factura
@return True: Regeneración realizada con éxito, False: Error
\end */
function oficial_regenerarRecibosCli(cursor:FLSqlCursor, emitirComo:String):Boolean
{
        var util:FLUtil = new FLUtil();
        var contActiva:Boolean = sys.isLoadedModule("flcontppal") && util.sqlSelect("empresa", "contintegrada", "1 = 1");

        var idFactura:Number = cursor.valueBuffer("idfactura");
        var total:Number = parseFloat(cursor.valueBuffer("total"));

        if (!this.iface.borrarRecibosCli(idFactura))
                return false;

        if (total == 0)
                return true;

        var codPago:String = cursor.valueBuffer("codpago");
        var codCliente:String = cursor.valueBuffer("codcliente");

        var emitirComo:String = util.sqlSelect("formaspago", "genrecibos", "codpago = '" + codPago + "'");
        var datosCuentaDom = this.iface.obtenerDatosCuentaDom(codCliente);
        if (datosCuentaDom.error == 2)
                return false;
        var numRecibo:Number = 1;
        var numPlazo:Number = 1;
        var importe:Number;
        var diasAplazado:Number;
        var fechaVencimiento:String;
        var datosCuentaEmp:Array = false;
        var datosSubcuentaEmp:Array = false;

        if (emitirComo == "Pagados") {
                emitirComo = "Pagado";
                /* \D Si los recibos deben emitirse como pagados, se generarán los registros de pago asociados a cada recibo. Si el módulo Principal de contabilidad está cargado, se generará el correspondienta asiento. La subcuenta contable del Debe del apunte corresponderá a la subcuenta contable asociada a la cuenta corriente correspondiente a la forma de pago de la factura. Si dicha cuenta corriente no está especificada, la subcuenta contable del Debe del asiento será la correspondiente a la cuenta especial Caja.
                \end */
                datosCuentaEmp = this.iface.obtenerDatosCuentaEmp(codCliente, codPago);
                if (datosCuentaEmp.error == 2)
                        return false;
                if (contActiva) {
                        datosSubcuentaEmp = this.iface.obtenerDatosSubcuentaEmp(datosCuentaEmp);
                        if (datosSubcuentaEmp.error == 2)
                                return false;
                }
        } else
                emitirComo = "Emitido";

        var importeAcumulado:Number = 0;
        var curPlazos:FLSqlCursor = new FLSqlCursor("plazos");
        curPlazos.select("codpago = '" + codPago + "'  ORDER BY dias");
        if(curPlazos.size() == 0) {
                MessageBox.warning(util.translate("scripts", "No se pueden generar los recibos, la forma de pago ") + codPago + util.translate("scripts", "no tiene plazos de pago asociados"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
                return false;
        }
        while (curPlazos.next()) {
                diasAplazado = curPlazos.valueBuffer("dias");

                if ( curPlazos.at() == ( curPlazos.size() - 1 ) )
                        importe = parseFloat(total) - parseFloat(importeAcumulado);
                else
                        importe = (parseFloat(total) * parseFloat(curPlazos.valueBuffer("aplazado"))) / 100;

                importe = util.roundFieldValue(importe, "reciboscli","importe");
                importeAcumulado = parseFloat(importeAcumulado) + parseFloat(importe);

                fechaVencimiento = this.iface.calcFechaVencimientoCli(cursor, numPlazo, diasAplazado);
                if (!this.iface.generarReciboCli(cursor, numRecibo, importe, fechaVencimiento, emitirComo, datosCuentaDom, datosCuentaEmp, datosSubcuentaEmp))
                        return false;
                numRecibo++;
                numPlazo++;
        }

        if (emitirComo == "Pagado") {
                if (!this.iface.calcularEstadoFacturaCli(false, idFactura))
                        return false;
        }

        if (cursor.valueBuffer("codcliente"))
                if (sys.isLoadedModule("flfactteso"))
                        this.iface.actualizarRiesgoCliente(codCliente);

        return true;
}

/* \D Genera un recibo con los datos proporcionados. Si el recibo se emite como pagado y la contabilidad está integrada, se generará el asiento de pago correspondiente

@param curFactura: Cursor posicionado en la factura de la que proviene el recibo
@param numRecibo: Ordinal del recibo dentro del grupo de recibos asociados a la factura
@param importe: Importe del recibo
@param fechaVto: Fecha de vencimiento
@param emitirComo: Indica si el recibo se emitirá como 'Pagado' o como 'Emitido'.
@param datosCuentaDom: Datos de la cuenta de domiciación, si existe
@param datosCuentaEmp: Datos de la cuenta de la empresa para realizar el pago
@param datosSubcuentaEmp: Datos contables de la subcuenta asociada a la cuenta bancaria de la empresa
@return True si no hay error, false en caso contrario
\end */
function oficial_generarReciboCli(curFactura:FLSqlCursor, numRecibo:String, importe:Number, fechaVto:String, emitirComo:String, datosCuentaDom:Array, datosCuentaEmp:Array, datosSubcuentaEmp:Array):Boolean
{
        if (!this.iface.curReciboCli)
                this.iface.curReciboCli = new FLSqlCursor("reciboscli");

        var util:FLUtil = new FLUtil();
        var importeEuros:Number  = importe * parseFloat(curFactura.valueBuffer("tasaconv"));
        var divisa:String = util.sqlSelect("divisas", "descripcion", "coddivisa = '" + curFactura.valueBuffer("coddivisa") + "'");
        var codDir:Number = curFactura.valueBuffer("coddir");
        with (this.iface.curReciboCli) {
                setModeAccess(Insert);
                refreshBuffer();
                setValueBuffer("numero", numRecibo);
                setValueBuffer("idfactura", curFactura.valueBuffer("idfactura"));
                setValueBuffer("importe", importe);
                setValueBuffer("texto", util.enLetraMoneda(importe, divisa));
                setValueBuffer("importeeuros", importeEuros);
                setValueBuffer("coddivisa", curFactura.valueBuffer("coddivisa"));
                setValueBuffer("codigo", curFactura.valueBuffer("codigo") + "-" + flfacturac.iface.pub_cerosIzquierda(numRecibo, 2));
                setValueBuffer("codcliente", curFactura.valueBuffer("codcliente"));
                setValueBuffer("nombrecliente", curFactura.valueBuffer("nombrecliente"));
                setValueBuffer("cifnif", curFactura.valueBuffer("cifnif"));
                if (codDir == 0)
                        setNull("coddir");
                else
                        setValueBuffer("coddir", codDir);
                setValueBuffer("direccion", curFactura.valueBuffer("direccion"));
                setValueBuffer("codpostal", curFactura.valueBuffer("codpostal"));
                setValueBuffer("ciudad", curFactura.valueBuffer("ciudad"));
                setValueBuffer("provincia", curFactura.valueBuffer("provincia"));
                setValueBuffer("codpais", curFactura.valueBuffer("codpais"));
                setValueBuffer("fecha", curFactura.valueBuffer("fecha"));

                if (datosCuentaDom.error == 0) {
                        setValueBuffer("codcuenta", datosCuentaDom.codcuenta);
                        setValueBuffer("descripcion", datosCuentaDom.descripcion);
                        setValueBuffer("ctaentidad", datosCuentaDom.ctaentidad);
                        setValueBuffer("ctaagencia", datosCuentaDom.ctaagencia);
                        setValueBuffer("cuenta", datosCuentaDom.cuenta);
                        setValueBuffer("dc", datosCuentaDom.dc);
                }
                setValueBuffer("fechav", fechaVto);
                setValueBuffer("estado", emitirComo);
        }
        if (!this.iface.datosReciboCli(curFactura))
                return false;

        if (!this.iface.curReciboCli.commitBuffer())
                return false;

        if (emitirComo == "Pagado") {
                var idRecibo = this.iface.curReciboCli.valueBuffer("idrecibo");
                var curPago = new FLSqlCursor("pagosdevolcli");
                with(curPago) {
                        setModeAccess(Insert);
                        refreshBuffer();
                        setValueBuffer("idrecibo", idRecibo);
                        setValueBuffer("tipo", "Pago");
                        setValueBuffer("fecha", curFactura.valueBuffer("fecha"));
                        setValueBuffer("tasaconv", curFactura.valueBuffer("tasaconv"));
                        if (datosCuentaEmp.error == 0) {
                                setValueBuffer("codcuenta", datosCuentaEmp.codcuenta);
                                setValueBuffer("descripcion", datosCuentaEmp.descripcion);
                                setValueBuffer("ctaentidad", datosCuentaEmp.ctaentidad);
                                setValueBuffer("ctaagencia", datosCuentaEmp.ctaagencia);
                                setValueBuffer("dc", datosCuentaEmp.dc);
                                setValueBuffer("cuenta", datosCuentaEmp.cuenta);
                        }
                        if (datosSubcuentaEmp && datosSubcuentaEmp.error == 0) {
                                setValueBuffer("codsubcuenta", datosSubcuentaEmp.codsubcuenta);
                                setValueBuffer("idsubcuenta", datosSubcuentaEmp.idsubcuenta);
                        }
                }
                if (!curPago.commitBuffer())
                        return false;
        }
        return true;
}

/* \D Borra los recibos asociados a una factura. No es posible borrar recibos que pertenecen a una remesa o que tienen pagos o devoluciones asociados.

@param idFactura: Identificador de la factura de la que provienen los recibos
@return False si hay error o si el recibo no se puede borrar, true si los recibos se borran correctamente
\end */
function oficial_borrarRecibosCli(idFactura:Number):Boolean
{
        var curRecibos = new FLSqlCursor("reciboscli");
        curRecibos.select("idfactura = " + idFactura);
        while (curRecibos.next()) {
                curRecibos.setModeAccess(curRecibos.Browse);
                curRecibos.refreshBuffer();
                if (curRecibos.valueBuffer("idremesa") != 0) {
                        return false;
                }
                if (this.iface.tienePagosDevCli(curRecibos.valueBuffer("idrecibo"))) {
                        return false;
                }
        }
        curRecibos.select("idfactura = " + idFactura);
        while (curRecibos.next()) {
                curRecibos.setModeAccess(curRecibos.Del);
                curRecibos.refreshBuffer();
                if (!curRecibos.commitBuffer())
                        return false;
        }
        return true;
}

/* \D Obtiene los datos de la cuenta de domiciliación de un cliente

@param codCliente: Identificador del cliente
@return Array con los datos de la cuenta o false si no existe o hay un error. Los elementos de este array son:
        descripcion: Descripcion de la cuenta
        ctaentidad: Código de entidad bancaria
        ctaagencia: Código de oficina
        cuenta: Número de cuenta
        dc: Dígitos de control
        codcuenta: Código de la cuenta en la tabla de cuentas
        error: 0.Sin error 1.Datos no encontrados 2.Error
\end */
function oficial_obtenerDatosCuentaDom(codCliente:String):Array
{
        var datosCuentaDom:Array = [];
        var util:FLUtil = new FLUtil;
        var domiciliarEn:String = util.sqlSelect("clientes", "codcuentadom", "codcliente = '" + codCliente + "'");

        if (domiciliarEn != "") {
                datosCuentaDom = flfactppal.iface.pub_ejecutarQry("cuentasbcocli", "descripcion,ctaentidad,ctaagencia,cuenta,codcuenta", "codcuenta = '" + domiciliarEn + "'");
                switch (datosCuentaDom.result) {
                case -1:
                        datosCuentaDom.error = 1;
                        break;
                case 0:
                        datosCuentaDom.error = 2;
                        break;
                case 1:
                        datosCuentaDom.dc = util.calcularDC(datosCuentaDom.ctaentidad + datosCuentaDom.ctaagencia) + util.calcularDC(datosCuentaDom.cuenta);
                        datosCuentaDom.error = 0;
                        break;
                }
        } else {
                datosCuentaDom.error = 1;
        }

        return datosCuentaDom;
}

/* \D Obtiene los datos de la cuenta de la empresa asociada a un determinado cliente o forma de pago. Si el cliente está informado, toma su cuenta 'Remesar en'. Si no lo está, se toma la cuenta bancaria asociada a la forma de pago

@param codPago: Identificador de la forma de pago
@return Array con los datos de la cuenta o false si no existe o hay un error. Los elementos de este array son:
        descripcion: Descripcion de la cuenta
        ctaentidad: Código de entidad bancaria
        ctaagencia: Código de oficina
        cuenta: Número de cuenta
        dc: Dígitos de control
        codsubcuenta: Código de la subcuenta contable asociada
        codcuenta: Código de la cuenta en la tabla de cuentas
        error: 0.Sin error 1.Datos no encontrados 2.Error
\end */
function oficial_obtenerDatosCuentaEmp(codCliente:String, codPago:String):Array
{
        var util:FLUtil = new FLUtil;
        var datosCuentaEmp:Array = [];
        var codCuentaEmp:String = util.sqlSelect("clientes", "codcuentarem", "codcliente = '" + codCliente + "'");
        if (!codCuentaEmp)
                codCuentaEmp = util.sqlSelect("formaspago", "codcuenta", "codpago = '" + codPago + "'");

        if (!codCuentaEmp.toString().isEmpty()) {
                datosCuentaEmp = flfactppal.iface.pub_ejecutarQry("cuentasbanco", "descripcion,ctaentidad,ctaagencia,cuenta,codsubcuenta,codcuenta", "codcuenta = '" + codCuentaEmp + "'");
                switch (datosCuentaEmp.result) {
                case -1:
                        datosCuentaEmp.error = 1;
                        break;
                case 0:
                        datosCuentaEmp.error = 2;
                        break;
                case 1:
                        datosCuentaEmp.dc = util.calcularDC(datosCuentaEmp.ctaentidad + datosCuentaEmp.ctaagencia) + util.calcularDC(datosCuentaEmp.cuenta);
                        datosCuentaEmp.error = 0;
                        break;
                }
        } else {
                datosCuentaEmp.error = 1;
        }
        return datosCuentaEmp;
}

/* \D Obtiene los datos de la subcuenta contable asociada a una determinada cuenta bancaria. Si la cuenta bancaria no existe busca la subcuenta contable correspondiente a Caja.

@param datosCuentaEmp: Datos de la cuenta bancaria
@return Array con los datos de la subcuenta o false si no existe o hay un error. Los elementos de este array son:
        codsubcuenta: Código de subcuenta
        idsubcuenta: Identificador de la subcuenta en la tabla de subcuenta
        error: 0.Sin error 1.Datos no encontrados 2.Error
\end */
function oficial_obtenerDatosSubcuentaEmp(datosCuentaEmp:Array):Array
{
        var util:FLUtil = new FLUtil;
        var datosSubcuentaEmp:Array = [];
        var codEjercicio:String = flfactppal.iface.pub_ejercicioActual();
        if (datosCuentaEmp.error == 0) {
                datosSubcuentaEmp = flfactppal.iface.pub_ejecutarQry("co_subcuentas", "idsubcuenta,codsubcuenta", "codsubcuenta = '" + datosCuentaEmp.codsubcuenta + "' AND codejercicio = '" + codEjercicio + "'");
                switch (datosSubcuentaEmp.result) {
                case -1:
                        MessageBox.warning(util.translate("scripts", "La cuenta bancaria asociada a la forma de pago seleccionada no tiene una cuenta contable válida asociada"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
                        datosSubcuentaEmp.error = 2;
                        break;
                case 0:
                        datosSubcuentaEmp.error = 2;
                        break;
                case 1:
                        datosSubcuentaEmp.error = 0;
                }
        } else {
                datosSubcuentaEmp = flfacturac.iface.pub_datosCtaEspecial("CAJA", codEjercicio);
        }
        return datosSubcuentaEmp;
}

/* \D Regenera los recibos asociados a una factura a proveedor. Funcionalidad no disponible en la versión oficial
\end */
function oficial_regenerarRecibosProv(cursor:FLSqlCursor, emitirComo:String):Boolean
{
        return true;
}

/* \D Función para sobrecargar. Sirve para añadir al cursor del recibo los datos que añada la extensión
\end */
function oficial_datosReciboCli(curFactura:FLSqlCursor):Boolean
{
        return true;
}

/** \D Cambia la factura relacionada con un recibo a editable o no editable en función de si tiene pagos asociados o no
@param        idRecibo: Identificador de un recibo asociado a la factura
@param        idFactura: Identificador de la factura
@return        true si la verificación del estado es correcta, false en caso contrario
\end */
function oficial_calcularEstadoFacturaCli(idRecibo:String, idFactura:String):Boolean
{
        var util:FLUtil = new FLUtil();
        if (!idFactura)
                idFactura = util.sqlSelect("reciboscli", "idfactura", "idrecibo = " + idRecibo);

        var qryPagos:FLSqlQuery = new FLSqlQuery();
        qryPagos.setTablesList("reciboscli,pagosdevolcli");
        qryPagos.setSelect("p.idpagodevol");
        qryPagos.setFrom("reciboscli r INNER JOIN pagosdevolcli p ON r.idrecibo = p.idrecibo");
        qryPagos.setWhere("r.idfactura = " + idFactura);
        try { qryPagos.setForwardOnly( true ); } catch (e) {}
        if (!qryPagos.exec())
                return false;

        var curFactura:FLSqlCursor = new FLSqlCursor("facturascli");
        curFactura.select("idfactura = " + idFactura);
        curFactura.first();
        if (qryPagos.size() == 0)
                curFactura.setUnLock("editable", true);
        else
                curFactura.setUnLock("editable", false);
        return true;
}

/** \D Cambia la el estado del último pago anterior al especificado, de forma que se mantenga como único pago editable el último de todos
@param        idRecibo: Identificador del recibo al que pertenecen los pagos tratados
@param        idPagoDevol: Identificador del pago que ha cambiado
@param        unlock: Indicador de si el últim pago debe ser editable o no
@return        true si la verificación del estado es correcta, false en caso contrario
\end */
function oficial_cambiaUltimoPagoCli(idRecibo:String, idPagoDevol:String, unlock:Boolean):Boolean
{
        var curPagosDevol:FLSqlCursor = new FLSqlCursor("pagosdevolcli");
        curPagosDevol.select("idrecibo = " + idRecibo + " AND idpagodevol <> " + idPagoDevol + " ORDER BY fecha, idpagodevol");
        if (curPagosDevol.last())
                curPagosDevol.setUnLock("editable", unlock);

        return true;
}

/** \Genera o regenera el asiento contable asociado a un pago o devolución de recibo
@param        curPD: Cursor posicionado en el pago o devolución cuyo asiento se va a regenerar
@return        true si la regeneración se realiza correctamente, false en caso contrario
\end */
function oficial_generarAsientoPagoDevolCli(curPD:FLSqlCursor):Boolean
{
        var util:FLUtil = new FLUtil();
        if (curPD.modeAccess() != curPD.Insert && curPD.modeAccess() != curPD.Edit) {
                return true;
        }

        if (curPD.valueBuffer("nogenerarasiento")) {
                curPD.setNull("idasiento");
                return true;
        }

        var codEjercicio:String = flfactppal.iface.pub_ejercicioActual();
        var datosDoc:Array = flfacturac.iface.pub_datosDocFacturacion(curPD.valueBuffer("fecha"), codEjercicio, "pagosdevolcli");
        if (!datosDoc.ok)
                return false;
        if (datosDoc.modificaciones == true) {
                codEjercicio = datosDoc.codEjercicio;
                curPD.setValueBuffer("fecha", datosDoc.fecha);
        }

        var datosAsiento:Array = [];
        var valoresDefecto:Array;
        valoresDefecto["codejercicio"] = codEjercicio;
        valoresDefecto["coddivisa"] = util.sqlSelect("empresa", "coddivisa", "1 = 1");

        var curTransaccion:FLSqlCursor = new FLSqlCursor("empresa");
        curTransaccion.transaction(false);
        try {
                datosAsiento = flfacturac.iface.pub_regenerarAsiento(curPD, valoresDefecto);
                if (datosAsiento.error == true) {
                        throw util.translate("scripts", "Error al regenerar el asiento");
                }

                if (curPD.valueBuffer("tipo") == "Pago") {
                        var recibo:Array = flfactppal.iface.pub_ejecutarQry("reciboscli", "coddivisa,importe,importeeuros,idfactura,codigo,nombrecliente", "idrecibo = " + curPD.valueBuffer("idrecibo"));
                        if (recibo.result != 1) {
                                throw util.translate("scripts", "Error al obtener los datos del recibo");
                        }
                        if (!this.iface.generarPartidasCli(curPD, valoresDefecto, datosAsiento, recibo)) {
                                throw util.translate("scripts", "Error al obtener la partida de cliente");
                        }
                        if (!this.iface.generarPartidasBanco(curPD, valoresDefecto, datosAsiento, recibo)) {
                                throw util.translate("scripts", "Error al obtener la partida de banco");
                        }
                        if (!this.iface.generarPartidasCambio(curPD, valoresDefecto, datosAsiento, recibo)) {
                                throw util.translate("scripts", "Error al obtener la partida de diferencias por cambio");
                        }
                } else {
                        var recibo:Array = flfactppal.iface.pub_ejecutarQry("reciboscli", "coddivisa,importe,importeeuros,idfactura,codigo,nombrecliente", "idrecibo = " + curPD.valueBuffer("idrecibo"));
                        if (recibo.result != 1) {
                                throw util.translate("scripts", "Error al obtener los datos del recibo");
                        }
                        if (!this.iface.generarPartidasCli(curPD, valoresDefecto, datosAsiento, recibo)) {
                                throw util.translate("scripts", "Error al obtener la partida de cliente");
                        }
                        if (!this.iface.generarPartidasBanco(curPD, valoresDefecto, datosAsiento, recibo)) {
                                throw util.translate("scripts", "Error al obtener la partida de banco");
                        }
                        if (!this.iface.generarPartidasCambio(curPD, valoresDefecto, datosAsiento, recibo)) {
                                throw util.translate("scripts", "Error al obtener la partida de diferencias por cambio");
                        }
                }

                curPD.setValueBuffer("idasiento", datosAsiento.idasiento);

                if (!flcontppal.iface.pub_comprobarAsiento(datosAsiento.idasiento)) {
                        throw util.translate("scripts", "Error al comprobar el asiento");
                }
        } catch (e) {
                curTransaccion.rollback();
                var codRecibo:String = util.sqlSelect("reciboscli", "codigo", "idrecibo = " + curPD.valueBuffer("idrecibo"));
                MessageBox.warning(util.translate("scripts", "Error al generar el asiento correspondiente a %1 del recibo %2:").arg(curPD.valueBuffer("tipo")).arg(codRecibo) + "\n" + e, MessageBox.Ok, MessageBox.NoButton);
                return false;
        }
        curTransaccion.commit();
        return true;
}

/** \D Genera la partida correspondiente al cliente del asiento de pago
@param        curPD: Cursor del pago o devolución
@param        valoresDefecto: Array de valores por defecto (ejercicio, divisa, etc.)
@param        datosAsiento: Array con los datos del asiento
@param        recibo: Array con los datos del recibo asociado al pago
@return        true si la generación es correcta, false en caso contrario
\end */
function oficial_generarPartidasCli(curPD:FLSqlCursor, valoresDefecto:Array, datosAsiento:Array, recibo:Array):Boolean
{
        var util:FLUtil = new FLUtil();
        var ctaHaber:Array = [];
        var codEjercicioFac:String;
        /** \C La cuenta del haber del asiento de pago será la misma cuenta de tipo CLIENT que se usó para realizar el asiento de la correspondiente factura
        \end */
        var idAsientoFactura:Number = util.sqlSelect("reciboscli r INNER JOIN facturascli f" +
                " ON r.idfactura = f.idfactura", "f.idasiento",
                "r.idrecibo = " + curPD.valueBuffer("idrecibo"),
                "facturascli,reciboscli");
        if (!idAsientoFactura) {
                codEjercicioFac = false;
        } else {
                codEjercicioFac = util.sqlSelect("co_asientos", "codejercicio", "idasiento = " + idAsientoFactura);
        }
        if (codEjercicioFac == valoresDefecto.codejercicio) {
                ctaHaber.codsubcuenta = util.sqlSelect("co_partidas p" +
                        " INNER JOIN co_subcuentas s ON p.idsubcuenta = s.idsubcuenta" +
                        " INNER JOIN co_cuentas c ON c.idcuenta = s.idcuenta",
                        "s.codsubcuenta",
                        "p.idasiento = " + idAsientoFactura + " AND c.idcuentaesp = 'CLIENT'",
                        "co_partidas,co_subcuentas,co_cuentas");

                if (!ctaHaber.codsubcuenta) {
			MessageBox.warning(util.translate("scripts", "No se ha encontrado la subcuenta de cliente del asiento contable correspondiente a la factura a pagar.\n Revise que la cuenta contable asociada a la subcuenta tenga el tipo especial 'CLIENT'."), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
                        return false;
                }
        } else {
                var codCliente:String = util.sqlSelect("reciboscli", "codcliente", "idrecibo = " + curPD.valueBuffer("idrecibo"));
                if (codCliente && codCliente != "") {
                        ctaHaber.codsubcuenta = util.sqlSelect("co_subcuentascli", "codsubcuenta", "codcliente = '" + codCliente + "' AND codejercicio = '" + valoresDefecto.codejercicio + "'");
                        if (!ctaHaber.codsubcuenta) {
                                MessageBox.warning(util.translate("scripts", "El cliente %1 no tiene definida ninguna subcuenta en el ejercicio %2.\nEspecifique la subcuenta en la pestaña de contabilidad del formulario de clientes").arg(codCliente).arg(valoresDefecto.codejercicio), MessageBox.Ok, MessageBox.NoButton);
                                return false;
                        }
                } else {
                        ctaHaber = flfacturac.iface.pub_datosCtaEspecial("CLIENT", valoresDefecto.codejercicio);
                        if (!ctaHaber.codsubcuenta) {
                                MessageBox.warning(util.translate("scripts", "No tiene definida ninguna cuenta de tipo CLIENT.\nDebe crear este tipo especial y asociarlo a una cuenta\nen el módulo principal de contabilidad"), MessageBox.Ok, MessageBox.NoButton);
                                return false;
                        }
                }
        }

        ctaHaber.idsubcuenta = util.sqlSelect("co_subcuentas", "idsubcuenta", "codsubcuenta = '" + ctaHaber.codsubcuenta + "' AND codejercicio = '" + valoresDefecto.codejercicio + "'");
        if (!ctaHaber.idsubcuenta) {
                MessageBox.warning(util.translate("scripts", "No existe la subcuenta ")  + ctaHaber.codsubcuenta + util.translate("scripts", " correspondiente al ejercicio ") + valoresDefecto.codejercicio + util.translate("scripts", ".\nPara poder realizar el pago debe crear antes esta subcuenta"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
                return false;
        }

        var haber:Number = 0;
        var haberME:Number = 0;
        var tasaconvHaber:Number = 1;

        if (valoresDefecto.coddivisa == recibo.coddivisa) {
                haber = recibo.importe;
                haberMe = 0;
        } else {
                tasaconvHaber = util.sqlSelect("reciboscli r INNER JOIN facturascli f ON r.idfactura = f.idfactura ", "tasaconv", "idrecibo = " + curPD.valueBuffer("idrecibo"), "reciboscli,facturascli");
                haber = parseFloat(recibo.importeeuros);
                haberME = parseFloat(recibo.importe);
        }
        haber = util.roundFieldValue(haber, "co_partidas", "haber");
        haberME = util.roundFieldValue(haberME, "co_partidas", "haberme");

        var esAbono:Boolean = util.sqlSelect("reciboscli r INNER JOIN facturascli f ON r.idfactura = f.idfactura", "deabono", "idrecibo = " + curPD.valueBuffer("idrecibo"), "reciboscli,facturascli");
        var esPago:Boolean = this.iface.esPagoEstePagoDevol(curPD);

        var curPartida:FLSqlCursor = new FLSqlCursor("co_partidas");
        with(curPartida) {
                setModeAccess(curPartida.Insert);
                refreshBuffer();
                try {
                        setValueBuffer("concepto", datosAsiento.concepto);
                } catch (e) {
                        setValueBuffer("concepto", curPD.valueBuffer("tipo") + " recibo " + recibo.codigo + " - " + recibo.nombrecliente);
                }
                setValueBuffer("idsubcuenta", ctaHaber.idsubcuenta);
                setValueBuffer("codsubcuenta", ctaHaber.codsubcuenta);
                setValueBuffer("idasiento", datosAsiento.idasiento);
                if (esPago) {
                        if (esAbono) {
                                setValueBuffer("debe", haber * -1);
                                setValueBuffer("haber", 0);
                        } else {
                                setValueBuffer("debe", 0);
                                setValueBuffer("haber", haber);
                        }
                } else {
                        if (esAbono) {
                                setValueBuffer("haber", haber * -1);
                                setValueBuffer("debe", 0);
                        } else {
                                setValueBuffer("haber", 0);
                                setValueBuffer("debe", haber);
                        }
                }
                setValueBuffer("coddivisa", recibo.coddivisa);
                setValueBuffer("tasaconv", tasaconvHaber);
                setValueBuffer("debeME", 0);
                setValueBuffer("haberME", haberME);
        }
        if (!curPartida.commitBuffer())
                return false;

        return true;
}

/** \D Genera la partida correspondiente al banco o a caja del asiento de pago
@param        curPD: Cursor del pago o devolución
@param        valoresDefecto: Array de valores por defecto (ejercicio, divisa, etc.)
@param        datosAsiento: Array con los datos del asiento
@param        recibo: Array con los datos del recibo asociado al pago
@return        true si la generación es correcta, false en caso contrario
\end */
function oficial_generarPartidasBanco(curPD:FLSqlCursor, valoresDefecto:Array, datosAsiento:Array, recibo:Array):Boolean
{
        var util:FLUtil = new FLUtil();
        var ctaDebe:Array = [];
        ctaDebe.codsubcuenta = curPD.valueBuffer("codsubcuenta");
        ctaDebe.idsubcuenta = util.sqlSelect("co_subcuentas", "idsubcuenta", "codsubcuenta = '" + ctaDebe.codsubcuenta + "' AND codejercicio = '" + valoresDefecto.codejercicio + "'");
        if (!ctaDebe.idsubcuenta) {
                MessageBox.warning(util.translate("scripts", "No tiene definida la subcuenta %1 en el ejercicio %2.\nAntes de dar el pago debe crear la subcuenta o modificar el ejercicio").arg(ctaDebe.codsubcuenta).arg(valoresDefecto.codejercicio), MessageBox.Ok, MessageBox.NoButton);
                return false;
        }

        var debe:Number = 0;
        var debeME:Number = 0;
        var tasaconvDebe:Number = 1;
        if (valoresDefecto.coddivisa == recibo.coddivisa) {
                debe = recibo.importe;
                debeME = 0;
        } else {
                tasaconvDebe = curPD.valueBuffer("tasaconv");
                debe = parseFloat(recibo.importe) * parseFloat(tasaconvDebe);
                debeME = parseFloat(recibo.importe);
        }
        debe = util.roundFieldValue(debe, "co_partidas", "debe");
        debeME = util.roundFieldValue(debeME, "co_partidas", "debeme");

        var esAbono:Boolean = util.sqlSelect("reciboscli r INNER JOIN facturascli f ON r.idfactura = f.idfactura", "deabono", "idrecibo = " + curPD.valueBuffer("idrecibo"), "reciboscli,facturascli");
        var esPago:Boolean = this.iface.esPagoEstePagoDevol(curPD);

        var curPartida:FLSqlCursor = new FLSqlCursor("co_partidas");
        with(curPartida) {
                setModeAccess(curPartida.Insert);
                refreshBuffer();
                try {
                        setValueBuffer("concepto", datosAsiento.concepto);
                } catch (e) {
                        setValueBuffer("concepto", curPD.valueBuffer("tipo") + " recibo " + recibo.codigo + " - " + recibo.nombrecliente);
                }
                setValueBuffer("idsubcuenta", ctaDebe.idsubcuenta);
                setValueBuffer("codsubcuenta", ctaDebe.codsubcuenta);
                setValueBuffer("idasiento", datosAsiento.idasiento);
                if (esPago) {
                        if (esAbono) {
                                setValueBuffer("debe", 0);
                                setValueBuffer("haber", debe * -1);
                        } else {
                                setValueBuffer("debe", debe);
                                setValueBuffer("haber", 0);
                        }
                } else {
                        if (esAbono) {
                                setValueBuffer("haber", 0);
                                setValueBuffer("debe", debe * -1);
                        } else {
                                setValueBuffer("haber", debe);
                                setValueBuffer("debe", 0);
                        }
                }

                setValueBuffer("coddivisa", recibo.coddivisa);
                setValueBuffer("tasaconv", tasaconvDebe);
                setValueBuffer("debeME", debeME);
                setValueBuffer("haberME", 0);
        }
        if (!curPartida.commitBuffer())
                return false;

        return true;
}
/** \D Genera, si es necesario, la partida de diferecias positivas o negativas de cambio
@param        curPD: Cursor del pago o devolución
@param        valoresDefecto: Array de valores por defecto (ejercicio, divisa, etc.)
@param        datosAsiento: Array con los datos del asiento
@param        recibo: Array con los datos del recibo asociado al pago
@return        true si la generación es correcta, false en caso contrario
\end */
function oficial_generarPartidasCambio(curPD:FLSqlCursor, valoresDefecto:Array, datosAsiento:Array, recibo:Array):Boolean
{
        /** \C En el caso de que la divisa sea extranjera y la tasa de cambio haya variado desde el momento de la emisión de la factura, la diferencia se imputará a la correspondiente cuenta de diferencias de cambio.
        \end */

        if (valoresDefecto.coddivisa == recibo.coddivisa)
                return true;

        var util:FLUtil = new FLUtil();
        var debe:Number = 0;
        var haber:Number = 0;
        var tasaconvDebe:Number = 1;
        var tasaconvHaber:Number = 1;
        var diferenciaCambio:Number = 0;

        tasaconvDebe = curPD.valueBuffer("tasaconv");
        tasaconvHaber = util.sqlSelect("reciboscli r INNER JOIN facturascli f ON r.idfactura = f.idfactura ", "tasaconv", "idrecibo = " + curPD.valueBuffer("idrecibo"), "reciboscli,facturascli");
        debe = parseFloat(recibo.importe) * parseFloat(tasaconvDebe);
        debe = util.roundFieldValue(debe, "co_partidas", "debe");

        haber = parseFloat(recibo.importeeuros);
        haber = util.roundFieldValue(haber, "co_partidas", "debe");

        diferenciaCambio = debe - haber;
        if (util.buildNumber(diferenciaCambio, "f", 2) == "0.00" || util.buildNumber(diferenciaCambio, "f", 2) == "-0.00") {
                diferenciaCambio = 0;
                return true;
        }

        diferenciaCambio = util.roundFieldValue(diferenciaCambio, "co_partidas", "debe");

        var ctaDifCambio:Array = [];
        var debeDifCambio:Number = 0;
        var haberDifCambio:Number = 0;
        if (diferenciaCambio > 0) {
                ctaDifCambio = flfacturac.iface.pub_datosCtaEspecial("CAMPOS", valoresDefecto.codejercicio);
                if (ctaDifCambio.error != 0)
                        return false;
                debeDifCambio = 0;
                haberDifCambio = diferenciaCambio;
        } else {
                ctaDifCambio = flfacturac.iface.pub_datosCtaEspecial("CAMNEG", valoresDefecto.codejercicio);
                if (ctaDifCambio.error != 0)
                        return false;
                diferenciaCambio = 0 - diferenciaCambio;
                debeDifCambio = diferenciaCambio;
                haberDifCambio = 0;
        }
        /// Esto lo usan algunas extensiones
//         if (curPD.valueBuffer("tipo") == "Devolución") {
//                 var aux:Number = debeDifCambio;
//                 debeDifCambio = haberDifCambio;
//                 haberDifCambio = aux;
//         }
        var esPago:Boolean = this.iface.esPagoEstePagoDevol(curPD);

        var curPartida:FLSqlCursor = new FLSqlCursor("co_partidas");
        with(curPartida) {
                setModeAccess(curPartida.Insert);
                refreshBuffer();
                try {
                        setValueBuffer("concepto", datosAsiento.concepto);
                } catch (e) {
                        setValueBuffer("concepto", curPD.valueBuffer("tipo") + " recibo " + recibo.codigo + " - " + recibo.nombrecliente);
                }
                setValueBuffer("idsubcuenta", ctaDifCambio.idsubcuenta);
                setValueBuffer("codsubcuenta", ctaDifCambio.codsubcuenta);
                setValueBuffer("idasiento", datosAsiento.idasiento);
                if (esPago) {
                        setValueBuffer("debe", debeDifCambio);
                        setValueBuffer("haber", haberDifCambio);
                } else {
                        setValueBuffer("debe", haberDifCambio);
                        setValueBuffer("haber", debeDifCambio);
                }
                setValueBuffer("coddivisa", valoresDefecto.coddivisa);
                setValueBuffer("tasaconv", 1);
                setValueBuffer("debeME", 0);
                setValueBuffer("haberME", 0);
        }
        if (!curPartida.commitBuffer())
                return false;

        return true;
}

function oficial_esPagoEstePagoDevol(curPD:FLSqlCursor):Boolean
{
        return (curPD.valueBuffer("tipo") == "Pago");
}

function oficial_comprobarCuentasDom(idRemesa:String):Boolean
{
        var util:FLUtil = new FLUtil();

        var qryRecibos:FLSqlQuery = new FLSqlQuery;
        qryRecibos.setTablesList("pagosdevolcli,reciboscli,cuentasbcocli");
        qryRecibos.setSelect("r.codigo, r.codcliente, r.nombrecliente");
        qryRecibos.setFrom("pagosdevolcli pd INNER JOIN reciboscli r ON pd.idrecibo = r.idrecibo LEFT OUTER JOIN cuentasbcocli cc ON (r.codcliente = cc.codcliente AND r.codcuenta = cc.codcuenta)");
        qryRecibos.setWhere("pd.idremesa = " + idRemesa + " AND cc.codcuenta IS NULL ORDER BY codcliente, codigo");
        qryRecibos.setForwardOnly( true );
        if (!qryRecibos.exec())
                return false;
debug(qryRecibos.sql());
        var msgError:String = "";
        var i:Number = 0;
        while (qryRecibos.next()) {
                msgError += "\n" + util.translate("scripts", "Cliente: %1 (%2), Recibo %3").arg(qryRecibos.value("r.nombrecliente")).arg(qryRecibos.value("r.codcliente")).arg(qryRecibos.value("r.codigo"));
        }
        if (msgError != "") {
                var res:Number = MessageBox.warning(util.translate("scripts", "Los siguientes recibos no tienen especificada una cuenta de domiciliación válida:") + msgError + "\n" + util.translate("scripts", "¿Desea continuar?"), MessageBox.Yes, MessageBox.No);
                if (res != MessageBox.Yes)
                        return false;
        }
        return true;
}

/** \D Indica si el módulo de autómata está instalado y activado
@return        true si está activado, false en caso contrario
\end */
function oficial_automataActivado():Boolean
{
        if (!sys.isLoadedModule("flautomata"))
                return false;

        if (formau_automata.iface.pub_activado())
                return true;

        return false;
}

/** \Genera o regenera el asiento contable asociado a un pago de una remesa
@param        curPR: Cursor posicionado en el pago cuyo asiento se va a regenerar
@return        true si la regeneración se realiza correctamente, false en caso contrario
\end */
function oficial_generarAsientoPagoRemesa(curPR:FLSqlCursor):Boolean
{
        var util:FLUtil = new FLUtil();
        if (curPR.modeAccess() != curPR.Insert && curPR.modeAccess() != curPR.Edit)
                return true;

        if (curPR.valueBuffer("nogenerarasiento")) {
                curPR.setNull("idasiento");
                return true;
        }
        var codEjercicio:String = flfactppal.iface.pub_ejercicioActual();
        var datosDoc:Array = flfacturac.iface.pub_datosDocFacturacion(curPR.valueBuffer("fecha"), codEjercicio, "pagosdevolrem");
        if (!datosDoc.ok)
                return false;
        if (datosDoc.modificaciones == true) {
                codEjercicio = datosDoc.codEjercicio;
                curPR.setValueBuffer("fecha", datosDoc.fecha);
        }

        var datosAsiento:Array = [];
        var valoresDefecto:Array;
        valoresDefecto["codejercicio"] = codEjercicio;
        valoresDefecto["coddivisa"] = util.sqlSelect("empresa", "coddivisa", "1 = 1");

        var curTransaccion:FLSqlCursor = new FLSqlCursor("empresa");
        curTransaccion.transaction(false);
        try {
                datosAsiento = flfacturac.iface.pub_regenerarAsiento(curPR, valoresDefecto);
                if (datosAsiento.error == true) {
                        throw util.translate("scripts", "Error al regenerar el asiento");
                }
                var remesa:Array = flfactppal.iface.pub_ejecutarQry("remesas", "coddivisa,total,fecha,idremesa,codsubcuenta,codcuenta", "idremesa = " + curPR.valueBuffer("idremesa"));
                if (remesa.result != 1) {
                        throw util.translate("scripts", "Error al obtener los datos de la remesa");
                }
                if (curPR.valueBuffer("tipo") == "Pago") {
                        if (!this.iface.generarPartidasEFCOGC(curPR, valoresDefecto, datosAsiento, remesa)) {
                                throw util.translate("scripts", "Error al obtener la partida de efectos comerciales de gestión de cobro");
                        }
                        if (!this.iface.generarPartidasBancoRem(curPR, valoresDefecto, datosAsiento, remesa)) {
                                throw util.translate("scripts", "Error al generar la partida de banco");
                        }
                }
                curPR.setValueBuffer("idasiento", datosAsiento.idasiento);
                if (!flcontppal.iface.pub_comprobarAsiento(datosAsiento.idasiento)) {
                        throw util.translate("scripts", "Error al comprobar el asiento");
                }
        } catch (e) {
                curTransaccion.rollback();
                MessageBox.warning(util.translate("scripts", "Error al generar el asiento de la remesa:") + "\n" + e, MessageBox.Ok, MessageBox.NoButton);
                return false;
        }
        curTransaccion.commit();

        return true;
}

/** \D Genera la parte del asiento del pago correspondiente a la subcuenta especial EFCOGC
@param        curPR: Cursor del pago de la remesa
@param        idAsiento: Id del asiento asociado
@param        valoresDefecto: Array con los valores por defecto de ejercicio y divisa
@return        VERDADERO si no hay error, FALSO en otro caso
\end */
function oficial_generarPartidasEFCOGC(curPR:FLSqlCursor, valoresDefecto:Array, datosAsiento:Array, remesa:Array):Boolean
{
        var util:FLUtil = new FLUtil();

        var haber:Number = 0;
        var haberME:Number = 0;
        var ctaHaber:Array = [];
        ctaHaber.codsubcuenta = util.sqlSelect("cuentasbanco","codsubcuentaecgc","codcuenta = '" + remesa.codcuenta + "'");

        if (!ctaHaber.codsubcuenta || ctaHaber.codsubcuenta == "") {
                MessageBox.warning(util.translate("scripts", "No tiene definida de efectos comerciales de gestión de cobro para la cuenta %1").arg(remesa.codcuenta), MessageBox.Ok, MessageBox.NoButton);
                return false;
        }

        ctaHaber.idsubcuenta = util.sqlSelect("co_subcuentas", "idsubcuenta", "codsubcuenta = '" + ctaHaber.codsubcuenta + "' AND codejercicio = '" + valoresDefecto.codejercicio + "'");
        if (!ctaHaber.idsubcuenta) {
                MessageBox.warning(util.translate("scripts", "No tiene definida la subcuenta %1 en el ejercicio %2.\nAntes de dar el pago debe crear la subcuenta o modificar el ejercicio").arg(ctaDebe.codsubcuenta).arg(valoresDefecto.codejercicio), MessageBox.Ok, MessageBox.NoButton);
                return false;
        }

        haber = remesa.total;
        haberME = 0;
        haber = util.roundFieldValue(haber, "co_partidas", "haber");
        haberME = util.roundFieldValue(haberME, "co_partidas", "haberme");

        var curPartida:FLSqlCursor = new FLSqlCursor("co_partidas");
        with (curPartida) {
                setModeAccess(curPartida.Insert);
                refreshBuffer();
                setValueBuffer("concepto", curPR.valueBuffer("tipo") + " " + util.translate("scripts", "remesa") + " " + remesa.idremesa);
                setValueBuffer("idsubcuenta", ctaHaber.idsubcuenta);
                setValueBuffer("codsubcuenta", ctaHaber.codsubcuenta);
                setValueBuffer("idasiento", datosAsiento.idasiento);
                setValueBuffer("debe", 0);
                setValueBuffer("haber", haber);
                setValueBuffer("debeME", 0);
                setValueBuffer("haberME", haberME);
        }

        if (!curPartida.commitBuffer())
                return false;

        return true;
}

/** \D Genera la partida correspondiente al banco o a caja del asiento de pago de la remesa
@param        curPR: Cursor del pago de la remesa
@param        valoresDefecto: Array de valores por defecto (ejercicio, divisa, etc.)
@param        datosAsiento: Array con los datos del asiento
@param        recibo: Array con los datos del recibo asociado al pago de la remesa
@return        true si la generación es correcta, false en caso contrario
\end */
function oficial_generarPartidasBancoRem(curPR:FLSqlCursor, valoresDefecto:Array, datosAsiento:Array, remesa:Array):Boolean
{
        var util:FLUtil = new FLUtil();
        var ctaDebe:Array = [];
        ctaDebe.codsubcuenta = util.sqlSelect("cuentasbanco", "codsubcuenta", "codcuenta = '" + remesa.codcuenta + "'");
        ctaDebe.idsubcuenta = util.sqlSelect("co_subcuentas", "idsubcuenta", "codsubcuenta = '" + ctaDebe.codsubcuenta + "' AND codejercicio = '" + valoresDefecto.codejercicio + "'");
        if (!ctaDebe.idsubcuenta) {
                MessageBox.warning(util.translate("scripts", "No tiene definida la subcuenta %1 en el ejercicio %2.\nAntes de dar el pago debe crear la subcuenta o modificar el ejercicio").arg(ctaDebe.codsubcuenta).arg(valoresDefecto.codejercicio), MessageBox.Ok, MessageBox.NoButton);
                return false;
        }

        var debe:Number = 0;
        var debeME:Number = 0;
        var tasaconvDebe:Number = 1;
        if (valoresDefecto.coddivisa == remesa.coddivisa) {
                debe = parseFloat(remesa.total);
                debeME = 0;
        } else {
                tasaconvDebe = curPR.valueBuffer("tasaconv");
                debe = parseFloat(remesa.total) * parseFloat(tasaconvDebe);
                debeME = parseFloat(remesa.total);
        }
        debe = util.roundFieldValue(debe, "co_partidas", "debe");
        debeME = util.roundFieldValue(debeME, "co_partidas", "debeme");

        var curPartida:FLSqlCursor = new FLSqlCursor("co_partidas");
        with(curPartida) {
                setModeAccess(curPartida.Insert);
                refreshBuffer();
                setValueBuffer("concepto", curPR.valueBuffer("tipo") + " " + util.translate("scripts", "remesa") + " " + remesa.idremesa);
                setValueBuffer("idsubcuenta", ctaDebe.idsubcuenta);
                setValueBuffer("codsubcuenta", ctaDebe.codsubcuenta);
                setValueBuffer("idasiento", datosAsiento.idasiento);
                setValueBuffer("debe", debe);
                setValueBuffer("haber", 0);
                setValueBuffer("coddivisa", remesa.coddivisa);
                setValueBuffer("tasaconv", tasaconvDebe);
                setValueBuffer("debeME", debeME);
                setValueBuffer("haberME", 0);
        }
        if (!curPartida.commitBuffer())
                return false;

        return true;
}
//// OFICIAL /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition proveed */
/////////////////////////////////////////////////////////////////
//// PROVEED ////////////////////////////////////////////////////
/** \D
Indica si un determinado recibo tiene pagos y/o devoluciones asociadas.
@param idRecibo: Identificador del recibo
@return True: Tiene, False: No tiene
\end */
function proveed_tienePagosDevProv(idRecibo:Number):Boolean
{
	var curPagosDev:FLSqlCursor = new FLSqlCursor("pagosdevolprov");
	curPagosDev.select("idrecibo = " + idRecibo);
	return curPagosDev.next();
}

function proveed_regenerarRecibosProv(cursor:FLSqlCursor, forzarEmitirComo:String):Boolean
{
	if (!this.iface.siGenerarRecibosProv(cursor)) {
		return true;
	}

	var util:FLUtil = new FLUtil();
	var contActiva:Boolean = sys.isLoadedModule("flcontppal") && util.sqlSelect("empresa", "contintegrada", "1 = 1");
	var idFactura:Number = cursor.valueBuffer("idfactura");

	if (!this.iface.curReciboProv) {
		this.iface.curReciboProv = new FLSqlCursor("recibosprov");
	}
	if (!this.iface.borrarRecibosProv(idFactura)) {
		return false;
	}
	if (parseFloat(cursor.valueBuffer("total")) == 0) {
		return true;
	}

	var codPago:String = cursor.valueBuffer("codpago");
	var emitirComo:String;
	if (forzarEmitirComo) {
		emitirComo = forzarEmitirComo;
	} else {
		emitirComo = util.sqlSelect("formaspago", "genrecibos", "codpago = '" + codPago + "'");
	}

	var codProveedor:String = cursor.valueBuffer("codproveedor");
	var datosCuentaDom = this.iface.obtenerDatosCuentaDomProv(codProveedor);
	if (datosCuentaDom.error == 2) {
		return false;
	}

	var total:Number = parseFloat(cursor.valueBuffer("total"));
	var idRecibo:Number;
	var numRecibo:Number = 1;
	var importeRecibo:Number, importeEuros:Number;
	var diasAplazado:Number, fechaVencimiento:String;
	var tasaConv:Number = parseFloat(cursor.valueBuffer("tasaconv"));
	var divisa:String = util.sqlSelect("divisas", "descripcion", "coddivisa = '" + cursor.valueBuffer("coddivisa") + "'");

	var codCuentaEmp:String = "";
	var desCuentaEmp:String = "";
	var ctaEntidadEmp:String = "";
	var ctaAgenciaEmp:String = "";
	var dCEmp:String = "";
	var cuentaEmp:String = "";
	var codSubcuentaEmp:String = "";
	var idSubcuentaEmp:String = "";
	if (emitirComo == "Pagados") {
		emitirComo = "Pagado";
		/*D Si los recibos deben emitirse como pagados, se generarán los registros de pago asociados a cada recibo. Si el módulo Principal de contabilidad está cargado, se generará el correspondienta asiento. La subcuenta contable del Debe del apunte corresponderá a la subcuenta contable asociada a la cuenta corriente correspondiente a la cuenta de pago del proveedor, o en su defecto a la forma de pago de la factura. Si dicha cuenta corriente no está especificada, la subcuenta contable del Debe del asiento será la correspondiente a la cuenta especial Caja.
		\end */
		codCuentaEmp = this.iface.codCuentaPagoProv(cursor);

		if (!codCuentaEmp) {
			codCuentaEmp = util.sqlSelect("proveedores", "codcuentapago", "codproveedor = '" + codProveedor + "'");
		}
		if (!codCuentaEmp) {
			codCuentaEmp = util.sqlSelect("formaspago", "codcuenta", "codpago = '" + codPago + "'");
		}
		var datosCuentaEmp:Array = [];
		if (codCuentaEmp.toString().isEmpty()) {
			if (contActiva) {
				var qrySubcuenta:FLSqlQuery = new FLSqlQuery();
				with (qrySubcuenta) {
					setTablesList("co_cuentas,co_subcuentas");
					setSelect("s.idsubcuenta, s.codsubcuenta");
					setFrom("co_cuentas c INNER JOIN co_subcuentas s ON c.idcuenta = s.idcuenta");
					setWhere("c.codejercicio = '" + cursor.valueBuffer("codejercicio") + "'" + " AND c.idcuentaesp = 'CAJA'");
				}
				if (!qrySubcuenta.exec()) {
					return false;
				}
				if (!qrySubcuenta.first())
					return false;
				idSubcuentaEmp = qrySubcuenta.value(0);
				codSubcuentaEmp = qrySubcuenta.value(1);
			}
		} else {
			datosCuentaEmp = flfactppal.iface.pub_ejecutarQry("cuentasbanco", "descripcion,ctaentidad,ctaagencia,cuenta,codsubcuenta", "codcuenta = '" + codCuentaEmp + "'");
			idSubcuentaEmp = util.sqlSelect("co_subcuentas", "idsubcuenta", "codsubcuenta = '" + datosCuentaEmp.codsubcuenta + "'" + " AND codejercicio = '" + cursor.valueBuffer("codEjercicio") + "'");
			desCuentaEmp = datosCuentaEmp.descripcion;
			ctaEntidadEmp = datosCuentaEmp.ctaentidad;
			ctaAgenciaEmp = datosCuentaEmp.ctaagencia;
			cuentaEmp = datosCuentaEmp.cuenta;
			var dc1:String = util.calcularDC(ctaEntidadEmp + ctaAgenciaEmp);
			var dc2:String = util.calcularDC(cuentaEmp);
			dCEmp = dc1 + dc2;
			codSubcuentaEmp =  datosCuentaEmp.codsubcuenta;
		}
	} else
		emitirComo = "Emitido";
	var numPlazo:Number = 1;
	var curPlazos:FLSqlCursor = new FLSqlCursor("plazos");
	var importeAcumulado:Number = 0;
	curPlazos.select("codpago = '" + codPago + "' ORDER BY dias");
	while (curPlazos.next()) {
		if ( curPlazos.at() == ( curPlazos.size() - 1 ) ) {
			importeRecibo = parseFloat(total) - parseFloat(importeAcumulado);
		} else {
			importeRecibo = (parseFloat(total) * parseFloat(curPlazos.valueBuffer("aplazado"))) / 100;
		}
		importeRecibo = util.roundFieldValue(importeRecibo, "recibosprov","importe");
		importeAcumulado = parseFloat(importeAcumulado) + parseFloat(importeRecibo);

		importeEuros = importeRecibo * tasaConv;
		diasAplazado = curPlazos.valueBuffer("dias");

		with (this.iface.curReciboProv) {
			setModeAccess(Insert);
			refreshBuffer();
			setValueBuffer("numero", numRecibo);
			setValueBuffer("idfactura", idFactura);
			setValueBuffer("importe", importeRecibo);
			setValueBuffer("texto", util.enLetraMoneda(importeRecibo, divisa));
			setValueBuffer("importeeuros", importeEuros);
			setValueBuffer("coddivisa", cursor.valueBuffer("coddivisa"));
			setValueBuffer("codigo", cursor.valueBuffer("codigo") + "-" + flfacturac.iface.pub_cerosIzquierda(numRecibo, 2));
			setValueBuffer("codproveedor", codProveedor);
			setValueBuffer("nombreproveedor", cursor.valueBuffer("nombre"));
			setValueBuffer("cifnif", cursor.valueBuffer("cifnif"));
			setValueBuffer("fecha", cursor.valueBuffer("fecha"));
			setValueBuffer("estado", emitirComo);

			if (datosCuentaDom.error == 0) {
				setValueBuffer("codcuenta", datosCuentaDom.codcuenta);
				setValueBuffer("descripcion", datosCuentaDom.descripcion);
				setValueBuffer("ctaentidad", datosCuentaDom.ctaentidad);
				setValueBuffer("ctaagencia", datosCuentaDom.ctaagencia);
				setValueBuffer("cuenta", datosCuentaDom.cuenta);
				setValueBuffer("dc", datosCuentaDom.dc);
			}
		}
		if (codProveedor && codProveedor != "") {
			var qryDir:FLSqlQuery = new FLSqlQuery;
			with (qryDir) {
				setTablesList("dirproveedores");
				setSelect("id, direccion, ciudad, codpostal, provincia, codpais");
				setFrom("dirproveedores");
				setWhere("codproveedor = '" + codProveedor + "' AND direccionppal = true");
				setForwardOnly(true);
			}
			if (!qryDir.exec())
				return false;
			if (qryDir.first()) {
				with (this.iface.curReciboProv) {
					setValueBuffer("coddir", qryDir.value("id"));
					setValueBuffer("direccion", qryDir.value("direccion"));
					setValueBuffer("ciudad", qryDir.value("ciudad"));
					setValueBuffer("codpostal", qryDir.value("codpostal"));
					setValueBuffer("provincia", qryDir.value("provincia"));
					setValueBuffer("codpais", qryDir.value("codpais"));
				}
			}
		}

		fechaVencimiento = this.iface.calcFechaVencimientoProv(cursor, numPlazo, diasAplazado);
		this.iface.curReciboProv.setValueBuffer("fechav", fechaVencimiento);

		if (!this.iface.datosReciboProv())
			return false;

		if (!this.iface.curReciboProv.commitBuffer())
			return false;

		if (emitirComo == "Pagado") {
			idRecibo = this.iface.curReciboProv.valueBuffer("idrecibo");

			var curPago:FLSqlCursor = new FLSqlCursor("pagosdevolprov");
			with(curPago) {
				setModeAccess(Insert);
				refreshBuffer();
				setValueBuffer("idrecibo", idRecibo);
				setValueBuffer("tipo", "Pago");
				setValueBuffer("fecha", cursor.valueBuffer("fecha"));
				setValueBuffer("codcuenta", codCuentaEmp);
				setValueBuffer("descripcion", desCuentaEmp);
				setValueBuffer("ctaentidad", ctaEntidadEmp);
				setValueBuffer("ctaagencia", ctaAgenciaEmp);
				setValueBuffer("dc", dCEmp);
				setValueBuffer("cuenta", cuentaEmp);
				setValueBuffer("codsubcuenta", codSubcuentaEmp);
				setValueBuffer("idSubcuenta", idSubcuentaEmp);
				setValueBuffer("tasaconv", cursor.valueBuffer("tasaconv"));
			}

			if (!curPago.commitBuffer())
				return false;
		}
		numRecibo++;
	}

	if (emitirComo == "Pagado") {
		if (!this.iface.calcularEstadoFacturaProv(false, idFactura))
			return false;
	}

	return true;
}

/** \C Se elimina, si es posible, el asiento contable asociado al pago o devolución
\end */
function proveed_afterCommit_pagosdevolprov(curPD:FLSqlCursor):Boolean
{
	var idRecibo:String = curPD.valueBuffer("idrecibo");

	/** \C Se cambia el pago anterior al actual para que sólo el último sea editable
	\end */
	switch (curPD.modeAccess()) {
		case curPD.Insert:
		case curPD.Edit: {
			if (!this.iface.cambiaUltimoPagoProv(idRecibo, curPD.valueBuffer("idpagodevol"), false))
			return false;
			break;
		}
		case curPD.Del: {
			if (!this.iface.cambiaUltimoPagoProv(idRecibo, curPD.valueBuffer("idpagodevol"), true))
			return false;
			break;
		}
	}

	if (!this.iface.calcularEstadoFacturaProv(idRecibo))
		return false;

	var util:FLUtil = new FLUtil();
	if (sys.isLoadedModule("flcontppal") == false || util.sqlSelect("empresa", "contintegrada", "1 = 1") == false)
		return true;

	switch (curPD.modeAccess()) {
		case curPD.Del: {
			if (curPD.isNull("idasiento"))
				return true;

			var idAsiento:Number = curPD.valueBuffer("idasiento");
			if (flfacturac.iface.pub_asientoBorrable(idAsiento) == false)
				return false;

			var curAsiento:FLSqlCursor = new FLSqlCursor("co_asientos");
			curAsiento.select("idasiento = " + idAsiento);
			if (curAsiento.first()) {
				curAsiento.setUnLock("editable", true);
				curAsiento.setModeAccess(curAsiento.Del);
				curAsiento.refreshBuffer();
				if (!curAsiento.commitBuffer())
					return false;
			}
			break;
		}
		case curPD.Edit: {
			if (curPD.valueBuffer("nogenerarasiento")) {
				var idAsientoAnterior:String = curPD.valueBufferCopy("idasiento");
				if (idAsientoAnterior && idAsientoAnterior != "") {
					if (!flfacturac.iface.pub_eliminarAsiento(idAsientoAnterior))
						return false;
				}
			}
			break;
		}
	}
	return true;
}

/** \C Se regenera, si es posible, el asiento contable asociado al pago o devolución
\end */
function proveed_beforeCommit_pagosdevolprov(curPD:FLSqlCursor):Boolean
{
	var util:FLUtil = new FLUtil();
	if (sys.isLoadedModule("flcontppal") && util.sqlSelect("empresa", "contintegrada", "1 = 1") && !curPD.valueBuffer("nogenerarasiento")) {
		if (!this.iface.generarAsientoPagoDevolProv(curPD))
			return false;
	}
	return true;
}

function proveed_generarAsientoPagoDevolProv(curPD:FLSqlCursor):Boolean
{
	var util:FLUtil = new FLUtil();
	if (curPD.modeAccess() != curPD.Insert && curPD.modeAccess() != curPD.Edit)
		return true;

	if (curPD.valueBuffer("nogenerarasiento")) {
		curPD.setNull("idasiento");
		return true;
	}

	var codEjercicio:String = flfactppal.iface.pub_ejercicioActual();
	var datosDoc:Array = flfacturac.iface.pub_datosDocFacturacion(curPD.valueBuffer("fecha"), codEjercicio, "pagosdevolprov");
	if (!datosDoc.ok)
		return false;
	if (datosDoc.modificaciones == true) {
		codEjercicio = datosDoc.codEjercicio;
		curPD.setValueBuffer("fecha", datosDoc.fecha);
	}

	var datosAsiento:Array = [];
	var valoresDefecto:Array;
	valoresDefecto["codejercicio"] = codEjercicio;
	valoresDefecto["coddivisa"] = util.sqlSelect("empresa", "coddivisa", "1 = 1");

	var curTransaccion:FLSqlCursor = new FLSqlCursor("empresa");
	curTransaccion.transaction(false);
	try {
		datosAsiento = flfacturac.iface.pub_regenerarAsiento(curPD, valoresDefecto);
		if (datosAsiento.error == true) {
			throw util.translate("scripts", "Error al regenerar el asiento");
		}
		if (curPD.valueBuffer("tipo") == "Pago") {
			var recibo:Array = flfactppal.iface.pub_ejecutarQry("recibosprov", "coddivisa,importe,importeeuros,idfactura,codigo,nombreproveedor", "idrecibo = " + curPD.valueBuffer("idrecibo"));
			if (recibo.result != 1) {
				throw util.translate("scripts", "Error al obtener los datos del recibo");
			}
			if (!this.iface.generarPartidasProv(curPD, valoresDefecto, datosAsiento, recibo)) {
				throw util.translate("scripts", "Error al obtener la partida de proveedor");
			}
			if (!this.iface.generarPartidasBancoProv(curPD, valoresDefecto, datosAsiento, recibo)) {
				throw util.translate("scripts", "Error al obtener la partida de banco");
			}
			if (!this.iface.generarPartidasCambioProv(curPD, valoresDefecto, datosAsiento, recibo)) {
				throw util.translate("scripts", "Error al obtener la partida de diferencias por cambio");
			}
		} else {
			/** \D En el caso de dar una devolución, las subcuentas del asiento contable serán las inversas al asiento contable correspondiente al último pago
			\end */
			var idAsientoPago:Number = util.sqlSelect("pagosdevolprov", "idasiento", "idrecibo = " + curPD.valueBuffer("idrecibo") + " AND  tipo = 'Pago' ORDER BY fecha DESC");
			if (this.iface.generarAsientoInverso(datosAsiento.idasiento, idAsientoPago, datosAsiento.concepto, valoresDefecto.codejercicio) == false) {
				throw util.translate("scripts", "Error al generar el asiento inverso al pago");
			}
		}

		curPD.setValueBuffer("idasiento", datosAsiento.idasiento);

		if (!flcontppal.iface.pub_comprobarAsiento(datosAsiento.idasiento)) {
			throw util.translate("scripts", "Error al comprobar el asiento");
		}
	} catch (e) {
		curTransaccion.rollback();
		var codRecibo:String = util.sqlSelect("recibosprov", "codigo", "idrecibo = " + curPD.valueBuffer("idrecibo"));
		MessageBox.warning(util.translate("scripts", "Error al generar el asiento correspondiente a %1 del recibo %2:").arg(curPD.valueBuffer("tipo")).arg(codRecibo) + "\n" + e, MessageBox.Ok, MessageBox.NoButton);
		return false;
	}
	curTransaccion.commit();

	return true;
}

/** \D Genera la partida correspondiente al proveedor del asiento de pago
@param	curPD: Cursor del pago o devolución
@param	valoresDefecto: Array de valores por defecto (ejercicio, divisa, etc.)
@param	datosAsiento: Array con los datos del asiento
@param	recibo: Array con los datos del recibo asociado al pago
@return	true si la generación es correcta, false en caso contrario
\end */
function proveed_generarPartidasProv(curPD:FLSqlCursor, valoresDefecto:Array, datosAsiento:Array, recibo:Array):Boolean
{
	var util:FLUtil = new FLUtil();
	var ctaDebe:Array = [];
	var codEjercicioFac:String;

	/** \C La cuenta del debe del asiento de pago será la misma cuenta de tipo PROVEE que se usó para realizar el asiento de la correspondiente factura
	\end */
	var idAsientoFactura:Number = util.sqlSelect("recibosprov r INNER JOIN facturasprov f" + " ON r.idfactura = f.idfactura", "f.idasiento", "r.idrecibo = " + curPD.valueBuffer("idrecibo"), "facturasprov,recibosprov");
	if (!idAsientoFactura) {
		codEjercicioFac = false;
	} else {
		codEjercicioFac = util.sqlSelect("co_asientos", "codejercicio", "idasiento = " + idAsientoFactura);
	}
	if (codEjercicioFac == valoresDefecto.codejercicio) {
		ctaDebe.codsubcuenta = util.sqlSelect("co_partidas p" + " INNER JOIN co_subcuentas s ON p.idsubcuenta = s.idsubcuenta" + " INNER JOIN co_cuentas c ON c.idcuenta = s.idcuenta", "s.codsubcuenta", "p.idasiento = " + idAsientoFactura + " AND c.idcuentaesp = 'PROVEE'", "co_partidas,co_subcuentas,co_cuentas");

		if (!ctaDebe.codsubcuenta) {
			MessageBox.warning(util.translate("scripts", "No se ha encontrado la subcuenta de proveedor del asiento contable correspondiente a la factura a pagar"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
			return false;
		}
	} else {
		var codProveedor:String = util.sqlSelect("recibosprov", "codproveedor", "idrecibo = " + curPD.valueBuffer("idrecibo"));
		if (codProveedor && codProveedor != "") {
			ctaDebe.codsubcuenta = util.sqlSelect("co_subcuentasprov", "codsubcuenta", "codproveedor = '" + codProveedor + "' AND codejercicio = '" + valoresDefecto.codejercicio + "'");
			if (!ctaDebe.codsubcuenta) {
				MessageBox.warning(util.translate("scripts", "El proveedor %1 no tiene definida ninguna subcuenta en el ejercicio %2.\nEspecifique la subcuenta en la pestaña de contabilidad del formulario de proveedores").arg(codProveedor).arg(valoresDefecto.codejercicio), MessageBox.Ok, MessageBox.NoButton);
				return false;
			}
		} else {
			ctaDebe = flfacturac.iface.pub_datosCtaEspecial("PROVEE", valoresDefecto.codejercicio);
			if (!ctaDebe.codsubcuenta) {
				MessageBox.warning(util.translate("scripts", "No tiene definida ninguna cuenta de tipo PROVEE.\nDebe crear este tipo especial y asociarlo a una cuenta\nen el módulo principal de contabilidad"), MessageBox.Ok, MessageBox.NoButton);
				return false;
			}
		}
	}

	ctaDebe.idsubcuenta = util.sqlSelect("co_subcuentas", "idsubcuenta", "codsubcuenta = '" + ctaDebe.codsubcuenta +  "' AND codejercicio = '" + valoresDefecto.codejercicio + "'");
	if (!ctaDebe.idsubcuenta) {
		MessageBox.warning(util.translate("scripts", "No existe la subcuenta ")  + ctaDebe.codsubcuenta + util.translate("scripts", " correspondiente al ejercicio ") + valoresDefecto.codejercicio + util.translate("scripts", ".\nPara poder realizar el pago debe crear antes esta subcuenta"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
		return false;
	}

	var debe:Number = 0;
	var debeME:Number = 0;
	var tasaconvDebe:Number = 1;

	if (valoresDefecto.coddivisa == recibo.coddivisa) {
		debe = parseFloat(recibo.importe);
		debeME = 0;
	} else {
		tasaconvDebe = util.sqlSelect("recibosprov r INNER JOIN facturasprov f ON r.idfactura = f.idfactura ", "tasaconv", "idrecibo = " + curPD.valueBuffer("idrecibo"), "recibosprov,facturasprov");
		debe = parseFloat(recibo.importeeuros);
		debeME = parseFloat(recibo.importe);
	}

	debe = util.roundFieldValue(debe, "co_partidas", "debe");
	debeME = util.roundFieldValue(debeME, "co_partidas", "debeme");


	var esAbono:Boolean = util.sqlSelect("recibosprov r INNER JOIN facturasprov f ON r.idfactura = f.idfactura", "deabono", "idrecibo = " + curPD.valueBuffer("idrecibo"), "recibosprov,facturasprov");

	var curPartida:FLSqlCursor = new FLSqlCursor("co_partidas");
	with(curPartida) {
		setModeAccess(curPartida.Insert);
		refreshBuffer();
		try {
			setValueBuffer("concepto", datosAsiento.concepto);
		} catch (e) {
			setValueBuffer("concepto", curPD.valueBuffer("tipo") + " recibo prov. " + recibo.codigo + " - " + recibo.nombreproveedor);
		}
		setValueBuffer("idsubcuenta", ctaDebe.idsubcuenta);
		setValueBuffer("codsubcuenta", ctaDebe.codsubcuenta);
		setValueBuffer("idasiento", datosAsiento.idasiento);
		if (esAbono) {
			setValueBuffer("debe", 0);
			setValueBuffer("haber", debe * -1);
		} else {
			setValueBuffer("debe", debe);
			setValueBuffer("haber", 0);
		}
		setValueBuffer("coddivisa", recibo.coddivisa);
		setValueBuffer("tasaconv", tasaconvDebe);
		setValueBuffer("debeME", debeME);
		setValueBuffer("haberME", 0);
	}
	if (!curPartida.commitBuffer())
		return false;

	return true;
}

function proveed_generarPartidasBancoProv(curPD:FLSqlCursor, valoresDefecto:Array, datosAsiento:Array, recibo:Array):Boolean
{
	var util:FLUtil = new FLUtil();
	var ctaHaber:Array = [];

	ctaHaber.codsubcuenta = curPD.valueBuffer("codsubcuenta");
	ctaHaber.idsubcuenta = util.sqlSelect("co_subcuentas", "idsubcuenta", "codsubcuenta = '" + ctaHaber.codsubcuenta + "' AND codejercicio = '" + valoresDefecto.codejercicio + "'");
	if (!ctaHaber.idsubcuenta) {
		MessageBox.warning(util.translate("scripts", "No tiene definida la subcuenta %1 en el ejercicio %2.\nAntes de dar el pago debe crear la subcuenta o modificar el ejercicio").arg(ctaHaber.codsubcuenta).arg(valoresDefecto.codejercicio), MessageBox.Ok, MessageBox.NoButton);
		return false;
	}

	var haber:Number = 0;
	var haberME:Number = 0;
	var tasaconvHaber:Number = 1;

	if (valoresDefecto.coddivisa == recibo.coddivisa) {
		haber = parseFloat(recibo.importe);
		haberMe = 0;
	} else {
		tasaconvHaber = curPD.valueBuffer("tasaconv");
		haber = parseFloat(recibo.importe) * parseFloat(tasaconvHaber);
		haberME = parseFloat(recibo.importe);
	}
	haber = util.roundFieldValue(haber, "co_partidas", "haber");
	haberME = util.roundFieldValue(haberME, "co_partidas", "haberme");

	var esAbono:Boolean = util.sqlSelect("recibosprov r INNER JOIN facturasprov f ON r.idfactura = f.idfactura", "deabono", "idrecibo = " + curPD.valueBuffer("idrecibo"), "recibosprov,facturasprov");

	var curPartida:FLSqlCursor = new FLSqlCursor("co_partidas");
	with(curPartida) {
		setModeAccess(curPartida.Insert);
		refreshBuffer();
		try {
			setValueBuffer("concepto", datosAsiento.concepto);
		} catch (e) {
			setValueBuffer("concepto", curPD.valueBuffer("tipo") + " recibo prov. " + recibo.codigo + " - " + recibo.nombreproveedor);
		}
		setValueBuffer("idsubcuenta", ctaHaber.idsubcuenta);
		setValueBuffer("codsubcuenta", ctaHaber.codsubcuenta);
		setValueBuffer("idasiento", datosAsiento.idasiento);
		if (esAbono) {
			setValueBuffer("debe", haber * -1);
			setValueBuffer("haber", 0);
		} else {
			setValueBuffer("debe", 0);
			setValueBuffer("haber", haber);
		}
		setValueBuffer("coddivisa", recibo.coddivisa);
		setValueBuffer("tasaconv", tasaconvHaber);
		setValueBuffer("debeME", 0);
		setValueBuffer("haberME", haberME);
	}
	if (!curPartida.commitBuffer())
		return false;

	return true;
}

/** \D Genera, si es necesario, la partida de diferecias positivas o negativas de cambio
@param	curPD: Cursor del pago o devolución
@param	valoresDefecto: Array de valores por defecto (ejercicio, divisa, etc.)
@param	datosAsiento: Array con los datos del asiento
@param	recibo: Array con los datos del recibo asociado al pago
@return	true si la generación es correcta, false en caso contrario
\end */
function proveed_generarPartidasCambioProv(curPD:FLSqlCursor, valoresDefecto:Array, datosAsiento:Array, recibo:Array):Boolean
{
	/** \C En el caso de que la divisa sea extranjera y la tasa de cambio haya variado desde el momento de la emisión de la factura, la diferencia se imputará a la correspondiente cuenta de diferencias de cambio.
	\end */
	if (valoresDefecto.coddivisa == recibo.coddivisa)
		return true;

	var util:FLUtil = new FLUtil();
	var debe:Number = 0;
	var haber:Number = 0;
	var tasaconvDebe:Number = 1;
	var tasaconvHaber:Number = 1;
	var diferenciaCambio:Number = 0;


	tasaconvHaber = curPD.valueBuffer("tasaconv");
	tasaconvDebe = util.sqlSelect("recibosprov r INNER JOIN facturasprov f ON r.idfactura = f.idfactura ", "tasaconv", "idrecibo = " + curPD.valueBuffer("idrecibo"), "recibosprov,facturasprov");
	haber = parseFloat(recibo.importe) * parseFloat(tasaconvHaber);
	haber = util.roundFieldValue(haber, "co_partidas", "haber");

	debe = parseFloat(recibo.importeeuros);
	debe = util.roundFieldValue(debe, "co_partidas", "debe");
	diferenciaCambio = debe - haber;
	if (util.buildNumber(diferenciaCambio, "f", 2) == "0.00" || util.buildNumber(diferenciaCambio, "f", 2) == "-0.00") {
		diferenciaCambio = 0;
		return true;
	}
	diferenciaCambio = util.roundFieldValue(diferenciaCambio, "co_partidas", "haber");

	var ctaDifCambio:Array = [];
	var debeDifCambio:Number = 0;
	var haberDifCambio:Number = 0;
	if (diferenciaCambio > 0) {
		ctaDifCambio = flfacturac.iface.pub_datosCtaEspecial("CAMPOS", valoresDefecto.codejercicio);
		if (ctaDifCambio.error != 0)
			return false;
		debeDifCambio = 0;
		haberDifCambio = diferenciaCambio;
	} else {
		ctaDifCambio = flfacturac.iface.pub_datosCtaEspecial("CAMNEG", valoresDefecto.codejercicio);
		if (ctaDifCambio.error != 0)
			return false;
		diferenciaCambio = 0 - diferenciaCambio;
		debeDifCambio = diferenciaCambio;
		haberDifCambio = 0;
	}

	/// Esto lo usan algunas extensiones
	if (curPD.valueBuffer("tipo") == "Devolución") {
		var aux:Number = debeDifCambio;
		debeDifCambio = haberDifCambio;
		haberDifCambio = aux;
	}

	var curPartida:FLSqlCursor = new FLSqlCursor("co_partidas");
	with(curPartida) {
		setModeAccess(curPartida.Insert);
		refreshBuffer();
		try {
			setValueBuffer("concepto", datosAsiento.concepto);
		} catch (e) {
			setValueBuffer("concepto", curPD.valueBuffer("tipo") + " recibo prov. " + recibo.codigo + " - " + recibo.nombreproveedor);
		}
		setValueBuffer("idsubcuenta", ctaDifCambio.idsubcuenta);
		setValueBuffer("codsubcuenta", ctaDifCambio.codsubcuenta);
		setValueBuffer("idasiento", datosAsiento.idasiento);
		setValueBuffer("debe", debeDifCambio);
		setValueBuffer("haber", haberDifCambio);
		setValueBuffer("coddivisa", valoresDefecto.coddivisa);
		setValueBuffer("tasaconv", 1);
		setValueBuffer("debeME", 0);
		setValueBuffer("haberME", 0);
	}
	if (!curPartida.commitBuffer())
		return false;

	return true;
}

/** \D Calcula la fecha de vencimiento de un recibo de proveedor, como la fecha de facturación más los días del plazo correspondiente
@param curFactura: Cursor posicionado en el registro de facturas correspondiente a la factura
@param numPlazo: Número del plazo actual
@param diasAplazado: Días de aplazamiento del pago
@return Fecha de vencimiento
\end */
function proveed_calcFechaVencimientoProv(curFactura:FLSqlCursor, numPlazo:Number, diasAplazado:Number):String
{
	var util:FLUtil = new FLUtil;
	return util.addDays(curFactura.valueBuffer("fecha"), diasAplazado);
}

/* \D Función para sobrecargar. Sirve para añadir al cursor del recibo los datos que añada la extensión
\end */
function proveed_datosReciboProv():Boolean
{
	return true;
}

/** \D Cambia la el estado del último pago anterior al especificado, de forma que se mantenga como único pago editable el último de todos
@param	idRecibo: Identificador del recibo al que pertenecen los pagos tratados
@param	idPagoDevol: Identificador del pago que ha cambiado
@param	unlock: Indicador de si el últim pago debe ser editable o no
@return	true si la verificación del estado es correcta, false en caso contrario
\end */
function proveed_cambiaUltimoPagoProv(idRecibo:String, idPagoDevol:String, unlock:Boolean):Boolean
{
	var curPagosDevol:FLSqlCursor = new FLSqlCursor("pagosdevolprov");
	curPagosDevol.select("idrecibo = " + idRecibo + " AND idpagodevol <> " + idPagoDevol + " ORDER BY fecha, idpagodevol");
	if (curPagosDevol.last())
		curPagosDevol.setUnLock("editable", unlock);

	return true;
}

/** \D Cambia la factura relacionada con un recibo a editable o no editable en función de si tiene pagos asociados o no
@param	idRecibo: Identificador de un recibo asociado a la factura
@param	idFactura: Identificador de la factura
@return	true si la verificación del estado es correcta, false en caso contrario
\end */
function proveed_calcularEstadoFacturaProv(idRecibo:String, idFactura:String):Boolean
{
	var util:FLUtil = new FLUtil();
	if (!idFactura)
		idFactura = util.sqlSelect("recibosprov", "idfactura", "idrecibo = " + idRecibo);

	var qryPagos:FLSqlQuery = new FLSqlQuery();
	qryPagos.setTablesList("recibosprov,pagosdevolprov");
	qryPagos.setSelect("p.idpagodevol");
	qryPagos.setFrom("recibosprov r INNER JOIN pagosdevolprov p ON r.idrecibo = p.idrecibo");
	qryPagos.setWhere("r.idfactura = " + idFactura);
	try { qryPagos.setForwardOnly( true ); } catch (e) {}
	if (!qryPagos.exec())
		return false;

	var curFactura:FLSqlCursor = new FLSqlCursor("facturasprov");
	curFactura.select("idfactura = " + idFactura);
	curFactura.first();
	if (qryPagos.size() == 0)
		curFactura.setUnLock("editable", true);
	else
		curFactura.setUnLock("editable", false);
	return true
}

/* \D Borra los recibos asociados a una factura.

@param idFactura: Identificador de la factura de la que provienen los recibos
@return False si hay error o si el recibo no se puede borrar, true si los recibos se borran correctamente
\end */
function proveed_borrarRecibosProv(idFactura:Number):Boolean
{
	var curRecibos = new FLSqlCursor("recibosprov");
	curRecibos.select("idfactura = " + idFactura);
	while (curRecibos.next()) {
		curRecibos.setModeAccess(curRecibos.Browse);
		curRecibos.refreshBuffer();
		if (this.iface.tienePagosDevProv(curRecibos.valueBuffer("idrecibo"))) {
			return false;
		}
	}
	curRecibos.select("idfactura = " + idFactura);
	while (curRecibos.next()) {
		curRecibos.setModeAccess(curRecibos.Del);
		curRecibos.refreshBuffer();
		if (!curRecibos.commitBuffer())
			return false;
	}
	return true;
}

/** Para sobrecargar en extensiones
*/
function proveed_codCuentaPagoProv(curFactura:FLSqlCursor):String
{
	return "";
}

function proveed_siGenerarRecibosProv(curFactura:FLSqlCursor, masCampos:Array):Boolean
{
 	var camposAcomprobar = new Array("codproveedor","total","codpago","fecha");

	for (var i:Number = 0; i < camposAcomprobar.length; i++)
		if (curFactura.valueBuffer(camposAcomprobar[i]) != curFactura.valueBufferCopy(camposAcomprobar[i]))
			return true;

	if (masCampos) {
		for (i = 0; i < masCampos.length; i++)
			if (curFactura.valueBuffer(masCampos[i]) != curFactura.valueBufferCopy(masCampos[i]))
				return true;
	}

	return false;
}

/** \D Obtiene los datos de la cuenta de domiciliación de un proveedor

@param codProveedor: Identificador del cliente
@return Array con los datos de la cuenta o false si no existe o hay un error. Los elementos de este array son:
	descripcion: Descripcion de la cuenta
	ctaentidad: Código de entidad bancaria
	ctaagencia: Código de oficina
	cuenta: Número de cuenta
	dc: Dígitos de control
	codcuenta: Código de la cuenta en la tabla de cuentas
	error: 0.Sin error 1.Datos no encontrados 2.Error
\end */
function proveed_obtenerDatosCuentaDomProv(codProveedor:String):Array
{
	var datosCuentaDom:Array = [];
	var util:FLUtil = new FLUtil;
	var domiciliarEn:String = util.sqlSelect("proveedores", "codcuentadom", "codproveedor= '" + codProveedor + "'");

	if (domiciliarEn != "") {
		datosCuentaDom = flfactppal.iface.pub_ejecutarQry("cuentasbcopro", "descripcion,ctaentidad,ctaagencia,cuenta,codcuenta", "codcuenta = '" + domiciliarEn + "'");
		switch (datosCuentaDom.result) {
		case -1:
			datosCuentaDom.error = 1;
			break;
		case 0:
			datosCuentaDom.error = 2;
			break;
		case 1:
			datosCuentaDom.dc = util.calcularDC(datosCuentaDom.ctaentidad + datosCuentaDom.ctaagencia) + util.calcularDC(datosCuentaDom.cuenta);
			datosCuentaDom.error = 0;
			break;
		}
	} else {
		datosCuentaDom.error = 1;
	}

	return datosCuentaDom;
}

//// PROVEED ////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////

/** @class_definition diasPagoProv */
/////////////////////////////////////////////////////////////////
//// DIAS_PAGO_PROV /////////////////////////////////////////////
/* \D Calcula la fecha de vencimiento de un recibo en base a los días de pago y vacaciones del proveedor
@param curFactura: Cursor posicionado en el registro de facturas correspondiente a la factura
@param numPlazo: Número del plazo actual
@param diasAplazado: Días de aplazamiento del pago
@return Fecha de vencimiento
\end */
function diasPagoProv_calcFechaVencimientoProv(curFactura:FLSqlCursor, numPlazo:Number, diasAplazado:Number):String
{
	var util:FLUtil = new FLUtil;
	var fechaFactura:String = curFactura.valueBuffer("fecha")
	var f:String = this.iface.__calcFechaVencimientoProv(curFactura, numPlazo, diasAplazado);

	var codProveedor:String = curFactura.valueBuffer("codproveedor");
	if (!codProveedor || codProveedor == "")
		return f;

	var diasPago:Array;
	var cadenaDiasPago:String = util.sqlSelect("proveedores", "diaspago", "codproveedor = '" + codProveedor + "'");
	if (!cadenaDiasPago || cadenaDiasPago == "")
		diasPago = "";
	else
		diasPago = cadenaDiasPago.split(",");

	var buscarDia:String = util.sqlSelect("proveedores", "buscardia", "codproveedor = '" + codProveedor + "'");
	if (buscarDia == "Posterior")
		fechaVencimiento = this.iface.procesarDiasPagoProv(f, diasPago);
	else {
		fechaVencimiento = this.iface.procesarDiasPagoProvAnt(f, diasPago);
		if (util.daysTo(fechaVencimiento, fechaFactura) > 0)
			fechaVencimiento = this.iface.procesarDiasPagoProv(f, diasPago);
	}

	return fechaVencimiento;
}

/** \D Modifica la fecha de vencimiento en función del día de pago al proveedor, buscando el siguiente día de pago
@param	fechaV: String con la fecha de vencimiento actual
@param	diasPago: Array con los días de pago para cada plazo
@return	Fecha de vencimiento modificada
\end */
function diasPagoProv_procesarDiasPagoProv(fechaV:String, diasPago:Array):String
{
	var util:FLUtil = new FLUtil;
	var fechaVencimiento:Date = new Date (Date.parse(fechaV.toString()));

	if (diasPago == "" || !diasPago)
		return fechaV;
	var diaFV:Number = parseFloat(fechaVencimiento.getDate());

	var i:Number = 0;
	var distancia:Number;
	var diaPago:Number;
	for (i = 0; i < diasPago.length && parseFloat(diasPago[i]) < diaFV; i++);

	if (i < diasPago.length) {
		diaPago = diasPago[i];
	} else {
		var aux = util.addMonths(fechaVencimiento.toString(), 1);
		fechaVencimiento = new Date(Date.parse(aux.toString()));
		diaPago = diasPago[0];
	}

	// Control de fechas inexistentes (30 de febrero, 31 de abril, etc)
	var fechaVencimientoBk:String = fechaVencimiento.toString();

	var paso:Number = 0;
	fechaVencimiento.setDate(diaPago);
	while (!fechaVencimiento) {
		fechaVencimiento = new Date(Date.parse(fechaVencimientoBk));
		fechaVencimiento.setDate(--diaPago);
		if (paso++ == 10) {
			MessageBox.warning(util.translate("scripts", "Hubo un problema al establecer el día de pago"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
			return false;
		}
	}

	return fechaVencimiento.toString();
}

/** \D Modifica la fecha de vencimiento en función del día de pago del proveedor, buscando el anterior día de pago
@param	fechaV: String con la fecha de vencimiento actual
@param	diasPago: Array con los días de pago para cada plazo
@return	Fecha de vencimiento modificada
\end */
function diasPagoProv_procesarDiasPagoProvAnt(fechaV:String, diasPago:Array):String
{
	var util:FLUtil = new FLUtil;
	var fechaVencimiento:Date = new Date (Date.parse(fechaV.toString()));
	if (diasPago == "" || !diasPago)
		return fechaV;
	var diaFV:Number = parseFloat(fechaVencimiento.getDate());
	var i:Number = 0;
	var distancia:Number;
	for (i = (diasPago.length - 1); i >= 0 && parseFloat(diasPago[i]) > diaFV; i--);
	if (i >= 0 ) {
		fechaVencimiento.setDate(diasPago[i]);
	} else {
		var aux = util.addMonths(fechaVencimiento.toString(), -1);
		fechaVencimiento = new Date(Date.parse(aux.toString()));
		fechaVencimiento.setDate(diasPago[(diasPago.length - 1)]);
	}

	return fechaVencimiento.toString();
}
//// DIAS_PAGO_PROV /////////////////////////////////////////////
////////////////////////////////////////////////////////////////

/** @class_definition remesaProv */
/////////////////////////////////////////////////////////////////
//// REMESAS DE RECIBOS DE PROVEEDOR ////////////////////////////
function remesaProv_beforeCommit_remesasprov(curRemesa:FLSqlCursor):Boolean
{

	switch (curRemesa.modeAccess()) {
		/** \C La remesa puede borrarse si todos los pagos asociados pueden ser excluidos
		\end */
		case curRemesa.Del: {
			var idRemesa:Number = curRemesa.valueBuffer("idremesa");
			var qryRecibos:FLSqlQuery = new FLSqlQuery;
			qryRecibos.setTablesList("pagosdevolprov");
			qryRecibos.setSelect("DISTINCT(idrecibo)");
			qryRecibos.setFrom("pagosdevolprov");
			qryRecibos.setWhere("idremesa = " + idRemesa);
			if (!qryRecibos.exec())
				return false;
			while (qryRecibos.next()) {
				if (!formRecordremesasprov.iface.pub_excluirReciboRemesa(qryRecibos.value(0), idRemesa))
					return false;
			}
		}
	}
	return true;
}
/**
@param	curPR: Cursor del pago de la remesa de proveedor
@param	idAsiento: Id del asiento asociado
@param	valoresDefecto: Array con los valores por defecto de ejercicio y divisa
@return	VERDADERO si no hay error, FALSO en otro caso
\end */
function remesaProv_generarPartidasEFCOGP(curPR:FLSqlCursor, valoresDefecto:Array, datosAsiento:Array, remesa:Array):Boolean
{
	var util:FLUtil = new FLUtil();

	var haber:Number = 0;
	var haberME:Number = 0;
	var ctaHaber:Array = [];
	ctaHaber.codsubcuenta = util.sqlSelect("cuentasbanco","codsubcuentaecgp","codcuenta = '" + remesa.codcuenta + "'");

	if (!ctaHaber.codsubcuenta || ctaHaber.codsubcuenta == "") {
		MessageBox.warning(util.translate("scripts", "No tiene definida de efectos comerciales de gestión de pago para la cuenta %1").arg(remesa.codcuenta), MessageBox.Ok, MessageBox.NoButton);
		return false;
	}

	ctaHaber.idsubcuenta = util.sqlSelect("co_subcuentas", "idsubcuenta", "codsubcuenta = '" + ctaHaber.codsubcuenta + "' AND codejercicio = '" + valoresDefecto.codejercicio + "'");
	if (!ctaHaber.idsubcuenta) {
		MessageBox.warning(util.translate("scripts", "No tiene definida la subcuenta %1 en el ejercicio %2.\nAntes de dar el pago debe crear la subcuenta o modificar el ejercicio").arg(ctaDebe.codsubcuenta).arg(valoresDefecto.codejercicio), MessageBox.Ok, MessageBox.NoButton);
		return false;
	}

	debe = remesa.total;
	debeME = 0;
	debe = util.roundFieldValue(debe, "co_partidas", "debe");
	debeME = util.roundFieldValue(debeME, "co_partidas", "debeme");

	var curPartida:FLSqlCursor = new FLSqlCursor("co_partidas");
	with (curPartida) {
		setModeAccess(curPartida.Insert);
		refreshBuffer();
		setValueBuffer("concepto", curPR.valueBuffer("tipo") + " " + util.translate("scripts", "remesa") + " " + remesa.idremesa);
		setValueBuffer("idsubcuenta", ctaHaber.idsubcuenta);
		setValueBuffer("codsubcuenta", ctaHaber.codsubcuenta);
		setValueBuffer("idasiento", datosAsiento.idasiento);
		setValueBuffer("debe", debe);
		setValueBuffer("haber", 0);
		setValueBuffer("debeME", debeME);
		setValueBuffer("haberME", 0);
	}

	if (!curPartida.commitBuffer())
		return false;

	return true;
}

/** \Genera o regenera el asiento contable asociado a un pago de una remesa de proveedor
@param	curPR: Cursor posicionado en el pago cuyo asiento se va a regenerar
@return	true si la regeneración se realiza correctamente, false en caso contrario
\end */
function remesaProv_generarAsientoPagoRemesaProv(curPR:FLSqlCursor):Boolean
{
	var util:FLUtil = new FLUtil();
	if (curPR.modeAccess() != curPR.Insert && curPR.modeAccess() != curPR.Edit)
		return true;

	if (curPR.valueBuffer("nogenerarasiento")) {
		curPR.setNull("idasiento");
		return true;
	}
	var codEjercicio:String = flfactppal.iface.pub_ejercicioActual();
	var datosDoc:Array = flfacturac.iface.pub_datosDocFacturacion(curPR.valueBuffer("fecha"), codEjercicio, "pagosdevolremprov");
	if (!datosDoc.ok)
		return false;
	if (datosDoc.modificaciones == true) {
		codEjercicio = datosDoc.codEjercicio;
		curPR.setValueBuffer("fecha", datosDoc.fecha);
	}

	var datosAsiento:Array = [];
	var valoresDefecto:Array;
	valoresDefecto["codejercicio"] = codEjercicio;
	valoresDefecto["coddivisa"] = util.sqlSelect("empresa", "coddivisa", "1 = 1");

	datosAsiento = flfacturac.iface.pub_regenerarAsiento(curPR, valoresDefecto);
	if (datosAsiento.error == true)
		return false;

	var remesa:Array = flfactppal.iface.pub_ejecutarQry("remesasprov", "coddivisa,total,fecha,idremesa,codsubcuenta,codcuenta", "idremesa = " + curPR.valueBuffer("idremesa"));
		if (remesa.result != 1)
			return false;

	if (curPR.valueBuffer("tipo") == "Pago") {
		if (!this.iface.generarPartidasEFCOGP(curPR, valoresDefecto, datosAsiento, remesa))
			return false;

		if (!this.iface.generarPartidasBancoRemProv(curPR, valoresDefecto, datosAsiento, remesa))
			return false;
	}
	curPR.setValueBuffer("idasiento", datosAsiento.idasiento);
	if (!flcontppal.iface.pub_comprobarAsiento(datosAsiento.idasiento))
		return false;

	return true;
}

/** \D Genera la partida correspondiente al banco o a caja del asiento de pago de la remesa de proveedor
@param	curPR: Cursor del pago de la remesa de proveedor
@param	valoresDefecto: Array de valores por defecto (ejercicio, divisa, etc.)
@param	datosAsiento: Array con los datos del asiento
@param	recibo: Array con los datos del recibo de proveedor asociado al pago de la remesa
@return	true si la generación es correcta, false en caso contrario
\end */
function remesaProv_generarPartidasBancoRemProv(curPR:FLSqlCursor, valoresDefecto:Array, datosAsiento:Array, remesa:Array):Boolean
{
	var util:FLUtil = new FLUtil();
	var ctaHaber:Array = [];
	ctaHaber.codsubcuenta = util.sqlSelect("cuentasbanco", "codsubcuenta", "codcuenta = '" + remesa.codcuenta + "'");
	ctaHaber.idsubcuenta = util.sqlSelect("co_subcuentas", "idsubcuenta", "codsubcuenta = '" + ctaHaber.codsubcuenta + "' AND codejercicio = '" + valoresDefecto.codejercicio + "'");
	if (!ctaHaber.idsubcuenta) {
		MessageBox.warning(util.translate("scripts", "No tiene definida la subcuenta %1 en el ejercicio %2.\nAntes de dar el pago debe crear la subcuenta o modificar el ejercicio").arg(ctaHaber.codsubcuenta).arg(valoresDefecto.codejercicio), MessageBox.Ok, MessageBox.NoButton);
		return false;
	}

	var haber:Number = 0;
	var haberME:Number = 0;
	var tasaconvHaber:Number = 1;
	if (valoresDefecto.coddivisa == remesa.coddivisa) {
		haber = parseFloat(remesa.total);
		haberME = 0;
	} else {
		tasaconvHaber = curPR.valueBuffer("tasaconv");
		haber = parseFloat(remesa.total) * parseFloat(tasaconvHaber);
		haberME = parseFloat(remesa.total);
	}
	haber = util.roundFieldValue(haber, "co_partidas", "haber");
	haberME = util.roundFieldValue(haberME, "co_partidas", "haberme");

	var curPartida:FLSqlCursor = new FLSqlCursor("co_partidas");
	with(curPartida) {
		setModeAccess(curPartida.Insert);
		refreshBuffer();
		setValueBuffer("concepto", curPR.valueBuffer("tipo") + " " + util.translate("scripts", "remesa") + " " + remesa.idremesa);
		setValueBuffer("idsubcuenta", ctaHaber.idsubcuenta);
		setValueBuffer("codsubcuenta", ctaHaber.codsubcuenta);
		setValueBuffer("idasiento", datosAsiento.idasiento);
		setValueBuffer("debe", 0);
		setValueBuffer("haber", haber);
		setValueBuffer("coddivisa", remesa.coddivisa);
		setValueBuffer("tasaconv", tasaconvHaber);
		setValueBuffer("debeME", 0);
		setValueBuffer("haberME", haberME);
	}
	if (!curPartida.commitBuffer())
		return false;

	return true;
}

/** \C Se regenera, si es posible, el asiento contable asociado al pago de una remesa de proveedor
\end */
function remesaProv_beforeCommit_pagosdevolremprov(curPR:FLSqlCursor):Boolean
{
	var util:FLUtil = new FLUtil();
	if (sys.isLoadedModule("flcontppal") && flfactppal.iface.pub_valorDefectoEmpresa("contintegrada") && !curPR.valueBuffer("nogenerarasiento")) {
		if (!this.iface.generarAsientoPagoRemesaProv(curPR))
			return false;
	}

	return true;
}

/** \C Se elimina, si es posible, el asiento contable asociado al pago o devolución
\end */
function remesaProv_afterCommit_pagosdevolremprov(curPD:FLSqlCursor):Boolean
{
	var util:FLUtil = new FLUtil();
	if (sys.isLoadedModule("flcontppal") == false || util.sqlSelect("empresa", "contintegrada", "1 = 1") == false)
		return true;

	switch (curPD.modeAccess()) {
		case curPD.Del: {
			if (curPD.isNull("idasiento"))
				return true;

			var idAsiento:Number = curPD.valueBuffer("idasiento");
			if (flfacturac.iface.pub_asientoBorrable(idAsiento) == false)
				return false;

			var curAsiento:FLSqlCursor = new FLSqlCursor("co_asientos");
			curAsiento.select("idasiento = " + idAsiento);
			if (curAsiento.first()) {
				curAsiento.setUnLock("editable", true);
				curAsiento.setModeAccess(curAsiento.Del);
				curAsiento.refreshBuffer();
				if (!curAsiento.commitBuffer())
					return false;
			}
			break;
		}
		case curPD.Edit: {
			if (curPD.valueBuffer("nogenerarasiento")) {
				var idAsientoAnterior:String = curPD.valueBufferCopy("idasiento");
				if (idAsientoAnterior && idAsientoAnterior != "") {
					if (!flfacturac.iface.pub_eliminarAsiento(idAsientoAnterior))
						return false;
				}
			}
			break;
		}
	}

	return true;
}
//// REMESAS DE RECIBOS DE PROVEEDOR ////////////////////////////
////////////////////////////////////////////////////////////////

/** @class_definition modelo340 */
/////////////////////////////////////////////////////////////////
//// MODELO 340 /////////////////////////////////////////////////
function modelo340_beforeCommit_pagosdevolprov(curPD)
{
  var _i = this.iface;
  if (!_i.__beforeCommit_pagosdevolprov(curPD)) {
    return false;
  }
  if (curPD.modeAccess() == curPD.Insert || curPD.modeAccess() == curPD.Edit) {
    var idRecibo = curPD.valueBuffer("idrecibo");
    var qRecibos = new AQSqlQuery;
    qRecibos.setSelect("codproveedor, codpago");
    qRecibos.setFrom("recibosprov");
    qRecibos.setWhere("idRecibo = " + idRecibo);
    if (!qRecibos.exec()) {
      return;
    }
    if (!qRecibos.first()) {
      return false;
    }
    var codProveedor = qRecibos.value("codproveedor");
    var codPago = qRecibos.value("codpago");
    var criterioCaja = AQUtil.sqlSelect("proveedores", "criteriocaja", "codproveedor = '" + codProveedor + "' ");
    if (codPago && codPago != "" && criterioCaja) {
      var medioPago340 = AQUtil.sqlSelect("formaspago", "mediopago340", "codpago='" + codPago + "' ");
      switch (medioPago340) {
        case "C" : {
          var iban = curPD.valueBuffer("iban");
          if (!iban || iban == "") {
            MessageBox.warning(util.translate("El proveedor está acogido al régimen especial de criterio de caja.\nSegún el medio de pago de la factura debe de informar la cuenta bancaria"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
            return false;
          }
          break;
        }
        case "T" : {
          var numeroCheque = curPD.valueBuffer("numerocheque");
          if (!numeroCheque || numeroCheque == "") {
            MessageBox.warning(util.translate("El proveedor está acogido al régimen especial de criterio de caja.\nSegún el medio de pago de la factura debe de informar el número de cheque"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
            return false;
          }
          break;
        }
        case "O" : {
          var descripcion = curPD.valueBuffer("numerocheque");
          if (!descripcion || descripcion == "") {
            MessageBox.warning(util.translate("El proveedor está acogido al régimen especial de criterio de caja.\nSegún el medio de pago de la factura debe de informar la descripción o identificación de cualquier otro medio utilizado"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
            return false;
          }
          break;
        }
      }
    }
  }
  return true;
}

function modelo340_afterCommit_pagosdevolprov(curPD)
{
  var _i = this.iface;

  if (!_i.__afterCommit_pagosdevolprov(curPD)) {
    return false;
  }
  var idRecibo = curPD.valueBuffer("idrecibo");
  switch (curPD.modeAccess()) {
    case curPD.Insert: {
      if (!_i.marcarPrimerPago(idRecibo)) {
        return false;
      }
      break;
    }
  }
  return true;
}
function modelo340_marcarPrimerPago(idRecibo)
{
  var _i = this.iface;
  var numPagos = AQUtil.sqlSelect("pagosdevolprov", "count(*)", "idrecibo = " + idRecibo);
  debug("Numpagos: " + numPagos);
  if (numPagos && numPagos == 1) {
    var curPagosDevol = new FLSqlCursor("pagosdevolprov");
    curPagosDevol.select("idrecibo = " + idRecibo);
    if (!curPagosDevol.first()) {
      return false;
    }
    curPagosDevol.setModeAccess(curPagosDevol.Edit);
    curPagosDevol.refreshBuffer();
    curPagosDevol.setValueBuffer("primerpago", true);
    if (!curPagosDevol.commitBuffer()) {
      return false;
    }
  }

  return true;
}
//// MODELO 340 /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////

//// DESARROLLO /////////////////////////////////////////////////
////////////////////////////////////////////////////

