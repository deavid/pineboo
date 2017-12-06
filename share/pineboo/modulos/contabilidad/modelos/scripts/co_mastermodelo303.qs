/***************************************************************************
                 i_mastermodelo303.qs  -  description
                             -------------------
    begin                : jue may 19 2005
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

//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
class oficial extends interna {
	function oficial( context ) { interna( context ); }
	function lanzar() {
		return this.ctx.oficial_lanzar();
	}
	function presTelematica() {
		return this.ctx.oficial_presTelematica();
	}
	function presTelematica2009() {
		return this.ctx.oficial_presTelematica2009();
	}
	function presTelematica2014() {
		return this.ctx.oficial_presTelematica2014();
	}
	function errorAcumuladoControl(acumuladoControl:Number, nombreDato:String):Boolean {
		return this.ctx.oficial_errorAcumuladoControl(acumuladoControl, nombreDato);
	}
	function formatoFecha(fecha) {
    return this.ctx.oficial_formatoFecha(fecha);
  }
}
//// OFICIAL /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////
class head extends oficial {
	function head( context ) { oficial ( context ); }
}
//// DESARROLLO /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////
//// INTERFACE  /////////////////////////////////////////////////
class ifaceCtx extends head {
	function ifaceCtx( context ) { head( context ); }
}

const iface = new ifaceCtx( this );
//// INTERFACE  /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////
//// DEFINICION ////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////
//// INTERNA /////////////////////////////////////////////////////
function interna_init()
{
	this.child("toolButtonPrint").close();
	connect (this.child("toolButtonAeat"), "clicked()", this, "iface.presTelematica()");
}
//// INTERNA /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
/** \D Lanza el informe asociado al modelo 300 seleccionado
\end */
function oficial_lanzar()
{
	var cursor:FLSqlCursor = this.cursor();
	var nombreInforme:String = cursor.action();
	flcontmode.iface.pub_lanzar(cursor, nombreInforme, nombreInforme + ".id=" + cursor.valueBuffer( "id" ) );
}

/** \D Genera un fichero para realizar la presentación telemática del modelo
\end */
function oficial_presTelematica()
{
	var _i = this.iface;
	var cursor = this.cursor();
	if (!cursor.isValid()) {
		return;
	}

	var ejercicio = parseFloat(cursor.valueBuffer("fechainicio"));
	var temp = ejercicio.toString().left(4); 
	if (temp < 2013) {
		_i.presTelematica2009();
	}
	else {
		_i.presTelematica2014();
	}
}

/** \D Genera un fichero para realizar la presentación telemática del modelo para el ejercicio 2007
\end */
function oficial_presTelematica2009()
{
	var util:FLUtil = new FLUtil();
	var cursor:FLSqlCursor = this.cursor();
	if (!cursor.isValid())
		return;
	
	var nombreFichero:String = FileDialog.getSaveFileName("*.*");
	if (!nombreFichero)
		return;
		
	var acumuladoControl:Number = 1;
	var nombreDato:String;
	var contenido:String = "";
	var file:Object = new File(nombreFichero);
	file.open(File.WriteOnly);

	nombreDato = util.translate("scripts", "Inicio de Id. de modelo y página");
	if ((contenido.length + 1) !=  1) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	contenido += "<T";
	
	nombreDato = util.translate("scripts", "Modelo");
	if ((contenido.length + 1) !=  3) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	contenido += "303";
	
	nombreDato = util.translate("scripts", "Página");
	if ((contenido.length + 1) !=  6) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	contenido += "01";
	
	nombreDato = util.translate("scripts", "Fin de Id. de modelo y página");
	if ((contenido.length + 1) !=  8) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	contenido += ">";
	
	nombreDato = util.translate("scripts", "Indicador de página complementaria");
	if ((contenido.length + 1) !=  9) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	contenido += " ";
	
	nombreDato = util.translate("scripts", "Tipo de declaración");
	if ((contenido.length + 1) !=  10) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	var temp:String = cursor.valueBuffer("idtipodec");
	if (!flcontmode.iface.pub_verificarDato(temp, true, nombreDato, 1)) {
		return false;
	}
	contenido += temp;
	
	nombreDato = util.translate("scripts", "NIF");
	if ((contenido.length + 1) !=  11) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = flcontmode.iface.pub_valorDefectoDatosFiscales("cifnif");
	if (!flcontmode.iface.pub_verificarDato(temp, true, nombreDato, 9))
		return false;
	contenido += temp; 
	
	nombreDato = util.translate("scripts", "Apellidos o razón social");
	if ((contenido.length + 1) !=  20) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	
	if (flcontmode.iface.pub_valorDefectoDatosFiscales("personafisica")) {
		temp = flcontmode.iface.pub_valorDefectoDatosFiscales("apellidospf");
	} else {
		temp = flcontmode.iface.pub_valorDefectoDatosFiscales("apellidosrs");
	}

	if (!flcontmode.iface.pub_verificarDato(temp, true, nombreDato, 30))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 30); 
	
	nombreDato = util.translate("scripts", "Nombre");
	if ((contenido.length + 1) !=  50) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = flcontmode.iface.pub_valorDefectoDatosFiscales("nombrepf");
	if (!flcontmode.iface.pub_verificarDato(temp, false, nombreDato, 15))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 15); 
	
	nombreDato = util.translate("scripts", "Inscrito en Registro de devolución mensual");
	if ((contenido.length + 1) !=  65) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	if (cursor.valueBuffer("inscritoregdev")) {
		temp = "1";
	} else {
		temp = "2";
	}
	contenido += temp;
	
	nombreDato = util.translate("scripts", "Ejercicio");
	if ((contenido.length + 1) !=  66) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("fechainicio");
	contenido += temp.toString().left(4);
	
	nombreDato = util.translate("scripts", "Período");
	if ((contenido.length + 1) !=  70) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	if (cursor.valueBuffer("tipoperiodo") == "Trimestre") {
		temp = cursor.valueBuffer("trimestre");
		if (!flcontmode.iface.pub_verificarDato(temp, true, nombreDato, 2))
			return false;
	} else {
		temp = cursor.valueBuffer("fechainicio");
//		temp = temp.toString().substr(5, 2);
		temp = temp.toString().left(7);
		temp = temp.right(2);
	}
	contenido += temp; 
	
	nombreDato = util.translate("scripts", "Base imponible [01]");
	if ((contenido.length + 1) !=  72) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("baseimponiblerg1");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2);
	
	nombreDato = util.translate("scripts", "Tipo % [02]");
	if ((contenido.length + 1) !=  89) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("tiporg1");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 3, 2); 
	
	nombreDato = util.translate("scripts", "Cuota [03]");
	if ((contenido.length + 1) !=  94) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotarg1");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Base imponible [04]");
	if ((contenido.length + 1) !=  111) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("baseimponiblerg2");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Tipo % [05]");
	if ((contenido.length + 1) !=  128) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("tiporg2");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 3, 2); 
	
	nombreDato = util.translate("scripts", "Cuota  [06]");
	if ((contenido.length + 1) !=  133) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotarg2");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Base imponible [07]");
	if ((contenido.length + 1) !=  150) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("baseimponiblerg3");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Tipo % [08]");
	if ((contenido.length + 1) !=  167) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("tiporg3");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 3, 2); 
	
	nombreDato = util.translate("scripts", "Cuota [09]");
	if ((contenido.length + 1) !=  172) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotarg3");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Base imponible recargo equivalencia [10]");
	if ((contenido.length + 1) !=  189) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("baseimponiblere1");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Tipo % recargo equivalencia [11]");
	if ((contenido.length + 1) !=  206) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("tipore1");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 3, 2);
	
	nombreDato = util.translate("scripts", "Cuota recargo equivalencia [12]");
	if ((contenido.length + 1) !=  211) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotare1");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Base imponible recargo equivalencia [13]");
	if ((contenido.length + 1) !=  228) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("baseimponiblere2");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Tipo % recargo equivalencia [14]");
	if ((contenido.length + 1) !=  245) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("tipore2");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 3, 2); 
	
	nombreDato = util.translate("scripts", "Cuota recargo equivalencia [15]");
	if ((contenido.length + 1) !=  250) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotare2");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Base imponible recargo equivalencia [16]");
	if ((contenido.length + 1) !=  267) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("baseimponiblere3");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Tipo % recargo equivalencia [17]");
	if ((contenido.length + 1) !=  284) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("tipore3");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 3, 2); 
	
	nombreDato = util.translate("scripts", "Cuota recargo equivalencia [18]");
	if ((contenido.length + 1) !=  289) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotare3");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Base imponible por adquisiciones intracomunitarias [19]");
	if ((contenido.length + 1) !=  306) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("baseimponibleai");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Cuota por adquisiciones intracomunitarias [20]");
	if ((contenido.length + 1) !=  323) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotaai");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA Devengado: Cuota total (03 + 06 + 09 + 12 + 15 + 18 + 20) [21]");
	if ((contenido.length + 1) !=  340) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotadevtotal");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible por cuotas soportadas en operaciones interiores corrientes. BI [22]");
	if ((contenido.length + 1) !=  357) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("basededoibc");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible por cuotas soportadas en operaciones interiores corrientes. Cuota [23]");
	if ((contenido.length + 1) !=  374) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotadedoibc");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible por cuotas soportadas en operaciones interiores con bienes de inversión. BI [24]");
	if ((contenido.length + 1) !=  391) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("basededoibi");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible por cuotas soportadas en operaciones interiores con bienes de inversión. Cuota [25]");
	if ((contenido.length + 1) !=  408) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotadedoibi");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible por cuotas soportadas en las importaciones de bienes corrientes. BI [26]");
	if ((contenido.length + 1) !=  425) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("basededimbc");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible por cuotas soportadas en las importaciones de bienes corrientes. Cuota [27]");
	if ((contenido.length + 1) !=  442) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotadedimbc");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 

	nombreDato = util.translate("scripts", "IVA deducible por cuotas soportadas en las importaciones de bienes de inversión. BI [28]");
	if ((contenido.length + 1) !=  459) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("basededimbi");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible por cuotas soportadas en las importaciones de bienes de inversión. Cuota [29]");
	if ((contenido.length + 1) !=  476) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotadedimbi");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible en adquisiciones intracomunitarias de bienes corrientes. BI [30]");
	if ((contenido.length + 1) !=  493) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("basededaibc");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible en adquisiciones intracomunitarias de bienes corrientes. Cuota [31]");
	if ((contenido.length + 1) !=  510) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotadedaibc");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible en adquisiciones intracomunitarias de bienes de inversión. BI [32]");
	if ((contenido.length + 1) !=  527) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("basededaibi");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible en adquisiciones intracomunitarias de bienes de inversión. Cuota [33]");
	if ((contenido.length + 1) !=  544) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotadedaibi");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 

	nombreDato = util.translate("scripts", "IVA deducible en compensaciones Régimen Especial A.G. y P. [34]");
	if ((contenido.length + 1) !=  561) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotacomre");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible: Regularización inversiones [35]");
	if ((contenido.length + 1) !=  578) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotaregin");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible: Regularización por aplicación del porcentaje def. de prorrata [36]");
	if ((contenido.length + 1) !=  595) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotaregapli");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 

	nombreDato = util.translate("scripts", "IVA deducible: Total a deducir (?23 + 25 + 27 + 29 + 31 + 33 + 34 + 35 + 36?) [37]");
	if ((contenido.length + 1) !=  612) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotadedtotal");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 

	nombreDato = util.translate("scripts", "Diferencia (21 - 37) [38]");
	if ((contenido.length + 1) !=  629) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotadif");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 

	nombreDato = util.translate("scripts", "Atribuible a la administración del estado - % [39]");
	if ((contenido.length + 1) !=  646) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("porcuotaestado");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 3, 2); 
	
	nombreDato = util.translate("scripts", "Atribuible a la Administración del Estado [40]");
	if ((contenido.length + 1) !=  651) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotaestado");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Cuota a compensar de periodos anteriores [41]");
	if ((contenido.length + 1) !=  668) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotaanterior");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Entregas intracomunitarias [42]");
	if ((contenido.length + 1) !=  685) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("entregasi");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Exportaciones y operaciones asimiladas [43]");
	if ((contenido.length + 1) !=  702) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("exportaciones");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Operaciones no sujetas o con inversión del sujeto pasivo. Derecho a deducción [44]");
	if ((contenido.length + 1) !=  719) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("nosujetas");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Cuota exclusiva para sujetos pasivos que tributan conjuntamente a la Administración del Estado y a las Diputaciones Forales [45]");
	if ((contenido.length + 1) !=  736) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("sujetospasivos");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Resultado (?40 - 41 + 45?) [46]");
	if ((contenido.length + 1) !=  753) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotaresultado");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Importe a deducir [47]");
	if ((contenido.length + 1) !=  770) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("adeducircompl");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Resultado de la liquidación (46 - 47) [48]");
	if ((contenido.length + 1) !=  787) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("resliquid");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Importe a compensar en caso de que la casilla 48 resulte negativa [49]");
	if ((contenido.length + 1) !=  804) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("impcompensar");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Sin actividad");
	if ((contenido.length + 1) !=  821) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	if (cursor.valueBuffer("sinactividad")) {
		temp = "1";
	} else {
		temp = "0";
	}
	contenido += temp;
	
	nombreDato = util.translate("scripts", "Importe a devolver [50]");
	if ((contenido.length + 1) !=  822) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("imported");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Devolución código cuenta cliente - Entidad");
	if ((contenido.length + 1) !=  839) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("ctaentidaddev");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Cuenta de devolución: Entidad "), 4))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 4); 
	
	nombreDato = util.translate("scripts", "Devolución código cuenta cliente - Oficina");
	if ((contenido.length + 1) !=  843) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("ctaagenciadev");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Cuenta de devolución: Oficina "), 4))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 4); 
	
	nombreDato = util.translate("scripts", "Devolución código cuenta cliente - DC");
	if ((contenido.length + 1) !=  847) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("dcdev");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Cuenta de devolución: Dígito de control"), 2))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 2); 
	
	nombreDato = util.translate("scripts", "Devolución código cuenta cliente - Número de cuenta");
	if ((contenido.length + 1) !=  849) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuentadev");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Cuenta de devolución: Nº cuenta"), 10))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 10); 

	nombreDato = util.translate("scripts", "Forma de pago");
	if ((contenido.length + 1) !=  859) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("formapago");
	if (temp == "") {
		temp = "0";
	}
	contenido += temp.left(1); 

	nombreDato = util.translate("scripts", "Importe a ingresar [50]");
	if ((contenido.length + 1) !=  860) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("importei");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 

	
	nombreDato = util.translate("scripts", "Ingreso código cuenta cliente - Entidad");
	if ((contenido.length + 1) !=  877) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("ctaentidadingreso");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Cuenta de ingreso: Entidad"), 4))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 4); 

	nombreDato = util.translate("scripts", "Ingreso código cuenta cliente - Oficina");
	if ((contenido.length + 1) !=  881) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("ctaagenciaingreso");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Cuenta de ingreso: Oficina "), 4))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 4); 

	nombreDato = util.translate("scripts", "Ingreso código cuenta cliente - DC");
	if ((contenido.length + 1) !=  885) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("dcingreso");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Cuenta de ingreso: Dígito de control"), 2))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 2); 

	nombreDato = util.translate("scripts", "Ingreso código cuenta cliente - Número de cuenta");
	if ((contenido.length + 1) !=  887) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuentaingreso");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Cuenta de ingreso: Nº cuenta"), 10))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 10); 

	nombreDato = util.translate("scripts", "Autoliquidación complementaria");
	if ((contenido.length + 1) !=  897) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	if (cursor.valueBuffer("complementaria")) {
		temp = "1";
	} else {
		temp = "0";
	}
	contenido += temp;
	
	nombreDato = util.translate("scripts", "Numero de justificante de la declaracion anterior");
	if ((contenido.length + 1) !=  898) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("numjustificante");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Numero de justificante de la declaracion anterior"), 13))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 13); 

	nombreDato = util.translate("scripts", "Campo reservado");
	if ((contenido.length + 1) !=  911) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = "";
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 400); 

	nombreDato = util.translate("scripts", "Localidad de la firma");
	if ((contenido.length + 1) !=  1311) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("localidadfirma");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Localidad de la firma"), 16))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 16); 

	nombreDato = util.translate("scripts", "Día de la firma");
	if ((contenido.length + 1) !=  1327) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("fechafirma");
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Fecha firma"), 19))
		return false;
	contenido += flfactppal.iface.pub_cerosIzquierda(temp.getDate(), 2);

	nombreDato = util.translate("scripts", "Mes de la firma");
	if ((contenido.length + 1) !=  1329) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("fechafirma");
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Fecha firma"), 19))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(flcontmode.iface.pub_mesPorIndice(temp.getMonth()), 10);

	nombreDato = util.translate("scripts", "Año de la firma");
	if ((contenido.length + 1) !=  1339) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("fechafirma");
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Fecha firma"), 19))
		return false;
	contenido += flfactppal.iface.pub_cerosIzquierda(temp.getYear(), 4);
	
	nombreDato = util.translate("scripts", "Identificador de Fin de registro");
	if ((contenido.length + 1) != 1343) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	contenido += "</T30301>";
	
	nombreDato = util.translate("scripts", "Fin de registro");
	if ((contenido.length + 1) != 1352) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
// 	temp = "\n";
	temp = String.fromCharCode(13, 10);
	contenido += temp;
	
	file.write(contenido);
	file.close();

	MessageBox.information(util.translate("scripts", "El fichero se ha generado en :\n\n" + nombreFichero + "\n\n"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
}

function oficial_presTelematica2014()
{
	var util:FLUtil = new FLUtil();
	var cursor:FLSqlCursor = this.cursor();
	if (!cursor.isValid())
		return;
	
	var nombreFichero:String = FileDialog.getSaveFileName("*.*");
	if (!nombreFichero)
		return;
		
	var acumuladoControl:Number = 1;
	var nombreDato:String;
	var contenido:String = "";
	var file:Object = new File(nombreFichero);
	file.open(File.WriteOnly);

	nombreDato = util.translate("scripts", "Inicio de Id. de modelo y página");
	if ((contenido.length + 1) !=  1) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	contenido += "<T";
	
	nombreDato = util.translate("scripts", "Modelo");
	if ((contenido.length + 1) !=  3) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	contenido += "303";
	
	nombreDato = util.translate("scripts", "Página");
	if ((contenido.length + 1) !=  6) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	contenido += "0";
	
	nombreDato = util.translate("scripts", "Ejercicio");
	if ((contenido.length + 1) !=  7) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("fechainicio");
	contenido += temp.toString().left(4);

	nombreDato = util.translate("scripts", "Período");
	if ((contenido.length + 1) !=  11) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	if (cursor.valueBuffer("tipoperiodo") == "Trimestre") {
		temp = cursor.valueBuffer("trimestre");
		if (!flcontmode.iface.pub_verificarDato(temp, true, nombreDato, 2))
			return false;
	} else {
		temp = cursor.valueBuffer("fechainicio");
//		temp = temp.toString().substr(5, 2);
		temp = temp.toString().left(7);
		temp = temp.right(2);
	}
	contenido += temp; 
	
	nombreDato = util.translate("scripts", "Constante 0000>");
	if ((contenido.length + 1) !=  13) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	contenido += "0000>";
	
	nombreDato = util.translate("scripts", "Constante <AUX>");
	if ((contenido.length + 1) !=  18) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	contenido += "<AUX>";
	
	nombreDato = util.translate("scripts", "Reservado Admón 1");
	if ((contenido.length + 1) !=  23) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = "";
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 70); 
	
	nombreDato = util.translate("scripts", "Version del programa");
	if ((contenido.length + 1) !=  93) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	contenido += "0024";
	
	nombreDato = util.translate("scripts", "Reservado Admón 2");
	if ((contenido.length + 1) !=  97) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = "";
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 4); 
	
	nombreDato = util.translate("scripts", "NIF Empresa Desarrolladora");
	if ((contenido.length + 1) !=  101) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	contenido += "B02352961";
	
	nombreDato = util.translate("scripts", "Reservado Admón 3");
	if ((contenido.length + 1) !=  110) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = "";
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 213); 
	
	nombreDato = util.translate("scripts", "Constante </AUX>");
	if ((contenido.length + 1) !=  323) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	contenido += "</AUX>";
	
	nombreDato = util.translate("scripts", "Constante <VECTOR>");
	if ((contenido.length + 1) !=  329) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = "<VECTOR>001000100200000030001FIN"
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 308);
	
	nombreDato = util.translate("scripts", "Constante </VECTOR>");
	if ((contenido.length + 1) !=  637) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	contenido += "</VECTOR>";
	
	/**
		Contenido
	*/
	
	var contenido1 = "";
	
	nombreDato = util.translate("scripts", "Inicio de Id. de modelo y página");
	if ((contenido1.length + 1) !=  1) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	contenido1 += "<T";
	
	nombreDato = util.translate("scripts", "Modelo");
	if ((contenido1.length + 1) !=  3) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	contenido1 += "303";
	
	nombreDato = util.translate("scripts", "Pagina");
	if ((contenido1.length + 1) !=  6) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	contenido1 += "01"; 
	
	nombreDato = util.translate("scripts", "Fin de Id. de modelo");
	if ((contenido1.length + 1) !=  8) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	contenido1 += ">"; 
	
	nombreDato = util.translate("scripts", "Tipo de declaración");
	if ((contenido1.length + 1) !=  9) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	var temp = cursor.valueBuffer("idtipodec");
	if (!flcontmode.iface.pub_verificarDato(temp, true, nombreDato, 1)) {
		return false;
	}
	contenido1 += temp;
	
	nombreDato = util.translate("scripts", "NIF");
	if ((contenido1.length + 1) !=  10) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = flcontmode.iface.pub_valorDefectoDatosFiscales("cifnif");
	if (!flcontmode.iface.pub_verificarDato(temp, true, nombreDato, 9))
		return false;
	contenido1 += temp; 
	
	nombreDato = util.translate("scripts", "Apellidos o razón social");
	if ((contenido1.length + 1) !=  19) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	
	if (flcontmode.iface.pub_valorDefectoDatosFiscales("personafisica")) {
		temp = flcontmode.iface.pub_valorDefectoDatosFiscales("apellidospf");
	} else {
		temp = flcontmode.iface.pub_valorDefectoDatosFiscales("apellidosrs");
	}

	if (!flcontmode.iface.pub_verificarDato(temp, true, nombreDato, 30))
		return false;
	contenido1 += flfactppal.iface.pub_espaciosDerecha(temp, 30);
	
	nombreDato = util.translate("scripts", "Nombre");
	if ((contenido1.length + 1) !=  49) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = flcontmode.iface.pub_valorDefectoDatosFiscales("nombrepf");
	if (!flcontmode.iface.pub_verificarDato(temp, false, nombreDato, 15))
		return false;
	contenido1 += flfactppal.iface.pub_espaciosDerecha(temp, 15); 
	
	nombreDato = util.translate("scripts", "Inscrito en Registro de devolución mensual");
	if ((contenido1.length + 1) !=  64) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	if (cursor.valueBuffer("inscritoregdev")) {
		temp = "1";
	} else {
		temp = "2";
	}
	contenido1 += temp;
	
	nombreDato = util.translate("scripts", "Tributa en régimen simplificado");
	if ((contenido1.length + 1) !=  65) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	if (cursor.valueBuffer("tributaexcsimp")) {	
		temp = "1";
	} else {
		temp = "2";
	}
	contenido1 += temp;
	
	nombreDato = util.translate("scripts", "Autoliquidación conjunta");
	if ((contenido1.length + 1) !=  66) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	if (cursor.valueBuffer("autoliqconjunta")) {	
		temp = "1";
	} else {
		temp = "2";
	}
	contenido1 += temp;
	
	nombreDato = util.translate("scripts", "Declarado en concurso de acreedores en este periodo");
	if ((contenido1.length + 1) !=  67) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	if (cursor.valueBuffer("concursoacre")) {	
		temp = "1";
	} else {
		temp = "2";
	}
	contenido1 += temp;
	
	nombreDato = util.translate("scripts", "Fecha auto declaración concurso");
	if ((contenido1.length + 1) !=  68) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	
	temp = cursor.valueBuffer("fechaconcurso");
  temp = this.iface.formatoFecha(temp.toString());
  temp = flfactppal.iface.pub_espaciosDerecha(temp, 8);		
	//temp = flfactppal.iface.pub_espaciosDerecha("", 8);
	contenido1 += temp;
	
	nombreDato = util.translate("scripts", "Auto declaración concurso dictado en período");
	if ((contenido1.length + 1) !=  76) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	var tipoConcurso = cursor.valueBuffer("tipodecconcurso");
	switch (tipoConcurso) {
		case "No": {		
			temp = " ";
			break; 
		}
		case "Preconcursal": {
			temp = "1";
			break;
		}
		case "Postconcursal": {
			temp = "2";
			break;		
		}
		default: {
			temp = " ";
		}
	}
	contenido1 += temp;
	
	nombreDato = util.translate("scripts", "Opción por el régimen especial de criterio de Caja");
	if ((contenido1.length + 1) !=  77) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	if (cursor.valueBuffer("criteriocaja")) {	
		temp = "1";
	} else {
		temp = "2";
	}
	contenido1 += temp;
	
	nombreDato = util.translate("scripts", "Destinatario de las operaciones a las que se aplique el régimen especial del criterio de Caja");
	if ((contenido1.length + 1) !=  78) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	if (cursor.valueBuffer("destcriteriocaja")) {	
		temp = "1";
	} else {
		temp = "2";
	}
	contenido1 += temp;
	
	nombreDato = util.translate("scripts", " Opción por la aplicación de la prorrata especial");
	if ((contenido1.length + 1) !=  79) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	if (cursor.valueBuffer("prorrataespecial")) {	
		temp = "1";
	} else {
		temp = "2";
	}
	contenido1 += temp;

	nombreDato = util.translate("scripts", " Revocación de la opción por la aplicación de la prorrata especial");
	if ((contenido1.length + 1) !=  80) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	if (cursor.valueBuffer("revocacionprorrata")) {	
		temp = "1";
	} else {
		temp = "2";
	}
	contenido1 += temp;
	
	nombreDato = util.translate("scripts", "Ejercicio");
	if ((contenido1.length + 1) !=  81) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("fechainicio");
	contenido1 += temp.toString().left(4);

	nombreDato = util.translate("scripts", "Período");
	if ((contenido1.length + 1) !=  85) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	if (cursor.valueBuffer("tipoperiodo") == "Trimestre") {
		temp = cursor.valueBuffer("trimestre");
		if (!flcontmode.iface.pub_verificarDato(temp, true, nombreDato, 2))
			return false;
	} else {
		temp = cursor.valueBuffer("fechainicio");
//		temp = temp.toString().substr(5, 2);
		temp = temp.toString().left(7);
		temp = temp.right(2);
	}
	contenido1 += temp; 
	
	nombreDato = util.translate("scripts", "Base imponible [01]");
	if ((contenido1.length + 1) !=  87) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("baseimponiblerg1");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2);
	
	nombreDato = util.translate("scripts", "Tipo % [02]");
	if ((contenido1.length + 1) !=  104) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("tiporg1");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 3, 2); 
	
	nombreDato = util.translate("scripts", "Cuota [03]");
	if ((contenido1.length + 1) !=  109) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotarg1");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Base imponible [04]");
	if ((contenido1.length + 1) !=  126) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("baseimponiblerg2");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Tipo % [05]");
	if ((contenido1.length + 1) !=  143) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("tiporg2");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 3, 2); 
	
	nombreDato = util.translate("scripts", "Cuota  [06]");
	if ((contenido1.length + 1) !=  148) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotarg2");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Base imponible [07]");
	if ((contenido1.length + 1) !=  165) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("baseimponiblerg3");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Tipo % [08]");
	if ((contenido1.length + 1) !=  182) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("tiporg3");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 3, 2); 
	
	nombreDato = util.translate("scripts", "Cuota [09]");
	if ((contenido1.length + 1) !=  187) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotarg3");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Base imponible por adquisiciones intracomunitarias [10]"); // Antiguo 19
	if ((contenido1.length + 1) !=  204) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("baseimponibleai");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Cuota por adquisiciones intracomunitarias [11]"); // Antiguo 20
	if ((contenido1.length + 1) !=  221) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotaai");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Base Otras operaciones con inversión del sujeto pasivo [12]");
	if ((contenido1.length + 1) !=  238) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("baseimponibleoo");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Cuota Otras operaciones con inversión del sujeto pasivo [13]");
	if ((contenido1.length + 1) !=  255) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotaoo");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 	
	
	nombreDato = util.translate("scripts", "Base modificación bases y cuotas [14]");
	if ((contenido1.length + 1) !=  272) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("baseimponiblembc");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Cuota modificación bases y cuotas [15]");
	if ((contenido1.length + 1) !=  289) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotambc");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 	
	
	nombreDato = util.translate("scripts", "Base imponible recargo equivalencia [16]"); //Antiguo 10
	if ((contenido1.length + 1) !=  306) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("baseimponiblere1");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Tipo % recargo equivalencia [17]"); //Antiguo 11
	if ((contenido1.length + 1) !=  323) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("tipore1");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 3, 2);
	
	nombreDato = util.translate("scripts", "Cuota recargo equivalencia [18]");//Antiguo 12
	if ((contenido1.length + 1) !=  328) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotare1");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Base imponible recargo equivalencia [19]"); //Antiguo 13
	if ((contenido1.length + 1) !=  345) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("baseimponiblere2");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Tipo % recargo equivalencia [20]"); //Antiguo 14
	if ((contenido1.length + 1) !=  362) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("tipore2");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 3, 2); 
	
	nombreDato = util.translate("scripts", "Cuota recargo equivalencia [21]"); //Antiguo 15
	if ((contenido1.length + 1) !=  367) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotare2");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Base imponible recargo equivalencia [22]"); //Antiguo 16
	if ((contenido1.length + 1) !=  384) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("baseimponiblere3");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Tipo % recargo equivalencia [23]"); //Antiguo 17
	if ((contenido1.length + 1) !=  401) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("tipore3");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 3, 2); 
	
	nombreDato = util.translate("scripts", "Cuota recargo equivalencia [24]"); //Antiguo 18
	if ((contenido1.length + 1) !=  406) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotare3");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	
	nombreDato = util.translate("scripts", "Base modificación bases y cuotas del recargdo de equivalencia [25]");
	if ((contenido1.length + 1) !=  423) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("baseimponiblembcrec");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Cuota modificación bases y cuotas del recargdo de equivalencia [26]");
	if ((contenido1.length + 1) !=  440) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotambcre");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 		
		
	nombreDato = util.translate("scripts", "IVA Devengado: Cuota total (03 + 06 + 09 + 11 + 13 + 15 + 18 + 21 + 24 + 26 + 27) [27]"); //Antiguo 21
	if ((contenido1.length + 1) !=  457) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotadevtotal");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible por cuotas soportadas en operaciones interiores corrientes. BI [28]"); //Antiguo 22
	if ((contenido1.length + 1) !=  474) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("basededoibc");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible por cuotas soportadas en operaciones interiores corrientes. Cuota [29]"); //Antiguo 23
	if ((contenido1.length + 1) !=  491) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotadedoibc");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible por cuotas soportadas en operaciones interiores con bienes de inversión. BI [30]"); //Antiguo 24
	if ((contenido1.length + 1) !=  508) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("basededoibi");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible por cuotas soportadas en operaciones interiores con bienes de inversión. Cuota [31]"); //Antiguo 25
	if ((contenido1.length + 1) !=  525) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotadedoibi");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible por cuotas soportadas en las importaciones de bienes corrientes. BI [32]"); //Antiguo 26
	if ((contenido1.length + 1) !=  542) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("basededimbc");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible por cuotas soportadas en las importaciones de bienes corrientes. Cuota [33]"); //Antiguo 27
	if ((contenido1.length + 1) !=  559) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotadedimbc");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 

	nombreDato = util.translate("scripts", "IVA deducible por cuotas soportadas en las importaciones de bienes de inversión. BI [34]"); //Antiguo 28
	if ((contenido1.length + 1) !=  576) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("basededimbi");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible por cuotas soportadas en las importaciones de bienes de inversión. Cuota [35]"); //Antiguo 29
	if ((contenido1.length + 1) !=  593) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotadedimbi");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible en adquisiciones intracomunitarias de bienes corrientes. BI [36]"); //Antiguo 30
	if ((contenido1.length + 1) !=  610) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("basededaibc");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible en adquisiciones intracomunitarias de bienes corrientes. Cuota [37]"); //Antiguo 31
	if ((contenido1.length + 1) !=  627) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotadedaibc");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible en adquisiciones intracomunitarias de bienes de inversión. BI [38]"); //Antiguo 32
	if ((contenido1.length + 1) !=  644) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("basededaibi");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible en adquisiciones intracomunitarias de bienes de inversión. Cuota [39]"); //Antiguo 33
	if ((contenido1.length + 1) !=  661) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotadedaibi");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 	
	
	
	nombreDato = util.translate("scripts", "Base Rectificación de deducciones [40]");
	if ((contenido1.length + 1) !=  678) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("baserecded");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Cuota Rectificación de deducciones [41]");
	if ((contenido1.length + 1) !=  695) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotarecded");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 				
	
	nombreDato = util.translate("scripts", "IVA deducible en compensaciones Régimen Especial A.G. y P. [42]"); //Antiguo 34
	if ((contenido1.length + 1) !=  712) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotacomre");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible: Regularización inversiones [43]"); //Antiguo 35
	if ((contenido1.length + 1) !=  729) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotaregin");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "IVA deducible: Regularización por aplicación del porcentaje def. de prorrata [44]"); //Antiguo 36
	if ((contenido1.length + 1) !=  746) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotaregapli");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 

	nombreDato = util.translate("scripts", "IVA deducible: Total a deducir (29 + 31 + 33 + 35 + 37 + 39 + 41 + 42 + 43 + 44) [45]"); //Antiguo 37
	if ((contenido1.length + 1) !=  763) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotadedtotal");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 

	nombreDato = util.translate("scripts", "IVA Deducible. Resultado régimen general (27 - 45) [46]"); //Antiguo 38
	if ((contenido1.length + 1) !=  780) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotadif");
	contenido1 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 

	nombreDato = util.translate("scripts", "Reservado AEAT");
	if ((contenido1.length + 1) !=  797) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	temp = "";
	contenido1 += flfactppal.iface.pub_espaciosDerecha(temp, 93); 
	
	nombreDato = util.translate("scripts", "Fin registro 1");
	if ((contenido1.length + 1) !=  890) {
		return this.iface.errorAcumuladoControl(contenido1.length + 1, nombreDato);
	}
	contenido1 += "</T30301>"; 
	
	temp = String.fromCharCode(13, 10)
	contenido1 += temp;
	
	/// FIN 1	
	
	/// INICIO 2
	var contenido2 = "";
	/// FIN 2
	
	/// INICIO 3
	var contenido3 = "";
	
	nombreDato = util.translate("scripts", "Inicio de Id. de modelo y página");
	if ((contenido3.length + 1) !=  1) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}
	contenido3 += "<T";
	
	nombreDato = util.translate("scripts", "Modelo");
	if ((contenido3.length + 1) !=  3) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}
	contenido3 += "303";
	
	nombreDato = util.translate("scripts", "Página");
	if ((contenido3.length + 1) !=  6) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}
	contenido3 += "03";
	
	nombreDato = util.translate("scripts", "Fin de Id. de modelo y página");
	if ((contenido3.length + 1) !=  8) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}
	contenido3 += ">";
	
	nombreDato = util.translate("scripts", "Entregas intracomunitarias [59]"); //Antiguo 42
	if ((contenido3.length + 1) !=  9) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("entregasi");
	contenido3 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 

	nombreDato = util.translate("scripts", "Exportaciones y operaciones asimiladas [60]"); //Antiguo 43
	if ((contenido3.length + 1) !=  26) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("exportaciones");
	contenido3 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Operaciones no sujetas o con inversión del sujeto pasivo. Derecho a deducción [61]"); //Antiguo 44
	if ((contenido3.length + 1) !=  43) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("nosujetas");
	contenido3 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Resultado: Suma de resultados [64]"); 
	if ((contenido3.length + 1) !=  60) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("sumaresultados");
	contenido3 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 	


	nombreDato = util.translate("scripts", "Atribuible a la administración del estado - % [65]"); //Antiguo 39
	if ((contenido3.length + 1) !=  77) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("porcuotaestado");
	contenido3 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 3, 2); 
	
	nombreDato = util.translate("scripts", "Atribuible a la Administración del Estado [66]"); //Antiguo 40
	if ((contenido3.length + 1) !=  82) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotaestado");
	contenido3 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Cuota a compensar de periodos anteriores [67]"); //Antiguo 41
	if ((contenido3.length + 1) !=  99) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotaanterior");
	contenido3 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Cuota exclusiva para sujetos pasivos que tributan conjuntamente a la Administración del Estado y a las Diputaciones Forales [68]"); //Antiguo 45
	if ((contenido3.length + 1) !=  116) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("sujetospasivos");
	contenido3 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Resultado (66-67+-68) [69]"); //Antiguo 46
	if ((contenido3.length + 1) !=  133) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuotaresultado");
	contenido3 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Importe a deducir [70]"); //Antiguo 47
	if ((contenido3.length + 1) !=  150) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("adeducircompl");
	contenido3 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Resultado de la liquidación (69 - 70) [71]"); //Antiguo 48
	if ((contenido3.length + 1) !=  167) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("resliquid");
	contenido3 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 

	nombreDato = util.translate("scripts", "CRITERIO CAJA: Base imponible entregas [62]");
	if ((contenido3.length + 1) !=  184) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}	
	temp = cursor.valueBuffer("baseentregascc");
	contenido3 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2);
	
	nombreDato = util.translate("scripts", "CRITERIO CAJA: Cuota entregas [63]");
	if ((contenido3.length + 1) !=  201) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}	
	temp = cursor.valueBuffer("cuotaentregascc");
	contenido3 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2);
	
	nombreDato = util.translate("scripts", "CRITERIO CAJA: Base imponible adquisiciones [74]");
	if ((contenido3.length + 1) !=  218) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}	
	temp = cursor.valueBuffer("baseadquisicionescc");
	contenido3 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2);
	
	nombreDato = util.translate("scripts", "CRITERIO CAJA: Cuota adquisiciones [75]");
	if ((contenido3.length + 1) !=  235) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}	
	temp = cursor.valueBuffer("cuotaadquisicionescc");
	contenido3 += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2);
	
	nombreDato = util.translate("scripts", "Declaración complementaria");
	if ((contenido3.length + 1) !=  252) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}	
	if (cursor.valueBuffer("complementaria")) {
		temp = "X";
	} else {
		temp = " ";
	}	
	contenido3 += temp;
	//contenido3 += flfactppal.iface.pub_cerosIzquierda(temp, 1);	
	
	nombreDato = util.translate("scripts", "Numero de justificante de la declaracion anterior");
	if ((contenido3.length + 1) !=  253) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("numjustificante");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Numero de justificante de la declaracion anterior"), 13))
		return false;
	contenido3 += flfactppal.iface.pub_espaciosDerecha(temp, 13);
	
	nombreDato = util.translate("scripts", "Sin actividad");
	if ((contenido3.length + 1) !=  266) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}
	if (cursor.valueBuffer("sinactividad")) {
		temp = "X";
	} else {
		temp = " ";
	}
	contenido3 += temp;
	
	var codCuenta = cursor.valueBuffer("codcuentadev");
	if (!codCuenta) {
        MessageBox.warning(util.translate("Debe indicar la cuenta de devolución (aunque el resultado sea a ingresar) para obtener el IBAN"), MessageBox.Ok, MessageBox.NoButton);
		return false;
	}
	var iban = AQUtil.sqlSelect("cuentasbanco", "iban", "codcuenta = '" + codCuenta + "'");
	if (!iban) {
        MessageBox.warning(util.translate("Debe informar el IBAN de la cuenta %1").arg(codCuenta), MessageBox.Ok, MessageBox.NoButton);
		return false;
	}
	nombreDato = util.translate("scripts", "IBAN");
	if ((contenido3.length + 1) !=  267) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}
	contenido3 += flfactppal.iface.pub_espaciosDerecha(iban, 34); 
	
	nombreDato = util.translate("scripts", "Reservado AEAT");
	if ((contenido3.length + 1) !=  301) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}
	temp = "";
	contenido3 += flfactppal.iface.pub_espaciosDerecha(temp, 289); 
	
	nombreDato = util.translate("scripts", "Fin registro 1");
	if ((contenido3.length + 1) !=  590) {
		return this.iface.errorAcumuladoControl(contenido3.length + 1, nombreDato);
	}
	contenido3 += "</T30303>"; 
	
	temp = String.fromCharCode(13, 10)
	contenido3 += temp;
	
	contenido += contenido1 + contenido2 + contenido3;
	
	contenido += "</T3030";
	
	temp = cursor.valueBuffer("fechainicio");
	contenido += temp.toString().left(4);

	if (cursor.valueBuffer("tipoperiodo") == "Trimestre") {
		temp = cursor.valueBuffer("trimestre");
		if (!flcontmode.iface.pub_verificarDato(temp, true, nombreDato, 2))
			return false;
	} else {
		temp = cursor.valueBuffer("fechainicio");
//		temp = temp.toString().substr(5, 2);
		temp = temp.toString().left(7);
		temp = temp.right(2);
	}
	contenido += temp; 
	contenido += "0000>";
	
	temp = String.fromCharCode(13, 10);
	contenido += temp;
	
	/// XXX
	/*nombreDato = util.translate("scripts", "Página complementaria");
	if ((contenido2.length + 1) !=  9) {
		return this.iface.errorAcumuladoControl(contenido2.length + 1, nombreDato);
	}
	contenido2 += " ";	
	
	nombreDato = util.translate("scripts", "Datos C1");
	if ((contenido2.length + 1) !=  9) {
		return this.iface.errorAcumuladoControl(contenido2.length + 1, nombreDato);
	}
	temp = "";
	contenido2 += flfactppal.iface.pub_cerosIzquierda(temp, 701);	
	
	
	nombreDato = util.translate("scripts", "Importe a compensar en caso de que la casilla 48 resulte negativa [49]");
	if ((contenido.length + 1) !=  930) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("impcompensar");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	
	nombreDato = util.translate("scripts", "Sin actividad");
	if ((contenido.length + 1) !=  947) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	if (cursor.valueBuffer("sinactividad")) {
		temp = "1";
	} else {
		temp = "0";
	}
	contenido += temp;
	
	nombreDato = util.translate("scripts", "Importe a devolver [50]");
	if ((contenido.length + 1) !=  947) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("imported");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 
	

	nombreDato = util.translate("scripts", "Fin de Id. de modelo y página");
	if ((contenido.length + 1) !=  7) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	contenido += ">";
	
	nombreDato = util.translate("scripts", "Indicador de página complementaria");
	if ((contenido.length + 1) !=  9) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	contenido += " ";
	
	nombreDato = util.translate("scripts", "Tipo de declaración");
	if ((contenido.length + 1) !=  10) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	var temp:String = cursor.valueBuffer("idtipodec");
	if (!flcontmode.iface.pub_verificarDato(temp, true, nombreDato, 1)) {
		return false;
	}
	contenido += temp;
	
	nombreDato = util.translate("scripts", "NIF");
	if ((contenido.length + 1) !=  11) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = flcontmode.iface.pub_valorDefectoDatosFiscales("cifnif");
	if (!flcontmode.iface.pub_verificarDato(temp, true, nombreDato, 9))
		return false;
	contenido += temp; 
	
	nombreDato = util.translate("scripts", "Apellidos o razón social");
	if ((contenido.length + 1) !=  20) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	
	if (flcontmode.iface.pub_valorDefectoDatosFiscales("personafisica")) {
		temp = flcontmode.iface.pub_valorDefectoDatosFiscales("apellidospf");
	} else {
		temp = flcontmode.iface.pub_valorDefectoDatosFiscales("apellidosrs");
	}

	if (!flcontmode.iface.pub_verificarDato(temp, true, nombreDato, 30))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 30); 
	
	nombreDato = util.translate("scripts", "Nombre");
	if ((contenido.length + 1) !=  50) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = flcontmode.iface.pub_valorDefectoDatosFiscales("nombrepf");
	if (!flcontmode.iface.pub_verificarDato(temp, false, nombreDato, 15))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 15); 
	
	nombreDato = util.translate("scripts", "Inscrito en Registro de devolución mensual");
	if ((contenido.length + 1) !=  65) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	if (cursor.valueBuffer("inscritoregdev")) {
		temp = "1";
	} else {
		temp = "2";
	}
	contenido += temp;	
	

	
	
	
	
	
	nombreDato = util.translate("scripts", "Devolución código cuenta cliente - Entidad");
	if ((contenido.length + 1) !=  839) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("ctaentidaddev");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Cuenta de devolución: Entidad "), 4))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 4); 
	
	nombreDato = util.translate("scripts", "Devolución código cuenta cliente - Oficina");
	if ((contenido.length + 1) !=  843) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("ctaagenciadev");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Cuenta de devolución: Oficina "), 4))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 4); 
	
	nombreDato = util.translate("scripts", "Devolución código cuenta cliente - DC");
	if ((contenido.length + 1) !=  847) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("dcdev");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Cuenta de devolución: Dígito de control"), 2))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 2); 
	
	nombreDato = util.translate("scripts", "Devolución código cuenta cliente - Número de cuenta");
	if ((contenido.length + 1) !=  849) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuentadev");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Cuenta de devolución: Nº cuenta"), 10))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 10); 

	nombreDato = util.translate("scripts", "Forma de pago");
	if ((contenido.length + 1) !=  859) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("formapago");
	if (temp == "") {
		temp = "0";
	}
	contenido += temp.left(1); 

	nombreDato = util.translate("scripts", "Importe a ingresar [50]");
	if ((contenido.length + 1) !=  860) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("importei");
	contenido += flcontmode.iface.pub_formatoNumero(parseFloat(temp), 15, 2); 

	
	nombreDato = util.translate("scripts", "Ingreso código cuenta cliente - Entidad");
	if ((contenido.length + 1) !=  877) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("ctaentidadingreso");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Cuenta de ingreso: Entidad"), 4))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 4); 

	nombreDato = util.translate("scripts", "Ingreso código cuenta cliente - Oficina");
	if ((contenido.length + 1) !=  881) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("ctaagenciaingreso");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Cuenta de ingreso: Oficina "), 4))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 4); 

	nombreDato = util.translate("scripts", "Ingreso código cuenta cliente - DC");
	if ((contenido.length + 1) !=  885) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("dcingreso");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Cuenta de ingreso: Dígito de control"), 2))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 2); 

	nombreDato = util.translate("scripts", "Ingreso código cuenta cliente - Número de cuenta");
	if ((contenido.length + 1) !=  887) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("cuentaingreso");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Cuenta de ingreso: Nº cuenta"), 10))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 10); 

	nombreDato = util.translate("scripts", "Autoliquidación complementaria");
	if ((contenido.length + 1) !=  897) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	if (cursor.valueBuffer("complementaria")) {
		temp = "1";
	} else {
		temp = "0";
	}
	contenido += temp;
	
	nombreDato = util.translate("scripts", "Numero de justificante de la declaracion anterior");
	if ((contenido.length + 1) !=  898) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("numjustificante");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Numero de justificante de la declaracion anterior"), 13))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 13); 

	nombreDato = util.translate("scripts", "Campo reservado");
	if ((contenido.length + 1) !=  911) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = "";
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 400); 

	nombreDato = util.translate("scripts", "Localidad de la firma");
	if ((contenido.length + 1) !=  1311) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("localidadfirma");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Localidad de la firma"), 16))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(temp, 16); 

	nombreDato = util.translate("scripts", "Día de la firma");
	if ((contenido.length + 1) !=  1327) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("fechafirma");
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Fecha firma"), 19))
		return false;
	contenido += flfactppal.iface.pub_cerosIzquierda(temp.getDate(), 2);

	nombreDato = util.translate("scripts", "Mes de la firma");
	if ((contenido.length + 1) !=  1329) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("fechafirma");
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Fecha firma"), 19))
		return false;
	contenido += flfactppal.iface.pub_espaciosDerecha(flcontmode.iface.pub_mesPorIndice(temp.getMonth()), 10);

	nombreDato = util.translate("scripts", "Año de la firma");
	if ((contenido.length + 1) !=  1339) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	temp = cursor.valueBuffer("fechafirma");
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Fecha firma"), 19))
		return false;
	contenido += flfactppal.iface.pub_cerosIzquierda(temp.getYear(), 4);
	
	nombreDato = util.translate("scripts", "Identificador de Fin de registro");
	if ((contenido.length + 1) != 1343) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
	contenido += "</T30301>";
	
	nombreDato = util.translate("scripts", "Fin de registro");
	if ((contenido.length + 1) != 1352) {
		return this.iface.errorAcumuladoControl(contenido.length + 1, nombreDato);
	}
// 	temp = "\n";
	temp = String.fromCharCode(13, 10);
	contenido += temp;*/
	
	file.write(contenido);
	file.close();

	MessageBox.information(util.translate("scripts", "El fichero se ha generado en :\n\n" + nombreFichero + "\n\n"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
}


function oficial_errorAcumuladoControl(acumuladoControl:Number, nombreDato:String):Boolean
{
	var util:FLUtil = new FLUtil;
	MessageBox.warning(util.translate("scripts", "Error al crear el fichero: El dato %1 no comienza en la posición %2").arg(nombreDato).arg(acumuladoControl), MessageBox.Ok, MessageBox.NoButton);
	return false;
}
function oficial_formatoFecha(fecha) {
  var res = fecha.substring(0, 4) + fecha.substring(5, 7) + fecha.substring(8, 10);
  return res;
}
//// OFICIAL /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////

//// DESARROLLO /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////
//// INTERFACE  /////////////////////////////////////////////////

//// INTERFACE  /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
