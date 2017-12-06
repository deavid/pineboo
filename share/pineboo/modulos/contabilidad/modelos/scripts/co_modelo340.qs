var form = this;
/***************************************************************************
                 co_modelo340.qs  -  description
                             -------------------
    begin                : mar feb 17 2009
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

/** @class_declaration interna */
////////////////////////////////////////////////////////////////////////////
//// DECLARACION ///////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////
//// INTERNA /////////////////////////////////////////////////////
class interna
{
  var ctx: Object;
  var numsecuencial_: Number = "0";
  function interna(context)
  {
    this.ctx = context;
  }
  function init()
  {
    return this.ctx.interna_init();
  }
  function calculateField(fN: String): String {
    return this.ctx.interna_calculateField(fN);
  }
  function validateForm(): Boolean {
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
  function oficial(context)
  {
    interna(context);
  }
  function bufferChanged(fN)
  {
    return this.ctx.oficial_bufferChanged(fN);
  }
  function establecerFechasPeriodo()
  {
    return this.ctx.oficial_establecerFechasPeriodo();
  }
  function comprobarFechas(): String {
    return this.ctx.oficial_comprobarFechas();
  }
  function habilitarPeriodo()
  {
    return this.ctx.oficial_habilitarPeriodo();
  }
  function calcularTotales()
  {
    return this.ctx.oficial_calcularTotales();
  }
  function pbnCalcularValores_clicked()
  {
    return this.ctx.oficial_pbnCalcularValores_clicked();
  }
  function cargarFacturasEmitidas(): Boolean {
    return this.ctx.oficial_cargarFacturasEmitidas();
  }
  function limpiarFacturasEmitidas(): Boolean {
    return this.ctx.oficial_limpiarFacturasEmitidas();
  }
  function cargarFacturasRecibidas(): Boolean {
    return this.ctx.oficial_cargarFacturasRecibidas();
  }
  function limpiarFacturasRecibidas(): Boolean {
    return this.ctx.oficial_limpiarFacturasRecibidas();
  }
  function cargarVariosIVAEmi(): Boolean {
    return this.ctx.oficial_cargarVariosIVAEmi();
  }
  function cargarVariosIVARec(): Boolean {
    return this.ctx.oficial_cargarVariosIVARec();
  }
  function dameWhereEmi(): String {
    return this.ctx.oficial_dameWhereEmi();
  }
  function dameWhereRec(): String {
    return this.ctx.oficial_dameWhereRec();
  }
  function tbnVerFacturaEmi_clicked()
  {
    return this.ctx.oficial_tbnVerFacturaEmi_clicked();
  }
  function tbnVerAsientoEmi_clicked()
  {
    return this.ctx.oficial_tbnVerAsientoEmi_clicked();
  }
  function tbnVerRecibosMetalico_clicked()
  {
    return this.ctx.oficial_tbnVerRecibosMetalico_clicked();
  }
  function tbnVerFacturaRec_clicked()
  {
    return this.ctx.oficial_tbnVerFacturaRec_clicked();
  }
  function tbnVerAsientoRec_clicked()
  {
    return this.ctx.oficial_tbnVerAsientoRec_clicked();
  }
  function obtenerTipoIdFiscal(tipoIdFiscal: String): String {
    return this.ctx.oficial_obtenerTipoIdFiscal(tipoIdFiscal);
  }
  function formatearTexto340(texto: String): String {
    return this.ctx.oficial_formatearTexto340(texto);
  }
  function cargaCobrosEfectivo()
  {
    return this.ctx.oficial_cargaCobrosEfectivo();
  }
  function dameDatosClienteEmi(qryEmitidas)
  {
    return this.ctx.oficial_dameDatosClienteEmi(qryEmitidas);
  }
  function dameFiltroPagoEfectivo()
  {
    return this.ctx.oficial_dameFiltroPagoEfectivo();
  }
  function dameFiltroEjerciciosEfectivo()
  {
    return this.ctx.oficial_dameFiltroEjerciciosEfectivo();
  }
  function revisarClaves()
  {
    return this.ctx.oficial_revisarClaves();
  }
  function cargarFacturasRecibidasCaja()
  {
    return this.ctx.oficial_cargarFacturasRecibidasCaja();
  }
}
//// OFICIAL /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////
class head extends oficial
{
  function head(context)
  {
    oficial(context);
  }
}
//// DESARROLLO /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_declaration ifaceCtx */
/////////////////////////////////////////////////////////////////
//// INTERFACE  /////////////////////////////////////////////////
class ifaceCtx extends head
{
  function ifaceCtx(context)
  {
    head(context);
  }
}

const iface = new ifaceCtx(this);
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
  var util = new FLUtil;
  var cursor = this.cursor();

  connect(cursor, "bufferChanged(QString)", this, "iface.bufferChanged");
  connect(this.child("pbnCalcularValores"), "clicked()", this, "iface.pbnCalcularValores_clicked");
  connect(this.child("tdbFacturasEmitidas").cursor(), "bufferCommited()", this, "iface.calcularTotales");
  connect(this.child("tdbFacturasRecibidas").cursor(), "bufferCommited()", this, "iface.calcularTotales");
  connect(this.child("tdbBienesInversion").cursor(), "bufferCommited()", this, "iface.calcularTotales");
  connect(this.child("tdbOperacionesIntracomunitarias").cursor(), "bufferCommited()", this, "iface.calcularTotales");
  connect(this.child("tbnVerFacturaEmi"), "clicked()", this, "iface.tbnVerFacturaEmi_clicked");
  connect(this.child("tbnVerRecibosMetalico"), "clicked()", this, "iface.tbnVerRecibosMetalico_clicked");
  connect(this.child("tbnVerAsientoEmi"), "clicked()", this, "iface.tbnVerAsientoEmi_clicked");
  connect(this.child("tbnVerFacturaRec"), "clicked()", this, "iface.tbnVerFacturaRec_clicked");
  connect(this.child("tbnVerAsientoRec"), "clicked()", this, "iface.tbnVerAsientoRec_clicked");

  if (cursor.modeAccess() == cursor.Insert) {
    this.child("fdbCodEjercicio").setValue(flfactppal.iface.pub_ejercicioActual());
    this.iface.numsecuencial_++;
    this.child("fdbNumIdentificativo").setValue(this.iface.calculateField("numidentificativo"));
    var apellidosNom: String = util.sqlSelect("co_datosfiscales", "apellidosrs", "1 = 1");
    if (apellidosNom) {
      this.child("fdbApellidosNombreRS").setValue(apellidosNom);
    }
    var cifNif: String = util.sqlSelect("co_datosfiscales", "cifnif", "1 = 1");
    if (cifNif) {
      this.child("fdbCifNif").setValue(cifNif);
    }
    var telefono: Number = util.sqlSelect("co_datosfiscales", "telefono", "1 = 1");
    if (telefono) {
      this.child("fdbTelefono").setValue(telefono);
    }
    var contacto: Number = util.sqlSelect("co_datosfiscales", "nombre", "1 = 1");
    if (contacto) {
      this.child("fdbContacto").setValue(contacto);
    }
  }

  this.child("tbwModelo340").setTabEnabled("bienesinversion", false);
  this.child("tbwModelo340").setTabEnabled("operacionesintracomunitarias", false);

  this.iface.habilitarPeriodo();

  switch (cursor.modeAccess()) {
    case cursor.Insert: {
      this.iface.establecerFechasPeriodo();
      break;
    }
  }
}

function interna_calculateField(fN): String {
  var util: FLUtil = new FLUtil;
  var cursor: FLSqlCursor = this.cursor();
  var valor: String;
  var numero: Number;
  switch (fN)
  {
    case "numidentificativo": {
      var periodo: String;
      if (cursor.valueBuffer("tipoperiodo") == "Mes") {
        periodo = cursor.valueBuffer("mes");
      } else {
        if (cursor.valueBuffer("trimestre") == "1T") {
          periodo = "03";
        }
        if (cursor.valueBuffer("trimestre") == "2T") {
          periodo = "06";
        }
        if (cursor.valueBuffer("trimestre") == "3T") {
          periodo = "09";
        }
        if (cursor.valueBuffer("trimestre") == "4T") {
          periodo = "12";
        }
      }
      numero = flfactppal.iface.pub_cerosIzquierda(this.iface.numsecuencial_, 4);
      valor = "340" + cursor.valueBuffer("codejercicio") + periodo + numero;
      break;
    }
    case "baseimponible": {
      var idModelo: String = cursor.valueBuffer("idmodelo");
      var baseEmi: Number = parseFloat(util.sqlSelect("co_facturasemi340", "SUM(baseimponible)", "idmodelo = " + idModelo));
      if (isNaN(baseEmi)) {
        baseEmi = 0;
      }
      var baseRec: Number = parseFloat(util.sqlSelect("co_facturasrec340", "SUM(baseimponible)", "idmodelo = " + idModelo));
      if (isNaN(baseRec)) {
        baseRec = 0;
      }
      valor = parseFloat(baseEmi) + parseFloat(baseRec);
      break;
    }
    case "cuotaimpuesto": {
      var idModelo: String = cursor.valueBuffer("idmodelo");
      var baseEmi: Number = parseFloat(util.sqlSelect("co_facturasemi340", "SUM(cuotaimpuesto)", "idmodelo = " + idModelo));
      if (isNaN(baseEmi)) {
        baseEmi = 0;
      }
      var baseRec: Number = parseFloat(util.sqlSelect("co_facturasrec340", "SUM(cuotaimpuesto)", "idmodelo = " + idModelo));
      if (isNaN(baseRec)) {
        baseRec = 0;
      }
      valor = parseFloat(baseEmi) + parseFloat(baseRec);
      break;
    }
    case "totalfacturas": {
      var idModelo: String = cursor.valueBuffer("idmodelo");
      var baseEmi: Number = parseFloat(util.sqlSelect("co_facturasemi340", "SUM(importetotal)", "idmodelo = " + idModelo));
      if (isNaN(baseEmi)) {
        baseEmi = 0;
      }
      var baseRec: Number = parseFloat(util.sqlSelect("co_facturasrec340", "SUM(importetotal)", "idmodelo = " + idModelo));
      if (isNaN(baseRec)) {
        baseRec = 0;
      }
      valor = parseFloat(baseEmi) + parseFloat(baseRec);
      break;
    }
  }
  return valor;
}

function interna_validateForm(): Boolean {
  if (!this.iface.comprobarFechas())
  {
    return false;
  }

  return true;
}
//// INTERNA /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
function oficial_bufferChanged(fN)
{
  var cursor: FLSqlCursor = this.cursor();
  switch (fN) {
    case "codejercicio": {
      this.child("fdbNumIdentificativo").setValue(this.iface.calculateField("numidentificativo"));
      break;
    }
    case "tipoperiodo": {
      this.iface.habilitarPeriodo();
      this.iface.establecerFechasPeriodo();
      this.child("fdbNumIdentificativo").setValue(this.iface.calculateField("numidentificativo"));
      break;
    }
    case "mes":
    case "trimestre": {
      this.iface.establecerFechasPeriodo();
      this.child("fdbNumIdentificativo").setValue(this.iface.calculateField("numidentificativo"));
      break;
    }
  }
}

/** \D Establece las fechas de inicio y fin de trimestre en función del trimestre seleccionado
\end */
function oficial_establecerFechasPeriodo()
{
  var util: FLUtil = new FLUtil();
  var cursor: FLSqlCursor = this.cursor();

  var fechaInicio: Date;
  var fechaFin: Date;
  var codEjercicio: String = this.child("fdbCodEjercicio").value();
  var inicioEjercicio = util.sqlSelect("ejercicios", "fechainicio", "codejercicio = '" + codEjercicio + "'");

  if (!inicioEjercicio) {
    return false;
  }

  fechaInicio.setYear(inicioEjercicio.getYear());
  fechaFin.setYear(inicioEjercicio.getYear());
  fechaInicio.setDate(1);

  switch (cursor.valueBuffer("tipoperiodo")) {
    case "Trimestre": {
      switch (cursor.valueBuffer("trimestre")) {
        case "1T": {
          fechaInicio.setMonth(1);
          fechaFin.setMonth(3);
          fechaFin.setDate(31);
          break;
        }
        case "2T": {
          fechaInicio.setMonth(4);
          fechaFin.setMonth(6);
          fechaFin.setDate(30);
          break;
        }
        case "3T":
          fechaInicio.setMonth(7);
          fechaFin.setMonth(9);
          fechaFin.setDate(30);
          break;
        case "4T": {
          fechaInicio.setMonth(10);
          fechaFin.setMonth(12);
          fechaFin.setDate(31);
          break;
        }
        default: {
          fechaInicio = false;
        }
      }
      break;
    }
    case "Mes": {
      var numMes: Number = parseInt(cursor.valueBuffer("mes"));
      fechaInicio.setDate(1);
      fechaInicio.setMonth(numMes);
      fechaFin = util.addMonths(fechaInicio, 1);
      fechaFin = util.addDays(fechaFin, -1);
      break;
    }
  }

  if (fechaInicio) {
    this.child("fdbFechaInicio").setValue(fechaInicio);
    this.child("fdbFechaFin").setValue(fechaFin);
  } else {
    cursor.setNull("fechainicio");
    cursor.setNull("fechafin");
  }
}

/** \D Comprueba que fechainicio es menor que fechafin y que ambas pertenecen al ejercicio seleccionado
@return True si la comprobación es buena, false en caso contrario
\end */
function oficial_comprobarFechas(): Boolean {
  var util: FLUtil = new FLUtil();

  var codEjercicio: String = this.child("fdbCodEjercicio").value();
  var fechaInicio: String = this.child("fdbFechaInicio").value();
  var fechaFin: String = this.child("fdbFechaFin").value();

  if (util.daysTo(fechaInicio, fechaFin) < 0)
  {
    MessageBox.critical(util.translate("scripts", "La fecha de inicio debe ser menor que la de fin"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
    return false;
  }

  var inicioEjercicio: String = util.sqlSelect("ejercicios", "fechainicio", "codejercicio = '" + codEjercicio + "'");
  var finEjercicio: String = util.sqlSelect("ejercicios", "fechafin", "codejercicio = '" + codEjercicio + "'");

  if ((util.daysTo(inicioEjercicio, fechaInicio) < 0) || (util.daysTo(fechaFin, finEjercicio) < 0))
  {
    MessageBox.critical(util.translate("scripts", "Las fechas seleccionadas no corresponden al ejercicio"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
    return false;
  }

  return true;
}

function oficial_habilitarPeriodo()
{
  var cursor: FLSqlCursor = this.cursor();

  if (cursor.valueBuffer("tipoperiodo") == "Mes") {
    this.child("fdbMes").setShowAlias(true);
    this.child("fdbMes").setShowEditor(true);
    this.child("fdbTrimestre").setShowAlias(false);
    this.child("fdbTrimestre").setShowEditor(false);
  } else {
    this.child("fdbTrimestre").setShowAlias(true);
    this.child("fdbTrimestre").setShowEditor(true);
    this.child("fdbMes").setShowAlias(false);
    this.child("fdbMes").setShowEditor(false);
  }
}

function oficial_calcularTotales()
{
  var cursor: FLSqlCursor = this.cursor();
  var util: FLUtil = new FLUtil();
  var numero: Number = 0;

  numero += util.sqlSelect("co_facturasemi340", "COUNT(id)", "idmodelo = " + cursor.valueBuffer("idmodelo"));
  numero += util.sqlSelect("co_facturasrec340", "COUNT(id)", "idmodelo = " + cursor.valueBuffer("idmodelo"));
  numero += util.sqlSelect("co_bienesinv340", "COUNT(id)", "idmodelo = " + cursor.valueBuffer("idmodelo"));
  numero += util.sqlSelect("co_opintracomunitarias340", "COUNT(id)", "idmodelo = " + cursor.valueBuffer("idmodelo"));

  this.child("fdbNumRegistros").setValue(numero);
  this.child("fdbBaseImponible").setValue(this.iface.calculateField("baseimponible"));
  this.child("fdbCuotaImpuesto").setValue(this.iface.calculateField("cuotaimpuesto"));
  this.child("fdbTotalFacturas").setValue(this.iface.calculateField("totalfacturas"));
}

function oficial_pbnCalcularValores_clicked()
{
  var _i = this.iface;
  var util = new FLUtil;
  var cursor = this.cursor();

  if (cursor.modeAccess() == cursor.Insert) {
    var curEmitidas: FLSqlCursor = this.child("tdbFacturasEmitidas").cursor();
    if (!curEmitidas.commitBufferCursorRelation()) {
      return false;
    }
  }

  if (cursor.valueBuffer("revisarclaves")) {
    if (!_i.revisarClaves()) {
      return false;
    }
  }

  if (!this.iface.cargarFacturasEmitidas()) {
    return false;
  }
  this.child("tdbFacturasEmitidas").refresh();

  if (!this.iface.cargarFacturasRecibidas()) {
    return false;
  }
  if (!_i.cargarFacturasRecibidasCaja()) {
    return false;
  }
  this.child("tdbFacturasRecibidas").refresh();
  this.iface.calcularTotales();

  MessageBox.information(sys.translate("Los datos relativos al modelo han sido cargados correctamente"), MessageBox.Ok, MessageBox.NoButton);
}

function oficial_revisarClaves()
{
  var _i = this.iface;
  var cursor = this.cursor();
  var codEjercicio = cursor.valueBuffer("codejercicio");
  var fechaInicio = cursor.valueBuffer("fechainicio");
  var fechaFin = cursor.valueBuffer("fechafin");
  var p, editable, clave, claveCal, desglose, desgloseCal;


  var qEmi = new FLSqlQuery;
  qEmi.setSelect("idfactura");
  qEmi.setFrom("facturascli");
  qEmi.setWhere("codejercicio = '" + codEjercicio + "' AND fecha BETWEEN '" + fechaInicio + "' AND '" + fechaFin + "' AND NOT manual340");
  if (!qEmi.exec()) {
    return false;
  }
  var curEmi = new FLSqlCursor("facturascli");
  curEmi.setActivatedCommitActions(false);
  curEmi.setActivatedCheckIntegrity(false);
  AQUtil.createProgressDialog(sys.translate("Revisando claves de facturas emitidas"), qEmi.size());
  p = 0;
  while (qEmi.next()) {
    AQUtil.setProgress(p++);

    curEmi.select("idfactura = " + qEmi.value("idfactura"));
    if (!curEmi.first()) {
      AQUtil.destroyProgressDialog();
      return false;
    }
    curEmi.setModeAccess(curEmi.Browse);
    curEmi.refreshBuffer();
    clave = curEmi.valueBuffer("claveoperacion340");
    desglose = curEmi.valueBuffer("desglose340");

    claveCal = formfacturascli.iface.pub_commonCalculateField("claveoperacion340", curEmi);
    desgloseCal = formfacturascli.iface.pub_commonCalculateField("desglose340", curEmi);

    if (clave == claveCal && desglose == desgloseCal) {
      continue;
    }

    editable = curEmi.valueBuffer("editable");
    if (!editable) {
      curEmi.setUnLock("editable", true);
      curEmi.select("idfactura = " + qEmi.value("idfactura"));
      if (!curEmi.first()) {
        AQUtil.destroyProgressDialog();
        return false;
      }
    }
    curEmi.setModeAccess(curEmi.Edit);
    curEmi.refreshBuffer();
    curEmi.setValueBuffer("claveoperacion340", claveCal);
    curEmi.setValueBuffer("desglose340", desgloseCal);
    if (!curEmi.commitBuffer()) {
      AQUtil.destroyProgressDialog();
      return false;
    }
    if (!editable) {
      curEmi.select("idfactura = " + qEmi.value("idfactura"));
      if (!curEmi.first()) {
        AQUtil.destroyProgressDialog();
        return false;
      }
      curEmi.setUnLock("editable", false);
    }
  }
  AQUtil.destroyProgressDialog();


  var qRec = new FLSqlQuery;
  qRec.setSelect("idfactura");
  qRec.setFrom("facturasprov");
  qRec.setWhere("codejercicio = '" + codEjercicio + "' AND fecha BETWEEN '" + fechaInicio + "' AND '" + fechaFin + "' AND NOT manual340");
  if (!qRec.exec()) {
    return false;
  }
  var curRec = new FLSqlCursor("facturasprov");
  curRec.setActivatedCommitActions(false);
  curRec.setActivatedCheckIntegrity(false);
  AQUtil.createProgressDialog(sys.translate("Revisando claves de facturas recibidas"), qRec.size());
  p = 0;
  while (qRec.next()) {
    AQUtil.setProgress(p++);

    curRec.select("idfactura = " + qRec.value("idfactura"));
    if (!curRec.first()) {
      AQUtil.destroyProgressDialog();
      return false;
    }
    curRec.setModeAccess(curRec.Browse);
    curRec.refreshBuffer();
    clave = curRec.valueBuffer("claveoperacion340");
    desglose = curRec.valueBuffer("desglose340");

    claveCal = formfacturasprov.iface.pub_commonCalculateField("claveoperacion340", curRec);
    desgloseCal = formfacturasprov.iface.pub_commonCalculateField("desglose340", curRec);

    if (clave == claveCal && desglose == desgloseCal) {
      continue;
    }

    editable = curRec.valueBuffer("editable");
    if (!editable) {
      curRec.setUnLock("editable", true);
      curRec.select("idfactura = " + qRec.value("idfactura"));
      if (!curRec.first()) {
        AQUtil.destroyProgressDialog();
        return false;
      }
    }
    curRec.setModeAccess(curRec.Edit);
    curRec.refreshBuffer();
    curRec.setValueBuffer("claveoperacion340", claveCal);
    curRec.setValueBuffer("desglose340", desgloseCal);
    if (!curRec.commitBuffer()) {
      AQUtil.destroyProgressDialog();
      return false;
    }
    if (!editable) {
      curRec.select("idfactura = " + qRec.value("idfactura"));
      if (!curRec.first()) {
        AQUtil.destroyProgressDialog();
        return false;
      }
      curRec.setUnLock("editable", false);
    }
  }
  AQUtil.destroyProgressDialog();

  return true;
}

function oficial_cargarFacturasEmitidas()
{
  var _i = this.iface;
  var util = new FLUtil;
  var cursor = this.cursor();

  var idModelo = cursor.valueBuffer("idmodelo");
  var codEjercicio = cursor.valueBuffer("codejercicio");
  var fechaInicioE = util.sqlSelect("ejercicios", "fechainicio", "codejercicio = '" + codEjercicio + "'");
  var anoF = fechaInicioE.getYear();

  if (!_i.limpiarFacturasEmitidas()) {
    return false;
  }
  var qryEmitidas = new FLSqlQuery("co_i_facturasemi");
  var where = _i.dameWhereEmi();

  qryEmitidas.setWhere(where);
  qryEmitidas.setForwardOnly(true);
  if (!qryEmitidas.exec()) {
    return false;
  }
  var qryDatosCliente: FLSqlQuery = new FLSqlQuery;
  qryDatosCliente.setTablesList("clientes,dirclientes,paises");
  qryDatosCliente.setSelect("p.codiso, c.tipoidfiscal");
  qryDatosCliente.setFrom("clientes c INNER JOIN dirclientes dc ON (c.codcliente = dc.codcliente AND dc.domfacturacion = true) LEFT OUTER JOIN paises p ON dc.codpais = p.codpais");

  var qryFactura: FLSqlQuery = new FLSqlQuery;
  qryFactura.setTablesList("facturascli");
  qryFactura.setSelect("codcliente, nombrecliente, cifnif, idfactura, codigo, deabono, idfacturarect, codigo, claveoperacion340, codinmueble340, desglose340");
  qryFactura.setFrom("facturascli");

  var curEmitidas = new FLSqlCursor("co_facturasemi340");
  var cifNif, codPais;
  var base, cuota, importe, cuotaRecargor;
  var idAsiento, idFactura, operacion, codInmueble, desglose340, codFacRectificada, codFactura, numAsiento;
  var razonSocial, codCliente, tipoIdFiscal;
  AQUtil.createProgressDialog(sys.translate("Cargando facturas emitidas..."), qryEmitidas.size());
  var paso = 0;
  var codTipoEspecial;

  while (qryEmitidas.next()) {
    util.setProgress(++paso);
    tipoIdFiscal = "1";
    operacion = "";
    idFactura = "";
    codFacRectificada = "";
    idAsiento = qryEmitidas.value("co_asientos.idasiento");
    numAsiento = qryEmitidas.value("co_asientos.numero");
    codTipoEspecial = qryEmitidas.value("sc1.idcuentaesp");

    qryFactura.setWhere("idasiento = " + idAsiento);
    if (!qryFactura.exec()) {
      AQUtil.destroyProgressDialog();
      return false;
    }
    if (qryFactura.first()) {
      codCliente = qryFactura.value("codcliente");
      cifNif = qryFactura.value("cifnif");
      idFactura = qryFactura.value("idfactura");
      codFactura = qryFactura.value("codigo");
      operacion = qryFactura.value("claveoperacion340");
      codInmueble = qryFactura.value("codinmueble340");
      desglose340 = qryFactura.value("desglose340");
      if (qryFactura.value("deabono")) {
        codFacRectificada = util.sqlSelect("facturascli", "codigo", "idfactura = " + qryFactura.value("idfacturarect"));
      }
      razonSocial = qryFactura.value("nombrecliente");
      qryDatosCliente.setWhere("c.codcliente = '" + codCliente + "'");
      codFactura = qryFactura.value("codigo");
    } else {
      var oDatos = _i.dameDatosClienteEmi(qryEmitidas);
      if (!oDatos) {
        return false;
      }
      codCliente = oDatos.codCliente;
      qryDatosCliente.setWhere("c.codcliente = '" + codCliente + "'");
      razonSocial = oDatos.razonSocial;
      cifNif = oDatos.cifNif;
      codFactura = oDatos.codFactura;
    }
    razonSocial = razonSocial.left(40);
    razonSocial = this.iface.formatearTexto340(razonSocial)

    if (!qryDatosCliente.exec()) {
      AQUtil.destroyProgressDialog();
      return false;
    }
    if (qryDatosCliente.first()) {
      tipoIdFiscal = qryDatosCliente.value("c.tipoidfiscal");
      codPais = qryDatosCliente.value("p.codiso");
    }
    if (!codPais || codPais == "") {
      codPais = "ES";
    }

    curEmitidas.setModeAccess(curEmitidas.Insert);
    curEmitidas.refreshBuffer();
    curEmitidas.setValueBuffer("idmodelo", idModelo);
    if (codPais == "ES") {
      cifNif = flcontmode.iface.pub_limpiarCifNif(cifNif);
      if (cifNif.length > 9) {
        var mensaje: String;
        if (idFactura != "") {
          mensaje = util.translate("scripts", "El N.I.F. %1 de la factura %2 (%3) tiene más de 9 caracteres.\nPulse Calcelar para cancelar la operación o Ignorar para ignorar esta factura").arg(cifNif).arg(codFactura).arg(razonSocial);
        } else {
          mensaje = util.translate("scripts", "El N.I.F. %1 del asiento %2 (%3) tiene más de 9 caracteres.\nPulse Calcelar para cancelar la operación o Ignorar para ignorar esta factura").arg(cifNif).arg(numAsiento).arg(razonSocial);
        }
        var res: Number = MessageBox.warning(mensaje, MessageBox.Ignore, MessageBox.Cancel);
        if (res == MessageBox.Ignore) {
          continue;
        } else {
          AQUtil.destroyProgressDialog();
          return false;
        }
      }
      curEmitidas.setValueBuffer("cifnif", cifNif);
    } else {
      curEmitidas.setValueBuffer("numidentificacion", cifNif);
    }
    if (!cifNif || cifNif == "") {
      var mensaje: String;
      if (idFactura != "") {
        mensaje = util.translate("scripts", "La factura %1 (%2) no tiene Identificador Fiscal asociado.\nPulse Calcelar para cancelar la operación o Ignorar para ignorar esta factura").arg(codFactura).arg(razonSocial);
      } else {
        mensaje = util.translate("scripts", "El asiento (%2) no tiene Identificador Fiscal asociado.\nPulse Calcelar para cancelar la operación o Ignorar para ignorar esta factura").arg(numAsiento).arg(razonSocial);
      }
      var res = MessageBox.warning(mensaje, MessageBox.Ignore, MessageBox.Cancel);
      if (res == MessageBox.Ignore) {
        continue;
      } else {
        util.destroyProgressDialog();
        return false;
      }
    }
    curEmitidas.setValueBuffer("apellidosnomrs", razonSocial);
    curEmitidas.setValueBuffer("codpais", codPais);
    if (tipoIdFiscal != "1") {
      tipoIdFiscal = this.iface.obtenerTipoIdFiscal(tipoIdFiscal);
      if ((tipoIdFiscal != "1" && codPais == "ES") || (tipoIdFiscal == "1" && codPais != "ES")) {
        var res: Number = MessageBox.warning(util.translate("scripts", "Los datos de Tipo de Identificación Fiscal y país del cliente no son coherentes para:\n%1\nFactura / Asiento: %2").arg(razonSocial).arg(idFactura != "" ? codFactura : numAsiento), MessageBox.Ignore, MessageBox.Cancel);
        if (res == MessageBox.Ignore) {
          continue;
        } else {
          util.destroyProgressDialog();
          return false;
        }
      }
    }
    curEmitidas.setValueBuffer("claveidentificacion", tipoIdFiscal);
    curEmitidas.setValueBuffer("tipolibro", "E");
    if (operacion == "") {
      curEmitidas.setNull("operacion");
    } else {
      curEmitidas.setValueBuffer("operacion", operacion);
    }

    /// Clave R (Arrendamiento)
    if (operacion == "R" && codInmueble != "") {
      var qInmueble = new FLSqlQuery;
      qInmueble.setSelect("situacion, refcatastral");
      qInmueble.setFrom("co_inmueble");
      qInmueble.setWhere("codinmueble = '" + codInmueble + "'");
      if (!qInmueble.exec()) {
        return false;
      }
      if (!qInmueble.first()) {
        return false;
      }
      curEmitidas.setValueBuffer("codinmueble", codInmueble);
      curEmitidas.setValueBuffer("codsituinmueble", qInmueble.value("situacion"));
      curEmitidas.setValueBuffer("refcatastral", qInmueble.value("refcatastral"));
    }

    /// Clave C (Varios IVA)
    if (operacion == "C" && desglose340) {
      curEmitidas.setValueBuffer("desgloseregistro", desglose340);
    } else {
      curEmitidas.setValueBuffer("desgloseregistro", 1);
    }

    curEmitidas.setValueBuffer("fechaexpedicion", qryEmitidas.value("co_asientos.fecha"));
    curEmitidas.setValueBuffer("fechaoperacion", qryEmitidas.value("co_asientos.fecha"));
    curEmitidas.setValueBuffer("tipoimpositivo", qryEmitidas.value("co_partidas.iva"));
    base = qryEmitidas.value("co_partidas.baseimponible");
    curEmitidas.setValueBuffer("baseimponible", base);
    cuota = qryEmitidas.value("(co_partidas.haber - co_partidas.debe)");
    curEmitidas.setValueBuffer("cuotaimpuesto", cuota);
    importe = parseFloat(base) + parseFloat(cuota);
    curEmitidas.setValueBuffer("importetotal", util.roundFieldValue(importe, "co_facturasemi340", "importetotal"));
    curEmitidas.setValueBuffer("baseimponiblecoste", 0);
    curEmitidas.setValueBuffer("idenfactura", codFactura);
    curEmitidas.setValueBuffer("numregistro", numAsiento);
    curEmitidas.setValueBuffer("numfacturas", 1);
    if (codFacRectificada && codFacRectificada != "" && operacion == "D") {
      curEmitidas.setValueBuffer("identfacturarect", codFacRectificada);
    }
    recargo = qryEmitidas.value("co_partidas.recargo");
    curEmitidas.setValueBuffer("tiporecequi", recargo);
    curEmitidas.setValueBuffer("idasiento", idAsiento);
    if (idFactura && idFactura != "") {
      curEmitidas.setValueBuffer("idfactura", idFactura);
    }
    cuotaRecargo = base * recargo / 100;
    curEmitidas.setValueBuffer("cuotarecequi", util.roundFieldValue(cuotaRecargo, "co_facturasemi340", "cuotarecequi"));
    curEmitidas.setValueBuffer("ejerciciometalico", anoF);
    if (!curEmitidas.commitBuffer()) {
      AQUtil.destroyProgressDialog();
      return false;
    }
  }
  AQUtil.destroyProgressDialog();

  if (!_i.cargarVariosIVAEmi()) {
    return false;
  }

  if (!_i.cargaCobrosEfectivo()) {
    return false;
  }
  return true;
}

function oficial_dameDatosClienteEmi(qryEmitidas)
{
  var cursor = this.cursor();

  var codEjercicio = cursor.valueBuffer("codejercicio");
  var oDatos = new Object;
  var codSubcuentaCli = qryEmitidas.value("co_partidas.codcontrapartida");
  var codCliente = AQUtil.sqlSelect("co_subcuentascli", "codcliente", "codsubcuenta = '" + codSubcuentaCli + "' AND codejercicio = '" + codEjercicio + "'");
  if (!codCliente) {
    MessageBox.warning(sys.translate("No se ha encontrado el cliente asociado a la subcuenta %1 y el ejercicio %2").arg(codSubcuentaCli).arg(codEjercicio), MessageBox.Ok, MessageBox.NoButton);
    return false;
  }
  oDatos.razonSocial = qryEmitidas.value("sc2.descripcion");
  oDatos.cifNif = qryEmitidas.value("co_partidas.cifnif");
  oDatos.codFactura = qryEmitidas.value("co_partidas.documento");
  oDatos.codCliente = codCliente;
  return oDatos;
}

function oficial_cargaCobrosEfectivo()
{
  return true; /// Hay que cambiarlo para usar cuentas contables de caja / efectivo
  var _i = this.iface;
  var util = new FLUtil;
  var cursor = this.cursor();

  var codEjercicio = cursor.valueBuffer("codejercicio");
  var idModelo = cursor.valueBuffer("idmodelo");
  var filtroPagoEfectivo = _i.dameFiltroPagoEfectivo();
  var filtroEjerciciosEfectivo = _i.dameFiltroEjerciciosEfectivo();
  var qEfectivo = new FLSqlQuery; /// \D Esta consulta solo detecta si hay o no pagos en efectivo. El cálculo se hace dentro del bucle
  qEfectivo.setSelect("f.codcliente, f.codejercicio");
  qEfectivo.setFrom("facturascli f INNER JOIN reciboscli r ON f.idfactura = r.idfactura INNER JOIN pagosdevolcli pd ON r.idrecibo = pd.idrecibo INNER JOIN co_asientos a ON pd.idasiento = a.idasiento");
  qEfectivo.setWhere("pd.fecha BETWEEN '" + cursor.valueBuffer("fechainicio") + "' AND '" + cursor.valueBuffer("fechafin") + "' AND a.codejercicio = '" + codEjercicio + "' AND " + filtroPagoEfectivo + " AND " + filtroEjerciciosEfectivo + " GROUP BY f.codcliente, f.codejercicio");
  qEfectivo.setForwardOnly(true);
  debug(qEfectivo.sql());
  if (!qEfectivo.exec()) {
    return false;
  }
  var fInicio = util.sqlSelect("ejercicios", "fechainicio", "codejercicio = '" + codEjercicio + "'");
  var metalicoPagos, metalicoDevs, metalico, paso = 0;
  var codEjercicioF, fechaInicioF, anoF, codCliente, codPais, cifNif, nombreCliente;
  var curEmitidas = new FLSqlCursor("co_facturasemi340");

  var qryDatosCliente = new FLSqlQuery;
  qryDatosCliente.setTablesList("clientes,dirclientes,paises");
  qryDatosCliente.setSelect("p.codiso, c.tipoidfiscal, c.cifnif, c.nombre");
  qryDatosCliente.setFrom("clientes c INNER JOIN dirclientes dc ON (c.codcliente = dc.codcliente AND dc.domfacturacion = true) LEFT OUTER JOIN paises p ON dc.codpais = p.codpais");
  qryDatosCliente.setForwardOnly(true);

  util.createProgressDialog(util.translate("scripts", "Generando cobros de importes en metálico..."), qEfectivo.size());
  while (qEfectivo.next()) {
    util.setProgress(paso++);
    codEjercicioF = qEfectivo.value("f.codejercicio");
    fechaInicioF = util.sqlSelect("ejercicios", "fechainicio", "codejercicio = '" + codEjercicioF + "'");
    anoF = fechaInicioF.getYear();
    codCliente = qEfectivo.value("f.codcliente");
    metalicoPagos = util.sqlSelect("facturascli f INNER JOIN reciboscli r ON f.idfactura = r.idfactura INNER JOIN pagosdevolcli pd ON r.idrecibo = pd.idrecibo INNER JOIN co_asientos a ON pd.idasiento = a.idasiento", "SUM(r.importe)", "f.codcliente = '" + codCliente + "' AND a.codejercicio = '" + codEjercicio + "' AND pd.fecha BETWEEN '" + fInicio + "' AND '" + cursor.valueBuffer("fechafin") + "' AND f.codejercicio = '" + codEjercicioF + "' AND " + filtroPagoEfectivo + " AND pd.tipo = 'Pago'", "facturascli");
    metalicoDevs = util.sqlSelect("facturascli f INNER JOIN reciboscli r ON f.idfactura = r.idfactura INNER JOIN pagosdevolcli pd ON r.idrecibo = pd.idrecibo INNER JOIN co_asientos a ON pd.idasiento = a.idasiento", "SUM(r.importe)", "f.codcliente = '" + codCliente + "' AND a.codejercicio = '" + codEjercicio + "' AND pd.fecha BETWEEN '" + fInicio + "' AND '" + cursor.valueBuffer("fechafin") + "' AND f.codejercicio = '" + codEjercicioF + "' AND " + filtroPagoEfectivo + " AND pd.tipo = 'Devolución'", "facturascli");
    metalicoPagos = isNaN(metalicoPagos) ? 0 : metalicoPagos;
    metalicoDevs = isNaN(metalicoDevs) ? 0 : metalicoDevs;
    metalico = metalicoPagos - metalicoDevs;
    if (isNaN(metalico) || metalico <= 6000) {
      continue;
    }
    qryDatosCliente.setWhere("c.codcliente = '" + codCliente + "'");
    if (!qryDatosCliente.exec()) {
      util.destroyProgressDialog();
      return false;
    }
    if (!qryDatosCliente.first()) {
      util.destroyProgressDialog();
      return false;
    }
    tipoIdFiscal = qryDatosCliente.value("c.tipoidfiscal");
    cifNif = qryDatosCliente.value("c.cifnif");
    codPais = qryDatosCliente.value("p.codiso");
    nombreCliente = qryDatosCliente.value("c.nombre");
    nombreCliente = nombreCliente.left(40);
    nombreCliente = _i.formatearTexto340(nombreCliente);
    if (!codPais || codPais == "") {
      codPais = "ES";
    }

    curEmitidas.setModeAccess(curEmitidas.Insert);
    curEmitidas.refreshBuffer();
    curEmitidas.setValueBuffer("idmodelo", idModelo);
    if (codPais == "ES") {
      cifNif = flcontmode.iface.pub_limpiarCifNif(cifNif);
      if (cifNif.length > 9) {
        var mensaje = util.translate("scripts", "El N.I.F. %1 del cliente %2 (%3) tiene más de 9 caracteres.\nPulse Calcelar para cancelar la operación o Ignorar para ignorar este registro de metálico").arg(cifNif).arg(codCliente).arg(nombreCliente);
        var res = MessageBox.warning(mensaje, MessageBox.Ignore, MessageBox.Cancel, MessageBox.NoButton, "AbanQ");
        if (res == MessageBox.Ignore) {
          continue;
        } else {
          util.destroyProgressDialog();
          return false;
        }
      }
      curEmitidas.setValueBuffer("cifnif", cifNif);
    } else {
      curEmitidas.setValueBuffer("numidentificacion", cifNif);
    }
    if (!cifNif || cifNif == "") {
      var mensaje = util.translate("scripts", "El N.I.F. El cliente %2 (%3) no tiene Identificador Fiscal asociado.\nPulse Calcelar para cancelar la operación o Ignorar para ignorar este registro de metálico").arg(codCliente).arg(nombreCliente);
      var res = MessageBox.warning(mensaje, MessageBox.Ignore, MessageBox.Cancel, MessageBox.NoButton, "AbanQ");
      if (res == MessageBox.Ignore) {
        continue;
      } else {
        util.destroyProgressDialog();
        return false;
      }
    }
    curEmitidas.setValueBuffer("apellidosnomrs", nombreCliente);
    curEmitidas.setValueBuffer("codpais", codPais);
    if (tipoIdFiscal != "1") {
      tipoIdFiscal = _i.obtenerTipoIdFiscal(tipoIdFiscal);
      if ((tipoIdFiscal != "1" && codPais == "ES") || (tipoIdFiscal == "1" && codPais != "ES")) {
        var res: Number = MessageBox.warning(util.translate("scripts", "Los datos de Tipo de Identificación Fiscal y país del cliente no son coherentes para:\n%1\nPulse Calcelar para cancelar la operación o Ignorar para ignorar este registro de metálico").arg(razonSocial), MessageBox.Ignore, MessageBox.Cancel, MessageBox.NoButton, "AbanQ");
        if (res == MessageBox.Ignore) {
          continue;
        } else {
          util.destroyProgressDialog();
          return false;
        }
      }
    }
    curEmitidas.setValueBuffer("claveidentificacion", tipoIdFiscal);
    curEmitidas.setValueBuffer("tipolibro", "E");
    curEmitidas.setNull("operacion");
    curEmitidas.setNull("fechaexpedicion");
    curEmitidas.setNull("fechaoperacion");
    curEmitidas.setValueBuffer("tipoimpositivo", 0);
    curEmitidas.setValueBuffer("baseimponible", 0);
    curEmitidas.setValueBuffer("cuotaimpuesto", 0);
    curEmitidas.setValueBuffer("importetotal", 0);
    curEmitidas.setValueBuffer("baseimponiblecoste", 0);
    //curEmitidas.setValueBuffer("idenfactura", codFactura);
    //curEmitidas.setValueBuffer("numregistro", numAsiento);
    //curEmitidas.setValueBuffer("numfacturas", 1);
    curEmitidas.setValueBuffer("desgloseregistro", 1);
    curEmitidas.setValueBuffer("tiporecequi", 0);
    curEmitidas.setValueBuffer("cuotarecequi", 0);
    curEmitidas.setValueBuffer("importemetalico", metalico);
    curEmitidas.setValueBuffer("ejerciciometalico", anoF);
    curEmitidas.setValueBuffer("codcliente", codCliente);
    if (!curEmitidas.commitBuffer()) {
      util.destroyProgressDialog();
      return false;
    }
  }
  return true;
}

function oficial_dameFiltroPagoEfectivo()
{
  var cuentas = flcontmode.iface.pub_cuentasMetalico();
  var caja = "pd.codcuenta = '' OR pd.codcuenta IS NULL";
  caja += cuentas != "" ? (" OR pd.codcuenta IN (" + cuentas + ")") : "";
  caja = "(" + caja + ")";
  debug("FPE = " + caja);
  return caja;
}

function oficial_dameFiltroEjerciciosEfectivo()
{
  return "f.fecha >= '2012-01-01'";
}

function oficial_dameWhereEmi(): String {
  var cursor: FLSqlCursor = this.cursor();
  var where: String = "co_asientos.codejercicio = '" + cursor.valueBuffer("codejercicio") + "' AND sc1.idcuentaesp IN ('IVAREP', 'IVAEUE', 'IVARXP', 'IVAREX') AND co_asientos.fecha BETWEEN '" + cursor.valueBuffer("fechainicio") + "' AND '" + cursor.valueBuffer("fechafin") + "'";
  return where;
}

function oficial_limpiarFacturasEmitidas(): Boolean {
  var util: FLUtil = new FLUtil;
  var cursor: FLSqlCursor = this.cursor();

  if (!util.sqlDelete("co_facturasemi340", "idmodelo = " + cursor.valueBuffer("idmodelo")))
  {
    return false;
  }
  return true;
}

function oficial_cargarFacturasRecibidas(): Boolean {
  var util: FLUtil = new FLUtil;
  var cursor: FLSqlCursor = this.cursor();

  var codEjercicio: String = cursor.valueBuffer("codejercicio");
  var idModelo: String = cursor.valueBuffer("idmodelo");

  if (!this.iface.limpiarFacturasRecibidas())
  {
    return false;
  }


  var qryRecibidas: FLSqlQuery = new FLSqlQuery("co_i_facturasrec");
  var where: String = this.iface.dameWhereRec();

  qryRecibidas.setWhere(where);
  qryRecibidas.setForwardOnly(true);
  debug("QWERY 1 :" + qryRecibidas.sql());
  if (!qryRecibidas.exec())
  {
    return false;
  }
  var qryDatosProveedor: FLSqlQuery = new FLSqlQuery;
  qryDatosProveedor.setTablesList("proveedores,dirproveedores,paises");
  qryDatosProveedor.setSelect("p.codiso, pr.tipoidfiscal");
  qryDatosProveedor.setFrom("proveedores pr INNER JOIN dirproveedores dp ON (pr.codproveedor = dp.codproveedor AND dp.direccionppal = true) LEFT OUTER JOIN paises p ON dp.codpais = p.codpais");

  var qryFactura: FLSqlQuery = new FLSqlQuery;
  qryFactura.setTablesList("facturasprov");
  qryFactura.setSelect("codproveedor, nombre, cifnif, idfactura, codigo, deabono, idfacturarect, numproveedor, claveoperacion340, desglose340");
  qryFactura.setFrom("facturasprov");


  var curRecibidas: FLSqlCursor = new FLSqlCursor("co_facturasrec340");
  var cifNif: String;
  var codPais: String;
  var base: Number;
  var cuota: Number;
  var importe: Number;
  var cuotaRecargo: Number;
  var idAsiento: String;
  var idFactura: String;
  var operacion, desglose340;
  var codFacRectificada: String;
  var codFactura: String;
  var razonSocial: String;
  var numAsiento: String;
  var codProveedor: String;
  util.createProgressDialog(util.translate("scripts", "Cargando facturas recibidas..."), qryRecibidas.size());
  var paso: Number = 0;
  var tipoIdFiscal: String;
  var codTipoEspecial: String;
  // lim = Input.getNumber("Tope");
  while (qryRecibidas.next())
  {
    util.setProgress(++paso);
    // if (paso > lim) return true;
    tipoIdFiscal = "1";
    operacion = "";
    idFactura = "";
    codFacRectificada = "";
    idAsiento = qryRecibidas.value("co_asientos.idasiento");
    numAsiento = qryRecibidas.value("co_asientos.numero");
    codTipoEspecial = qryRecibidas.value("sc1.idcuentaesp");

    qryFactura.setWhere("idasiento = " + idAsiento);
    if (!qryFactura.exec()) {
      util.destroyProgressDialog();
      return false;
    }
    if (qryFactura.first() && codTipoEspecial != "IVASIM") {
      codProveedor = qryFactura.value("codproveedor");
      cifNif = qryFactura.value("cifnif");
      idFactura = qryFactura.value("idfactura");
      codFactura = qryFactura.value("numproveedor");
      if (!codFactura || codFactura == "") {
        codFactura = qryFactura.value("codigo");
      }
      operacion = qryFactura.value("claveoperacion340");
      desglose340 = qryFactura.value("desglose340");
      if (qryFactura.value("deabono")) {
        /** Sólo para emitidas
        codFacRectificada = util.sqlSelect("facturasprov", "codigo", "idfactura = " + qryFactura.value("idfacturarect"));
        if (codFacRectificada && codFacRectificada != "") {
          operacion = "D";
        } */
      }
      qryDatosProveedor.setWhere("pr.codproveedor = '" + codProveedor + "'");
      razonSocial = qryFactura.value("nombre");
    } else {
      cifNif = qryRecibidas.value("co_partidas.cifnif");
      var codSubcuentaProv: String = qryRecibidas.value("co_partidas.codcontrapartida");
      codProveedor = util.sqlSelect("co_subcuentasprov", "codproveedor", "codsubcuenta = '" + codSubcuentaProv + "' AND codejercicio = '" + codEjercicio + "'");
      if (!codProveedor) {
        MessageBox.warning(util.translate("scripts", "Error al cargar los datos del asiento %1.\nNo se ha encontrado el proveedor asociado a la subcuenta %2 y el ejercicio %3").arg(numAsiento).arg(codSubcuentaProv).arg(codEjercicio), MessageBox.Ok, MessageBox.NoButton);
        return false;
      }
      qryDatosProveedor.setWhere("pr.codproveedor = '" + codProveedor + "'");
      //        qryDatosProveedor.setWhere("pr.cifnif = '" + cifNif + "'");
      razonSocial = qryRecibidas.value("sc2.descripcion");
      codFactura = qryRecibidas.value("co_partidas.documento");
      idFactura = qryFactura.value("idfactura"); /// Para cuando es IVASIM
    }
    razonSocial = razonSocial.left(40);
    razonSocial = this.iface.formatearTexto340(razonSocial)

    if (!qryDatosProveedor.exec()) {
      util.destroyProgressDialog();
      return false;
    }
    if (qryDatosProveedor.first()) {
      codPais = qryDatosProveedor.value("p.codiso");
      tipoIdFiscal = qryDatosProveedor.value("pr.tipoidfiscal");
    }
    if (!codPais || codPais == "") {
      codPais = "ES";
    }

    curRecibidas.setModeAccess(curRecibidas.Insert);
    curRecibidas.refreshBuffer();
    curRecibidas.setValueBuffer("idmodelo", idModelo);
    if (codPais == "ES") {
      cifNif = flcontmode.iface.pub_limpiarCifNif(cifNif);
      if (cifNif.length > 9) {
        var mensaje: String;
        if (idFactura != "") {
          mensaje = util.translate("scripts", "El N.I.F. %1 de la factura %2 (%3) tiene más de 9 caracteres.\nPulse Calcelar para cancelar la operación o Ignorar para ignorar esta factura").arg(cifNif).arg(codFactura).arg(razonSocial);
        } else {
          mensaje = util.translate("scripts", "El N.I.F. %1 del asiento %2 (%3) tiene más de 9 caracteres.\nPulse Calcelar para cancelar la operación o Ignorar para ignorar esta factura").arg(cifNif).arg(numAsiento).arg(razonSocial);
        }
        var res: Number = MessageBox.warning(mensaje, MessageBox.Cancel, MessageBox.Ignore);
        if (res == MessageBox.Ignore) {
          continue;
        } else {
          util.destroyProgressDialog();
          return false;
        }
      }
      curRecibidas.setValueBuffer("cifnif", cifNif);
    } else {
      curRecibidas.setValueBuffer("numidentificacion", cifNif);
    }
    if (!cifNif || cifNif == "") {
      var mensaje: String;
      if (idFactura != "") {
        mensaje = util.translate("scripts", "La factura %1 (%2) no tiene Identificador Fiscal asociado.\nPulse Calcelar para cancelar la operación o Ignorar para ignorar esta factura").arg(codFactura).arg(razonSocial);
      } else {
        mensaje = util.translate("scripts", "El asiento (%2) no tiene Identificador Fiscal asociado.\nPulse Calcelar para cancelar la operación o Ignorar para ignorar esta factura").arg(numAsiento).arg(razonSocial);
      }
      var res: Number = MessageBox.warning(mensaje, MessageBox.Ignore, MessageBox.Cancel);
      if (res == MessageBox.Ignore) {
        continue;
      } else {
        util.destroyProgressDialog();
        return false;
      }
    }
    curRecibidas.setValueBuffer("apellidosnomrs", razonSocial);
    curRecibidas.setValueBuffer("codpais", codPais);
    if (tipoIdFiscal != "1") {
      tipoIdFiscal = this.iface.obtenerTipoIdFiscal(tipoIdFiscal);
      if ((tipoIdFiscal != "1" && codPais == "ES") || (tipoIdFiscal == "1" && codPais != "ES")) {
        var res: Number = MessageBox.warning(util.translate("scripts", "Los datos de Tipo de Identificación Fiscal y país del proveedor no son coherentes para:\n%1\nFactura / Asiento: %2").arg(razonSocial).arg(idFactura != "" ? codFactura : numAsiento), MessageBox.Ignore, MessageBox.Cancel);
        if (res == MessageBox.Ignore) {
          continue;
        } else {
          util.destroyProgressDialog();
          return false;
        }
      }
    }
    curRecibidas.setValueBuffer("claveidentificacion", tipoIdFiscal);
    curRecibidas.setValueBuffer("tipolibro", "R");
    if (operacion == "") {
      curRecibidas.setNull("operacion");
    } else {
      curRecibidas.setValueBuffer("operacion", operacion);
    }

    /// Clave C (Varios IVA)
    if (operacion == "C" && desglose340) {
      curRecibidas.setValueBuffer("desgloseregistro", desglose340);
    } else {
      curRecibidas.setValueBuffer("desgloseregistro", 1);
    }

    curRecibidas.setValueBuffer("fechaexpedicion", qryRecibidas.value("co_asientos.fecha"));
    curRecibidas.setValueBuffer("fechaoperacion", qryRecibidas.value("co_asientos.fecha"));
    curRecibidas.setValueBuffer("tipoimpositivo", qryRecibidas.value("co_partidas.iva"));
    base = qryRecibidas.value("co_partidas.baseimponible");
    curRecibidas.setValueBuffer("baseimponible", base);
    cuota = qryRecibidas.value("(co_partidas.debe - co_partidas.haber)");
    curRecibidas.setValueBuffer("cuotaimpuesto", cuota);
    importe = parseFloat(base) + parseFloat(cuota);
    curRecibidas.setValueBuffer("importetotal", util.roundFieldValue(importe, "co_facturasemi340", "importetotal"));
    curRecibidas.setValueBuffer("baseimponiblecoste", 0);
    curRecibidas.setValueBuffer("idenfactura", codFactura);
    curRecibidas.setValueBuffer("numregistro", numAsiento);
    curRecibidas.setValueBuffer("numfacturas", 1);
    curRecibidas.setValueBuffer("idasiento", idAsiento);
    if (idFactura && idFactura != "") {
      curRecibidas.setValueBuffer("idfactura", idFactura);
    }
    ctaIvaEsp = qryRecibidas.value("sc1.idcuentaesp");
    switch (ctaIvaEsp) {
      case "IVASUE":
      case "IVASSE": {
        curRecibidas.setValueBuffer("cuotadeducible", cuota);
        break;
      }
    }
    if (!curRecibidas.commitBuffer()) {
      util.destroyProgressDialog();
      return false;
    }
  }
  util.destroyProgressDialog();

  if (!this.iface.cargarVariosIVARec())
  {
    return false;
  }

  return true;
}

function oficial_cargarFacturasRecibidasCaja()
{
  var _i = this.iface;
  var cursor = this.cursor();
  var criterioCaja = true;
  var qryRecibidasCaja = new FLSqlQuery;
  qryRecibidasCaja.setTablesList("proveedores,facturasprov,recibosprov,pagosdevolprov,dirproveedores,paises");
  qryRecibidasCaja.setSelect("proveedores.tipoidfiscal, facturasprov.codserie, facturasprov.codigo,co_asientos.fecha,facturasprov.codproveedor, facturasprov.nombre, facturasprov.cifnif, facturasprov.idfactura, facturasprov.codigo, facturasprov.deabono, facturasprov.idfacturarect, facturasprov.numproveedor, facturasprov.claveoperacion340, facturasprov.desglose340, facturasprov.codpago, recibosprov.importe, pagosdevolprov.fecha, pagosdevolprov.tipo, pagosdevolprov.iban, pagosdevolprov.numerocheque, paises.codiso, co_asientos.numero,co_asientos.codejercicio,co_asientos.idasiento, co_partidas.iva, co_partidas.baseimponible, (co_partidas.debe - co_partidas.haber), co_subcuentas.idcuentaesp");
  qryRecibidasCaja.setFrom("proveedores INNER JOIN facturasprov ON proveedores.codproveedor = facturasprov.codproveedor INNER JOIN recibosprov ON facturasprov.idfactura= recibosprov.idfactura INNER JOIN pagosdevolprov ON recibosprov.idrecibo=pagosdevolprov.idrecibo INNER JOIN dirproveedores ON (proveedores.codproveedor = dirproveedores.codproveedor AND dirproveedores.direccionppal = true) LEFT OUTER JOIN paises ON dirproveedores.codpais = paises.codpais INNER JOIN co_asientos ON co_asientos.idasiento = facturasprov.idasiento INNER JOIN co_partidas ON  co_asientos.idasiento = co_partidas.idasiento INNER JOIN co_subcuentas ON co_partidas.idsubcuenta = co_subcuentas.idsubcuenta ");
  qryRecibidasCaja.setWhere("proveedores.criteriocaja AND pagosdevolprov.primerpago AND pagosdevolprov.fecha BETWEEN '" + cursor.valueBuffer("fechainicio") + "' AND '" + cursor.valueBuffer("fechafin") + "' and co_asientos.codejercicio = '" + cursor.valueBuffer("codejercicio") + "' and co_subcuentas.idcuentaesp IN ('IVASOP', 'IVASUE', 'IVASIM', 'IVASEX', 'IVASSE')");
  debug("QWERY: " + qryRecibidasCaja.sql());
  qryRecibidasCaja.setForwardOnly(true);
  if (!qryRecibidasCaja.exec()) {
    return false;
  }

  var codEjercicio = cursor.valueBuffer("codejercicio");
  var idModelo = cursor.valueBuffer("idmodelo");
  var curRecibidas = new FLSqlCursor("co_facturasrec340");
  var cifNif;
  var codPais;
  var base;
  var cuota;
  var importe;
  var cuotaRecargo;
  var idAsiento;
  var idFactura;
  var operacion, desglose340;
  var codFacRectificada;
  var codFactura;
  var razonSocial;
  var numAsiento;
  var codProveedor;
  var importePago, fechaPago, iban, numeroCheque, codPago, medioPago340;
  AQUtil.createProgressDialog(sys.translate("Cargando facturas recibidas criterio caja..."), qryRecibidasCaja.size());

  var paso = 0;
  var tipoIdFiscal;
  var codTipoEspecial;

  while (qryRecibidasCaja.next()) {
    AQUtil.setProgress(++paso);
    tipoIdFiscal = "1";
    operacion = "";
    idFactura = "";
    codFacRectificada = "";
    idAsiento = qryRecibidasCaja.value("co_asientos.idasiento");
    numAsiento = qryRecibidasCaja.value("co_asientos.numero");
    codProveedor = qryRecibidasCaja.value("facturasprov.codproveedor");
    cifNif = qryRecibidasCaja.value("facturasprov.cifnif");
    idFactura = qryRecibidasCaja.value("facturasprov.idfactura");
    codFactura = qryRecibidasCaja.value("facturasprov.numproveedor");
    if (!codFactura || codFactura == "") {
      codFactura = qryRecibidasCaja.value("facturasprov.codigo");
    }
    operacion = qryRecibidasCaja.value("facturasprov.claveoperacion340");
    desglose340 = qryRecibidasCaja.value("facturasprov.desglose340");
    razonSocial = qryRecibidasCaja.value("facturasprov.nombre");
    razonSocial = razonSocial.left(40);
    razonSocial = _i.formatearTexto340(razonSocial);
    codPais = qryRecibidasCaja.value("paises.codiso");
    tipoIdFiscal = qryRecibidasCaja.value("proveedores.tipoidfiscal");
    if (!codPais || codPais == "") {
      codPais = "ES";
    }
    curRecibidas.setModeAccess(curRecibidas.Insert);
    curRecibidas.refreshBuffer();
    curRecibidas.setValueBuffer("idmodelo", idModelo);
    if (codPais == "ES") {
      cifNif = flcontmode.iface.pub_limpiarCifNif(cifNif);
      if (cifNif.length > 9) {
        var mensaje = sys.translate("El N.I.F. %1 de la factura %2 (%3) tiene más de 9 caracteres.\nPulse Calcelar para cancelar la operación o Ignorar para ignorar esta factura").arg(cifNif).arg(codFactura).arg(razonSocial);
        var res = MessageBox.warning(mensaje, MessageBox.Cancel, MessageBox.Ignore);
        if (res == MessageBox.Ignore) {
          continue;
        } else {
          AQUtil.destroyProgressDialog();
          return false;
        }
      }
      curRecibidas.setValueBuffer("cifnif", cifNif);
    } else {
      curRecibidas.setValueBuffer("numidentificacion", cifNif);
    }
    if (!cifNif || cifNif == "") {
      var mensaje = AQUtil.translate("La factura %1 (%2) no tiene Identificador Fiscal asociado.\nPulse Calcelar para cancelar la operación o Ignorar para ignorar esta factura").arg(codFactura).arg(razonSocial);
      var res = MessageBox.warning(mensaje, MessageBox.Ignore, MessageBox.Cancel);
      if (res == MessageBox.Ignore) {
        continue;
      } else {
        AQUtil.destroyProgressDialog();
        return false;
      }
    }
    curRecibidas.setValueBuffer("apellidosnomrs", razonSocial);
    curRecibidas.setValueBuffer("codpais", codPais);
    if (tipoIdFiscal != "1") {
      tipoIdFiscal = _i.obtenerTipoIdFiscal(tipoIdFiscal);
      if ((tipoIdFiscal != "1" && codPais == "ES") || (tipoIdFiscal == "1" && codPais != "ES")) {
        var res = MessageBox.warning(sys.translate("Los datos de Tipo de Identificación Fiscal y país del proveedor no son coherentes para:\n%1\nFactura / Asiento: %2").arg(razonSocial).arg(idFactura != "" ? codFactura : numAsiento), MessageBox.Ignore, MessageBox.Cancel);
        if (res == MessageBox.Ignore) {
          continue;
        } else {
          AQUtil.destroyProgressDialog();
          return false;
        }
      }
    }
    curRecibidas.setValueBuffer("claveidentificacion", tipoIdFiscal);
    curRecibidas.setValueBuffer("tipolibro", "R");
    if (operacion == "") {
      curRecibidas.setNull("operacion");
    } else {
      curRecibidas.setValueBuffer("operacion", operacion);
    }

    /// Clave C (Varios IVA)
    if (operacion == "C" && desglose340) {
      curRecibidas.setValueBuffer("desgloseregistro", desglose340);
    } else {
      curRecibidas.setValueBuffer("desgloseregistro", 1);
    }

    curRecibidas.setValueBuffer("fechaexpedicion", qryRecibidasCaja.value("co_asientos.fecha"));
    curRecibidas.setValueBuffer("fechaoperacion", qryRecibidasCaja.value("co_asientos.fecha"));
    curRecibidas.setValueBuffer("tipoimpositivo", qryRecibidasCaja.value("co_partidas.iva"));
    base = qryRecibidasCaja.value("co_partidas.baseimponible");
    curRecibidas.setValueBuffer("baseimponible", base);
    cuota = qryRecibidasCaja.value("(co_partidas.debe - co_partidas.haber)");
    curRecibidas.setValueBuffer("cuotaimpuesto", cuota);
    importe = parseFloat(base) + parseFloat(cuota);
    curRecibidas.setValueBuffer("importetotal", AQUtil.roundFieldValue(importe, "co_facturasemi340", "importetotal"));
    curRecibidas.setValueBuffer("baseimponiblecoste", 0);
    curRecibidas.setValueBuffer("idenfactura", codFactura);
    curRecibidas.setValueBuffer("numregistro", numAsiento);
    curRecibidas.setValueBuffer("numfacturas", 1);
    curRecibidas.setValueBuffer("idasiento", idAsiento);
    if (idFactura && idFactura != "") {
      curRecibidas.setValueBuffer("idfactura", idFactura);
    }
    ctaIvaEsp = qryRecibidasCaja.value("co_subcuentas.idcuentaesp");
    switch (ctaIvaEsp) {
      case "IVASUE":
      case "IVASSE": {
        curRecibidas.setValueBuffer("cuotadeducible", cuota);
        break;
      }
    }

    //criterio caja

    importePago = qryRecibidasCaja.value("recibosprov.importe");
    fechaPago = qryRecibidasCaja.value("pagosdevolprov.fecha");
    iban = qryRecibidasCaja.value("pagosdevolprov.iban");
    numeroCheque = qryRecibidasCaja.value("pagosdevolprov.numerocheque");
    codPago = qryRecibidasCaja.value("facturasprov.codpago");
    medioPago340 = AQUtil.sqlSelect("formaspago", "mediopago340", "codpago='" + codPago + "' ");
    curRecibidas.setValueBuffer("mediopago", medioPago340);
    switch (medioPago340) {
      case "C" : {
        curRecibidas.setValueBuffer("cuentabancaria", iban);
        break;
      }
      case "T" :
      case "O" : {
        curRecibidas.setValueBuffer("cuentabancaria", numeroCheque);
        break;
      }
    }
    curRecibidas.setValueBuffer("importepagado", importePago);
    curRecibidas.setValueBuffer("fechapago", fechaPago);
    if (!curRecibidas.commitBuffer()) {
      AQUtil.destroyProgressDialog();
      return false;
    }
  }


  AQUtil.destroyProgressDialog();

  if (!_i.cargarVariosIVARec()) {
    return false;
  }
  return true;
}

/** \C Pasa un texto a mayúsculas y elimina las tildes y caracteres no válidos
@param texto: Texto a formatear
@return Texto formateado
\end */
function oficial_formatearTexto340(texto: String): String {
  if (!texto || texto == "")
  {
    return texto;
  }
  var carValidos: String = " &,-.0123456789:;ABCDEFGHIJKLMNOPQRSTUVWXYZ_ÇÑ/'()";
  var textoMay: String = texto.toUpperCase();
  var resultado: String = "";
  var caracter: String;

  for (var i: Number = 0; i < textoMay.length; i++)
  {
    caracter = textoMay.charAt(i);
    switch (caracter) {
      case "Á":
      case "À": {
        resultado += "A";
        break;
      }
      case "É":
      case "È": {
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
      case "Ù": {
        resultado += "U";
        break;
      }
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


function oficial_dameWhereRec(): String {
  var cursor: FLSqlCursor = this.cursor();
  var where: String = "co_asientos.codejercicio = '" + cursor.valueBuffer("codejercicio") + "' AND sc1.idcuentaesp IN ('IVASOP', 'IVASUE', 'IVASIM', 'IVASEX', 'IVASSE') AND co_asientos.fecha BETWEEN '" + cursor.valueBuffer("fechainicio") + "' AND '" + cursor.valueBuffer("fechafin") + "'";
  return where;
}


function oficial_cargarVariosIVAEmi()
{
  return true; /// Ya se hace en las facturas directamente.

  var util: FLUtil = new FLUtil;
  var cursor: FLSqlCursor = this.cursor();

  var idModelo: String = cursor.valueBuffer("idmodelo");

  var qryEmitidas: FLSqlQuery = new FLSqlQuery("co_i_facturasemi");
  qryEmitidas.setSelect("co_asientos.idasiento, COUNT(co_partidas.idpartida)");
  var where: String = this.iface.dameWhereEmi() + " GROUP BY co_asientos.idasiento HAVING COUNT(co_partidas.idpartida) > 1";

  qryEmitidas.setWhere(where);
  qryEmitidas.setForwardOnly(true);
  if (!qryEmitidas.exec()) {
    return false;
  }
  var curEmitidas: FLSqlCursor = new FLSqlCursor("co_facturasemi340");
  util.createProgressDialog(util.translate("scripts", "Marcando facturas emitidas con varios tipos impositivos..."), qryEmitidas.size());
  var paso: Number = 0;
  while (qryEmitidas.next()) {
    util.setProgress(++paso);
    curEmitidas.select("idmodelo = " + idModelo + " AND idasiento = " + qryEmitidas.value("co_asientos.idasiento"));
    while (curEmitidas.next()) {
      curEmitidas.setModeAccess(curEmitidas.Edit);
      curEmitidas.refreshBuffer();
      curEmitidas.setValueBuffer("desgloseregistro", qryEmitidas.value("COUNT(co_partidas.idpartida)"));
      curEmitidas.setValueBuffer("operacion", "C");
      if (!curEmitidas.commitBuffer()) {
        util.destroyProgressDialog();
        return false;
      }
    }
  }
  util.destroyProgressDialog();

  return true;
}

function oficial_cargarVariosIVARec(): Boolean {
  return true; /// Ya se hace directamente en facturas de proveedor

  var util: FLUtil = new FLUtil;
  var cursor: FLSqlCursor = this.cursor();

  var idModelo: String = cursor.valueBuffer("idmodelo");

  var qryRecibidas: FLSqlQuery = new FLSqlQuery("co_i_facturasrec");
  qryRecibidas.setSelect("co_asientos.idasiento, COUNT(co_partidas.idpartida)");
  var where: String = this.iface.dameWhereRec() + " GROUP BY co_asientos.idasiento HAVING COUNT(co_partidas.idpartida) > 1";

  qryRecibidas.setWhere(where);
  qryRecibidas.setForwardOnly(true);
  if (!qryRecibidas.exec())
  {
    return false;
  }
  var curRecibidas: FLSqlCursor = new FLSqlCursor("co_facturasrec340");
  util.createProgressDialog(util.translate("scripts", "Marcando facturas recibidas con varios tipos impositivos..."), qryRecibidas.size());
  var paso: Number = 0;
  while (qryRecibidas.next())
  {
    util.setProgress(++paso);
    curRecibidas.select("idmodelo = " + idModelo + " AND idasiento = " + qryRecibidas.value("co_asientos.idasiento"));
    while (curRecibidas.next()) {
      curRecibidas.setModeAccess(curRecibidas.Edit);
      curRecibidas.refreshBuffer();
      curRecibidas.setValueBuffer("desgloseregistro", qryRecibidas.value("COUNT(co_partidas.idpartida)"));
      curRecibidas.setValueBuffer("operacion", "C");
      if (!curRecibidas.commitBuffer()) {
        util.destroyProgressDialog();
        return false;
      }
    }
  }
  util.destroyProgressDialog();

  return true;
}

function oficial_limpiarFacturasRecibidas(): Boolean {
  var util: FLUtil = new FLUtil;
  var cursor: FLSqlCursor = this.cursor();

  if (!util.sqlDelete("co_facturasrec340", "idmodelo = " + cursor.valueBuffer("idmodelo")))
  {
    return false;
  }
  return true;
}

function oficial_tbnVerFacturaEmi_clicked()
{
  var cursor: FLSqlCursor = this.cursor();
  var util: FLUtil = new FLUtil();
  var idFactura: String = this.child("tdbFacturasEmitidas").cursor().valueBuffer("idfactura");
  if (!idFactura) {
    return false;
  }
  var curFactura: FLSqlCursor = new FLSqlCursor("facturascli");
  curFactura.select("idfactura = " + idFactura);
  if (!curFactura.first()) {
    return false;
  }
  curFactura.browseRecord();
}

function oficial_tbnVerRecibosMetalico_clicked()
{
  var _i = this.iface;
  var util = new FLUtil;
  var cursor = this.cursor();
  var curEmi = this.child("tdbFacturasEmitidas").cursor();
  var metalico = curEmi.valueBuffer("importemetalico");
  if (!metalico) {
    MessageBox.warning(util.translate("scripts", "El registro seleccionado no contiene cobros en metálico"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton, "AbanQ");
    return;
  }
  var codCliente = curEmi.valueBuffer("codcliente");
  var codEjercicio = cursor.valueBuffer("codejercicio");
  var codEjercicioF = curEmi.valueBuffer("ejerciciometalico");
  var fInicio = util.sqlSelect("ejercicios", "fechainicio", "codejercicio = '" + codEjercicio + "'");
  var filtroPagoEfectivo = _i.dameFiltroPagoEfectivo();
  var f = new FLFormSearchDB("reciboscli");
  var c = f.cursor();
  c.setMainFilter("idrecibo IN (SELECT r.idrecibo FROM facturascli f INNER JOIN reciboscli r ON f.idfactura = r.idfactura INNER JOIN pagosdevolcli pd ON r.idrecibo = pd.idrecibo INNER JOIN co_asientos a ON pd.idasiento = a.idasiento WHERE f.codcliente = '" + codCliente + "' AND a.codejercicio = '" + codEjercicio + "' AND pd.fecha BETWEEN '" + fInicio + "' AND '" + cursor.valueBuffer("fechafin") + "' AND f.codejercicio = '" + codEjercicioF + "' AND " + filtroPagoEfectivo + ")");
  f.setMainWidget();
  f.exec();
}

function oficial_tbnVerAsientoEmi_clicked()
{
  var cursor: FLSqlCursor = this.cursor();
  var util: FLUtil = new FLUtil();
  var idAsiento: String = this.child("tdbFacturasEmitidas").cursor().valueBuffer("idasiento");
  if (!idAsiento) {
    return false;
  }
  var curAsiento: FLSqlCursor = new FLSqlCursor("co_asientos");
  curAsiento.select("idasiento = " + idAsiento);
  if (!curAsiento.first()) {
    return false;
  }
  curAsiento.browseRecord();
}

function oficial_tbnVerFacturaRec_clicked()
{
  var cursor: FLSqlCursor = this.cursor();
  var util: FLUtil = new FLUtil();
  var idFactura: String = this.child("tdbFacturasRecibidas").cursor().valueBuffer("idfactura");
  if (!idFactura) {
    return false;
  }
  var curFactura: FLSqlCursor = new FLSqlCursor("facturasprov");
  curFactura.select("idfactura = " + idFactura);
  if (!curFactura.first()) {
    return false;
  }
  curFactura.browseRecord();
}

function oficial_tbnVerAsientoRec_clicked()
{
  var cursor: FLSqlCursor = this.cursor();
  var util: FLUtil = new FLUtil();
  var idAsiento: String = this.child("tdbFacturasRecibidas").cursor().valueBuffer("idasiento");
  if (!idAsiento) {
    return false;
  }
  var curAsiento: FLSqlCursor = new FLSqlCursor("co_asientos");
  curAsiento.select("idasiento = " + idAsiento);
  if (!curAsiento.first()) {
    return false;
  }
  curAsiento.browseRecord();
}

function oficial_obtenerTipoIdFiscal(tipoIdFiscal: String): String {
  var valor: String = "1";
  switch (tipoIdFiscal)
  {
    case "NIF": {
      valor = "1";
      break;
    }
    case "NIF/IVA": {
      valor = "2";
      break;
    }
    case "Pasaporte": {
      valor = "3";
      break;
    }
    case "Doc.Oficial País": {
      valor = "4";
      break;
    }
    case "Cert.Residencia": {
      valor = "5";
      break;
    }
    case "Otro": {
      valor = "6";
      break;
    }
  }
  return valor;
}
//// OFICIAL /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////

//// DESARROLLO /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
