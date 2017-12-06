var form = this;
/***************************************************************************
                      vdisco34sepa.qs  -  description
                             -------------------
    begin                : vie feb 28 2014
    copyright            : (C) 2014 by InfoSiAL S.L.
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
    var ctx;
    function interna( context ) { this.ctx = context; }
    function init() { this.ctx.interna_init(); }
	function validateForm() { return this.ctx.interna_validateForm(); }
	function acceptedForm() { return this.ctx.interna_acceptedForm(); }
}
//// INTERNA /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
class oficial extends interna {
	var xml_;
	var extensionFichero_;
	var tipoFichero_;
	var linea_;
	
  function oficial( context ) { interna( context ); }
  
  function establecerFichero() {
		return this.ctx.oficial_establecerFichero();
	}
	function ficheroTextoPlano(file) {
		return this.ctx.oficial_ficheroTextoPlano(file);
	}
	function incluirPresentadorTP(file) {
		return this.ctx.oficial_incluirPresentadorTP(file);
	}
	function incluirCabeceraTransferenciaTP(file) {
		return this.ctx.oficial_incluirCabeceraTransferenciaTP(file);
	}
	function incluirRegistroTransferenciaTP(idRecibo, file) {
		return this.ctx.oficial_incluirRegistroTransferenciaTP(idRecibo, file);
	}
	function incluirTotalTransferenciasTP(file) {
		return this.ctx.oficial_incluirTotalTransferenciasTP(file);
	}
	function incluirTotalGeneralTP(file) {
		return this.ctx.oficial_incluirTotalGeneralTP(file);
	}
	function addCampo(valor,tipo,longitud,file) {
		return this.ctx.oficial_addCampo(valor,tipo,longitud,file);
	}
	function rellenarVacios(valor,tipo,longitud) {
		return this.ctx.oficial_rellenarVacios(valor,tipo,longitud);
	}
	function devolverIdentificadorAcreedor() {
		return this.ctx.oficial_devolverIdentificadorAcreedor();
	}
	function ficheroXML(file) {
		return this.ctx.oficial_ficheroXML(file);
	}
	function crearDocumentoXML() {
		return this.ctx.oficial_crearDocumentoXML();
	}
	function incluirCabeceraXML(nodoPadre) {
		return this.ctx.oficial_incluirCabeceraXML(nodoPadre);
	}
	function incluirIdParteXML(nodoPadre) {
		return this.ctx.oficial_incluirIdParteXML(nodoPadre);
	}
	function incluirPersonaJuridicaXML(nodoPadre) {
		return this.ctx.oficial_incluirPersonaJuridicaXML(nodoPadre);
	}
	function incluirPersonaFisicaXML(nodoPadre) {
		return this.ctx.oficial_incluirPersonaFisicaXML(nodoPadre);
	}
	function incluirInformacionPagoXML(nodoPadre) {
		return this.ctx.oficial_incluirInformacionPagoXML(nodoPadre);
	}
	function incluirInformacionTipoPagoXML(nodoPadre) {
		return this.ctx.oficial_incluirInformacionTipoPagoXML(nodoPadre);
	}
	function incluirOrdenanteXML(nodoPadre) {
		return this.ctx.oficial_incluirOrdenanteXML(nodoPadre);
	}
	function incluirDireccionPostalXML(nodoPadre) {
		return this.ctx.oficial_incluirDireccionPostalXML(nodoPadre);
	}
	function incluirOperacionTransferenciaXML(nodoPadre,idRecibo) {
		return this.ctx.oficial_incluirOperacionTransferenciaXML(nodoPadre,idRecibo);
	}
	function incluirBeneficiarioXML(nodoPadre,idRecibo) {
		return this.ctx.oficial_incluirBeneficiarioXML(nodoPadre,idRecibo);
	}
	function bngFormatoFichero_clicked(opcion) {
		return this.ctx.oficial_bngFormatoFichero_clicked(opcion);
	}
	function bngTipoFichero_clicked(opcion) {
		return this.ctx.oficial_bngTipoFichero_clicked(opcion);
	}
	function formateaFecha(fecha, tipoFecha) {
		return this.ctx.oficial_formateaFecha(fecha, tipoFecha);
	}
	function formateaCadena(c) {
		return this.ctx.oficial_formateaCadena(c);
	}
	function comprobarValidate() {
		return this.ctx.oficial_comprobarValidate();
	}
	function tbnExportarErroneos_clicked() {
		return this.ctx.oficial_tbnExportarErroneos_clicked();
	}
	function comprobarCuentas() {
		return this.ctx.oficial_comprobarCuentas();
	}
	function colgarNodo(nombreHijo, nodoPadre) {
		return this.ctx.oficial_colgarNodo(nombreHijo, nodoPadre);
	}
	function colgarNodoTexto(nodoPadre, valor, tipo, min, max, decimales) {
		return this.ctx.oficial_colgarNodoTexto(nodoPadre, valor, tipo, min, max, decimales);
	}
	function validarTextoNodo(valor, tipo, min, max, decimales) {
		return this.ctx.oficial_validarTextoNodo(valor, tipo, min, max, decimales);
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
/** \D No de muestran los botones est·ndar de un formulario de registro
\end */
function interna_init()
{
	var _i = this.iface;
	
	with(form) {
		child("fdbDivisa").setDisabled(true);
		child("pushButtonAcceptContinue").close();
		child("pushButtonFirst").close();
		child("pushButtonLast").close();
		child("pushButtonNext").close();
		child("pushButtonPrevious").close();
		connect(child("pbnExaminar"), "clicked()", _i, "establecerFichero");
	}
	
	connect(this.child("bngFormatoFichero"), "clicked(int)", _i, "bngFormatoFichero_clicked");
	connect(this.child("bngTipoFichero"), "clicked(int)", _i, "bngTipoFichero_clicked");
	connect(this.child("tbnExportarErroneos"), "clicked()", _i, "tbnExportarErroneos_clicked");
	
	_i.bngFormatoFichero_clicked(0);
	_i.bngTipoFichero_clicked(0);
}

/** \C El nombre del fichero de destino debe indicarse
\end */
function interna_validateForm()
{
    var util:FLUtil = new FLUtil;
	var _i = this.iface;
	
	if (this.child("leFichero").text.isEmpty()) {
        MessageBox.warning(util.translate("scripts", "Hay que indicar el fichero."), MessageBox.Ok, MessageBox.NoButton);
		return false;
	}
	
	if (!this.child("leFichero").text.endsWith("." + _i.extensionFichero_)) {
		this.child("leFichero").text = this.child("leFichero").text + "." + _i.extensionFichero_; 
	}
	
	return true;
}

/** \C Se genera el fichero de texto con los datos de la remesa en el fichero especificado
\end */
function interna_acceptedForm()
{
    var util:FLUtil = new FLUtil;
	var _i = this.iface;
	
	if(!_i.comprobarValidate()){
        MessageBox.critical(util.translate("scripts", "No se ha podido generar el fichero."), MessageBox.Ok, MessageBox.NoButton);
        return false;
	}
	
	var file = new File(this.child("leFichero").text);
	file.open(File.WriteOnly);
		
	if(_i.extensionFichero_ == "xml"){
		if(!_i.ficheroXML(file)){
			file.remove();
            MessageBox.critical(util.translate("scripts", "No se ha podido generar el fichero."), MessageBox.Ok, MessageBox.NoButton);
			return false;
		}
	}
	else if(_i.extensionFichero_ == "txt"){
		if(!_i.ficheroTextoPlano(file)){
			file.remove();
            MessageBox.critical(util.translate("scripts", "No se ha podido generar el fichero."), MessageBox.Ok, MessageBox.NoButton);
			return false;
		}
	}
	else {
        MessageBox.critical(util.translate("scripts", "Revisa la extensiÛn del archivo."), MessageBox.Ok, MessageBox.NoButton);
		return false;
	}

	file.close();

    MessageBox.information(util.translate("scripts", "Fichero generado en: \n\n%1\n\n").arg(this.child("leFichero").text), MessageBox.Ok, MessageBox.NoButton);

	return true;
}

//// INTERNA /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////

function oficial_establecerFichero()
{
	var _i = this.iface;
	
	this.child("leFichero").text = FileDialog.getSaveFileName("*." + _i.extensionFichero_);
}

function oficial_ficheroTextoPlano(file)
{
    var util:FLUtil = new FLUtil;
	var _i = this.iface;
	var cursor = this.cursor();
	
	var idRemesa = cursor.valueBuffer("idremesa");
	
	if(!_i.incluirPresentadorTP(file)){
		return false;
	}
    
	if(!_i.incluirCabeceraTransferenciaTP(file)) {
		return false;
	}
	
	var qryRecibos = new AQSqlQuery();
  qryRecibos.setSelect("idrecibo");
  qryRecibos.setFrom("recibosprov");
  qryRecibos.setWhere("idrecibo IN (SELECT idrecibo FROM pagosdevolprov WHERE idremesa = " + idRemesa + ") OR idremesa = " + idRemesa);

  if (!qryRecibos.exec()) {
    MessageBox.warning(util.translate("Error query."), MessageBox.Ok, MessageBox.NoButton);
  	return false;
  }
  
	while(qryRecibos.next()){
		if(!_i.incluirRegistroTransferenciaTP(qryRecibos.value("idrecibo"),file)) {
			return false;
		}
	}
	
	if(!_i.incluirTotalTransferenciasTP(file)) {
		return false;
	}
	
	if(!_i.incluirTotalGeneralTP(file)) {
		return false;
	}
	
	return true;
}

function oficial_incluirPresentadorTP(file)
{
    var util:FLUtil = new FLUtil;
	var _i = this.iface;
	var cursor = this.cursor();
	_i.linea_ = "";
	
	var codCuenta = cursor.valueBuffer("codcuenta");
	var cifEmpresa = flfactppal.iface.pub_valorDefectoEmpresa("cifnif");
	var sufijo = AQUtil.sqlSelect("cuentasbanco","sufijo34","codcuenta = '" + codCuenta + "'");
	var fechaActual = _i.formateaFecha(new Date(),"AMD");
	var fechaRemesa = _i.formateaFecha(cursor.valueBuffer("fecha"),"AMD");
	var IBAN = AQUtil.sqlSelect("cuentasbanco","iban","codcuenta = '" + codCuenta + "'");
	var nombreEmpresa = flfactppal.iface.pub_valorDefectoEmpresa("nombre");
	
	if(!IBAN || IBAN == "") {
		sys.warnMsgBox(sys.translate("Falta el cÛdigo IBAN para la cuenta %1 del ordenante").arg(codCuenta));
        MessageBox.warning(util.translate("Falta el cÛdigo IBAN para la cuenta %1 del ordenante").arg(codCuenta), MessageBox.Ok, MessageBox.NoButton);
		return false;
	}

	if(!_i.addCampo(1,"num",2, 2)) {return false;}
	if(!_i.addCampo("ORD","String",3,5)) {return false;}
	if(!_i.addCampo(34145,"num",5,10)) {return false;}
	if(!_i.addCampo(1,"num",3,13)) {return false;}
	if(!_i.addCampo(cifEmpresa,"String",9,22)) {return false;}
	if(!_i.addCampo(sufijo,"num",3,25)) {return false;}
	if(!_i.addCampo(fechaActual,"String",8,33)) {return false;}
	if(!_i.addCampo(fechaRemesa,"String",8,41)) {return false;}
	if(!_i.addCampo("A","String",1,42)) {return false;}
	if(!_i.addCampo(IBAN,"String",34,76)) {return false;}
	if(_i.tipoFichero_ == "Agrupado") {
		if(!_i.addCampo(0,"num",1,77)) {return false;}
	}
	else if(_i.tipoFichero_ == "Detalle") {
		if(!_i.addCampo(1,"num",1,77)) {return false;}	
	}
	else {
		return false;
	}
	if(!_i.addCampo(nombreEmpresa,"String",70,147)) {return false;}
	if(!_i.addCampo(_i.rellenarVacios("","String",50),"String",50,197)) {return false;}
	if(!_i.addCampo(_i.rellenarVacios("","String",50),"String",50,247)) {return false;}
	if(!_i.addCampo(_i.rellenarVacios("","String",40),"String",40,287)) {return false;}
	if(!_i.addCampo(_i.rellenarVacios("","String",2),"String",2,289)) {return false;}
	if(!_i.addCampo(_i.rellenarVacios("","String",311),"String",311,600)) {return false;}
	
	file.writeLine(_i.linea_);
	_i.linea_ = "";
	
	return true;
}

function oficial_incluirCabeceraTransferenciaTP(file)
{
	var _i = this.iface;
	var cursor = this.cursor();
	_i.linea_ = "";
	
	var cifEmpresa = flfactppal.iface.pub_valorDefectoEmpresa("cifnif");
	var sufijo = AQUtil.sqlSelect("cuentasbanco","sufijo34","codcuenta = '" + cursor.valueBuffer("codcuenta") + "'");

	if(!_i.addCampo(2,"num",2, 2)) {return false;}
	if(!_i.addCampo("SCT","String",3,5)) {return false;}
	if(!_i.addCampo(34145,"num",5,10)) {return false;}
	if(!_i.addCampo(cifEmpresa,"String",9,19)) {return false;}
	if(!_i.addCampo(sufijo,"num",3,22)) {return false;}
	if(!_i.addCampo(_i.rellenarVacios("","String",578),"String",578,600)) {return false;}
	
	file.writeLine(_i.linea_);
	_i.linea_ = "";
	
	return true;
}

function oficial_incluirRegistroTransferenciaTP(idRecibo, file)
{
    var util:FLUtil = new FLUtil;
	var _i = this.iface;
	var cursor = this.cursor();
	
	var curRecibo = new AQSqlCursor("recibosprov");
	curRecibo.select("idrecibo = " + idRecibo);
	
	if(!curRecibo.first()) {
		return false;
	}
	
	curRecibo.setModeAccess(AQSql.Browse);
	curRecibo.refreshBuffer();
	
	var codCuenta = curRecibo.valueBuffer("codcuenta");
	var nombre = curRecibo.valueBuffer("nombreproveedor");
	var IBAN = AQUtil.sqlSelect("cuentasbcopro","iban","codcuenta = '" + codCuenta + "'");
	var BIC = AQUtil.sqlSelect("cuentasbcopro","bic","codcuenta = '" + codCuenta + "'");
	var concepto = "Pago del recibo " + curRecibo.valueBuffer("codigo");
	
	if(!IBAN || IBAN == "") {
        MessageBox.warning(util.translate("Falta el cÛdigo IBAN para la cuenta %1 del proveedor %2").arg(codCuenta).arg(nombre), MessageBox.Ok, MessageBox.NoButton);
		return false;
	}
	
	if(!BIC || BIC == "") {
        MessageBox.warning(util.translate("Falta el cÛdigo BIC para la cuenta con IBAN %1 del proveedor %2").arg(IBAN).arg(nombre), MessageBox.Ok, MessageBox.NoButton);
		return false;
	}

	if(!_i.addCampo(3,"num",2, 2)) {return false;}
	if(!_i.addCampo("SCT","String",3,5)) {return false;}
	if(!_i.addCampo(34145,"num",5,10)) {return false;}
	if(!_i.addCampo(2,"num",3,13)) {return false;}
	if(!_i.addCampo(curRecibo.valueBuffer("codigo"),"String",35,48)) {return false;}
	if(!_i.addCampo("A","String",1,49)) {return false;}
	if(!_i.addCampo(IBAN,"String",34,83)) {return false;}
	if(!_i.addCampo(curRecibo.valueBuffer("importe"),"numDec",11,94)) {return false;}
	if(!_i.addCampo(3,"num",1,95)) {return false;}
	if(!_i.addCampo(BIC,"String",11,106)) {return false;}
	if(!_i.addCampo(curRecibo.valueBuffer("nombreproveedor"),"String",70,176)) {return false;}
	if(!_i.addCampo(_i.rellenarVacios("","String",50),"String",50,226)) {return false;}
	if(!_i.addCampo(_i.rellenarVacios("","String",50),"String",50,276)) {return false;}
	if(!_i.addCampo(_i.rellenarVacios("","String",40),"String",40,316)) {return false;}
	if(!_i.addCampo(_i.rellenarVacios("","String",2),"String",2,318)) {return false;}
	if(!_i.addCampo(concepto,"String",140,458)) {return false;}
	if(!_i.addCampo(_i.rellenarVacios("","String",35),"String",35,493)) {return false;}
	/* Para incluir salarios SALA, PENS, OTHR (SUPP) */
	if(!_i.addCampo("SUPP","String",4,497)) {return false;}
	if(!_i.addCampo(_i.rellenarVacios("","String",4),"String",4,501)) {return false;}
	if(!_i.addCampo(_i.rellenarVacios("","String",99),"String",99,600)) {return false;}
	
	file.writeLine(_i.linea_);
	_i.linea_ = "";
	
	return true;
}

function oficial_incluirTotalTransferenciasTP(file)
{
	var _i = this.iface;
	var cursor = this.cursor();
	_i.linea_ = "";
	
	var idRemesa = cursor.valueBuffer("idremesa");
	var totalImporte = AQUtil.sqlSelect("recibosprov","sum(importe)","idrecibo IN (SELECT idrecibo FROM pagosdevolprov WHERE idremesa = " + idRemesa + ") OR idremesa = " + idRemesa);
	var totalRecibos = AQUtil.sqlSelect("recibosprov","count(*)","idrecibo IN (SELECT idrecibo FROM pagosdevolprov WHERE idremesa = " + idRemesa + ") OR idremesa = " + idRemesa);

	if(!_i.addCampo(4,"num",2, 2)) {return false;}
	if(!_i.addCampo("SCT","String",3,5)) {return false;}
	if(!_i.addCampo(totalImporte,"numDec",17,22)) {return false;}
	if(!_i.addCampo(totalRecibos,"num",8,30)) {return false;}
	if(!_i.addCampo(totalRecibos+2,"num",10,40)) {return false;}
	if(!_i.addCampo(_i.rellenarVacios("","String",560),"String",560,600)) {return false;}
	
	file.writeLine(_i.linea_);
	_i.linea_ = "";
	
	return true;
}

function oficial_incluirTotalGeneralTP(file)
{
	var _i = this.iface;
	var cursor = this.cursor();
	_i.linea_ = "";
	
	var idRemesa = cursor.valueBuffer("idremesa");
	var totalImporte = AQUtil.sqlSelect("recibosprov","sum(importe)","idrecibo IN (SELECT idrecibo FROM pagosdevolprov WHERE idremesa = " + idRemesa + ") OR idremesa = " + idRemesa);
	var totalRecibos = AQUtil.sqlSelect("recibosprov","count(*)","idrecibo IN (SELECT idrecibo FROM pagosdevolprov WHERE idremesa = " + idRemesa + ") OR idremesa = " + idRemesa);

	if(!_i.addCampo(99,"num",2, 2)) {return false;}
	if(!_i.addCampo("ORD","String",3,5)) {return false;}
	if(!_i.addCampo(totalImporte,"numDec",17,22)) {return false;}
	if(!_i.addCampo(totalRecibos,"num",8,30)) {return false;}
	if(!_i.addCampo(totalRecibos+4,"num",10,40)) {return false;}
	if(!_i.addCampo(_i.rellenarVacios("","String",560),"String",560,600)) {return false;}
	
	file.writeLine(_i.linea_);
	_i.linea_ = "";
	
	return true;
}

function oficial_addCampo(valor,tipo,longitud,longLinea)
{
    var util:FLUtil = new FLUtil;
	var _i = this.iface;
		
	var str = valor.toString();
	str = _i.formateaCadena(str);
	var strFormateada;
	
	if(tipo == "numDec"){
		var pEnt = parseInt(valor);
		var pDec = AQUtil.roundFieldValue(valor - parseInt(valor), "reciboscli", "importe");
		subDec = pDec.substring(2);
		str = pEnt.toString() + subDec.toString();
		valor = str;
	}
	
	if(str.length < longitud){
		strFormateada = _i.rellenarVacios(str,tipo,longitud);
	}
	else if(str.length == longitud){
		strFormateada = str;
	}
	else {
		strFormateada = str.left(longitud);
	}
	
	_i.linea_ += strFormateada.toString();
	
	var l = _i.linea_.length;
	if (l != longLinea) {
        MessageBox.warning(util.translate("Error en el formato de la linea."), MessageBox.Ok, MessageBox.NoButton);
		debug("_i.linea_ " + _i.linea_);
		return false;
	}
	return true;
}

function oficial_rellenarVacios(valor, tipo, longitud)
{
	var _i = this.iface;
	var strFormateada;
	
	switch(tipo){
		case "String": {
			strFormateada = flfactppal.iface.pub_espaciosDerecha(valor,longitud);
			break;
		}
		case "numDec":
		case "num": {
			strFormateada = flfactppal.iface.pub_cerosIzquierda(valor,longitud);
			break;
		}
		default: {
			strFormateada = flfactppal.iface.pub_espaciosDerecha(valor,longitud);
			break;
		}
	}
	return strFormateada;
}

function oficial_bngFormatoFichero_clicked(opcion)
{
	var _i = this.iface;
	
	switch (opcion) {
		case 0: {
			_i.extensionFichero_ = "txt";
			break;
		}
		case 1: {
			_i.extensionFichero_ = "xml";
			break;
		}
		default: {
			return false;
		}
	}
}

function oficial_bngTipoFichero_clicked(opcion)
{
	var _i = this.iface;
	
	switch (opcion) {
		case 0: {
			_i.tipoFichero_ = "Detalle";
			break;
		}
		case 1: {
			_i.tipoFichero_ = "Agrupado";
			break;
		}
		default: {
			return false;
		}
	}
}

function oficial_formateaFecha(fecha, tipoFecha)
{
	var _i = this.iface;
	
	var anyo, mes, dia, hora, minuto, segundo, milisegundo;
	
	switch(tipoFecha){
		case "AMDhms": {
			hora = fecha.getHours().toString();
			minuto = fecha.getMinutes().toString();
			segundo = fecha.getSeconds().toString();
			milisegundo = fecha.getMilliseconds().toString();
			anyo = fecha.getYear().toString();
			mes = fecha.getMonth().toString();
			dia = fecha.getDate().toString();
			break;
		}
		case "A-M-D":
		case "AMD": {
			hora = "";
			minuto = "";
			segundo = "";
			milisegundo = "";
			anyo = fecha.getYear().toString();
			mes = fecha.getMonth().toString();
			dia = fecha.getDate().toString();
			break;
		}
		default: {
			return "";
		}
	}
	
	if(hora != "" && hora.length < 2) {
		hora = flfactppal.iface.pub_cerosIzquierda(hora,2);
	}
	if(minuto != "" && minuto.length < 2) {
		minuto = flfactppal.iface.pub_cerosIzquierda(minuto,2);
	}
	if(segundo != "" && segundo.length < 2) {
		segundo = flfactppal.iface.pub_cerosIzquierda(segundo,2);
	}
	if(anyo != "" && anyo.length < 4) {
		anyo = flfactppal.iface.pub_cerosIzquierda(anyo,4);
	}
	if(mes != "" && mes.length < 2) {
		mes = flfactppal.iface.pub_cerosIzquierda(mes,2);
	}
	if(dia != "" && dia.length < 2) {
		dia = flfactppal.iface.pub_cerosIzquierda(dia,2);
	}
	if(milisegundo != "" && milisegundo.length < 5) {
		milisegundo = flfactppal.iface.pub_cerosIzquierda(milisegundo,5);
	}
	else if(milisegundo > 5){
		milisegundo = milisegundo.toString().left(5);
	}
	
	var nuevaFecha;
	
	if(tipoFecha == "A-M-D") {
		nuevaFecha = anyo + "-" + mes + "-" + dia;
	}
	else {
		nuevaFecha = anyo + mes + dia + hora + minuto + segundo + milisegundo;
	}
	
	return nuevaFecha;
}

function oficial_formateaCadena(cIn)
{
	var cOut = "";
	var equivA = "—Ò«Á¡·…ÈÕÌ”Û⁄˙¿‡»ËÃÏ“ÚŸ˘¬‚ ÍŒÓ‘Ù€˚ƒ‰ÀÎœÔ÷ˆ‹¸";
	var equivB = "NnCcAaEeIiOoUuAaEeIiOoUuAaEeIiOoUuAaEeIiOoUu";
	var validos = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ /-?+:,.'()";
	var iEq;
	for (var i = 0; i < cIn.length; i++) {
		iEq = equivA.find(cIn.charAt(i));
		if (iEq >= 0) {
			cOut += equivB.charAt(iEq);
		} else {
			if (validos.find(cIn.charAt(i)) >= 0) {
				cOut += cIn.charAt(i);
			}
		}
	}
	return cOut;
}

function oficial_comprobarValidate()
{
    var util:FLUtil = new FLUtil;
	var _i = this.iface;
	var cursor = this.cursor();
	
	var aDatosCuentas = _i.comprobarCuentas();

	if(!aDatosCuentas || aDatosCuentas.length == 0) {
		return false;
	}
	if(!aDatosCuentas[0]) {
		return true;
	}
	
	var mensaje = "";
	
	if(aDatosCuentas[1].length != 0) {
		mensaje += "Hay " + aDatosCuentas[1].length + " recibos que no tienen cuentas v·lidas.\n";
	}
	if(aDatosCuentas[2].length != 0) {
		mensaje += "Hay " + aDatosCuentas[2].length + " cuentas que no tienen IBAN v·lido.\n";
	}
	if(aDatosCuentas[3].length != 0) {
		mensaje += "Hay " + aDatosCuentas[3].length + " cuentas que no tienen BIC v·lido.\n";
	}
	
	mensaje += "\nPuede exportarlas a un fichero pulsando el botÛn 'Exportar cuentas con datos errÛneos', en el formulario actual.\n\n"
				
		
	if(aDatosCuentas[1].length != 0 || aDatosCuentas[2].length != 0 || aDatosCuentas[3].length != 0) {
		mensaje += "Debe rectificar los recibos/cuentas errÛneos para poder remesar los recibos.";
        MessageBox.information(util.translate("scripts", mensaje), MessageBox.Ok, MessageBox.NoButton);
		return false;
	}

	return true;
}

function oficial_tbnExportarErroneos_clicked() 
{
    var util:FLUtil = new FLUtil;
	var _i = this.iface;
	var cursor = this.cursor();
	
	var aDatosCuentas = _i.comprobarCuentas();
	
	if(!aDatosCuentas || aDatosCuentas.length == 0) {
		return false;
	}
	if(!aDatosCuentas[0]) {
        MessageBox.information(util.translate("scripts", "Todos los recibos y datos de cuentas son v·lidos, no se generar· el fichero."), MessageBox.Ok, MessageBox.NoButton);
		return false;
	}
	
	if(aDatosCuentas[1].length != 0 || aDatosCuentas[2].length != 0 || aDatosCuentas[3].length != 0) {
		var archivo = FileDialog.getSaveFileName("*.txt");
		
		if(!archivo || archivo == "") {
			return false;
		}
		
		if(!archivo.endsWith(".txt")) {
			archivo += ".txt";
		}
		
		var file = new File(archivo);
		file.open(File.WriteOnly);
		
		var mensaje = "";
		
		if(aDatosCuentas[1].length != 0) {
			mensaje += "Los siguientes recibos no tienen cuentas v·lidos:\n\n";
			for(var i = 0; i < aDatosCuentas[1].length; i++) {
				mensaje += "     Recibo " + aDatosCuentas[1][i][0] + " del proveedor " + aDatosCuentas[1][i][1] + " - " + aDatosCuentas[1][i][2] + "\n";
			}
			mensaje += "\n\n";
		}
		if(aDatosCuentas[2].length != 0) {
			mensaje += "Las siguientes cuentas no tienen IBAN v·lido:\n\n";
			for(var i = 0; i < aDatosCuentas[2].length; i++) {
				mensaje += "     Cuenta " + aDatosCuentas[2][i][0] + " del proveedor " + aDatosCuentas[2][i][1] + " - " + aDatosCuentas[2][i][2] + "\n";
			}
			mensaje += "\n\n";
		}
		if(aDatosCuentas[3].length != 0) {
			mensaje += "Las siguientes cuentas no tienen BIC v·lido:\n\n";
			for(var i = 0; i < aDatosCuentas[3].length; i++) {
				mensaje += "     Cuenta " + aDatosCuentas[3][i][0] + " - " + aDatosCuentas[3][i][1] + " del proveedor " + aDatosCuentas[3][i][2] + " - " + aDatosCuentas[3][i][3] + "\n";
			}
			mensaje += "\n\n";
		}
		
		file.write(mensaje);
		file.close();
		
        MessageBox.information(util.translate("scripts", "El fichero se ha generado con Èxito en %1").arg(archivo), MessageBox.Ok, MessageBox.NoButton);
	}
	else {
        MessageBox.information(util.translate("scripts", "Todos los recibos y datos de cuentas son v·lidos, no se generar· el fichero."), MessageBox.Ok, MessageBox.NoButton);
	}
	
	return true;
}

function oficial_comprobarCuentas()
{
    var util:FLUtil = new FLUtil;
	var _i = this.iface;
	var cursor = this.cursor();
	
	var recibosError = [];
	var cuentasError = [];
	var bicError = [];
	
	var error = false;
	
	var idRemesa = cursor.valueBuffer("idremesa");
	
	var qryRecibos = new FLSqlQuery();
	var groupBy = " GROUP BY codigo, codproveedor, nombreproveedor, codcuenta";
  qryRecibos.setSelect("codigo, codproveedor, nombreproveedor, codcuenta");
  qryRecibos.setFrom("recibosprov");
  qryRecibos.setWhere("idrecibo IN (SELECT idrecibo FROM pagosdevolprov WHERE idremesa = " + idRemesa + ") OR idremesa = " + idRemesa + "" + groupBy);
  
  if (!qryRecibos.exec()) {
    MessageBox.warning(util.translate("scripts", "Error query."), MessageBox.Ok, MessageBox.NoButton);
  	return false;
  }
      
	while(qryRecibos.next()){
		var curRecibos = new FLSqlCursor("recibosprov");
	curRecibos.select("codproveedor = '" + qryRecibos.value("codproveedor") + "' AND nombreproveedor = '" + qryRecibos.value("nombreproveedor") + "' AND codcuenta = '" + qryRecibos.value("codcuenta") + "' AND idrecibo IN (SELECT idrecibo FROM pagosdevolprov WHERE idremesa = " + cursor.valueBuffer("idremesa") + ")");
	
		if(!qryRecibos.value("codcuenta") || qryRecibos.value("codcuenta") == "") {
				var nArray = [qryRecibos.value("codigo"),qryRecibos.value("codproveedor"),qryRecibos.value("nombreproveedor")];
				recibosError.push(nArray);
				error = true;
				continue;
		}
		
		while(curRecibos.next()) {
			curRecibos.setModeAccess(curRecibos.Browse);
			curRecibos.refreshBuffer();
					
			var codCuenta = curRecibos.valueBuffer("codcuenta");
			var nombre = curRecibos.valueBuffer("nombreproveedor");
			var codProv = curRecibos.valueBuffer("codproveedor");
			var fechaRec = curRecibos.valueBuffer("fecha");
			var IBAN = AQUtil.sqlSelect("cuentasbcopro","iban","codcuenta = '" + codCuenta + "'");
			var BIC = AQUtil.sqlSelect("cuentasbcopro","bic","codcuenta = '" + codCuenta + "'");
			
			if(!IBAN || IBAN == "") {
				var encontrado = false;
				for(var i = 0; i < cuentasError.length; i++) {
					if(cuentasError[i][0] == codCuenta) {
						encontrado = true;
						break;
					}
				}
				if(!encontrado) {
					var nArray = [codCuenta,codProv,nombre];
					cuentasError.push(nArray);
					error = true;
				}
			}
			
			if(!BIC || BIC == "") {
				var encontrado = false;
				for(var i = 0; i < bicError.length; i++) {
					if(bicError[i][0] == codCuenta) {
						encontrado = true;
						break;
					}
				}
				if(!encontrado) {
					if(!IBAN || IBAN == "") {
						IBAN = "noIBAN";
					}
					var nArray = [codCuenta,IBAN,codProv,nombre];
					bicError.push(nArray);
					error = true;
				}
			}
		} while(curRecibos.next());
	}
	
	var aDatosCuentas = [];
	aDatosCuentas.push(error);
	aDatosCuentas.push(recibosError);
	aDatosCuentas.push(cuentasError);
	aDatosCuentas.push(bicError);
	
	return aDatosCuentas;
}

function oficial_ficheroXML(file)
{
	var _i = this.iface;
	
	_i.crearDocumentoXML();
	
	var eCstmrCdtTrfInitn = _i.colgarNodo("CstmrCdtTrfInitn","raiz");
	
	if(!_i.incluirCabeceraXML(eCstmrCdtTrfInitn)) {
		return false;
	}
	
	/* 1 a N veces */
	/* En nuestro caso siempre va a ser 1 */	
	var x = 0;
	while(x < 1) {
		if(!_i.incluirInformacionPagoXML(eCstmrCdtTrfInitn)) {
			return false;
		}
		
		x++;
	}
	
	file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
	file.write(_i.xml_.toString(2));
	
	return true;
}

function oficial_crearDocumentoXML()
{
	var _i = this.iface;
	
	_i.xml_ = new FLDomDocument;
	_i.xml_.setContent("<Document xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns='urn:iso:std:iso:20022:tech:xsd:pain.001.001.03'/>");
}

function oficial_incluirCabeceraXML(nodoPadre)
{
    var util:FLUtil = new FLUtil;
	var _i = this.iface;
	var cursor = this.cursor();
	
	var curEmpresa = new FLSqlCursor("empresa");
	curEmpresa.select("cifnif = '" + flfactppal.iface.pub_valorDefectoEmpresa("cifnif") + "'");
	if(!curEmpresa.first()) {
        MessageBox.warning(util.translate("scripts", "No hay empresa."), MessageBox.Ok, MessageBox.NoButton);
		return false;
	}
	curEmpresa.setModeAccess(curEmpresa.Browse);
	curEmpresa.refreshBuffer();
	
	var idRemesa = cursor.valueBuffer("idremesa");
	var nRecibos = AQUtil.sqlSelect("recibosprov","count(*)","idremesa = " + idRemesa);
	
	var totalImporte = AQUtil.sqlSelect("recibosprov","sum(importe)","idrecibo IN (SELECT idrecibo FROM pagosdevolprov WHERE idremesa = " + idRemesa + ") OR idremesa = " + idRemesa);
	totalImporte = AQUtil.roundFieldValue(totalImporte,"facturascli","totaliva");
	
	var eGrpHdr = _i.colgarNodo("GrpHdr",nodoPadre);
	
	var eMsgId = _i.colgarNodo("MsgId",eGrpHdr);
	if (!_i.colgarNodoTexto(eMsgId,idRemesa.toString(),"String",1,35)) {return false;}
	
	var eCreDtTm = _i.colgarNodo("CreDtTm",eGrpHdr);
	if (!_i.colgarNodoTexto(eCreDtTm,cursor.valueBuffer("fecha"),"DateTime")) {return false;}
	
	var eNbOfTxs = _i.colgarNodo("NbOfTxs",eGrpHdr);
	if (!_i.colgarNodoTexto(eNbOfTxs,nRecibos,"int",1,5)) {return false;}
	
	/* 0 o 1 veces */
	if(1==1) {
		var eCtrlSum = _i.colgarNodo("CtrlSum",eGrpHdr);
		if (!_i.colgarNodoTexto(eCtrlSum,totalImporte,"double",3,18,2)) {return false;}
	}
	
	var eInitgPty = _i.colgarNodo("InitgPty",eGrpHdr);
	
	/* 0 o 1 veces */
	if(1==1) {
		var eNm = _i.colgarNodo("Nm",eInitgPty);
		if (!_i.colgarNodoTexto(eNm,curEmpresa.valueBuffer("nombre"),"String",1,70)) {return false;}
	}
	
	/* 0 o 1 veces */
	if(1==1){
		if(!_i.incluirIdParteXML(eInitgPty)){
			return false;
		}
	}
	return true;
}

function oficial_incluirIdParteXML(nodoPadre)
{
	var _i = this.iface;

	eId = _i.colgarNodo("Id",nodoPadre);
	
	/* Condicion OR para OrgId y PrvtId */
	if(1==1) {
		if(!_i.incluirPersonaJuridicaXML(eId)) {
			return false;
		}
	}
	else {
		if(!_i.incluirPersonaFisicaXML(eId)) {
			return false;
		}
	}
	
	return true;
}

function oficial_incluirPersonaJuridicaXML(nodoPadre)
{
	var _i = this.iface;
	
	var eOrgId = _i.colgarNodo("OrgId",nodoPadre);
	
	/* 0 o 1 veces */
	if(1==0) {
		var eBICOrBEI = _i.colgarNodo("BICOrBEI",eOrgId);
		if (!_i.colgarNodoTexto(eBICOrBEI,/* valorBICOrBEI */ "valorBicOrBei","String")) {return false;}
	}

	/* 0 o 1 veces */
	if(1==1) {
		var eOthr = _i.colgarNodo("Othr",eOrgId);
		
		var id = _i.devolverIdentificadorAcreedor();
		
		var eId = _i.colgarNodo("Id",eOthr);
		if (!_i.colgarNodoTexto(eId,id,"String",1,35)) {return false;}

		/* 0 o 1 veces */
		if(1==0){
			var eSchmeNm = _i.colgarNodo("SchmeNm",eOthr);
			
			/* Condicion OR para Cd y ePrtry */
			if(1==0) {
				var eCd = _i.colgarNodo("Cd",eSchmeNm);
				if (!_i.colgarNodoTexto(eCd,/* valorCd */ "valorCd","String",1,4)) {return false;}
			}
			else {
				var ePrtry = _i.colgarNodo("Prtry",eSchmeNm);
				if (!_i.colgarNodoTexto(ePrtry,/* valorPrtry */ "valorPrtry","String",1,35)) {return false;}
			}
		}
		/* 0 o 1 veces */
		if(1==0){
			var eIssr = _i.colgarNodo("Issr",eOthr);
			if (!_i.colgarNodoTexto(eIssr,/* valorIssr */ "valorIssr","String",1,35)) {return false;}
		}
	}
	return true;
}

function oficial_incluirPersonaFisicaXML(nodoPadre)
{
	var _i = this.iface;
	
	ePrvtId = _i.colgarNodo("PrvtId",nodoPadre);
	
	/* 0 o 1 veces */
	if(1==0){
		var eDtAndPlcOfBirth = _i.colgarNodo("DtAndPlcOfBirth",ePrvtId);
		
		var eBirthDt = _i.colgarNodo("BirthDt",eDtAndPlcOfBirth);
		if (!_i.colgarNodoTexto(eBirthDt,/* valorBirthDt */ "valorBirthDt","Date")) {return false;}
		
		/* 0 o 1 veces */
		if(1==0){
			var ePrvcOfBirth = _i.colgarNodo("PrvcOfBirth",eDtAndPlcOfBirth);
			if (!_i.colgarNodoTexto(ePrvcOfBirth,/* valorPrvcOfBirth */ "valorPrvcOfBirth","String",1,35)) {return false;}
		}
		
		var eCityOfBirth = _i.colgarNodo("CityOfBirth",eDtAndPlcOfBirth);
		if (!_i.colgarNodoTexto(eCityOfBirth,/* valorCityOfBirth */ "valorCityOfBirth","String",1,35)) {return false;}
		
		var eCtryOfBirth = _i.colgarNodo("CtryOfBirth",eDtAndPlcOfBirth);
		if (!_i.colgarNodoTexto(eCtryOfBirth,/* valorCtryOfBirth */ "valorCtryOfBirth","String")) {return false;}
	}
	
	/* 0 o 1 veces */
	if(1==0){
		var eOthr = _i.colgarNodo("Othr",ePrvtId);
		
		var eId = _i.colgarNodo("Id",eOthr);
		if (!_i.colgarNodoTexto(eId,/* idEmpresa?? */ "valorId","String",1,35)) {return false;}

		/* 0 o 1 veces */
		if(1==0){
			var eSchmeNm = _i.colgarNodo("SchmeNm",eOthr);
			
			/* Condicion OR para Cd y ePrtry */
			if(1==0) {
				var eCd = _i.colgarNodo("Cd",eSchmeNm);
				if (!_i.colgarNodoTexto(eCd,/* valorCd */ "valorCd","String",1,4)) {return false;}
			}
			else {
				var ePrtry = _i.colgarNodo("Prtry",eSchmeNm);
				if (!_i.colgarNodoTexto(ePrtry,/* valorPrtry */ "valorPrtry","String",1,35)) {return false;}
			}
		}
		/* 0 o 1 veces */
		if(1==0){
			var eIssr = _i.colgarNodo("Issr",eOthr);
			if (!_i.colgarNodoTexto(eIssr,/* valorIssr */ "valorIssr","String",1,35)) {return false;}
		}
	}
	return true;
}

function oficial_incluirInformacionPagoXML(nodoPadre)
{
    var util:FLUtil = new FLUtil;
	var _i = this.iface;
	var cursor = this.cursor();
	
	var codCuenta = cursor.valueBuffer("codcuenta");
	var idRemesa = cursor.valueBuffer("idremesa");
	var fechaPago = cursor.valueBuffer("fechapago");

	var ePmtInf = _i.colgarNodo("PmtInf",nodoPadre);
	
	var ePmtInfId = _i.colgarNodo("PmtInfId",ePmtInf);
	if (!_i.colgarNodoTexto(ePmtInfId,idRemesa.toString() + "-" + codCuenta,"String",1,35)) {return false;}
	
	var ePmtMtd = _i.colgarNodo("PmtMtd",ePmtInf);
	if (!_i.colgarNodoTexto(ePmtMtd,"TRF","String")) {return false;}
	
	/* 0 o 1 veces */
	if(1==0){
		var eBtchBookg = _i.colgarNodo("BtchBookg",ePmtInf);
		if (!_i.colgarNodoTexto(eBtchBookg,/* valorBtchBookg */true,"boolean")) {return false;}
	}
	
	/* 0 o 1 veces */
	if(1==0){
		var eNbOfTxs = _i.colgarNodo("NbOfTxs",ePmtInf);
		if (!_i.colgarNodoTexto(eNbOfTxs,/* valorNbOfTxs */6,"int",1,15)) {return false;}
	}
	
	/* 0 o 1 veces */
	if(1==0) {
		var eCtrlSum = _i.colgarNodo("CtrlSum",ePmtInf);
		if (!_i.colgarNodoTexto(eCtrlSum,/* valorCtrlSum */6.6,"double",3,19,2)) {return false;}
	}
	
	/* 0 o 1 veces */
	if(1==1){
		if(!_i.incluirInformacionTipoPagoXML(ePmtInf)) {
			return false;
		}
	}
	
	var eReqdExctnDt = _i.colgarNodo("ReqdExctnDt",ePmtInf);
	if (!_i.colgarNodoTexto(eReqdExctnDt,fechaPago.toString().left(10),"Date")) {return false;}
	
	if(!_i.incluirOrdenanteXML(ePmtInf)) {
		return false;
	}
	
	/* 0 o 1 veces */
	if(1==0){
		var eUltmtCdtr = _i.colgarNodo("UltmtCdtr",ePmtInf);
		
		var eNm = _i.colgarNodo("Nm",eUltmtCdtr);
		if (!_i.colgarNodoTexto(eNm,/*valorNm*/"valorNm","String",1,70)) {return false;}
		
		/* 0 o 1 veces */
		if(1==0) {
			if(!_i.incluirIdParteXML(eUltmtCdtr)) {
				return false;
			}
		}
	}
	
	/* 0 o 1 veces */
	if(1==1){
		var eChrgBr = _i.colgarNodo("ChrgBr",ePmtInf);
		if (!_i.colgarNodoTexto(eChrgBr,"SLEV","String",1,4)) {return false;}
	}

	var qryRecibos = new FLSqlQuery();
  qryRecibos.setSelect("idrecibo");
  qryRecibos.setFrom("recibosprov");
  qryRecibos.setWhere("idrecibo IN (SELECT idrecibo FROM pagosdevolprov WHERE idremesa = " + idRemesa + ") OR idremesa = " + idRemesa);
  
  if (!qryRecibos.exec()) {
    MessageBox.warning(util.translate("scripts", "Error query."), MessageBox.Ok, MessageBox.NoButton);
  	return false;
  }
      
	while(qryRecibos.next()){
		if(!_i.incluirOperacionTransferenciaXML(ePmtInf,qryRecibos.value("idrecibo"))) {
			return false;
		}
	}
	
	return true;
}

function oficial_incluirInformacionTipoPagoXML(nodoPadre)
{
	var _i = this.iface;
	
	var ePmtTpInf = _i.colgarNodo("PmtTpInf",nodoPadre);
	
	/* 0 o 1 veces */
	if(1==1){
		var eInstrPrty = _i.colgarNodo("InstrPrty",ePmtTpInf);
		if (!_i.colgarNodoTexto(eInstrPrty,"NORM","String")) {return false;}
	}
	
	/* 0 o 1 veces */
	if(1==1){
		var eSvcLvl = _i.colgarNodo("SvcLvl",ePmtTpInf);
	
		var eCd1 = _i.colgarNodo("Cd",eSvcLvl);
		if (!_i.colgarNodoTexto(eCd1,"SEPA","String")) {return false;}
	}
	
	/* 0 o 1 veces */
	if(1==0){
		var eLclInstrm = _i.colgarNodo("LclInstrm",ePmtTpInf);
	
		if(1==1) {
			var eCd2 = _i.colgarNodo("Cd",eLclInstrm);
			if (!_i.colgarNodoTexto(eCd2,"B2B","String",1,4)) {return false;}
		}
		else {
			var ePrtry = _i.colgarNodo("Prtry",eLclInstrm);
			if (!_i.colgarNodoTexto(ePrtry,"B2B","String",1,35)) {return false;}
		}
	}
	
	/* 0 o 1 veces */
	if(1==1){
		var eCtgyPurp = _i.colgarNodo("CtgyPurp",ePmtTpInf);
	
		var eCd3 = _i.colgarNodo("Cd",eCtgyPurp);
		/* Para incluir salarios SALA, PENS, OTHR, (SUPP) */
		if (!_i.colgarNodoTexto(eCd3,"SUPP","String",1,4)) {return false;}
	}

	return true;
}

function oficial_incluirOrdenanteXML(nodoPadre)
{
    var util:FLUtil = new FLUtil;
	var _i = this.iface;
	var cursor = this.cursor();
	
	var curEmpresa = new FLSqlCursor("empresa");
	curEmpresa.select("cifnif = '" + flfactppal.iface.pub_valorDefectoEmpresa("cifnif") + "'");
	if(!curEmpresa.first()) {
        MessageBox.warning(util.translate("scripts", "No hay empresa."), MessageBox.Ok, MessageBox.NoButton);
		return false;
	}
	curEmpresa.setModeAccess(curEmpresa.Browse);
	curEmpresa.refreshBuffer();
	
	var codCuenta = cursor.valueBuffer("codcuenta");
	
	var IBAN = AQUtil.sqlSelect("cuentasbanco","iban","codcuenta = '" + codCuenta + "'");
	var bic = AQUtil.sqlSelect("cuentasbanco","bic","codcuenta = '" + codCuenta + "'");
	
	var eDbtr = _i.colgarNodo("Dbtr",nodoPadre);
	
	var eNm = _i.colgarNodo("Nm",eDbtr);
	if (!_i.colgarNodoTexto(eNm,curEmpresa.valueBuffer("nombre"),"String",1,70)) {return false;}
	
	/* 0 o 1 veces */
	if(1==0){
		if(!_i.incluirDireccionPostalXML(eDbtr)){
			return false;
		}
	}
	
	/* 0 o 1 veces */
	if(1==1){
		if(!_i.incluirIdParteXML(eDbtr)){
			return false;
		}
	}
	
	var eDbtrAcct = _i.colgarNodo("DbtrAcct",nodoPadre);
	
	var eId = _i.colgarNodo("Id",eDbtrAcct);
	
	if(!IBAN || IBAN == "") {
        MessageBox.warning(util.translate("scripts", "Falta el cÛdigo IBAN para la cuenta %1 del ordenante").arg(codCuenta), MessageBox.Ok, MessageBox.NoButton);
		return false;
	}
	
	var eIBAN = _i.colgarNodo("IBAN",eId);
	if (!_i.colgarNodoTexto(eIBAN,IBAN,"String")) {return false;}
	
	/* 0 o 1 veces */
	if(1==1){
		var divisa = flfactppal.iface.pub_valorDefectoEmpresa("coddivisa");
		
		var eCcy = _i.colgarNodo("Ccy",eDbtrAcct);
		if (!_i.colgarNodoTexto(eCcy,divisa,"String")) {return false;}
	}
	
	var eDbtrAgt = _i.colgarNodo("DbtrAgt",nodoPadre);
	
	var eFinInstnId = _i.colgarNodo("FinInstnId",eDbtrAgt);
	
	if(!bic || bic == "") {
        MessageBox.warning(util.translate("scripts", "Falta el cÛdigo BIC para la cuenta con IBAN %1 del ordenante").arg(IBAN), MessageBox.Ok, MessageBox.NoButton);
		return false;
	}
	
	var eBIC = _i.colgarNodo("BIC",eFinInstnId);
	if (!_i.colgarNodoTexto(eBIC,bic,"String")) {return false;}
	
	return true;
}

function oficial_incluirDireccionPostalXML(nodoPadre)
{
	var _i = this.iface;
	
	var ePstlAdr = _i.colgarNodo("PstlAdr",nodoPadre);
	
	/* 0 o 1 veces */
	var eCtry = _i.colgarNodo("Ctry",ePstlAdr);
	if (!_i.colgarNodoTexto(eCtry,/* valorCtry */ "valorCtry","String")) {return false;}

	/* 0 a 2 veces */
	var y = 0;
	while(y < 1) {
		var eAdrLine = _i.colgarNodo("AdrLine",ePstlAdr);
		if (!_i.colgarNodoTexto(eAdrLine,/* valorAdrLine */ "valorAdrLine","String",1,70)) {return false;}
	
		y++;
	}
		
	return true;
}

function oficial_incluirOperacionTransferenciaXML(nodoPadre,idRecibo)
{
    var util:FLUtil = new FLUtil;
	var _i = this.iface;
	var cursor = this.cursor();
		
	var curRecibo = new FLSqlCursor("recibosprov");
	curRecibo.select("idrecibo = " + idRecibo);

	if(!curRecibo.first()) {
		sys.warnMsgBox(sys.translate("No se han encontrado el recibo %1").arg(idRecibo));
		return false;
	}
	
	curRecibo.setModeAccess(curRecibo.Browse);
	curRecibo.refreshBuffer();
	
	var fechaPago = cursor.valueBuffer("fechapago");
	var codCuenta = curRecibo.valueBuffer("codCuenta");
	var codProv = curRecibo.valueBuffer("codproveedor");
	var nombre = curRecibo.valueBuffer("nombreproveedor");
	var fechaRec = curRecibo.valueBuffer("fecha");
	
	var eCdtTrfTxInf = _i.colgarNodo("CdtTrfTxInf",nodoPadre);

	var bicBanco = AQUtil.sqlSelect("cuentasbcopro","bic","codcuenta = '" + curRecibo.valueBuffer("codcuenta") + "'");
	var IBAN = AQUtil.sqlSelect("cuentasbcopro","iban","codcuenta = '" + curRecibo.valueBuffer("codcuenta") + "'");

	var ePmtId = _i.colgarNodo("PmtId",eCdtTrfTxInf);
	
	/* 0 o 1 veces */
	if(1==0) {
		var eInstrId = _i.colgarNodo("InstrId",eInstrId);
		if (!_i.colgarNodoTexto(eInstrId,/* InstrId */"InstrId","String",1,35)) {return false;}
	}
	
	var eEndToEndId = _i.colgarNodo("EndToEndId",ePmtId);
	if (!_i.colgarNodoTexto(eEndToEndId,curRecibo.valueBuffer("codigo"),"String",1,35)) {return false;}
	
	if(1==0){
		if(!_i.incluirInformacionTipoPagoXML(eCdtTrfTxInf)) {
			return false;
		}
	}

	var eAmt = _i.colgarNodo("Amt",eCdtTrfTxInf);
	
	var eInstdAmt = _i.colgarNodo("InstdAmt",eAmt);
	eInstdAmt.setAttribute("Ccy",curRecibo.valueBuffer("coddivisa"));
	
	var importeRecibo = curRecibo.valueBuffer("importe");
	importeRecibo = AQUtil.roundFieldValue(importeRecibo,"facturascli","totaliva");
	
	if (!_i.colgarNodoTexto(eInstdAmt,importeRecibo,"double",3,12,2)) {return false;}
	
	var eCdtrAgt = _i.colgarNodo("CdtrAgt",eCdtTrfTxInf);
	
	var eFinInstnId = _i.colgarNodo("FinInstnId",eCdtrAgt);
	
	if(!IBAN || IBAN == "") {
        MessageBox.warning(util.translate("scripts", "Falta el cÛdigo IBAN para la cuenta %1 del proveedor %2").arg(codCuenta).arg(nombre), MessageBox.Ok, MessageBox.NoButton);
		return false;
	}
	
	if(!bicBanco || bicBanco == "") {
        MessageBox.warning(util.translate("scripts", "Falta el cÛdigo BIC para la cuenta con IBAN %1 del proveedor %2").arg(IBAN).arg(nombre), MessageBox.Ok, MessageBox.NoButton);
		return false;
	}

	var eBIC = _i.colgarNodo("BIC",eFinInstnId);
	if (!_i.colgarNodoTexto(eBIC,bicBanco,"String")) {return false;}
	
	if(!_i.incluirBeneficiarioXML(eCdtTrfTxInf,idRecibo)){
		return false;
	}

	var eCdtrAcct = _i.colgarNodo("CdtrAcct",eCdtTrfTxInf);

	var eId = _i.colgarNodo("Id",eCdtrAcct);

	var eIBAN = _i.colgarNodo("IBAN",eId);
	if (!_i.colgarNodoTexto(eIBAN,IBAN,"String")) {return false;}
	
	/* 0 o 1 veces */
	if(1==0){
		var ePurp = _i.colgarNodo("Purp",eCdtTrfTxInf);
	
		var eCd = _i.colgarNodo("Cd",ePurp);
		if (!_i.colgarNodoTexto(eCd,/* Cd */"cd","String",1,4)) {return false;}
	}
	
	var y = 0;
	while(y < 0) {
		/*
		if(!_i.incluirInformacionRegulatoriaXML(eCdtTrfTxInf)) {
			return false;
		}
		*/
		y++;
	}
	
	/* 0 o 1 veces */
	if(1==1) {
		var eRmtInf = _i.colgarNodo("RmtInf",eCdtTrfTxInf);
		
		var concepto = "Pago del recibo " + curRecibo.valueBuffer("codigo");

		var eUstrd = _i.colgarNodo("Ustrd",eRmtInf);
		if (!_i.colgarNodoTexto(eUstrd,concepto,"String",1,140)) {return false;}
	}
	
	return true;
}

function oficial_incluirBeneficiarioXML(nodoPadre,idRecibo)
{
	var _i = this.iface;
	
	var nombreProveedor = AQUtil.sqlSelect("recibosprov","nombreproveedor","idrecibo = " + idRecibo);
	
	var eCdtr = _i.colgarNodo("Cdtr",nodoPadre);
	
	/* 0 o 1 veces */
	if(1==1){
		var eNm = _i.colgarNodo("Nm",eCdtr);
		if (!_i.colgarNodoTexto(eNm,nombreProveedor,"String",1,70)) {return false;}
	}
	
	/* 0 o 1 veces */
	if(1==0){		
		if(!_i.incluirDireccionPostalXML(eCdtr)){
			return false;
		}
	}
	
	if(1==0){
		if(!_i.incluirIdParteXML(eCdtr)){
			return false;
		}
	}
	
	return true;
}

function oficial_colgarNodo(nombreHijo, nodoPadre)
{
	var _i = this.iface;
	
	var eHijo = _i.xml_.createElement(nombreHijo);
	
	if(nodoPadre == "raiz") {
		nodoPadre = _i.xml_.firstChild.toElement();
	}
	
	nodoPadre.appendChild(eHijo);

	return eHijo;
}

function oficial_colgarNodoTexto(nodoPadre, valor, tipo, min, max, decimales)
{
	var _i = this.iface;

	if(typeof(valor) == "string"){
		valor = _i.formateaCadena(valor);
	}
	
	if(!_i.validarTextoNodo(valor, tipo, min, max, decimales)) {
		return false;
	}
	
	var eHijo = _i.xml_.createTextNode("nodoTexto");
	nodoPadre.appendChild(eHijo);
	eHijo.setNodeValue(valor);
	
	return true;
}

function oficial_validarTextoNodo(valor, tipo, min, max, decimales)
{
    var util:FLUtil = new FLUtil;
	var _i = this.iface;
	
	var typeOf = typeof(valor);
	var str = valor.toString();
	
	switch(tipo) {
		case "String": {
			if(typeOf != "string") {
                MessageBox.warning(util.translate("scripts", "El valor debe ser una cadena de texto."), MessageBox.Ok, MessageBox.NoButton);
				return false;
			}
			if(min && valor.length < min) {
                MessageBox.warning(util.translate("scripts", "Longitud de campo por debajo del mÌnimo."), MessageBox.Ok, MessageBox.NoButton);
				return false;
			}
			if(max && valor.length > max) {
			/**cortar*/
                MessageBox.warning(util.translate("scripts", "Excedida la longitud m·xima de campo."), MessageBox.Ok, MessageBox.NoButton);
				return false;
			}
			break;
		}
		case "int": {
			if(typeOf != "number") {
                MessageBox.warning(util.translate("scripts", "El valor debe ser un n˙mero entero."), MessageBox.Ok, MessageBox.NoButton);
				return false;
			}
			for(var i = 0; i < str.length; i++){
				if(str.charAt(i) > '9' || str.charAt(i) < '0'){
                    MessageBox.warning(util.translate("scripts", "El valor no debe contener decimales."), MessageBox.Ok, MessageBox.NoButton);
					return false;
				}
			}
			if(min && str.length < min) {
                MessageBox.warning(util.translate("scripts", "Longitud de campo por debajo del mÌnimo."), MessageBox.Ok, MessageBox.NoButton);
				return false;
			}
			if(max && str.length > max) {
                MessageBox.warning(util.translate("scripts", "Excedida la longitud m·xima de campo."), MessageBox.Ok, MessageBox.NoButton);
				return false;
			}
			break;
		}
		case "double": {
			if(min && str.length < min) {
                MessageBox.warning(util.translate("scripts", "Longitud de campo por debajo del mÌnimo."), MessageBox.Ok, MessageBox.NoButton);
				return false;
			}
			if(max && str.length > max) {
                MessageBox.warning(util.translate("scripts", "Excedida la longitud m·xima de campo."), MessageBox.Ok, MessageBox.NoButton);
				return false;
			}
			if(decimales > 0) {
				var dec = 0;
				var punto = false;
				for(var i = 0; i < str.length; i++){
					if(punto){
						dec++;
					}
					if(str.charAt(i) > '9' || str.charAt(i) < '0'){
						punto = true;
					}
				}
				if(dec > decimales) {
                    MessageBox.warning(util.translate("scripts", "La parte decimal excede la longitud requerida."), MessageBox.Ok, MessageBox.NoButton);
					return false;
				}
			}
			break;
		}
		case "boolean": {
			if(typeOf != "boolean") {
                MessageBox.warning(util.translate("scripts", "El valor debe ser verdadero o falso."), MessageBox.Ok, MessageBox.NoButton);
				return false;
			}
			break;
		}
		case "Date": {
			if(str.length != 10) {
                MessageBox.warning(util.translate("scripts", "El formato de la fecha debe ser 'YYYY-MM-DD'."), MessageBox.Ok, MessageBox.NoButton);
				return false;
			}
			break;
		}
		case "DateTime": {
			if(str.length != 19) {
                MessageBox.warning(util.translate("scripts", "El formato de la fecha debe ser 'YYYY-MM-DDThh:mm:ss'."), MessageBox.Ok, MessageBox.NoButton);
				return false;
			}
			break;
		}
		default: {
            MessageBox.warning(util.translate("scripts", "Formato no v·lido."), MessageBox.Ok, MessageBox.NoButton);
			return false;
			break;
		}
	}
	return true;
}

function oficial_devolverIdentificadorAcreedor()
{
	var _i = this.iface;
	var cursor = this.cursor();
	
	var codCuenta = cursor.valueBuffer("codcuenta");
	var CIFNIF = flfactppal.iface.pub_valorDefectoEmpresa("cifnif");
	
	var identificador = flfactppal.iface.calcularIdentificadorAcreedor(CIFNIF, codCuenta);
	
	return identificador;
}

//// OFICIAL /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////

//// DESARROLLO /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
