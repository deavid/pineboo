/***************************************************************************
                 co_datos347.qs  -  description
                             -------------------
    begin                : mie jun 1 2005
    copyright            : (C) 2005 by InfoSiAL S.L.
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
	function calculateField(fN:String):String {
		return this.ctx.interna_calculateField(fN);
	}
}
//// INTERNA /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
class oficial extends interna {
    function oficial( context ) { interna( context ); }
	function bufferChanged(fN:String) {
		return this.ctx.oficial_bufferChanged(fN);
	}
	function habilitarPorTipo() {
		return this.ctx.oficial_habilitarPorTipo();
	}
	function buscarCampo() {
		return this.ctx.oficial_buscarCampo();
	}
	function valoresDefecto() {
		return this.ctx.oficial_valoresDefecto();
	}
}
//// OFICIAL /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration boe2011 */
//////////////////////////////////////////////////////////////////
//// BOE2011 /////////////////////////////////////////////////////
class boe2011 extends oficial {
    function boe2011( context ) { oficial( context ); }
    function buscarCampo() {
        return this.ctx.boe2011_buscarCampo();
    }
    function valoresDefecto() {
        return this.ctx.boe2011_valoresDefecto();
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
function interna_init() {
	var cursor:FLSqlCursor = this.cursor();
	connect(cursor, "bufferChanged(QString)", this, "iface.bufferChanged");
	connect (this.child("tbnBuscarCampo"), "clicked()", this, "iface.buscarCampo()");		
	connect (this.child("tbnDatosDefecto"), "clicked()", this, "iface.valoresDefecto()");	this.iface.bufferChanged("origen");

	this.iface.habilitarPorTipo();
}

function interna_calculateField(fN:String):String
{
	var util:FLUtil = new FLUtil;
	var cursor:FLSqlCursor = this.cursor();
	var valor:String = "";
	switch (fN) {
		case "lblorigen": {
			if (cursor.valueBuffer("origen") == "Facturación") {
				valor = util.translate("scripts", "Los datos se obtienen de la suma del campo Total de las facturas de clientes o proveedores del CIF seleccionado.");
			} else {
				valor = util.translate("scripts", "Los datos se obtienen de una consulta similar a la del informe de facturas emitidas / recibidas del módulo de informes de contabilidad. Cada cliente / proveedor asociado al CIF indicado debe tener una subcuenta individual.");
			}
			break;
		}
		case "cifnifcli": {
			valor = util.sqlSelect("clientes", "cifnif", "codcliente = '" + cursor.valueBuffer("codcliente") + "'");
			break;
		}
		case "cifnifprov": {
			valor = util.sqlSelect("proveedores", "cifnif", "codproveedor = '" + cursor.valueBuffer("codproveedor") + "'");
			break;
		}
	}
	return valor;
}
//// INTERNA /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
function oficial_habilitarPorTipo()
{
	var util:FLUtil = new FLUtil;
	var cursor:FLSqlCursor = this.cursor();
	switch (cursor.valueBuffer("tipo")) {
		case "Clientes": {
			this.child("fdbCodCliente").setDisabled(false);
			this.child("fdbCodProveedor").setValue("");
			this.child("fdbCodProveedor").setDisabled(true);
			break;
		}
		case "Proveedores": {
			this.child("fdbCodProveedor").setDisabled(false);
			this.child("fdbCodCliente").setValue("");
			this.child("fdbCodCliente").setDisabled(true);
			break;
		}
	}
}

function oficial_bufferChanged(fN:String)
{
	switch (fN) {
		case "origen": {
			this.child("lblOrigen").text = this.iface.calculateField("lblorigen");
			break;
		}
		case "tipo": {
			this.iface.habilitarPorTipo();
			break;
		}
		case "codcliente": {
			this.child("fdbCifNif").setValue(this.iface.calculateField("cifnifcli"));
			break;
		}
		case "codproveedor": {
			this.child("fdbCifNif").setValue(this.iface.calculateField("cifnifprov"));
			break;
		}
	}
}

function oficial_buscarCampo()
{
	var util:FLUtil = new FLUtil;
	var cursor:FLSqlCursor = this.cursor();
	
/*	var codCampana:String = cursor.valueBuffer("codcampana");
	var plantilla:String = cursor.valueBuffer("plantiemail");
	if (!plantilla) {
		plantilla = "";
	}

	var arrayAlias:Array = flcrm_mark.iface.pub_arrayAliasCampana(codCampana);*/
	var arrayAlias:Array = ["IMPORTE", "EJERCICIO"];
	var seleccion:String = Input.getItem(util.translate("scripts", "Seleccione alias"), arrayAlias);
	if (!seleccion) {
		return;
	}
	this.child("fdbParrafo1").editor().insert("#" + seleccion + "#");
}

function oficial_valoresDefecto()
{
	var saludo:String = "Muy Sres. Nuestros:";
	this.child("fdbSaludo").setValue(saludo);

	var parrafo1:String = "      En cumplimiento del Real Decreto 2027/95 sobre ingresos y pagos a terceros cuyo importe supere los #IMPORTE# ?, les comunicamos que el volumen total de operaciones con ustedes correspondientes al ejercicio #EJERCICIO#, asciende a:";
	this.child("fdbParrafo1").setValue(parrafo1);

	var parrafo2:String = "      Rogamos que de no estar conforme con dicha cantidad nos lo comunique a la mayor brevedad, entendiendo, de no recibir observaciones por su parte, que la cantidad indicada es correcta.";
	this.child("fdbParrafo2").setValue(parrafo2);

	var despedida:String = "Sin otro particular, le saluda atentamente.";
	this.child("fdbDespedida").setValue(despedida);
}

//// OFICIAL /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition boe2011 */
/////////////////////////////////////////////////////////////////
//// BOE2011 ////////////////////////////////////////////////////
function boe2011_buscarCampo()
{
    var util:FLUtil = new FLUtil;
    var cursor:FLSqlCursor = this.cursor();
    
    var dialog = new Dialog(util.translate ( "scripts", "Carta 347" ), 0);
    dialog.caption = "Seleccione un campo";
    dialog.OKButtonText = util.translate ( "scripts", "Aceptar" );
    dialog.cancelButtonText = util.translate ( "scripts", "Cancelar" );
        
    var grupo1:GroupBox = new GroupBox;
    dialog.add( grupo1 );
    grupo1.title = util.translate ( "scripts", "Seleccione un campo" );
        
    var combo1 = new ComboBox;
    grupo1.add( combo1 );
    combo1.label = util.translate ( "scripts", "Campo" );
    combo1.itemList = new Array("IMPORTEMINIMO","EJERCICIO","IMPORTE","IMPORTE1T","IMPORTE2T","IMPORTE3T","IMPORTE4T");

    var grupo2:GroupBox = new GroupBox;
    dialog.add( grupo2 );
    grupo2.title = util.translate ( "scripts", "Seleccione el parrafo" );
    
    var combo2 = new ComboBox;
    grupo2.add( combo2 );
    combo2.label = util.translate ( "scripts", "Parrafo" );
    combo2.itemList = new Array("1","2","3");
    
    var campoS:String;
    var parrafoS:String;
    if( dialog.exec() ) {
        campoS = combo1.currentItem;
        parrafoS = combo2.currentItem;
    }
    
    switch(parrafoS) {
        case "1": this.child("fdbParrafo1").editor().insert("#" + campoS + "#");break;
        case "2": this.child("fdbParrafo2").editor().insert("#" + campoS + "#");break;
        case "3": this.child("fdbParrafo3").editor().insert("#" + campoS + "#");break;
    }
    
}

function boe2011_valoresDefecto()
{
    var saludo:String = "Muy Sres. Nuestros:";
    this.child("fdbSaludo").setValue(saludo);

    var parrafo1:String = "      En cumplimiento del Real Decreto 2027/95 sobre ingresos y pagos a terceros cuyo importe supere los #IMPORTEMINIMO# ?, les comunicamos que el volumen total de operaciones con ustedes correspondientes al ejercicio #EJERCICIO#, asciende a: #IMPORTE# ?\n";
    this.child("fdbParrafo1").setValue(parrafo1);

    var parrafo2:String = "      Con relación a las modificaciones en la orden EHA/3378/2011, los importes trimestrales se verán detallados a continuación:\n\n                       Primer trimestre:  #IMPORTE1T# ?\n                       Segundo trimestre: #IMPORTE2T# ?\n                       Tercer trimestre:  #IMPORTE3T# ?\n                       Cuarto trimestre:  #IMPORTE4T# ?\n";
    this.child("fdbParrafo2").setValue(parrafo2);
    
    var parrafo3:String = "      Rogamos que de no estar conforme con las cantidades, nos lo comunique a la mayor brevedad, entendiendo, de no recibir observaciones por su parte, que la cantidad indicada es correcta.";
    this.child("fdbParrafo3").setValue(parrafo3);

    var despedida:String = "Sin otro particular, le saluda atentamente.";
    this.child("fdbDespedida").setValue(despedida);
}
//// BOE2011 ////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////

//// DESARROLLO /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
