/***************************************************************************
                 co_mastermodelo031.qs  -  description
                             -------------------
    begin                : mar sept 11 2012
    copyright            : (C) 2005 by InfoSiAL S.L.
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
    function abrirCerrarModeloClicked(){
        return this.ctx.oficial_abrirCerrarModeloClicked();
    }
    
    function abrirCerrarModelo(idModelo:String, ac:String):Boolean{
        return this.ctx.oficial_abrirCerrarModelo(idModelo, ac);
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
    connect (this.child("tbnAbrirCerrar"), "clicked()", this, "iface.abrirCerrarModeloClicked()");
}
//// INTERNA /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
/*El modelo tendra los tres estados en orden estricto: 
Emitido para la edición de datos
Cerrado para con los datos finales generar el asiento correspondiente
Pagado cuando el importe del modelo se paga por el banco*/

function oficial_abrirCerrarModeloClicked(){
        
    var cursor:FLSqlCursor = this.cursor();
    if (cursor.size() == 0) {
        return;
    }
        
    var ok:Boolean = true;
    cursor.transaction(false);
                
    var util:FLUtil = new FLUtil();
    var idModelo:Number = cursor.valueBuffer("idmodelo");
    var cerrado = cursor.valueBuffer("cerrado");
        
    if (cerrado == false){
        if (!this.iface.abrirCerrarModelo(cursor, "cerrar")){
            MessageBox.information("No ha sido posible cerrar el modelo", MessageBox.Ok, MessageBox.NoButton);
            ok = false;
        }
    } else if (cerrado == true){
        var res = MessageBox.information("El modelo está Cerrado, ¿Desea abrirlo?",MessageBox.Ok, MessageBox.Cancel);
        if (res != MessageBox.Ok){
            ok = false;
        }else{  
            if (!this.iface.abrirCerrarModelo(cursor, "abrir")){
                MessageBox.information("No ha sido posible re-abrir el modelo", MessageBox.Ok, MessageBox.NoButton);    
                ok = false;
            }
        }
    }
        
    if (ok){
        cursor.commit();
    }else{
        cursor.rollback();
    }
       
}

function oficial_abrirCerrarModelo(curModelo:FLSqlCursor, ac:String):Boolean
{
    var util:FLUtil = new FLUtil();
    var msn:String;
    if (ac == "cerrar") msn = "Cerrando";
    if (ac == "abrir") msn = "Abriendo";
    util.createProgressDialog(msn +" modelo 031 con DUA "+curModelo.valueBuffer("numreferencia"),5);
    util.setProgress(1);
    var cerrado:Boolean;
    
    var idModelo = curModelo.valueBuffer("idmodelo");
    util.setProgress(2);
    
    if (ac == "cerrar"){
        util.setProgress(3);
        cerrado = true;
    }        
                
    if (ac == "abrir"){
        util.setProgress(3);
        var idPagoModelo = util.sqlSelect("co_pagomodelo031","idpago","idmodelo="+idModelo);
        if (idPagoModelo && idPagoModelo!=""){
            MessageBox.warning("El modelo no puede abrirse, por favor elimine el pago",MessageBox.Ok, MessageBox.NoButton);
            util.destroyProgressDialog();
            return false;
        }
    }
    
    util.setProgress(4);
    
    curModelo.setModeAccess(curModelo.Edit);
    curModelo.refreshBuffer();
    curModelo.setValueBuffer("cerrado", cerrado);
    if (!curModelo.commitBuffer()) {
        util.destroyProgressDialog();
        return false;
    }
    
    util.destroyProgressDialog();
    
    this.child("tableDBRecords").refresh();
    return true;

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
