/***************************************************************************
                 flfactinfo.qs  -  description
                             -------------------
    begin                : lun abr 26 2004
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
    function init() { this.ctx.interna_init(); }
}
//// INTERNA /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
class oficial extends interna {
        var visor_:FLReportViewer;
        var variosIvas_:Boolean;
        var acumulados:Array = []; // Acumulados de valores numéricos en el informe
        var cuentaAcum:Array = []; // Almacena cuántos valores se han acumulado en cada índice del array acumulados
        var ultIdDocPagina:String;
        var paginaActual:Number;
    function oficial( context ) { interna( context ); }
        function datosPieFactura(nodo:FLDomNode, campo:String):Number {
                return this.ctx.oficial_datosPieFactura(nodo, campo);
        }
        function crearInforme(nombreInforme:String) {
                return this.ctx.oficial_crearInforme(nombreInforme);
        }
        function lanzarInforme(cursor:FLSqlCursor, nombreInforme:String, orderBy:String, groupBy:String, etiquetas:Boolean, impDirecta:Boolean, whereFijo:String, nombreReport:String, numCopias:Number, impresora:String, pdf:Boolean) {
                return this.ctx.oficial_lanzarInforme(cursor, nombreInforme, orderBy, groupBy, etiquetas, impDirecta, whereFijo, nombreReport, numCopias, impresora, pdf);
        }
        function seleccionEtiquetaInicial():Array {
                return this.ctx.oficial_seleccionEtiquetaInicial();
        }
        function establecerConsulta(cursor:FLSqlCursor, nombreConsulta:String, orderBy:String, groupBy:String, whereFijo:String):FLSqlQuery {
                return this.ctx.oficial_establecerConsulta(cursor, nombreConsulta, orderBy, groupBy, whereFijo);
        }
        function obtenerSigno(s:String):String {
                return this.ctx.oficial_obtenerSigno(s);
        }
        function fieldName(s:String):String {
                return this.ctx.oficial_fieldName(s);
        }
        function obtenerAcumulado(nodo:FLDomNode, campo:String):String {
                return this.ctx.oficial_obtenerAcumulado(nodo,campo);
        }
        function acumularValor(nodo:FLDomNode, campo:String):String {
                return this.ctx.oficial_acumularValor(nodo, campo);
        }
        function restaurarAcumulado(nodo:FLDomNode, campo:String):String {
                return this.ctx.oficial_restaurarAcumulado(nodo, campo);
        }
        function logo(nodo:FLDomNode, campo:String):String {
                return this.ctx.oficial_logo(nodo, campo);
        }
        function porIVA(nodo:FLDomNode, campo:String):String {
                return this.ctx.oficial_porIVA(nodo, campo);
        }
        function desgloseIva(nodo:FLDomNode, campo:String):String {
                return this.ctx.oficial_desgloseIva(nodo, campo);
        }
        function desgloseBaseImponible(nodo:FLDomNode, campo:String):String {
                return this.ctx.oficial_desgloseBaseImponible(nodo, campo);
        }
        function desgloseRecargo(nodo:FLDomNode, campo:String):String {
                return this.ctx.oficial_desgloseRecargo(nodo, campo);
        }
        function desgloseTotal(nodo:FLDomNode, campo:String):String {
                return this.ctx.oficial_desgloseTotal(nodo, campo);
        }
        function vencimiento(nodo:FLDomNode, campo:String):String {
                return this.ctx.oficial_vencimiento(nodo, campo);
        }
        function reemplazar(cadena:String, patronOrigen:String, patronDestino:String):String {
                return this.ctx.oficial_reemplazar(cadena, patronOrigen, patronDestino);
        }
        function cuentaFacturaCli(nodo:FLDomNode, campo:String):String {
                return this.ctx.oficial_cuentaFacturaCli(nodo, campo);
        }
        function valorIRPF(nodo:FLDomNode, campo:String):String {
                return this.ctx.oficial_valorIRPF(nodo, campo);
        }
        function numPagina(nodo:FLDomNode, campo:String):String {
                return this.ctx.oficial_numPagina(nodo, campo);
        }
        function aplicarCriterio(tabla:String, campo:String, valor:String, signo:String):String {
                return this.ctx.oficial_aplicarCriterio(tabla, campo, valor, signo);
        }
        function ampliarWhere(nombreConsulta:String):String {
                return this.ctx.oficial_ampliarWhere(nombreConsulta);
        }
        function dibujarGrafico(xmlDatos:FLDomDocument):Picture {
                return this.ctx.oficial_dibujarGrafico(xmlDatos);
        }
        function dibujarGrafico2DBarras(xmlDatos:FLDomDocument):Picture {
                return this.ctx.oficial_dibujarGrafico2DBarras(xmlDatos);
        }
        function dibujarGrafico2DMapaProvEs(xmlDatos:FLDomDocument):Picture {
                return this.ctx.oficial_dibujarGrafico2DMapaProvEs(xmlDatos);
        }
        function dibujarGrafico2DMapaPaisesEu(xmlDatos:FLDomDocument):Picture {
                return this.ctx.oficial_dibujarGrafico2DMapaPaisesEu(xmlDatos);
        }
        function formatearValor(valor:String,formatValor:String):String {
                return this.ctx.oficial_formatearValor(valor,formatValor);
        }
        function dameColor(color:String):Color {
                return this.ctx.oficial_dameColor(color);
        }
        function dameFuente(family:String, size:Number):Font {
                return this.ctx.oficial_dameFuente(family, size);
        }
        function mostrarInformeVisor(visor:FLReportViewer):Boolean {
                return this.ctx.oficial_mostrarInformeVisor(visor);
        }
}
//// OFICIAL /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration jasperPlugin */
//////////////////////////////////////////////////////////////////
//// JASPER_PLUGIN ///////////////////////////////////////////////
class jasperPlugin extends oficial /** %from: oficial */ {
    var rutaReports:String;
    var dbName:String;
    var reportsFolder:String;
    var barra:String;
    var procesoJP:Process;
    var procesoInicializado:Boolean = false;
    var procesoVisible:Boolean = false;
    var rutaTrabajoVieja:String;
    var detectarRutaTrabajo:Boolean;
    var guardaTemporal:Boolean;
    var whereCursor:String;
    var reportAnterior;
    function jasperPlugin( context ) { oficial( context ); }
function lanzarInforme(cursor:FLSqlCursor, nombreInforme:String, orderBy:String, groupBy:String, etiquetas:Boolean, impDirecta:Boolean, whereFijo:String, nombreReport:String, numCopias:Number, impresora:String, pdf:Boolean) {
        return this.ctx.jasperPlugin_lanzarInforme(cursor, nombreInforme, orderBy, groupBy, etiquetas, impDirecta, whereFijo, nombreReport, numCopias, impresora, pdf);
    }
function comprobarJasperFisico( reportName:String ):Boolean {
            return this.ctx.jasperPlugin_comprobarJasperFisico(reportName);
    }
function seteaBarra():String {
        return this.ctx.jasperPlugin_seteaBarra();
    }
    function tratarReport(nombreFichero:String, consultaOriginalSQL:String ):String {
        return this.ctx.jasperPlugin_tratarReport(nombreFichero, consultaOriginalSQL);
    }
    function generarComando( rutaJP:String ):Boolean {
       return this.ctx.jasperPlugin_generarComando(rutaJP );
    }
   function datosProcesoRecibidos() {
       return this.ctx.jasperPlugin_datosProcesoRecibidos();
    }
    function establecerConsulta(cursor:FLSqlCursor, nombreConsulta:String, orderBy:String, groupBy:String, whereFijo:String):FLSqlQuery {
                return this.ctx.jasperPlugin_establecerConsulta(cursor, nombreConsulta, orderBy, groupBy, whereFijo);
        }

}
//// JASPER_PLUGIN ///////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration jPluginPlus */
/////////////////////////////////////////////////////////////////
//// JPLUGIN_PLUS //////////////////////////////////////////////
class jPluginPlus extends jasperPlugin /** %from: jasperPlugin */ {
    function jPluginPlus( context ) { jasperPlugin ( context ); }
	function lanzarInforme(cursor:FLSqlCursor, nombreInforme:String, orderBy:String, groupBy:String, etiquetas:Boolean, impDirecta:Boolean, whereFijo:String, nombreReport:String, numCopias:Number, impresora:String, pdf:Boolean) {
		return this.ctx.jPluginPlus_lanzarInforme(cursor, nombreInforme, orderBy, groupBy, etiquetas, impDirecta, whereFijo, nombreReport, numCopias, impresora, pdf);
	}
	function cargaDescripcionJasper(fichero:String):String {
		return this.ctx.jPluginPlus_cargaDescripcionJasper(fichero);
	}
}

//// JPLUGIN_PLUS ////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration recibosProv */
/////////////////////////////////////////////////////////////////
//// RECIBOS PROV ///////////////////////////////////////////////
class recibosProv extends jPluginPlus /** %from: oficial */ {
    function recibosProv( context ) { jPluginPlus ( context ); }
	function aplicarCriterio(tabla:String, campo:String, valor:String, signo:String):String {
		return this.ctx.recibosProv_aplicarCriterio(tabla, campo, valor, signo);
	}
}
//// RECIBOS PROV ///////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration infoVtos */
/////////////////////////////////////////////////////////////////
//// INFO_VENCIMIENTOS //////////////////////////////////////////
class infoVtos extends recibosProv /** %from: oficial */ {
    function infoVtos( context ) { recibosProv ( context ); }
	function cabeceraVencimientos(nodo:FLDomNode, campo:String):String {
		return this.ctx.infoVtos_cabeceraVencimientos(nodo, campo);
	}
}
//// INFO_VENCIMIENTOS //////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration infoCliProv */
/////////////////////////////////////////////////////////////////
//// INFOCLIPROV //////////////////////////////////////////////////
class infoCliProv extends infoVtos /** %from: oficial */ {
	var idInformeActual:Number;
	function infoCliProv( context ) { infoVtos ( context ); }
	function cabeceraClientes(nodo:FLDomNode, campo:String):String {
		return this.ctx.infoCliProv_cabeceraClientes(nodo, campo);
	}
	function cabeceraProveedores(nodo:FLDomNode, campo:String):String {
		return this.ctx.infoCliProv_cabeceraProveedores(nodo, campo);
	}
	function establecerId(id:Number) {
		return this.ctx.infoCliProv_establecerId(id);
	}
}
//// INFOCLIPROV //////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration envioMail */
/////////////////////////////////////////////////////////////////
//// ENVIO MAIL /////////////////////////////////////////////////
class envioMail extends infoCliProv /** %from: oficial */ {
	var datosEMail:Array;
    function envioMail( context ) { infoCliProv ( context ); }
	function mostrarInformeVisor(visor:FLReportViewer):Boolean {
		return this.ctx.envioMail_mostrarInformeVisor(visor);
	}
}
//// ENVIO MAIL /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration dtoEspecial */
/////////////////////////////////////////////////////////////////
//// DTOESPECIAL/////////////////////////////////////////////////
class dtoEspecial extends envioMail /** %from: oficial */ {
    function dtoEspecial( context ) { envioMail ( context ); }
	function descuento(nodo:FLDomNode, campo:String):String {
		return this.ctx.dtoEspecial_descuento(nodo, campo);
	}
}
//// DTOESPECIAL /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration sepa19b2b */
/////////////////////////////////////////////////////////////////
//// SEPA19B2B /////////////////////////////////////////////////
class sepa19b2b extends dtoEspecial /** %from: oficial */
{
  function sepa19b2b(context)
  {
    dtoEspecial(context);
  }
  function codpostalCiudadProvinciaCliente(nodo, campo)
  {
  	return this.ctx.sepa19b2b_codpostalCiudadProvinciaCliente(nodo, campo);
  }
  function dameIdentificadorAcreedor(nodo, campo)
  {
  	return this.ctx.sepa19b2b_dameIdentificadorAcreedor(nodo, campo);
  }
  function codpostalCiudadProvincia(nodo, campo)
  {
    return this.ctx.sepa19b2b_codpostalCiudadProvincia(nodo, campo);
  }
}
//// SEPA_19B2B /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration pubInfoCliProv */
/////////////////////////////////////////////////////////////////
//// PUBINFOCLIPROV //////////////////////////////////////////////////
class pubInfoCliProv extends sepa19b2b /** %from: infoCliProv */ {
	function pubInfoCliProv( context ) { sepa19b2b ( context ); }
	function pub_cabeceraClientes(nodo:FLDomNode, campo:String):String {
		return this.cabeceraClientes(nodo, campo);
	}
	function pub_cabeceraProveedores(nodo:FLDomNode, campo:String):String {
		return this.cabeceraProveedores(nodo, campo);
	}
	function pub_establecerId(id:Number) {
		return this.establecerId(id);
	}
}

//// PUBINFOCLIPROV //////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////
class head extends pubInfoCliProv {
    function head( context ) { pubInfoCliProv ( context ); }
}
//// DESARROLLO /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration ifaceCtx */
/////////////////////////////////////////////////////////////////
//// INTERFACE  /////////////////////////////////////////////////
class ifaceCtx extends head {
        function ifaceCtx( context ) { head( context ); }
        function pub_lanzarInforme(cursor:FLSqlCursor, nombreInforme:String, orderBy:String, groupBy:String, etiquetas:Boolean, impDirecta:Boolean, whereFijo:String, nombreReport:String, numCopias:Number, impresora:String, pdf:Boolean) {
        return this.lanzarInforme(cursor, nombreInforme, orderBy, groupBy, etiquetas, impDirecta, whereFijo, nombreReport, numCopias, impresora, pdf);
        }
        function pub_datosPieFactura(nodo:FLDomNode, campo:String):Number {
                return this.datosPieFactura(nodo, campo);
        }
        function pub_logo(nodo:FLDomNode, campo:String):String {
                return this.logo(nodo, campo);
        }
        function pub_porIVA(nodo:FLDomNode, campo:String):String {
                return this.porIVA(nodo, campo);
        }
        function pub_desgloseIva(nodo:FLDomNode, campo:String):String {
                return this.desgloseIva(nodo, campo);
        }
        function pub_desgloseBaseImponible(nodo:FLDomNode, campo:String):String {
                return this.desgloseBaseImponible(nodo, campo);
        }
        function pub_desgloseRecargo(nodo:FLDomNode, campo:String):String {
                return this.desgloseRecargo(nodo, campo);
        }
        function pub_desgloseTotal(nodo:FLDomNode, campo:String):String {
                return this.desgloseTotal(nodo, campo);
        }
        function pub_valorIRPF(nodo:FLDomNode, campo:String):String {
                return this.valorIRPF(nodo, campo);
        }
        function pub_establecerConsulta(cursor:FLSqlCursor, nombreConsulta:String, orderBy:String, groupBy:String, whereFijo:String):FLSqlQuery {
                return this.establecerConsulta(cursor, nombreConsulta, orderBy, groupBy, whereFijo);
        }
        function pub_dibujarGrafico(xmlDatos:FLDomDocument):Picture {
                return this.dibujarGrafico(xmlDatos);
        }
        function pub_mostrarInformeVisor(visor:FLReportViewer):Boolean {
                return this.mostrarInformeVisor(visor);
        }
}

//// INTERFACE  /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

const iface = new pubDtoEspecial( this );

/** @class_declaration pubInfoVtos */
/////////////////////////////////////////////////////////////////
//// PUB_INFO_VENCIMIENTOS //////////////////////////////////////
class pubInfoVtos extends ifaceCtx /** %from: ifaceCtx */ {
    function pubInfoVtos( context ) { ifaceCtx ( context ); }
	function pub_cabeceraVencimientos(nodo:FLDomNode, campo:String):String {
		return this.cabeceraVencimientos(nodo, campo);
	}
}
//// PUB_INFO_VENCIMIENTOS //////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration pubDtoEspecial */
/////////////////////////////////////////////////////////////////
//// PUB_DTOESPECIAL//////////////////////////////////////////////////
class pubDtoEspecial extends pubInfoVtos /** %from: ifaceCtx */ {
	function pubDtoEspecial( context ) { pubInfoVtos( context ); }
	function pub_descuento(nodo:FLDomNode, campo:String):Number {
		return this.descuento(nodo, campo);
	}
}

//// PUB_DTOESPECIAL /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition interna */
////////////////////////////////////////////////////////////////////////////
//// DEFINICION ////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////
//// INTERNA /////////////////////////////////////////////////////
function interna_init() {
        var util:FLUtil = new FLUtil;
        util.writeSettingEntry("kugar/banner", "");
}
//// INTERNA /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
/** \D
Obtiene los datos de totalización de pie de factura
@param        nodo: Nodo XML con los datos de la línea que se va a mostrar en el informe
@param        campo: Campo a mostrar
@return        Valor del campo
\end */
function oficial_datosPieFactura(nodo:FLDomNode, campo:String):Number
{
                var util:FLUtil = new FLUtil();
                var sCampo:String = campo.toString();
                var tablaFacturas:String;
                var tablaIva:String;
                if (sCampo.charAt(0) == "P"
                                && sCampo.charAt(1) == "_") {
                                tablaFacturas = "facturasprov";
                                tablaIva = "lineasivafactprov";
                                campo = "";
                                for (var i:Number = 2; i < sCampo.length; i++)
                                                campo += sCampo.charAt(i);
                } else {
                                tablaFacturas = "facturascli";
                                tablaIva = "lineasivafactcli";
                }

                var idFactura:Number = nodo.attributeValue(tablaFacturas + ".idfactura");
                var util:FLUtil = new FLUtil;
                var res:Number;
                if (campo == "BI4") {
                                res = util.sqlSelect(tablaIva, "neto", "idfactura = " + idFactura + " AND iva = 4");
                } else if (campo == "BI7") {
                                res = util.sqlSelect(tablaIva, "neto", "idfactura = " + idFactura + " AND (iva = 7 OR iva = 8)");
                } else if (campo == "BI16") {
                                res = util.sqlSelect(tablaIva, "neto", "idfactura = " + idFactura + " AND (iva = 16 OR iva = 18)");
                } else if (campo == "IVA4") {
                                res = util.sqlSelect(tablaIva, "totaliva", "idfactura = " + idFactura + " AND iva = 4");
                } else if (campo == "IVA7") {
                                res = util.sqlSelect(tablaIva, "totaliva", "idfactura = " + idFactura + " AND (iva = 7 OR iva = 8)");
                } else if (campo == "IVA16") {
                                res = util.sqlSelect(tablaIva, "totaliva", "idfactura = " + idFactura + " AND (iva = 16 OR iva = 18)");
                } else if (campo == "POR_RE4") {
                                res = util.sqlSelect(tablaIva, "recargo", "idfactura = " + idFactura + " AND iva = 4");
                                if (res && parseFloat(res) != 0)
                                                res += "%";
                } else if (campo == "POR_RE7") {
                                res = util.sqlSelect(tablaIva, "recargo", "idfactura = " + idFactura + " AND (iva = 7 OR iva = 8)");
                                if (res && parseFloat(res) != 0)
                                                res += "%";
                } else if (campo == "POR_RE16") {
                                res = util.sqlSelect(tablaIva, "recargo", "idfactura = " + idFactura + " AND (iva = 16 OR iva = 18)");
                                if (res && parseFloat(res) != 0)
                                                res += "%";
                } else if (campo == "RE4") {
                                res = util.sqlSelect(tablaIva, "totalrecargo", "idfactura = " + idFactura + " AND iva = 4");
                                if (parseFloat(res) != 0)
                                                res = util.buildNumber(res, "f", 2);
                } else if (campo == "RE7") {
                                res = util.sqlSelect(tablaIva, "totalrecargo", "idfactura = " + idFactura + " AND (iva = 7 OR iva = 8)");
                                if (parseFloat(res) != 0)
                                                res = util.buildNumber(res, "f", 2);
                } else if (campo == "RE16") {
                                res = util.sqlSelect(tablaIva, "totalrecargo", "idfactura = " + idFactura + " AND (iva = 16 OR iva = 18)");
                                if (parseFloat(res) != 0)
                                                res = util.buildNumber(res, "f", 2);
                } else if (campo == "T4") {
                                res = util.sqlSelect(tablaIva, "totallinea", "idfactura = " + idFactura + " AND iva = 4");
                } else if (campo == "T7") {
                                res = util.sqlSelect(tablaIva, "totallinea", "idfactura = " + idFactura + " AND (iva = 7 OR iva = 8)");
                } else if (campo == "T16") {
                                res = util.sqlSelect(tablaIva, "totallinea", "idfactura = " + idFactura + " AND (iva = 16 OR iva = 18)");
                }
                if (parseFloat(res) == 0 || !res)
                                res = "";
                return res;
}

/** \D
Crea el informe especificado
@param        nombreinforme: Nombre del informe a crear
\end */
function oficial_crearInforme(nombreInforme:String)
{
                if (this.iface.establecerCriteriosBusqueda(nombreInforme) == true);
                        this.iface.lanzarInforme(nombreInforme);
}

/** \D Establece la fila y columna de la primera etiqueta a imprimir para los informes de etiquetas
\end */
function oficial_seleccionEtiquetaInicial():Array
{
        var etiquetaInicial:Array = [];
        etiquetaInicial["fila"] = 0;
        etiquetaInicial["col"] = 0;
        var util:FLUtil = new FLUtil;
        var dialog:Object = new Dialog;
        dialog.caption = util.translate("scripts","Elegir fila y columna a imprimir");
        dialog.okButtonText = util.translate("scripts","Aceptar");
        dialog.cancelButtonText = util.translate("scripts","Cancelar");

        var text:Object = new Label;
        text.text = util.translate("scripts","Ha seleccionado un informe de etiquetas,\nelija la fila y la columna a imprimir:");
        dialog.add(text);

        var spbNumColum:Object= new SpinBox;
        spbNumColum.label = util.translate("scripts","Columnas");
        spbNumColum.minimum = 1;
        spbNumColum.maximum = 30;
        dialog.add(spbNumColum);

        var spbNumFila:Object = new SpinBox;
        spbNumFila.label = util.translate("scripts","Filas");
        spbNumFila.minimum = 1;
        spbNumFila.maximum = 30;
        dialog.add(spbNumFila);

        if (dialog.exec()){
                etiquetaInicial["fila"] = spbNumFila.value;
                etiquetaInicial["col"] = spbNumColum.value;
        }
        return etiquetaInicial;
}

/** \D Establece la consulta del informe, creando el where a partir de los campos del cursor
@param        cursor: Cursor posicionado en un registro de criterios de búsqueda
@param        nombreConsulta: Nombre del fichero con la descripción de la consulta
@param        orderBy: Cláusula Order By
@param        groupBy: Cláusula Group By
@param        whereFijo: Cláusula Where que se añade al construido a partir de los campos del cursor
@return        consulta o false si hay error
\end */
function oficial_establecerConsulta(cursor:FLSqlCursor, nombreConsulta:String, orderBy:String, groupBy:String, whereFijo:String):FLSqlQuery
{
        var util:FLUtil = new FLUtil();
        var q:FLSqlQuery = new FLSqlQuery(nombreConsulta);
        var fieldList:String = util.nombreCampos(cursor.table());
        var cuenta:Number = parseFloat(fieldList[0]);

        var signo:String;
        var fN:String;
        var valor:String;
        var primerCriterio:Boolean = false;
        var where:String = "";
        var criterio:String;
        for (var i:Number = 1; i <= cuenta; i++) {
                if (cursor.isNull(fieldList[i])) {
                        continue;
                }
                signo = this.iface.obtenerSigno(fieldList[i]);
                if (signo != "") {
                        fN = this.iface.fieldName(fieldList[i]);
                        valor = cursor.valueBuffer(fieldList[i]);
                        criterio = this.iface.aplicarCriterio(cursor.table(), fN, valor, signo);
                        if (criterio && criterio != "") {
                                if (primerCriterio == true) {
                                        where += " AND ";
                                }
                                where += criterio;
                                primerCriterio = true;
                        }
                }
        }

        if (whereFijo && whereFijo != "") {
                if (where == "")
                        where = whereFijo;
                else
                        where = whereFijo + " AND (" + where + ")";
        }

        var ampliarWhere:String = this.iface.ampliarWhere(nombreConsulta);
        if (ampliarWhere)
                if (where)
                        where += " AND " + ampliarWhere;
                else
                        where += ampliarWhere;

        if (groupBy && groupBy != "") {
                if (where == "")
                        where = "1 = 1";
                where += " GROUP BY " + groupBy;
        }

        q.setWhere(where);

        if (orderBy)
                q.setOrderBy(orderBy);

        return q;
}

/** Construye un criterio de búsqueda para la consulta
@param        Tabla: Tabla de criterios
@param        Campo: Campo de criterios
@param        Valor: Valor del criterio
@param        Signo: Signo del criterio
@return Criterio (típicamente tabla.campo signo criterio. Ej facturascli.codcliente = '000001')
\end */
function oficial_aplicarCriterio(tabla:String, campo:String, valor:String, signo:String):String
{
        var criterio:String = "";
        switch (tabla) {
                case "i_reciboscli": {
                        switch (campo) {
                                case "reciboscli.estado": {
                                        switch (valor) {
                                                case "Pendiente": {
                                                        criterio = "reciboscli.estado IN ('Emitido', 'Devuelto')";
                                                        break;
                                                }
                                        }
                                        break;
                                }
                        }
                        break;
                }
                case "i_pedidoscli": {
                        switch (campo) {
                                case "pedidoscli.servido": {
                                        switch(valor) {
                                                case "Pendiente": {
                                                        criterio = "pedidoscli.servido IN ('No','Parcial')";
                                                }
                                        }
                                        break;
                                }
                        }
                        break;
                }
                case "i_pedidosprov": {
                        switch (campo) {
                                case "pedidosprov.servido": {
                                        switch(valor) {
                                                case "Pendiente": {
                                                        criterio = "pedidosprov.servido IN ('No','Parcial')";
                                                }
                                        }
                                        break;
                                }
                        }
                        break;
                }
        }

        if (criterio == "") {
                if (valor == "Sí")
                        valor = 1;
                if (valor == "No")
                        valor = 0;
                if (valor == "Todos")
                        valor = "";
                if (!valor.toString().isEmpty()) {
                        criterio = campo + " " + signo + " '" + valor + "' ";
                }
        }
        return criterio;
}
/** \D
Lanza un informe
@param        cursor: Cursor con los criterios de búsqueda para la consulta base del informe
@param        nombreinforme: Nombre del informe
@param        orderBy: Cláusula ORDER BY de la consulta base
@param        groupBy: Cláusula GROUP BY de la consulta base
@param        etiquetas: Indicador de si se trata de un informe de etiquetas
@param        impDirecta: Indicador para imprimir directaemnte el informe, sin previsualización
@param        whereFijo: Sentencia where que debe preceder a la sentencia where calculada por la función
\end */
function oficial_lanzarInforme(cursor:FLSqlCursor, nombreInforme:String, orderBy:String, groupBy:String, etiquetas:Boolean, impDirecta:Boolean, whereFijo:String, nombreReport:String, numCopias:Number, impresora:String, pdf:Boolean)
{
        var util:FLUtil = new FLUtil();
        var etiquetaInicial:Array = [];
        if (etiquetas == true) {
                etiquetaInicial = this.iface.seleccionEtiquetaInicial();
        } else {
                etiquetaInicial["fila"] = 0;
                etiquetaInicial["col"] = 0;
        }

        this.iface.ultIdDocPagina = "";

        var q:FLSqlQuery = this.iface.establecerConsulta(cursor, nombreInforme, orderBy, groupBy, whereFijo);
debug("------ CONSULTA -------" + q.sql());
        if (q.exec() == false) {
                MessageBox.critical(util.translate("scripts", "Falló la consulta"), MessageBox.Ok, MessageBox.NoButton);
                return;
        } else {
                if (q.first() == false) {
                        MessageBox.warning(util.translate("scripts", "No hay registros que cumplan los criterios de búsqueda establecidos"), MessageBox.Ok, MessageBox.NoButton);
                        return;
                }
        }

        var tipoReport:String = "";
        if (!nombreReport || nombreReport == "") {
                nombreReport = nombreInforme;
        } else {
                var extension:String;
                var iPunto:Number = nombreReport.findRev(".");
                if (iPunto > -1) {
                        extension = nombreReport.right(nombreReport.length - (iPunto + 1));
                        nombreReport = nombreReport.left(iPunto);
                        if (extension.toLowerCase() == "jxml") {
                                tipoReport = "JasperQueryData";
                        } else if (extension.toLowerCase() == "jdxml") {
                                tipoReport = "JasperXmlData";
                        }
                }
                debug("extension = '" + extension + "'");
                debug("nombreReport = '" + nombreReport + "'");
                debug("tipoReport = '" + tipoReport + "'");
        }

        switch (tipoReport) {
                case "JasperQueryData": {
                        var jpViewer = new FLJasperViewer;
                        jpViewer.setReportData(q);
                        jpViewer.setReportTemplate(nombreReport);
                        jpViewer.exec();
                        break;
                }
                case "JasperXmlData": {
                  var xmlData = sys.toXmlReportData(q);
                  var regExp = new RegExp(" \\|\\| ' ' \\|\\| ");

                  regExp.global = true;
                  xmlData.setContent(xmlData.toString(0).replace(regExp,"_"));

      var jpViewer = new FLJasperViewer;
      jpViewer.setReportData(xmlData);
      jpViewer.setReportTemplate(nombreReport);
      jpViewer.exec();
                        break;
                }
                default: {
                        var rptViewer:FLReportViewer = new FLReportViewer();
                        rptViewer.setReportTemplate(nombreReport);
                        rptViewer.setReportData(q);
                        rptViewer.renderReport(etiquetaInicial.fila, etiquetaInicial.col);
                        if (numCopias)
                                rptViewer.setNumCopies(numCopias);
                        if (impresora) {
                                try {
                                        rptViewer.setPrinterName(impresora);
                                }
                                catch (e) {}
                        }
                        if (impDirecta) {
                                rptViewer.printReport();
                        } else if (pdf) {
                                //Si pdf es true, en el parámetro impresora está la ruta completa del fichero pdf
                                rptViewer.printReportToPDF(impresora);
                        } else {
                                this.iface.mostrarInformeVisor(rptViewer);
                        }
                }
        }
}

/** \D
Obtiene el operador lógico a aplicar en la cláusula where de la consulta a partir de los primeros caracteres del parámetro
@param        s: Nombre del campo que contiene un criterio de búsqueda
@return        Operador lógico a aplicar
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

/** \D
Obtiene el nombre del campo de la cadena s desde su segunda posición. Sustituye '_' por '.', dos '_" seguidos indica que realmente es '_"
@param        s: Nombre del campo que contiene un criterio de búsqueda
@return        Nombre procesado
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

/** \D Devuelve el valor del acumulado para el la variable indicada
@param        campo: Identificador del acumulado a devolver
*/
function oficial_obtenerAcumulado(nodo:FLDomNode, campo:String):String
{
        return this.iface.acumulados[campo];
}

/** \D Acumula el valor del registro actual del informe
@param        campo: String con dos valores separados por '/':
        1. Identificador del acumulado a devolver
        2. Nombre del campo de la consulta del informe cuyo valor hay que acumular
*/
function oficial_acumularValor(nodo:FLDomNode, campo:String):String
{
        var campos:Array = campo.split("/");
        var valor:Number = parseFloat(campos[1]);
        if (isNaN(valor))
                valor = parseFloat(nodo.attributeValue(campos[1]));

        if (!this.iface.acumulados[campos[0]]) {
                this.iface.acumulados[campos[0]] = valor;
                this.iface.cuentaAcum[campos[0]] = 1;
        } else {
                this.iface.acumulados[campos[0]] += valor;
                this.iface.cuentaAcum[campos[0]]++;
        }
        return "0";
}

/** \D Restaura la variable del acumulado
@param        campo: Identificador del acumulado a restaurar
*/
function oficial_restaurarAcumulado(nodo:FLDomNode, campo:String):String
{
        this.iface.acumulados[campo] = 0;
        this.iface.cuentaAcum[campo] = 0;

        return "0";
}

/** \D
Obtiene el xpm del logo de la empresa
@return xpm del logo
*/
function oficial_logo(nodo:FLDomNode, campo:String):String
{
        var util:FLUtil = new FLUtil;
        return util.sqlSelect("empresa", "logo", "1 = 1");
}

function oficial_porIVA(nodo:FLDomNode, campo:String):String
{
        var util:FLUtil = new FLUtil;
        var idDocumento:String;
        var tablaPadre:String;
        var tabla:String;
        var campoClave:String;
        var porIva:String;
        switch (campo) {
                case "facturacli": {
                        tablaPadre = "facturascli";
                        tabla = "lineasfacturascli";
                        campoClave = "idfactura";
                        break;
                }
                case "facturaprov": {
                        tablaPadre = "facturasprov";
                        tabla = "lineasfacturasprov";
                        campoClave = "idfactura";
                        break;
                }
        }
        idDocumento = nodo.attributeValue(tablaPadre + "." + campoClave);
        this.iface.variosIvas_ = false;
        porIva = parseFloat(util.sqlSelect(tabla, "iva", campoClave + " = " + idDocumento));
        if (!porIva)
                porIva = 0;

        if (util.sqlSelect(tabla, campoClave, campoClave + " = " + idDocumento + " AND iva <> " + porIva)) {
                this.iface.variosIvas_ = true;
                porIva = 0;
        }

        if (porIva.toString() == "0") {
                return "I.V.A.";
        } else {
                return "I.V.A. " + porIva.toString() + "%";
        }
}


function oficial_desgloseIva(nodo:FLDomNode, campo:String):String
{
        if (!this.iface.variosIvas_)
                return "";

        var util:FLUtil = new FLUtil;
        var idDocumento:String;
        var tabla:String;
        var campoClave:String;
        switch (campo) {
                case "facturacli": {
                        tablaPadre = "facturascli";
                        tabla = "lineasivafactcli";
                        campoClave = "idfactura";
                        break;
                }
                case "facturaprov": {
                        tablaPadre = "facturasprov";
                        tabla = "lineasivafactprov";
                        campoClave = "idfactura";
                        break;
                }
        }
        idDocumento = nodo.attributeValue(tablaPadre + "." + campoClave);

        var qryIvas:FLSqlQuery = new FLSqlQuery();
        with (qryIvas) {
                setTablesList(tabla);
                setSelect("totaliva");
                setFrom(tabla);
                setWhere(campoClave + " = " + idDocumento + " ORDER BY iva");
        }
        if (!qryIvas.exec())
                return false;
        var listaIvas:String = "";
        while (qryIvas.next()) {
                if (listaIvas != "")
                        listaIvas += "\n";
                listaIvas += util.roundFieldValue(qryIvas.value("totaliva"), tabla, "totaliva");
        }
        return listaIvas;
}

function oficial_desgloseBaseImponible(nodo:FLDomNode, campo:String):String
{
        if (!this.iface.variosIvas_)
                return "";

        var util:FLUtil = new FLUtil;
        var idDocumento:String;
        var tabla:String;
        var campoClave:String;
        switch (campo) {
                case "facturacli": {
                        tablaPadre = "facturascli";
                        tabla = "lineasivafactcli";
                        campoClave = "idfactura";
                        break;
                }
                case "facturaprov": {
                        tablaPadre = "facturasprov";
                        tabla = "lineasivafactprov";
                        campoClave = "idfactura";
                        break;
                }
        }
        idDocumento = nodo.attributeValue(tablaPadre + "." + campoClave);

        var qryIvas:FLSqlQuery = new FLSqlQuery();
        with (qryIvas) {
                setTablesList(tabla);
                setSelect("iva, neto");
                setFrom(tabla);
                setWhere(campoClave + " = " + idDocumento + " ORDER BY iva");
        }
        if (!qryIvas.exec())
                return false;
        var listaBases:String = "";
        while (qryIvas.next()) {
                if (listaBases != "")
                        listaBases += "\n";
                listaBases += "I.V.A. " + qryIvas.value("iva") + "%: " + util.roundFieldValue(qryIvas.value("neto"), tabla, "neto");
        }
        return listaBases;
}

function oficial_desgloseRecargo(nodo:FLDomNode, campo:String):String
{
        if (!this.iface.variosIvas_)
                return "";

        var util:FLUtil = new FLUtil;
        var idDocumento:String;
        var tabla:String;
        var campoClave:String;
        switch (campo) {
                case "facturacli": {
                        tablaPadre = "facturascli";
                        tabla = "lineasivafactcli";
                        campoClave = "idfactura";
                        break;
                }
                case "facturaprov": {
                        tablaPadre = "facturasprov";
                        tabla = "lineasivafactprov";
                        campoClave = "idfactura";
                        break;
                }
        }
        idDocumento = nodo.attributeValue(tablaPadre + "." + campoClave);

        var qryIvas:FLSqlQuery = new FLSqlQuery();
        with (qryIvas) {
                setTablesList(tabla);
                setSelect("totalrecargo");
                setFrom(tabla);
                setWhere(campoClave + " = " + idDocumento + " ORDER BY iva");
        }
        if (!qryIvas.exec())
                return false;
        var listaRecargo:String = "";
        while (qryIvas.next()) {
                if (listaRecargo != "")
                        listaRecargo += "\n";
                if (qryIvas.value("totalrecargo") == 0)
                        listaRecargo += " ";
                else
                        listaRecargo += util.roundFieldValue(qryIvas.value("totalrecargo"), tabla, "totalrecargo");
        }
        return listaRecargo;
}


function oficial_desgloseTotal(nodo:FLDomNode, campo:String):String
{
        if (!this.iface.variosIvas_)
                return "";

        var util:FLUtil = new FLUtil;
        var idDocumento:String;
        var tabla:String;
        var campoClave:String;
        switch (campo) {
                case "facturacli": {
                        tablaPadre = "facturascli";
                        tabla = "lineasivafactcli";
                        campoClave = "idfactura";
                        break;
                }
                case "facturaprov": {
                        tablaPadre = "facturasprov";
                        tabla = "lineasivafactprov";
                        campoClave = "idfactura";
                        break;
                }
        }
        idDocumento = nodo.attributeValue(tablaPadre + "." + campoClave);

        var qryIvas:FLSqlQuery = new FLSqlQuery();
        with (qryIvas) {
                setTablesList(tabla);
                setSelect("totallinea");
                setFrom(tabla);
                setWhere(campoClave + " = " + idDocumento + " ORDER BY iva");
        }
        if (!qryIvas.exec())
                return false;
        var listaTotal:String = "";
        while (qryIvas.next()) {
                if (listaTotal != "")
                        listaTotal += "\n";
                listaTotal += util.roundFieldValue(qryIvas.value("totallinea"), tabla, "totallinea");
        }
        return listaTotal;
}

/** \D
Función para campos calculados que obtiene los vencimientos de una factura de cliente
*/
function oficial_vencimiento(nodo:FLDomNode, campo:String):String
{
        var util:FLUtil = new FLUtil();
        if (!sys.isLoadedModule("flfactteso")) {
                var codPago:String;
                var fecha:String;
                if (campo == "reciboscli"){
                        codPago = nodo.attributeValue("facturascli.codpago");
                        fecha = nodo.attributeValue("facturascli.fecha");
                }
                else if (campo == "recibosprov"){
                        codPago = nodo.attributeValue("facturasprov.codpago");
                        fecha = nodo.attributeValue("facturasprov.fecha");
                }

                var qryDias:FLSqlQuery = new FLSqlQuery();
                var vencimientos:String = "";
                with(qryDias){
                        setTablesList("plazos");
                        setSelect("dias");
                        setFrom("plazos");
                        setWhere("codpago = '" + codPago + "' ORDER BY dias");
                }
                if (!qryDias.exec())
                        return "";

                while (qryDias.next()) {
                        if (vencimientos != "")
                                        vencimientos += ", ";
                        vencimientos += util.dateAMDtoDMA(util.addDays(fecha, qryDias.value(0)));
                }
                var res:String = this.iface.reemplazar(vencimientos, '-', '/')
                return res;
        }

        var tabla:String;
        var idFactura:FLDomNode;

        if (campo == "reciboscli"){
                tabla = "reciboscli";
                idFactura = nodo.attributeValue("facturascli.idfactura");
        }
        else if (campo == "recibosprov"){
                tabla = "recibosprov";
                idFactura = nodo.attributeValue("facturasprov.idfactura");
        }

        var qryRecibos:FLSqlQuery = new FLSqlQuery();
        var vencimientos:String = "";
        with (qryRecibos) {
                setTablesList(tabla);
                setSelect("fechav, importe");
                setFrom(tabla);
                setWhere("idfactura = '" + idFactura + "' ORDER BY fechav");
        }
        if (!qryRecibos.exec())
                return "";

        var fecha:String;
        while (qryRecibos.next()) {
                fecha = util.dateAMDtoDMA(qryRecibos.value(0));
                if (vencimientos != "")
                        vencimientos += "\n";
                vencimientos += this.iface.reemplazar(fecha.substring(0,10), '-', '/');
                vencimientos += ": " + util.formatoMiles(util.roundFieldValue(qryRecibos.value("importe"), "reciboscli", "importe"));
        }
        //var res:String = this.iface.reemplazar(vencimientos, '-', '/')
        //res = this.iface.reemplazar(res, '.', ',')
        return vencimientos;
}

/** \D
Función para campos calculados que obtiene el número de cuenta corriente de la factura.
En primer lugar se busca si la forma de pago es domiciliada o no.
Si lo es, se busca la cuenta de domiciliación del cliente.
Si no lo es o no se encuentra la del cliente, se busca una cuenta de la forma de pago
*/
function oficial_cuentaFacturaCli(nodo:FLDomNode, campo:String):String
{
        var util:FLUtil = new FLUtil;
        var datosCuenta:String;
        var ret:String;
        var codCliente:String = nodo.attributeValue("facturascli.codcliente");
        var codPago:String = nodo.attributeValue("facturascli.codpago");
        var domiciliado:Boolean = util.sqlSelect("formaspago", "domiciliado", "codpago = '" + codPago + "'");
        var codCuenta:String

        var tipoCuenta:String;

        // Si no hay cliente, se busca la forma de pago
        if (!codCliente)
                tipoCuenta = "formaPago";

        else
                if (domiciliado)
                        tipoCuenta = "domiciliado";
                else
                        tipoCuenta = "formaPago";


        if (tipoCuenta == "domiciliado") {
                codCuenta = util.sqlSelect("clientes", "codcuentadom", "codcliente = '" + codCliente + "'");
                if (codCuenta)
                        datosCuenta = flfactppal.iface.pub_ejecutarQry("cuentasbcocli", "ctaentidad,ctaagencia,cuenta", "codcuenta = '" + codCuenta + "'");
        }

        if (!codCuenta) {
                codCuenta = util.sqlSelect("formaspago", "codcuenta", "codpago = '" + codPago + "'");
                if (!codCuenta)
                        return "";
                datosCuenta = flfactppal.iface.pub_ejecutarQry("cuentasbanco", "ctaentidad,ctaagencia,cuenta", "codcuenta = '" + codCuenta + "'");
        }

        if (datosCuenta.result != 1)
                return "";
        var dc:String = util.calcularDC(datosCuenta.ctaentidad + datosCuenta.ctaagencia) + util.calcularDC(datosCuenta.cuenta);
        ret = datosCuenta.ctaentidad + " " + datosCuenta.ctaagencia + " " + dc + " " + datosCuenta.cuenta;
        return ret;





        // Si no hay cliente, se busca la forma de pago
        if (!codCliente) {
                codCuenta = util.sqlSelect("formaspago", "codcuenta", "codpago = '" + codPago + "'");
                if (!codCuenta)
                        return "";
                datosCuenta = flfactppal.iface.pub_ejecutarQry("cuentasbanco", "ctaentidad,ctaagencia,cuenta", "codcuenta = '" + codCuenta + "'");
        }

        else {

                if (domiciliado) {
                        codCuenta = util.sqlSelect("clientes", "codcuentadom", "codcliente = '" + codCliente + "'");
                        if (codCuenta)
                                datosCuenta = flfactppal.iface.pub_ejecutarQry("cuentasbcocli", "ctaentidad,ctaagencia,cuenta", "codcuenta = '" + codCuenta + "'");
                        else {
                                codCuenta = util.sqlSelect("formaspago", "codcuenta", "codpago = '" + codPago + "'");
                                if (!codCuenta)
                                        return "";
                                datosCuenta = flfactppal.iface.pub_ejecutarQry("cuentasbcocli", "ctaentidad,ctaagencia,cuenta", "codcuenta = '" + codCuenta + "'");
                        }
                }

                else {
                        codCuenta = util.sqlSelect("formaspago", "codcuenta", "codpago = '" + codPago + "'");
                        if (!codCuenta)
                                return "";
                        datosCuenta = flfactppal.iface.pub_ejecutarQry("cuentasbcocli", "ctaentidad,ctaagencia,cuenta", "codcuenta = '" + codCuenta + "'");
                }

        }







        var codCuenta:String = util.sqlSelect("clientes", "codcuentadom", "codcliente = '" + codCliente + "'");
        if (codCuenta) {
                datosCuenta = flfactppal.iface.pub_ejecutarQry("cuentasbcocli", "ctaentidad,ctaagencia,cuenta", "codcuenta = '" + codCuenta + "'");
        } else {
                codCuenta = util.sqlSelect("clientes", "codcuentarem", "codcliente = '" + codCliente + "'");
                if (!codCuenta)
                        codCuenta = util.sqlSelect("formaspago", "codcuenta", "codpago = '" + codPago + "'");
                if (!codCuenta)
                        return "";

                datosCuenta = flfactppal.iface.pub_ejecutarQry("cuentasbanco", "ctaentidad,ctaagencia,cuenta", "codcuenta = '" + codCuenta + "'");
        }
        if (datosCuenta.result != 1)
                        return "";
        var dc:String = util.calcularDC(datosCuenta.ctaentidad + datosCuenta.ctaagencia) + util.calcularDC(datosCuenta.cuenta);
        ret = datosCuenta.ctaentidad + " " + datosCuenta.ctaagencia + " " + dc + " " + datosCuenta.cuenta;
        return ret;
}



function oficial_valorIRPF(nodo:FLDomNode, campo:String):String
{
        var util:FLUtil = new FLUtil();
        debug(campo);

        var partesCampo:Array = campo.split(".");
        if (!partesCampo.length)
                return "";

        var tabla:String = partesCampo[0];
        var campoClave:String = partesCampo[1];

        var q:FLSqlQuery = new FLSqlQuery();
        with (q) {
                setTablesList("lineas" + tabla);
                setSelect("distinct irpf");
                setFrom("lineas" + tabla);
                setWhere(campoClave + " = " + nodo.attributeValue(campo));
        }
        if (!q.exec())
                return "";

        if (!q.size())
                return "";

        var valor:Number = nodo.attributeValue(tabla + ".totalirpf");
        valor = util.formatoMiles(util.buildNumber(valor, "f", 2));
        if (valor == "0,00")
                return valor;

        if (q.size() > 1)
                return valor;

        q.first();
        return q.value(0) + "%  " + valor;
}


/** Devuelve el número de página, usado en informes de detalle de
facturación para establecer números por documento, no por páginas totales
del informe
*/
function oficial_numPagina(nodo:FLDomNode, campo:String):String
{
        var codigo:String = nodo.attributeValue(campo);

        if (codigo != this.iface.ultIdDocPagina)
                this.iface.paginaActual = 1;
        else
                this.iface.paginaActual++;

        this.iface.ultIdDocPagina = codigo;
        return this.iface.paginaActual;
}



/** \D
Reemplaza en una cadena un carácter por otro
@param        cadena: Cadena a tratar
@param        patronOrigen: Caracter a reemplazar
@param        patronDestino: Caracter que sustituye al origen
@return        Cadena tratada
*/
function oficial_reemplazar(cadena:String, patronOrigen:String, patronDestino:String):String
{
        var res:String = "";
        if (cadena != "") {
                for (var i:Number = 0; i < cadena.length; i++) {
                        if (cadena.charAt(i) == patronOrigen)
                                res += patronDestino;
                        else
                                res += cadena.charAt(i);
                }
        }
        return res;
}

function oficial_ampliarWhere(nombreConsulta:String):String
{
        var where:String = "";

        switch (nombreConsulta)        {

                case "i_pedidosprov":
                case "i_albaranesprov":
                case "i_facturasprov":
                        where += "(dirproveedores.direccionppal = true OR dirproveedores.direccion IS NULL)";
                break;
        }

        return where;
}

/** \D
Formato de xmlDatos:
@param        xmlDatos: Xml con los datos necesarios para la generación del gráfico.
@return        Picture del gráfico creado
*/

// FORMATO DE xmlDatos:
//
//         <Grafico Tipo='2d_barras' Informe='1' Alto='' Ancho='' MargenDerecho='0' MargenInferior='0' MargenIzquierdo='0' MargenSuperior='0'>
//                 <EjeX Min='0' Max='' MarcarCada='1' MargenLabels = '30' MarcarLabels='0'/>
//                 <EjeY Min='0' Max='' MarcarCada='1' MargenLabels = '20' MarcarLabels='1'/>
//                 <Valores Color='220,220,220'>
//                         <Valor x='x1' y='y1' LabelX='Valor1' LabelY=''/>
//                         <Valor x='x2' y='y2' LabelX='Valor2' LabelY=''/>
//                         <Valor ...

//                 </Valores>
//         </Grafico>
function oficial_dibujarGrafico(xmlDatos:FLDomDocument):Picture
{
        var pic:Picture;
        var eGrafico:FLDomElement = xmlDatos.firstChild().toElement();
        var tipoGrafico:String = eGrafico.attribute("Tipo");
        switch (tipoGrafico) {
                case "2d_barras": {
                        pic = this.iface.dibujarGrafico2DBarras(xmlDatos);
                        break;
                }
                case "2d_mapaproves": {
                        pic = this.iface.dibujarGrafico2DMapaProvEs(xmlDatos);
                        break;
                }
                case "2d_mapapaiseseu": {
                        pic = this.iface.dibujarGrafico2DMapaPaisesEu(xmlDatos);
                        break;
                }
        }
        return pic;
}

function oficial_dameColor(color:String):Color
{
        var rgb:Array = new Array;
        if(!color || color == "") {
                rgb[0] = 220;
                rgb[1] = 220;
                rgb[2] = 220;
        }
        else {
                rgb = color.split(",");
        }

        var clr = new Color();
        clr.setRgb(rgb[0],rgb[1],rgb[2]);

        return clr;
}

function oficial_dameFuente(family:String, size:Number):Font
{
        var clf = new Font();
        if(!family || family == "") {
                family = "Arial";
        }
        if(!size || size == "") {
                size = 10;
        }

        clf.pointSize = size;
        clf.family = family;

        return clf;
}

function oficial_dibujarGrafico2DBarras(xmlDatos:FLDomDocument):Picture
{
debug("oficial_dibujarGrafico2DBarras");
        var pic:Picture = new Picture;
        var clr = new Color();
        var clf = new Font();
        pic.begin();

        var eGrafico:FLDomElement = xmlDatos.firstChild().toElement();

        var tipoGrafico:String = eGrafico.attribute("Tipo");
        var esInforme:String = eGrafico.attribute("Informe");
        var ancho:Number = parseInt(eGrafico.attribute("Ancho"));
        var alto:Number = parseInt(eGrafico.attribute("Alto"));

        var margenSuperior:Number = parseInt(eGrafico.attribute("MargenSuperior"));
        if (isNaN(margenSuperior)) { margenSuperior = 0;}
        var margenInferior:Number = parseInt(eGrafico.attribute("MargenInferior"));
        if (isNaN(margenInferior)) { margenInferior = 0;}
        var margenIzquierdo:Number = parseInt(eGrafico.attribute("MargenIzquierdo"));
        if (isNaN(margenIzquierdo)) { margenIzquierdo = 0;}
        var margenDerecho:Number = parseInt(eGrafico.attribute("MargenDerecho"));
        if (isNaN(margenDerecho)) { margenDerecho = 0;}

        var x:Array = [];
        var y:Array = [];

        var family:FLDomElement = eGrafico.attribute("FontFamily");
        var size:FLDomElement = eGrafico.attribute("FontSize");
        var clf = this.iface.dameFuente(family, size); // FUENTE DE LAS ETIQUETAS EN LOS EJES
        pic.setFont( clf );

        var eEjeX:FLDomElement = eGrafico.namedItem("EjeX").toElement();
        var minX:Number = parseFloat(eEjeX.attribute("Min"));
        if (isNaN(minX)) {
                minX = 0;
        }
        var maxX:Number = parseFloat(eEjeX.attribute("Max"));
        var margenLabelsX:Number = parseFloat(eEjeX.attribute("MargenLabels"));
        if (isNaN(margenLabelsX)) { margenLabelsX = 0;}
        var anguloLabelX:Number = parseFloat(eEjeX.attribute("AnguloLabel"));
        if (isNaN(anguloLabelX)) { anguloLabelX = 0;}

        var marcarLabelsX:Boolean = false;
        if (eEjeX.attribute("MarcarLabels") == "true" || eEjeX.attribute("MarcarLabels") == "1") {
                marcarLabelsX = true;
        }

        var eEjeY:FLDomElement = eGrafico.namedItem("EjeY").toElement();
        var minY:Number = parseFloat(eEjeY.attribute("Min"));
        if (isNaN(minY)) {
                minY = 0;
        }

        var maxY:Number = parseFloat(eEjeY.attribute("Max"));
        var margenLabelsY:Number = parseFloat(eEjeY.attribute("MargenLabels"));
        if (isNaN(margenLabelsY)) { margenLabelsY = 0;}

        var marcarLabelsY:Boolean = false;
        if (eEjeY.attribute("MarcarLabels") == "true" || eEjeY.attribute("MarcarLabels") == "1")
                marcarLabelsY = true;

        var factorX:Number = (ancho - margenIzquierdo - margenDerecho - margenLabelsY) / (maxX-minX);
        var offGraficoX:Number = margenIzquierdo + margenLabelsY;

        var factorY:Number = (alto - margenSuperior - margenInferior - margenLabelsX) / (maxY-minY);
        var offGraficoY:Number = margenSuperior;

        var fMaxX = ((maxX-minX) * factorX);
        var fMaxY = (maxY-minY) * factorY;

        clr.setRgb( 0, 0, 0 );
        pic.setPen( clr, 1); // pic.DotLine );

        pic.drawLine( offGraficoX, parseInt(offGraficoY) + parseInt(fMaxY), parseInt(offGraficoX) + parseInt(fMaxX), parseInt(offGraficoY) + parseInt(fMaxY));
        pic.drawLine( offGraficoX, parseInt(offGraficoY) + parseInt(fMaxY), offGraficoX, offGraficoY );

// PINTANDO EJE X
        var marcarCadaX:Number = parseFloat(eEjeX.attribute("MarcarCada"));
        if (!isNaN(marcarCadaX) && marcarCadaX > 0) {
                var fMarcarCadaX:Number = marcarCadaX * factorX;
                var fX:Number;
                for (var x:Number = minX; x <= maxX; x += marcarCadaX) {
                        fX = (x * factorX);
                        fX = fX - (minX * factorX);
                        pic.drawLine( parseInt(offGraficoX) + parseInt(fX), parseInt(offGraficoY) + parseInt(fMaxY), parseInt(offGraficoX) + parseInt(fX), parseInt(offGraficoY) + parseInt(fMaxY) + 5);
                        if (marcarLabelsX) {
                                pic.drawText(parseInt(offGraficoX) + parseInt(fX), parseFloat(fMaxY) + parseFloat(margenLabelsX), parseInt(x).toString());
                        }
                }
        }

// PINTANDO EJE Y
        var marcarCadaY:Number = parseFloat(eEjeY.attribute("MarcarCada"));
        var colorLineaMarcaY:String = eEjeY.attribute("ColorLineaMarca");
        var estiloLineaMarcaY:Number = parseInt(eEjeY.attribute("EstiloLineaMarca"));
        if (!estiloLineaMarcaY || isNaN(estiloLineaMarcaY)) {
                estiloLineaMarcaY = 1;
        }
        var clrLineaMarcaY:Color;
        if (colorLineaMarcaY && colorLineaMarcaY != "") {
                clrLineaMarcaY = this.iface.dameColor(colorLineaMarcaY);
        } else {
                clrLineaMarcaY = false;
        }
        if (!isNaN(marcarCadaY) && marcarCadaY > 0) {
                var fMarcarCadaY:Number = marcarCadaY * factorY;
                var fY:Number;
                var totalMarcas:Number = Math.ceil((maxY - minY) / marcarCadaY);
                for (var y:Number = minY; y < (maxY+marcarCadaY); y += marcarCadaY) {
                        fY = y * factorY-1;
                        fY = parseFloat(fMaxY) - fY + (minY * factorY);
                        pic.drawLine( parseInt(offGraficoX),parseInt(offGraficoY) + parseInt(fY), parseInt(offGraficoX)-5, parseInt(offGraficoY) + parseInt(fY));
                        if (clrLineaMarcaY && y > minY) {
                                pic.setPen(clrLineaMarcaY, 1, estiloLineaMarcaY);
                                pic.drawLine( parseInt(offGraficoX), parseInt(offGraficoY) + parseInt(fY), parseInt(offGraficoX) + parseInt(fMaxX), parseInt(offGraficoY) + parseInt(fY));
                                pic.setPen(clr, 1, 1);
                        }
                        if (marcarLabelsY) {
                                pic.drawText(parseInt(margenIzquierdo),parseInt(offGraficoY) + parseInt(fY),parseInt(y).toString());
                        }
                }
        }

// PINTAR BARRAS
        var valores:FLDomElement = eGrafico.namedItem("Valores").toElement();

        var separacion:Number = factorX*5/100 // SEPARACION ENTRE BARRAS
        var colorBarras:String = valores.attribute("Color");
        var clrBarras = this.iface.dameColor(colorBarras); // COLOR BARRAS
        var nodos:FLDomNodeList = valores.toElement().elementsByTagName("Valor");
        var valor:FLDomElement;
        for(var i:Number = 0; i < nodos.length(); i++) {
                valor = nodos.item(i).toElement();
                var x:Number = (parseFloat(offGraficoX) + (parseFloat(valor.attribute("X")) * parseFloat(factorX)) + 1) - (minX * factorX);
                var anchoRect:Number = (factorX-separacion);
                var y:String = ((parseFloat(fMaxY) - (parseFloat(valor.attribute("Y")) * parseFloat(factorY))) + parseFloat(offGraficoY)) + (minY * factorY);
                var labelX:String = valor.attribute("LabelX");
                var labelY:String = valor.attribute("LabelY");
                var altoRect:Number = (parseFloat(valor.attribute("Y")) * parseFloat(factorY));
                pic.fillRect(x, y, anchoRect, altoRect, clrBarras);

                if (labelX && labelX != "") {
debug("Rotando1 " + parseInt(x).toString());
                        if (anguloLabelX != 0) {
//                                 pic.savePainter();
//                                 pic.translate(x - (factorX / 2) - margenLabelsX, parseFloat(fMaxY) + parseFloat(margenLabelsX));
//                                 pic.rotate(anguloLabelX * -1);
//                                 var r = new Rect(0, 0, margenLabelsX, margenLabelsX);
//                                 var maxLetras:Number = 10;
//                                 pic.drawText(r, 0, labelX, maxLetras);
//                                 pic.restorePainter();
//                                 pic.drawLine((x + (factorX / 2)), parseFloat(fMaxY) + parseFloat(offGraficoY), (x + (factorX / 2) - margenLabelsX), parseFloat(fMaxY) + parseFloat(offGraficoY) + parseFloat(margenLabelsX));
                                pic.savePainter();
                                pic.translate(x + factorX, parseFloat(fMaxY) + parseFloat(offGraficoY));
                                pic.rotate(anguloLabelX);
                                var r = new Rect(0, 0, -margenLabelsX, margenLabelsX);
                                var maxLetras:Number = 10;
//                                 pic.drawText(r, 0, labelX, maxLetras);
                                pic.drawText((-1 * margenLabelsX), 0, labelX, maxLetras);
                                pic.drawLine(0, 0, -margenLabelsX, 0)
                                pic.restorePainter();
                        } else {
                                pic.drawText(x, parseFloat(fMaxY) + parseFloat(margenLabelsX), labelX);
                        }
                }

                if(labelY && labelY != "") {
                        pic.drawText(parseInt(margenIzquierdo), y, labelY);
                }
        }

        //pic.save("/home/lorena/picture.svg","svg");
        return pic;
}

function oficial_dibujarGrafico2DMapaProvEs(xmlDatos:FLDomDocument):Picture
{
        var util:FLUtil = new FLUtil;
        var eGrafico:FLDomElement = xmlDatos.firstChild().toElement();

        var mapa = new Picture();
        var pic = new Picture();
        var clr = new Color();
        var clrValor = new Color();

        pic.begin();

//         var contenido:String = util.sqlSelect("i_ficheros", "contenido", "nombre = 'i_provincias_es.svg'");
//         if (!contenido) {
//                 MessageBox.warning(util.translate("scripts", "No tiene cargado el fichero i_provincias_es.svg.\nEste fichero es necesario para representar el gráfico de provincias."), MessageBox.Ok, MessageBox.NoButton);
//                 return false;
//         }
//         File.write("i_provincias_es.svg", contenido);
//         mapa.load( "i_provincias_es.svg", "svg" );
//         mapa.load( "/home/arodriguez/tmp/maceflor/MapaProvincias4.svg", "svg" );

        var provincias:Array = [];
// [x,396-y]
        /* ALAVA*/ provincias["01"] = [210, 43];
        /*ALBACETE*/ provincias["02"] = [230, 230];
        /*ALICANTE*/ provincias["03"] = [290, 250];
        /*ALMERIA*/ provincias["04"] = [225, 315];
        /*ASTURIAS*/ provincias["33"] = [91, 21];
        /*AVILA*/ provincias["05"] = [125, 151];
        /*BADAJOZ*/ provincias["06"] = [78, 240];
        /*BALEARES*/ provincias["07"] = [415, 218];
        /*BARCELONA*/ provincias["08"] = [380, 100];
        /*BURGOS*/ provincias["09"] = [170, 71];
        /*CACERES*/ provincias["10"] = [75, 187];
        /*CADIZ*/ provincias["11"] = [85, 340];
        /*CANTABRIA*/ provincias["39"] = [150, 27];
        /*CASTELLON*/ provincias["12"] = [314,165];
        /*CIUDAD REAL*/ provincias["13"] = [153, 227];
        /*CORDOBA*/ provincias["14"] = [121, 264];
        /*LA CORUÑA*/ provincias["15"] = [0, 10];
        /*CUENCA*/ provincias["16"] = [224, 181];
        /*GERONA*/ provincias["17"] = [405, 64];
        /*GRANADA*/ provincias["18"] = [177, 304];
        /*GUADALAJARA*/ provincias["19"] = [210, 137];
        /*GUIPUZCOA*/ provincias["20"] = [250, 20];
        /*HUELVA*/ provincias["21"] = [45, 280];
        /*HUESCA*/ provincias["22"] = [295, 75];
        /*JAEN*/ provincias["23"] = [180, 266];
        /*LEON*/ provincias["24"] = [83, 54];
        /*LERIDA*/ provincias["25"] = [343, 75];
        /*LUGO*/ provincias["27"] = [45, 33];
        /*MADRID*/ provincias["28"] = [165, 153];
        /*MALAGA*/ provincias["29"] = [137, 330];
        /*MURCIA*/ provincias["30"] = [255, 278];
        /*NAVARRA*/ provincias["31"] = [250, 52];
        /*ORENSE*/ provincias["32"] = [32, 85];
        /*PALENCIA*/ provincias["34"] = [125, 55];
        /*LAS PALMAS*/ provincias["35"] = [400, 350];
        /*PONTEVEDRA*/ provincias["36"] = [0, 60];
        /*LA RIOJA*/ provincias["26"] = [217, 78];
        /*SALAMANCA*/ provincias["37"] = [76, 133];
        /*SANTA CRUZ*/ provincias["38"] = [300, 325];
        /*SEGOVIA*/ provincias["40"] = [161, 125];
        /*SEVILLA*/ provincias["41"] = [95, 296];
        /*SORIA*/ provincias["42"] = [212, 105];
        /*TARRAGONA*/ provincias["43"] = [335, 130];
        /*TERUEL*/ provincias["44"] = [268, 150];
        /*TOLEDO*/ provincias["45"] = [150, 185];
        /*VALENCIA*/ provincias["46"] = [290, 205];
        /*VALLADOLID*/ provincias["47"] = [130, 100];
        /*VIZCAYA*/ provincias["48"] = [205, 11];
        /*ZAMORA*/ provincias["49"] = [85, 95];
        /*ZARAGOZA*/ provincias["50"] = [253, 104];


// debug(File.read("/home/arodriguez/dib.svg"));
//         pic.setWindow( devRect );
//         pic.setViewport( devRect );
        pic.drawPicture( mapa );

        var family:String = eGrafico.attribute("FontFamily");
        if (!family || family == "") {
                family = "Arial";
        }
        var size:String = eGrafico.attribute("FontSize");
        if (!size || size == "") {
                size = "7";
        }
        var sizeValor:String = eGrafico.attribute("FontSizeValor");
        if (!sizeValor || sizeValor == "") {
                sizeValor = "10";
        }

        var formatValor:String = eGrafico.attribute("Format");
        if (!formatValor || formatValor == "") {
                formatValor = "KM";
        }

        var clf = this.iface.dameFuente(family, size); // FUENTE DE LAS ETIQUETAS EN LOS EJES
        var clfValor = this.iface.dameFuente(family, sizeValor); // FUENTE DE LAS ETIQUETAS EN LOS EJES

        var valores:FLDomElement = eGrafico.namedItem("Valores").toElement();
        var eValor:FLDomElement;
        var idProvincia:String;
        var codProvincia:String;
        var provincia:String;
        clr.setRgb( 100, 100, 100 );
        clrValor.setRgb( 0, 0, 255 );

        var valor:String = "";
        var aProvincia:Array = [];
        for (var nodoValor:FLDomNode = valores.firstChild(); nodoValor; nodoValor = nodoValor.nextSibling()) {
                eValor = nodoValor.toElement();
                valor = eValor.attribute("Valor");
                valor = this.iface.formatearValor(valor,formatValor);
                codProvincia = util.sqlSelect("provincias", "codigo", "idprovincia = " + eValor.attribute("Prov"));
                if (!codProvincia) {
                        continue;
                }
                provincia = util.sqlSelect("provincias", "provincia", "idprovincia = " + eValor.attribute("Prov"));
                pic.setFont( clf );
                pic.setPen( clr, 1);
                try {
                        aProvincia = provincias[codProvincia];
                } catch (e) {
                        continue;
                }
                pic.drawText(aProvincia[0], aProvincia[1], provincia);
                pic.setFont( clfValor );
                pic.setPen( clrValor, 1);
                pic.drawText(aProvincia[0], aProvincia[1] + (parseInt(size) * 2), valor);
        }

        return pic;
}

function oficial_dibujarGrafico2DMapaPaisesEu(xmlDatos:FLDomDocument):Picture
{
debug("oficial_dibujarGrafico2DMapaPaisesEu");
        var util:FLUtil = new FLUtil;
        var eGrafico:FLDomElement = xmlDatos.firstChild().toElement();

        var mapa = new Picture();
        var pic = new Picture();
        var clr = new Color();
        var clrValor = new Color();

        pic.begin();

//         var contenido:String = util.sqlSelect("i_ficheros", "contenido", "nombre = 'i_paises_eu.svg'");
//         if (!contenido) {
//                 MessageBox.warning(util.translate("scripts", "No tiene cargado el fichero i_paises_eu.svg.\nEste fichero es necesario para representar el gráfico de paises."), MessageBox.Ok, MessageBox.NoButton);
//                 return false;
//         }
// debug("oficial_dibujarGrafico2DMapaPaisesEu2");
//         File.write("i_paises_eu.svg", contenido);
// debug("oficial_dibujarGrafico2DMapaPaisesEu3");
//         mapa.load( "i_provincias_es.svg", "svg" );
// debug("oficial_dibujarGrafico2DMapaPaisesEu4");

        var paises:Array = [];
        /* ESPAÑA */ paises["ES"] = [65, 348];
        /* FRANCIA */ paises["FR"] = [125, 265];
        /* ITALIA */ paises["IT"] = [225, 338];
        /* GRECIA */ paises["GR"] = [331, 359];
        /* PORTUGAL */ paises["PT"] = [8, 320];
        /* REINO UNIDO */ paises["GB"] = [70, 117];
        /* IRLANDA */ paises["IE"] = [47, 160];
        /* SUIZA */ paises["CH"] = [182, 261];
        /* BÉLGICA */ paises["BE"] = [150, 210];
        /* LUXEMBURGO */ paises["LU"] = [152, 235];
        /* PAISES BAJOS */ paises["NL"] = [155, 180];
        /* ALEMANIA */ paises["DE"] = [196, 203];
        /* ISLANDIA */ paises["IS"] = [40, 25];
        /* NORUEGA */ paises["NO"] = [183, 69];
        /* SUECIA */ paises["SE"] = [236, 86];
        /* FINLANDIA */ paises["FI"] = [290, 43];
        /* DINAMARCA */ paises["DK"] = [182, 137];
        /* ESTONIA */ paises["EE"] = [299, 90];
        /* LETONIA */ paises["LV"] = [302, 115];
        /* LITUANIA */ paises["LT"] = [289, 136];
        /* RUSIA */ paises["RU"] = [405, 103];
        /* AUSTRIA */ paises["AT"] = [237, 240];
        /* REP. CHECA */ paises["CZ"] = [234, 215];
        /* POLONIA */ paises["PL"] = [270, 185];
        /* POLONIA */ paises["PL"] = [270, 185];
        /* CROACIA */ paises["HR"] = [267, 275];
        /* BOSNIA-HERZEGOVINA */ paises["BA"] = [272, 301];
        /* ESLOVENIA */ paises["SI"] = [225, 270];
        /* ALBANIA */ paises["AL"] = [286, 328];
        /* MACEDONIA */ paises["MK"] = [321, 323];
        /* BULGARIA */ paises["BG"] = [346, 300];
        /* SERBIA */ paises["CS"] = [311, 290];
        /* TURQUÍA */ paises["TR"] = [412, 333];
        /* UCRANIA */ paises["UA"] = [342, 200];
        /* MOLDAVIA */ paises["MD"] = [365, 235];
        /* HUNGRÍA */ paises["HU"] = [279, 252];
        /* ESLOVAQUIA */ paises["SK"] = [283, 225];
        /* BIELORUSIA */ paises["BY"] = [333, 155];
        /* RUMANÍA */ paises["RO"] = [333, 265];
        /* ANDORRA */ paises["AD"] = [118, 311];




        pic.drawPicture( mapa );
debug("oficial_dibujarGrafico2DMapaPaisesEu4");
        var family:String = eGrafico.attribute("FontFamily");
        if (!family || family == "") {
                family = "Arial";
        }
        var size:String = eGrafico.attribute("FontSize");
        if (!size || size == "") {
                size = "7";
        }
        var sizeValor:String = eGrafico.attribute("FontSizeValor");
        if (!sizeValor || sizeValor == "") {
                sizeValor = "10";
        }

        var formatValor:String = eGrafico.attribute("Format");
        if (!formatValor || formatValor == "") {
                formatValor = "KM";
        }

        var clf = this.iface.dameFuente(family, size); // FUENTE DE LAS ETIQUETAS EN LOS EJES
        var clfValor = this.iface.dameFuente(family, sizeValor); // FUENTE DE LAS ETIQUETAS EN LOS EJES

        var valores:FLDomElement = eGrafico.namedItem("Valores").toElement();
        var eValor:FLDomElement;
        var idPais:String;
        var codPais:String;
        var pais:String;
        clr.setRgb( 100, 100, 100 );
        clrValor.setRgb( 0, 0, 255 );

        var valor:String = "";
        var aPais:Array = [];
debug("oficial_dibujarGrafico2DMapaPaisesEu5");
        for (var nodoValor:FLDomNode = valores.firstChild(); nodoValor; nodoValor = nodoValor.nextSibling()) {
debug("oficial_dibujarGrafico2DMapaPaisesEu4 " + eValor.attribute("Pais"));
                eValor = nodoValor.toElement();
                valor = eValor.attribute("Valor");
                valor = this.iface.formatearValor(valor,formatValor);
                codPais = util.sqlSelect("paises", "codiso", "codpais = '" + eValor.attribute("Pais") + "'");
                if (!codPais) {
                        continue;
                }
                pais = util.sqlSelect("paises", "nombre", "codpais = '" + eValor.attribute("Pais") + "'");
                pic.setFont( clf );
                pic.setPen( clr, 1);
                try {
                        aPais = paises[codPais];
                } catch (e) {
                        continue;
                }
                pic.drawText(aPais[0], aPais[1], pais);
                pic.setFont( clfValor );
                pic.setPen( clrValor, 1);
                pic.drawText(aPais[0], aPais[1] + (parseInt(size) * 2), valor);
        }

        return pic;
}

function oficial_formatearValor(valor:String,formatValor:String):String
{
        if(!valor || valor == "")
                return;

        var result:String = valor;

        var numero:Number = parseFloat(valor);
        var n:Number;
        switch(formatValor) {
                case "KM": {
                        if(numero >= 1000000) {
                                n = numero / 1000000;
                                result = n.toString().split(".")[0] + "." + n.toString().split(".")[1].left(1) + "M";
                                break
                        }
                        if(numero >= 1000) {
                                n = numero / 1000;
                                result = n.toString().split(".")[0] + "K";
                                break;
                        }

                        if(numero < 1000) {
                                n = numero / 1000;
                                result = n.toString().split(".")[0] + "." + n.toString().split(".")[1].left(1) + "K";
                                break
                        }
                        break;
                }
                default: {
                        break;
                }
        }

        return result;
}

function oficial_mostrarInformeVisor(visor:FLReportViewer):Boolean
{
        this.iface.visor_ = visor;
        this.iface.visor_.exec();
}
//// OFICIAL /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition jasperPlugin */
//////////////////////////////////////////////////////////////////
//// JASPER_PLUGIN ///////////////////////////////////////////////

function jasperPlugin_lanzarInforme(cursor:FLSqlCursor, nombreInforme:String, orderBy:String, groupBy:String, etiquetas:Boolean, impDirecta:Boolean, whereFijo:String, nombreReport:String, numCopias:Number, impresora:String, pdf:Boolean)
    {
            var util:FLUtil = new FLUtil();
            var etiquetaInicial:Array = [];

  	    //Comprobamos si whereFijo contiene parametrosJasper.
          	  //Contamos \n

                             	var cadena1:String = "";
                             	var cadena2:String;
                             	if (!whereFijo || whereFijo == "")
                             	{
                             	cadena2 = "";
                             	debug("JASPER_PLUGIN :: WhereFijo está vacío");
                             	}
                             	else cadena2 = whereFijo;
                             	var cantidadParametrosJasper:Number = -1;
                             	var parametrosJasper:String = ""; // Aquí guardamos la lista de parametros a pasar a la librería.
                             	do
                             	  {
                             	  cadena1 = cadena2;
                             	  cantidadParametrosJasper++;
                             	  cadena2 = cadena2.replace("\n","");
                             	  } while (cadena1 != cadena2);
                             	 if (cantidadParametrosJasper > 0)
                             	 			{
                             	 			debug("JASPER_PLUGIN :: Se han encontrado varios saltos de linea (PARAMETROS) en whereFijo");
		            				parametrosJasper = whereFijo;
		            				//Se procede a sacar whereFijo si existe
		            				if ( whereFijo.lastIndexOf("WHEREFIJO\n") == -1)
		            					{
		            					debug("JASPER_PLUGIN :: Entre los PARAMETROS no se encuentra WHEREFIFO");
		            					whereFijo = ""; //ponemos whereFijo vacio
		            					}
		            					else
		            						{
		            						whereFijo = whereFijo.right(whereFijo.length - (whereFijo.lastIndexOf("WHEREFIJO") + 10));
		            						whereFijo = whereFijo.mid(0,whereFijo.indexOf("\n"));
		            						if (whereFijo != "")
		            						debug("JASPER_PLUGIN :: WHEREFIJO = " + whereFijo);
		            						else
		            						debug("JASPER_PLUGIN :: WHEREFIJO existe, pero está vacío");
		            						}
		            				} else debug("JASPER_PLUGIN :: whereFijo NO contiene saltos de linea(PARAMETROS)");






            if (etiquetas == true) {
                    etiquetaInicial = this.iface.seleccionEtiquetaInicial();
            } else {
                    etiquetaInicial["fila"] = 0;
                    etiquetaInicial["col"] = 0;
            }

            this.iface.ultIdDocPagina = "";
            var q:FLSqlQuery;
            if(nombreInforme != "version")
                    {

            q = this.iface.establecerConsulta(cursor, nombreInforme, orderBy, groupBy, whereFijo);
    //debug("------ CONSULTA -------" + q.sql());
    	  if (util.sqlSelect("flfiles", "nombre", "nombre = '" + nombreInforme + ".qry'"))
    	  	{
                 if (q.exec() == false) {
                    MessageBox.critical(util.translate("scripts", "Falló la consulta"), MessageBox.Ok, MessageBox.NoButton);
                    return;
                 } else {
                         if (q.first() == false) {
                         MessageBox.warning(util.translate("scripts", "No hay registros que cumplan los criterios de búsqueda establecidos"), MessageBox.Ok, MessageBox.NoButton);
                         return;
                    				}
            		}
               }
                 }
            var tipoReport:String = "";
            if (!nombreReport || nombreReport == "") {
                    nombreReport = nombreInforme;
            } else {
                    var extension:String;
                    var iPunto:Number = nombreReport.findRev(".");
                    if (iPunto > -1) {
                            extension = nombreReport.right(nombreReport.length - (iPunto + 1));
                            nombreReport = nombreReport.left(iPunto);
                            if (extension.toLowerCase() == "jxml") {
                                    tipoReport = "JasperQueryData";
                            } else if (extension.toLowerCase() == "jdxml") {
                                    tipoReport = "JasperXmlData";
                            }
                    }
                    //debug("extension = '" + extension + "'");
                    debug("JASPER_PLUGIN :: nombreReport = '" + nombreReport + "'");
                    debug("JASPER_PLUGIN :: nombreInforme = '" + nombreInforme + "'");
                    //debug("tipoReport = '" + tipoReport + "'");
            }


            switch (tipoReport) {
                    case "JasperQueryData": {
                            var jpViewer = new FLJasperViewer;
                            jpViewer.setReportData(q);
                            jpViewer.setReportTemplate(nombreReport);
                            jpViewer.exec();
                            break;
                    }
                    case "JasperXmlData": {
                      var xmlData = sys.toXmlReportData(q);
                      var regExp = new RegExp(" \\|\\| ' ' \\|\\| ");

                      regExp.global = true;
                      xmlData.setContent(xmlData.toString(0).replace(regExp,"_"));

          var jpViewer = new FLJasperViewer;
          jpViewer.setReportData(xmlData);
          jpViewer.setReportTemplate(nombreReport);
          jpViewer.exec();
                            break;
                    }
                    default: {

                    	//Cargamos configuración plugin
                        this.iface.rutaReports =  util.readSettingEntry("jasperplugin/reportspath");
                        this.iface.guardaTemporal = util.readSettingEntry("jasperplugin/guardatemporal");
                        this.iface.dbName = util.readSettingEntry("DBA/lastDB");
                        this.iface.detectarRutaTrabajo = util.readSettingEntry("jasperplugin/detecRT");
                        this.iface.barra = this.iface.seteaBarra(); //Barra de separacion.
                        //Generamos ruta a directorio de reports
                        var fullPath:String  = this.iface.rutaReports + this.iface.dbName + this.iface.barra + "reports" + this.iface.barra + nombreInforme + this.iface.barra;
                        var fullPathReport:String = fullPath + nombreReport + ".jrxml";
                        //Si existe un report en ruta " path / dbName / reports / nombre_informe / nombre_report.jrxml " o pregunto por versión
                        if (this.iface.comprobarJasperFisico(fullPathReport) || nombreInforme == "version")
                                     {
                                  debug ("JASPER_PLUGIN :: Report encontrado");
                                  debug ("JASPER_PLUGIN :: Procesando plantilla " + fullPathReport);




                        	 if (cantidadParametrosJasper % 2 == 0)
	                             	 		cantidadParametrosJasper = cantidadParametrosJasper / 2 ; //Sacamos parejas en limpio
 								 else
                             						{
                             						debug ("JASPER_PLUGIN :: ERROR :: PARAMETRO - VALOR impares. Se pasan solo los Automáticos");
                             						cantidadParametrosJasper = 0;
                             						parametrosJasper="";
                             						}
				//comprobamos orderBy y groupBy !undefined
				if (!orderBy) orderBy="";
				if (!groupBy) groupBy="";

                               	//Ahora añadimos parametros especiales a parametrosJasper (where,orderby,groupby) y añadimos 6 saltos de linea a cantidadParametrosJasper


                               	if ( parametrosJasper.lastIndexOf("WHERE\n") == -1)
                               					{
                               					parametrosJasper = "WHERE\n" + this.iface.whereCursor+"\n" + parametrosJasper;
                               					cantidadParametrosJasper++;
                               					} else debug("JASPER_PLUGIN :: PELIGRO :: El parámetro WHERE no es el automático");
                             	if ( parametrosJasper.lastIndexOf("ORDERBY\n") == -1)
                             					{
                             					parametrosJasper = "ORDERBY\n" + orderBy+"\n" + parametrosJasper;
                             					cantidadParametrosJasper++;
                             					} else debug("JASPER_PLUGIN :: PELIGRO :: El parámetro ORDERBY no es el automático");
                            	if ( parametrosJasper.lastIndexOf("GROUPBY\n") == -1)
                            					{
                            					parametrosJasper = "GROUPBY\n" + groupBy+"\n" + parametrosJasper;
                            					cantidadParametrosJasper++;
                            					} else debug("JASPER_PLUGIN :: PELIGRO :: El parámetro GROUPBY no es el automático");

                            	if (etiquetas == true) //Si son etiquetas.
                            		{
                            	if ( parametrosJasper.lastIndexOf("ETIQUETAFILA\n") == -1)
                            					{
                            					parametrosJasper = "ETIQUETAFILA\n" + etiquetaInicial["fila"] +"\n" + parametrosJasper;
                            					cantidadParametrosJasper++;
                            					} else debug("JASPER_PLUGIN :: PELIGRO :: El parámetro ETIQUETAFILA no es el automático");
                            	if ( parametrosJasper.lastIndexOf("ETIQUETACOLUMNA\n") == -1)
                            					{
                            					parametrosJasper = "ETIQUETACOLUMNA\n" + etiquetaInicial["col"] +"\n" + parametrosJasper;
                            					cantidadParametrosJasper++;
                            					} else debug("JASPER_PLUGIN :: PELIGRO :: El parámetro ETIQUETACOLUMNA no es el automático");
                            		}


                                var stdin:String; //Cadena que se envia a la librería
                                var ficheroTemporal;

                        if (this.iface.procesoInicializado)
                             if (!this.iface.procesoJP.running)
                          		this.iface.reportAnterior ="";


                          if(nombreInforme == "version")
                          {
                          ficheroTemporal = "version";
                          this.iface.reportAnterior ="";
                          }
                          			    else ficheroTemporal = this.iface.tratarReport(nombreInforme, nombreReport);
				    if (!ficheroTemporal)
							{
							debug("JASPER_PLUGIN :: ERROR :: El report " + nombreReport + " no es una plantilla válida.");
							this.iface.reportAnterior="";
							return;
							}
                                    debug("JASPER_PLUGIN :: Usando fichero temporal " + ficheroTemporal);
                                    stdin = ficheroTemporal + "\n";
                                    stdin += this.iface.guardaTemporal + "\n"; //Valor guardaTemporal para borrar o no temporales


                                    if (pdf) stdin += "true\n";
                                    	else
                                 	     stdin += "false\n";


                             	    if (numCopias) stdin += numCopias + "\n";
                                 	 else
                                 	     stdin += "1\n";


                             	    if (impresora) stdin += impresora+"\n";
                                 	else
                                	      stdin += "false\n";


                                    if (impDirecta) stdin += "true\n";
                                    	else
                                 	     stdin += "false\n";


                                    stdin+= cantidadParametrosJasper + "\n";
                                    stdin += parametrosJasper;






                             //Seteamos directorio del report a usar.
                             var rutaTrabajo:String;
                             if (nombreReport =="version") rutaTrabajo = this.iface.rutaReports //Si marco el reporte "version" seteo el path principal de reports, pues reporte version no existe.
                             		else rutaTrabajo = this.iface.rutaReports + this.iface.dbName + this.iface.barra + "reports" + this.iface.barra + nombreInforme+ this.iface.barra;

                             debug("JASPER_PLUGIN :: Ruta de trabajo con fichero temporal = " + rutaTrabajo);
                             debug ("JASPER_PLUGIN :: GuardaTemporal " + this.iface.guardaTemporal);

                             //Si la libreria no se ha ejecutado antes

                             if (!this.iface.procesoInicializado)
                                        {
                                      debug("JASPER_PLUGIN :: Inicializando la librería ");
                                         var rutaPlugin= util.readSettingEntry("jasperplugin/pluginpath");
                                         if (rutaPlugin == "")
                                                                 {
                                                                  MessageBox.critical("JASPER_PLUGIN ERROR \n No se ha especificado el path de JasperPlugin", MessageBox.Ok);
                                                                  break;
                                                                 }
                                       this.iface.generarComando(rutaPlugin);
                                       debug("JASPER_PLUGIN :: Ruta de trabajo actual ("+rutaTrabajo+")");
                                       this.iface.rutaTrabajoVieja = rutaTrabajo;
                                       this.iface.procesoInicializado = true;


                                           }
                             //Miramos si el cambio de directorio está activo
                            var detectRT = this.iface.detectarRutaTrabajo;
                            if (detectRT == "true")
                                                {
                                                debug("JASPER_PLUGIN :: Detectar RT activado");
                                                if (rutaTrabajo != this.iface.rutaTrabajoVieja)
                                                                            {
                                                                            this.iface.procesoJP.kill(); //Si cambiamos de carpeta de trabajo , paramos el proceso.
                                                                           debug ("JASPER_PLUGIN :: ( KILL/START ) CAMBIO DE RUTA. La ruta no era la misma");
                                                                           this.iface.rutaTrabajoVieja = rutaTrabajo;
                                                                           this.iface.procesoJP.workingDirectory = rutaTrabajo;
                                                                           debug ("JASPER_PLUGIN :: Ruta cambiada.");
                                                                            this.iface.procesoJP.start();
                                                                            }
                                               }

                                         if (!this.iface.procesoJP.running)
                                                                     {
                                                                    debug ("JASPER_PLUGIN :: START");
                                                                    this.iface.procesoJP.workingDirectory = rutaTrabajo;
                                                                     this.iface.procesoJP.start();

                                                                     }

                                        this.iface.procesoJP.writeToStdin(stdin);
                                      	debug("JASPER_PLUGIN :: Enviando por stdin : \n\n" + stdin);






                                     }
                              else
                                {
                            var rptViewer:FLReportViewer = new FLReportViewer();
                            rptViewer.setReportTemplate(nombreReport);
                            rptViewer.setReportData(q);
                            rptViewer.renderReport(etiquetaInicial.fila, etiquetaInicial.col);
                            if (numCopias)
                                    rptViewer.setNumCopies(numCopias);
                            if (impresora) {
                                    try {
                                            rptViewer.setPrinterName(impresora);
                                    }
                                    catch (e) {}
                            }
                            if (impDirecta) {
                                    rptViewer.printReport();
                            } else if (pdf) {
                                    //Si pdf es true, en el parámetro impresora está la ruta completa del fichero pdf
                                    rptViewer.printReportToPDF(impresora);
                            } else {
                                    this.iface.mostrarInformeVisor(rptViewer);
                            }
                      }
                    }
            }
    }

/** Comprueba si existe un jrxml en la carpeta compartida
@return true = Existe , false = No existe
\end */
function jasperPlugin_comprobarJasperFisico(reportName:String):Boolean
  {
    debug ("JASPER_PLUGIN :: buscando " + reportName);
    if (File.exists(reportName)) return true;
     else
     return false;

   }


/** Especifica que barras usa el S.O. al poner una ruta
@return / , linux, mac y  \\ windows
\end */
function jasperPlugin_seteaBarra():String
 {
    var retorno:String;
    var util:FLUtil = new FLUtil;
    var plataforma = util.getOS();
    if (plataforma == "WIN32")
        retorno = "\\";
    else
        retorno = "/";
    return retorno;

}

/** Genera ficheroTemporal en carpeta Temp.
@return Nombre del fichero temporal
\end */
function jasperPlugin_tratarReport(nombreInforme:String, nombreReport:String):String
{
    var date = new Date();
    var xmlFinal:String;
    var util:FLUtil = new FLUtil;
    var compilarSiempre:Boolean = false;
    compilarSiempre = util.readSettingEntry("jasperplugin/compilarSiempre");

    //Aqui introducimos el where y las rutas de los objetos..
    var rutaFicheroOriginal = this.iface.rutaReports + this.iface.dbName + this.iface.barra + "reports" + this.iface.barra + nombreInforme + this.iface.barra + nombreReport + ".jrxml"

    if (compilarSiempre == "false")
    	{
    	if (this.iface.reportAnterior == rutaFicheroOriginal)
    		{
    		debug("JASPER_PLUGIN :: Este report no será compilado");
    		return "Repetir";
    		}
    		else
    		{
    		debug("JASPER_PLUGIN :: Este report será compilado");
    		this.iface.reportAnterior = rutaFicheroOriginal;
    		}
    	} else debug("JASPER_PLUGIN :: COMPILAR SIEMPRE :: Activado");

    var ficheroO = new File(rutaFicheroOriginal);
        ficheroO.open(File.ReadOnly);
    var f = ficheroO.read();
    ficheroO.close();

    var consultaSQL:String;
    var nodeJasperReports;
    var xmlReport = new FLDomDocument();
if (sys.osName() == "WIN32")
  f = sys.toUnicode(f, "latin1");
    if (xmlReport.setContent(f)) {
	        if (xmlReport.namedItem("jasperReport"))
	                    {
	                     xmlFinal = xmlReport.toString(2);
			     //Tratamos codificación
				var codificacion = util.readSettingEntry("jasperplugin/codificacion");
				if (!codificacion) codificacion = 0;
				if ( codificacion == 1 ) xmlFinal = xmlFinal.replace("ISO-8859-1","UTF-8");
				if ( codificacion == 2 ) xmlFinal = xmlFinal.replace("UTF-8","ISO-8859-1");
	                     //xmlFinal =  xmlFinal.replace("groovy","java");
                             if (sys.osName() != "WIN32") //Convertimos el fichero a UTF8 si no es win32
     	                     xmlFinal = sys.toUnicode(xmlFinal, "utf8");
     	                     //Creamos el nombre del fichero...
                             var ficheroTemporal = this.iface.rutaReports + this.iface.dbName + this.iface.barra + "temp_files" + this.iface.barra + nombreReport + date.getYear().toString() + "_"
                       + date.getMonth().toString() + "_" + date.getDay().toString() + "_" + date.getHours().toString() + "_" + date.getMinutes().toString() + date.getSeconds().toString()+ date.getMilliseconds().toString() + ".jrxml";

                        //guardamos el fichero
                        try {
                            var ficheroD = new File(ficheroTemporal);
                            ficheroD.open(File.WriteOnly);
                            ficheroD.write(xmlFinal);
                            ficheroD.close();
                        } catch (e) {
                          AQUtil.destroyProgressDialog();
                          debug(e);
                          MessageBox.critical("" + e, MessageBox.Ok);
                          return;
                                    }
                 return ficheroTemporal;
                }   else  debug("JASPER_PLUGIN :: ERROR :: No se encuentra la etiqueta jasperReport");
        } else debug("JASPER_PLUGIN :: ERROR :: No se puede leer el contenido de la plantilla " + rutaFicheroOriginal);
}


function jasperPlugin_generarComando(rutaJP:String):Boolean
{
     var util:FLUtil = new FLUtil();
    var comando:String;
    var db_ = aqApp.db();

    var driver = db_.driverName();
    var driverJava:String;
    var jdbc:String;
    if (driver.startsWith("FLQPSQL"))
    {
    driverJava = "org.postgresql.Driver";
    jdbc = "jdbc:postgresql://" + db_.host() + ":" + db_.port() + "/" + db_.database();

    }else
    {
        driverJava = "com.mysql.jdbc.Driver";
        jdbc = "jdbc:mysql://"+ db_.host() + ":" + db_.port() + "/" + db_.database();
    }
    rutaJP = rutaJP + "enebooreports.jar";

    var maxJVM:String = util.readSettingEntry("jasperplugin/MaxJVM");
    if (maxJVM != "")
    		{
    		maxJVM = "-Xmx" + maxJVM + "m";
    		this.iface.procesoJP = new Process("java",maxJVM,"-jar",rutaJP,driverJava,jdbc,db_.user(),db_.password()) ;//Aqui ponemos java -jar la ruta al plugin , con los datos de la conexion
    		}
    		else this.iface.procesoJP = new Process("java","-jar",rutaJP,driverJava,jdbc,db_.user(),db_.password()) ;

    return true;
}


function jasperPlugin_establecerConsulta(cursor:FLSqlCursor, nombreConsulta:String, orderBy:String, groupBy:String, whereFijo:String):FLSqlQuery
{
        var util:FLUtil = new FLUtil();
        var q:FLSqlQuery = new FLSqlQuery(nombreConsulta);
        var fieldList:String = util.nombreCampos(cursor.table());
        var cuenta:Number = parseFloat(fieldList[0]);

        var signo:String;
        var fN:String;
        var valor:String;
        var primerCriterio:Boolean = false;
        var where:String = "";
        var criterio:String;
        for (var i:Number = 1; i <= cuenta; i++) {
                if (cursor.isNull(fieldList[i])) {
                        continue;
                }
                signo = this.iface.obtenerSigno(fieldList[i]);
                if (signo != "") {
                        fN = this.iface.fieldName(fieldList[i]);
                        valor = cursor.valueBuffer(fieldList[i]);
                        criterio = this.iface.aplicarCriterio(cursor.table(), fN, valor, signo);
                        if (criterio && criterio != "") {
                                if (primerCriterio == true) {
                                        where += " AND ";
                                }
                                where += criterio;
                                primerCriterio = true;
                        }
                }
        }

        if (whereFijo && whereFijo != "") {
                if (where == "")
                        where = whereFijo;
                else
                        where = whereFijo + " AND (" + where + ")";
        }

        this.iface.whereCursor = where; //Recogemos el where limpio (wherefijo + where de cursor);

        var ampliarWhere:String = this.iface.ampliarWhere(nombreConsulta);
        if (ampliarWhere)
                if (where)
                        where += " AND " + ampliarWhere;
                else
                        where += ampliarWhere;

        if (groupBy && groupBy != "") {
                if (where == "")
                        where = "1 = 1";
                where += " GROUP BY " + groupBy;
        }
        //Si no existe el .qry no continua procesandose la consulta
	if (!util.sqlSelect("flfiles", "nombre", "nombre = '" + nombreConsulta + ".qry'"))
		return q;

        q.setWhere(where);

        if (orderBy)
                q.setOrderBy(orderBy);

        return q;
}
//// JASPER_PLUGIN ///////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_definition jPluginPlus */
//////////////////////////////////////////////////////////////////
//// JPLUGIN_PLUS ///////////////////////////////////////////////
function jPluginPlus_lanzarInforme(cursor:FLSqlCursor, nombreInforme:String, orderBy:String, groupBy:String, etiquetas:Boolean, impDirecta:Boolean, whereFijo:String, nombreReport:String, numCopias:Number, impresora:String, pdf:Boolean)
{
    debug("KLO--> jPluginPlus_lanzarInforme()");
    debug("nombreInforme " + nombreInforme);
    switch(nombreInforme) {
        case "i_presupuestoscli":
        case "i_pedidoscli":
        case "i_albaranescli":
        case "i_facturascli":
        case "i_reciboscli":
        case "i_pedidosprov":
        case "i_albaranesprov":
        case "i_facturasprov":
        case "i_servicioscli":
        case "i_recibosprov": {
            break;
        }
        default: {
            return this.iface.__lanzarInforme(cursor, nombreInforme, orderBy, groupBy, etiquetas, impDirecta, whereFijo, nombreReport, numCopias, impresora, pdf);
        }
    }

    var util:FLUtil = new FLUtil();
    var report:String = "";
    var consulta:String = "";
    var ordenacion:String = "";
    var arrayModelos:Array = [];

    var nomTabla:String = cursor.table();
    if (nomTabla.startsWith("i_"))
        nomTabla = nomTabla.right(nomTabla.length - 2);

    //================================================================================================
    // KLO. Aqui es donde tengo que capturar los informes de topo jxml que haya en el directorio dado.
    // KLO this.iface.rutaReports + this.iface.dbName + this.iface.barra + "reports" + this.iface.barra + nombreInforme + this.iface.barra + nombreReport + ".jrxml"
    this.iface.rutaReports =  util.readSettingEntry("jasperplugin/reportspath");
    this.iface.dbName = util.readSettingEntry("DBA/lastDB");
    this.iface.barra = this.iface.seteaBarra(); //Barra de separacion.

    var rutaInforme:String = this.iface.rutaReports + this.iface.dbName + this.iface.barra + "reports" + this.iface.barra + nombreInforme + this.iface.barra;
    debug("KLO rutaInforme: "+rutaInforme);
    var dir:Dir = new Dir(rutaInforme);
    var listaF:Array = [];
    listaF = dir.entryList("*.jrxml");

    //for (var i = 0; i < listaF.length; i++)
      //debug("KLO--> Lista de ficheros jasper 2: "+listaF[i]);

    // KLO Código original.
    var dialog = new Dialog(util.translate ( "scripts", "Modelos de impresion" ), 0);
    dialog.caption = "Seleccionar un modelo de impresion";
    dialog.OKButtonText = util.translate ( "scripts", "Aceptar" );
    dialog.cancelButtonText = util.translate ( "scripts", "Cancelar" );

    var bgroup:GroupBox = new GroupBox;
    dialog.add( bgroup );
    var rB:Array = [];
    var nModelos:Number = 0;
    var hayDefecto:Boolean = false;
    var hayOficial:Boolean = false;
    var iniReport:String;
    var cont:Number = 0;
    var textModelo:String;

    for (nModelos = 0; nModelos < listaF.length; nModelos++) {
        textModelo = listaF[cont];
        var nombreReport:String = this.iface.cargaDescripcionJasper(rutaInforme + textModelo);
        if ( !nombreReport ) nombreReport =  textModelo.left(textModelo.find(".jrxml",0));
        //debug("Nombre del informe 2: "+textModelo.left(textModelo.find(".jrxml",0)));
        rB[cont] = new RadioButton;
        rB[cont].text = nombreReport;
        if (listaF[cont] == nombreInforme+".jrxml") {
            rB[cont].checked = true; //!hayDefecto;
            hayOficial = true;
        } else {
            rB[cont].checked = false;
        }
        arrayModelos[cont] = new Array(2);

        arrayModelos[cont]["report"] = listaF[cont];
        arrayModelos[cont]["consulta"] = "";
        arrayModelos[cont]["ordenacion"] = "";
        bgroup.add( rB[cont] );
        //debug("KLO-----> Metido1: "+arrayModelos[cont].report+", En posicion: "+cont);
        cont ++;
    }
//debug("KLO=====> cont = "+cont);

    if (!hayOficial) {
        //debug("KLO--> No hay IReport para oficial: "+nombreInforme);
        rB[cont] = new RadioButton;
        rB[cont].text = util.translate ( "scripts", "Modelo oficial" );
        arrayModelos[cont] = new Array(2);
        arrayModelos[cont]["report"] = nombreInforme;
        //debug("KLO-----> Metido: "+arrayModelos[cont].report+", En posicion: "+cont);
        arrayModelos[cont]["consulta"] = nombreInforme;
        arrayModelos[cont]["ordenacion"] = "";
        rB[cont].checked = true; //!hayDefecto;
        bgroup.add( rB[cont] );
        cont ++;
    }

    // No hay modelos adicionales
    if (cont-1 <= 0) {
        this.iface.__lanzarInforme(cursor, nombreInforme, orderBy, groupBy, etiquetas, impDirecta, whereFijo, nombreReport, numCopias, impresora, pdf);
        return;
    }

    var lista:String = "";
    if (!dialog.exec()) {
        return;
    }
    for (var i:Number = 0; i <= cont; i++) {
        //debug("KLO------> i = "+i);
        //debug("KLO--> arrayModelos en formulario: "+arrayModelos[i].report);
        if (rB[i].checked == true) {
            report = arrayModelos[i]["report"];
            //debug("KLO--> report devuelto: "+report);
            consulta = arrayModelos[i]["consulta"];
            if (!consulta || consulta == "") {
                consulta = nombreInforme;
            }
            ordenacion = arrayModelos[i]["ordenacion"];
            if (!ordenacion || ordenacion == "") {
                ordenacion = orderBy;
            }
            break;
        }
    }

    //if (!report) {
    //  report = nombreReport;
    //}

    this.iface.__lanzarInforme(cursor, consulta, ordenacion, groupBy, etiquetas, impDirecta, whereFijo, report, numCopias, impresora, pdf);
}

function jPluginPlus_cargaDescripcionJasper(fichero:String):String
{
   var xmlFinal:String;
    var ficheroO = new File(fichero);
        ficheroO.open(File.ReadOnly);
    var f = ficheroO.read();
    	ficheroO.close();
    var xmlReport = new FLDomDocument();
if (sys.osName() == "WIN32")
  f = sys.toUnicode(f, "latin1");
    if (xmlReport.setContent(f)) {
	        		if (xmlReport.namedItem("jasperReport"))
	                    		{
	                     		xmlFinal = xmlReport.toString(2);
					xmlFinal = xmlFinal.left(xmlFinal.find("\" >",0));
					xmlFinal = xmlFinal.mid(xmlFinal.find("name=\"",0));
					xmlFinal = xmlFinal.left(xmlFinal.find("\" ",0));
					xmlFinal = xmlFinal.right(xmlFinal.length - 6);
					if (sys.osName() != "WIN32") //Convertimos el fichero a UTF8 si no es win32
     	                     			xmlFinal = sys.toUnicode(xmlFinal, "utf8");
			    		}
				}
return xmlFinal;
}
//// JPLUGIN_PLUS ////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_definition recibosProv */
/////////////////////////////////////////////////////////////////
//// RECIBOS PROV ///////////////////////////////////////////////
function recibosProv_aplicarCriterio(tabla:String, campo:String, valor:String, signo:String):String
{
	var criterio:String = "";
	switch (tabla) {
		case "i_recibosprov": {
			switch (campo) {
				case "recibosprov.estado": {
					switch (valor) {
						case "Pendiente": {
							criterio = "recibosprov.estado IN ('Emitido', 'Devuelto')";
							break;
						}
					}
					break;
				}
			}
			break;
		}
	}

	if (criterio == "") {
		criterio = this.iface.__aplicarCriterio(tabla, campo, valor, signo);
	}
	return criterio;
}
//// RECIBOS PROV ///////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition infoVtos */
/////////////////////////////////////////////////////////////////
//// INFO_VENCIMIENTOS //////////////////////////////////////////
function infoVtos_cabeceraVencimientos(nodo:FLDomNode, campo:String):String
{
	switch (campo) {
		case "codejercicio":
			return nodo.attributeValue("criterios.codejercicio");
			break;
		case "empresa":
			return nodo.attributeValue("empresa.nombre");
			break;
		case "fachavtodesde":
			return nodo.attributeValue("criterios.fechavtodesde");
			break;
		case "fachavtohasta":
			return nodo.attributeValue("criterios.fechavtohasta");
			break;
	}
}
//// INFO_VENCIMIENTOS //////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition infoCliProv */
/////////////////////////////////////////////////////////////////
//// INFOCLIPROV //////////////////////////////////////////////////

function infoCliProv_cabeceraClientes(nodo:FLDomNode, campo:String):String
{
	var texCampo:String = new String(campo);

	var util:FLUtil = new FLUtil();

	var texto:String;
	var sep:String = "       ";

	var cri:Array = flfactppal.iface.pub_ejecutarQry("i_clientes", "descripcion,d_clientes_codcliente,h_clientes_codcliente,i_clientes_codagente,i_clientes_codgrupo,i_clientes_codserie,i_clientes_regimeniva,i_dirclientes_codpais","id = '" + this.iface.idInformeActual + "'");

	texto = " " + cri.descripcion + sep + sep;

	if (cri.d_clientes_codcliente || cri.h_clientes_codcliente)
		texto += util.translate("scripts","Clientes");

	if (cri.d_clientes_codcliente)
		texto += " " + util.translate("scripts","desde") + " " + cri.d_clientes_codcliente;

	if (cri.h_clientes_codcliente)
		texto += " " + util.translate("scripts","hasta") + " " + cri.h_clientes_codcliente;

	if (cri.i_clientes_codagente)
		texto += sep + util.translate("scripts","Agente") + " " + cri.i_clientes_codagente;

	if (cri.i_clientes_codgrupo)
		texto += sep + util.translate("scripts","Grupo") + " " + cri.i_clientes_codgrupo;

	if (cri.i_clientes_codserie)
		texto += sep + util.translate("scripts","Serie de facturación") + " " + cri.i_clientes_codserie;

	if (cri.i_clientes_regimeniva && cri.i_clientes_regimeniva != util.translate("scripts","Todos"))
		texto += sep + util.translate("scripts","Régimen I.V.A.") + " " + cri.i_clientes_regimeniva;

	if (cri.i_dirclientes_codpais)
		texto += sep + util.translate("scripts","País") + " " + cri.i_dirclientes_codpais;

	return texto;
}

function infoCliProv_cabeceraProveedores(nodo:FLDomNode, campo:String):String
{
	var texCampo:String = new String(campo);

	var util:FLUtil = new FLUtil();

	var texto:String;
	var sep:String = "       ";

	var cri:Array = flfactppal.iface.pub_ejecutarQry("i_proveedores", "descripcion,d_proveedores_codproveedor,h_proveedores_codproveedor,i_proveedores_codserie,i_proveedores_regimeniva,i_dirproveedores_codpais","id = '" + this.iface.idInformeActual + "'");

	texto = " " + cri.descripcion + sep + sep;

	if (cri.d_proveedores_codproveedor || cri.h_proveedores_codproveedor)
		texto += util.translate("scripts","Proveedores");

	if (cri.d_proveedores_codproveedor)
		texto += " " + util.translate("scripts","desde") + " " + cri.d_proveedores_codproveedor;

	if (cri.h_proveedores_codproveedor)
		texto += " " + util.translate("scripts","hasta") + " " + cri.h_proveedores_codproveedor;

	if (cri.i_proveedores_codserie)
		texto += sep + util.translate("scripts","Serie de facturación") + " " + cri.i_proveedores_codserie;

	if (cri.i_proveedores_regimeniva && cri.i_proveedores_regimeniva != util.translate("scripts","Todos"))
		texto += sep + util.translate("scripts","Régimen I.V.A.") + " " + cri.i_proveedores_regimeniva;

	if (cri.i_dirproveedores_codpais)
		texto += sep + util.translate("scripts","País") + " " + cri.i_dirproveedores_codpais;

	return texto;
}

/** \D Establece el id del informe que está siendo impreso
*/
function infoCliProv_establecerId(id:Number)
{
	this.iface.idInformeActual = id;
}

//// INFOCLIPROV //////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition envioMail */
/////////////////////////////////////////////////////////////////
//// ENVIO MAIL /////////////////////////////////////////////////
function envioMail_mostrarInformeVisor(visor:FLReportViewer):Boolean
{
	this.iface.visor_ = visor;
	this.iface.visor_.exec();
	return true;

/*	this.iface.visor_ = visor;
	var f = new FLFormSearchDB( "customviewer" );
	f.setMainWidget();
    f.exec();*/
}
//// ENVIO MAIL /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition dtoEspecial */
/////////////////////////////////////////////////////////////////
//// DTOESPECIAL/////////////////////////////////////////////////

function dtoEspecial_descuento(nodo:FLDomNode, campo:String):String
{
	var res:String;
	var idDescuento:String;
	var tabla:String;

	switch (campo) {
		case "facturacli": {
			tabla = "facturascli";
			break;
		}
		case "facturaprov": {
			tabla = "facturasprov";
			break;
		}
	}
    if ( nodo.attributeValue(tabla + ".pordtoesp") == 0 )
		res = "";
	else
		res = nodo.attributeValue(tabla + ".pordtoesp") + " %";

	return res;
}
//// DTOESPECIAL/////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition sepa19b2b */
/////////////////////////////////////////////////////////////////
//// SEPA19B2B /////////////////////////////////////////////////
function sepa19b2b_codpostalCiudadProvinciaCliente(nodo, campo)
{
	var _i = this.iface;

	var valor = "";
	var codPostal = nodo.attributeValue("dirclientes.codpostal");
	var ciudad = nodo.attributeValue("dirclientes.ciudad");
	var provincia = nodo.attributeValue("dirclientes.provincia");

	if (codPostal) {
		if(ciudad) {
			if(provincia) {
				valor = codPostal + " - " + ciudad + " (" + provincia + ")";
			}
		}
		else if(provincia) {
			valor = codPostal + " (" + provincia + ")";
		}
	}
	else {
		if(ciudad) {
			if(provincia) {
				valor = ciudad + " (" + provincia + ")";
			}
		}
		else if(provincia) {
			valor = "(" + provincia + ")";
		}
	}
	return valor;
}

function sepa19b2b_dameIdentificadorAcreedor(nodo, campo)
{
	var cifEmpresa = nodo.attributeValue("empresa.cifnif");
	var codCuenta = nodo.attributeValue("mandatoscli.codcuenta");

	var identificador = flfactppal.iface.calcularIdentificadorAcreedor(cifEmpresa, codCuenta);

	return identificador;
}

function sepa19b2b_codpostalCiudadProvincia(nodo, campo)
{
    var _i = this.iface;

    var valor = "";
    var codPostal = nodo.attributeValue("empresa.codpostal");
    var ciudad = nodo.attributeValue("empresa.ciudad");
    var provincia = nodo.attributeValue("empresa.provincia");

    if (codPostal) {
        if(ciudad) {
            if(provincia) {
                valor = codPostal + " - " + ciudad + " (" + provincia + ")";
            }
        }
        else if(provincia) {
            valor = codPostal + " (" + provincia + ")";
        }
    }
    else {
        if(ciudad) {
            if(provincia) {
                valor = ciudad + " (" + provincia + ")";
            }
        }
        else if(provincia) {
            valor = "(" + provincia + ")";
        }
    }
    return valor;
}
//// SEPA19B2B /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////

//// DESARROLLO /////////////////////////////////////////////////
////////////////////////////////////////////////////////////

