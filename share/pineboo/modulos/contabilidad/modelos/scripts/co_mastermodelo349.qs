/***************************************************************************
                 co_mastermodelo349.qs  -  description
                             -------------------
    begin                : jue mar 12 2009
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
	function presTelematica2000() {
		return this.ctx.oficial_presTelematica2000();
	}
	function presTelematica2009() {
		return this.ctx.oficial_presTelematica2009();
	}
	function presTelematica2010() {
		return this.ctx.oficial_presTelematica2010();
	}
}
//// OFICIAL /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration boe2011 */
//////////////////////////////////////////////////////////////////
//// BOE2011 /////////////////////////////////////////////////////
class boe2011 extends oficial {
    function boe2011( context ) { oficial( context ); }
    function presTelematica() {
        return this.ctx.boe2011_presTelematica();
    }
    function presTelematica2011() {
        return this.ctx.boe2011_presTelematica2011();
    }
    function nombreFichero():String {
        return this.ctx.boe2011_nombreFichero();
    }
    function soporteModelo():String{
        return this.ctx.boe2011_soporteModelo();
    }
    function tiporeg1(curMod:FLSlqCursor):String {
        return this.ctx.boe2011_tiporeg1(curMod);
    }
    function tiporeg2(curMod:FLSlqCursor,curMod2:FlsqlCursor):String {
        return this.ctx.boe2011_tiporeg2(curMod,curMod2);
    }
    function tiporeg2r(curMod:FLSlqCursor,curMod2r:FlsqlCursor):String {
        return this.ctx.boe2011_tiporeg2r(curMod,curMod2r);
    }
}
//// BOE2011 /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////
class head extends boe2011 {
	function head( context ) { boe2011 ( context ); }
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
	connect (this.child("toolButtonPrint"), "clicked()", this, "iface.lanzar()");
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
	var util:FLUtil = new FLUtil;
	var cursor:FLSqlCursor = this.cursor();

	var dialogo = new Dialog;
	dialogo.caption = util.translate("scripts", "Imprimir modelo 349");
	dialogo.okButtonText = util.translate("scripts", "Aceptar");
	dialogo.cancelButtonText = util.translate("scripts", "Cancelar");

	var chkDR = new CheckBox;
	chkDR.text = util.translate("scripts", "Declaración recapitulativa");
	chkDR.checked = true;
	dialogo.add(chkDR);

	var chkOperaciones = new CheckBox;
	chkOperaciones.text = util.translate("scripts", "Relación de operaciones");
	chkOperaciones.checked = true;
	dialogo.add(chkOperaciones);

	var chkRectificaciones = new CheckBox;
	chkRectificaciones.text = util.translate("scripts", "Rectificaciones");
	chkRectificaciones.checked = true;
	dialogo.add(chkRectificaciones);

	if (!dialogo.exec())
		return;

	var nombreInforme:String;
	if (chkDR.checked) {
		nombreInforme = cursor.action();
		flcontmode.iface.pub_lanzar(cursor, nombreInforme, nombreInforme + ".idmodelo = " + cursor.valueBuffer( "idmodelo" ) );
	}
	if (chkOperaciones.checked) {
		nombreInforme = "co_modelo349_op";
		flcontmode.iface.pub_lanzar(cursor, nombreInforme, "co_modelo349.idmodelo = " + cursor.valueBuffer( "idmodelo" ) );
	}
	if (chkRectificaciones.checked) {
		nombreInforme = "co_modelo349_re";
		flcontmode.iface.pub_lanzar(cursor, nombreInforme, "co_modelo349.idmodelo = " + cursor.valueBuffer( "idmodelo" ) );
	}
}

/** \D Genera un fichero para realizar la presentación telemática del modelo
\end */
function oficial_presTelematica()
{
	var util:FLUtil = new FLUtil();
	var cursor:FLSqlCursor = this.cursor();
	if (!cursor.isValid()) {
		return;
	}

	// Ejercicio
	var ejercicio:String;
	var temp:String = util.sqlSelect("ejercicios", "fechainicio", "codejercicio = '" + cursor.valueBuffer("codejercicio") + "'");
	ejercicio = temp.toString().left(4);
	if(parseInt(ejercicio) < 2009)
		this.iface.presTelematica2000();
	else {
		switch (ejercicio) {
			case "2009": {
				this.iface.presTelematica2009();
				break;
			}
			default: {
				this.iface.presTelematica2010();
			}
		}
	}
}

function oficial_presTelematica2000()
{
	var util:FLUtil = new FLUtil();
	var cursor:FLSqlCursor = this.cursor();

	// Ejercicio
	var ejercicio:String;
	var temp:String = util.sqlSelect("ejercicios", "fechainicio", "codejercicio = '" + cursor.valueBuffer("codejercicio") + "'");
	ejercicio = temp.toString().left(4);
	
	// Tipo de soporte
	var tipoSoporte:String;
	var presTelematica:String = util.translate("scripts", "Transmisión telemática");
	var disquete:String = util.translate("scripts", "Disquete");
	var cintaMagnetica:String = util.translate("scripts", "Cinta magnética");
	var soportes:Array = [presTelematica, disquete, cintaMagnetica];
	var opcion:String = Input.getItem(util.translate("scripts", "Indique el tipo de soporte"), soportes, presTelematica, false);
	if (!opcion)
		return;
	switch (opcion) {
		case presTelematica:
			tipoSoporte = "T";
			break;
		case disquete:
			tipoSoporte = "D";
			break;
		case cintaMagnetica:
			tipoSoporte = "C";
			break;
	}
	
	var nombreFichero:String = FileDialog.getSaveFileName("*.*");
	if (!nombreFichero)
		return;
		
	var file:Object = new File(nombreFichero);
	file.open(File.WriteOnly);

	// Ejercicio

	file.write("1"); // Tipo de registro (Declarante)
	file.write("349"); // Modelo
		
	// Ejercicio
	file.write(ejercicio); 
	
	// CIF
	var nifDeclarante:String;
	temp = flcontmode.iface.pub_valorDefectoDatosFiscales("cifnif");
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "CIF"), 9))
		return false;
	nifDeclarante = flfactppal.iface.pub_espaciosDerecha(temp, 9);
	file.write(nifDeclarante); 
	
	// Apellidos y nombre o razón social
	temp = flcontmode.iface.pub_valorDefectoDatosFiscales("apellidosrs");// + " " + flcontmode.iface.pub_valorDefectoDatosFiscales("nombre");
debug(temp);
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Apellidos o razón social"), 40))
		return false;
	temp = flcontmode.iface.pub_controlCaracteres(temp);
	file.write(flfactppal.iface.pub_espaciosDerecha(temp, 40)); 
	
	// Tipo de soporte
	file.write(tipoSoporte); 
	
	// Persona con quien relacionarse (teléfono)
	temp = cursor.valueBuffer("telefonorel");
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Persona con quien relacionarse (teléfono)"), 9))
		return false;
	file.write(flfactppal.iface.pub_espaciosDerecha(temp, 9));
	
	// Persona con quien relacionarse (apellidos y nombre)
	temp = cursor.valueBuffer("personarel");
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Persona con quien relacionarse (apellidos y nombre)"), 40))
		return false;
	temp = flcontmode.iface.pub_controlCaracteres(temp);
	file.write(flfactppal.iface.pub_espaciosDerecha(temp, 40)); 
	
	// Número de justificante
	temp = cursor.valueBuffer("numjustificante");
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Número de justificante"), 13))
		return false;
	file.write(flfactppal.iface.pub_cerosIzquierda(temp, 13)); 
	
	// Declaración complementaria
	if (cursor.valueBuffer("complementaria"))
		temp = "C";
	else
		temp = " ";
	file.write(temp); 
	
	// Declaración sustitutiva
	if (cursor.valueBuffer("sustitutiva"))
		temp = "S";
	else
		temp = " ";
	file.write(temp); 
	
	// Número de justificante de la declaración anterior
	temp = cursor.valueBuffer("numdecanterior");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Número de justificante de la declaración anterior"), 13))
		return false;
	file.write(flfactppal.iface.pub_cerosIzquierda(temp, 13)); 
	
	// Período
	temp = cursor.valueBuffer("periodo");
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Período"), 2))
		return false;
	file.write(temp); 
	
	// Número total de operadores intracomunitarios
	temp = parseFloat(cursor.valueBuffer("numtotaloi"));
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Número total de operadores intracomunitarios"), 9))
		return false;
	file.write(flfactppal.iface.pub_cerosIzquierda(temp, 9)); 
	
	// Importe de las operaciones intracomunitarias
	temp = cursor.valueBuffer("importetotaloi");
	file.write(flcontmode.iface.pub_formatoNumeroAbs(parseFloat(temp), 13, 2)); 
	
	// Número total de operadores intracomunitarios con rectificaciones
	temp = parseFloat(cursor.valueBuffer("numtotaloirec"));
	if (temp || temp == "")
		temp = "0";
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Número total de operadores intracomunitarios con rectificaciones"), 9))
		return false;
	file.write(flfactppal.iface.pub_cerosIzquierda(temp, 9)); 
	
	// Importe de las rectificaciones
	temp = cursor.valueBuffer("importetotaloirec");
	file.write(flcontmode.iface.pub_formatoNumeroAbs(parseFloat(temp), 13, 2)); 
	
	// Relleno hasta 250
	file.write(flfactppal.iface.pub_espaciosDerecha("", 65));
	
	// Fin de registro
	temp = "\n";
	file.write(temp);
	
	//Registros tipo 2 (Operación)
	var qryMod349Tipo2:FLSqlQuery = new FLSqlQuery();
	qryMod349Tipo2.setTablesList("co_operaciones349");
	qryMod349Tipo2.setSelect("codue, cifnif, nombre, clave, baseimponible");
	qryMod349Tipo2.setFrom("co_operaciones349");
	qryMod349Tipo2.setWhere("idmodelo = " + cursor.valueBuffer("idmodelo"));
	if (!qryMod349Tipo2.exec()) {
		MessageBox.critical(util.translate("scripts", "Hubo un error al acceder a los datos de registros de operaciones.\nEl fichero no se ha podido generar correctamente"), MessageBox.Ok, MessageBox.NoButton);
		return;
	}
	var codUE:String;
	while (qryMod349Tipo2.next()) {
		file.write("2"); // Tipo de registro
		file.write("349"); // Modelo
		
		// Ejercicio
		file.write(ejercicio); 
		
		// NIF del declarante
		file.write(nifDeclarante); 
		
		// Relleno hasta 75
		file.write(flfactppal.iface.pub_espaciosDerecha("", 58));
	
		// Código del país
		temp = qryMod349Tipo2.value("codue");
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Código del país"), 2))
			return false;
		codUE = temp;
		file.write(flfactppal.iface.pub_cerosIzquierda(temp, 2)); 
		
		// NIF del operador
		temp = qryMod349Tipo2.value("cifnif");
		if (temp && temp != "")
			if (temp.startsWith(codUE))
				temp = temp.right(temp.length - 2);
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "NIF del operador"), 15))
			return false;
		file.write(flfactppal.iface.pub_espaciosDerecha(temp, 15)); 
	
		// Nombre del operador
		temp = qryMod349Tipo2.value("nombre");
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Nombre del operador"), 40))
			return false;
		temp = flcontmode.iface.pub_controlCaracteres(temp);
		file.write(flfactppal.iface.pub_espaciosDerecha(temp, 40)); 
	
		// Clave de operacion
		temp = qryMod349Tipo2.value("clave");
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Clave de operacion"), 1))
			return false;
		file.write(flfactppal.iface.pub_espaciosDerecha(temp, 1));
		
		// Importe de las rectificaciones
		temp = qryMod349Tipo2.value("baseimponible");
		file.write(flcontmode.iface.pub_formatoNumeroAbs(parseFloat(temp), 11, 2)); 
	
		// Relleno hasta 250
		file.write(flfactppal.iface.pub_espaciosDerecha("", 104));
		
		// Fin de registro
		temp = "\n";
		file.write(temp);
	}
	
	//Registros tipo 3 (Rectificación)
	var qryMod349Tipo2:FLSqlQuery = new FLSqlQuery();
	qryMod349Tipo2.setTablesList("co_rectificaciones349");
	qryMod349Tipo2.setSelect("codue, cifnif, nombre, clave, codejercicio, periodo, birectificada, bianterior");
	qryMod349Tipo2.setFrom("co_rectificaciones349");
	qryMod349Tipo2.setWhere("idmodelo = " + cursor.valueBuffer("idmodelo"));
	if (!qryMod349Tipo2.exec()) {
		MessageBox.critical(util.translate("scripts", "Hubo un error al acceder a los datos de registros de operaciones.\nEl fichero no se ha podido generar correctamente"), MessageBox.Ok, MessageBox.NoButton);
		return;
	}
	while (qryMod349Tipo2.next()) {
		file.write("2"); // Tipo de registro
		file.write("349"); // Modelo
		
		// Ejercicio
		file.write(ejercicio); 
		
		// NIF del declarante
		file.write(nifDeclarante); 
		
		// Relleno hasta 75
		file.write(flfactppal.iface.pub_espaciosDerecha("", 58));
	
		// Código del país
		temp = qryMod349Tipo2.value("codue");
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Código del país"), 2))
			return false;
		codUE = temp;
		file.write(flfactppal.iface.pub_cerosIzquierda(temp, 2)); 
		
		// NIF del operador
		temp = qryMod349Tipo2.value("cifnif");
		if (temp && temp != "")
			if (temp.startsWith(codUE))
				temp = temp.right(temp.length - 2);
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "NIF del operador"), 15))
			return false;
		file.write(flfactppal.iface.pub_espaciosDerecha(temp, 15)); 
	
		// Nombre del operador
		temp = qryMod349Tipo2.value("nombre");
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Nombre del operador"), 40))
			return false;
		temp = flcontmode.iface.pub_controlCaracteres(temp);
		file.write(flfactppal.iface.pub_espaciosDerecha(temp, 40)); 
	
		// Clave de operacion
		temp = qryMod349Tipo2.value("clave");
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Clave de operacion"), 1))
			return false;
		file.write(flfactppal.iface.pub_espaciosDerecha(temp, 1));
		
		// Relleno hasta 146
		file.write(flfactppal.iface.pub_espaciosDerecha("", 13));
		
		// Ejercicio rectificado
		temp = util.sqlSelect("ejercicios", "fechainicio", "codejercicio = '" + qryMod349Tipo2.value("codejercicio") + "'");
		temp = temp.toString().left(4); 
		file.write(temp); 
	
		// Período rectificado
		temp = qryMod349Tipo2.value("periodo");
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Período rectificado"), 2))
			return false;
		file.write(flfactppal.iface.pub_espaciosDerecha(temp, 2));
		
		// Base imponible rectificada
		temp = qryMod349Tipo2.value("birectificada");
		file.write(flcontmode.iface.pub_formatoNumeroAbs(parseFloat(temp), 11, 2)); 
	
		// Base imponible declarada anteriormente
		temp = qryMod349Tipo2.value("bianterior");
		file.write(flcontmode.iface.pub_formatoNumeroAbs(parseFloat(temp), 11, 2)); 
	
		// Relleno hasta 250
		file.write(flfactppal.iface.pub_espaciosDerecha("", 72));
		
		// Fin de registro
		temp = "\n";
		file.write(temp);
	}
	
	file.close();

	MessageBox.information(util.translate("scripts", "Generado fichero en :\n\n" + nombreFichero + "\n\n"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
}

/** \D Genera un fichero para realizar la presentación telemática del modelo
\end */
function oficial_presTelematica2009()
{
	var util:FLUtil = new FLUtil();
	var cursor:FLSqlCursor = this.cursor();
	if (!cursor.isValid()) {
		return;
	}

	// Ejercicio
	var ejercicio:String;
	var temp:String = util.sqlSelect("ejercicios", "fechainicio", "codejercicio = '" + cursor.valueBuffer("codejercicio") + "'");
	ejercicio = temp.toString().left(4);
	
	// Tipo de soporte
	var tipoSoporte:String;
	var presTelematica:String = util.translate("scripts", "Transmisión telemática");
	var disquete:String = util.translate("scripts", "Disquete");
	var cintaMagnetica:String = util.translate("scripts", "Cinta magnética");
	var soportes:Array = [presTelematica, disquete, cintaMagnetica];
	var opcion:String = Input.getItem(util.translate("scripts", "Indique el tipo de soporte"), soportes, presTelematica, false);
	if (!opcion)
		return;
	switch (opcion) {
		case presTelematica:
			tipoSoporte = "T";
			break;
		case disquete:
			tipoSoporte = "D";
			break;
		case cintaMagnetica:
			tipoSoporte = "C";
			break;
	}
	
	var nombreFichero:String = FileDialog.getSaveFileName("*.*");
	if (!nombreFichero)
		return;
		
	var file:Object = new File(nombreFichero);
	file.open(File.WriteOnly);

	file.write("1"); /// Tipo de registro (Declarante) 1 - 1 (1)
	file.write("349"); /// Modelo 2 - 4 (3)
		
	/// Ejercicio 5 - 8 (4)
	file.write(ejercicio); 
	
	/// CIF 9 - 17 (9)
	var nifDeclarante:String;
	temp = flcontmode.iface.pub_valorDefectoDatosFiscales("cifnif");
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "CIF"), 9))
		return false;
	nifDeclarante = flfactppal.iface.pub_espaciosDerecha(temp, 9);
	file.write(nifDeclarante); 
	
	/// Apellidos y nombre o razón social 18 - 57 (40)
	temp = flcontmode.iface.pub_valorDefectoDatosFiscales("apellidosrs");// + " " + flcontmode.iface.pub_valorDefectoDatosFiscales("nombre");
debug(temp);
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Apellidos o razón social"), 40))
		return false;
	temp = flcontmode.iface.pub_controlCaracteres(temp);
	file.write(flfactppal.iface.pub_espaciosDerecha(temp, 40)); 
	
	/// Tipo de soporte 58 - 58 (1)
	file.write(tipoSoporte); 
	
	/// Persona con quien relacionarse (teléfono) 59 - 67 (9)
	temp = cursor.valueBuffer("telefonorel");
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Persona con quien relacionarse (teléfono)"), 9))
		return false;
	file.write(flfactppal.iface.pub_espaciosDerecha(temp, 9));
	
	/// Persona con quien relacionarse (apellidos y nombre) 59 - 107 (39)
	temp = cursor.valueBuffer("personarel");
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Persona con quien relacionarse (apellidos y nombre)"), 40))
		return false;
	temp = flcontmode.iface.pub_controlCaracteres(temp);
	file.write(flfactppal.iface.pub_espaciosDerecha(temp, 40)); 
	
	/// Número de justificante 108 - 120 (13)
	temp = cursor.valueBuffer("numjustificante");
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Número de justificante"), 13))
		return false;
	file.write(flfactppal.iface.pub_cerosIzquierda(temp, 13)); 
	
	/// Declaración complementaria 121 - 121 (1)
	if (cursor.valueBuffer("complementaria"))
		temp = "C";
	else
		temp = " ";
	file.write(temp); 
	
	/// Declaración sustitutiva 122 - 122 (1)
	if (cursor.valueBuffer("sustitutiva"))
		temp = "S";
	else
		temp = " ";
	file.write(temp); 
	
	/// Número de justificante de la declaración anterior 123 - 135 (13)
	temp = cursor.valueBuffer("numdecanterior");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Número de justificante de la declaración anterior"), 13))
		return false;
	file.write(flfactppal.iface.pub_cerosIzquierda(temp, 13)); 
	
	/// Período 136 - 137 (2)
	var nombreDato:String;
	switch (cursor.valueBuffer("tipoperiodo")) {
		case "Mes": {
			nombreDato = util.translate("scripts", "Mes");
			temp = cursor.valueBuffer("mes");
			break;
		}
		case "Trimestre": {
			nombreDato = util.translate("scripts", "Trimestre");
			temp = cursor.valueBuffer("periodo");
			break;
		}
		case "Año": {
			nombreDato = util.translate("scripts", "Año");
			temp = "0A";
			break;
		}
	}
	if (!flcontmode.iface.pub_verificarDato(temp, true, nombreDato, 2)) {
		return false;
	}
// 	temp = cursor.valueBuffer("periodo");
// 	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Período"), 2))
// 		return false;
	file.write(temp); 
	
	/// Número total de operadores intracomunitarios 138 - 146 (9)
	temp = parseFloat(cursor.valueBuffer("numtotaloi"));
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Número total de operadores intracomunitarios"), 9))
		return false;
	file.write(flfactppal.iface.pub_cerosIzquierda(temp, 9)); 
	
	/// Importe de las operaciones intracomunitarias 147 - 161 (15)
	temp = cursor.valueBuffer("importetotaloi");
	file.write(flcontmode.iface.pub_formatoNumeroAbs(parseFloat(temp), 13, 2)); 
	
	/// Número total de operadores intracomunitarios con rectificaciones 162 - 170 (9)
	temp = parseFloat(cursor.valueBuffer("numtotaloirec"));
	if (temp || temp == "")
		temp = "0";
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Número total de operadores intracomunitarios con rectificaciones"), 9))
		return false;
	file.write(flfactppal.iface.pub_cerosIzquierda(temp, 9)); 
	
	/// Importe de las rectificaciones 171 - 185 (15)
	temp = cursor.valueBuffer("importetotaloirec");
	file.write(flcontmode.iface.pub_formatoNumeroAbs(parseFloat(temp), 13, 2)); 
	
	/// Indicador de cambio en la periodicidad 186 - 186 (1)
	temp = (cursor.valueBuffer("cambioperiodicidad") ? "X" : " ");
	file.write(temp); 
	
	/// Relleno hasta 187 - 250 (64)
	file.write(flfactppal.iface.pub_espaciosDerecha("", 64));
	
/** Parcheado porque la ayuda de informativas espera 250 para 2009, aunque la descripción 2009 indica 500 caracteres
	/// Relleno hasta 187 - 390 (204)
	file.write(flfactppal.iface.pub_espaciosDerecha("", 204));
	
	/// Nif representante legal 391 - 399 (9)
	temp = cursor.valueBuffer("cifnifreplegal");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "CIF Rep.Legal"), 9)) {
		return false;
	}
	var nifRepLegal:String = flfactppal.iface.pub_espaciosDerecha(temp, 9);
	file.write(nifRepLegal);

	/// Relleno a blancos 400 - 487 (88)
	file.write(flfactppal.iface.pub_espaciosDerecha("", 88));
	
	/// Sello electrónico 488 - 500 (13)
	file.write(flfactppal.iface.pub_espaciosDerecha("", 13));
*/

	// Fin de registro
	temp = "\n";
	file.write(temp);
	
	//Registros tipo 2 (Operación)
	var qryMod349Tipo2:FLSqlQuery = new FLSqlQuery();
	qryMod349Tipo2.setTablesList("co_operaciones349");
	qryMod349Tipo2.setSelect("codue, cifnif, nombre, clave, baseimponible");
	qryMod349Tipo2.setFrom("co_operaciones349");
	qryMod349Tipo2.setWhere("idmodelo = " + cursor.valueBuffer("idmodelo"));
	if (!qryMod349Tipo2.exec()) {
		MessageBox.critical(util.translate("scripts", "Hubo un error al acceder a los datos de registros de operaciones.\nEl fichero no se ha podido generar correctamente"), MessageBox.Ok, MessageBox.NoButton);
		return;
	}
	var codUE:String;
	while (qryMod349Tipo2.next()) {
		file.write("2"); /// Tipo de registro 1 - 1 (1)
		file.write("349"); /// Modelo 2 - 4 (3)
		
		/// Ejercicio 5 - 8 (4)
		file.write(ejercicio); 
		
		/// NIF del declarante 9 - 17 (9)
		file.write(nifDeclarante); 
		
		/// Relleno 18 - 75 (58)
		file.write(flfactppal.iface.pub_espaciosDerecha("", 58));
	
		/// Código del país 76 - 77 (2)
		temp = qryMod349Tipo2.value("codue");
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Código del país"), 2))
			return false;
		codUE = temp;
		file.write(flfactppal.iface.pub_cerosIzquierda(temp, 2)); 
		
		/// NIF del operador 78 - 92 (15)
		temp = qryMod349Tipo2.value("cifnif");
		if (temp && temp != "")
			if (temp.startsWith(codUE))
				temp = temp.right(temp.length - 2);
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "NIF del operador"), 15))
			return false;
		file.write(flfactppal.iface.pub_espaciosDerecha(temp, 15)); 
	
		/// Nombre del operador 93 - 132 (40)
		temp = qryMod349Tipo2.value("nombre");
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Nombre del operador"), 40))
			return false;
		temp = flcontmode.iface.pub_controlCaracteres(temp);
		file.write(flfactppal.iface.pub_espaciosDerecha(temp, 40)); 
	
		/// Clave de operacion 133 - 133 (1)
		temp = qryMod349Tipo2.value("clave");
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Clave de operacion"), 1))
			return false;
		file.write(flfactppal.iface.pub_espaciosDerecha(temp, 1));
		
		/// Base imponible 134 - 146
		temp = qryMod349Tipo2.value("baseimponible");
		file.write(flcontmode.iface.pub_formatoNumeroAbs(parseFloat(temp), 11, 2)); 
	
		/// Relleno 147 - 250 (104)
		file.write(flfactppal.iface.pub_espaciosDerecha("", 104));

/** Parcheado porque la ayuda de informativas espera 250 para 2009, aunque la descripción 2009 indica 500 caracteres
		/// Relleno 147 - 500 (354)
		file.write(flfactppal.iface.pub_espaciosDerecha("", 354));
*/		
		/// Fin de registro
		temp = "\n";
		file.write(temp);
	}
	
	/// Registros tipo 3 (Rectificación)
	var qryMod349Tipo2:FLSqlQuery = new FLSqlQuery();
	qryMod349Tipo2.setTablesList("co_rectificaciones349");
	qryMod349Tipo2.setSelect("codue, cifnif, nombre, clave, codejercicio, periodo, birectificada, bianterior");
	qryMod349Tipo2.setFrom("co_rectificaciones349");
	qryMod349Tipo2.setWhere("idmodelo = " + cursor.valueBuffer("idmodelo"));
	if (!qryMod349Tipo2.exec()) {
		MessageBox.critical(util.translate("scripts", "Hubo un error al acceder a los datos de registros de operaciones.\nEl fichero no se ha podido generar correctamente"), MessageBox.Ok, MessageBox.NoButton);
		return;
	}
	while (qryMod349Tipo2.next()) {
		file.write("2"); /// Tipo de registro 1 -1 (1)
		file.write("349"); /// Modelo 2 - 4 (3)
		
		/// Ejercicio 5 - 8 (4)
		file.write(ejercicio); 
		
		/// NIF del declarante 9 - 17 (9)
		file.write(nifDeclarante); 
		
		/// Relleno  18 - 75 (58)
		file.write(flfactppal.iface.pub_espaciosDerecha("", 58));
	
		/// Código del país 76 - 77 (2)
		temp = qryMod349Tipo2.value("codue");
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Código del país"), 2))
			return false;
		codUE = temp;
		file.write(flfactppal.iface.pub_cerosIzquierda(temp, 2)); 
		
		/// NIF del operador 78 - 92 (15)
		temp = qryMod349Tipo2.value("cifnif");
		if (temp && temp != "")
			if (temp.startsWith(codUE))
				temp = temp.right(temp.length - 2);
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "NIF del operador"), 15))
			return false;
		file.write(flfactppal.iface.pub_espaciosDerecha(temp, 15)); 
	
		/// Nombre del operador 93 - 132 (40)
		temp = qryMod349Tipo2.value("nombre");
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Nombre del operador"), 40))
			return false;
		temp = flcontmode.iface.pub_controlCaracteres(temp);
		file.write(flfactppal.iface.pub_espaciosDerecha(temp, 40)); 
	
		/// Clave de operacion 133 - 133 (1)
		temp = qryMod349Tipo2.value("clave");
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Clave de operacion"), 1))
			return false;
		file.write(flfactppal.iface.pub_espaciosDerecha(temp, 1));
		
		/// Relleno 134 - 146 (13)
		file.write(flfactppal.iface.pub_espaciosDerecha("", 13));
		
		/// Ejercicio rectificado 147 - 150 (4)
		temp = qryMod349Tipo2.value("codejercicio");
		temp = temp.toString().left(4); 
		file.write(temp); 
	
		/// Período rectificado 151 - 152 (2)
		temp = qryMod349Tipo2.value("periodo");
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Período rectificado"), 2))
			return false;
		file.write(flfactppal.iface.pub_espaciosDerecha(temp, 2));
		
		/// Base imponible rectificada 153 - 165 (13)
		temp = qryMod349Tipo2.value("birectificada");
		file.write(flcontmode.iface.pub_formatoNumeroAbs(parseFloat(temp), 11, 2)); 
	
		/// Base imponible declarada anteriormente 166 - 178 (13)
		temp = qryMod349Tipo2.value("bianterior");
		file.write(flcontmode.iface.pub_formatoNumeroAbs(parseFloat(temp), 11, 2)); 
	
		/// Relleno 179 - 250 (72)
		file.write(flfactppal.iface.pub_espaciosDerecha("", 72));

/** Parcheado porque la ayuda de informativas espera 250 para 2009, aunque la descripción 2009 indica 500 caracteres
		/// Relleno 179 - 500 (322)
		file.write(flfactppal.iface.pub_espaciosDerecha("", 322));
*/		
		/// Fin de registro
		temp = "\n";
		file.write(temp);
	}
	
	file.close();

	MessageBox.information(util.translate("scripts", "Generado fichero en :\n\n" + nombreFichero + "\n\n"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
}

/** \D Genera un fichero para realizar la presentación telemática del modelo
\end */
function oficial_presTelematica2010()
{
	var util:FLUtil = new FLUtil();
	var cursor:FLSqlCursor = this.cursor();
	if (!cursor.isValid()) {
		return;
	}

	// Ejercicio
	var ejercicio:String;
	var temp:String = util.sqlSelect("ejercicios", "fechainicio", "codejercicio = '" + cursor.valueBuffer("codejercicio") + "'");
	ejercicio = temp.toString().left(4);
	
	// Tipo de soporte
	var tipoSoporte:String;
	var presTelematica:String = util.translate("scripts", "Transmisión telemática");
	var disquete:String = util.translate("scripts", "Disquete");
	var cintaMagnetica:String = util.translate("scripts", "Cinta magnética");
	var soportes:Array = [presTelematica, disquete, cintaMagnetica];
	var opcion:String = Input.getItem(util.translate("scripts", "Indique el tipo de soporte"), soportes, presTelematica, false);
	if (!opcion)
		return;
	switch (opcion) {
		case presTelematica:
			tipoSoporte = "T";
			break;
		case disquete:
			tipoSoporte = "D";
			break;
		case cintaMagnetica:
			tipoSoporte = "C";
			break;
	}
	
	var nombreFichero:String = FileDialog.getSaveFileName("*.*");
	if (!nombreFichero)
		return;
		
	var file:Object = new File(nombreFichero);
	file.open(File.WriteOnly);

	file.write("1"); /// Tipo de registro (Declarante) 1 - 1 (1)
	file.write("349"); /// Modelo 2 - 4 (3)
		
	/// Ejercicio 5 - 8 (4)
	file.write(ejercicio); 
	
	/// CIF 9 - 17 (9)
	var nifDeclarante:String;
	temp = flcontmode.iface.pub_valorDefectoDatosFiscales("cifnif");
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "CIF"), 9))
		return false;
	nifDeclarante = flfactppal.iface.pub_espaciosDerecha(temp, 9);
	file.write(nifDeclarante); 
	
	/// Apellidos y nombre o razón social 18 - 57 (40)
	temp = flcontmode.iface.pub_valorDefectoDatosFiscales("apellidosrs");// + " " + flcontmode.iface.pub_valorDefectoDatosFiscales("nombre");
debug(temp);
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Apellidos o razón social"), 40))
		return false;
	temp = flcontmode.iface.pub_formatoAlfanumerico349(temp);
	file.write(flfactppal.iface.pub_espaciosDerecha(temp, 40)); 
	
	/// Tipo de soporte 58 - 58 (1)
	file.write(tipoSoporte); 
	
	/// Persona con quien relacionarse (teléfono) 59 - 67 (9)
	temp = cursor.valueBuffer("telefonorel");
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Persona con quien relacionarse (teléfono)"), 9))
		return false;
	temp = flcontmode.iface.pub_formatoAlfanumerico349(temp);
	file.write(flfactppal.iface.pub_espaciosDerecha(temp, 9));
	
	/// Persona con quien relacionarse (apellidos y nombre) 59 - 107 (39)
	temp = cursor.valueBuffer("personarel");
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Persona con quien relacionarse (apellidos y nombre)"), 40))
		return false;
	temp = flcontmode.iface.pub_formatoAlfanumerico349(temp);
	file.write(flfactppal.iface.pub_espaciosDerecha(temp, 40)); 
	
	/// Número de justificante 108 - 120 (13)
	temp = cursor.valueBuffer("numjustificante");
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Número de justificante"), 13))
		return false;
	file.write(flfactppal.iface.pub_cerosIzquierda(temp, 13)); 
	
	/// Declaración complementaria 121 - 121 (1)
	if (cursor.valueBuffer("complementaria"))
		temp = "C";
	else
		temp = " ";
	file.write(temp); 
	
	/// Declaración sustitutiva 122 - 122 (1)
	if (cursor.valueBuffer("sustitutiva"))
		temp = "S";
	else
		temp = " ";
	file.write(temp); 
	
	/// Número de justificante de la declaración anterior 123 - 135 (13)
	temp = cursor.valueBuffer("numdecanterior");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "Número de justificante de la declaración anterior"), 13))
		return false;
	file.write(flfactppal.iface.pub_cerosIzquierda(temp, 13)); 
	
	/// Período 136 - 137 (2)
	var nombreDato:String;
	switch (cursor.valueBuffer("tipoperiodo")) {
		case "Mes": {
			nombreDato = util.translate("scripts", "Mes");
			temp = cursor.valueBuffer("mes");
			break;
		}
		case "Trimestre": {
			nombreDato = util.translate("scripts", "Trimestre");
			temp = cursor.valueBuffer("periodo");
			break;
		}
		case "Año": {
			nombreDato = util.translate("scripts", "Año");
			temp = "0A";
			break;
		}
	}
	if (!flcontmode.iface.pub_verificarDato(temp, true, nombreDato, 2)) {
		return false;
	}
	file.write(temp);
	
	/// Número total de operadores intracomunitarios 138 - 146 (9)
	temp = parseFloat(cursor.valueBuffer("numtotaloi"));
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Número total de operadores intracomunitarios"), 9))
		return false;
	file.write(flfactppal.iface.pub_cerosIzquierda(temp, 9)); 
	
	/// Importe de las operaciones intracomunitarias 147 - 161 (15)
	temp = cursor.valueBuffer("importetotaloi");
	file.write(flcontmode.iface.pub_formatoNumeroAbs(parseFloat(temp), 13, 2)); 
	
	/// Número total de operadores intracomunitarios con rectificaciones 162 - 170 (9)
	temp = parseFloat(cursor.valueBuffer("numtotaloirec"));
	if (temp || temp == "")
		temp = "0";
	if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Número total de operadores intracomunitarios con rectificaciones"), 9))
		return false;
	file.write(flfactppal.iface.pub_cerosIzquierda(temp, 9)); 
	
	/// Importe de las rectificaciones 171 - 185 (15)
	temp = cursor.valueBuffer("importetotaloirec");
	file.write(flcontmode.iface.pub_formatoNumeroAbs(parseFloat(temp), 13, 2)); 
	
	/// Indicador de cambio en la periodicidad 186 - 186 (1)
	temp = (cursor.valueBuffer("cambioperiodicidad") ? "X" : " ");
	file.write(temp); 
	
	/// Relleno hasta 187 - 250 (64)
// 	file.write(flfactppal.iface.pub_espaciosDerecha("", 64));
	
	/// Relleno hasta 187 - 390 (204)
	file.write(flfactppal.iface.pub_espaciosDerecha("", 204));
	
	/// Nif representante legal 391 - 399 (9)
	temp = cursor.valueBuffer("cifnifreplegal");
	if (!flcontmode.iface.pub_verificarDato(temp, false, util.translate("scripts", "CIF Rep.Legal"), 9)) {
		return false;
	}
	var nifRepLegal:String = flfactppal.iface.pub_espaciosDerecha(temp, 9);
	file.write(nifRepLegal);

	/// Relleno a blancos 400 - 487 (88)
	file.write(flfactppal.iface.pub_espaciosDerecha("", 88));
	
	/// Sello electrónico 488 - 500 (13)
	file.write(flfactppal.iface.pub_espaciosDerecha("", 13));

	// Fin de registro
	temp = "\n";
	file.write(temp);
	
	//Registros tipo 2 (Operación)
	var qryMod349Tipo2:FLSqlQuery = new FLSqlQuery();
	qryMod349Tipo2.setTablesList("co_operaciones349");
	qryMod349Tipo2.setSelect("codue, cifnif, nombre, clave, baseimponible");
	qryMod349Tipo2.setFrom("co_operaciones349");
	qryMod349Tipo2.setWhere("idmodelo = " + cursor.valueBuffer("idmodelo"));
	if (!qryMod349Tipo2.exec()) {
		MessageBox.critical(util.translate("scripts", "Hubo un error al acceder a los datos de registros de operaciones.\nEl fichero no se ha podido generar correctamente"), MessageBox.Ok, MessageBox.NoButton);
		return;
	}
	var codUE:String;
	while (qryMod349Tipo2.next()) {
		file.write("2"); /// Tipo de registro 1 - 1 (1)
		file.write("349"); /// Modelo 2 - 4 (3)
		
		/// Ejercicio 5 - 8 (4)
		file.write(ejercicio); 
		
		/// NIF del declarante 9 - 17 (9)
		file.write(nifDeclarante); 
		
		/// Relleno 18 - 75 (58)
		file.write(flfactppal.iface.pub_espaciosDerecha("", 58));
	
		/// Código del país 76 - 77 (2)
		temp = qryMod349Tipo2.value("codue");
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Código del país"), 2))
			return false;
		codUE = temp;
		file.write(flfactppal.iface.pub_cerosIzquierda(temp, 2)); 
		
		/// NIF del operador 78 - 92 (15)
		temp = qryMod349Tipo2.value("cifnif");
		if (temp && temp != "")
			if (temp.startsWith(codUE))
				temp = temp.right(temp.length - 2);
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "NIF del operador"), 15))
			return false;
		file.write(flfactppal.iface.pub_espaciosDerecha(temp, 15)); 
	
		/// Nombre del operador 93 - 132 (40)
		temp = qryMod349Tipo2.value("nombre");
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Nombre del operador"), 40))
			return false;
		temp = flcontmode.iface.pub_formatoAlfanumerico349(temp);
		file.write(flfactppal.iface.pub_espaciosDerecha(temp, 40)); 
	
		/// Clave de operacion 133 - 133 (1)
		temp = qryMod349Tipo2.value("clave");
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Clave de operacion"), 1))
			return false;
		file.write(flfactppal.iface.pub_espaciosDerecha(temp, 1));
		
		/// Base imponible 134 - 146
		temp = qryMod349Tipo2.value("baseimponible");
		file.write(flcontmode.iface.pub_formatoNumeroAbs(parseFloat(temp), 11, 2)); 
	
		/// Relleno 147 - 250 (104)
// 		file.write(flfactppal.iface.pub_espaciosDerecha("", 104));

		/// Relleno 147 - 500 (354)
		file.write(flfactppal.iface.pub_espaciosDerecha("", 354));

		/// Fin de registro
		temp = "\n";
		file.write(temp);
	}
	
	/// Registros tipo 3 (Rectificación)
	var qryMod349Tipo2:FLSqlQuery = new FLSqlQuery();
	qryMod349Tipo2.setTablesList("co_rectificaciones349");
	qryMod349Tipo2.setSelect("codue, cifnif, nombre, clave, codejercicio, periodo, birectificada, bianterior");
	qryMod349Tipo2.setFrom("co_rectificaciones349");
	qryMod349Tipo2.setWhere("idmodelo = " + cursor.valueBuffer("idmodelo"));
	if (!qryMod349Tipo2.exec()) {
		MessageBox.critical(util.translate("scripts", "Hubo un error al acceder a los datos de registros de operaciones.\nEl fichero no se ha podido generar correctamente"), MessageBox.Ok, MessageBox.NoButton);
		return;
	}
	while (qryMod349Tipo2.next()) {
		file.write("2"); /// Tipo de registro 1 -1 (1)
		file.write("349"); /// Modelo 2 - 4 (3)
		
		/// Ejercicio 5 - 8 (4)
		file.write(ejercicio); 
		
		/// NIF del declarante 9 - 17 (9)
		file.write(nifDeclarante); 
		
		/// Relleno  18 - 75 (58)
		file.write(flfactppal.iface.pub_espaciosDerecha("", 58));
	
		/// Código del país 76 - 77 (2)
		temp = qryMod349Tipo2.value("codue");
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Código del país"), 2))
			return false;
		codUE = temp;
		file.write(flfactppal.iface.pub_cerosIzquierda(temp, 2)); 
		
		/// NIF del operador 78 - 92 (15)
		temp = qryMod349Tipo2.value("cifnif");
		if (temp && temp != "")
			if (temp.startsWith(codUE))
				temp = temp.right(temp.length - 2);
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "NIF del operador"), 15))
			return false;
		file.write(flfactppal.iface.pub_espaciosDerecha(temp, 15)); 
	
		/// Nombre del operador 93 - 132 (40)
		temp = qryMod349Tipo2.value("nombre");
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Nombre del operador"), 40))
			return false;
		temp = flcontmode.iface.pub_formatoAlfanumerico349(temp);
		file.write(flfactppal.iface.pub_espaciosDerecha(temp, 40)); 
	
		/// Clave de operacion 133 - 133 (1)
		temp = qryMod349Tipo2.value("clave");
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Clave de operacion"), 1))
			return false;
		file.write(flfactppal.iface.pub_espaciosDerecha(temp, 1));
		
		/// Relleno 134 - 146 (13)
		file.write(flfactppal.iface.pub_espaciosDerecha("", 13));
		
		/// Ejercicio rectificado 147 - 150 (4)
		var ejercicio:String;
		var temp:String = util.sqlSelect("ejercicios", "fechainicio", "codejercicio = '" + qryMod349Tipo2.value("codejercicio") + "'");
		temp = temp.toString().left(4);
		file.write(temp);
	
		/// Período rectificado 151 - 152 (2)
		temp = qryMod349Tipo2.value("periodo");
		if (!flcontmode.iface.pub_verificarDato(temp, true, util.translate("scripts", "Período rectificado"), 2))
			return false;
		file.write(flfactppal.iface.pub_espaciosDerecha(temp, 2));
		
		/// Base imponible rectificada 153 - 165 (13)
		temp = qryMod349Tipo2.value("birectificada");
		file.write(flcontmode.iface.pub_formatoNumeroAbs(parseFloat(temp), 11, 2)); 
	
		/// Base imponible declarada anteriormente 166 - 178 (13)
		temp = qryMod349Tipo2.value("bianterior");
		file.write(flcontmode.iface.pub_formatoNumeroAbs(parseFloat(temp), 11, 2)); 
	
		/// Relleno 179 - 250 (72)
// 		file.write(flfactppal.iface.pub_espaciosDerecha("", 72));

		/// Relleno 179 - 500 (322)
		file.write(flfactppal.iface.pub_espaciosDerecha("", 322));

		/// Fin de registro
		temp = "\n";
		file.write(temp);
	}
	
	file.close();

	MessageBox.information(util.translate("scripts", "Generado fichero en :\n\n" + nombreFichero + "\n\n"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
}
//// OFICIAL /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition boe2011 */
//////////////////////////////////////////////////////////////////
//// BOE2011 /////////////////////////////////////////////////////
/** \D Genera un fichero para realizar la presentación telemática del modelo
\end */

function boe2011_presTelematica()
{
    this.iface.presTelematica2011();
}

/*Los diseños lógicos de registro para presentación telemática del modelo 349 no han cambiado desde 2010, pero se realiza una llamada a una nueva función para adaptar la generación del registro a nuevas funciones fácilmente modificables*/
function boe2011_presTelematica2011() {
    
    var curMod:FLSqlCursor = this.cursor();
    if (!curMod.isValid()){
        return;
    }
    
    var nombreFichero = this.iface.nombreFichero();
    if (!nombreFichero){
        return;
    }

    /*var soporteModelo = this.iface.soporteModelo();
    if (!soporteModelo) {
        return;
    }*/
    
    var util:FLUtil = new FLUtil();
    util.createProgressDialog(util.translate("scripts", "Generando registro de tipo 1"), 10);
    util.setProgress(2);

    flcontmode.iface.error = "";
    
    var file:Object = new File(nombreFichero);
    file.open(File.WriteOnly);
    
    file.write(this.iface.tiporeg1(curMod) + "\r\n");
    
    util.setProgress(10);
    util.destroyProgressDialog();
    
    var curMod2:FLSqlCursor = new FLSqlCursor("co_operaciones349");
    curMod2.select("idmodelo = " + curMod.valueBuffer("idmodelo"));
    util.createProgressDialog(util.translate("scripts", "Generando registro de tipo 2 Operaciones Intracomunitarias"), curMod2.size());
    var progreso:Number = 0;
    while (curMod2.next()){
        util.setProgress(progreso++);
        file.write(this.iface.tiporeg2(curMod,curMod2) + "\r\n");
    }
    util.destroyProgressDialog();
    
    var curMod2r:FLSqlCursor = new FLSqlCursor("co_rectificaciones349");
    curMod2r.select("idmodelo = " + curMod.valueBuffer("idmodelo"));
    util.createProgressDialog(util.translate("scripts", "Generando registro de tipo 2 facturas recibidas"), curMod2r.size());
    var progreso:Number = 0;
    while (curMod2r.next()){
        file.write(this.iface.tiporeg2r(curMod,curMod2r) + "\r\n");
    }
    util.destroyProgressDialog();

    file.close();
     
    util.destroyProgressDialog();
    
    var util:FLUtil = new FLUtil();
    if (flcontmode.iface.error == "") {
       MessageBox.information(util.translate("scripts", "Generado fichero en :\n\n" + nombreFichero + "\n\n"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
    } else {
        MessageBox.information(util.translate("scripts", "Se han detectado los siguientes errores :\n\n" +flcontmode.iface.error+ "\n\n"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
    }
}

function boe2011_nombreFichero():String
{
    var nombreFichero:String = FileDialog.getSaveFileName("*.*");
    if (!nombreFichero) {
        MessageBox.warning("No ha indicado el nombre del fichero",MessageBox.Ok, MessageBox.NoButton);
        return "";
    } else {
        return nombreFichero;
    }

}

function boe2011_soporteModelo():String{
    
    var util:FLUtil = new FLUtil();
    
    // Tipo de soporte
    var tipoSoporte:String;
    var presTelematica:String = util.translate("scripts", "Transmisión telemática");
    var soporteMagnetico:String = util.translate("scripts", "Soporte Magnético");
    var soportes:Array = [presTelematica, soporteMagnetico];
    var opcion:String = Input.getItem(util.translate("scripts", "Indique el tipo de soporte"), soportes, presTelematica, false);
    if (!opcion){
        MessageBox.warning("No ha indicado el tipo de soporte.\nSe asignara presentación telemática como valor por defecto",MessageBox.Ok,MessageBox.NoButton);
        return "T";
    }
        
    switch (opcion) {
        case presTelematica:
            tipoSoporte = "T";
            break;
    
    case soporteMagnetico:
            tipoSoporte = "C";
            break;
    }
    
    return tipoSoporte;
}
    
function boe2011_tiporeg1(curMod:FLSlqCursor):String {

    //Registro de tipo 1 declarante
    var codReg = "1";
    var desReg:Array = flcontmode.iface.pub_desRegistro349(codReg);
    
    var util:FLUtil = new FLUtil();
    var valorCampo;
    var nombreCampo = "";
    var formatoCampo = "";
    var registro:Object = {};
    
    for (var i = 0; i < desReg.length; i++) {
        nombreCampo = desReg[i][0];
        longitudCampo = desReg[i][2];
        formatoCampo = desReg[i][3];
        if (formatoCampo == "B") {
            valorCampo = " ";
        } else {
            switch(nombreCampo) {
                case "tiporeg":
                    valorCampo = "1";
                    break;
                
                case "modelo":
                    valorCampo = "349";
                    break;
                    
                case "ejercicio":
                    var fecha:Date = curMod.valueBuffer("fechainicio");
                    valorCampo = fecha.getYear().toString();
                    break;
                    
                case "tiposoporte":
                    valorCampo = this.iface.soporteModelo();
                    break;
                
                case "complementaria":
                    if (curMod.valueBuffer("complementaria")) {
                        valorCampo = "C";
                    } else {
                        valorCampo = " ";
                    }
                    break;
                    
                case "sustitutiva":
                    if (curMod.valueBuffer("sustitutiva")) {
                        valorCampo = "S";
                    } else{
                        valorCampo = " ";
                    }
                    break;
                    
                case "jusanterior":
                    if (curMod.valueBuffer("complementaria") || curMod.valueBuffer("sustitutiva")) {
                        valorCampo = curMod.valueBuffer("numanterior");
                    } else {
                        valorCampo = "0";
                    }
                    break;
                
                case "periodo":
                    if (curMod.valueBuffer("tipoperiodo") == "Trimestre") {
                        valorCampo = curMod.valueBuffer("periodo");
                    } else if (curMod.valueBuffer("tipoperiodo") == "Mes") {
                        valorCampo = curMod.valueBuffer("mes");
                    } else {
                        valorCampo = "0A";
                    }
                    break;
                
                case "cambioperiodicidad":
                    if (curMod.valueBuffer("cambioperiodicidad")){
                        valorCampo = "X";
                    } else {
                       valorCampo = " "; 
                    }
                    break;
                    
                case "importetotaloi":
                case "importetotaloirec":
                    valorCampo = flcontmode.iface.pub_formatoNumero(Math.abs(parseFloat(curMod.valueBuffer(nombreCampo))), (parseFloat(longitudCampo)-2), 2); 
                    break;

                default :
                    // cifnifpres
                    // nombrepres
                    // tiposoporte
                    // telefonorel
                    // personarel
                    // numjustificante
                    // numtotaloi
                    // numtotaloirec
                    // cifnifreplegal
                    valorCampo = curMod.valueBuffer(nombreCampo);
                    break;
            }
        }
        debug("registro["+nombreCampo+"] = "+valorCampo);
        registro[nombreCampo] = valorCampo;
    }
    
    return flcontmode.iface.pub_generarRegistro(desReg,registro);

}

/*Registro de declarados operadores intracomunitarios*/
function boe2011_tiporeg2(curMod:FLSlqCursor,curMod2:FlsqlCursor):String {

    var codReg = "2";
    var desReg:Array = flcontmode.iface.pub_desRegistro349(codReg);
    
    var util:FLUtil = new FLUtil();
    var valorCampo;
    var nombreCampo = "";
    var formatoCampo = "";
    var registro:Object = {};
    
    for (var i = 0; i < desReg.length; i++) {
        nombreCampo = desReg[i][0];
        longitudCampo = desReg[i][2];
        formatoCampo = desReg[i][3];
        if (formatoCampo == "B") {
            valorCampo = " ";
        } else {
            switch(nombreCampo) {
                case "tiporeg":
                    valorCampo = "2";
                    break;
                
                case "modelo":
                    valorCampo = "349";
                    break;
                    
                case "ejercicio":
                    var fecha:Date = curMod.valueBuffer("fechainicio");
                    valorCampo = fecha.getYear().toString();
                    break;
                    
                case "cifnifpres":
                    valorCampo = curMod.valueBuffer("cifnifpres");
                    break;

                case "baseimponible":
                    valorCampo = flcontmode.iface.pub_formatoNumero(Math.abs(parseFloat(curMod2.valueBuffer(nombreCampo))), (parseFloat(longitudCampo)-2), 2); 
                    break;
                
                default :
                    // codue
                    // cifnif
                    // nombre
                    // clave
                    valorCampo = curMod2.valueBuffer(nombreCampo);
                    break;
            }
        }

        registro[nombreCampo] = valorCampo;
    }
    
    return flcontmode.iface.pub_generarRegistro(desReg,registro);

}

/*Registro de rectificaciones*/
function boe2011_tiporeg2r(curMod:FLSlqCursor,curMod2r:FlsqlCursor):String {

    var codReg = "2r";
    var desReg:Array = flcontmode.iface.pub_desRegistro349(codReg);
    
    var util:FLUtil = new FLUtil();
    var valorCampo;
    var nombreCampo = "";
    var formatoCampo = "";
    var registro:Object = {};
    
    for (var i = 0; i < desReg.length; i++) {
        nombreCampo = desReg[i][0];
        longitudCampo = desReg[i][2];
        formatoCampo = desReg[i][3];
        if (formatoCampo == "B") {
            valorCampo = " ";
        } else {
            switch(nombreCampo) {
                case "tiporeg":
                    valorCampo = "2";
                    break;
                
                case "modelo":
                    valorCampo = "349";
                    break;
                    
                case "ejercicio":
                    var fecha:Date = curMod.valueBuffer("fechainicio");
                    valorCampo = fecha.getYear().toString();
                    break;
                    
                case "cifnifpres":
                    valorCampo = curMod.valueBuffer("cifnifpres");
                    break;

                case "baseimponible":
                case "bianterior":
                    valorCampo = flcontmode.iface.pub_formatoNumero(Math.abs(parseFloat(curMod2r.valueBuffer(nombreCampo))), (parseFloat(longitudCampo)-2), 2); 
                    break;
                    
                case "codejercicio":
                    var fecha:Date = util.sqlSelect("ejercicios","fechainicio","codejercicio='"+curMod2r.valueBuffer("codejercicio")+"'");
                    valorCampo = fecha.getYear().toString();
                    break;
                
                default :
                    // codue
                    // cifnif
                    // nombre
                    // clave
                    // periodo
                    valorCampo = curMod2r.valueBuffer(nombreCampo);
                    break;
            }
        }
        
        registro[nombreCampo] = valorCampo;
    }
    
    return flcontmode.iface.pub_generarRegistro(desReg,registro);

}

//// BOE2011 /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////

//// DESARROLLO /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////
//// INTERFACE  /////////////////////////////////////////////////

//// INTERFACE  /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
