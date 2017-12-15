/***************************************************************************
                 co_masterdatos347.qs  -  description
                             -------------------
    begin                : jue mar 122009
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
	function init() { this.ctx.interna_init(); }
}
//// INTERNA /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
class oficial extends interna {
	var datosCliente_:Array;
	var datosProveedor_:Array;
	var ultimoNIF_:String;
	var contabilidad:Boolean;
	var total_:Number;
	function oficial( context ) { interna( context ); }
	function lanzar() {
		return this.ctx.oficial_lanzar();
	}
	function totalCliProv(nodo:FLDomNode, campo:String):String {
		return this.ctx.oficial_totalCliProv(nodo, campo);
	}
	function nombreProveedor(nodo:FLDomNode,campo:String):String {
		return this.ctx.oficial_nombreProveedor(nodo, campo);
	}
	function nombreCliente(nodo:FLDomNode,campo:String):String {
		return this.ctx.oficial_nombreCliente(nodo, campo);
	}
	function dirCliente(nodo:FLDomNode,campo:String):String {
		return this.ctx.oficial_dirCliente(nodo, campo);
	}
	function ciudadCliente(nodo:FLDomNode,campo:String):String {
		return this.ctx.oficial_ciudadCliente(nodo, campo);
	}
	function provCliente(nodo:FLDomNode,campo:String):String {
		return this.ctx.oficial_provCliente(nodo, campo);
	}
	function datosCliente(nodo:FLDomNode,campo:String) {
		return this.ctx.oficial_datosCliente(nodo, campo);
	}
	function dirProveedor(nodo:FLDomNode,campo:String):String {
		return this.ctx.oficial_dirProveedor(nodo, campo);
	}
	function ciudadProveedor(nodo:FLDomNode,campo:String):String {
		return this.ctx.oficial_ciudadProveedor(nodo, campo);
	}
	function provProveedor(nodo:FLDomNode,campo:String):String {
		return this.ctx.oficial_provProveedor(nodo, campo);
	}
	function datosProveedor(nodo:FLDomNode,campo:String) {
		return this.ctx.oficial_datosProveedor(nodo, campo);
	}
	function fechaEnLetra(nodo:FLDomNode,campo:String):String {
		return this.ctx.oficial_fechaEnLetra(nodo, campo);
	}
	function mostrarValores(nodo:FLDomNode,campo:String):String {
		return this.ctx.oficial_mostrarValores(nodo, campo);
	}
	function totalListado(nodo:FLDomNode,campo:String):Number {
		return this.ctx.oficial_totalListado(nodo, campo);
	}
	function textoFecha(fecha:String):String {
		return this.ctx.oficial_textoFecha(fecha);
	}
}
//// OFICIAL /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////
class head extends oficial {
	function head( context ) { oficial ( context ); }
}
//// DESARROLLO /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration boe2011 */
//////////////////////////////////////////////////////////////////
//// BOE2011 /////////////////////////////////////////////////////
class boe2011 extends oficial {
    function boe2011( context ) { oficial( context ); }
    function lanzar() {
        return this.ctx.boe2011_lanzar();
    }
    function listadeclarados347(cursor:FLSqlCursor){
        return this.ctx.boe2011_listadeclarados347(cursor);
    }
    function listado347(cursor:FLSqlCursor){
        return this.ctx.boe2011_listado347(cursor);
    }
    function guardarDatosListado(cursor:FLSqlCursor, p:Array, qryDeclarados:FLSqlQuery):Boolean {
        return this.ctx.boe2011_guardarDatosListado(cursor, p, qryDeclarados);
    }
    function calcularDireccion(clave:String, codCP:String):String {
        return this.ctx.boe2011_calcularDireccion(clave, codCP);
    }
    function calcularParrafo(cursor:FLSqlCursor,parrafo:String,datosDec:Array):String {
        return this.ctx.boe2011_calcularParrafo(cursor,parrafo,datosDec);
    }
    function formatearImporte(valor:Number, enteros:Number, decimales:Number):String {
        return this.ctx.boe2011_formatearImporte(valor, enteros, decimales);
    }
}
//// BOE2011 /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration goyza */
//////////////////////////////////////////////////////////////////
//// GOYZA /////////////////////////////////////////////////////
class goyza extends boe2011 {
    function goyza( context ) { boe2011( context ); }
    function listado347(cursor:FLSqlCursor){
        return this.ctx.goyza_listado347(cursor);
    }
}
//// GOYZA /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration ifaceCtx */
/////////////////////////////////////////////////////////////////
//// INTERFACE  /////////////////////////////////////////////////
class ifaceCtx extends goyza {
	function ifaceCtx( context ) { goyza( context ); }
	function pub_totalCliProv(nodo:FLDomNode, campo:String):String {
		return this.totalCliProv(nodo, campo);
	}
	function pub_nombreProveedor(nodo:FLDomNode,campo:String):String {
		return this.nombreProveedor(nodo, campo);
	}
	function pub_nombreCliente(nodo:FLDomNode,campo:String):String {
		return this.nombreCliente(nodo, campo);
	}
	function pub_fechaEnLetra(nodo:FLDomNode,campo:String):String {
		return this.fechaEnLetra(nodo, campo);
	}
	function pub_mostrarValores(nodo:FLDomNode,campo:String):String {
		return this.mostrarValores(nodo, campo);
	}
	function pub_dirCliente(nodo:FLDomNode,campo:String):String {
		return this.dirCliente(nodo,campo);
	}
	function pub_ciudadCliente(nodo:FLDomNode,campo:String):String {
		return this.ciudadCliente(nodo, campo);
	}
	function pub_provCliente(nodo:FLDomNode,campo:String):String {
		return this.provCliente(nodo, campo);
	}
	function pub_dirProveedor(nodo:FLDomNode,campo:String):String {
		return this.dirProveedor(nodo,campo);
	}
	function pub_ciudadProveedor(nodo:FLDomNode,campo:String):String {
		return this.ciudadProveedor(nodo, campo);
	}
	function pub_provProveedor(nodo:FLDomNode,campo:String):String {
		return this.provProveedor(nodo, campo);
	}
	function pub_totalListado(nodo:FLDomNode,campo:String):Number {
		return this.totalListado(nodo, campo);
	}
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
	connect (this.child("toolButtonPrint"), "clicked()", this, "iface.lanzar()");
}
//// INTERNA /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
function oficial_lanzar()
{
	this.iface.total_ = 0;
	var util:FLUtil = new FLUtil;
	var cursor:FLSqlCursor = this.cursor();
	var seleccion:String = cursor.valueBuffer("id");
	if (!seleccion)
		return;

	var cantidad:Number = cursor.valueBuffer("cantidad");
	var tipo:String = cursor.valueBuffer("tipo");
	var codSerie:String = cursor.valueBuffer("codserie");
	var codEjercicio:String = cursor.valueBuffer("codejercicio");
	this.iface.contabilidad = (cursor.valueBuffer("origen") == "Contabilidad");
	var consulta:String;
	var report:String;
	
	var where:String = "paises.codiso = 'ES'";
	if (this.iface.contabilidad) {
	 	where += "AND (co_asientos.nomodelo347 = false OR co_asientos.nomodelo347 IS NULL)";
	} else {
		where += "AND f.codejercicio = '" + cursor.valueBuffer("codejercicio") + "' AND (f.nomodelo347 = false OR f.nomodelo347 IS NULL)";
		if (codSerie && codSerie != "") {
			where += " AND f.codserie = '" + codSerie + "'";
		}
	}
	var orden:String = cursor.valueBuffer("orden");
	var orderBy:String;

	if (tipo == "Proveedores") {
		var cifNif:String = cursor.valueBuffer("cifnif");
		orderBy = (orden == "Nombre" ? "proveedores.nombre" : "proveedores.cifnif");
		
// 		var codProveedor:String = cursor.valueBuffer("codproveedor");
		report = cursor.valueBuffer( "listado" ) ? "co_datos347listprov" : "co_datos347prov";
		consulta = "co_datos347prov";
		if (this.iface.contabilidad) {
			where += "AND co_asientos.codejercicio = '" + cursor.valueBuffer("codejercicio") + "' AND co_asientos.tipodocumento = 'Factura de proveedor'";
			consulta += "_con";
			if (cifNif && cifNif != "") {
				var qrySubcuentas:FLSqlQuery = new FLSqlQuery;
				qrySubcuentas.setTablesList("proveedores,co_subcuentasprov");
				qrySubcuentas.setSelect("sp.idsubcuenta");
				qrySubcuentas.setFrom("proveedores p INNER JOIN co_subcuentasprov sp ON p.codproveedor = sp.codproveedor");
				qrySubcuentas.setWhere("p.cifnif = '" + cifNif + "' AND sp.codejercicio = '" + codEjercicio + "'");
				qrySubcuentas.setForwardOnly(true);
				if (!qrySubcuentas.exec()) {
					return false;
				}
				var listaSubcuentas:String = "";
				while (qrySubcuentas.next()) {
					if (listaSubcuentas != "") {
						listaSubcuentas += ", ";
					}
					listaSubcuentas += qrySubcuentas.value("sp.idsubcuenta");
				}
				if (listaSubcuentas == "") {
					MessageBox.warning(util.translate("scripts", "Los proveedores de Cif/Nif %1 no tiene subcuenta asignada para el ejercicio %2").arg(cifNif).arg(codEjercicio), MessageBox.Ok, MessageBox.NoButton);
					return;
				}
				where += " AND scp.idsubcuenta IN (" + listaSubcuentas + ")";
			}
			flcontmode.iface.pub_lanzar(cursor, consulta, where + " GROUP BY empresa.nombre, empresa.cifnif, empresa.direccion, empresa.codpostal, empresa.ciudad, proveedores.cifnif, proveedores.nombre HAVING SUM(pprov.haber - pprov.debe) >= " + cantidad + " ORDER BY " + orderBy, report);
		} else {
			if (cifNif && cifNif != "") {
				where += " AND f.cifnif = '" + cifNif + "'";
			}
			flcontmode.iface.pub_lanzar(cursor, consulta, where + " GROUP BY empresa.nombre, empresa.logo, empresa.cifnif, empresa.direccion, empresa.codpostal, empresa.ciudad, proveedores.cifnif, proveedores.nombre HAVING SUM(f.total) >= " + cantidad + " ORDER BY " + orderBy, report);
		}
	} else {
		var cifNif:String = cursor.valueBuffer("cifnif");
		report = cursor.valueBuffer( "listado" ) ? "co_datos347list" : "co_datos347";
		consulta = "co_datos347";
		orderBy = (orden == "Nombre" ? "clientes.nombre" : "clientes.cifnif");

		if (this.iface.contabilidad) {
			where += " AND co_asientos.codejercicio = '" + cursor.valueBuffer("codejercicio") + "' AND co_asientos.tipodocumento = 'Factura de cliente'";
			if (codSerie && codSerie != "")
				where += " AND piva.codserie = '" + codSerie + "'";
			consulta += "_con";
			if (cifNif && cifNif != "") {
				var qrySubcuentas:FLSqlQuery = new FLSqlQuery;
				qrySubcuentas.setTablesList("clientes,co_subcuentascli");
				qrySubcuentas.setSelect("sc.idsubcuenta");
				qrySubcuentas.setFrom("clientes c INNER JOIN co_subcuentascli sc ON c.codcliente = sc.codcliente");
				qrySubcuentas.setWhere("c.cifnif = '" + cifNif + "' AND sc.codejercicio = '" + codEjercicio + "'");
				qrySubcuentas.setForwardOnly(true);
				if (!qrySubcuentas.exec()) {
					return false;
				}
				var listaSubcuentas:String = "";
				while (qrySubcuentas.next()) {
					if (listaSubcuentas != "") {
						listaSubcuentas += ", ";
					}
					listaSubcuentas += qrySubcuentas.value("sc.idsubcuenta");
				}
				if (listaSubcuentas == "") {
					MessageBox.warning(util.translate("scripts", "Los clientes de Cif/Nif %1 no tiene subcuenta asignada para el ejercicio %2").arg(cifNif).arg(codEjercicio), MessageBox.Ok, MessageBox.NoButton);
					return;
				}
				where += " AND scc.idsubcuenta IN (" + listaSubcuentas + ")";
			}
			flcontmode.iface.pub_lanzar(cursor, consulta, where + " GROUP BY empresa.nombre, empresa.cifnif, empresa.direccion, empresa.codpostal, empresa.ciudad, clientes.cifnif, clientes.nombre HAVING SUM(pcli.debe - pcli.haber) >= " + cantidad + " ORDER BY " + orderBy, report);
		} else {
			if (cifNif && cifNif != "") {
				where += " AND f.cifnif = '" + cifNif + "'";
			}
			flcontmode.iface.pub_lanzar(cursor, consulta, where + " GROUP BY empresa.nombre, empresa.cifnif, empresa.direccion, empresa.codpostal, empresa.ciudad, clientes.cifnif, clientes.nombre HAVING SUM(f.total) >= " + cantidad + " ORDER BY " + orderBy, report);
		}
	}
}
 
function oficial_totalCliProv(nodo:FLDomNode,campo:String):String
{
	var valor:String;
	if (this.iface.contabilidad) {
		if (campo == "cli") {
			valor = nodo.attributeValue("SUM(pcli.debe - pcli.haber)");
		} else {
			valor = nodo.attributeValue("SUM(pprov.haber - pprov.debe)");
		}
	} else {
		valor = nodo.attributeValue("SUM(f.total)");
	}
	this.iface.total_ += parseFloat(valor);
	return valor;
}

function oficial_totalListado(nodo:FLDomNode,campo:String):Number
{
	return this.iface.total_;
}

function oficial_nombreCliente(nodo:FLDomNode,campo:String):String
{
	if (nodo.attributeValue("clientes.cifnif") != this.iface.ultimoNIF_) {
		this.iface.datosCliente(nodo, campo);
	}
	return this.iface.datosCliente_["nombre"];
}

function oficial_fechaEnLetra(nodo:FLDomNode,campo:String):String
{
	var hoy:Date = new Date();
	var fecha:String = hoy.toString().left(10);
	var valor:String = this.iface.textoFecha(fecha);

	return valor;
}

function oficial_textoFecha(fecha:String):String
{
	var util:FLUtil;
	if (!fecha || fecha == "") {
		return "";
	}
	var mes:String = fecha.mid(5, 2);
	var textoMes:String;
	switch (mes) {
		case "01": { textoMes = util.translate("scripts", "Enero"); break; }
		case "02": { textoMes = util.translate("scripts", "Febrero"); break; }
		case "03": { textoMes = util.translate("scripts", "Marzo"); break; }
		case "04": { textoMes = util.translate("scripts", "Abril"); break; }
		case "05": { textoMes = util.translate("scripts", "Mayo"); break; }
		case "06": { textoMes = util.translate("scripts", "Junio"); break; }
		case "07": { textoMes = util.translate("scripts", "Julio"); break; }
		case "08": { textoMes = util.translate("scripts", "Agosto"); break; }
		case "09": { textoMes = util.translate("scripts", "Septiembre"); break; }
		case "10": { textoMes = util.translate("scripts", "Octubre"); break; }
		case "11": { textoMes = util.translate("scripts", "Noviembre"); break; }
		case "12": { textoMes = util.translate("scripts", "Diciembre"); break; }
	}
	var dia:String = fecha.mid(8, 3);
	var ano:String = parseInt(fecha.mid(0, 4));
	var texto:String = util.translate("scripts", "%1 de %2 de %3").arg(dia.toString()).arg(textoMes).arg(ano);
	return texto;
}

function oficial_dirCliente(nodo:FLDomNode,campo:String):String
{
	if (nodo.attributeValue("clientes.cifnif") != this.iface.ultimoNIF_) {
		this.iface.datosCliente(nodo, campo);
	}
	return this.iface.datosCliente_["direccion"];
}

function oficial_ciudadCliente(nodo:FLDomNode,campo:String):String
{
	if (nodo.attributeValue("clientes.cifnif") != this.iface.ultimoNIF_) {
		this.iface.datosCliente(nodo, campo);
	}
	return this.iface.datosCliente_["codpostal"] + " " + this.iface.datosCliente_["ciudad"];
}

function oficial_provCliente(nodo:FLDomNode,campo:String):String
{
	if (nodo.attributeValue("clientes.cifnif") != this.iface.ultimoNIF_) {
		this.iface.datosCliente(nodo, campo);
	}
	return this.iface.datosCliente_["provincia"];
}

function oficial_datosCliente(nodo:FLDomNode,campo:String)
{
	if (!this.iface.datosCliente_) {
		this.iface.datosCliente_ = [];
	}

	var qryCliente:FLSqlQuery = new FLSqlQuery;
	qryCliente.setTablesList("clientes,dirclientes");
	qryCliente.setSelect("c.nombre, d.direccion, d.codpostal, d.ciudad, d.provincia");
	qryCliente.setFrom("clientes c INNER JOIN dirclientes d ON c.codcliente = d.codcliente");
	qryCliente.setWhere("c.cifnif = '" + nodo.attributeValue("clientes.cifnif") + "' AND d.domfacturacion = true");

	if (!qryCliente.exec()) {
		this.iface.datosCliente_["nombre"] = "";
		this.iface.datosCliente_["direccion"] = "";
		this.iface.datosCliente_["codpostal"] = "";
		this.iface.datosCliente_["ciudad"] = "";
		this.iface.datosCliente_["provincia"] = "";
	}
	if (qryCliente.first()) {
		this.iface.datosCliente_["nombre"] = qryCliente.value("c.nombre");
		this.iface.datosCliente_["direccion"] = qryCliente.value("d.direccion");
		this.iface.datosCliente_["codpostal"] = qryCliente.value("d.codpostal");
		this.iface.datosCliente_["ciudad"] = qryCliente.value("d.ciudad");
		this.iface.datosCliente_["provincia"] = qryCliente.value("d.provincia");
	} else {
		this.iface.datosCliente_["nombre"] = "";
		this.iface.datosCliente_["direccion"] = "";
		this.iface.datosCliente_["codpostal"] = "";
		this.iface.datosCliente_["ciudad"] = "";
		this.iface.datosCliente_["provincia"] = "";
	}
	this.iface.ultimoNIF_ = nodo.attributeValue("clientes.cifnif");
}

function oficial_nombreProveedor(nodo:FLDomNode,campo:String):String
{
	if (nodo.attributeValue("proveedores.cifnif") != this.iface.ultimoNIF_) {
		this.iface.datosProveedor(nodo, campo);
	}
	return this.iface.datosProveedor_["nombre"];
}

function oficial_dirProveedor(nodo:FLDomNode,campo:String):String
{
	if (nodo.attributeValue("proveedores.cifnif") != this.iface.ultimoNIF_) {
		this.iface.datosProveedor(nodo, campo);
	}
	return this.iface.datosProveedor_["direccion"];
}

function oficial_ciudadProveedor(nodo:FLDomNode,campo:String):String
{
	if (nodo.attributeValue("proveedores.cifnif") != this.iface.ultimoNIF_) {
		this.iface.datosProveedor(nodo, campo);
	}
	return this.iface.datosProveedor_["codpostal"] + " " + this.iface.datosProveedor_["ciudad"];
}

function oficial_provProveedor(nodo:FLDomNode,campo:String):String
{
	if (nodo.attributeValue("proveedores.cifnif") != this.iface.ultimoNIF_) {
		this.iface.datosProveedor(nodo, campo);
	}
	return this.iface.datosProveedor_["provincia"];
}

function oficial_datosProveedor(nodo:FLDomNode,campo:String)
{
	if (!this.iface.datosProveedor_) {
		this.iface.datosProveedor_ = [];
	}

	var qryProveedor:FLSqlQuery = new FLSqlQuery;
	qryProveedor.setTablesList("proveedores,dirproveedores");
	qryProveedor.setSelect("p.nombre, d.direccion, d.codpostal, d.ciudad, d.provincia");
	qryProveedor.setFrom("proveedores p INNER JOIN dirproveedores d ON p.codproveedor = d.codproveedor");
	qryProveedor.setWhere("p.cifnif = '" + nodo.attributeValue("proveedores.cifnif") + "' AND d.direccionppal = true");

	if (!qryProveedor.exec()) {
		this.iface.datosProveedor_["nombre"] = "";
		this.iface.datosProveedor_["direccion"] = "";
		this.iface.datosProveedor_["codpostal"] = "";
		this.iface.datosProveedor_["ciudad"] = "";
		this.iface.datosProveedor_["provincia"] = "";
	}
	if (qryProveedor.first()) {
		this.iface.datosProveedor_["nombre"] = qryProveedor.value("p.nombre");
		this.iface.datosProveedor_["direccion"] = qryProveedor.value("d.direccion");
		this.iface.datosProveedor_["codpostal"] = qryProveedor.value("d.codpostal");
		this.iface.datosProveedor_["ciudad"] = qryProveedor.value("d.ciudad");
		this.iface.datosProveedor_["provincia"] = qryProveedor.value("d.provincia");
	} else {
		this.iface.datosProveedor_["nombre"] = "";
		this.iface.datosProveedor_["direccion"] = "";
		this.iface.datosProveedor_["codpostal"] = "";
		this.iface.datosProveedor_["ciudad"] = "";
		this.iface.datosProveedor_["provincia"] = "";
	}
	this.iface.ultimoNIF_ = nodo.attributeValue("proveedores.cifnif");
}

function oficial_mostrarValores(nodo:FLDomNode,campo:String):String
{
	var cursor:FLSqlCursor = this.cursor();
	var cantidad:Number = cursor.valueBuffer("cantidad");
	var codEjercicio:String = cursor.valueBuffer("codejercicio");
	var valor:String;
	if (campo == "parrafo1") {
		var valorAux:String = cursor.valueBuffer(campo);
		if (valorAux && valorAux != "") {
			var iPos:Number = valorAux.find("#EJERCICIO#");
			if (iPos >= 0) {
				valor = valorAux.left(iPos) + codEjercicio + valorAux.right(valorAux.length - iPos - 11);
			}
			
			valorAux = valor;
			iPos = valorAux.find("#IMPORTE#");
			if (iPos >= 0) {
				valor = valorAux.left(iPos) + cantidad + valorAux.right(valorAux.length - iPos - 9);
			}
		}
	} else {
		valor = cursor.valueBuffer(campo);
	}
	return valor;
}

//// OFICIAL /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition boe2011 */
/////////////////////////////////////////////////////////////////
//// BOE2011 ///////////////////////////////////////////////////
function boe2011_lanzar()
{
    this.iface.total_ = 0;
    var util:FLUtil = new FLUtil;
    var cursor:FLSqlCursor = this.cursor();
    var seleccion:String = cursor.valueBuffer("id");
    if (!seleccion)
        return;
    
    this.iface.listadeclarados347(cursor);
    
    this.iface.listado347(cursor);
    
}

function boe2011_listadeclarados347(cursor):Boolean{

    var util:FLUtil = new FLUtil;
    
    var p:Array;
    p["tipoimp"] = "Importe";
    p = formRecordco_modelo347.iface.establecerParametrosConsulta(cursor,p);
    
    var qryDeclarados= new FLSqlQuery;  
    qryDeclarados = flcontmode.iface.pub_consultaDeclarados347(p);
    qryDeclarados.setForwardOnly(true);
    if (!qryDeclarados.exec()) {
        MessageBox.critical(util.translate("scripts", "Falló la consulta"), MessageBox.Ok, MessageBox.NoButton);
        return;
    }
    
    if (!this.iface.guardarDatosListado(cursor, p, qryDeclarados)) {
        MessageBox.critical(util.translate("scripts", "Falló el almacenamiento de datos para el listado"), MessageBox.Ok, MessageBox.NoButton);
        return false;
    }
    
    return true;
}
    
    
    
function boe2011_listado347(cursor:FLSqlCursor){
    
    var curInforme:FLSqlCursor = new FLSqlCursor("i_co_datos347_list");
    curInforme.setModeAccess(curInforme.Insert);
    curInforme.refreshBuffer();
    curInforme.setValueBuffer("i_co__datos347__list_id",cursor.valueBuffer("id"));
    
    var orderBy:String;
    if (cursor.valueBuffer("orden") == "NIF") {
        orderBy = " nifdeclarado";
    } else {
        orderBy = " apellidosnombrers";
    }
    
    var nombreInforme:String;
    if (cursor.valueBuffer("listado")) {
        nombreInforme = "co_datos347_list";
    } else {
        nombreInforme = "co_datos347_carta";
    }
    
    flcontmode.iface.pub_lanzar(curInforme, "co_datos347_list", "", nombreInforme, orderBy);
    
    
}
    
function boe2011_guardarDatosListado(cursor:FLSqlCursor, p:Array, qryDeclarados:FLSqlQuery):Boolean {
    
    var util:FLUtil = new FLUtil;
    if (!util.sqlDelete("co_datos347_list","id="+cursor.valueBuffer("id"))){
        return false;
    }
    
    var curDatos:FLSqlCursor = new FLSqlCursor("co_datos347_list");
    util.createProgressDialog(util.translate("scripts", "Guardando datos ..."), qryDeclarados.size());
    var progreso:Number = 0;
    while (qryDeclarados.next()) {
        if (progreso%100==0) util.setProgress(progreso);
        progreso++;
        var datosDec:Array = flcontmode.iface.pub_datosDeclarados(p,qryDeclarados);
        if ((datosDec.codPais && datosDec.codPais.toUpperCase() != "ES") || datosDec.codPais == "") {
            continue;
        }

        datosDec.codPais = "  ";
        
        if (datosDec.cifCP.length > 9) {
            var res= MessageBox.warning(util.translate("scripts", "El CIF ó NIF %1 (%2) correspondiente a %3 tiene más de nueve dígitos, por lo que no debería entrar en el listado de la declaración.\nPulse Ignorar para incluirlo en el listado de todas maneras,\no Cancelar para continuar con el siguiente registro").arg(datosDec.cifCP).arg(qryDeclarados.value("cifnif")).arg(datosDec.nombreCP), MessageBox.Ignore, MessageBox.Cancel);
            if (res != MessageBox.Ignore) {
                continue;
            }
        }
        
        var direccion:String = this.iface.calcularDireccion(p.clave,datosDec.codCP);
        var parrafo1:String = this.iface.calcularParrafo(cursor,"parrafo1",datosDec);
        var parrafo2:String = this.iface.calcularParrafo(cursor,"parrafo2",datosDec);
        var parrafo3:String = this.iface.calcularParrafo(cursor,"parrafo3",datosDec);
        
        curDatos.setModeAccess(curDatos.Insert);
        curDatos.refreshBuffer();
        curDatos.setValueBuffer("id", cursor.valueBuffer("id"));
        curDatos.setValueBuffer("clavecodigo", p.clave);
        curDatos.setValueBuffer("nifdeclarado", datosDec.cifCP);
        curDatos.setValueBuffer("apellidosnombrers", datosDec.nombreCP);
        curDatos.setValueBuffer("direccion", direccion);
        curDatos.setValueBuffer("importe", datosDec.importe);
        curDatos.setValueBuffer("importe1t", datosDec.importe1t);
        curDatos.setValueBuffer("importe2t", datosDec.importe2t);
        curDatos.setValueBuffer("importe3t", datosDec.importe3t);
        curDatos.setValueBuffer("importe4t", datosDec.importe4t);
        curDatos.setValueBuffer("parrafo1", parrafo1);
        curDatos.setValueBuffer("parrafo2", parrafo2);
        curDatos.setValueBuffer("parrafo3", parrafo3);
        
        if (!curDatos.commitBuffer()){
            debug("error guardando datos en listado de 347");
            util.destroyProgressDialog();
            return false;
        }
    }
    util.destroyProgressDialog();
    return true;
}

function boe2011_calcularDireccion(clave:String, codCP:String){
    
    var qryCP:FLSqlQuery = new FLSqlQuery;
    if (clave == "B") {
        qryCP.setTablesList("clientes,dirclientes");
        qryCP.setSelect("d.direccion, d.codpostal, d.ciudad, d.provincia");
        qryCP.setFrom("clientes cp INNER JOIN dirclientes d ON cp.codcliente = d.codcliente");
        qryCP.setWhere("cp.codcliente = '" + codCP + "' AND d.domfacturacion = true");
    } else {
        qryCP.setTablesList("proveedores,dirproveedores");
        qryCP.setSelect("d.direccion, d.codpostal, d.ciudad, d.provincia");
        qryCP.setFrom("proveedores cp INNER JOIN dirproveedores d ON cp.codproveedor = d.codproveedor");
        qryCP.setWhere("cp.codproveedor = '" + codCP + "' AND d.direccionppal = true");
    }
    qryCP.exec();
    var direccion:String = "";
    if (qryCP.first()) {
        direccion += qryCP.value("d.direccion")+"\n";
        direccion += qryCP.value("d.codpostal")+" - "+qryCP.value("d.ciudad")+"\n";
        direccion += qryCP.value("d.provincia");
    }
    
    return direccion;
}

function boe2011_calcularParrafo(cursor:FLSqlCursor,parrafo:String,datosDec:Array):String
{
    var cursor:FLSqlCursor = this.cursor();
    var valor:String = cursor.valueBuffer(parrafo);
    var importe:String;
    
    var regExp1:RegExp = new RegExp("#IMPORTEMINIMO#");
    regExp1.global = true;
    valor = valor.replace( regExp1, cursor.valueBuffer("cantidad") );
    
    var regExp2:RegExp = new RegExp("#EJERCICIO#");
    regExp2.global = true;
    valor = valor.replace( regExp2, cursor.valueBuffer("codejercicio") );
    
    var regExp3:RegExp = new RegExp("#IMPORTE#");
    regExp3.global = true;
    importe = this.iface.formatearImporte(datosDec.importe, 13, 2); 
    valor = valor.replace( regExp3,  importe);
    
    var regExp4:RegExp = new RegExp("#IMPORTE1T#");
    regExp4.global = true;
    importe = this.iface.formatearImporte(datosDec.importe1t, 13, 2); 
    valor = valor.replace( regExp4, importe );
    
    var regExp5:RegExp = new RegExp("#IMPORTE2T#");
    regExp5.global = true;
    importe = this.iface.formatearImporte(datosDec.importe2t, 13, 2); 
    valor = valor.replace( regExp5, importe );
    
    var regExp6:RegExp = new RegExp("#IMPORTE3T#");
    regExp6.global = true;
    importe = this.iface.formatearImporte(datosDec.importe3t, 13, 2); 
    valor = valor.replace( regExp6, importe );
    
    var regExp7:RegExp = new RegExp("#IMPORTE4T#");
    regExp7.global = true;
    importe = this.iface.formatearImporte(datosDec.importe4t, 13, 2); 
    valor = valor.replace( regExp7, importe );
    
    return valor;
}

function boe2011_formatearImporte(valor:Number, enteros:Number, decimales:Number):String
{
   
    var util:FLUtil = new FLUtil;
    var importe:String = util.roundFieldValue(valor,"co_modelo347","importetotal");
    importe = util.formatoMiles(importe);
    
    return importe;
    
}
//// BOE2011 ///////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition goyza */
/////////////////////////////////////////////////////////////////
//// GOYZA /////////////////////////////////////////////////

// OJO. ROMPE HERENCIA.
function goyza_listado347(cursor:FLSqlCursor){
    
    var curInforme:FLSqlCursor = new FLSqlCursor("i_co_datos347_list");
    curInforme.setModeAccess(curInforme.Insert);
    curInforme.refreshBuffer();
    curInforme.setValueBuffer("i_co__datos347__list_id",cursor.valueBuffer("id"));
    
    var where:String = " AND 1 = 1 ";
    if (cursor.valueBuffer("cifnif")) {
        where = " AND co_datos347_list.nifdeclarado = '"+cursor.valueBuffer("cifnif")+"'";
    }
    
    var orderBy:String;
    if (cursor.valueBuffer("orden") == "NIF") {
        orderBy = where+" ORDER BY nifdeclarado";
    } else {
        orderBy = where+" ORDER BY apellidosnombrers";
    }
    
    var nombreInforme:String;
    if (cursor.valueBuffer("listado")) {
        nombreInforme = "co_datos347_list";
    } else {
        nombreInforme = "co_datos347_carta";
    }
    
    flcontmode.iface.pub_lanzar(curInforme, "co_datos347_list", orderBy, nombreInforme);
}
//// GOYZA /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////

//// DESARROLLO /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

