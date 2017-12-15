/**************************************************************************
                 co_masterfacturacionprov347.qs  -  description
                             -------------------
    begin                : jue feb 05 2009
    copyright            : (C) 2009 by InfoSiAL S.L.
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
    function init() { 
		return this.ctx.interna_init(); 
	}
}
//// INTERNA /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
class oficial extends interna {
    function oficial( context ) { interna( context ); } 
	function calcularTotal() {
		return this.ctx.oficial_calcularTotal();
	}
}
//// OFICIAL /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration boe2011 */
//////////////////////////////////////////////////////////////////
//// BOE2011 ////////////////////////////////////////////////////
class boe2011 extends oficial {
    function boe2011( context ) { oficial( context ); } 
    function init() {
        return this.ctx.boe2011_init(); 
    }
    function filtroTrimestre(trimestre:String):String {
        return this.ctx.boe2011_filtroTrimestre(trimestre);
    }
    function calcularTotal() {
        return this.ctx.boe2011_calcularTotal();
    }
    function calcularTotalTrimestre(trimestre:String) {
        return this.ctx.boe2011_calcularTotalTrimestre(trimestre);
    }
    function detalleMetalico(){
        return this.ctx.boe2011_detalleMetalico();
    }
}
//// BOE2011 /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////
class head extends boe2011 {
    function head( context ) { boe2011 ( context ); }
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
function interna_init()
{
	this.iface.calcularTotal();
}
//// INTERNA /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
function oficial_calcularTotal()
{
	var util:FLUtil = new FLUtil;
	var cursor:FLSqlCursor = this.cursor();
	var total:Number = parseFloat(util.sqlSelect("facturasprov", "SUM(total)", "cifnif = '" + cursor.valueBuffer("cifnif") + "' AND codejercicio = '" + cursor.valueBuffer("codejercicio") + "' AND codserie = '" + cursor.valueBuffer("codserie") + "'"));
		if (!total || isNaN(total)) {
			total = 0;
		}
	this.child("lblTotal").text = util.translate("scripts", "TOTAL: %1").arg(util.roundFieldValue(total, "facturasprov", "total"));
}
//// OFICIAL /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition boe2011 */
//////////////////////////////////////////////////////////////////
//// BOE2011 ////////////////////////////////////////////////////
function boe2011_init()
{
    
    var cursor:FLSqlCursor = this.cursor();
    var clave:String = "A";
    var cifnif:String = cursor.valueBuffer("cifnif");
    var inFacturas1T: String = formRecordco_modelo347.iface.dameIdsFacturas(clave,cifnif,"1T");
    var inFacturas2T: String = formRecordco_modelo347.iface.dameIdsFacturas(clave,cifnif,"2T");
    var inFacturas3T: String = formRecordco_modelo347.iface.dameIdsFacturas(clave,cifnif,"3T");
    var inFacturas4T: String = formRecordco_modelo347.iface.dameIdsFacturas(clave,cifnif,"4T");
    
    this.child("tableDBRecords1T").setFilter("idfactura IN("+inFacturas1T+")");
    this.child("tableDBRecords1T").refresh();
    this.child("tableDBRecords2T").setFilter("idfactura IN("+inFacturas2T+")");
    this.child("tableDBRecords2T").refresh();
    this.child("tableDBRecords3T").setFilter("idfactura IN("+inFacturas3T+")");
    this.child("tableDBRecords3T").refresh();
    this.child("tableDBRecords4T").setFilter("idfactura IN("+inFacturas4T+")");
    this.child("tableDBRecords4T").refresh();
    
    
    this.iface.calcularTotal();
    this.iface.detalleMetalico();
    
}

function boe2011_calcularTotal()
{
    this.iface.__calcularTotal();
    
    this.iface.calcularTotalTrimestre("1T");
    this.iface.calcularTotalTrimestre("2T");
    this.iface.calcularTotalTrimestre("3T");
    this.iface.calcularTotalTrimestre("4T");
    
}

function boe2011_calcularTotalTrimestre(trimestre:String) {
    
    var filtro = this.child("tableDBRecords"+trimestre).filter();
 
    var util:FLUtil = new FLUtil;
    var totalT:Number = parseFloat(util.sqlSelect("facturasprov", "SUM(total)", filtro));
    if (!totalT || isNaN(totalT)) {
        totalT = 0;
    }
    
    var nombreEtiqueta:String = "lblTotal"+trimestre;
    
    this.child(nombreEtiqueta).text = util.translate("scripts", "TOTAL: %1").arg(util.roundFieldValue(totalT, "facturasprov", "total"));
}

function boe2011_detalleMetalico() 
{
    var util:FLUtil = new FLUtil;
    
    this.child("gbxRecibosCli").setHidden(true);
    this.child("gbxRecibosProv").setHidden(false);
    var recibos:String = formRecordco_modelo347.iface.inRecibos;
    this.child("tdbRecibosProv").cursor().setMainFilter("idrecibo IN ("+recibos+")");

    var total:Number = parseFloat(util.sqlSelect("recibosprov", "SUM(importeeuros)", "idrecibo IN("+recibos+")"));
    if (!total || isNaN(total)) {
        total = 0;
    }
    
    this.child("lblMetalicoProv").text = util.translate("scripts", "TOTAL: %1").arg(util.roundFieldValue(total, "recibosprov", "importeeuros"));
}
//// BOE2011 ////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////


/** @class_definition head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////

//// DESARROLLO /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
