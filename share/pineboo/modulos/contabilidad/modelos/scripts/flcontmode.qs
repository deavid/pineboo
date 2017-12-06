/***************************************************************************
                 co_modelo390.qs  -  description
                             -------------------
    begin                : mon may 16 2005
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
}
//// INTERNA /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
class oficial extends interna {
	var numPagina_:Number;

	function oficial( context ) { interna( context ); }
	function listaAsientosReg():String {
		return this.ctx.oficial_listaAsientosReg();
	}
	function lanzar(cursor:FLSqlCursor, nombreInforme:String, masWhere:String, nombreReport:String, orderBy:String) {
		return this.ctx.oficial_lanzar(cursor, nombreInforme, masWhere, nombreReport, orderBy);
	}
	function obtenerSigno(s:String):String {
		return this.ctx.oficial_obtenerSigno(s);
	}
	function fieldName(s:String):String {
		return this.ctx.oficial_fieldName(s);
	}
	function valorDefectoDatosFiscales(fN:String):String {
		return this.ctx.oficial_valorDefectoDatosFiscales(fN);
	}
	function valoresIniciales(){
		this.ctx.oficial_valoresIniciales();
	}
	function informarTiposVia() {
		this.ctx.oficial_informarTiposVia();
	}
	function verificarDato(valor:String, requerido:Boolean, nombre:String, maxLon:Number):Boolean {
		return this.ctx.oficial_verificarDato(valor, requerido, nombre, maxLon);
	}
	function formatoNumero(valor:Number, enteros:Number, decimales:Number):String {
		return this.ctx.oficial_formatoNumero(valor, enteros, decimales);
	}
	function formatoNumeroAbs(valor, enteros, decimales) {
                return this.ctx.oficial_formatoNumeroAbs(valor, enteros, decimales);
        }
	function mesPorIndice(indice:Number):String {
		return this.ctx.oficial_mesPorIndice(indice);
	}
	function iniciarPagina(nodo:FLDomNode,campo:String):String {
		return this.ctx.oficial_iniciarPagina(nodo, campo);
	}
	function numPagina(nodo:FLDomNode,campo:String):String {
		return this.ctx.oficial_numPagina(nodo, campo);
	}
	function controlCaracteres(valor:String):String {
		return this.ctx.oficial_controlCaracteres(valor);
	}
	function formatearTexto(texto:String):String {
		return this.ctx.oficial_formatearTexto(texto);
	}
	function limpiarCifNif(cifNif:String):String {
		return this.ctx.oficial_limpiarCifNif(cifNif);
	}
}
//// OFICIAL /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration modelo390 */
/////////////////////////////////////////////////////////////////
//// MODELO 390 /////////////////////////////////////////////////
class modelo390 extends oficial {
	function modelo390( context ) { oficial ( context ); }
	function calcularCampoBooleano(nodo:FLDomNode, campo:String):String {
		this.ctx.modelo390_calcularCampoBooleano(nodo, campo);
	}
	function lanzarInforme(cursor:FLSqlCursor, nombreInforme:String, masWhere:String) {
		return this.ctx.modelo390_lanzarInforme(cursor, nombreInforme, masWhere);
	}
}
//// MODELO 390 /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration modelo349 */
/////////////////////////////////////////////////////////////////
//// MODELO 349 /////////////////////////////////////////////////
class modelo349 extends modelo390 {
	var numOperador349:Number;

	function modelo349( context ) { modelo390 ( context ); }
	function iniciarOP349(nodo:FLDomNode,campo:String):String {
		return this.ctx.modelo349_iniciarOP349(nodo, campo);
	}
	function siguienteOP349(nodo:FLDomNode,campo:String):String {
		return this.ctx.modelo349_siguienteOP349(nodo, campo);
	}
	function formatoAlfabetico349(texto:String):String {
                return this.ctx.modelo349_formatoAlfabetico349(texto);
        }
        function formatoAlfanumerico349(texto:String):String {
                return this.ctx.modelo349_formatoAlfanumerico349(texto);
        }
}
//// MODELO 349 /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration modelo347 */
/////////////////////////////////////////////////////////////////
//// MODELO 347 /////////////////////////////////////////////////
class modelo347 extends modelo349 {
	var numOperador347:Number;
	var parcialHoja347:Number;

	function modelo347( context ) { modelo349 ( context ); }
	function iniciarDE347(nodo:FLDomNode,campo:String):String {
		return this.ctx.modelo347_iniciarDE347(nodo, campo);
	}
	function siguienteDE347(nodo:FLDomNode,campo:String):String {
		return this.ctx.modelo347_siguienteDE347(nodo, campo);
	}
	function iniciarParcial347(nodo:FLDomNode,campo:String):String {
		return this.ctx.modelo347_iniciarParcial347(nodo, campo);
	}
	function incrementarParcial347(nodo:FLDomNode,campo:String):String {
		return this.ctx.modelo347_incrementarParcial347(nodo, campo);
	}
	function valorParcial347(nodo:FLDomNode,campo:String):String {
		return this.ctx.modelo347_valorParcial347(nodo, campo);
	}
	function formatoAlfabetico347(cadena:String):String {
		return this.ctx.modelo347_formatoAlfabetico347(cadena);
	}
	function formatoAlfanumerico347(texto:String):String {
		return this.ctx.modelo347_formatoAlfanumerico347(texto);
	}
}
//// MODELO 347 /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration modelo340 */
/////////////////////////////////////////////////////////////////
//// MODELO 340 /////////////////////////////////////////////////
class modelo340 extends modelo347
{
  function modelo340(context)
  {
    modelo347(context);
  }
  function init()
  {
    return this.ctx.modelo340_init();
  }
  function rellenarTablasModelo340()
  {
    return this.ctx.modelo340_rellenarTablasModelo340();
  }
  function tablas340_2012()
  {
    return this.ctx.modelo340_tablas340_2012();
  }
  function tablas340_2014()
  {
    return this.ctx.modelo340_tablas340_2014();
  }
  function beforeCommit_co_claveoperacion(curC)
  {
    return this.ctx.modelo340_beforeCommit_co_claveoperacion(curC);
  }
  function formatoNumeroSS(valor, enteros, decimales)
  {
    return this.ctx.modelo340_formatoNumeroSS(valor, enteros, decimales);
  }
}
//// MODELO 340 /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration modelo303 */
/////////////////////////////////////////////////////////////////
//// MODELO 303 /////////////////////////////////////////////////
class modelo303 extends modelo340 {
	function modelo303( context ) { modelo340 ( context ); }
	function init() {
		this.ctx.modelo303_init();
	}
	function informarTiposDec303() {
		this.ctx.modelo303_informarTiposDec303();
	}
	function informarCasillas303() {
			this.ctx.modelo303_informarCasillas303();
	}
}
//// MODELO 303 /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration modelo180 */
/////////////////////////////////////////////////////////////////
//// MODELO 180 /////////////////////////////////////////////////
class modelo180 extends modelo303 {
	function modelo180( context ) { modelo303 ( context ); }
	function init() {
		this.ctx.modelo180_init();
	}
	function informarTiposDec180() {
		this.ctx.modelo180_informarTiposDec180();
	}
}
//// MODELO 180 /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration modelo115 */
/////////////////////////////////////////////////////////////////
//// MODELO 115 /////////////////////////////////////////////////
class modelo115 extends modelo180 {
	function modelo115( context ) { modelo180 ( context ); }
	function init() {
		this.ctx.modelo115_init();
	}
	function informarTiposDec115() {
		this.ctx.modelo115_informarTiposDec115();
	}
}

//// MODELO 115 /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration boe2011 */
/////////////////////////////////////////////////////////////////
//// BOE2011 ////////////////////////////////////////////////////
class boe2011 extends modelo115 {
    var error:String;
    var xGesteso:Boolean;
    var xC0:Boolean;
    var xMulti:Boolean;

    function boe2011( context ) { modelo115 ( context ); }
    function init() {
        this.ctx.boe2011_init();
    }
    function rellenarTablaMod340ClaveOp() {
        return this.ctx.boe2011_rellenarTablaMod340ClaveOp();
    }
    function aplicarFormato(formatoCampo:String,valorCampo:String,nombreCampo:String,longitudCampo:Number):String{
        return this.ctx.boe2011_aplicarFormato(formatoCampo,valorCampo,nombreCampo,longitudCampo);
    }
    function validarFormato(formatoCampo:String,valorCampo:String,nombreCampo:String,longitudCampo:Number):Boolean{
        return this.ctx.boe2011_validarFormato(formatoCampo,valorCampo,nombreCampo,longitudCampo);
    }
    function desRegistro347(codReg:String):Array {
        return this.ctx.boe2011_desRegistro347(codReg);
    }
    function desRegistro340(codReg:String):Array {
        return this.ctx.boe2011_desRegistro340(codReg);
    }
    function desRegistro349(codReg:String):Array {
        return this.ctx.boe2011_desRegistro349(codReg);
    }
    function generarRegistro(desReg:Array,registro:Object):String {
        return this.ctx.boe2011_generarRegistro(desReg,registro);
    }
    function generarCSV(desReg:Array,registro:Object):String {
        return this.ctx.boe2011_generarCSV(desReg,registro);
    }
    function establecerFechasPeriodo(codEjercicio:String, tipo:String, valor:String):Array{
        return this.ctx.boe2011_establecerFechasPeriodo(codEjercicio, tipo, valor);
    }
    function validarExtension(extension:String):Boolean {
        return this.ctx.boe2011_validarExtension(extension);
    }
    function consultaDeclarados347(p:Array):FLSqlQuery{
        return this.ctx.boe2011_consultaDeclarados347(p);
    }
    function establecerFromMetalico(p:Array):Array {
        return this.ctx.boe2011_establecerFromMetalico(p);
    }
    function consultaDeclaradosMetalico(p:Array):FLSqlQuery{
        return this.ctx.boe2011_consultaDeclaradosMetalico(p);
    }
    function datosDeclarados(p:Array,qryDeclarados:FLSqlQuery):Array {
        return this.ctx.boe2011_datosDeclarados(p,qryDeclarados);
    }
    function importeTrimestre(p:Array,codEjercicio:String,cifnif:String,trimestre:String):Number{
        return this.ctx.boe2011_importeTrimestre(p,codEjercicio,cifnif,trimestre);
    }
    function identFraDeclaradosMetalico(p:Array, cifnif:String):String{
        return this.ctx.boe2011_identFraDeclaradosMetalico(p, cifnif);
    }
}

//// BOE2011 ////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration modelo031 */
/////////////////////////////////////////////////////////////////
//// MODELO031 //////////////////////////////////////////////////
class modelo031 extends boe2011 {
    function modelo031( context ) { boe2011 ( context ); }
    function beforeCommit_co_modelo031(curModelo:FLsqlCursor):Boolean{
        return this.ctx.modelo031_beforeCommit_co_modelo031(curModelo);
    }
    function afterCommit_co_modelo031(curModelo:FLsqlCursor):Boolean{
        return this.ctx.modelo031_afterCommit_co_modelo031(curModelo);
    }
    function generarAsientoModelo031(curModelo:FLSqlCursor):Boolean {
        return this.ctx.modelo031_generarAsientoModelo031(curModelo);
    }
    function generarPartidaIvaImportacion(curModelo:FLSqlCursor, datosAsiento:Array, valoresDefecto:Array) {
        return this.ctx.modelo031_generarPartidaIvaImportacion(curModelo, datosAsiento, valoresDefecto);
    }
    function generarPartidaHPAcreedorIva(curModelo:FLSqlCursor, datosAsiento:Array, valoresDefecto:Array) {
        return this.ctx.modelo031_generarPartidaHPAcreedorIva(curModelo, datosAsiento, valoresDefecto) ;
    }
    function beforeCommit_co_pagomodelo031(curPago:FLsqlCursor):Boolean{
        return this.ctx.modelo031_beforeCommit_co_pagomodelo031(curPago);
    }
    function afterCommit_co_pagomodelo031(curPago:FLsqlCursor):Boolean{
        return this.ctx.modelo031_afterCommit_co_pagomodelo031(curPago);
    }
    function generarAsientoPagoModelo031(curPago:FLSqlCursor):Boolean {
        return this.ctx.modelo031_generarAsientoPagoModelo031(curPago);
    }
    function generarPartidaBanco(curPago:FLSqlCursor, datosAsiento:Array, valoresDefecto:Array) {
        return this.ctx.modelo031_generarPartidaBanco(curPago, datosAsiento, valoresDefecto);
    }
    function generarPartidaPagoHPAcreedorIva(curPago:FLSqlCursor, datosAsiento:Array, valoresDefecto:Array) {
        return this.ctx.modelo031_generarPartidaPagoHPAcreedorIva(curPago, datosAsiento, valoresDefecto);
    }
    function cambiarEstadoModelo031(idModelo:Number):Boolean{
        return this.ctx.modelo031_cambiarEstadoModelo031(idModelo);
    }
}
//// MODELO031 /////////////////////////////////////////////////
////////////////////////////////////////////////////////////////

/** @class_declaration head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////
class head extends modelo031 {
	function head( context ) { modelo031 ( context ); }
}
//// DESARROLLO /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration pubModelo390 */
/////////////////////////////////////////////////////////////////
//// PUB_MODELO 390 /////////////////////////////////////////////
class pubModelo390 extends head {
	function pubModelo390( context ) { head( context ); }
	function pub_calcularCampoBooleano(nodo:FLDomNode,campo:String):String{
		return this.calcularCampoBooleano(nodo, campo);
	}
	function pub_lanzarInforme(cursor:FLSqlCursor, nombreInforme:String, masWhere:String) {
		return this.lanzarInforme(cursor, nombreInforme, masWhere);
	}
}

//// PUB_MODELO390 ///////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration pubModelo349 */
/////////////////////////////////////////////////////////////////
//// PUB_MODELO349 /////////////////////////////////////////////
class pubModelo349 extends pubModelo390 {
	function pubModelo349( context ) { pubModelo390( context ); }
	function pub_iniciarOP349(nodo:FLDomNode,campo:String):String {
		return this.iniciarOP349(nodo, campo);
	}
	function pub_siguienteOP349(nodo:FLDomNode,campo:String):String {
		return this.siguienteOP349(nodo, campo);
	}
        function pub_formatoAlfabetico349(texto:String):String {
                return this.formatoAlfabetico349(texto);
        }
        function pub_formatoAlfanumerico349(texto:String):String {
                return this.formatoAlfanumerico349(texto);
        }
}

//// PUB_MODELO349 ///////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration pubModelo347 */
/////////////////////////////////////////////////////////////////
//// PUB_MODELO347 /////////////////////////////////////////////
class pubModelo347 extends pubModelo349 {
	function pubModelo347( context ) { pubModelo349( context ); }
	function pub_iniciarDE347(nodo:FLDomNode,campo:String):String {
		return this.iniciarDE347(nodo, campo);
	}
	function pub_siguienteDE347(nodo:FLDomNode,campo:String):String {
		return this.siguienteDE347(nodo, campo);
	}
	function pub_iniciarParcial347(nodo:FLDomNode,campo:String):String {
		return this.iniciarParcial347(nodo, campo);
	}
	function pub_incrementarParcial347(nodo:FLDomNode,campo:String):String {
		return this.incrementarParcial347(nodo, campo);
	}
	function pub_valorParcial347(nodo:FLDomNode,campo:String):String {
		return this.valorParcial347(nodo, campo);
	}
	function pub_formatoAlfabetico347(cadena:String):String {
		return this.formatoAlfabetico347(cadena);
	}
	function pub_formatoAlfanumerico347(cadena:String):String {
		return this.formatoAlfanumerico347(cadena);
	}
}

//// PUB_MODELO347 /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration pubBoe2011 */
/////////////////////////////////////////////////////////////////
//// PUBBOE2011 /////////////////////////////////////////////////
class pubBoe2011 extends pubModelo347 {
    function pubBoe2011( context ) { pubModelo347 ( context ); }
    function pub_aplicarFormato(formatoCampo:String,valorCampo:String,nombreCampo:String,longitudCampo:Number):String{
        return this.aplicarFormato(formatoCampo,valorCampo,nombreCampo,longitudCampo);
    }
    function pub_validarFormato(formatoCampo:String,valorCampo:String,nombreCampo:String,longitudCampo:Number):Boolean{
        return this.validarFormato(formatoCampo,valorCampo,nombreCampo,longitudCampo);
    }
    function pub_desRegistro347(codReg:String):Array {
        return this.desRegistro347(codReg);
    }
    function pub_desRegistro340(codReg:String):Array {
        return this.desRegistro340(codReg);
    }
    function pub_desRegistro349(codReg:String):Array {
        return this.desRegistro349(codReg);
    }
    function pub_generarRegistro(desReg:Array,registro:Object):String {
        return this.generarRegistro(desReg,registro);
    }
    function pub_generarCSV(desReg:Array,registro:Object):String {
        return this.generarCSV(desReg,registro);
    }
    function pub_establecerFechasPeriodo(codEjercicio:String, tipo:String, valor:String):Array{
        return this.establecerFechasPeriodo(codEjercicio, tipo, valor);
    }
    function pub_consultaDeclarados347(p:Array):FLSqlQuery{
        return this.consultaDeclarados347(p);
    }
    function pub_establecerFromMetalico(p:Array):Array {
        return this.establecerFromMetalico(p);
    }
    function pub_consultaDeclaradosMetalico(p:Array):FLSqlQuery{
        return this.consultaDeclaradosMetalico(p);
    }
    function pub_datosDeclarados(p:Array,qryDeclarados:FLSqlQuery):Array {
        return this.datosDeclarados(p,qryDeclarados);
    }
    function pub_importeTrimestre(p:Array,codEjercicio:String,cifnif:String,trimestre:String):Number{
        return this.importeTrimestre(p,codEjercicio,cifnif,trimestre);
    }
    function pub_identFraDeclaradosMetalico(p:Array, cifnif):String{
        return this.identFraDeclaradosMetalico(p, cifnif);
    }
}

//// PUB_BOE2011 /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration ifaceCtx */
/////////////////////////////////////////////////////////////////
//// INTERFACE  /////////////////////////////////////////////////
class ifaceCtx extends pubBoe2011 {
	function ifaceCtx( context ) { pubBoe2011( context ); }
	function pub_listaAsientosReg():String {
		return this.listaAsientosReg();
	}
	function pub_lanzar(cursor:FLSqlCursor, nombreInforme:String, masWhere:String, nombreReport:String, orderBy:String) {
		return this.lanzar(cursor, nombreInforme, masWhere, nombreReport, orderBy);
	}
	function pub_valorDefectoDatosFiscales(fN:String):String {
		return this.valorDefectoDatosFiscales(fN);
	}
	function pub_verificarDato(valor:String, requerido:Boolean, nombre:String, maxLon:Number):Boolean {
		return this.verificarDato(valor, requerido, nombre, maxLon);
	}
	function pub_formatoNumero(valor:Number, enteros:Number, decimales:Number):String {
		return this.formatoNumero(valor, enteros, decimales);
	}
	function pub_formatoNumeroAbs(valor, enteros, decimales) {
                return this.formatoNumeroAbs(valor, enteros, decimales);
        }
	function pub_mesPorIndice(indice:Number):String {
		return this.mesPorIndice(indice);
	}
	function pub_numPagina(nodo:FLDomNode,campo:String):String {
		return this.numPagina(nodo, campo);
	}
	function pub_iniciarPagina(nodo:FLDomNode,campo:String):String {
		return this.iniciarPagina(nodo, campo);
	}
	function pub_controlCaracteres(valor:String):String {
		return this.controlCaracteres(valor);
	}
	function pub_formatearTexto(texto:String):String {
		return this.formatearTexto(texto);
	}
	function pub_limpiarCifNif(cifNif:String):String {
		return this.limpiarCifNif(cifNif);
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
function interna_init() {
	var util:FLUtil = new FLUtil();
	if (!util.sqlSelect("co_tiposvia", "codtipovia", "1 = 1"))
		this.iface.informarTiposVia();

	var cursor:FLSqlCursor = new FLSqlCursor("co_datosfiscales");
	cursor.select();
	if (!cursor.first()) {
			MessageBox.information(util.translate("scripts",
					"Se insertarán algunos datos fiscales para empezar a trabajar."),
					MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
			this.iface.valoresIniciales();
			this.execMainScript("co_datosfiscales");
	}
}
//// INTERNA /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
/** \D Lanza un informe basado en unos determinados criterios de búsqueda

@param	cursor: Cursor posicionado en un registro de criterios de búsqueda
@param	nombreInforme: Nombre del informe a lanzar
@param	masWhere: Parte a añadir a la cláusula where
\end */
function oficial_lanzar(cursor:FLSqlCursor, nombreInforme:String, masWhere:String, nombreReport:String, orderBy:String)
{
	var util:FLUtil = new FLUtil;
	var q:FLSqlQuery = new FLSqlQuery(nombreInforme);

	if (!nombreReport)
		nombreReport = nombreInforme;

	var fieldList:String = util.nombreCampos(cursor.table());
	var cuenta:Number = parseFloat(fieldList[0]);

	var signo:String;
	var fN:String;
	var valor:String;
	var primerCriterio:Boolean = false;
	var where:String = "";
	for (var i:Number = 1; i <= cuenta; i++) {
		if (cursor.isNull(fieldList[i]))
			continue;
		signo = this.iface.obtenerSigno(fieldList[i]);
		if (signo != "") {
			fN = this.iface.fieldName(fieldList[i]);
			valor = cursor.valueBuffer(fieldList[i]);
			if (valor == "Sí")
				valor = 1;
			if (valor == "No")
				valor = 0;
			if (valor == "Todos")
				valor = "";
			if (!valor.toString().isEmpty()) {
				if (primerCriterio == true)
					where += "AND ";
				where += fN + " " + signo + " '" + valor + "' ";
				primerCriterio = true;
			}
		}
	}

	if ( masWhere && !masWhere.isEmpty() )
		where += masWhere;
	q.setWhere(where);
debug(q.sql())
	if (q.exec() == false) {
		MessageBox.critical(util.translate("scripts", "Falló la consulta"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
		return;
	} else {
		if (q.first() == false) {
			MessageBox.warning(util.translate("scripts", "No hay registros que cumplan los criterios de búsqueda establecidos"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
			return;
		}
	}

        var rptViewer:FLReportViewer = new FLReportViewer();
        rptViewer.setReportTemplate(nombreReport);
        rptViewer.setReportData(q);
        rptViewer.renderReport();
        rptViewer.exec();

}

/** \D Construye una lista separada por comas con los idasientos de los asientos de regularización de iva
\end */
function oficial_listaAsientosReg():String
{
	var lista:String = "";
	var q:FLSqlQuery = new FLSqlQuery();
	q.setTablesList("co_regiva");
	q.setSelect("idasiento");
	q.setFrom("co_regiva");
	if (!q.exec()) return lista;
	while (q.next()) {
		lista += q.value(0) + ",";
	}
	lista = lista.left(lista.length - 1);
	if (!lista) lista = "-1";
	return lista;
}

/** \D
Obtiene el operador lógico a aplicar en la cláusula where de la consulta a partir de los primeros caracteres del parámetro
@param	s: Nombre del campo que contiene un criterio de búsqueda
@return	Operador lógico a aplicar
\end */
function oficial_obtenerSigno(s:String):String
{
	if (s.toString().charAt(1) == "_") {
		switch(s.toString().charAt(0)) {
			case "d": {
				return ">=";
			}
			case "h": {
				return "<=";
			}
			case "i": {
				return "=";
			}
		}
	}
	return  "";
}

/** \D Convierte el nombre de un campo de una tabla de informe en un nombre de tabla más un nombre de campo separados por un punto. Se utiliza en campos que definen condiciones lógicas en la consulta del informe como 'igual a', 'mayor o igual que' o 'menor o igual que'. Ejemplo: d_co__asientos_numero como entrada daría como resultado co_asientos.numero

Sustituye '_' por '.'; dos '_' seguidos indica que realmente es '_'

@param s Nombre del campo en la tabla del informe
@return Nombre de campo.Nombre de tabla
\end */
function oficial_fieldName(s:String):String
{
	var fN:String = "";
	var c:String;
	for (var i:Number = 2; (s.toString().charAt(i)); i++) {
		c = s.toString().charAt(i);
		if (c == "_")
			if (s.toString().charAt(i + 1) == "_") {
				fN += "_";
				i++;
			} else
				fN += "."
		else
			fN += s.toString().charAt(i);
	}
	return fN;
}

function oficial_valorDefectoDatosFiscales(fN:String):String
{
	var cursorDatosFiscales:FLSqlCursor = new FLSqlCursor("co_datosfiscales");
	cursorDatosFiscales.select();
	if (cursorDatosFiscales.first())
		return cursorDatosFiscales.valueBuffer(fN);
}

function oficial_valoresIniciales()
{
	var q:FLSqlQuery= new FLSqlQuery();
	var cursor:FLSqlCursor = new FLSqlCursor("co_datosfiscales");

	q.setSelect("nombre,cifnif,codpostal,ciudad,provincia,telefono,administrador,idprovincia");
	q.setFrom("empresa");
	q.setTablesList("empresa");

	q.exec();
	if (!q.first()) return;

	var temp:String;
	with(cursor) {
		setModeAccess(cursor.Insert);
		refreshBuffer();
		temp = q.value(0);
		if (temp && temp != "")
			temp = temp.left(30);
		setValueBuffer("apellidosrs", temp);

		temp = q.value(1);
		if (temp && temp != "")
			temp = temp.left(9);
		setValueBuffer("cifnif", temp);

		temp = q.value(2);
		if (temp && temp != "")
			temp = temp.left(5);
		setValueBuffer("codpos", temp);

		temp = q.value(3);
		if (temp && temp != "")
			temp = temp.left(20);
		setValueBuffer("municipio", temp);

		temp = q.value(4);
		if (temp && temp != "")
			temp = temp.left(15);
		setValueBuffer("provincia", temp);

		temp = q.value(5);
		if (temp && temp != "")
			temp = temp.left(9);
		setValueBuffer("telefono", temp);

		temp = q.value(6);
		if (temp && temp != "")
			temp = temp.left(15);
		setValueBuffer("nombre", temp);

		temp = q.value(7);
		if (temp == 0)
			setNull("idprovincia");
		else
			setValueBuffer("idprovincia", temp);

		commitBuffer();
	}
}

function oficial_informarTiposVia()
{
	var curTipoVia:FLSqlCursor = new FLSqlCursor("co_tiposvia");
	var valores:Array = [
	["AL", "Alameda, aldea"],
	["AP", "Apartamento"],
	["AV", "Avenida"],
	["BL", "Bloque"],
	["BO", "Barrio"],
	["CH", "Chalet"],
	["CL", "Calle"],
	["CM", "Camino"],
	["CO", "Colonia"],
	["CR", "Carretera"],
	["CS", "Caserío"],
	["CT", "Cuesta"],
	["ED", "Edificio"],
	["GL", "Glorieta"],
	["GR", "Grupo"],
	["LU", "Lugar"],
	["ME", "Mercado"],
	["MU", "Municipio"],
	["MZ", "Manzana"],
	["PB", "Poblado"],
	["PG", "Polígono"],
	["PJ", "Pasaje"],
	["PQ", "Parque"],
	["PZ", "Plaza"],
	["PR", "Prolongación"],
	["PS", "Paseo"],
	["RB", "Rambla"],
	["RD", "Ronda"],
	["TR", "Travesía"],
	["UR", "Urbanización"]];

	for (var i:Number = 0; i < valores.length; i++) {
		with (curTipoVia) {
			setModeAccess(Insert);
			refreshBuffer();
			setValueBuffer("codtipovia", valores[i][0]);
			setValueBuffer("descripcion", valores[i][1]);
			commitBuffer();
		}
	}
}

/** \D Comprueba que si un campo es requerido esté informado, y si lo está, que tenga una longitud inferior al máximo establecido
@param	valor: Valor a comprobar
@param	requerido: Indica si el campo es requerido o no
@param	nombre: Nombre del campo para mostrar en caso de error
@param	maxLon: Longitud máxima del campo
@return	true si la comprobación es correcta, false en caso contrario
\end */
function oficial_verificarDato(valor:String, requerido:Boolean, nombre:String, maxLon:Number):Boolean
{
	var util:FLUtil = new FLUtil;
	if (!valor || valor == "") {
		if (!requerido)
			return true;
		MessageBox.warning(util.translate("scripts", "Debe establecer el valor del siguiente campo: ") + nombre, MessageBox.Ok, MessageBox.NoButton);
		return false;
	}

	valor = sys.fromUnicode(valor, "ISO-8859-1");

	if (valor.toString().length > maxLon) {
		MessageBox.warning(util.translate("scripts", "La longitud del dato excede su longitud máxima: ") + nombre + " - " + maxLon, MessageBox.Ok, MessageBox.NoButton);
		return false;
	}

	return true;
}

/** \D Sustituye ciertos caracteres por caracteres válidos
@param	valor: Valor a comprobar
@return	valor revisado
\end */
function oficial_controlCaracteres(valor:String):String
{
	var valorRevisado:String = valor;
	if (!valorRevisado || valorRevisado == "")
		return valorRevisado;

	valorRevisado = valorRevisado.toUpperCase();

	var caracteres:Array = [["Ç", "C"], ["[ÀÁÂ]", "A"], ["[ÈÉÊ]", "E"], ["[ÌÍÌ]", "I"], ["[ÒÓÒ]", "O"], ["[ÙÚÛ]", "U"]];
	var regExpTemp:RegExp;
	for (var i:Number = 0; i < caracteres.length; i++) {
		regExpTemp = new RegExp(caracteres[i][0]);
		while (valorRevisado.find(regExpTemp) > -1)
			valorRevisado = valorRevisado.replace(regExpTemp, caracteres[i][1]);
	}
	return valorRevisado;
}

/** \D Formatea un número de acuerdo con los parámetros establecidos
@param	valor: Valor a formatear
@param	enteros: Número de cifras enteras
@param	decimales: Número de cifras decimales
@return	número formateado
\end */
function oficial_formatoNumero(valor:Number, enteros:Number, decimales:Number):String
{
	for (var i:Number = 0; i < decimales; i++)
		valor *= 10;

	valor = Math.round(valor);

	var resultado:String = flfactppal.iface.pub_cerosIzquierda(valor, (enteros + decimales));
	return resultado;
}

function oficial_formatoNumeroAbs(valor:Number, enteros:Number, decimales:Number):String
{
        for (var i:Number = 0; i < decimales; i++)
                valor *= 10;

        valor = Math.round(valor);
        valor = Math.abs(valor);

        var resultado:String = flfactppal.iface.pub_cerosIzquierda(valor, (enteros + decimales));
        return resultado;
}

/** \D Obtiene el nombre del mes a partir de su número
@param	indice: Número del mes
@return	Nombre del mes
\end */
function oficial_mesPorIndice(indice:Number):String
{
	var meses:Array = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
	return meses[indice - 1];
}

/** \D Inicia a 1 el contador de páginas
\end */
function oficial_iniciarPagina(nodo:FLDomNode,campo:String):String
{
	this.iface.numPagina_ = 1;
}

/** \D Devuelve el valor del contador de páginas
\end */
function oficial_numPagina(nodo:FLDomNode,campo:String):String
{
	return this.iface.numPagina_++;
}

/** \C Pasa un texto a mayúsculas y elimina las tildes
@param texto: Texto a formatear
@return Texto formateado
\end */
function oficial_formatearTexto(texto:String):String
{
	if (!texto || texto == "") {
		return texto;
	}
        var carValidos:String = " &,-.0123456789:;ABCDEFGHIJKLMNOPQRSTUVWXYZ_ÇÑ/'()";
        var textoMay:String = texto.toUpperCase();
        var resultado:String = "";
        var caracter:String;

        for (var i:Number = 0; i < textoMay.length; i++) {
                caracter = textoMay.charAt(i);
                switch (caracter) {
			case "Á":
			case "À":
                        case "Â":{
				resultado += "A";
				break;
			}
			case "É":
			case "È":
                        case "Ê":{
				resultado += "E";
				break;
			}
			case "Í":
			case "Ì": {
				resultado += "I";
				break;
			}
			case "Ó":
			case "Ò": {
				resultado += "O";
				break;
			}
			case "Ú":
			case "Ù":
                        case "Û":{
				resultado += "U";
				break;
			}

                        case "  ":
                        case "\"":
                            resultado += "";
                            break;

			default: {
                                if (carValidos.find(caracter) >= 0) {
                                        resultado += caracter;
                                } else {
                                        debug("ignorando '" + caracter + "'");
                                }
                                break;
                        }
		}
	}
	return resultado;
}

/** \C Elimina caracteres inválidos de un CIF o NIF (".", "-", etc.)
@param CIF o NIF a limpiar
@return CIF o NIF limpio
\end */
function oficial_limpiarCifNif(cifNif:String):String
{
	var cifLimpio:String = "";
	if (cifNif && cifNif != "") {
		var caracter:String;
		for (var i:Number = 0; i < cifNif.length; i++) {
			caracter = cifNif.charAt(i);
			switch (caracter) {
				case ".":
				case " ":
				case "-": {
					break;
				}
				default: {
					cifLimpio += caracter;
				}
			}
		}
	}
	return cifLimpio;
}

//// OFICIAL /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition modelo390 */
/////////////////////////////////////////////////////////////////
//// MODELO 390 /////////////////////////////////////////////////
/** \D Devuelve una X si el valor del campo es verdadero. Esta función se usa desde los scripts para cumplimentas correctamente los campos de tipo casilla de verificación

@param	nodo: Nodo con los valores de la fila actual del informe
@param	campo: Nombre del campo (no se usa en esta función)
@return	X si el valor del campo es verdadero, cadena vacía si es falso
\end */
function modelo390_calcularCampoBooleano(nodo:FLDomNode, campo:String):String
{
	var decpterceros:String = nodo.attributeValue("co_modelo390.declaracionopterceros3");

	if (decpterceros)
		return "X"
	else
		return ""
}

function modelo390_lanzarInforme( cursor:FLSqlCursor, nombreInforme:String, masWhere:String )
{
	var util:FLUtil = new FLUtil;
	var dialog:Object = new Dialog;
	dialog.caption = util.translate("scripts","Elegir página a imprimir");
	dialog.okButtonText = util.translate("scripts","Aceptar");
	dialog.cancelButtonText = util.translate("scripts","Cancelar");

	var text:Object = new Label;
	text.text = util.translate("scripts","Ha seleccionado un informe de varias páginas,\nelija la página/s a imprimir:");
	dialog.add(text);

	var bgroup:GroupBox = new GroupBox;
	dialog.add( bgroup );

	var imprimirtodas:CheckBox = new CheckBox;
	imprimirtodas.text = util.translate ( "scripts", "Todas" );
	imprimirtodas.checked = true;
	bgroup.add( imprimirtodas );

	var imprimiruna:CheckBox = new CheckBox;
	imprimiruna.text = util.translate ( "scripts", "Página 1" );
	imprimiruna.checked = false;
	bgroup.add( imprimiruna );

	var imprimirdos:CheckBox = new CheckBox;
	imprimirdos.text = util.translate ( "scripts", "Página 2" );
	imprimirdos.checked = false;
	bgroup.add( imprimirdos);

	var imprimirtres:CheckBox = new CheckBox;
	imprimirtres.text = util.translate ( "scripts", "Página 3" );
	imprimirtres.checked = false;
	bgroup.add( imprimirtres);

	var imprimircuatro:CheckBox = new CheckBox;
	imprimircuatro.text = util.translate ( "scripts", "Página 4" );
	imprimircuatro.checked = false;
	bgroup.add( imprimircuatro );

	var imprimircinco:CheckBox = new CheckBox;
	imprimircinco.text = util.translate ( "scripts", "Página 5" );
	imprimircinco.checked = false;
	bgroup.add( imprimircinco );

	if ( !dialog.exec() )
		return;

	var imprimir = new Array(5);

	for (var i:Number = 0; i < 5; i++)
		imprimir[i] = true;

	if (imprimirtodas.checked == false) {
		if(imprimiruna.checked == false)
			imprimir[0] = false;
		if(imprimirdos.checked == false)
			imprimir[1] = false;
		if(imprimirtres.checked == false)
			imprimir[2] = false;
		if(imprimircuatro.checked == false)
			imprimir[3] = false;
		if(imprimircinco.checked == false)
			imprimir[4] = false;
	}

	nombreInforme = "co_modelo390_0";
	for (var i:Number = 1; i < 6; i++){
		if(imprimir[i-1] == true){
			this.iface.lanzar(cursor, nombreInforme + i.toString(), masWhere );
		}
	}
}

//// MODELO 390 /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition modelo349 */
/////////////////////////////////////////////////////////////////
//// MODELO 349 /////////////////////////////////////////////////
/** \D Inicia a cero el contador de operadores del modelo 349
\end */
function modelo349_iniciarOP349(nodo:FLDomNode,campo:String):String
{
	this.iface.numOperador349 = 0;
}

/** \D Devuelve la cadena "Operador" + número del contador de operadores, e incrementa el contador
\end */
function modelo349_siguienteOP349(nodo:FLDomNode,campo:String):String
{
	this.iface.numOperador349++;
	return "Operador " + this.iface.numOperador349;
}

function modelo349_formatoAlfabetico349(texto:String):String
{
        var validos:String = " ,-.ABCDEFGHIJKLMNOPQRSTUVWXYZÇÑ"; /// Se quita la comilla \' por error en mayton

        if (!texto || texto == "") {
                return texto;
        }
        var textoMay:String = this.iface.formatearTexto(texto);
        var resultado:String;
        var iPos:Number;
        var caracter:String;
        var carAnterior:String = "";
        for (var i:Number = 0; i < textoMay.length; i++) {
                caracter = textoMay.charAt(i);
                iPos = validos.find(caracter);
                if (iPos >= 0) {
                        if (!(caracter == " " && (carAnterior == " " || carAnterior == ""))) { /// Evita dos espacios seguidos
                                resultado += caracter;
                                carAnterior = caracter;
                        }
                }
        }
        return resultado;
}

function modelo349_formatoAlfanumerico349(texto:String):String
{
        var validos:String = " &,-./0123456789:;ABCDEFGHIJKLMNOPQRSTUVWXYZ_ÇÑ"; /// Se quita la comilla \' por error en mayton

        if (!texto || texto == "") {
                return texto;
        }
        var textoMay:String = this.iface.formatearTexto(texto);
        var resultado:String;
        var iPos:Number;
        var caracter:String;
        var carAnterior:String = "";
        for (var i:Number = 0; i < textoMay.length; i++) {
                caracter = textoMay.charAt(i);
                iPos = validos.find(caracter);
                if (iPos >= 0) {
                        if (!(caracter == " " && (carAnterior == " " || carAnterior == ""))) { /// Evita dos espacios seguidos
                                resultado += caracter;
                                carAnterior = caracter;
                        }
                }
        }
        return resultado;
}
//// MODELO 349 //////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/** @class_definition modelo347 */
/////////////////////////////////////////////////////////////////
//// MODELO 347 /////////////////////////////////////////////////
/** \D Inicia a cero el contador de declarados del modelo 347
\end */
function modelo347_iniciarDE347(nodo:FLDomNode,campo:String):String
{
	this.iface.numOperador347 = 0;
}

/** \D Devuelve la cadena "Declarado" + número del contador de declarados, e incrementa el contador
\end */
function modelo347_siguienteDE347(nodo:FLDomNode,campo:String):String
{
	this.iface.numOperador347++;
	return "Declarado " + this.iface.numOperador347;
}

/** \D Inicia a cero la variable que suma el importe total de cada hoja en el modelo 347
\end */
function modelo347_iniciarParcial347(nodo:FLDomNode,campo:String):String
{
	this.iface.parcialHoja347 = 0;
debug("iniciando parcial");
}

/** \D Suma a la variable la cantidad correspondiente de cada declarado en el modelo 347
\end */
function modelo347_incrementarParcial347(nodo:FLDomNode,campo:String):String
{
	var importe:String =  nodo.attributeValue("co_modelo347_tipo2d.importe");
	this.iface.parcialHoja347 += parseFloat(importe);
debug("incrementando parcial a " + this.iface.parcialHoja347);
}

/** \D Devuelve el valor del importe total de la hoja
\end */
function modelo347_valorParcial347(nodo:FLDomNode,campo:String):String
{
debug("obteniendo parcial a " + this.iface.parcialHoja347);
	return this.iface.parcialHoja347;
}

function modelo347_formatoAlfabetico347(texto:String):String
{
	var validos:String = " ,-.ABCDEFGHIJKLMNOPQRSTUVWXYZ"; /// Se quita la comilla \' por error en mayton

	if (!texto || texto == "") {
		return texto;
	}
	var textoMay:String = this.iface.formatearTexto(texto);
	var resultado:String;
	var iPos:Number;
	var caracter:String;
	var carAnterior:String = "";
	for (var i:Number = 0; i < textoMay.length; i++) {
		caracter = textoMay.charAt(i);
		iPos = validos.find(caracter);
		if (iPos >= 0) {
			if (!(caracter == " " && (carAnterior == " " || carAnterior == ""))) { /// Evita dos espacios seguidos
				resultado += caracter;
				carAnterior = caracter;
			}
		}
	}
	return resultado;
}

function modelo347_formatoAlfanumerico347(texto:String):String
{
	var validos:String = " &,-./0123456789:;ABCDEFGHIJKLMNOPQRSTUVWXYZ_"; /// Se quita la comilla \' por error en mayton

	if (!texto || texto == "") {
		return texto;
	}
	var textoMay:String = this.iface.formatearTexto(texto);
	var resultado:String;
	var iPos:Number;
	var caracter:String;
	var carAnterior:String = "";
	for (var i:Number = 0; i < textoMay.length; i++) {
		caracter = textoMay.charAt(i);
		iPos = validos.find(caracter);
		if (!(caracter == " " && (carAnterior == " " || carAnterior == ""))) { /// Evita dos espacios seguidos
			resultado += caracter;
			carAnterior = caracter;
		}
	}
	return resultado;
}

//// MODELO 347 /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition modelo340 */
/////////////////////////////////////////////////////////////////
//// MODELO 340 /////////////////////////////////////////////////
function modelo340_init()
{
  var _i = this.iface;
  _i.__init();

  var util: FLUtil = new FLUtil();
  var cursor: FLSqlCursor = new FLSqlCursor("co_identifpaisresidencia");
  cursor.select();
  if (!cursor.first()) {
    var res: Number = MessageBox.information(util.translate("scripts", "Insertar tablas para el modelo 340."), MessageBox.Yes, MessageBox.No);
    if (res != MessageBox.Yes) {
      return false;
    } else {
      _i.rellenarTablasModelo340();
    }
  }
  if (!_i.tablas340_2012()) {
    return false;
  }
  if (!_i.tablas340_2014()) {
    return false;
  }
}

function modelo340_tablas340_2012()
{
  var _i = this.iface;
  if (!AQUtil.sqlSelect("co_claveoperacion", "codigo", "codigo = 'R'")) {
    if (!_i.rellenarTablasModelo340()) {
      return false;
    }
  }
  return true;
}

function modelo340_tablas340_2014()
{
  var _i = this.iface;
  if (!AQUtil.sqlSelect("co_claveoperacion", "codigo", "codigo = 'Z'")) {
    if (!_i.rellenarTablasModelo340()) {
      return false;
    }
  }
  return true;
}


function modelo340_rellenarTablasModelo340()
{
  var util: FLUtil = new FLUtil();
  var cursor: FLSqlCursor = new FLSqlCursor("co_identifpaisresidencia");
  var clavePaisResidencia: Array =
    [["1", "Corresponde a un NIF"], ["2", "Se consigna el NIF/IVA (NIF OPERADOR INTRACOMUNITARIO)"], ["3", "Pasaporte"], ["4", "Documento oficial de identificación expedido por el país o territorio de residencia"], ["5", "Certificado de residencia fiscal"], ["6", "Otro documento probatorio"]];
  for (var i: Number = 0; i < clavePaisResidencia.length; i++) {
    cursor.select("codigo = '" + clavePaisResidencia[i][0] + "'");
    if (cursor.first()) {
      continue;
    }
    with(cursor) {
      setModeAccess(cursor.Insert);
      refreshBuffer();
      setValueBuffer("codigo", clavePaisResidencia[i][0]);
      setValueBuffer("descripcion", clavePaisResidencia[i][1]);
      commitBuffer();
    }
  }

  var cursor: FLSqlCursor = new FLSqlCursor("co_tipolibro");
  var tipoLibro: Array =
    [["E", "Libro registro de facturas expedidas"], ["I", "Libro registro de bienes de inversión"], ["R", "Libro registro de facturas recibidas"], ["U", "Libro registro de determinadas operaciones intracomunitarias"], ["F", "Libro registro de facturas expedidas IGIC"], ["J", "Libro de registro de bienes de inversión IGIC"], ["S", "Libro de registro de facturas recibidas IGIC"]];
  for (var i: Number = 0; i < tipoLibro.length; i++) {
    cursor.select("codigo = '" + tipoLibro[i][0] + "'");
    if (cursor.first()) {
      continue;
    }
    with(cursor) {
      setModeAccess(cursor.Insert);
      refreshBuffer();
      setValueBuffer("codigo", tipoLibro[i][0]);
      setValueBuffer("descripcion", tipoLibro[i][1]);
      commitBuffer();
    }
  }

  var cursor: FLSqlCursor = new FLSqlCursor("co_claveoperacion");
  var claveOperacion: Array =
    [["A", "Asiento resumen de facturas"], ["B", "Asiento resumen de tique"], ["C", "Factura con varios asientos (varios tipos impositivos)"], ["D", "Factura rectificativa"], ["F", "Adquisiciones realizadas por las agencias de viajes directamente en interés del viajero (Régimen especial de agencias de viajes)"], ["G", "Régimen especial de grupo de entidades en IVA o IGIC (Incorpora la contraprestación real a coste)"], ["H", "Régimen especial de oro de inversión"], ["I", "Inversión del sujeto pasivo (ISP)"], ["J", "Tiques"], ["K", "Rectificación de errores registrales"], ["L", "Adquisiciones a comerciantes minoristas del IGIC. Ninguna de las anteriores",], ["R", "Arrendamientos"], ["S", "Subvenciones"], ["T", "Cobros por cuenta de terceros"], ["U", "Seguros"], ["V", "Compras de agencias de viajes"], ["W", "Operaciones sujetas al Impuesto sobre Producción, Servicios y Importación en Ceuta y Melilla"], ["X", "Operaciones por las que empresarios que satisfagan compensaciones agrícolas hayan expedido recibo"], ["Z", "Régimen especial del criterio de caja"], ["1", "IVA criterio de caja. Asiento resumen de facturas"], ["2", "IVA criterio de caja. Factura con varios asientos "], ["3", "IVA criterio de caja. Factura rectificativa"], ["4", "IVA criterio de caja. Adquisiciones realizadas por agencias de viajes..."], ["5", "IVA criterio de caja. Factura simplificada"], ["6", "IVA criterio de caja. Rectificación de errores registrales"], ["7", "IVA criterio de caja. Facturación de  agencias de viaje que actúan como mediadoras..."], ["8", "IVA criterio de caja. Operación de arrendamiento de local de negocio. "]];
  for (var i: Number = 0; i < claveOperacion.length; i++) {
    cursor.select("codigo = '" + claveOperacion[i][0] + "'");
    if (cursor.first()) {
      continue;
    }
    with(cursor) {
      setModeAccess(cursor.Insert);
      refreshBuffer();
      setValueBuffer("codigo", claveOperacion[i][0]);
      setValueBuffer("descripcion", claveOperacion[i][1]);
      commitBuffer();
    }
  }
  var cursor = new FLSqlCursor("co_mediopago340");
  var mediosPago340 = [["C", "Cuenta bancaria"], ["T", "Cheque"], ["O", "Otros medios"]];
  for (var i = 0; i < mediosPago340.length; i++) {
    cursor.select("codigo = '" + mediosPago340[i][0] + "'");
    if (cursor.first()) {
      continue;
    }
    with(cursor) {
      setModeAccess(cursor.Insert);
      refreshBuffer();
      setValueBuffer("codigo", mediosPago340[i][0]);
      setValueBuffer("descripcion", mediosPago340[i][1]);
      commitBuffer();
    }
  }
  return true;
}

function modelo340_beforeCommit_co_claveoperacion(curC)
{
  var _i = this.iface;

  if (!flfactalma.iface.pub_controlDatosMod(curC)) {
    return false;
  }

  return true;
}
function modelo340_formatoNumeroSS(valor, enteros, decimales)
{
  for (var i: Number = 0; i < decimales; i++) {
    valor *= 10;
  }
  var resultado: String = flfactppal.iface.pub_cerosIzquierda(valor, (enteros + decimales));
  return resultado;
}
//// MODELO 340 /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition modelo303 */
/////////////////////////////////////////////////////////////////
//// MODELO 303 /////////////////////////////////////////////////
function modelo303_init()
{
	this.iface.__init();

	var util:FLUtil = new FLUtil;

	if (!util.sqlSelect("co_tipodec303", "idtipodec", "1 = 1")) {
		this.iface.informarTiposDec303();
	}
	this.iface.informarCasillas303();
}

function modelo303_informarTiposDec303()
{
	var curTipoDec:FLSqlCursor = new FLSqlCursor("co_tipodec303");
	var valores:Array = [["C", "Solicitud de compensación"],
		["D", "Devolución"],
		["G", "Cuenta corriente tributaria - ingreso"],
		["I", "Ingreso"],
		["N", "Sin actividad / resultado 0"],
		["V", "Cuenta corriente tributaria - devolución"],
		["U", "Domiciliación de ingreso en CCC"]];

	for (var i:Number = 0; i < valores.length; i++) {
		with (curTipoDec) {
			setModeAccess(Insert);
			refreshBuffer();
			setValueBuffer("idtipodec", valores[i][0]);
			setValueBuffer("descripcion", valores[i][1]);
			commitBuffer();
		}
	}
}

function modelo303_informarCasillas303()
{
	var util:FLUtil = new FLUtil;

	var contenido:String = "<Todos>" +
	"<co_casillas303 casilla='[01]-[03]' descripcion='" + util.translate("scripts", "I.V.A. Devengado - Régimen General (Fila 1)") + "' />" +
	"<co_casillas303 casilla='[04]-[06]' descripcion='" + util.translate("scripts", "I.V.A. Devengado - Régimen General (Fila 2)") + "' />" +
	"<co_casillas303 casilla='[07]-[09]' descripcion='" + util.translate("scripts", "I.V.A. Devengado - Régimen General (Fila 3)") + "' />" +
	"<co_casillas303 casilla='[01]-[09]' descripcion='" + util.translate("scripts", "I.V.A. Devengado - Régimen General (Distribución por porcentaje de IVA)") + "' />" +
	"<co_casillas303 casilla='[10]-[11]' descripcion='" + util.translate("scripts", "Adquisiciones intracomunitarias de bienes y servicios") + "' />" +
	"<co_casillas303 casilla='[12]-[13]' descripcion='" + util.translate("scripts", "Otras operaciones con inversión del sujeto pasivo (excepto adq. intracom.") + "' />" +
	"<co_casillas303 casilla='[14]-[15]' descripcion='" + util.translate("scripts", "I.V.A. Devengado Adquisiciones intracomunitarias") + "' />" +
	"<co_casillas303 casilla='[16]-[24]' descripcion='" + util.translate("scripts", "I.V.A. Devengado Recargo de equivalencia Régimen General") + "' />" +
	"<co_casillas303 casilla='[25]-[26]' descripcion='" + util.translate("scripts", "Modificación de bases y cuotas del recargo de equivalencia") + "' />" +
	"<co_casillas303 casilla='[28]-[29]' descripcion='" + util.translate("scripts", "I.V.A. Deducible por cuotas soportadas en operaciones interiores con bienes corrientes") + "' />" +
	"<co_casillas303 casilla='[30]-[31]' descripcion='" + util.translate("scripts", "I.V.A. Deducible por cuotas soportadas en operaciones interiores con bienes de inversión") + "' />" +
	"<co_casillas303 casilla='[32]-[33]' descripcion='" + util.translate("scripts", "I.V.A. Deducible por cuotas soportadas en importaciones de bienes corrientes") + "' />" +
	"<co_casillas303 casilla='[34]-[35]' descripcion='" + util.translate("scripts", "I.V.A. Deducible por cuotas soportadas en importaciones de bienes de inversión") + "' />" +
	"<co_casillas303 casilla='[36]-[37]' descripcion='" + util.translate("scripts", "I.V.A. Deducible por cuotas soportadas en adquisiciones intracomunitarias de bienes corrientes") + "' />" +
	"<co_casillas303 casilla='[38]-[39]' descripcion='" + util.translate("scripts", "I.V.A. Deducible por cuotas soportadas en adquisiciones intracomunitarias de bienes de inversión") + "' />" +
	"<co_casillas303 casilla='[40]-[41]' descripcion='" + util.translate("scripts", "Rectificación de deducciones") + "' />" +
	"<co_casillas303 casilla='[42]' descripcion='" + util.translate("scripts", "I.V.A. Deducible por compensaciones de regimen especial A.G.y P.") + "' />" +
	"<co_casillas303 casilla='[43]' descripcion='" + util.translate("scripts", "Regularización bienes inversión") + "' />" +
	"<co_casillas303 casilla='[44]' descripcion='" + util.translate("scripts", "Regularización por aplicación del porcentaje definitivo de prorrata") + "' />" +
	"<co_casillas303 casilla='[59]' descripcion='" + util.translate("scripts", "Entregas intracomunitarias") + "' />" +
	"<co_casillas303 casilla='[60]' descripcion='" + util.translate("scripts", "Exportaciones y operaciones asimilables") + "' />" +
	"<co_casillas303 casilla='[61]' descripcion='" + util.translate("scripts", "Operaciones no sujetas o con inversión del sujeto pasivo que originan derecho a deducción") + "' />" +
	"</Todos>";

	xmlDoc = new FLDomDocument();
	if (!xmlDoc.setContent(contenido)) {
debug("!xmlDoc.setContent(contenido)");
		return false;
	}
	var xmlOD:FLDomNodeList = xmlDoc.elementsByTagName("co_casillas303");
	var eOD:FLDomElement;
	var curCasillas:FLSqlCursor = new FLSqlCursor("co_casillas303");
	for (var i:Number = 0; i < xmlOD.length(); i++) {
		eOD = xmlOD.item(i).toElement();
		curCasillas.setModeAccess(curCasillas.Insert);
		curCasillas.refreshBuffer();
		if (util.sqlSelect("co_casillas303", "casilla303", "casilla303 = '" + eOD.attribute("casilla") + "'")) {
			continue;
		}
		curCasillas.setValueBuffer("casilla303", eOD.attribute("casilla"));
		curCasillas.setValueBuffer("descripcion", eOD.attribute("descripcion"));
		if (!curCasillas.commitBuffer()) {
			return false;
		}
	}
	return true;
}

//// MODELO 303 /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition modelo180 */
/////////////////////////////////////////////////////////////////
//// MODELO 180 /////////////////////////////////////////////////
function modelo180_init()
{
	this.iface.__init();

	var util:FLUtil = new FLUtil;

	if (!util.sqlSelect("co_tipodec180", "idtipodec", "1 = 1")) {
		this.iface.informarTiposDec180();
	}
}

function modelo180_informarTiposDec180()
{
	var curTipoDec:FLSqlCursor = new FLSqlCursor("co_tipodec180");
	var valores:Array = [["G", "Cuenta corriente tributaria-ingreso"], ["I", "Ingreso"], ["N", "Negativa"], ["U", "Domiciliación del ingreso en CCC"]];

	for (var i:Number = 0; i < valores.length; i++) {
		with (curTipoDec) {
			setModeAccess(Insert);
			refreshBuffer();
			setValueBuffer("idtipodec", valores[i][0]);
			setValueBuffer("descripcion", valores[i][1]);
			commitBuffer();
		}
	}
}

//// MODELO 180 /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition modelo115 */
/////////////////////////////////////////////////////////////////
//// MODELO 115 /////////////////////////////////////////////////
function modelo115_init()
{
	this.iface.__init();

	var util:FLUtil = new FLUtil;

	if (!util.sqlSelect("co_tipodec115", "idtipodec", "1 = 1")) {
		this.iface.informarTiposDec115();
	}
}

function modelo115_informarTiposDec115()
{
	var curTipoDec:FLSqlCursor = new FLSqlCursor("co_tipodec115");
	var valores:Array = [["G", "Cuenta corriente tributaria-ingreso"], ["I", "Ingreso"], ["N", "Negativa"], ["U", "Domiciliación del ingreso en CCC"]];

	for (var i:Number = 0; i < valores.length; i++) {
		with (curTipoDec) {
			setModeAccess(Insert);
			refreshBuffer();
			setValueBuffer("idtipodec", valores[i][0]);
			setValueBuffer("descripcion", valores[i][1]);
			commitBuffer();
		}
	}
}

//// MODELO 115 /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition boe2011 */
/////////////////////////////////////////////////////////////////
//// BOE2011 ///////////////////////////////////////////////////

function boe2011_init()
{
    this.iface.__init();

    var util:FLUtil = new FLUtil();
    var totalClaves = util.sqlSelect("co_claveoperacion","count(codigo)","1=1");
    if (totalClaves != 24) {
        this.iface.rellenarTablaMod340ClaveOp();
    }

    this.iface.xGesteso = this.iface.validarExtension("gestesoreria");
    this.iface.xC0 = this.iface.validarExtension("column0");
    this.iface.xMulti = this.iface.validarExtension("multiempresa");

}

function boe2011_rellenarTablaMod340ClaveOp()
{
    var util:FLUtil = new FLUtil();

    var cursor:FLSqlCursor = new FLSqlCursor("co_claveoperacion");
    var claveOperacion:Array =
        [
        ["A", "Asiento resumen de facturas"],["B", "Asiento resumen de tique"],["C", "Factura con varios asientos (varios tipos impositivos)"],["D", "Factura rectificativa"],["F", "Adquisiciones realizadas por las agencias de viajes directamente en interés del viajero (Régimen especial de agencias de viajes)"],["G", "Régimen especial de grupo de entidades en IVA o IGIC (Incorpora la contraprestación real a coste)"],["H", "Régimen especial de oro de inversión"],["I", "Inversión del sujeto pasivo (ISP)"],["J", "Tiques"],["K", "Rectificación de errores registrales"],["L", "Adquisiciones a comerciantes minoristas del IGIC"],[" ","Ninguna de las anteriores"],["E","IVA/IGIC devengado pendiente de emitir factura"],["M","IVA/IGIC facturado pendiente de devengar (emitida factura)"],["N","Facturación de las prestaciones de servicios de agencias de viaje que actuan como mediadoras en nombre y por cuenta ajena (disposición adicional 4a RD 1496/2003)"],["O", "Factura emitida en sustición de tiques facturados y declarados"
],["P", "Adquisiciones intracomunitarias de bienes"],["Q", "Operaciones en las que se aplique el régimen especial de bienes usados,objetos de arte,antigüedades y objetos de colección según los artículos del 135 al 139 de la Ley 37/1992 de 28 de diciembre del Impuesto sobre el Valor Añadido"],["R", "Operación de arrendamiento de local de negocio"],["S", "Subvenciones, auxilios o ayudas satisfechas o recibidas, tanto por parte de administraciones públicas como de entidades privadas"],["T", "Cobros por cuenta de terceros de honorarios profesionales o de derechos derivados de la propiedad intelectual, industrial, de autor u otros por cuenta de sus socios, asociados o colegiados efectuados por sociedades, asociaciones, colegios profesionales u otras entidades que, entre sus funciones, realicen las de cobro"],["U", "Operación de seguros"],["V", "compras de agengias de viajes: operaciones de prestación de servicios de mediación en nombre y por cuenta ajena relativos a los servicios de transporte de viajeros y de "
+"sus equipajes que las agencias de viajes presten al destinatario de dichos servicios de transporte, de acuerdo con lo dispuesto en el apartado 3 de la disposición adicional cuarta del reglamento por el que se regulan las obligaciones de facturación"],["W", "Oparaciones sujetas al Impuesto sobre la Producción, los Servicios y la Importación en las Ciudades de Ceuta y Melilla"],["X", "Operaciones por las que los empresarios o profesionales que satisfagan compensaciones agrícolas, ganaderas y/o pesqueras hayan expedido el recibo correspondiente"]
        ];

    for (var i:Number = 0; i < claveOperacion.length; i++) {
        var existe = util.sqlSelect("co_claveoperacion","codigo","codigo='"+claveOperacion[i][0]+"'");
        if (!existe) {
            cursor.setModeAccess(cursor.Insert);
            cursor.refreshBuffer();
            cursor.setValueBuffer("codigo", claveOperacion[i][0]);
            cursor.setValueBuffer("descripcion", claveOperacion[i][1]);
            cursor.commitBuffer();
        }
    }

}

function boe2011_aplicarFormato(formatoCampo:String,valorCampo:String,nombreCampo:String,longitudCampo:Number):String
{
    switch(formatoCampo){
        case "N":
        //Tipo = Numerico.
            valorCampo = parseFloat(valorCampo);
            valorCampo = flfactppal.iface.pub_cerosIzquierda(valorCampo, longitudCampo);
            break;

        case "A":
        //Tipo = Alfanumerico.
        case "T":
        //Tipo = Texto
            var regExp1:RegExp = new RegExp( "^ +" );
            regExp1.global = true;
            valorCampo = valorCampo.replace(regExp1,"");
            valorCampo = valorCampo.toUpperCase();
            var regExp2:RegExp = new RegExp( " +$" );
            regExp2.global = true;
            var regExp2:RegExp = new RegExp("  ");
            regExp2.global = true;
            valorCampo = valorCampo.replace(regExp2,"");
            valorCampo = flfactppal.iface.pub_espaciosDerecha(valorCampo, longitudCampo);
            break;

        case "C":
        //Tipo = Alfanumérico relleno a ceros en cambio de espacios en blanco, utilizado para cifnif y cifnif replegal
            var regExp1:RegExp = new RegExp( "^ +" );
            regExp1.global = true;
            valorCampo = valorCampo.replace(regExp1,"");
            valorCampo = valorCampo.toUpperCase();
            var regExp2:RegExp = new RegExp( " +$" );
            regExp2.global = true;
            valorCampo = valorCampo.replace(regExp2,"");
            if (valorCampo !="") {
                valorCampo = flfactppal.iface.pub_cerosIzquierda(valorCampo, longitudCampo);
            } else {
                valorCampo = flfactppal.iface.pub_espaciosDerecha(valorCampo, longitudCampo);
            }
            break;

        case "B":
        //Tipo = Blancos
            valorCampo = flfactppal.iface.pub_espaciosDerecha(valorCampo, longitudCampo);
            break;

        default:
        //Cualquier otro tipo.
            break;
    }

    return valorCampo;
}

function boe2011_validarFormato(formatoCampo:String,valorCampo:String,nombreCampo:String,longitudCampo:Number):Boolean
{
    var regExp1:RegExp;
    var valido:Number;
    switch(formatoCampo){
        case "N": regExp1 = new RegExp( "^[0-9]+$" );  break;
        case "A": regExp1 = new RegExp( "^[0-9A-ZÑÇ ,\\.:;-&]+$" ); break;
        case "T": regExp1 = new RegExp( "^[A-ZÑÇ ,\\.:;-&]+$" ); break;
        case "B": regExp1 = new RegExp( "^[ ]+$" ); break;
    }

    valido = valorCampo.find(regExp1);

    if(valido<0) {
        debug("valorCampo = ["+valorCampo+"] + valido = ["+valido+"]");
        debug("Campo "+nombreCampo+" , formato {"+formatoCampo+"} no cumple RegExp {"+regExp1+"}");
        return false;
    }

    if (valorCampo.length != longitudCampo) {
         debug("nombreCampo = ["+nombreCampo+"] + valorCampo = ["+valorCampo+"]");
         debug("Error de longitud = Campo: ["+valorCampo.length+"] / formato = ["+longitudCampo+"]");
        return false;
    }

    return true;
}

function boe2011_desRegistro347(codReg:String):Array
{
    var ret = [];
    //  [REGISTRO  POSICION  LONGITUD   TIPO]
    /*  TIPO:   N : NUMERICO
     *          A : ALFANUMERICO
     *          T : ALFABETICO (TEXTO)
     *          B : ESPACIOS EN BLANCO
     *          C : ALFANUMERICO RELLENO DE CEROS HASTA LONGITUD
    */

    switch (codReg) {

    /** \D Registro de declarante \end */
    case "1":
        ret =   [
                ["tiporeg",             1,      1,      "N" ],
                ["modelo",              2,      3,      "N" ],
                ["ejercicio",           5,      4,      "N" ],
                ["cifnif",              9,      9,      "C" ],
                ["apellidosnombrers",   18,     40,     "A" ],
                ["tiposoporte",         58,     1,      "T" ],
                ["telefono",            59,     9,      "N" ],
                ["contacto",            68,     40,     "A" ],
                ["justificante",        108,    13,     "N" ],
                ["complementaria",      121,    1,      "T" ],
                ["sustitutiva",         122,    1,      "T" ],
                ["jusanterior",         123,    13,     "N" ],
                ["totalentidades",      136,    9,      "N" ],
                ["signo",               145,    1,      "T" ],
                ["importetotal",        146,    15,     "N" ],
                ["totalinmuebles",      161,    9,      "N" ],
                ["totalarrendamiento",  170,    15,     "N" ],
                ["blancos",             185,    206,    "B" ],
                ["nifreplegal",         391,    9,      "C" ],
                ["blancos2",            400,    88,     "B" ],
                ["sello",               488,    13,     "B" ]
                ];
      break;

    case "2d":
      /** \D Registro de declarados \end */
        ret =   [
                ["tiporeg",             1,      1,      "N" ],
                ["modelo",              2,      3,      "N" ],
                ["ejercicio",           5,      4,      "N" ],
                ["cifnif",              9,      9,      "C" ],
                ["nifdeclarado",        18,     9,      "C" ],
                ["nifreplegal",         27,     9,      "C" ],
                ["apellidosnombrers",   36,     40,     "A" ],
                ["tipohoja",            76,     1,      "T" ],
                ["codprovincia",        77,     2,      "N" ],
                ["codpais",             79,     2,      "T" ],
                ["blancos",             81,     1,      "B" ],
                ["clavecodigo",         82,     1,      "T" ],
                ["signo",               83,     1,      "T" ],
                ["importe",             84,     15,     "N" ],
                ["seguro",              99,     1,      "T" ],
                ["arrendlocal",         100,    1,      "T" ],
                ["importemetalico",     101,    15,     "N" ],
                ["signoinmuebles",      116,    1,      "T" ],
                ["importeinmuebles",    117,    15,     "N" ],
                ["ejerciciometalico",   132,    4,      "N" ],
                ["signo1t",             136,    1,      "T" ],
                ["importe1t",           137,    15,     "N" ],
                ["signoinmuebles1t",    152,    1,      "T" ],
                ["importeinmuebles1t",  153,    15,     "N" ],
                ["signo2t",             168,    1,      "T" ],
                ["importe2t",           169,    15,     "N" ],
                ["signoinmuebles2t",    184,    1,      "T" ],
                ["importeinmuebles2t",  185,    15,     "N" ],
                ["signo3t",             200,    1,      "T" ],
                ["importe3t",           201,    15,     "N" ],
                ["signoinmuebles3t",    216,    1,      "T" ],
                ["importeinmuebles3t",  217,    15,     "N" ],
                ["signo4t",             232,    1,      "T" ],
                ["importe4t",           233,    15,     "N" ],
                ["signoinmuebles4t",    248,    1,      "T" ],
                ["importeinmuebles4t",  249,    15,     "N" ],
                ["blancos2",            264,    237,    "B" ]
                ];
        break;

      /** \D Registro de inmuebles \end */
    case "2i":
        ret =   [
                ["tiporeg",             1,      1,      "N" ],
                ["modelo",              2,      3,      "N" ],
                ["ejercicio",           5,      4,      "N" ],
                ["cifnif",              9,      9,      "C" ],
                ["nifarrendatario",     18,     9,      "C" ],
                ["nifreplegal",         27,     9,      "C" ],
                ["apellidosnombrers",   36,     40,     "A" ],
                ["tipohoja",            76,     1,      "T" ],
                ["blancos",             77,     23,     "B" ],
                ["importe",             100,    15,     "N" ],
                ["situacion",           115,    1,      "T" ],
                ["refcatastral",        116,    25,     "A" ],
                ["codtipovia",          141,    5,      "T" ],
                ["nombrevia",           146,    50,     "A" ],
                ["tiponumeracion",      196,    3,      "A" ],
                ["numero",              199,    5,      "N" ],
                ["califnumero",         204,    3,      "A" ],
                ["bloque",              207,    3,      "A" ],
                ["portal",              210,    3,      "A" ],
                ["escalera",            213,    3,      "A" ],
                ["piso",                216,    3,      "A" ],
                ["puerta",              219,    3,      "A" ],
                ["complemento",         222,    40,     "A" ],
                ["localidad",           262,    30,     "A" ],
                ["municipio",           292,    30,     "A" ],
                ["codmunicipio",        322,    5,      "A" ],
                ["codprovincia",        327,    2,      "N" ],
                ["codpostal",           329,    5,      "N" ],
                ["blancos2",            334,    167,    "B" ]
                ];
      break;
    }

  return ret;
}

function boe2011_desRegistro340(codReg:String):Array
{
    var ret = [];
    //  [REGISTRO  POSICION  LONGITUD   TIPO]
    /*  TIPO:   N : NUMERICO
     *          A : ALFANUMERICO
     *          T : ALFABETICO (TEXTO)
     *          B : ESPACIOS EN BLANCO
    */

    switch (codReg) {

    /** \D Registro de declarante \end */
    case "1":
        ret =   [
                ["tiporeg",             1,      1,      "N",    "F" ],
                ["modelo",              2,      3,      "N",    "F" ],
                ["ejercicio",           5,      4,      "N",    "F" ],
                ["cifnif",              9,      9,      "C",    "F" ],
                ["apellidosnombrers",   18,     40,     "A",    "F" ],
                ["tiposoporte",         58,     1,      "T",    "F" ],
                ["telefono",            59,     9,      "N",    "F" ],
                ["contacto",            68,     40,     "A",    "F" ],
                ["numidentificativo",   108,    13,     "N",    "F" ],
                ["complementaria",      121,    1,      "T",    "F" ],
                ["sustitutiva",         122,    1,      "T",    "F" ],
                ["jusanterior",         123,    13,     "N",    "F" ],
                ["periodo",             136,    2,      "N",    "F" ],
                ["registros",           138,    9,      "N",    "F" ],
                ["sbaseimponible",      147,    1,      "T",    "F" ],
                ["baseimponible",       148,    17,     "N",    "T" ],
                ["scuotaimpuesto",      165,    1,      "T",    "F" ],
                ["cuotaimpuesto",       166,    17,     "N",    "T" ],
                ["stotalfacturas",      183,    1,      "T",    "F" ],
                ["totalfacturas",       184,    17,     "N",    "T" ],
                ["blancos",             201,    190,    "B",    "F" ],
                ["cifnifrepres",        391,    9,      "C",    "F" ],
                ["codigoelectronico",   400,    16,     "B",    "F" ],
                ["blancos",             416,    85,     "B",    "F" ]
                ];
      break;

    case "2e":
      /** \D Registro de declarado facturas emitidas \end */
        ret =   [
                ["tiporeg",             1,      1,      "N",    "F" ],
                ["modelo",              2,      3,      "N",    "F" ],
                ["ejercicio",           5,      4,      "N",    "F" ],
                ["cifnif",              9,      9,      "C",    "F" ],
                ["nifdeclarado",        18,     9,      "C",    "F" ],
                ["cifnifrp",            27,     9,      "C",    "F" ],
                ["apellidosnomrs",      36,     40,     "A",    "F" ],
                ["codpais",             76,     2,      "T",    "F" ],
                ["claveidentificacion", 78,     1,      "N",    "F" ],
                ["numidentificacion",   79,     20,     "A",    "F" ],
                ["tipolibro",           99,     1,      "T",    "F" ],
                ["operacion",           100,    1,      "T",    "F" ],
                ["fechaexpedicion",     101,    8,      "N",    "F" ],
                ["fechaoperacion",      109,    8,      "N",    "F" ],
                ["tipoimpositivo",      117,    5,      "N",    "T" ],
                ["sbaseimponible",      122,    1,      "T",    "F" ],
                ["baseimponible",       123,    13,     "N",    "T" ],
                ["scuotaimpuesto",      136,    1,      "T",    "F" ],
                ["cuotaimpuesto",       137,    13,     "N",    "T" ],
                ["simportetotal",       150,    1,      "T",    "F" ],
                ["importetotal",        151,    13,     "N",    "T" ],
                ["sbaseimponiblecoste", 164,    1,      "T",    "F" ],
                ["baseimponiblecoste",  165,    13,     "N",    "T" ],
                ["idenfactura",         178,    40,     "A",    "F" ],
                ["numregistro",         218,    18,     "A",    "F" ],
                ["numfacturas",         236,    8,      "N",    "F" ],
                ["desgloseregistro",    244,    2,      "N",    "F" ],
                ["intervidentif",       246,    40,     "A",    "F" ],
                ["intervidentif2",      286,    40,     "A",    "F" ],
                ["identfacturarect",    326,    40,     "A",    "F" ],
                ["tiporecequi",         366,    5,      "N",    "T" ],
                ["scuotarecequi",       371,    1,      "T",    "F" ],
                ["cuotarecequi",        372,    13,     "N",    "T" ],
                ["situacioninmueble",   385,    1,      "N",    "F" ],
                ["refcatastral",        386,    25,     "A",    "F" ],
                ["importemetalico",     411,    15,     "N",    "T" ],
                ["ejerciciometalico",   426,    4,      "N",    "F" ],
                ["importeinmuebles",    430,    15,     "N",    "T" ],
                ["blancos",             445,    56,      "B",     "F" ]
                ];
        break;

    case "2r":
      /** \D Registro de declarado facturas recibidas \end */
        ret =   [
                ["tiporeg",             1,      1,      "N",    "F" ],
                ["modelo",              2,      3,      "N",    "F" ],
                ["ejercicio",           5,      4,      "N",    "F" ],
                ["cifnif",              9,      9,      "C",    "F" ],
                ["nifdeclarado",        18,     9,      "C",    "F" ],
                ["cifnifrp",            27,     9,      "C",    "F" ],
                ["apellidosnomrs",      36,     40,     "A",    "F" ],
                ["codpais",             76,     2,      "T",    "F" ],
                ["claveidentificacion", 78,     1,      "N",    "F" ],
                ["numidentificacion",   79,     20,     "A",    "F" ],
                ["tipolibro",           99,     1,      "T",    "F" ],
                ["operacion",           100,    1,      "T",    "F" ],
                ["fechaexpedicion",     101,    8,      "N",    "F" ],
                ["fechaoperacion",      109,    8,      "N",    "F" ],
                ["tipoimpositivo",      117,    5,      "N",    "T" ],
                ["sbaseimponible",      122,    1,      "T",    "F" ],
                ["baseimponible",       123,    13,     "N",    "T" ],
                ["scuotaimpuesto",      136,    1,      "T",    "F" ],
                ["cuotaimpuesto",       137,    13,     "N",    "T" ],
                ["simportetotal",       150,    1,      "T",    "F" ],
                ["importetotal",        151,    13,     "N",    "T" ],
                ["sbaseimponiblecoste", 164,    1,      "T",    "F" ],
                ["baseimponiblecoste",  165,    13,     "N",    "T" ],
                ["idenfactura",         178,    40,     "A",    "F" ],
                ["numregistro",         218,    18,     "A",    "F" ],
                ["numfacturas",         236,    18,     "N",    "F" ],
                ["desgloseregistro",    254,    2,      "N",    "F" ],
                ["intervidentif",       256,    40,     "A",    "F" ],
                ["intervidentif2",      296,    40,     "A",    "F" ],
                ["scuotadeducible",     336,    1,      "T",    "F" ],
                ["cuotadeducible",      337,    13,     "N",    "T" ],
                ["blancos",             350,    151,    "B",    "F" ]
                ];
        break;

    case "2b":
      /** \D Registro de declarado bienes de inversion \end */
        ret =   [
                ["tiporeg",             1,      1,      "N",    "F" ],
                ["modelo",              2,      3,      "N",    "F" ],
                ["ejercicio",           5,      4,      "N",    "F" ],
                ["cifnif",              9,      9,      "C",    "F" ],
                ["nifdeclarado",        18,     9,      "C",    "F" ],
                ["cifnifrp",            27,     9,      "C",    "F" ],
                ["apellidosnomrs",      36,     40,     "A",    "F" ],
                ["codpais",             76,     2,      "T",    "F" ],
                ["claveidentificacion", 78,     1,      "N",    "F" ],
                ["numidentificacion",   79,     20,     "A",    "F" ],
                ["tipolibro",           99,     1,      "T",    "F" ],
                ["operacion",           100,    1,      "T",    "F" ],
                ["fechaexpedicion",     101,    8,      "N",    "F" ],
                ["fechaoperacion",      109,    8,      "N",    "F" ],
                ["tipoimpositivo",      117,    5,      "N",    "T" ],
                ["sbaseimponible",      122,    1,      "T",    "F" ],
                ["baseimponible",       123,    13,     "N",    "T" ],
                ["scuotaimpuesto",      136,    1,      "T",    "F" ],
                ["cuotaimpuesto",       137,    13,     "N",    "T" ],
                ["simportetotal",       150,    1,      "T",    "F" ],
                ["importetotal",        151,    13,     "N",    "T" ],
                ["sbaseimponiblecoste", 164,    1,      "T",    "F" ],
                ["baseimponiblecoste",  165,    13,     "N",    "T" ],
                ["idenfactura",         178,    40,     "A",    "F" ],
                ["numregistro",         218,    18,     "A",    "F" ],
                ["prorrata",            236,    3,      "N",    "F" ],
                ["sreganual",           239,    1,      "T",    "F" ],
                ["reganual",            240,    13,     "N",    "T" ],
                ["idententrega",        253,    40,     "A",    "F" ],
                ["sreganualefect",      293,    1,      "T",    "F" ],
                ["reganualefect",       294,    13,     "N",    "T" ],
                ["fechautilizacion",    307,    8,      "N",    "F" ],
                ["identbien",           315,    17,     "A",    "F" ],
                ["blancos",             332,    169,    "B",    "F" ]
                ];
        break;

    case "2i":
      /** \D Registro de declarado de determinadas operaciones intracomunitarias \end */
        ret =   [
                ["tiporeg",             1,      1,      "N",    "F" ],
                ["modelo",              2,      3,      "N",    "F" ],
                ["ejercicio",           5,      4,      "N",    "F" ],
                ["cifnif",              9,      9,      "C",    "F" ],
                ["nifdeclarado",        18,     9,      "C",    "F" ],
                ["cifnifrp",            27,     9,      "C",    "F" ],
                ["apellidosnomrs",      36,     40,     "A",    "F" ],
                ["codpais",             76,     2,      "T",    "F" ],
                ["claveidentificacion", 78,     1,      "N",    "F" ],
                ["numidentificacion",   79,     20,     "A",    "F" ],
                ["tipolibro",           99,     1,      "T",    "F" ],
                ["operacion",           100,    1,      "T",    "F" ],
                ["fechaexpedicion",     101,    8,      "N",    "F" ],
                ["fechaoperacion",      109,    8,      "N",    "F" ],
                ["tipoimpositivo",      117,    5,      "N",    "T" ],
                ["sbaseimponible",      122,    1,      "T",    "F" ],
                ["baseimponible",       123,    13,     "N",    "T" ],
                ["scuotaimpuesto",      136,    1,      "T",    "F" ],
                ["cuotaimpuesto",       137,    13,     "N",    "T" ],
                ["simportetotal",       150,    1,      "T",    "F" ],
                ["importetotal",        151,    13,     "N",    "T" ],
                ["sbaseimponiblecoste", 164,    1,      "T",    "F" ],
                ["baseimponiblecoste",  165,    13,     "N",    "T" ],
                ["idenfactura",         178,    40,     "A",    "F" ],
                ["numregistro",         218,    18,     "A",    "F" ],
                ["tipoopintra",         236,    1,      "T",    "F" ],
                ["clavedeclarado",      237,    1,      "T",    "F" ],
                ["codestadomiembro",    238,    2,      "A",    "F" ],
                ["plazooperacion",      240,    3,      "N",    "F" ],
                ["descripcion",         243,    35,     "A",    "F" ],
                ["domicilio",           278,    40,     "A",    "F" ],
                ["poblacion",           318,    22,     "A",    "F" ],
                ["codpostal",           340,    10,     "A",    "F" ],
                ["otrasfact",           350,    135,    "A",    "F" ],
                ["blancos",             485,    16,     "B",    "F" ]
                ];
        break;
    }

  return ret;
}

/** El modelo 349 no se modifica en el boletin oficial del 2011, pero se agregan cambios en esta clase como mejora para la generación del registro a presentar */
function boe2011_desRegistro349(codReg:String):Array
{
    var ret = [];
    //  [REGISTRO  POSICION  LONGITUD   TIPO]
    /*  TIPO:   N : NUMERICO
     *          A : ALFANUMERICO
     *          T : ALFABETICO (TEXTO)
     *          B : ESPACIOS EN BLANCO
     *          C : ALFANUMERICO RELLENO DE CEROS HASTA LONGITUD
    */

    switch (codReg) {

    /** \D Registro de declarante \end */
    case "1":
        ret =   [
                ["tiporeg",             1,      1,      "N" ],
                ["modelo",              2,      3,      "N" ],
                ["ejercicio",           5,      4,      "N" ],
                ["cifnifpres",          9,      9,      "C" ],
                ["nombrepres",          18,     40,     "A" ],
                ["tiposoporte",         58,     1,      "T" ],
                ["telefonorel",         59,     9,      "N" ],
                ["personarel",          68,     40,     "A" ],
                ["numjustificante",     108,    13,     "N" ],
                ["complementaria",      121,    1,      "T" ],
                ["sustitutiva",         122,    1,      "T" ],
                ["jusanterior",         123,    13,     "N" ],
                ["periodo",             136,    2,      "A" ],
                ["numtotaloi",          138,    9,      "N" ],
                ["importetotaloi",      147,    15,     "N" ],
                ["numtotaloirec",       162,    9,      "N" ],
                ["importetotaloirec",   171,    15,     "N" ],
                ["cambioperiodicidad",  186,    1,      "T" ],
                ["blancos",             187,    204,    "B" ],
                ["cifnifreplegal",      391,    9,      "C" ],
                ["blancos2",            400,    88,     "B" ],
                ["sello",               488,    13,     "B" ]
                ];
      break;

    case "2":
      /** \D Registro de declarados \end */
        ret =   [
                ["tiporeg",             1,      1,      "N" ],
                ["modelo",              2,      3,      "N" ],
                ["ejercicio",           5,      4,      "N" ],
                ["cifnifpres",          9,      9,      "C" ],
                ["blancos",             18,     58,     "B" ],
                ["codue",               76,     2,      "T" ],
                ["cifnif",              78,     15,     "A" ],
                ["nombre",              93,     40,     "A" ],
                ["clave",               133,    1,      "T" ],
                ["baseimponible",       134,    13,     "N" ],
                ["blancos2",            147,    354,    "B" ]
                ];
        break;

    case "2r":
      /** \D Registro de rectificaciones \end */
        ret =   [
                ["tiporeg",             1,      1,      "N" ],
                ["modelo",              2,      3,      "N" ],
                ["ejercicio",           5,      4,      "N" ],
                ["cifnifpres",          9,      9,      "C" ],
                ["blancos",             18,     58,     "B" ],
                ["codue",               76,     2,      "T" ],
                ["cifnif",              78,     15,     "A" ],
                ["nombre",              93,     40,     "A" ],
                ["clave",               133,    1,      "T" ],
                ["blancos2",            134,    13,     "B" ],
                ["codejercicio",        147,    4,      "N" ],
                ["periodo",             151,    2,      "A" ],
                ["bianterior",          153,    13,     "N" ],
                ["bianterior",          166,    13,     "N" ],
                ["blancos3",            179,    322,    "B" ]
                ];
        break;
    }

  return ret;
}

function boe2011_generarRegistro(desReg:Array,registro:Object):String {

    var contenidoReg:String="";
    var longReg:Number = 0;
    var tipoReg:Number = registro["tiporeg"];

    var nombreCampo:String = "";
    var posIni:Number = 0;
    var longitudCampo:Number = 0;
    var formatoCampo:String="";
    var valorCampo;

    for (var i = 0; i < desReg.length; i++) {
        nombreCampo = desReg[i][0];
        posIni = desReg[i][1];
        longitudCampo = desReg[i][2];
        formatoCampo = desReg[i][3];
        valorCampo = registro[nombreCampo].toString();

        if ((contenidoReg.length + 1) != posIni) {
            this.iface.error += "Registro tipo "+tipoReg+" - Campo:"+nombreCampo+" - Valor :"+valorCampo+" - Error de longitud, No empieza en posición "+posIni+"\n";
        }

        debug("1 Tiporeg["+tipoReg+"] - "+nombreCampo+"["+valorCampo+"] - PosIni["+(contenidoReg.length + 1)+"] - Longitud["+valorCampo.length+"]");

        valorCampo = this.iface.aplicarFormato(formatoCampo,valorCampo,nombreCampo,longitudCampo);

        if(!this.iface.validarFormato(formatoCampo,valorCampo,nombreCampo,longitudCampo)) {
            this.iface.error += "Registro tipo "+tipoReg+" - Campo:"+nombreCampo+" - Valor :"+valorCampo+" - Error de formato\n";
        }

        debug("2 Tiporeg["+tipoReg+"] - "+nombreCampo+"["+valorCampo+"] - PosIni["+(contenidoReg.length + 1)+"] - Longitud["+valorCampo.length+"]");

        contenidoReg += valorCampo;
        longReg = (posIni+longitudCampo)-1;
    }

    if (contenidoReg.length != longReg) {
        this.iface.error += "Registro tipo "+tipoReg+" - Error de longitud de registro";
    }

    return contenidoReg;
}

function boe2011_generarCSV(desReg:Array,registro:Object):String {

    var contenidoReg:String;
    var longReg:Number = 0;
    var tipoReg:Number = registro["tiporeg"];

    var nombreCampo:String = "";
    var posIni:Number = 0;
    var longitudCampo:Number = 0;
    var formatoCampo:String="";
    var compuesto:String ="";
    var valorCampo;

    for (var i = 0; i < desReg.length; i++) {
        nombreCampo = desReg[i][0];
        posIni = desReg[i][1];
        longitudCampo = desReg[i][2];
        formatoCampo = desReg[i][3];
        compuesto = desReg[i][4];
        valorCampo = registro[nombreCampo];

        valorCampo = this.iface.aplicarFormato(formatoCampo,valorCampo,nombreCampo,longitudCampo);

        if(!this.iface.validarFormato(formatoCampo,valorCampo,nombreCampo,longitudCampo)) {
            this.iface.error += "Registro tipo "+tipoReg+" - Campo:"+nombreCampo+" - Valor :"+valorCampo+" - Error de formato\n";
        }

        debug("Tiporeg["+tipoReg+"] - "+nombreCampo+"["+valorCampo+"] - PosIni["+(contenidoReg.length + 1)+"] - Longitud["+valorCampo.length+"]");

        if (compuesto == "T") {
            /*Campo de numero compuesto por enteros y decimales*/
            var sValorCampo:String = valorCampo.toString();
            var lEnteros:Number = parseFloat(longitudCampo - 2);
            var lDecimales:Number = 2;
            var sDecimales:String = sValorCampo.right(2);
            var nEnteros:Number = parseFloat(sValorCampo.left(lEnteros));
            var sEnteros:String = nEnteros.toString();
            valorCampo = sEnteros+","+sDecimales;
        }

        if (i == 0) {
            contenidoReg += valorCampo;
        } else {
            contenidoReg += "|"+valorCampo;
        }
    }

    return contenidoReg;
}


function boe2011_establecerFechasPeriodo(codEjercicio:String, tipo:String, valor:String):Array
{
    var util:FLUtil = new FLUtil();

    var fechaInicio:Date = new Date(Date.parse( "2001-01-01T00:00:00" ));
    var fechaFin:Date = new Date(Date.parse( "2001-01-01T00:00:00" ));
    var fechasP:Array = [];
    fechasP["inicio"] = "0000-00-00";
    fechasP["fin"] = "0000-00-00";

    var inicioEjercicio = util.sqlSelect("ejercicios", "fechainicio", "codejercicio = '" + codEjercicio + "'");
    if (!inicioEjercicio) {
        MessageBox.warning(util.translate("scripts","No se ha encontrado la fecha inicio del ejercicio  %1.No es posible continuar").arg(codEjercicio),MessageBox.Ok,MessageBox.NoButton);
        return fechasP;
    }

    fechaInicio.setYear(inicioEjercicio.getYear());
    fechaFin.setYear(inicioEjercicio.getYear());
    fechaInicio.setDate(1);


    switch (tipo) {
        case "Trimestre":
            switch (valor){
                case "1T":
                    fechaInicio.setMonth(1);
                    fechaFin.setMonth(3);
                    fechaFin.setDate(31);
                    break;

                case "2T":
                    fechaInicio.setMonth(4);
                    fechaFin.setMonth(6);
                    fechaFin.setDate(30);
                    break;

                case "3T":
                    fechaInicio.setMonth(7);
                    fechaFin.setMonth(9);
                    fechaFin.setDate(30);
                    break;
                case "4T":
                    fechaInicio.setMonth(10);
                    fechaFin.setMonth(12);
                    fechaFin.setDate(31);
                    break;
            }
            break;

        case "Mes":
                var numMes:Number = parseInt(valor);
                fechaInicio.setDate(1);
                fechaInicio.setMonth(numMes);
                fechaFin = util.addMonths(fechaInicio, 1);
                fechaFin = util.addDays(fechaFin, -1);
                break;

    }

    if (fechaInicio && fechaFin) {
        fechasP["inicio"] = fechaInicio.toString().left(10);
        fechasP["fin"] = fechaFin.toString().left(10);
    }


    return fechasP;
}

/*Valida extensiones en la base de datos*/
function boe2011_validarExtension(extension:String):Boolean
{
    var util = new FLUtil();

    var tabla:String;
    var campo:String;

    switch(extension) {
        case "gestesoreria":
            tabla = "reciboscli";
            campo = "codejercicio";
            break;

        case "multiempresa":
            tabla = "ejercicios";
            campo = "idempresa";
            break;

        case "column0":
            tabla = "empresa";
            campo = "column0";
            break;
    }


    var fieldList:String = util.nombreCampos(tabla);
    var ret:Boolean = false;

    for (var i:Number = 0; i<fieldList.length; i++) {
        var nombreCampo:String = fieldList[i];
        if (nombreCampo == campo) {
            ret = true;
            break;
        }
    }
    return ret;
}

function boe2011_consultaDeclarados347(p:Array):FLSqlQuery {

    var qryDeclarados= new FLSqlQuery;
    var where:String = p.where;
    if (p.origen == "Contabilidad"){
        /*Contabilidad"*/
        if (p.clave == "B"){
            qryDeclarados.setTablesList("clientes,co_asientos,co_partidas,co_subcuentascli");
            qryDeclarados.setSelect("cp.cifnif, SUM(p.debe - p.haber)");
            qryDeclarados.setFrom("co_partidas p INNER JOIN co_subcuentascli scp ON p.idsubcuenta = scp.idsubcuenta INNER JOIN clientes cp ON scp.codcliente = cp.codcliente INNER JOIN co_asientos a ON p.idasiento = a.idasiento");
            p["groupby"] = "cp.cifnif";
            p["having"]  = "ABS(SUM(p.debe - p.haber)) > "+p.importemin;

        }else if (p.clave == "A"){
            qryDeclarados.setTablesList("proveedores,co_asientos,co_partidas,co_subcuentasprov");
            qryDeclarados.setSelect("cp.cifnif, SUM(p.haber - p.debe)");
            qryDeclarados.setFrom("co_partidas p INNER JOIN co_subcuentasprov scp ON p.idsubcuenta = scp.idsubcuenta INNER JOIN proveedores cp ON scp.codproveedor = cp.codproveedor INNER JOIN co_asientos a ON a.idasiento = p.idasiento");
            p["groupby"] = "cp.cifnif";
            p["having"]  = "ABS(SUM(p.haber - p.debe)) > "+p.importemin;
        }
    } else {
        /*Facturación"*/
        var tablaOrig:String;
        if (p.clave == "B") tablaOrig = "facturascli";
        if (p.clave == "A") tablaOrig = "facturasprov";
        qryDeclarados.setTablesList(tablaOrig+",co_asientos");
        qryDeclarados.setSelect("f.cifnif,SUM(f.total)");
        qryDeclarados.setFrom(tablaOrig+" f INNER JOIN co_asientos a on f.idasiento = a.idasiento");
        p["groupby"] = "f.cifnif";
        p["having"]  = "ABS(SUM(f.total)) > "+p.importemin;
    }

    if (p["groupby"]) {
        where += " GROUP BY "+p["groupby"];
    }

    if (p["having"]) {
        where += " HAVING "+p["having"];
    }

    qryDeclarados.setWhere(where);
    debug("Consulta Declarados 347 / Clave:"+p.clave+" Tipo:"+p.tipoimp+" >>> "+qryDeclarados.sql());
    return qryDeclarados;

}

function boe2011_establecerFromMetalico(p:Array):Array
{
    var util= new FLUtil();

    p["tablas"] = [];

    if (p.clave == "A") {
        p["tablas"]["recibos"] = "recibosprov";
        p["tablas"]["pagosdevol"] = "pagosdevolprov";
        p["tablas"]["facturas"] = "facturasprov";
    } else if (p.clave == "B") {
        p["tablas"]["recibos"] = "reciboscli";
        p["tablas"]["pagosdevol"] = "pagosdevolcli";
        p["tablas"]["facturas"] = "facturascli";
    }

    p["from"] = p["tablas"]["recibos"]+" r INNER JOIN (SELECT r1.idrecibo,max(p1.idpagodevol) AS idpagodevol FROM "+p["tablas"]["recibos"]+" r1 INNER JOIN "+p["tablas"]["pagosdevol"]+" p1 ON r1.idrecibo = p1.idrecibo GROUP BY r1.idrecibo) x ON r.idrecibo = x.idrecibo INNER JOIN "+p["tablas"]["pagosdevol"]+" p on x.idrecibo = p.idrecibo AND x.idpagodevol = p.idpagodevol";

    if (flcontmode.iface.xGesteso) {
        p["from"] += " LEFT JOIN "+  p["tablas"]["facturas"] +" f on f.idfactura = r.idfactura ";
    } else {
        p["from"] += " INNER JOIN "+  p["tablas"]["facturas"] +" f on f.idfactura = r.idfactura ";
    }

    return p;
}

function boe2011_consultaDeclaradosMetalico(p:Array):FLSqlQuery {

    var where:String = p.where;

    var qryFiltro = new FLSqlQuery;
    var filtroCifNif:String = "'-1'";
    qryFiltro.setTablesList(p["tablas"]["recibos"]+","+p["tablas"]["pagosdevol"]+","+p["tablas"]["facturas"]);
    qryFiltro.setSelect(p["campos"]["cifnif"]+","+p["campos"]["valor"]);
    qryFiltro.setFrom(p["from"]);
    p["groupby"] = p["campos"]["cifnif"];
    p["having"]  = p["campos"]["valor"]+" > "+p.importemin;

    if (p["groupby"]) {
        where += " GROUP BY "+p["groupby"];
    }

    if (p["having"]) {
        where += " HAVING "+p["having"];
    }

    qryFiltro.setWhere(where);
    debug("ImporteEfectivo filtro>> "+qryFiltro.sql());
    qryFiltro.setForwardOnly(true);
    qryFiltro.exec();
    while (qryFiltro.next()){
        if (filtroCifNif) filtroCifNif+= ",";
        filtroCifNif += "'"+qryFiltro.value(0)+"'";
    }

    var qryDeclarados= new FLSqlQuery;
    qryDeclarados.setTablesList(p["tablas"]["recibos"]+","+p["tablas"]["pagosdevol"]+","+p["tablas"]["facturas"]);
    qryDeclarados.setSelect(p["campos"]["cifnif"]+","+p["campos"]["valor"]+","+p["campos"]["codejercicio"]);
    qryDeclarados.setFrom(p["from"]);
    where =  p.where;
    where += " AND "+p["campos"]["cifnif"]+" IN("+filtroCifNif+")";
    p["groupby"] = p["campos"]["cifnif"]+","+p["campos"]["codejercicio"];

    if (p["groupby"]) {
        where += " GROUP BY "+p["groupby"];
    }

    qryDeclarados.setWhere(where);
    debug("Consulta Declarados Metalico/ Clave:"+p.clave+" Tipo:"+p.tipoimp+" >>> "+qryDeclarados.sql());
    return qryDeclarados;

}

function boe2011_datosDeclarados(p:Array,qryDeclarados:FLSqlQuery):Array {

    var datos:Array;
    var util= new FLUtil();
    datos["importe"] = parseFloat(qryDeclarados.value(1));

    if (p.clave == "B"){
        datos["codCP"] = util.sqlSelect("clientes", "codcliente", "cifnif = '" + qryDeclarados.value(0) + "' ORDER BY codcliente");
        datos["codPais"] = util.sqlSelect("dirclientes dc INNER JOIN paises p ON dc.codpais = p.codpais", "p.codiso", "dc.codcliente = '" + datos["codCP"] + "' AND dc.domfacturacion = true", "dirclientes,paises");
        datos["nombreCP"] = util.sqlSelect("clientes", "nombre", "cifnif = '" + qryDeclarados.value(0) + "' ORDER BY codcliente");
        datos["codProvincia"] = util.sqlSelect("dirclientes dc INNER JOIN provincias p ON dc.idprovincia = p.idprovincia", "p.codigo", "dc.codcliente = '" + datos["codCP"] + "' AND dc.domfacturacion = true", "dirclientes,provincias");
        datos["tipoId"] = util.sqlSelect("clientes", "tipoidfiscal", "codcliente = '" + datos["codCP"] + "' ORDER BY codcliente");
    }else if (p.clave == "A"){
        datos["codCP"] = util.sqlSelect("proveedores", "codproveedor", "cifnif = '" + qryDeclarados.value(0) + "' ORDER BY codproveedor");
        datos["codPais"] = util.sqlSelect("dirproveedores dp INNER JOIN paises p ON dp.codpais = p.codpais", "p.codiso", "dp.codproveedor = '" + datos["codCP"] + "' AND dp.direccionppal = true", "dirproveedores,paises");
        datos["nombreCP"] = util.sqlSelect("proveedores", "nombre", "cifnif = '" + qryDeclarados.value(0) + "' ORDER BY codproveedor");
        datos["codProvincia"] = util.sqlSelect("dirproveedores dp INNER JOIN provincias p ON dp.idprovincia = p.idprovincia", "p.codigo", "dp.codproveedor = '" + datos["codCP"] + "' AND dp.direccionppal = true", "dirproveedores,provincias");
        datos["tipoId"] = util.sqlSelect("proveedores", "tipoidfiscal", "codproveedor = '" + datos["codCP"] + "' ORDER BY codproveedor");

    }

    datos["nombreCP"] = flcontmode.iface.pub_formatearTexto(datos["nombreCP"]);
    datos["cifCP"] = flcontmode.iface.pub_limpiarCifNif(qryDeclarados.value(0));

    if (p.tipoimp == "Importe") {
        datos["importe"] = qryDeclarados.value(1);
        datos["importe1t"] = this.iface.importeTrimestre(p,qryDeclarados.value(0),"1T");
        datos["importe2t"] = this.iface.importeTrimestre(p,qryDeclarados.value(0),"2T");
        datos["importe3t"] = this.iface.importeTrimestre(p,qryDeclarados.value(0),"3T");
        datos["importe4t"] = this.iface.importeTrimestre(p,qryDeclarados.value(0),"4T");
    } else if (p.tipoimp == "ImporteEfectivo") {
        datos["importeMetalico"] = qryDeclarados.value(1);
        datos["ejercicioMetalico"] = util.sqlSelect("ejercicios","date_part('year',fechainicio)","codejercicio='"+qryDeclarados.value(2)+"'");
    }

    return datos;
}

function boe2011_importeTrimestre(p:Array,cifnif:String,trimestre:String):Number{

    var fechaT:Array = flcontmode.iface.pub_establecerFechasPeriodo(p.codejercicio,"Trimestre",trimestre);
    var util= new FLUtil();
    var tablas:String;
    var tablasF:String;
    var valor:String;
    var condicion:String = p.where;

    if (p.origen == "Contabilidad") {
        condicion += " AND cp.cifnif = '"+cifnif+"' AND a.fecha between '"+fechaT.inicio+"' AND '"+fechaT.fin+"'";
        if (p.clave == "B") {
            valor = "SUM(p.debe - p.haber)";
            tablas = "clientes,co_asientos,co_partidas,co_subcuentascli";
            tablasF = "co_partidas p INNER JOIN co_subcuentascli scp ON p.idsubcuenta = scp.idsubcuenta INNER JOIN clientes cp ON scp.codcliente = cp.codcliente INNER JOIN co_asientos a ON p.idasiento = a.idasiento";
        }else if (p.clave == "A"){
            valor = "SUM(p.haber - p.debe)";
            tablas = "proveedores,co_asientos,co_partidas,co_subcuentasprov";
            tablasF = "co_partidas p INNER JOIN co_subcuentasprov scp ON p.idsubcuenta = scp.idsubcuenta INNER JOIN proveedores cp ON scp.codproveedor = cp.codproveedor INNER JOIN co_asientos a ON p.idasiento = a.idasiento";
        }
    } else {
        valor = "SUM(f.total)";
        condicion += " AND f.cifnif = '"+cifnif+"' AND a.fecha between '"+fechaT.inicio+"' AND '"+fechaT.fin+"'";
        if (p.clave == "B") {
            tablas = "facturascli,co_asientos";
            tablasF = "facturascli f inner join co_asientos a on f.idasiento = a.idasiento";
        } else if (p.clave == "A") {
            tablas = "facturasprov,co_asientos";
            tablasF = "facturasprov f inner join co_asientos a on f.idasiento = a.idasiento";
        }
    }

    var importe:Number = util.sqlSelect(tablasF,valor,condicion,tablas);
    if (!importe || isNaN(importe)){
        importe = 0;
    }

    return importe;

}

function boe2011_identFraDeclaradosMetalico(p:Array, cifnif:String):String {

    var util= new FLUtil();
    var codFactura:String = "";
    var where:String = p.where;

    var qryDeclarados= new FLSqlQuery;
    qryDeclarados.setTablesList(p["tablas"]["recibos"]+","+p["tablas"]["pagosdevol"]+","+p["tablas"]["facturas"]);
    qryDeclarados.setSelect("r.idfactura");
    qryDeclarados.setFrom(p["from"]);
    where =  p.where;
    where += " AND "+p["campos"]["cifnif"]+" = '"+cifnif+"'";
    where += " AND r.idfactura is not null";
    qryDeclarados.setWhere(where);

    //debug("Consulta identFra Metalico/ cifnif:"+cifnif+" >>> "+qryDeclarados.sql());
    if (!qryDeclarados.exec()) {
        MessageBox.critical(util.translate("scripts", "Falló la consulta de declarantes para importes en metálico / identificador de factura /"), MessageBox.Ok, MessageBox.NoButton);
        return codFactura;
    }

    if (qryDeclarados.first()) {
        codFactura = util.sqlSelect(p["tablas"]["facturas"],"codigo","idfactura="+qryDeclarados.value("r.idfactura"));
    }

    return codFactura;

}
//// BOE2011 ///////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition modelo031 */
/////////////////////////////////////////////////////////////////
//// MODELO031 //////////////////////////////////////////////////
function modelo031_beforeCommit_co_modelo031(curModelo:FLSqlCursor):Boolean{

    if (sys.isLoadedModule("flcontppal") && flfactppal.iface.pub_valorDefectoEmpresa("contintegrada") && curModelo.modeAccess() == curModelo.Edit) {
        if (curModelo.valueBuffer("cerrado") == true && curModelo.valueBufferCopy("cerrado") == false){
            if (this.iface.generarAsientoModelo031(curModelo) == false) {
                return false;
            }
        }

        if (curModelo.valueBuffer("cerrado") == false && curModelo.valueBuffer("idasiento") && curModelo.valueBuffer("idasiento")!=""){
            curModelo.setNull("idasiento");
        }

    }

    var util:FLUtil = new FLUtil();
    if (curModelo.modeAccess() == curModelo.Del) {
        var pago:Number = util.sqlSelect("co_pagomodelo031","idpago","idmodelo="+curModelo.valueBuffer("idmodelo"));
        if (pago) {
            if (!curModelo.valueBuffer("idfacturarepres")){
                MessageBox.warning(util.translate("scripts","Ocurrió un error al eliminar el modelo 031.\nElimine previamente el pago del modelo"), MessageBox.Ok, MessageBox.NoButton);
            } else {
                MessageBox.warning(util.translate("scripts","Ocurrió un error al eliminar el modelo 031 asociado a la factura %1.\nElimine previamente el pago del modelo").arg(util.sqlSelect("facturasprov","codigo","idfactura="+curModelo.valueBuffer("idfacturarepres"))), MessageBox.Ok, MessageBox.NoButton);
            }
            return false;
        }
    }

    return true;
}

function modelo031_afterCommit_co_modelo031(curModelo:FLSqlCursor):Boolean
{
    var util:FLUtil = new FLUtil();

    if (curModelo.modeAccess() == curModelo.Del) {
        if (curModelo.valueBuffer("idfacturarepres")) {
            if (!formfacturasprov.iface.asociarModelo031("false",curModelo.valueBuffer("idfacturarepres"))) {
                MessageBox.warning(util.translate("scripts", "Ocurrió un error al eliminar el modelo 031 asociado a la factura").arg(util.sqlSelect("facturasprov","codigo","idfactura="+curModelo.valueBuffer("idfacturarepres"))), MessageBox.Ok, MessageBox.NoButton);
                return false;
            }
        }
    }

    if (sys.isLoadedModule("flcontppal") && flfactppal.iface.pub_valorDefectoEmpresa("contintegrada")) {
        switch (curModelo.modeAccess()) {
            case curModelo.Edit:
            if (curModelo.valueBuffer("cerrado") == true && curModelo.valueBuffer("nogenerarasiento")) {
                var idAsientoAnterior:String = curModelo.valueBufferCopy("idasiento");
                if (idAsientoAnterior && idAsientoAnterior != "") {
                    if (!flfacturac.iface.pub_eliminarAsiento(idAsientoAnterior)) {
                        return false;
                    }
                }
            }
            if (curModelo.valueBuffer("cerrado") == false && curModelo.valueBufferCopy("cerrado") == true){
                var idAsientoAnterior:String = curModelo.valueBufferCopy("idasiento");
                if (!flfacturac.iface.eliminarAsiento(idAsientoAnterior)){
                    return false;
                }
            }
            if (curModelo.valueBuffer("cerrado") != curModelo.valueBufferCopy("cerrado")) {
                if (!this.iface.cambiarEstadoModelo031(curModelo.valueBuffer("idmodelo"))){
                    return false;
                }
            }
            break;

            case curModelo.Del:
                if (!flfacturac.iface.pub_eliminarAsiento(curModelo.valueBuffer("idasiento"))) {
                    return false;
                }
                break;
        }
    }

    return true;
}

function modelo031_generarAsientoModelo031(curModelo:FLSqlCursor):Boolean {

    if (curModelo.modeAccess() != curModelo.Insert && curModelo.modeAccess() != curModelo.Edit){
        return true;
    }

    var util:FLUtil = new FLUtil;
    if (curModelo.valueBuffer("nogenerarasiento")) {
        curModelo.setNull("idasiento");
        return true;
    }

    var datosAsiento:Array = [];
    var valoresDefecto:Array;
    valoresDefecto["codejercicio"] = curModelo.valueBuffer("codejercicio");
    valoresDefecto["coddivisa"] = flfactppal.iface.pub_valorDefectoEmpresa("coddivisa");

    var curTransaccion:FLSqlCursor = new FLSqlCursor("empresa");
    curTransaccion.transaction(false);
    try {
        datosAsiento = flfacturac.iface.pub_regenerarAsiento(curModelo, valoresDefecto);
        if (datosAsiento.error == true) {
            throw util.translate("scripts", "Error al regenerar el asiento");
        }

        if (!this.iface.generarPartidaIvaImportacion(curModelo, datosAsiento, valoresDefecto)) {
            throw util.translate("scripts", "Error al generar la partida de Iva de Importación");
        }

        if (!this.iface.generarPartidaHPAcreedorIva(curModelo, datosAsiento, valoresDefecto)){
            throw util.translate("scripts", "Error al generar las partidas de H.P. Acreedora por iva");
        }

        if (!flcontppal.iface.pub_comprobarAsiento(datosAsiento.idasiento)) {
            throw util.translate("scripts", "Error al comprobar el asiento");
        }

        curModelo.setValueBuffer("idasiento", datosAsiento.idasiento);

    } catch (e) {
        curTransaccion.rollback();
        MessageBox.warning(util.translate("scripts", "Error al generar el asiento correspondiente al DUA %1:").arg(curModelo.valueBuffer("numreferencia")) + "\n" + e, MessageBox.Ok, MessageBox.NoButton);
        return false;
    }
    curTransaccion.commit();

    return true;
}

function modelo031_generarPartidaIvaImportacion(curModelo:FLSqlCursor, datosAsiento:Array, valoresDefecto:Array) {

    var util:FLUtil = new FLUtil();
    var debe:Number = parseFloat(curModelo.valueBuffer("cuotaimport"));
    var debeME:Number = 0;

    debe = util.roundFieldValue(debe, "co_partidas", "debe");
    debeME = util.roundFieldValue(debeME, "co_partidas", "debeme");

    var subCtaIvaSim = this.iface.valorDefectoDatosFiscales("codsubcuentaivasim");
    if (!subCtaIvaSim) {
        MessageBox.warning(util.translate("scripts", "No tiene definida una subcuenta de Iva soportado de Importación.\nPor favor acceda al formulario de datos fiscales y configure dicha subcuenta.\nEl asiento asociado al modelo 031 no puede ser creado"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
        return false;
    }

    var idSubCtaIvaSim = util.sqlSelect("co_subcuentas","idsubcuenta","codsubcuenta='"+subCtaIvaSim+"' and codejercicio='"+valoresDefecto.codejercicio+"'");
    if (!idSubCtaIvaSim) {
        MessageBox.warning(util.translate("scripts", "La subcuenta %1 no existe para el ejercicio %2.\nEl asiento asociado al modelo 031 no puede ser creado").arg(subCtaIvaSim).arg(valoresDefecto.codejercicio), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
        return false;
    }

    var subCtaHP = this.iface.valorDefectoDatosFiscales("codsubcuentahpacre");
    if (!subCtaHP) {
        MessageBox.warning(util.translate("scripts", "No tiene definida una subcuenta de H.P Acreedora por Iva.\nPor favor acceda al formulario de datos fiscales y configure dicha subcuenta.\nEl asiento asociado al modelo 031 no puede ser creado"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
        return false;
    }

    var idSubCtaHP = util.sqlSelect("co_subcuentas","idsubcuenta","codsubcuenta='"+subCtaHP+"' and codejercicio='"+valoresDefecto.codejercicio+"'");
    if (!idSubCtaHP) {
        MessageBox.warning(util.translate("scripts", "La subcuenta %1 no existe para el ejercicio %2.\nEl asiento asociado al modelo 031 no puede ser creado").arg(subCtaHP).arg(valoresDefecto.codejercicio), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
        return false;
    }

    var casilla:String;
    switch(curModelo.valueBuffer("tipobienes")) {
        case "Corrientes":
            casilla = "[26]-[27]";
            break;

        case "De Inversión":
            casilla = "[28]-[29]";
            break;

        case "Indefinido":
            casilla = "";
            break;
    }

    var curPartida:FLSqlCursor = new FLSqlCursor("co_partidas");
    curPartida.setModeAccess(curPartida.Insert);
    curPartida.refreshBuffer();
    curPartida.setValueBuffer("idsubcuenta", idSubCtaIvaSim);
    curPartida.setValueBuffer("codsubcuenta", subCtaIvaSim);
    curPartida.setValueBuffer("idasiento", datosAsiento.idasiento);
    curPartida.setValueBuffer("debe", debe);
    curPartida.setValueBuffer("haber", 0);
    curPartida.setValueBuffer("coddivisa", valoresDefecto["coddivisa"]);
    curPartida.setValueBuffer("tasaconv", 1);
    curPartida.setValueBuffer("debeME", debeME);
    curPartida.setValueBuffer("haberME", 0);
    curPartida.setValueBuffer("baseimponible", curModelo.valueBuffer("baseimport"));
    curPartida.setValueBuffer("iva", curModelo.valueBuffer("tipoivaimport"));
    curPartida.setValueBuffer("concepto", datosAsiento.concepto);
    curPartida.setValueBuffer("cifnif", curModelo.valueBuffer("cifnif"));
    if (casilla && casilla != "") curPartida.setValueBuffer("casilla303", casilla);
    if (curModelo.valueBuffer("codfacturaimport")) {
        curPartida.setValueBuffer("tipodocumento", "Factura de proveedor");
        curPartida.setValueBuffer("documento", curModelo.valueBuffer("codfacturaimport"));
        curPartida.setValueBuffer("factura",util.sqlSelect("facturasprov","numero","idfactura="+curModelo.valueBuffer("idfacturaimport")));
        curPartida.setValueBuffer("codserie", util.sqlSelect("facturasprov","codserie","idfactura="+curModelo.valueBuffer("idfacturaimport")));
    }
    curPartida.setValueBuffer("idcontrapartida", idSubCtaHP);
    curPartida.setValueBuffer("codcontrapartida", subCtaHP);
    if (!curPartida.commitBuffer()){
        return false;
    }

    return true;

}

function modelo031_generarPartidaHPAcreedorIva(curModelo:FLSqlCursor, datosAsiento:Array, valoresDefecto:Array) {

    var util:FLUtil = new FLUtil();
    var haber:Number = parseFloat(curModelo.valueBuffer("cuotaimport"));
    var haberME:Number = 0;

    haber = util.roundFieldValue(haber, "co_partidas", "haber");
    haberME = util.roundFieldValue(haberME, "co_partidas", "haberme");

    var subCtaHP = this.iface.valorDefectoDatosFiscales("codsubcuentahpacre");
    if (!subCtaHP) {
        MessageBox.warning(util.translate("scripts", "No tiene definida una subcuenta de H.P Acreedora por Iva.\nPor favor acceda al formulario de datos fiscales y configure dicha subcuenta.\nEl asiento asociado al modelo 031 no puede ser creado"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
        return false;
    }

    var idSubCtaHP = util.sqlSelect("co_subcuentas","idsubcuenta","codsubcuenta='"+subCtaHP+"' and codejercicio='"+valoresDefecto.codejercicio+"'");
    if (!idSubCtaHP) {
        MessageBox.warning(util.translate("scripts", "La subcuenta %1 no existe para el ejercicio %2.\nEl asiento asociado al modelo 031 no puede ser creado").arg(subCtaHP).arg(valoresDefecto.codejercicio), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
        return false;
    }

    var curPartida:FLSqlCursor = new FLSqlCursor("co_partidas");

    curPartida.setModeAccess(curPartida.Insert);
    curPartida.refreshBuffer();
    curPartida.setValueBuffer("idsubcuenta", idSubCtaHP);
    curPartida.setValueBuffer("codsubcuenta", subCtaHP);
    curPartida.setValueBuffer("idasiento", datosAsiento.idasiento);
    curPartida.setValueBuffer("debe", 0);
    curPartida.setValueBuffer("haber", haber);
    curPartida.setValueBuffer("coddivisa", valoresDefecto["coddivisa"]);
    curPartida.setValueBuffer("tasaconv", 1);
    curPartida.setValueBuffer("debeME", 0);
    curPartida.setValueBuffer("haberME", haberME);
    curPartida.setValueBuffer("concepto", datosAsiento.concepto);

    if (!curPartida.commitBuffer()){
        return false;
    }

    return true;
}

function modelo031_beforeCommit_co_pagomodelo031(curPago:FLSqlCursor):Boolean{

    if (curPago.modeAccess() == curPago.Insert || curPago.modeAccess() == curPago.Edit) {
        if (sys.isLoadedModule("flcontppal") && flfactppal.iface.pub_valorDefectoEmpresa("contintegrada")) {
            if (!this.iface.generarAsientoPagoModelo031(curPago)) {
                return false;
            }
        }
    }

    return true;
}

function modelo031_afterCommit_co_pagomodelo031(curPago:FLSqlCursor):Boolean
{
    var util:FLUtil = new FLUtil();

    if (sys.isLoadedModule("flcontppal") && flfactppal.iface.pub_valorDefectoEmpresa("contintegrada")) {
        switch (curPago.modeAccess()) {
            case curPago.Edit:
            if (curPago.valueBuffer("nogenerarasiento")) {
                var idAsientoAnterior:String = curPago.valueBufferCopy("idasiento");
                if (idAsientoAnterior && idAsientoAnterior != "") {
                    if (!flfacturac.iface.pub_eliminarAsiento(idAsientoAnterior)) {
                        return false;
                    }
                }
            }
            break;

            case curPago.Del:
                if (!flfacturac.iface.pub_eliminarAsiento(curPago.valueBuffer("idasiento"))) {
                    return false;
                }
                break;
        }
    }

    if (!this.iface.cambiarEstadoModelo031(curPago.valueBuffer("idmodelo"))){
        return false;
    }

    return true;
}

function modelo031_generarAsientoPagoModelo031(curPago:FLSqlCursor):Boolean {

    if (curPago.modeAccess() != curPago.Insert && curPago.modeAccess() != curPago.Edit){
        return true;
    }

    var util:FLUtil = new FLUtil;
    if (curPago.valueBuffer("nogenerarasiento")) {
        curPago.setNull("idasiento");
        return true;
    }

    var codEjercicio:String = flfactppal.iface.pub_ejercicioActual();
    var datosDoc:Array = flfacturac.iface.pub_datosDocFacturacion(curPago.valueBuffer("fecha"), codEjercicio, "pagosdevolcli");
    if (!datosDoc.ok)
        return false;
    if (datosDoc.modificaciones == true) {
        codEjercicio = datosDoc.codEjercicio;
        curPago.setValueBuffer("fecha", datosDoc.fecha);
     }

    var datosAsiento:Array = [];
    var valoresDefecto:Array;
    valoresDefecto["codejercicio"] = codEjercicio;
    valoresDefecto["coddivisa"] = flfactppal.iface.pub_valorDefectoEmpresa("coddivisa");

    var curTransaccion:FLSqlCursor = new FLSqlCursor("empresa");
    curTransaccion.transaction(false);
    try {
        datosAsiento = flfacturac.iface.pub_regenerarAsiento(curPago, valoresDefecto);
        if (datosAsiento.error == true) {
            throw util.translate("scripts", "Error al regenerar el asiento");
        }

        if (!this.iface.generarPartidaBanco(curPago, datosAsiento, valoresDefecto)) {
            throw util.translate("scripts", "Error al generar la partida de Iva de Importación");
        }

        if (!this.iface.generarPartidaPagoHPAcreedorIva(curPago, datosAsiento, valoresDefecto)){
            throw util.translate("scripts", "Error al generar las partidas de H.P. Acreedora por iva");
        }

        if (!flcontppal.iface.pub_comprobarAsiento(datosAsiento.idasiento)) {
            throw util.translate("scripts", "Error al comprobar el asiento");
        }

        curPago.setValueBuffer("idasiento", datosAsiento.idasiento);

    } catch (e) {
        curTransaccion.rollback();
        MessageBox.warning(util.translate("scripts", "Error al generar el asiento correspondiente al Pago del modelo 031")+ "\n" + e, MessageBox.Ok, MessageBox.NoButton);
        return false;
    }
    curTransaccion.commit();

    return true;
}

function modelo031_generarPartidaBanco(curPago:FLSqlCursor, datosAsiento:Array, valoresDefecto:Array) {

    var util:FLUtil = new FLUtil();
    var cuotaImport:Number = util.sqlSelect("co_modelo031","cuotaimport","idmodelo="+curPago.valueBuffer("idmodelo"));
    var haber:Number = parseFloat(cuotaImport);
    var haberME:Number = 0;

    haber = util.roundFieldValue(haber, "co_partidas", "haber");
    haberME = util.roundFieldValue(haberME, "co_partidas", "haberME");

    var datosCuentaEmp:Array = [];
    if (curPago.valueBuffer("codcuenta") && curPago.valueBuffer("codcuenta")!="") {
        datosCuentaEmp.codcuenta = curPago.valueBuffer("codcuenta");
        datosCuentaEmp.codsubcuenta = util.sqlSelect("cuentasbanco","codsubcuenta","codcuenta='"+curPago.valueBuffer("codcuenta")+"'");
        if (datosCuentaEmp.codsubcuenta) {
            datosCuentaEmp.error = 0;
        } else {
            datosCuentaEmp.error = 1;
        }
    } else {
        datosCuentaEmp.error = 1;
    }

    var datosSubcuentaEmp:Array = flfactteso.iface.obtenerDatosSubcuentaEmp(datosCuentaEmp);

    if (datosSubcuentaEmp.error != 0) {
        return false;
    }

    var curPartida:FLSqlCursor = new FLSqlCursor("co_partidas");

    curPartida.setModeAccess(curPartida.Insert);
    curPartida.refreshBuffer();
    curPartida.setValueBuffer("codsubcuenta", datosSubcuentaEmp.codsubcuenta);
    curPartida.setValueBuffer("idsubcuenta", datosSubcuentaEmp.idsubcuenta);
    curPartida.setValueBuffer("idasiento", datosAsiento.idasiento);
    curPartida.setValueBuffer("debe", 0);
    curPartida.setValueBuffer("haber", haber);
    curPartida.setValueBuffer("coddivisa", valoresDefecto["coddivisa"]);
    curPartida.setValueBuffer("tasaconv", 1);
    curPartida.setValueBuffer("debeME", 0);
    curPartida.setValueBuffer("haberME", haberME);
    curPartida.setValueBuffer("concepto", datosAsiento.concepto);

    if (!curPartida.commitBuffer()){
        return false;
    }

    return true;

}

function modelo031_generarPartidaPagoHPAcreedorIva(curPago:FLSqlCursor, datosAsiento:Array, valoresDefecto:Array) {

    var util:FLUtil = new FLUtil();
    var cuotaImport:Number = util.sqlSelect("co_modelo031","cuotaimport","idmodelo="+curPago.valueBuffer("idmodelo"));
    var debe:Number = parseFloat(cuotaImport);
    var debeME:Number = 0;

    debe = util.roundFieldValue(debe, "co_partidas", "debe");
    debeME = util.roundFieldValue(debeME, "co_partidas", "debeme");

    var idAsientoModelo = util.sqlSelect("co_modelo031","idasiento","idmodelo="+curPago.valueBuffer("idmodelo"));

    if (!idAsientoModelo){
        return false;
    }

    subCtaHP = util.sqlSelect("co_partidas p INNER JOIN co_subcuentas s ON p.idsubcuenta = s.idsubcuenta INNER JOIN co_cuentas c ON c.idcuenta = s.idcuenta","s.codsubcuenta","p.idasiento = " + idAsientoModelo + " AND s.idcuentaesp = 'IVAACR' OR c.idcuentaesp = 'IVAACR'","co_partidas,co_subcuentas,co_cuentas");

    if(!subCtaHP) {
         MessageBox.warning(util.translate("scripts", "No se ha encontrado la subcuenta de H.P.acredora por iva, del asiento contable correspondiente al modelo a pagar"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
        return false;
    }

    var idSubCtaHP = util.sqlSelect("co_subcuentas","idsubcuenta","codsubcuenta='"+subCtaHP+"' and codejercicio='"+valoresDefecto.codejercicio+"'");
    if (!idSubCtaHP) {
        MessageBox.warning(util.translate("scripts", "La subcuenta %1 no existe para el ejercicio %2.\nEl asiento asociado al modelo 031 no puede ser creado").arg(subCtaHP).arg(valoresDefecto.codejercicio), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
        return false;
    }

    var curPartida:FLSqlCursor = new FLSqlCursor("co_partidas");

    curPartida.setModeAccess(curPartida.Insert);
    curPartida.refreshBuffer();
    curPartida.setValueBuffer("idsubcuenta", idSubCtaHP);
    curPartida.setValueBuffer("codsubcuenta", subCtaHP);
    curPartida.setValueBuffer("idasiento", datosAsiento.idasiento);
    curPartida.setValueBuffer("debe", debe);
    curPartida.setValueBuffer("haber", 0);
    curPartida.setValueBuffer("coddivisa", valoresDefecto["coddivisa"]);
    curPartida.setValueBuffer("tasaconv", 1);
    curPartida.setValueBuffer("debeME", debeME);
    curPartida.setValueBuffer("haberME", 0);
    curPartida.setValueBuffer("concepto", datosAsiento.concepto);

    if (!curPartida.commitBuffer()){
        return false;
    }

    return true;
}

function modelo031_cambiarEstadoModelo031(idModelo:Number):Boolean{

    var util:FLUtil = new FLUtil();
    var estado = formRecordco_modelo031.iface.calcularEstadoModelo031(idModelo);
    if (!util.sqlUpdate("co_modelo031","estado",estado,"idmodelo="+idModelo)){
        return false;
    }

    return true;
}

//// MODELO031 //////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////

//// DESARROLLO /////////////////////////////////////////////////
// /////////////////////////////////////////////

