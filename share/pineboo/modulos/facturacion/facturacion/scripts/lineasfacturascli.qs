/***************************************************************************
                 lineasfacturascli.qs  -  description
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
	function calculateField(fN:String):String { return this.ctx.interna_calculateField(fN); }
	function validateForm():Boolean { return this.ctx.interna_validateForm(); }
}
//// INTERNA /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
class oficial extends interna {
    function oficial( context ) { interna( context ); }
	function desconectar() {
		return this.ctx.oficial_desconectar();
	}
	function bufferChanged(fN:String) {
		return this.ctx.oficial_bufferChanged(fN);
	}
	function dameFiltroReferencia():String {
		return this.ctx.oficial_dameFiltroReferencia();
	}
}
//// OFICIAL /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration ctaVentasArt */
//////////////////////////////////////////////////////////////////
//// CTA_VENTAS_ART //////////////////////////////////////////////
class ctaVentasArt extends oficial /** %from: oficial */ {

	var longSubcuenta:Number;
	var bloqueoSubcuenta:Boolean;
	var ejercicioActual:String;
	var posActualPuntoSubcuenta:Number;

	function ctaVentasArt( context ) { oficial( context ); }
	function init() {
		this.ctx.ctaVentasArt_init();
	}
	function bufferChanged(fN:String) {
		return this.ctx.ctaVentasArt_bufferChanged(fN);
	}
	function calculateField(fN:String) {
		return this.ctx.ctaVentasArt_calculateField(fN);
	}
}
//// CTA_VENTAS_ART //////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////
class head extends ctaVentasArt {
    function head( context ) { ctaVentasArt ( context ); }
}
//// DESARROLLO /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration ifaceCtx */
/////////////////////////////////////////////////////////////////
//// INTERFACE  /////////////////////////////////////////////////
class ifaceCtx extends head {
    function ifaceCtx( context ) { head( context ); }
}

const iface = new ifaceCtx( this );
//// INTERFACE  /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition interna */
////////////////////////////////////////////////////////////////////////////
//// DEFINICION ////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////
//// INTERNA /////////////////////////////////////////////////////
/** \C
Este formulario realiza la gestión de las líneas de facturas a clientes.
\end */
function interna_init()
{
	var util:FLUtil = new FLUtil();
	var cursor:FLSqlCursor = this.cursor();
	connect(this.cursor(), "bufferChanged(QString)", this, "iface.bufferChanged");
	connect(form, "closed()", this, "iface.desconectar");

	var irpf:Number = util.sqlSelect("series", "irpf", "codserie = '" + cursor.cursorRelation().valueBuffer("codserie") + "'");
	if (!irpf) {
		irpf = 0;
	}

	if (cursor.cursorRelation().valueBuffer("porcomision")) {
		this.child("fdbPorComision").setDisabled(true);
	}

	this.child("lblComision").setText(this.iface.calculateField("lblComision"));
	this.child("lblDtoPor").setText(this.iface.calculateField("lbldtopor"));

	if (cursor.modeAccess() == cursor.Insert) {
		var opcionIvaRec:Number = flfacturac.iface.pub_tieneIvaDocCliente(cursor.cursorRelation().valueBuffer("codserie"), cursor.cursorRelation().valueBuffer("codcliente"));
		switch (opcionIvaRec) {
			case 0: {
				this.child("fdbCodImpuesto").setValue("");
				this.child("fdbIva").setValue(0);
			}
			case 1: {
				this.child("fdbRecargo").setValue(0);
				break;
			}
		}

		this.child("fdbIRPF").setValue(irpf);
		this.child("fdbDtoPor").setValue(this.iface.calculateField("dtopor"));
		if (cursor.cursorRelation().valueBuffer("porcomision")) {
			this.child("fdbPorComision").setDisabled(true);
		} else {
			if (!cursor.cursorRelation().valueBuffer("codagente") || cursor.cursorRelation().valueBuffer("codagente") == "") {
				this.child("fdbPorComision").setDisabled(true);
			} else {
				this.child("fdbPorComision").setValue(this.iface.calculateField("porcomision"));
			}
		}
	}

	var filtroReferencia:String = this.iface.dameFiltroReferencia();
	this.child("fdbReferencia").setFilter(filtroReferencia);
}

/** \C
Los campos calculados de este formulario son los mismos que los del formulario de líneas de pedido a cliente
\end */
function interna_calculateField(fN:String):String
{
		return formRecordlineaspedidoscli.iface.pub_commonCalculateField(fN, this.cursor());
}

function interna_validateForm():Boolean
{

	var util:FLUtil = new FLUtil();
	var cursor:FLSqlCursor = this.cursor();
	var curFactura:FLSqlCursor = cursor.cursorRelation();

	if (curFactura.valueBuffer("deabono") == true && cursor.valueBuffer("pvptotal") > 0) {
		var res:Number = MessageBox.warning(util.translate("scripts","Si esta creando una factura de abono la cantidad total debe ser negativa.\n\n¿Desea continuar?"), MessageBox.No, MessageBox.Yes, MessageBox.NoButton);
		if (res == MessageBox.No)
			return false;
	}
	if (curFactura.valueBuffer("deabono") == false && cursor.valueBuffer("pvptotal") < 0) {
		var res:Number = MessageBox.warning(util.translate("scripts","Si esta creando una factura que no es de abono la cantidad total debe ser positiva.\n\n¿Desea continuar?"), MessageBox.No, MessageBox.Yes, MessageBox.NoButton);
		if (res == MessageBox.No)
			return false;
	}
	return true;

}

//// INTERNA /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
function oficial_desconectar()
{
		disconnect(this.cursor(), "bufferChanged(QString)", this, "iface.bufferChanged");
}

/** \C
Las dependencias entre controles de este formulario son las mismas que las del formulario de líneas de pedido a cliente
\end */
function oficial_bufferChanged(fN:String)
{
		formRecordlineaspedidoscli.iface.pub_commonBufferChanged(fN, form);
}

function oficial_dameFiltroReferencia():String
{
	return "sevende";
}
//// OFICIAL /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition ctaVentasArt */
/////////////////////////////////////////////////////////////////
//// CTA_VENTAS_ART //////////////////////////////////////////////

function ctaVentasArt_init()
{
	this.iface.__init();

	var cursor:FLSqlCursor = this.cursor();
	var util:FLUtil = new FLUtil;

	if (sys.isLoadedModule("flcontppal")) {
		this.iface.ejercicioActual = flfactppal.iface.pub_ejercicioActual();
		this.iface.longSubcuenta = util.sqlSelect("ejercicios", "longsubcuenta",
				"codejercicio = '" + this.iface.ejercicioActual + "'");
		this.iface.bloqueoSubcuenta = false;
		this.iface.posActualPuntoSubcuenta = -1;
		this.child("fdbIdSubcuenta").setFilter("codejercicio = '" + this.iface.ejercicioActual + "'");
	} else
		this.child("gbxContabilidad").enabled = false;
}


function ctaVentasArt_bufferChanged(fN:String)
{
	var cursor:FLSqlCursor = this.cursor();
	var util:FLUtil = new FLUtil();

	switch(fN) {
		case "codsubcuenta":
			if (!this.iface.bloqueoSubcuenta) {
				this.iface.bloqueoSubcuenta = true;
				this.iface.posActualPuntoSubcuenta = flcontppal.iface.pub_formatearCodSubcta(this, "fdbCodSubcuenta", this.iface.longSubcuenta, this.iface.posActualPuntoSubcuenta);
				this.iface.bloqueoSubcuenta = false;
			}
			break;
		case "referencia":
			this.iface.bloqueoSubcuenta = true;
			this.child("fdbCodSubcuenta").setValue(this.iface.calculateField("codsubcuenta"));
			this.iface.bloqueoSubcuenta = false;
			this.child("fdbIdSubcuenta").setValue(this.iface.calculateField("idsubcuenta"));
			var serie:String = cursor.cursorRelation().valueBuffer("codserie");
			var sinIva:Boolean = util.sqlSelect("series","siniva","codserie = '" + serie + "'");
			if(sinIva == false)
				this.child("fdbCodImpuesto").setValue(this.iface.calculateField("codimpuesto", cursor));
		default:
			this.iface.__bufferChanged(fN);
	}
}

function ctaVentasArt_calculateField(fN:String):String
{
	var util:FLUtil = new FLUtil();
	var cursor:FLSqlCursor = this.cursor();
	var valor:String;
	switch(fN) {
		case "codsubcuenta": {
			var referencia:String = cursor.valueBuffer("referencia");
			if(!referencia || referencia == "")
				valor = "";
			else
				valor = util.sqlSelect("articulos", "codsubcuentaven", "referencia = '" + referencia + "'");
			break
		}
		case "idsubcuenta": {
			var idFactura:Number = cursor.valueBuffer("idfactura");
			if(!idFactura) {
				valor = "";
				break;
			}
			var codEjercicio:String = util.sqlSelect("facturascli","codejercicio","idfactura = " + idFactura);
			if(!codEjercicio || codEjercicio == "") {
				valor = "";
				break;
			}
			var codSubcuenta:String = cursor.valueBuffer("codsubcuenta");
			if(!codSubcuenta || codSubcuenta == "") {
				valor = "";
				break;
			}
			var idsubcuenta:Number = util.sqlSelect("co_subcuentas", "idsubcuenta", "codsubcuenta = '" + codSubcuenta + "' AND codejercicio = '" + codEjercicio + "'");

			if (!idsubcuenta)
				valor = "";
// 				MessageBox.warning(util.translate("scripts", "No existe la subcuenta ")  + cursor.valueBuffer("codsubcuenta") + util.translate("scripts", " correspondiente al ejercicio ") + codEjercicio + util.translate("scripts", ".\nPara poder crear la factura debe crear antes esta subcuenta"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
			else
				valor = idsubcuenta;
			break;
		}
		default:
			valor = this.iface.__calculateField(fN);
	}

	return valor;
}

//// CTA_VENTAS_ART //////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////

//// DESARROLLO /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

