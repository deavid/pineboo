/***************************************************************************
                 factalma_general.qs  -  description
                             -------------------
    begin                : mie nov 23 2005
    copyright            : (C) 2004 by InfoSiAL S.L.
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
}
//// OFICIAL /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration jasperPlugin */
//////////////////////////////////////////////////////////////////
//// JASPER_PLUGIN ///////////////////////////////////////////////
class jasperPlugin extends oficial /** %from: oficial */ {
    function jasperPlugin( context ) { oficial( context ); }
    function init() {
        return this.ctx.jasperPlugin_init();
    }
    function seteaPath() {
            return this.ctx.jasperPlugin_seteaPath();
     }
    function seteaPlugin() {
            return this.ctx.jasperPlugin_seteaPlugin();
     }
    function testJava() {
            return this.ctx.jasperPlugin_testJava();
     }
    function testPlugin() {
            return this.ctx.jasperPlugin_testPlugin();
     }
     function checkRT() {
            return this.ctx.jasperPlugin_checkRT();
     }
     function checkCompilar() {
            return this.ctx.jasperPlugin_checkCompilar();
     }
     function checkGuardaTemporal() {
            return this.ctx.jasperPlugin_checkGuardaTemporal();
     }
     function fixPath(ruta:String):String {
            return this.ctx.jasperPlugin_fixPath(ruta);
    }
    function guardaCodificacion() {
            return this.ctx.jasperPlugin_guardaCodificacion();
     }
    function guardaMaxJVM() {
            return this.ctx.jasperPlugin_guardaMaxJVM();
     }
    }

//// JASPER_PLUGIN ///////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////
class head extends jasperPlugin {
	function head( context ) { jasperPlugin ( context ); }
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
/**
\C Los datos generales son únicos, por tanto formulario de no presenta los botones de navegación por registros.
\end

\D La gestión del formulario se hace de forma manual mediante el objeto f (FLFormSearchDB)
\end
\end */
function interna_main()
{
	var f:Object = new FLFormSearchDB("factinfo_general");
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
		f.exec("id");
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

function interna_init()
{
	var util:FLUtil = new FLUtil;
	var cursor:FLSqlCursor = this.cursor();

	connect (cursor, "bufferChanged(QString)", this, "iface.bufferChanged");

}

function interna_calculateField(fN:String):String
{
	var util:FLUtil = new FLUtil;
	var cursor:FLSqlCursor = this.cursor();
	var valor:String;

	switch (fN) {
		case "x": {
			break;
		}
		default: {
			valor = this.iface.__calculateField(fN);
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
function oficial_bufferChanged(fN:String)
{
	var util:FLUtil = new FLUtil;
	var cursor:FLSqlCursor = this.cursor();
	switch (fN) {
		case "X": {
			break;
		}
	}
}
//// OFICIAL /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition jasperPlugin */
//////////////////////////////////////////////////////////////////
//// JASPER_PLUGIN ///////////////////////////////////////////////
function jasperPlugin_init()
{
    var util:FLUtil = new FLUtil;
    connect(this.child("pbPath"), "clicked()", this, "iface.seteaPath");
    connect(this.child("pbJPlugin"), "clicked()", this, "iface.seteaPlugin");
    connect(this.child("pbJava"), "clicked()", this, "iface.testJava");
    connect(this.child("pbPlugin"), "clicked()", this, "iface.testPlugin");
    connect(this.child("chbRT"), "clicked()", this, "iface.checkRT");
    connect(this.child("chbCompilar"), "clicked()", this, "iface.checkCompilar");
    connect(this.child("chbGuardaTemporal"), "clicked()", this, "iface.checkGuardaTemporal");
    connect(this.child("cBCodificacion"), "activated(int)", this, "iface.guardaCodificacion");
    connect(this.child("leMaxJVM"), "textChanged(QString)", this, "iface.guardaMaxJVM");;
    this.child("lnJPlugin").text = util.readSettingEntry("jasperplugin/pluginpath");
    this.child("lnJPlugin").setEnabled(false);
    this.child("lnPath").text = util.readSettingEntry("jasperplugin/reportspath");
    this.child("lnPath").setEnabled(false);
    this.child("leMaxJVM").text = util.readSettingEntry("jasperplugin/MaxJVM");
    this.child("chbRT").checked = util.readSettingEntry("jasperplugin/detecRT");
    this.child("chbGuardaTemporal").checked = util.readSettingEntry("jasperplugin/guardatemporal");
    this.child("chbCompilar").checked = util.readSettingEntry("jasperplugin/compilarSiempre");
    this.child("cBCodificacion").currentItem = util.readSettingEntry("jasperplugin/codificacion");
    this.iface.__init();
}
function jasperPlugin_seteaPath()
{
    var util:FLUtil = new FLUtil;
    var dirBasePath = this.iface.fixPath(FileDialog.getExistingDirectory(Dir.home));

    if (!dirBasePath)
    return;
    this.child("lnPath").text = dirBasePath;
    util.writeSettingEntry("jasperplugin/reportspath",dirBasePath);
}
function jasperPlugin_seteaPlugin()
{
    var util:FLUtil = new FLUtil;
    var dirBasePath = this.iface.fixPath(FileDialog.getExistingDirectory(Dir.home));

    if (!dirBasePath)
    return;
    this.child("lnJPlugin").text = dirBasePath;
    util.writeSettingEntry("jasperplugin/pluginpath",dirBasePath);
}
function jasperPlugin_testJava()
{
    var util:FLUtil = new FLUtil;
    var resultado:Array = flfactppal.iface.pub_ejecutarComandoAsincrono("java -version");
        MessageBox.information(util.translate("scripts", resultado["salida"]), MessageBox.Ok);
}
function jasperPlugin_testPlugin()
{
    var util:FLUtil = new FLUtil;
    var ruta:String = this.child("lnJPlugin").text + "enebooreports.jar";
    if (File.exists(ruta))
    	{
    	if (flfactinfo.iface.procesoInicializado)
    		{
    		flfactinfo.iface.procesoJP.kill();
    		flfactinfo.iface.procesoInicializado = false;
    		}
    	flfactinfo.iface.pub_lanzarInforme(this.cursor(), "version","", "", false, false,"","","","",false);
        }
     else MessageBox.information(util.translate("scripts", "¡¡ Ruta incorrecta !! \n " + ruta), MessageBox.Ok);
}
function jasperPlugin_checkRT()
{
   var util:FLUtil = new FLUtil;
   var pulsado:Boolean = false;
   if (this.child("chbRT").checked) pulsado = true;
  //debug ("JASPER_PLUGIN :: Guardando checkRT = " + pulsado);
   util.writeSettingEntry("jasperplugin/detecRT",pulsado);
}
function jasperPlugin_checkCompilar()
{
   var util:FLUtil = new FLUtil;
   var pulsado:Boolean = false;
   if (this.child("chbCompilar").checked) pulsado = true;
  //debug ("JASPER_PLUGIN :: Guardando checkCompilar = " + pulsado);
   util.writeSettingEntry("jasperplugin/compilarSiempre",pulsado);
}
function jasperPlugin_checkGuardaTemporal()
{
   var util:FLUtil = new FLUtil;
   var pulsado:Boolean = false;
   if (this.child("chbGuardaTemporal").checked) pulsado = true;
   util.writeSettingEntry("jasperplugin/guardatemporal",pulsado);
}
function jasperPlugin_fixPath(ruta:String):String
{
var rutaFixed:String;
    if (sys.osName() == "WIN32")
            {
           var barra = "\\";
        while (ruta != rutaFixed)
                    {
                    rutaFixed = ruta;
                    ruta = ruta.replace("/",barra);
                    }
        if (!rutaFixed.endsWith(barra)) rutaFixed +="\\";
            } else
                rutaFixed= ruta;
return rutaFixed;
}
function jasperPlugin_guardaCodificacion()
{
   var util:FLUtil = new FLUtil;
   util.writeSettingEntry("jasperplugin/codificacion",this.child("cBCodificacion").currentItem);
}

function jasperPlugin_guardaMaxJVM()
{
   var util:FLUtil = new FLUtil;
   util.writeSettingEntry("jasperplugin/MaxJVM",this.child("leMaxJVM").text);
}
//// JASPER_PLUGIN ///////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_definition head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////

//// DESARROLLO /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

