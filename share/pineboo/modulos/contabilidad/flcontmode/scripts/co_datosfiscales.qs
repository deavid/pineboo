/***************************************************************************
                 co_datosfiscales.qs  -  description
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
	function main() {
		this.ctx.interna_main();
	}
	function init() {
		this.ctx.interna_init();
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
class oficial extends interna {
	var bloqueoProvincia:Boolean;
    function oficial( context ) { interna( context ); }
	function bufferChanged(fN:String) {
		return this.ctx.oficial_bufferChanged(fN);
	}
}
//// OFICIAL /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration baseModelos */
/////////////////////////////////////////////////////////////////
//// BASE_MODELOS ///////////////////////////////////////////////
class baseModelos extends oficial {
    function baseModelos( context ) { oficial ( context ); }
	function init() {
		return this.ctx.baseModelos_init();
	}
	function bufferChanged(fN:String) {
		return this.ctx.baseModelos_bufferChanged(fN);
	}
}
//// BASE_MODELOS ///////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration modelo390 */
/////////////////////////////////////////////////////////////////
//// MODELO 390 /////////////////////////////////////////////////
class modelo390 extends baseModelos {
    function modelo390( context ) { baseModelos ( context ); }
	function bufferChanged(fN:String) {
		return this.ctx.modelo390_bufferChanged(fN);
	}
}
//// MODELO 390 /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration modelo031 */
/////////////////////////////////////////////////////////////////
//// MODELO 031 /////////////////////////////////////////////////
class modelo031 extends modelo390 {
    function modelo031( context ) { modelo390 ( context ); }
    var posActualPuntoSubSim:Number;
    var posActualPuntoSubHp:Number;
    var longSubcuenta:Number;
    var bloqueoSubcuenta:Boolean;
    function init() {
        return this.ctx.modelo031_init();
    }
    function validateForm():Boolean {
        return this.ctx.modelo031_validateForm();
    }
    function bufferChanged(fN:String) {
        return this.ctx.modelo031_bufferChanged(fN);
    }
}
//// MODELO 031 /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////
class head extends modelo031 {
    function head( context ) { modelo031 ( context ); }
}
//// DESARROLLO /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration ifaceCtx*/
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
/**
\C Los datos fiscales son únicos, por tanto el formulario no presenta los botones de navegación por registros.
\end

\D La gestión del formulario se hace de forma manual mediante el objeto f (FLFormSearchDB)
\end */
function interna_main()
{
		var f:Object = new FLFormSearchDB("co_datosfiscales");
		var cursor:FLSqlCursor = f.cursor();

		cursor.select();
		if (!cursor.first())
				cursor.setModeAccess(cursor.Insert);
		else
				cursor.setModeAccess(cursor.Edit);

		f.setMainWidget();
		if (cursor.modeAccess() == cursor.Insert)
				f.child("pushButtonCancel").setDisabled(true);
		cursor.refreshBuffer();
		var commitOk:Boolean = false;
		var acpt:Boolean;
		cursor.transaction(false);
		while (!commitOk) {
				acpt = false;
				f.exec("nombre");
				acpt = f.accepted();
				if (!acpt) {
						if (cursor.rollback())
								commitOk = true;
				} else {
						if (cursor.commitBuffer()) {
								cursor.commit();
								commitOk = true;
						}
				}
				f.close();
		}
}

function interna_validateForm():Boolean
{
	var cursor:FLSqlCursor = this.cursor();

	if (!flfactppal.iface.pub_validarProvincia(cursor)) {
		return false;
	}
}

function interna_init()
{
	var cursor:FLSqlCursor = this.cursor();

	this.iface.bloqueoProvincia = false;

	connect(cursor, "bufferChanged(QString)", this, "iface.bufferChanged");
}

//// INTERNA /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
function oficial_bufferChanged(fN:String)
{
	var util:FLUtil = new FLUtil();
	var cursor:FLSqlCursor = this.cursor();

	switch (fN) {
		case "provincia": {
			if (!this.iface.bloqueoProvincia) {
				this.iface.bloqueoProvincia = true;
				flfactppal.iface.pub_obtenerProvincia(this);
				this.iface.bloqueoProvincia = false;
			}
			break;
		}
		case "idprovincia": {
			if (cursor.valueBuffer("idprovincia") == 0) {
				cursor.setNull("idprovincia");
			}
			break;
		}
	}
}
//// OFICIAL /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition baseModelos */
/////////////////////////////////////////////////////////////////
//// BASE_MODELOS //////////////////////////////////////////////
function baseModelos_init()
{
	this.iface.__init();
	this.iface.bufferChanged("personafisica");
}

function baseModelos_bufferChanged(fN:String)
{
	var cursor:FLSqlCursor = this.cursor();
	var util:FLUtil = new FLUtil();
	var valor:String = "";
	switch (fN) {
		case "personafisica": {
			if (cursor.valueBuffer("personafisica") == true) {
				this.child("fdbApellidosRS").setDisabled(true);
				this.child("fdbNombrePF").setDisabled(false);
				this.child("fdbApellidosPF").setDisabled(false);
			} else {
				this.child("fdbApellidosRS").setDisabled(false);
				this.child("fdbNombrePF").setValue("");
				this.child("fdbApellidosPF").setValue("");
				this.child("fdbNombrePF").setDisabled(true);
				this.child("fdbApellidosPF").setDisabled(true);
			}
			break;
		}
		case "nombrepf": 
		case "apellidospf": {
			if (cursor.valueBuffer("apellidospf")) {
				valor += cursor.valueBuffer("apellidospf") + " ";
			}
			if (cursor.valueBuffer("nombrepf")) {
				valor += cursor.valueBuffer("nombrepf");
			}
			this.child("fdbApellidosRS").setValue(valor);
			break;
		}
		default: {
			this.iface.__bufferChanged(fN);
		}
	}
}
//// BASE_MODELOS ///////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition modelo390 */
/////////////////////////////////////////////////////////////////
//// MODELO 390 /////////////////////////////////////////////////
function modelo390_bufferChanged(fN:String)
{
	var cursor:FLSqlCursor = this.cursor();
	var util:FLUtil = new FLUtil();
	var valor:String = "";
	switch (fN) {
		case "personafisica": {
			if (cursor.valueBuffer("personafisica") == true) {
				this.child("fdbApellidosPF_2").setDisabled(false);
			} else {
				this.child("fdbApellidosPF_2").setValue("");
				this.child("fdbApellidosPF_2").setDisabled(true);
			}
			this.iface.__bufferChanged(fN);
			break;
		}
		case "nombrepf": 
		case "apellidospf":
		case "apellidospf2": {
			if (cursor.valueBuffer("apellidospf")) {
				valor += cursor.valueBuffer("apellidospf") + " ";
			}
			if (cursor.valueBuffer("apellidospf2")) {
				valor += cursor.valueBuffer("apellidospf2") + " ";
			}
			if (cursor.valueBuffer("nombrepf")) {
				valor += cursor.valueBuffer("nombrepf");
			}
			this.child("fdbApellidosRS").setValue(valor);
			break;
		}
		default: {
			this.iface.__bufferChanged(fN);
		}
	}
}

//// MODELO 390 /////////////////////////////////////////////////
////////////////////////////////////////////////////////////////

/** @class_definition modelo031 */
/////////////////////////////////////////////////////////////////
//// MODELO031 /////////////////////////////////////////////////
function modelo031_init()
{
    this.iface.__init();
    
    var util:FLUtil = new FLUtil();
    var cursor:FLSqlCursor = this.cursor();

    var ejercicioActual:String = flfactppal.iface.pub_ejercicioActual();
    this.child("fdbIdSubcuentaIVASIM").setFilter("codejercicio = '" + ejercicioActual + "'");
    this.child("fdbIdSubcuentaHPAcre").setFilter("codejercicio = '" + ejercicioActual + "'");

    if (sys.isLoadedModule("flcontppal")) {
        this.iface.longSubcuenta = util.sqlSelect("ejercicios", "longsubcuenta",  "codejercicio = '" + ejercicioActual + "'");
        this.iface.posActualPuntoSubSim = -1;
        this.iface.posActualPuntoSubHp = -1;
        this.iface.bloqueoSubcuenta = false;
    }
}

function modelo031_validateForm() {
    
    if(!this.iface.__validaForm()){
        return false;
    }
    
    if (!formRecordimpuestos.iface.comprobarSubcuentaIVA(cursor.valueBuffer("codsubcuentaivasim"), "IVASIM")) {
        return false;
    }
    
    if (!formRecordimpuestos.iface.comprobarSubcuentaIVA(cursor.valueBuffer("codsubcuentahpacre"), "IVAACR")) {
        return false;
    }
    
    return true;
}

function modelo031_bufferChanged(fN) {
    
    var cursor:FLSqlCursor = this.cursor();
    switch(fN) {
    /*U Al introducir un código de subcuenta, si el usuario pulsa la tecla del punto '.', la subcuenta se informa automaticamente con el código de cuenta más tantos ceros como sea necesario para completar la longitud de subcuenta asociada al ejercicio actual.
    \end */
    case "codsubcuentaivasim":
        if (!this.iface.bloqueoSubcuenta) {
            this.iface.bloqueoSubcuenta = true;
            this.iface.posActualPuntoSubSim = flcontppal.iface.pub_formatearCodSubcta(this, "fdbCodSubcuentaIVASIM", this.iface.longSubcuenta, this.iface.posActualPuntoSubSim);
            this.iface.bloqueoSubcuenta = false;
        }
        break;
    
    case "codsubcuentahpacre":
        if (!this.iface.bloqueoSubcuenta) {
            this.iface.bloqueoSubcuenta = true;
            this.iface.posActualPuntoSubHp = flcontppal.iface.pub_formatearCodSubcta(this, "fdbCodSubcuentaHPAcre", this.iface.longSubcuenta, this.iface.posActualPuntoSubHp);
            this.iface.bloqueoSubcuenta = false;
        }
        break;
    
    default:
        this.iface.__bufferChanged(fN);
    }
}
//// MODELO031 /////////////////////////////////////////////////
////////////////////////////////////////////////////////////////

/** @class_definition head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////

//// DESARROLLO /////////////////////////////////////////////////
//////////////////////////////////////////////////////////////