/***************************************************************************
                 co_modelo031.qs  -  description
                             -------------------
    begin                : mier sept 5 2012
    copyright            : (C) 2009 by InfoSiAL S.L.
    email                : info@gestiweb.com
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
	function validateForm():Boolean {
		return this.ctx.interna_validateForm();
	}
}
//// INTERNA /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
class oficial extends interna 
{
    function oficial( context ) { interna( context ); } 
    function bufferChanged(fN) {
            return this.ctx.oficial_bufferChanged(fN);
    }
    function comprobarFecha(){
        return this.ctx.oficial_comprobarFecha();
    }
    function informarConDatosFiscales() {
            return this.ctx.oficial_informarConDatosFiscales();
    }
    function calculateField(fN):String{
            return this.ctx.oficial_calculateField(fN);
    }
    function commonCalculateField(fN, cursor:FLSqlCursor):String{
            return this.ctx.oficial_commonCalculateField(fN, cursor);
    }
    function buscarFacturaImport() {
            this.ctx.oficial_buscarFacturaImport();
    }
    function borrarFactura(){
        return this.ctx.oficial_borrarFactura();
    }
    function cambiarEstado() {
        return this.ctx.oficial_cambiarEstado();
    }
    function calcularEstadoModelo031(idModelo:Number):String{
        return this.ctx.oficial_calcularEstadoModelo031(idModelo);
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
/** \C El ejercicio por defecto al crear un nuevo modelo es el ejercicio marcado como actual en el formulario de empresa
\end */
function interna_init() 
{
    var util:FLUtil = new FLUtil;
    var cursor:FLSqlCursor = this.cursor();
    
    connect(cursor, "bufferChanged(QString)", this, "iface.bufferChanged");
    connect(this.child("tbnBuscarFacturaImport"), "clicked()", this, "iface.buscarFacturaImport");
    connect(this.child("pbnDelFactura"), "clicked()", this, "iface.borrarFactura");
    connect(form.child("tdbPagoMod031").cursor(), "cursorUpdated()", this, "iface.cambiarEstado");
    
    if (cursor.modeAccess() == cursor.Insert) {
        var hoy:Date = new Date();
        this.child("fdbFecha").setValue(hoy);
        this.iface.informarConDatosFiscales();
    }
    
    this.child("tdbPartidas").setReadOnly(true);
    this.iface.cambiarEstado();
}

function interna_validateForm():Boolean
{
    if (!this.iface.comprobarFecha()) {
            return false;
    }
}

//// INTERNA /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
function oficial_bufferChanged( fN ) 
{
    var cursor:FLSqlCursor = this.cursor();
    var util:FLUtil = new FLUtil();
    switch ( fN ) {
    }
}


/** \D Comprueba que fecha pertenece al ejercicio seleccionado

@return	True si la comprobación es buena, false en caso contrario
\end */
function oficial_comprobarFecha():Boolean
{
    var util:FLUtil = new FLUtil();
	
    var codEjercicio:String = this.child("fdbCodEjercicio").value();
    var fecha:String = this.child("fdbFecha").value();
    
    var codEjerFecha = util.sqlSelect("ejercicios","codejercicio","'"+fecha+"'::Date between fechainicio and fechafin");
    
    if (codEjerFecha != codEjercicio) {
	MessageBox.critical(util.translate("scripts", "Las fecha seleccionada no corresponde al ejercicio"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
	return false;
    }
    
    if (!this.cursor().valueBuffer("fechav")) {
        MessageBox.critical(util.translate("scripts", "No ha indicado la fecha de vencimiento"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
        return false;
    }
	
    return true;
}

function oficial_informarConDatosFiscales()
{
    var util:FLUtil = new FLUtil();
    
    this.child("fdbCodEjercicio").setValue(this.iface.calculateField("codejercicio"));
    this.child("fdbCifNif").setValue(this.iface.calculateField("cifnif"));
    this.child("fdbApellidosRS").setValue(this.iface.calculateField("apellidosnombrers"));
    this.child("fdbCodTipoVia").setValue(this.iface.calculateField("codtipovia"));
    this.child("fdbNombreVia").setValue(this.iface.calculateField("nombrevia"));
    this.child("fdbNumero").setValue(this.iface.calculateField("numero"));
    this.child("fdbEscalera").setValue(this.iface.calculateField("escalera"));
    this.child("fdbPiso").setValue(this.iface.calculateField("piso"));
    this.child("fdbPuerta").setValue(this.iface.calculateField("puerta"));
    this.child("fdbMunicipio").setValue(this.iface.calculateField("municipio"));
    this.child("fdbCodPos").setValue(this.iface.calculateField("codpos"));
    this.child("fdbCodProvincia").setValue(this.iface.calculateField("codprovincia"));
    this.child("fdbConcepto").setValue(this.iface.calculateField("concepto"));
    
}

function oficial_calculateField(fN:String):String 
{
    var util:FLUtil = new FLUtil;
    var cursor:FLSqlCursor = this.cursor();
    
    return this.iface.commonCalculateField(fN, cursor);
}
        
function oficial_commonCalculateField(fN:String ,cursor:FLSqlCursor):String 
{
    var util:FLUtil = new FLUtil;
    var valor:String;
    switch ( fN ) {
        case "codejercicio":
            if (cursor.valueBuffer("fecha")) {
                var fecha = cursor.valueBuffer("fecha").toString().substring(0,10);
                valor = util.sqlSelect("ejercicios","codejercicio","'"+fecha+"'::Date between fechainicio and fechafin");
            } else {
                valor = flfactppal.iface.pub_ejercicioActual();
            }
            break;
            
        case "cifnif":
        case "codtipovia":
        case "nombrevia":
        case "numero":
        case "escalera":
        case "piso":
        case "puerta":
        case "municipio":
        case "codpos":
        case "codprovincia":
        case "provincia":
            valor = flcontmode.iface.pub_valorDefectoDatosFiscales(fN);
            break;
            
        case "apellidosnombrers":
            if (flcontmode.iface.pub_valorDefectoDatosFiscales("personafisica")) {
                var ap1 = flcontmode.iface.pub_valorDefectoDatosFiscales("apellidospf");
                var ap2 = flcontmode.iface.pub_valorDefectoDatosFiscales("apellidospf2");
                var nombre = flcontmode.iface.pub_valorDefectoDatosFiscales("nombrepf");
                valor = ap1;
                if (ap2) valor += " "+ap2;
                valor += " "+nombre;
            } else {
                valor = flcontmode.iface.pub_valorDefectoDatosFiscales("apellidosrs");
            }
            break;
            
        case "concepto":
            valor = "DERECHOS DE IMPORTACIÓN E IMPUESTOS INDIRECTOS";
            break;
            
        case "tipobienes":
            valor = "Corrientes";
            if (cursor.valueBuffer("idfacturaimport")){
                var idAsiento = util.sqlSelect("facturasprov","idasiento","idfactura="+cursor.valueBuffer("idfacturaimport"));
                if (idAsiento) {
                    var tipoBienes = formRecordco_modelo303.iface.dameTipoBienes(idAsiento);
                    switch(tipoBienes){
                        case "corrientes":
                            valor = "Corrientes";
                            break;
                            
                        case "inversion":
                            valor = "De Inversión";
                            break;
                        
                        case "indefinido":
                            MessageBox.warning(util.translate("scripts", "No se ha podido determinar si la factura %1 corresponde a la compra de bienes corrientes o de inversión.\nLa factura no será incluida de forma automática en el modelo 303").arg(cursor.valueBuffer("codfacturaimport")), MessageBox.Ok, MessageBox.NoButton);
                            valor = "Indefinido";
                            break;
        
                    }
                }
            }
            break;
        
        case "estado":
            valor = this.iface.calcularEstadoModelo031(cursor.valueBuffer("idmodelo"));
            break;
    }
    
    return valor;
        
}

function oficial_buscarFacturaImport()
{
    var cursor:FLSqlCursor = this.cursor();
    var util:FLUtil = new FLUtil();
    var f:Object = new FLFormSearchDB("busfactprov");
    var curFacturas:FLSqlCursor = f.cursor();
    f.setMainWidget();
    var idFactura:String = f.exec("idfactura");
    if (!idFactura) {
            return false;
    } else {
            cursor.setValueBuffer("idfacturaimport", idFactura);
            this.child("fdbCodFactura").setValue(util.sqlSelect("facturasprov","codigo","idfactura="+idFactura));
    }
    
    cursor.setValueBuffer("tipobienes",this.iface.calculateField("tipobienes"));
}

function oficial_borrarFactura(){
        
    this.child("fdbCodFactura").setValue("");
    this.cursor().setNull("idfacturaimport");
    this.cursor().setNull("codfacturaimport");
}

function oficial_cambiarEstado() {

    var util:FLUtil = new FLUtil();
    var habilitar:Boolean = true;
    
    this.cursor().setValueBuffer("estado",this.iface.calculateField("estado"));
    
    if (this.cursor().valueBuffer("estado") != "Emitido") {
        habilitar = false;
    }
    
    this.child("gbxCodejerPeriodo").setEnabled(habilitar);
    this.child("gbxTitular").setEnabled(habilitar);
    this.child("gbxRepres").setEnabled(habilitar);
    this.child("gbxConcepto").setEnabled(habilitar);
    this.child("fbxFacturaImport").setEnabled(habilitar);
    this.child("gbxTipoBienes").setEnabled(habilitar);
    this.child("gbxImportes").setEnabled(habilitar);
    this.child("gbxConta").setEnabled(habilitar);
    this.child("fdbNoGenerarAsiento").setDisabled(!habilitar);
    this.child("groupBoxPago").setEnabled(!habilitar);
   
}

function oficial_calcularEstadoModelo031(idModelo:Number):String{
    
    var util:FLUtil = new FLUtil();
    var estado = "Emitido";
    
    var cerrado:Boolean = util.sqlSelect("co_modelo031","cerrado","idmodelo="+idModelo);
    if (cerrado) {
        estado = "Cerrado";
        var idPago = util.sqlSelect("co_pagomodelo031","idpago","idmodelo="+idModelo);
            if (idPago) {
                estado = "Pagado";
            }
    }
    
    return estado;
    
}
//// OFICIAL /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////

//// DESARROLLO /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
