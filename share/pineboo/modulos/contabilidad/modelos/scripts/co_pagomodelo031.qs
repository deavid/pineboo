/***************************************************************************
                 co_pagomodelo031.qs  -  description
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
    function comprobarSiGenerarAsiento(){
        return this.ctx.oficial_comprobarSiGenerarAsiento();
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
    
    if (cursor.modeAccess() == cursor.Insert) {
        var hoy:Date = new Date();
        this.child("fdbFecha").setValue(hoy);
    }
    this.child("tdbPartidas").setReadOnly(true);

}

function interna_validateForm():Boolean
{
    if (!this.iface.comprobarSiGenerarAsiento()) {
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

function oficial_comprobarSiGenerarAsiento():Boolean
{
    var util:FLUtil = new FLUtil();
    
    var cursor = this.cursor();
    var noAsientoModelo = util.sqlSelect("co_modelo031","nogenerarasiento","idmodelo="+cursor.valueBuffer("idmodelo"));
    
    if (flfactppal.iface.pub_valorDefectoEmpresa("contintegrada") && noAsientoModelo && !this.child("fdbNoGenerarAsiento").value()) {
        MessageBox.warning(util.translate("scripts", "No se puede generar el asiento de pago cuyo modelo no tiene asiento asociado"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
            return false;
    }     
	
    return true;
}
//// OFICIAL /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////

//// DESARROLLO /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
