var form = this;
/***************************************************************************
                 co_modelo303.qs  -  description
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

/** \C
El modelo 300 recoge la información relativa a las declaraciones-liquidaciones trimestrales de IVA.
Restricciones del modelo: El proceso actual únicamente calcula los valores descritos en este documento. El resto de valores debe ser introducido por el usuario de forma manual.
Datos necesarios: En las partidas de asientos de contabilidad relativas a subcuentas de IVA devengado y deducible (subcuentas que derivan de cuentas marcadas como IVAREP e IVASOP), deben estar correctamente informados los campos relativos a base imponible, porcentaje de IVA y porcentaje de recargo de equivalencia.
\end */

/** @class_declaration interna */
////////////////////////////////////////////////////////////////////////////
//// DECLARACION ///////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////
//// INTERNA /////////////////////////////////////////////////////
class interna
{
  var ctx: Object;
  function interna(context)
  {
    this.ctx = context;
  }
  function init()
  {
    return this.ctx.interna_init();
  }
  function calculateField(fN)
  {
    return this.ctx.interna_calculateField(fN);
  }
  function validateForm()
  {
    return this.ctx.interna_validateForm();
  }
  function calculateField2009(fN)
  {
    return this.ctx.interna_calculateField2009(fN);
  }
  function calculateField2014(fN)
  {
    return this.ctx.interna_calculateField2014(fN);
  }
}
//// INTERNA /////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/** @class_declaration oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
class oficial extends interna
{
  var ejercicio;
  var curPartida_;
  var whereFechas_;
  function oficial(context)
  {
    interna(context);
  }
  function bufferChanged(fN)
  {
    return this.ctx.oficial_bufferChanged(fN);
  }
  function calcularValores()
  {
    this.ctx.oficial_calcularValores();
  }
  function calcularValores2009()
  {
    this.ctx.oficial_calcularValores2009();
  }
  function calcularValores2014()
  {
    this.ctx.oficial_calcularValores2014();
  }
  function establecerFechasPeriodo()
  {
    return this.ctx.oficial_establecerFechasPeriodo();
  }
  function comprobarFechas()
  {
    return this.ctx.oficial_comprobarFechas();
  }
  function bufferChanged2009(fN)
  {
    return this.ctx.oficial_bufferChanged2009(fN);
  }
  function bufferChanged2014(fN)
  {
    return this.ctx.oficial_bufferChanged2014(fN);
  }
  function habilitarPeriodo()
  {
    return this.ctx.oficial_habilitarPeriodo();
  }
  function calcularCasillas01a09()
  {
    return this.ctx.oficial_calcularCasillas01a09();
  }
  function calcularCasillas10a11()
  {
    return this.ctx.oficial_calcularCasillas10a11();
  }
  function calcularCasillas12a13()
  {
    return this.ctx.oficial_calcularCasillas12a13();
  }
  function calcularCasillas14a15()
  {
    return this.ctx.oficial_calcularCasillas14a15();
  }
  function calcularCasillas16a24()
  {
    return this.ctx.oficial_calcularCasillas16a24();
  }
  function calcularCasillas25a26()
  {
    return this.ctx.oficial_calcularCasillas25a26();
  }
  function calcularCasillas28a29()
  {
    return this.ctx.oficial_calcularCasillas28a29();
  }
  function calcularCasillas30a31()
  {
    return this.ctx.oficial_calcularCasillas30a31();
  }
  function calcularCasillas32a33()
  {
    return this.ctx.oficial_calcularCasillas32a33();
  }
  function calcularCasillas34a35()
  {
    return this.ctx.oficial_calcularCasillas34a35();
  }
  function calcularCasillas36a37()
  {
    return this.ctx.oficial_calcularCasillas36a37();
  }
  function calcularCasillas38a39()
  {
    return this.ctx.oficial_calcularCasillas38a39();
  }
  function calcularCasillas40a41()
  {
    return this.ctx.oficial_calcularCasillas40a41();
  }
  function calcularCasillas42()
  {
    return this.ctx.oficial_calcularCasillas42();
  }
  function calcularCasillas43()
  {
    return this.ctx.oficial_calcularCasillas43();
  }
  function calcularCasillas44()
  {
    return this.ctx.oficial_calcularCasillas44();
  }
  function calcularCasillas59()
  {
    return this.ctx.oficial_calcularCasillas59();
  }
  function calcularCasillas60()
  {
    return this.ctx.oficial_calcularCasillas60();
  }
  function calcularCasillas61()
  {
    return this.ctx.oficial_calcularCasillas61();
  }
  function calcularCasillas62a63()
  {
    return this.ctx.oficial_calcularCasillas62a63();
  }
  function calcularCasillas74a75()
  {
    return this.ctx.oficial_calcularCasillas74a75();
  }
  function revisarFacturas()
  {
    return this.ctx.oficial_revisarFacturas();
  }
  function dameTipoBienes(idAsiento)
  {
    return this.ctx.oficial_dameTipoBienes(idAsiento);
  }
  function actualizarCasilla303Partida(idPartida, casilla303)
  {
    return this.ctx.oficial_actualizarCasilla303Partida(idPartida, casilla303);
  }
  function conectarDetalles()
  {
    return this.ctx.oficial_conectarDetalles();
  }
  function partidasDatosRG1()
  {
    return this.ctx.oficial_partidasDatosRG1();
  }
  function partidasDatosRG2()
  {
    return this.ctx.oficial_partidasDatosRG2();
  }
  function partidasDatosRG3()
  {
    return this.ctx.oficial_partidasDatosRG3();
  }
  function partidasDatosRE1()
  {
    return this.ctx.oficial_partidasDatosRE1();
  }
  function partidasDatosRE2()
  {
    return this.ctx.oficial_partidasDatosRE2();
  }
  function partidasDatosRE3()
  {
    return this.ctx.oficial_partidasDatosRE3();
  }
  function partidasDatosIVADevAI()
  {
    return this.ctx.oficial_partidasDatosIVADevAI();
  }
  function partidasDatosIVADedOIBC()
  {
    return this.ctx.oficial_partidasDatosIVADedOIBC();
  }
  function partidasDatosIVADedOIBI()
  {
    return this.ctx.oficial_partidasDatosIVADedOIBI();
  }
  function partidasDatosIVADedImBC()
  {
    return this.ctx.oficial_partidasDatosIVADedImBC();
  }
  function partidasDatosIVADedImBI()
  {
    return this.ctx.oficial_partidasDatosIVADedImBI();
  }
  function partidasDatosIVADedAIBC()
  {
    return this.ctx.oficial_partidasDatosIVADedAIBC();
  }
  function partidasDatosIVADedAIBI()
  {
    return this.ctx.oficial_partidasDatosIVADedAIBI();
  }
  function partidasDatosIVAComRe()
  {
    return this.ctx.oficial_partidasDatosIVAComRe();
  }
  function partidasDatosEUE()
  {
    return this.ctx.oficial_partidasDatosEUE();
  }
  function partidasDatosRXP()
  {
    return this.ctx.oficial_partidasDatosRXP();
  }
  function partidasDatosREX()
  {
    return this.ctx.oficial_partidasDatosREX();
  }
  function mostrarPartidas(filtro)
  {
    return this.ctx.oficial_mostrarPartidas(filtro);
  }
  function limpiarValores()
  {
    return this.ctx.oficial_limpiarValores();
  }
  function limpiarValores2014()
  {
    return this.ctx.oficial_limpiarValores2014();
  }
  function actualizarWhereFechas()
  {
    return this.ctx.oficial_actualizarWhereFechas();
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
  var _i = this.iface;
  var cursor = this.cursor();

  connect(cursor, "bufferChanged(QString)", _i, "bufferChanged");
  connect(this.child("pbnCalcularValores"), "clicked()", _i, "calcularValores()");

  if (cursor.modeAccess() == cursor.Insert) {
    this.child("fdbCodEjercicio").setValue(flfactppal.iface.pub_ejercicioActual());
    var municipio = AQUtil.sqlSelect("co_datosfiscales", "municipio", "1 = 1");
    if (municipio) {
      this.child("fdbLocalidadFirma").setValue(municipio);
    }
  }

  _i.habilitarPeriodo();
  _i.conectarDetalles();
  _i.actualizarWhereFechas();
  //  _i.bloqueoPago = false;
}

function interna_calculateField(fN)
{
  var valor;
  var _i = this.iface;
  var cursor = this.cursor();
  var fecha = parseFloat(cursor.valueBuffer("fechainicio"));
  _i.ejercicio = fecha.toString().left(4);


  switch (_i.ejercicio) {
    default: {
      valor = _i.calculateField2014(fN);
      break;
    }
  }
  return valor;
}

function interna_calculateField2009(fN)
{
  var _i = this.iface;
  var cursor = this.cursor();
  var valor;
  switch (fN) {


    case "cuotadevtotal": {
      valor = parseFloat(cursor.valueBuffer("cuotarg1")) + parseFloat(cursor.valueBuffer("cuotarg2")) + parseFloat(cursor.valueBuffer("cuotarg3")) + parseFloat(cursor.valueBuffer("cuotare1")) + parseFloat(cursor.valueBuffer("cuotare2")) + parseFloat(cursor.valueBuffer("cuotare3")) + parseFloat(cursor.valueBuffer("cuotaai"));
      break;
    }
    case "cuotadedtotal": {
      valor = parseFloat(cursor.valueBuffer("cuotadedoibc")) + parseFloat(cursor.valueBuffer("cuotadedoibi")) + parseFloat(cursor.valueBuffer("cuotadedimbc")) + parseFloat(cursor.valueBuffer("cuotadedimbi")) + parseFloat(cursor.valueBuffer("cuotadedaibc")) + parseFloat(cursor.valueBuffer("cuotadedaibi")) + parseFloat(cursor.valueBuffer("cuotacomre")) + parseFloat(cursor.valueBuffer("cuotaregin")) + parseFloat(cursor.valueBuffer("cuotaregapli"));
      break;
    }
    case "cuotadif": {
      valor = parseFloat(cursor.valueBuffer("cuotadevtotal")) - parseFloat(cursor.valueBuffer("cuotadedtotal"));
      break;
    }
    case "cuotaestado": {
      valor = parseFloat(cursor.valueBuffer("cuotadif")) * parseFloat(cursor.valueBuffer("porcuotaestado")) / 100;
      break;
    }
    case "cuotaresultado": {
      valor = parseFloat(cursor.valueBuffer("cuotaestado")) - parseFloat(cursor.valueBuffer("cuotaanterior")) + parseFloat(cursor.valueBuffer("sujetospasivos"));
      break;
    }
    case "resliquid": {
      valor = parseFloat(cursor.valueBuffer("cuotaresultado")) - parseFloat(cursor.valueBuffer("adeducircompl"));
      break;
    }
    case "importei": {
      var resLiquid = parseFloat(cursor.valueBuffer("resliquid"));
      if (resLiquid > 0) {
        valor = resLiquid
      } else {
        valor = 0;
      }
      break;
    }
    case "imported": {
      var resLiquid = parseFloat(cursor.valueBuffer("resliquid"));
      if (resLiquid < 0) {
        valor = (resLiquid * -1) - parseFloat(cursor.valueBuffer("impcompensar"));
      } else {
        valor = 0;
      }
      break;
    }
    //    case "cuotaanterior":
    /** \C --cuotaanterior--: Suma de los saldos de las partidas correspondientes a la subcuenta de IVA compensado seleccionada, correspondientes al ejercicio seleccionado y anteriores a la fecha de fin del trimestre o período seleccionado
    \end */
    //      var fechaFin:Date = this.child("fdbFechaFin").value();
    //      var codEjercicio = this.child("fdbCodEjercicio").value();
    //      var idSubcuenta = this.child("fdbIdSubcuentaCA").value();
    //      var q = new FLSqlQuery();
    //      q.setTablesList("co_cuentas,co_subcuentas,co_asientos,co_partidas");
    //      q.setSelect("SUM(p.debe) - SUM(p.haber)");
    //      q.setFrom("co_cuentas c INNER JOIN co_subcuentas s ON c.idcuenta = s.idcuenta" +
    //          " INNER JOIN co_partidas p ON s.idsubcuenta = p.idsubcuenta" +
    //          " INNER JOIN co_asientos a ON p.idasiento = a.idasiento");
    //      q.setWhere("c.codejercicio = '" + codEjercicio + "'" +
    //          " AND a.fecha <= '" + fechaFin + "'" +
    //          " AND s.idsubcuenta = " + idSubcuenta);
    //      if (!q.exec()) return "";
    //      if (!q.first()) return "";
    //      valor = q.value(0);
    //      break;

    //    case "cuotarg1":
    //      valor = parseFloat(this.child("fdbTipoRG0").value()) *
    //        parseFloat(this.child("fdbBaseImponibleRG0").value()) / 100;
    //      break;
    //
    //    case "cuotarg2":
    //      valor = parseFloat(this.child("fdbTipoRG1").value()) *
    //        parseFloat(this.child("fdbBaseImponibleRG1").value()) / 100;
    //      break;
    //
    //    case "cuotarg3":
    //      valor = parseFloat(this.child("fdbTipoRG2").value()) *
    //        parseFloat(this.child("fdbBaseImponibleRG2").value()) / 100;
    //      break;
    //
    //    case "cuotare1":
    //      valor = parseFloat(this.child("fdbTipoRE0").value()) *
    //        parseFloat(this.child("fdbBaseImponibleRE0").value()) / 100;
    //      break;
    //
    //    case "cuotare2":
    //      valor = parseFloat(this.child("fdbTipoRE1").value()) *
    //        parseFloat(this.child("fdbBaseImponibleRE1").value()) / 100;
    //      break;
    //
    //    case "cuotare3":
    //      valor = parseFloat(this.child("fdbTipoRE2").value()) *
    //        parseFloat(this.child("fdbBaseImponibleRE2").value()) / 100;
    //      break;

    case "dcdev": {
      var entidad = cursor.valueBuffer("ctaentidaddev");
      var agencia = cursor.valueBuffer("ctaagenciadev");
      var cuenta = cursor.valueBuffer("cuentadev");
      if (!entidad.isEmpty() && !agencia.isEmpty() && ! cuenta.isEmpty() && entidad.length == 4 && agencia.length == 4 && cuenta.length == 10) {
        var dc1 = AQUtil.calcularDC(entidad + agencia);
        var dc2 = AQUtil.calcularDC(cuenta);
        valor = dc1 + dc2;
      }
      break;
    }
    case "dcingreso": {
      var entidad = cursor.valueBuffer("ctaentidadingreso");
      var agencia = cursor.valueBuffer("ctaagenciaingreso");
      var cuenta = cursor.valueBuffer("cuentaingreso");
      if (!entidad.isEmpty() && !agencia.isEmpty() && ! cuenta.isEmpty() && entidad.length == 4 && agencia.length == 4 && cuenta.length == 10) {
        var dc1 = AQUtil.calcularDC(entidad + agencia);
        var dc2 = AQUtil.calcularDC(cuenta);
        valor = dc1 + dc2;
      }
      break;
    }

    //    case "pagoefectivo":
    //      if (cursor.valueBuffer("pagocuenta"))
    //        valor = false;
    //      break;
    //
    //    case "pagocuenta":
    //      if (cursor.valueBuffer("pagoefectivo"))
    //        valor = false;
    //      break;
  }
  return valor;
}
function interna_calculateField2014(fN)
{
  var _i = this.iface;
  var cursor = this.cursor();
  var valor;
  switch (fN) {
    case "cuotadevtotal": {
      valor = parseFloat(cursor.valueBuffer("cuotarg1")) + parseFloat(cursor.valueBuffer("cuotarg2")) + parseFloat(cursor.valueBuffer("cuotarg3")) + parseFloat(cursor.valueBuffer("cuotaai")) + parseFloat(cursor.valueBuffer("cuotaoo")) + parseFloat(cursor.valueBuffer("cuotambc")) + parseFloat(cursor.valueBuffer("cuotare1")) + parseFloat(cursor.valueBuffer("cuotare2")) + parseFloat(cursor.valueBuffer("cuotare3")) + parseFloat(cursor.valueBuffer("cuotambcre"));
      break;
    }
    case "cuotadedtotal": {
      valor = parseFloat(cursor.valueBuffer("cuotadedoibc")) + parseFloat(cursor.valueBuffer("cuotadedoibi")) + parseFloat(cursor.valueBuffer("cuotadedimbc")) + parseFloat(cursor.valueBuffer("cuotadedimbi")) + parseFloat(cursor.valueBuffer("cuotadedaibc")) + parseFloat(cursor.valueBuffer("cuotadedaibi")) + parseFloat(cursor.valueBuffer("cuotarecded")) + parseFloat(cursor.valueBuffer("cuotacomre")) + parseFloat(cursor.valueBuffer("cuotaregin")) + parseFloat(cursor.valueBuffer("cuotaregapli"));
      break;
    }
    case "cuotadif": {
      valor = parseFloat(cursor.valueBuffer("cuotadevtotal")) - parseFloat(cursor.valueBuffer("cuotadedtotal"));
      break;
    }
    case "cuotaestado": {
      valor = parseFloat(cursor.valueBuffer("cuotadif")) * parseFloat(cursor.valueBuffer("porcuotaestado")) / 100;
      break;
    }
    case "cuotaresultado": {
      valor = parseFloat(cursor.valueBuffer("cuotaestado")) - parseFloat(cursor.valueBuffer("cuotaanterior")) + parseFloat(cursor.valueBuffer("sujetospasivos"));
      break;
    }
    case "resliquid": {
      valor = parseFloat(cursor.valueBuffer("cuotaresultado")) - parseFloat(cursor.valueBuffer("adeducircompl"));
      break;
    }
    case "importei": {
      var resLiquid = parseFloat(cursor.valueBuffer("resliquid"));
      if (resLiquid > 0) {
        valor = resLiquid
      } else {
        valor = 0;
      }
      break;
    }
    case "imported": {
      var resLiquid = parseFloat(cursor.valueBuffer("resliquid"));
      if (resLiquid < 0) {
        valor = (resLiquid * -1) - parseFloat(cursor.valueBuffer("impcompensar"));
      } else {
        valor = 0;
      }
      break;
    }
    case "dcdev": {
      var entidad = cursor.valueBuffer("ctaentidaddev");
      var agencia = cursor.valueBuffer("ctaagenciadev");
      var cuenta = cursor.valueBuffer("cuentadev");
      if (!entidad.isEmpty() && !agencia.isEmpty() && ! cuenta.isEmpty() && entidad.length == 4 && agencia.length == 4 && cuenta.length == 10) {
        var dc1 = AQUtil.calcularDC(entidad + agencia);
        var dc2 = AQUtil.calcularDC(cuenta);
        valor = dc1 + dc2;
      }
      break;
    }
    case "dcingreso": {
      var entidad = cursor.valueBuffer("ctaentidadingreso");
      var agencia = cursor.valueBuffer("ctaagenciaingreso");
      var cuenta = cursor.valueBuffer("cuentaingreso");
      if (!entidad.isEmpty() && !agencia.isEmpty() && ! cuenta.isEmpty() && entidad.length == 4 && agencia.length == 4 && cuenta.length == 10) {
        var dc1 = AQUtil.calcularDC(entidad + agencia);
        var dc2 = AQUtil.calcularDC(cuenta);
        valor = dc1 + dc2;
      }
      break;
    }
    case "sumaresultados": {
      valor = parseFloat(cursor.valueBuffer("cuotadif"));
      break;
    }
  }
  return valor;
}

function interna_validateForm()
{
  var _i = this.iface;
  var cursor = this.cursor();

  /** \C Las fechas que definen el período deben ser coherentes (fin > inicio) y pertenecer al ejercicio seleccionado
  \end */
  if (!_i.comprobarFechas()) {
    return false;
  }

  /// A petición de Barnaplant, porque están inscritos en el registro de devolución mensual
  //  if (cursor.valueBuffer("idtipodec") == "D") {
  //    if (cursor.valueBuffer("tipoperiodo") == "Trimestre" && cursor.valueBuffer("trimestre") != "4T") {
  //      MessageBox.warning(sys.translate("Sólo puede marcar la declaración como A devolver (D) en el cuarto trimestre (4T)"), MessageBox.Ok, MessageBox.NoButton);
  //      return false;
  //    }
  //    if (cursor.valueBuffer("tipoperiodo") == "Mes" && cursor.valueBuffer("mes") != "Diciembre") {
  //      MessageBox.warning(sys.translate("Sólo puede marcar la declaración como A devolver (D) en el últim mes (Diciembre)"), MessageBox.Ok, MessageBox.NoButton);
  //      return false;
  //    }
  //  }

  return true;
}
//// INTERNA /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition oficial */
//////////////////////////////////////////////////////////////////
//// OFICIAL /////////////////////////////////////////////////////
function oficial_bufferChanged(fN)
{
  var _i = this.iface;
  var cursor = this.cursor();
  var fecha = parseFloat(cursor.valueBuffer("fechainicio"));
  _i.ejercicio = fecha.toString().left(4);

  switch (_i.ejercicio) {
    default: {
      _i.bufferChanged2014(fN);
      break;
    }
  }
}

function oficial_bufferChanged2009(fN)
{
  var _i = this.iface;
  var cursor = this.cursor();
  switch (fN) {
    case "cuotarg1":
    case "cuotarg2":
    case "cuotarg3":
    case "cuotare1":
    case "cuotare2":
    case "cuotare3":
    case "cuotaai": {
      this.child("fdbCuotaDevTotal").setValue(_i.calculateField("cuotadevtotal"));
      break;
    }
    case "cuotadedoibc":
    case "cuotadedoibi":
    case "cuotadedimbc":
    case "cuotadedimbi":
    case "cuotadedaibc":
    case "cuotadedaibi":
    case "cuotacomre":
    case "cuotaregin":
    case "cuotaregapli": {
      this.child("fdbCuotaDedTotal").setValue(_i.calculateField("cuotadedtotal"));
      break;
    }
    case "cuotadedtotal":
    case "cuotadevtotal": {
      this.child("fdbCuotaDif").setValue(_i.calculateField("cuotadif"));
      break;
    }
    case "cuotadif":
    case "porcuotaestado": {
      this.child("fdbCuotaEstado").setValue(_i.calculateField("cuotaestado"));
      break;
    }
    case "cuotaestado":
    case "cuotaanterior":
    case "sujetospasivos": {
      this.child("fdbCuotaResultado").setValue(_i.calculateField("cuotaresultado"));
      break;
    }
    case "cuotaresultado":
    case "adeducircompl": {
      this.child("fdbResultadoLiquidacion").setValue(_i.calculateField("resliquid"));
      break;
    }
    case "resliquid": {
      this.child("fdbImported").setValue(_i.calculateField("imported"));
      this.child("fdbImporteI").setValue(_i.calculateField("importei"));
      break;
    }
    case "impcompensar": {
      this.child("fdbImported").setValue(_i.calculateField("imported"));
      break;
    }
    case "fechainicio":
    case "fechafin": {
      _i.limpiarValores();
      break;
    }
    case "tipoperiodo": {
      _i.habilitarPeriodo();
      _i.establecerFechasPeriodo();
    }
    case "mes":
    case "trimestre": {
      _i.establecerFechasPeriodo();
      break;
    }
    case "codcuentaingreso":
    case "ctaentidadingreso":
    case "ctaagenciaingreso":
    case "cuentaingreso": {
      this.child("fdbDcIngreso").setValue(_i.calculateField("dcingreso"));
      break;
    }
    case "codcuentaingreso":
    case "ctaentidadingreso":
    case "ctaagenciaingreso":
    case "cuentaingreso": {
      this.child("fdbDcIngreso").setValue(_i.calculateField("dcingreso"));
      break;
    }
    case "codcuentadev":
    case "ctaentidaddev":
    case "ctaagenciadev":
    case "cuentadev": {
      this.child("fdbDcDev").setValue(_i.calculateField("dcdev"));
      break;
    }
  }
  return;

  //    case "baseimponiblerg1":
  //    case "tiporg1":
  //      this.child( "fdbCuotaRG0" ).setValue( _i.calculateField( "cuotarg1" ) );
  //      break;
  //
  //    case "baseimponiblerg2":
  //    case "tiporg2":
  //      this.child( "fdbCuotaRG1" ).setValue( _i.calculateField( "cuotarg2" ) );
  //      break;
  //
  //    case "baseimponiblerg3":
  //    case "tiporg3":
  //      this.child( "fdbCuotaRG2" ).setValue( _i.calculateField( "cuotarg3" ) );
  //      break;
  //
  //    case "baseimponiblere1":
  //    case "tipore1":
  //      this.child( "fdbCuotaRE0" ).setValue( _i.calculateField( "cuotare1" ) );
  //      break;
  //
  //    case "baseimponiblere2":
  //    case "tipore2":
  //      this.child( "fdbCuotaRE1" ).setValue( _i.calculateField( "cuotare2" ) );
  //      break;
  //
  //    case "baseimponiblere3":
  //    case "tipore3":
  //      this.child( "fdbCuotaRE2" ).setValue( _i.calculateField( "cuotare3" ) );
  //      break;
  //
  //    case "sujetospasivos":
  //    case "cuotaestado":
  //    case "cuotaanterior":
  //      this.child( "fdbCuotaResultado" ).setValue( _i.calculateField( "cuotaresultado" ) );
  //      break;
  //
  //    case "cuotadedoi":
  //    case "cuotadedim":
  //    case "cuotadedai":
  //    case "cuotacomre":
  //    case "cuotaregin":
  //      this.child( "fdbCuotaDedTotal" ).setValue( _i.calculateField( "cuotadedtotal" ) );
  //      break;
  //
  //    case "cuotadedtotal":
  //    case "cuotadevtotal":
  //      this.child( "fdbCuotaDif" ).setValue(_i.calculateField( "cuotadif" ));
  //      break;
  //
  //    case "cuotadif":
  //    case "porcuotaestado":
  //      this.child( "fdbCuotaEstado" ).setValue(_i.calculateField( "cuotaestado" ));
  //      break;
  //
  //    case "cuotaestado":
  //    case "cuotaanterior":
  //    case "sujetospasivos":
  //      this.child( "fdbCuotaResultado" ).setValue(_i.calculateField( "cuotaresultado" ));
  //      break;
  //
  //    case "idsctacuotasanteriores":
  //      this.child( "fdbCuotaAnterior" ).setValue(_i.calculateField( "cuotaanterior" ));
  //      break;
  //
  //    case "codejercicio":
  //      _i.borrarValores();
  //        _i.establecerFechasPeriodo();
  //      break;
  //
  //    case "fechainicio":
  //    case "fechafin":
  //      _i.borrarValores();
  //      break;
  //
  //    case "codcuentadev":
  //    case "ctaentidaddev":
  //    case "ctaagenciadev":
  //    case "cuentadev":
  //      this.child("fdbDcDev").setValue(_i.calculateField("dcdev"));
  //      break;
  //
  //    case "codcuentaingreso":
  //    case "ctaentidadingreso":
  //    case "ctaagenciaingreso":
  //    case "cuentaingreso":
  //      this.child("fdbDcIngreso").setValue(_i.calculateField("dcingreso"));
  //      break;
  //
  //    case "pagoefectivo":
  //      if (!_i.bloqueoPago) {
  //        _i.bloqueoPago = true;
  //        this.child("fdbPagoCuenta").setValue(_i.calculateField("pagocuenta"));
  //        _i.bloqueoPago = false;
  //      }
  //      break;
  //
  //    case "pagocuenta":
  //      if (!_i.bloqueoPago) {
  //        _i.bloqueoPago = true;
  //        this.child("fdbPagoEfectivo").setValue(_i.calculateField("pagoefectivo"));
  //        _i.bloqueoPago = false;
  //      }
  //      break;
  //    case "cuotaregapli": {
  //      var ejercicio = parseFloat(cursor.valueBuffer("fechainicio"));
  //      var temp = ejercicio.toString().left(4);
  //      if (temp <= 2006)
  //        break;
  //      else
  //        this.child("fdbCuotaDedTotal").setValue(_i.calculateField("cuotadedtotal" ) );
  //      break;
  //    }
  //  }
}
function oficial_bufferChanged2014(fN)
{
  var _i = this.iface;
  var cursor = this.cursor();
  switch (fN) {
    case "cuotarg1":
    case "cuotarg2":
    case "cuotarg3":
    case "cuotaai":
    case "cuotaoo":
    case "cuotambc":
    case "cuotare1":
    case "cuotare2":
    case "cuotare3":
    case "cuotambcre": {
      this.child("fdbCuotaDevTotal").setValue(_i.calculateField("cuotadevtotal"));
      break;
    }
    case "cuotadedoibc":
    case "cuotadedoibi":
    case "cuotadedimbc":
    case "cuotadedimbi":
    case "cuotadedaibc":
    case "cuotadedaibi":
    case "cuotarecded":
    case "cuotacomre":
    case "cuotaregin":
    case "cuotaregapli": {
      this.child("fdbCuotaDedTotal").setValue(_i.calculateField("cuotadedtotal"));
      break;
    }
    case "cuotadedtotal":
    case "cuotadevtotal": {
      this.child("fdbCuotaDif").setValue(_i.calculateField("cuotadif"));
      break;
    }
    case "cuotadif":
    case "porcuotaestado": {
      this.child("fdbCuotaEstado").setValue(_i.calculateField("cuotaestado"));
      this.child("fdbSumaResultados").setValue(_i.calculateField("sumaresultados"));
      break;
    }
    case "cuotaestado":
    case "cuotaanterior":
    case "sujetospasivos": {
      this.child("fdbCuotaResultado").setValue(_i.calculateField("cuotaresultado"));
      break;
    }
    case "cuotaresultado":
    case "adeducircompl": {
      this.child("fdbResultadoLiquidacion").setValue(_i.calculateField("resliquid"));
      break;
    }
    case "resliquid": {
      this.child("fdbImported").setValue(_i.calculateField("imported"));
      this.child("fdbImporteI").setValue(_i.calculateField("importei"));
      break;
    }
    case "impcompensar": {
      this.child("fdbImported").setValue(_i.calculateField("imported"));
      break;
    }
    case "fechainicio":
    case "fechafin": {
      _i.limpiarValores2014();
      break;
    }
    case "tipoperiodo": {
      _i.habilitarPeriodo();
      _i.establecerFechasPeriodo();
    }
    case "mes":
    case "trimestre": {
      _i.establecerFechasPeriodo();
      break;
    }
    case "codcuentaingreso":
    case "ctaentidadingreso":
    case "ctaagenciaingreso":
    case "cuentaingreso": {
      this.child("fdbDcIngreso").setValue(_i.calculateField("dcingreso"));
      break;
    }
    case "codcuentaingreso":
    case "ctaentidadingreso":
    case "ctaagenciaingreso":
    case "cuentaingreso": {
      this.child("fdbDcIngreso").setValue(_i.calculateField("dcingreso"));
      break;
    }
    case "codcuentadev":
    case "ctaentidaddev":
    case "ctaagenciadev":
    case "cuentadev": {
      this.child("fdbDcDev").setValue(_i.calculateField("dcdev"));
      break;
    }
  }
  return;
}

/** \D Calcula algunas de las casillas del modelo a partir de los contenidos de la base de datos de contabilidad
\end */
function oficial_calcularValores()
{
  var _i = this.iface;
  _i.calcularValores2014();
  return;
}

/*function oficial_calcularValores2009()
{
  var _i = this.iface;
  //  if (!_i.cargarSubcuentas()) {
  //    MessageBox.warning(sys.translate("Ha habido un error al cargar los datos de subcuentas de I.V.A.\nEl modelo no puede calcularse"), MessageBox.Ok, MessageBox.NoButton);
  //    return false;
  //  }
  if (!_i.limpiarValores()) {
    return false;
  }

  if (!_i.comprobarFechas()) {
    return false;
  }

  if (!_i.revisarFacturas()) {
    return false;
  }

  if (!_i.calcularCasillas01a09()) {
    return false;
  }

  if (!_i.calcularCasillas10a18()) {
    return false;
  }

  if (!_i.calcularCasillas19a20()) {
    return false;
  }

  if (!_i.calcularCasillas22a23()) {
    return false;
  }

  if (!_i.calcularCasillas24a25()) {
    return false;
  }

  if (!_i.calcularCasillas26a27()) {
    return false;
  }

  if (!_i.calcularCasillas28a29()) {
    return false;
  }

  if (!_i.calcularCasillas30a31()) {
    return false;
  }

  if (!_i.calcularCasillas32a33()) {
    return false;
  }

  if (!_i.calcularCasillas34()) {
    return false;
  }

  if (!_i.calcularCasillas42()) {
    return false;
  }

  if (!_i.calcularCasillas43()) {
    return false;
  }

  if (!_i.calcularCasillas44()) {
    return false;
  }

  return;
}*/
function oficial_calcularValores2014()
{
  var _i = this.iface;
  if (!_i.limpiarValores2014()) {
    return false;
  }

  if (!_i.comprobarFechas()) {
    return false;
  }

  if (!_i.revisarFacturas()) {
    return false;
  }

  if (!_i.calcularCasillas01a09()) {
    return false;
  }

  if (!_i.calcularCasillas10a11()) {
    return false;
  }
  if (!_i.calcularCasillas12a13()) {
    return false;
  }
  if (!_i.calcularCasillas14a15()) {
    return false;
  }
  if (!_i.calcularCasillas16a24()) {
    return false;
  }
  if (!_i.calcularCasillas25a26()) {
    return false;
  }
  if (!_i.calcularCasillas28a29()) {
    return false;
  }

  if (!_i.calcularCasillas30a31()) {
    return false;
  }

  if (!_i.calcularCasillas32a33()) {
    return false;
  }

  if (!_i.calcularCasillas34a35()) {
    return false;
  }

  if (!_i.calcularCasillas36a37()) {
    return false;
  }

  if (!_i.calcularCasillas38a39()) {
    return false;
  }

  if (!_i.calcularCasillas40a41()) {
    return false;
  }

  if (!_i.calcularCasillas42()) {
    return false;
  }
  if (!_i.calcularCasillas43()) {
    return false;
  }
  if (!_i.calcularCasillas44()) {
    return false;
  }

  if (!_i.calcularCasillas59()) {
    return false;
  }

  if (!_i.calcularCasillas60()) {
    return false;
  }

  if (!_i.calcularCasillas61()) {
    return false;
  }
  if (!_i.calcularCasillas62a63()) {
    return false;
  }
  if (!_i.calcularCasillas74a75()) {
    return false;
  }
  return;
}
function oficial_calcularCasillas01a09()
{
  var _i = this.iface;
  var cursor = this.cursor();

  var porcentajes = "";
  var arrayPorcentajes: Array;
  var baseImponible = 0;
  var iva = 0;
  var cuota = 0;
  var i = 1;

  var qryPartidas = new FLSqlQuery();
  qryPartidas.setTablesList("co_partidas");
  qryPartidas.setSelect("SUM(p.baseimponible), p.iva, SUM(p.haber - p.debe)");
  qryPartidas.setFrom("co_asientos a INNER JOIN co_partidas p ON p.idasiento = a.idasiento");
  qryPartidas.setForwardOnly(true);

  var c1;
  var c2;
  var c3;
  for (var v = 0; v < 7; v = v + 3) {
    // Primera vuelta casillas 1 2 3
    // Segunda vuelta casillas 4 5 6
    // Tercera vuelta casillas 7 8 9
    c1 = 1 + v;
    c2 = 2 + v;
    c3 = 3 + v;
    arrayPorcentajes = [];
    porcentajes = AQUtil.sqlSelect("co_datosfiscales", "porcentajes" + c1 + c2 + c3, "1 = 1");
    if (!porcentajes || porcentajes == "")
      continue;

    arrayPorcentajes = porcentajes.split(",");
    porcentajes = "";
    for (var p = 0; p < arrayPorcentajes.length; p++) {
      if (porcentajes != "")
        porcentajes += ",";
      porcentajes += "'" + arrayPorcentajes[p] + "'";
    }
    if (porcentajes || porcentajes != "") {
      qryPartidas.setWhere(_i.whereFechas_ + " AND p.casilla303 = '[01]-[09]' AND p.iva IN (" + porcentajes + ") GROUP BY p.iva ORDER BY p.iva");
      if (!qryPartidas.exec()) {
        return false;
      }
      debug(qryPartidas.sql());
      //    if (qryPartidas.size() == 0) {
      //      MessageBox.warning(sys.translate("Error al obtener datos de I.V.A. del Régimen general:\nSe ha encontrado más de tres tipos de I.V.A."), MessageBox.Ok, MessageBox.NoButton);
      //      return false;
      //    }
      baseImponible = 0;
      cuota = 0;
      iva = 0;
      while (qryPartidas.next()) {
        baseImponible += parseFloat(qryPartidas.value("SUM(p.baseimponible)"));
        cuota += parseFloat(qryPartidas.value("SUM(p.haber - p.debe)"));
      }
      iva = cuota / baseImponible * 100;
      iva = AQUtil.roundFieldValue(iva, "co_partidas", "iva");

      this.child("fdbBaseImponibleRG" + i.toString()).setValue(baseImponible);
      this.child("fdbTipoRG" + i.toString()).setValue(iva);
      this.child("fdbCuotaRG" + i.toString()).setValue(cuota);
      i++;
    }
  }

  qryPartidas.setTablesList("co_partidas");
  qryPartidas.setSelect("SUM(p.baseimponible), SUM(p.haber - p.debe)");
  qryPartidas.setFrom("co_asientos a INNER JOIN co_partidas p ON p.idasiento = a.idasiento");

  var aCasillas = ["[01]-[03]", "[04]-[06]", "[07]-[09]"];
  //  var aPorcentajes = ["123", "456", "789"];
  var base2, cuota2;
  for (var i = 0; i < 3; i++) {
    //    porcentajes = flcontmode.iface.valorDefectoDatosFiscales("porcentajes" + aPorcentajes[i]);
    baseImponible = cursor.valueBuffer("baseimponiblerg" + (i + 1).toString());
    baseImponible = isNaN(baseImponible) ? 0 : baseImponible;
    cuota = cursor.valueBuffer("cuotarg" + (i + 1).toString());
    cuota = isNaN(cuota) ? 0 : cuota;
    qryPartidas.setWhere(_i.whereFechas_ + " AND p.casilla303 = '" + aCasillas[i] + "'"); // AND p.iva IN (" + porcentajes + ")");
    if (!qryPartidas.exec()) {
      return false;
    }
    if (qryPartidas.first()) {
      base2 = qryPartidas.value("SUM(p.baseimponible)");
      base2 = isNaN(base2) ? 0 : base2;
      baseImponible += parseFloat(base2);
      sys.setObjText(this, "fdbBaseImponibleRG" + (i + 1).toString(), baseImponible);
      cuota2 = qryPartidas.value("SUM(p.haber - p.debe)");
      cuota2 = isNaN(cuota2) ? 0 : cuota2;
      cuota += parseFloat(cuota2);
      sys.setObjText(this, "fdbCuotaRG" + (i + 1).toString(), cuota);
      iva = cuota / baseImponible * 100;
      iva = AQUtil.roundFieldValue(iva, "co_partidas", "iva");
      sys.setObjText(this, "fdbTipoRG" + (i + 1).toString(), iva);
    }
  }
  return true;
}


function oficial_calcularCasillas16a24()
{
  //Antes 10a18
  var _i = this.iface;
  var cursor = this.cursor();

  var porcentajes = "";
  var arrayPorcentajes: Array;
  var baseImponible = 0;
  var iva = 0;
  var cuota = 0;
  var i = 1;

  var qryPartidas = new FLSqlQuery();
  qryPartidas.setTablesList("co_partidas");
  qryPartidas.setSelect("SUM(p.baseimponible), p.recargo, SUM(p.haber - p.debe)");
  qryPartidas.setFrom("co_asientos a INNER JOIN co_partidas p ON p.idasiento = a.idasiento");
  qryPartidas.setForwardOnly(true);

  var c1;
  var c2;
  var c3;
  for (var v = 0; v < 7; v = v + 3) {
    // Primera vuelta casillas 1 2 3
    // Segunda vuelta casillas 4 5 6
    // Tercera vuelta casillas 7 8 9
    c1 = 1 + v;
    c2 = 2 + v;
    c3 = 3 + v;
    arrayPorcentajes = [];
    porcentajes = AQUtil.sqlSelect("co_datosfiscales", "porcentajesrecargo" + c1 + c2 + c3, "1 = 1");
    if (!porcentajes || porcentajes == "")
      continue;

    arrayPorcentajes = porcentajes.split(",");
    porcentajes = "";
    for (var p = 0; p < arrayPorcentajes.length; p++) {
      if (porcentajes != "") {
        porcentajes += ",";
      }
      porcentajes += "'" + arrayPorcentajes[p] + "'";
    }
    if (porcentajes || porcentajes != "") {
      qryPartidas.setWhere(_i.whereFechas_ + " AND p.casilla303 = '[16]-[24]' AND p.recargo IN (" + porcentajes + ") GROUP BY p.recargo ORDER BY p.recargo ");
      debug(qryPartidas.sql());
      if (!qryPartidas.exec()) {
        return false;
      }

      var baseImponible = 0;
      var re = 0;
      var cuota = 0;

      while (qryPartidas.next()) {
        baseImponible += qryPartidas.value("SUM(p.baseimponible)");
        cuota += qryPartidas.value("SUM(p.haber - p.debe)");
      }

      re = cuota / baseImponible * 100;
      re = AQUtil.roundFieldValue(re, "co_partidas", "recargo");
      this.child("fdbBaseImponibleRE" + i.toString()).setValue(baseImponible);
      this.child("fdbTipoRE" + i.toString()).setValue(re);
      this.child("fdbCuotaRE" + i.toString()).setValue(cuota);
      i++;

    }
  }

  qryPartidas.setTablesList("co_partidas");
  qryPartidas.setSelect("SUM(p.baseimponible), SUM(p.haber - p.debe)");
  qryPartidas.setFrom("co_asientos a INNER JOIN co_partidas p ON p.idasiento = a.idasiento");

  var aCasillas = ["[16]-[18]", "[19]-[21]", "[22]-[24]"];

  var base2, cuota2;
  for (var i = 0; i < 3; i++) {
    baseImponible = cursor.valueBuffer("baseimponiblere" + (i + 1).toString());
    baseImponible = isNaN(baseImponible) ? 0 : baseImponible;
    cuota = cursor.valueBuffer("cuotare" + (i + 1).toString());
    cuota = isNaN(cuota) ? 0 : cuota;
    qryPartidas.setWhere(_i.whereFechas_ + " AND p.casilla303 = '" + aCasillas[i] + "'");
    if (!qryPartidas.exec()) {
      return false;
    }
    if (qryPartidas.first()) {
      base2 = qryPartidas.value("SUM(p.baseimponible)");
      base2 = isNaN(base2) ? 0 : base2;
      baseImponible += parseFloat(base2);
      sys.setObjText(this, "fdbBaseImponibleRE" + (i + 1).toString(), baseImponible);
      cuota2 = qryPartidas.value("SUM(p.haber - p.debe)");
      cuota2 = isNaN(cuota2) ? 0 : cuota2;
      cuota += parseFloat(cuota2);
      sys.setObjText(this, "fdbCuotaRE" + (i + 1).toString(), cuota);
      re = cuota / baseImponible * 100;
      re = AQUtil.roundFieldValue(re, "co_partidas", "recargo");
      sys.setObjText(this, "fdbTipoRE" + (i + 1).toString(), re);
    }
  }
  return true;
}

function oficial_calcularCasillas10a11()
{
  //Antes 19a20
  var _i = this.iface;
  var cursor = this.cursor();

  var qryPartidas = new FLSqlQuery();
  qryPartidas.setTablesList("co_partidas");
  qryPartidas.setSelect("SUM(p.baseimponible), SUM(p.haber - p.debe)");
  qryPartidas.setFrom("co_asientos a INNER JOIN co_partidas p ON p.idasiento = a.idasiento");
  qryPartidas.setWhere(_i.whereFechas_ + " AND p.casilla303 = '[10]-[11]'");
  qryPartidas.setForwardOnly(true);
  if (!qryPartidas.exec()) {
    return false;
  }

  var baseImponible = 0;
  var cuota = 0;
  if (qryPartidas.first()) {
    baseImponible = qryPartidas.value("SUM(p.baseimponible)");
    cuota = qryPartidas.value("SUM(p.haber - p.debe)");
  }
  this.child("fdbBaseImponibleAI").setValue(baseImponible);
  this.child("fdbCuotaAI").setValue(cuota);

  return true;
}
function oficial_calcularCasillas28a29()
{
  //antes 22-23
  var _i = this.iface;
  var cursor = this.cursor();

  var qryPartidas = new FLSqlQuery();
  qryPartidas.setTablesList("co_partidas");
  qryPartidas.setSelect("SUM(p.baseimponible), SUM(p.debe - p.haber)");
  qryPartidas.setFrom("co_asientos a INNER JOIN co_partidas p ON p.idasiento = a.idasiento");
  qryPartidas.setWhere(_i.whereFechas_ + " AND p.casilla303 = '[28]-[29]'");
  qryPartidas.setForwardOnly(true);
  if (!qryPartidas.exec()) {
    return false;
  }

  var baseImponible = 0;
  var cuota = 0;
  if (qryPartidas.first()) {
    baseImponible = qryPartidas.value("SUM(p.baseimponible)");
    cuota = qryPartidas.value("SUM(p.debe - p.haber)");
  }
  this.child("fdbBaseDedoibc").setValue(baseImponible);
  this.child("fdbCuotaDedOI").setValue(cuota);

  return true;
}

function oficial_calcularCasillas30a31()
{
  //antes 24-25
  var _i = this.iface;
  var cursor = this.cursor();

  var qryPartidas = new FLSqlQuery();
  qryPartidas.setTablesList("co_partidas");
  qryPartidas.setSelect("SUM(p.baseimponible), SUM(p.debe - p.haber)");
  qryPartidas.setFrom("co_asientos a INNER JOIN co_partidas p ON p.idasiento = a.idasiento");
  qryPartidas.setWhere(_i.whereFechas_ + " AND p.casilla303 = '[30]-[31]'");
  qryPartidas.setForwardOnly(true);
  if (!qryPartidas.exec()) {
    return false;
  }

  var baseImponible = 0;
  var cuota = 0;
  if (qryPartidas.first()) {
    baseImponible = qryPartidas.value("SUM(p.baseimponible)");
    cuota = qryPartidas.value("SUM(p.debe - p.haber)");
  }
  this.child("fdbBaseDedoibi").setValue(baseImponible);
  this.child("fdbCuotaDedIm").setValue(cuota);

  return true;
}

function oficial_calcularCasillas32a33()
{
  //Antes 26a27
  var _i = this.iface;
  var cursor = this.cursor();

  var qryPartidas = new FLSqlQuery();
  qryPartidas.setTablesList("co_partidas");
  qryPartidas.setSelect("SUM(p.baseimponible), SUM(p.debe - p.haber)");
  qryPartidas.setFrom("co_asientos a INNER JOIN co_partidas p ON p.idasiento = a.idasiento");
  qryPartidas.setWhere(_i.whereFechas_ + " AND p.casilla303 = '[32]-[33]'");
  qryPartidas.setForwardOnly(true);
  if (!qryPartidas.exec()) {
    return false;
  }

  var baseImponible = 0;
  var cuota = 0;
  if (qryPartidas.first()) {
    baseImponible = qryPartidas.value("SUM(p.baseimponible)");
    cuota = qryPartidas.value("SUM(p.debe - p.haber)");
  }
  this.child("fdbBaseDedimc").setValue(baseImponible);
  this.child("fdbCuotaDedimbc").setValue(cuota);

  return true;
}

function oficial_calcularCasillas34a35()
{
  //antes 28a29
  var _i = this.iface;
  var cursor = this.cursor();

  var qryPartidas = new FLSqlQuery();
  qryPartidas.setTablesList("co_partidas");
  qryPartidas.setSelect("SUM(p.baseimponible), SUM(p.debe - p.haber)");
  qryPartidas.setFrom("co_asientos a INNER JOIN co_partidas p ON p.idasiento = a.idasiento");
  qryPartidas.setWhere(_i.whereFechas_ + " AND p.casilla303 = '[34]-[35]'");
  qryPartidas.setForwardOnly(true);
  if (!qryPartidas.exec()) {
    return false;
  }

  var baseImponible = 0;
  var cuota = 0;
  if (qryPartidas.first()) {
    baseImponible = qryPartidas.value("SUM(p.baseimponible)");
    cuota = qryPartidas.value("SUM(p.debe - p.haber)");
  }
  this.child("fdbBaseDedimbi").setValue(baseImponible);
  this.child("fdbCuotaDedimbi").setValue(cuota);

  return true;
}

function oficial_calcularCasillas36a37()
{
  //Antes 30a31
  var _i = this.iface;
  var cursor = this.cursor();

  var qryPartidas = new FLSqlQuery();
  qryPartidas.setTablesList("co_partidas");
  qryPartidas.setSelect("SUM(p.baseimponible), SUM(p.debe - p.haber)");
  qryPartidas.setFrom("co_asientos a INNER JOIN co_partidas p ON p.idasiento = a.idasiento");
  qryPartidas.setWhere(_i.whereFechas_ + " AND p.casilla303 = '[36]-[37]'");
  qryPartidas.setForwardOnly(true);
  if (!qryPartidas.exec()) {
    return false;
  }

  var baseImponible = 0;
  var cuota = 0;
  if (qryPartidas.first()) {
    baseImponible = qryPartidas.value("SUM(p.baseimponible)");
    cuota = qryPartidas.value("SUM(p.debe - p.haber)");
  }
  this.child("fdbBaseDedaibc").setValue(baseImponible);
  this.child("fdbCuotaDedaibc").setValue(cuota);

  return true;
}

function oficial_calcularCasillas38a39()
{
  //Antes 32a33
  var _i = this.iface;
  var cursor = this.cursor();

  var qryPartidas = new FLSqlQuery();
  qryPartidas.setTablesList("co_partidas");
  qryPartidas.setSelect("SUM(p.baseimponible), SUM(p.debe - p.haber)");
  qryPartidas.setFrom("co_asientos a INNER JOIN co_partidas p ON p.idasiento = a.idasiento");
  qryPartidas.setWhere(_i.whereFechas_ + " AND p.casilla303 = '[38]-[39]'");
  qryPartidas.setForwardOnly(true);
  if (!qryPartidas.exec()) {
    return false;
  }

  var baseImponible = 0;
  var cuota = 0;
  if (qryPartidas.first()) {
    baseImponible = qryPartidas.value("SUM(p.baseimponible)");
    cuota = qryPartidas.value("SUM(p.debe - p.haber)");
  }
  this.child("fdbBaseDedaibi").setValue(baseImponible);
  this.child("fdbCuotaDedaibi").setValue(cuota);

  return true;
}
function oficial_calcularCasillas40a41()
{

  var _i = this.iface;
  var cursor = this.cursor();

  var baseImponible = 0;
  var cuota = 0;

  this.child("fdbBaseRecDed").setValue(baseImponible);
  this.child("fdbCuotaRecDed").setValue(cuota);

  return true;
}
function oficial_calcularCasillas42()
{
  //Antes 34
  var _i = this.iface;
  var cursor = this.cursor();

  var qryPartidas = new FLSqlQuery();
  qryPartidas.setTablesList("co_partidas");
  qryPartidas.setSelect("SUM(p.baseimponible), SUM(p.debe - p.haber)");
  qryPartidas.setFrom("co_asientos a INNER JOIN co_partidas p ON p.idasiento = a.idasiento");
  qryPartidas.setWhere(_i.whereFechas_ + " AND p.casilla303 = '[42]'");
  qryPartidas.setForwardOnly(true);
  if (!qryPartidas.exec()) {
    return false;
  }

  var baseImponible = 0;
  var cuota = 0;
  if (qryPartidas.first()) {
    baseImponible = qryPartidas.value("SUM(p.baseimponible)");
    cuota = qryPartidas.value("SUM(p.debe - p.haber)");
  }
  this.child("fdbCuotaComRE").setValue(cuota);

  return true;
}
function oficial_calcularCasillas43()
{
  //Antes 35
  var _i = this.iface;
  var cursor = this.cursor();

  var cuota = 0;

  this.child("fdbCuotaRegIn").setValue(cuota);

  return true;
}
function oficial_calcularCasillas44()
{
  //Antes 36
  var _i = this.iface;
  var cursor = this.cursor();
  var cuota = 0;

  this.child("fdbCuotaRegApli").setValue(cuota);

  return true;
}
function oficial_calcularCasillas59()
{
  var _i = this.iface;
  var cursor = this.cursor();

  var qryPartidas = new FLSqlQuery();
  qryPartidas.setTablesList("co_partidas");
  qryPartidas.setSelect("SUM(p.baseimponible), SUM(p.debe - p.haber)");
  qryPartidas.setFrom("co_asientos a INNER JOIN co_partidas p ON p.idasiento = a.idasiento");
  qryPartidas.setWhere(_i.whereFechas_ + " AND p.casilla303 = '[59]'");
  qryPartidas.setForwardOnly(true);
  if (!qryPartidas.exec()) {
    return false;
  }

  var baseImponible = 0;
  var cuota = 0;
  if (qryPartidas.first()) {
    baseImponible = qryPartidas.value("SUM(p.baseimponible)");
    cuota = qryPartidas.value("SUM(p.debe - p.haber)");
  }
  this.child("fdbEntregasI").setValue(baseImponible);

  return true;
}

function oficial_calcularCasillas60()
{
  //antes 43
  var _i = this.iface;
  var cursor = this.cursor();

  var qryPartidas = new FLSqlQuery();
  qryPartidas.setTablesList("co_partidas");
  qryPartidas.setSelect("SUM(p.baseimponible), SUM(p.debe - p.haber)");
  qryPartidas.setFrom("co_asientos a INNER JOIN co_partidas p ON p.idasiento = a.idasiento");
  qryPartidas.setWhere(_i.whereFechas_ + " AND p.casilla303 = '[60]'");
  qryPartidas.setForwardOnly(true);
  if (!qryPartidas.exec()) {
    return false;
  }

  var baseImponible = 0;
  var cuota = 0;
  if (qryPartidas.first()) {
    baseImponible = qryPartidas.value("SUM(p.baseimponible)");
    cuota = qryPartidas.value("SUM(p.debe - p.haber)");
  }
  this.child("fdbExportaciones").setValue(baseImponible);

  return true;
}

function oficial_calcularCasillas61()
{
  //Antes calcularCasillas44
  var _i = this.iface;
  var cursor = this.cursor();

  var qryPartidas = new FLSqlQuery();
  qryPartidas.setTablesList("co_partidas");
  qryPartidas.setSelect("SUM(p.baseimponible), SUM(p.debe - p.haber)");
  qryPartidas.setFrom("co_asientos a INNER JOIN co_partidas p ON p.idasiento = a.idasiento");
  qryPartidas.setWhere(_i.whereFechas_ + " AND p.casilla303 = '[61]'");
  qryPartidas.setForwardOnly(true);
  if (!qryPartidas.exec()) {
    return false;
  }

  var baseImponible = 0;
  var cuota = 0;
  if (qryPartidas.first()) {
    baseImponible = qryPartidas.value("SUM(p.baseimponible)");
    cuota = qryPartidas.value("SUM(p.debe - p.haber)");
  }
  this.child("fdbNoSujetas").setValue(baseImponible);

  return true;
}
function oficial_calcularCasillas62a63()
{

  var _i = this.iface;
  var cursor = this.cursor();

  var baseImponible = 0;
  var cuota = 0;

  this.child("fdbBaseEntregasCC").setValue(baseImponible);
  this.child("fdbCuotaEntregasCC").setValue(cuota);

  return true;
}
function oficial_calcularCasillas74a75()
{

  var _i = this.iface;
  var cursor = this.cursor();

  var baseImponible = 0;
  var cuota = 0;

  this.child("fdbBaseAdquisicionesCC").setValue(baseImponible);
  this.child("fdbCuotaAdquisicionesCC").setValue(cuota);

  return true;
}
/** \D Establece las fechas de inicio y fin de trimestre en función del trimestre seleccionado
\end */
function oficial_establecerFechasPeriodo()
{
  var _i = this.iface;
  var cursor = this.cursor();

  var fechaInicio: Date;
  var fechaFin: Date;
  var codEjercicio = this.child("fdbCodEjercicio").value();
  var inicioEjercicio = AQUtil.sqlSelect("ejercicios", "fechainicio",
                                         "codejercicio = '" + codEjercicio + "'");

  if (!inicioEjercicio) {
    return false;
  }

  fechaInicio.setYear(inicioEjercicio.getYear());
  fechaFin.setYear(inicioEjercicio.getYear());
  fechaInicio.setDate(1);

  debug(cursor.valueBuffer("tipoperiodo") + " " + cursor.valueBuffer("trimestre"));
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
      switch (cursor.valueBuffer("mes")) {
        case "Enero": {
          fechaInicio.setMonth(1);
          fechaFin.setMonth(1);
          fechaFin.setDate(31);
          break;
        }
        case "Febrero": {
          fechaInicio.setMonth(2);
          fechaFin.setMonth(2);
          fechaFin.setDate(28);
          break;
        }
        case "Marzo": {
          fechaInicio.setMonth(3);
          fechaFin.setMonth(3);
          fechaFin.setDate(31);
          break;
        }
        case "Abril": {
          fechaInicio.setMonth(4);
          fechaFin.setMonth(4);
          fechaFin.setDate(30);
          break;
        }
        case "Mayo": {
          fechaInicio.setMonth(5);
          fechaFin.setMonth(5);
          fechaFin.setDate(31);
          break;
        }
        case "Junio": {
          fechaInicio.setMonth(6);
          fechaFin.setMonth(6);
          fechaFin.setDate(30);
          break;
        }
        case "Julio": {
          fechaInicio.setMonth(7);
          fechaFin.setMonth(7);
          fechaFin.setDate(31);
          break;
        }
        case "Agosto": {
          fechaInicio.setMonth(8);
          fechaFin.setMonth(8);
          fechaFin.setDate(31);
          break;
        }
        case "Septiembre": {
          fechaInicio.setMonth(9);
          fechaFin.setMonth(9);
          fechaFin.setDate(30);
          break;
        }
        case "Octubre": {
          fechaInicio.setMonth(10);
          fechaFin.setMonth(10);
          fechaFin.setDate(31);
          break;
        }
        case "Noviembre": {
          fechaInicio.setMonth(11);
          fechaFin.setMonth(11);
          fechaFin.setDate(30);
          break;
        }
        case "Diciembre": {
          fechaInicio.setMonth(12);
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
  }

  if (fechaInicio) {
    debug("Fechainicio = " + fechaInicio);
    this.child("fdbFechaInicio").setValue(fechaInicio);
    this.child("fdbFechaFin").setValue(fechaFin);
  } else {
    debug("!Fechainicio");
    cursor.setNull("fechainicio");
    cursor.setNull("fechafin");
  }
}

/** \D Borra algunas de las casillas calculadas
\end */
function oficial_borrarValores()
{
  if (!this.child("fdbBaseImponibleRG0")) return false;

  this.child("fdbBaseImponibleRG0").setValue(0);
  this.child("fdbBaseImponibleRG1").setValue(0);
  this.child("fdbBaseImponibleRG2").setValue(0);
  this.child("fdbBaseImponibleRE0").setValue(0);
  this.child("fdbBaseImponibleRE1").setValue(0);
  this.child("fdbBaseImponibleRE2").setValue(0);
  this.child("fdbCuotaDedOI").setValue(0);

}

/** \D Comprueba que fechainicio < fechafin y que ambas pertenecen al ejercicio seleccionado

@return True si la comprobación es buena, false en caso contrario
\end */
function oficial_comprobarFechas()
{
  var _i = this.iface;
  var cursor = this.cursor();

  var codEjercicio = this.child("fdbCodEjercicio").value();
  var fechaInicio = this.child("fdbFechaInicio").value();
  var fechaFin = this.child("fdbFechaFin").value();

  if (AQUtil.daysTo(fechaInicio, fechaFin) < 0) {
    MessageBox.critical(sys.translate("La fecha de inicio debe ser menor que la de fin"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
    return false;
  }

  var inicioEjercicio = AQUtil.sqlSelect("ejercicios", "fechainicio", "codejercicio = '" + codEjercicio + "'");
  var finEjercicio = AQUtil.sqlSelect("ejercicios", "fechafin", "codejercicio = '" + codEjercicio + "'");

  if ((AQUtil.daysTo(inicioEjercicio, fechaInicio) < 0) || (AQUtil.daysTo(fechaFin, finEjercicio) < 0)) {
    MessageBox.critical(sys.translate("Las fechas seleccionadas no corresponden al ejercicio"), MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton);
    return false;
  }

  return true;
}

function oficial_habilitarPeriodo()
{
  var _i = this.iface;
  var cursor = this.cursor();

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

function oficial_revisarFacturas()
{
  var _i = this.iface;
  var cursor = this.cursor();

  _i.actualizarWhereFechas();

  var fechaDesde = this.child("fdbFechaInicio").value();
  var fechaHasta = this.child("fdbFechaFin").value();
  var codEjercicio = this.child("fdbCodEjercicio").value();

  var whereFacturas = "a.codejercicio = '" + codEjercicio + "' AND a.fecha BETWEEN '" + fechaDesde + "' AND '" + fechaHasta + "' AND excluir303 <> true";
  var qryFacturasCli = new FLSqlQuery();
  with(qryFacturasCli) {
    setTablesList("clientes,facturascli,co_asientos,co_partidas,co_subcuentas");
    setSelect("p.idpartida");
    setFrom("facturascli f INNER JOIN co_asientos a ON f.idasiento = a.idasiento INNER JOIN co_partidas p ON a.idasiento = p.idasiento INNER JOIN co_subcuentas s ON p.idsubcuenta = s.idsubcuenta");
    setWhere(whereFacturas + " GROUP BY p.idpartida");
    setForwardOnly(true);
  }
  debug(qryFacturasCli.sql());
  if (!qryFacturasCli.exec()) {
    return false;
  }

  var totalPasos = qryFacturasCli.size();
  var paso = 0;
  AQUtil.createProgressDialog(sys.translate("Limpiando partidas de facturas de cliente"), totalPasos);
  while (qryFacturasCli.next()) {
    AQUtil.setProgress(++paso);
    if (!_i.actualizarCasilla303Partida(qryFacturasCli.value("p.idpartida"), "NULL")) {
      sys.AQTimer.singleShot(0, AQUtil.destroyProgressDialog);
      return false;
    }
  }
  sys.AQTimer.singleShot(0, AQUtil.destroyProgressDialog);

  with(qryFacturasCli) {
    setSelect("p.idpartida, p.codsubcuenta, s.idcuentaesp");
    setWhere(whereFacturas);
  }
  debug(qryFacturasCli.sql());
  if (!qryFacturasCli.exec()) {
    return false;
  }
  totalPasos = qryFacturasCli.size();
  paso = 0;
  AQUtil.createProgressDialog(sys.translate("Procesando facturas de cliente"), totalPasos);

  var idCuentaEsp;
  var casilla;
  var codSubcuenta;
  while (qryFacturasCli.next()) {
    AQUtil.setProgress(++paso);
    codSubcuenta = qryFacturasCli.value("p.codsubcuenta");
    idCuentaEsp = qryFacturasCli.value("s.idcuentaesp");
    debug("codSubcuenta = " + codSubcuenta + "  idCuentaEsp = " + idCuentaEsp);
    switch (idCuentaEsp) {
      case "IVAREP": {
        casilla = "[01]-[09]";
        break;
      }
      case "IVARRE":
      case "IVAACR": {
        //casilla = "[10]-[18]";
        casilla = "[16]-[24]";
        break;
      }
      case "IVAEUE": {
        //casilla = "[42]";
        casilla = "[59]";
        break;
      }
      case "IVARXP": {
        //casilla = "[43]";
        casilla = "[60]";
        break;
      }
      case "IVAREX": {
        //casilla = "[44]";
        casilla = "[61]";
        break;
      }
      default: {
        continue;
      }
    }

    if (!_i.actualizarCasilla303Partida(qryFacturasCli.value("p.idpartida"), casilla)) {
      sys.AQTimer.singleShot(0, AQUtil.destroyProgressDialog);
      return false;
    }
  }
  sys.AQTimer.singleShot(0, AQUtil.destroyProgressDialog);

  var qryFacturasProv = new FLSqlQuery();
  with(qryFacturasProv) {
    setTablesList("clientes,facturascli,co_asientos,co_partidas,co_subcuentas");
    setSelect("p.idpartida");
    setFrom("facturasprov f INNER JOIN co_asientos a ON f.idasiento = a.idasiento INNER JOIN co_partidas p ON a.idasiento = p.idasiento INNER JOIN co_subcuentas s ON p.idsubcuenta = s.idsubcuenta");
    setWhere(whereFacturas + " GROUP BY p.idpartida");
    setForwardOnly(true);
  }

  if (!qryFacturasProv.exec()) {
    return false;
  }

  totalPasos = qryFacturasProv.size();
  paso = 0;
  AQUtil.createProgressDialog(sys.translate("Limpiando partidas de facturas de proveedor"), totalPasos);
  while (qryFacturasProv.next()) {
    AQUtil.setProgress(++paso);
    if (!_i.actualizarCasilla303Partida(qryFacturasProv.value("p.idpartida"), "NULL")) {
      sys.AQTimer.singleShot(0, AQUtil.destroyProgressDialog);
      return false;
    }
  }
  sys.AQTimer.singleShot(0, AQUtil.destroyProgressDialog);


  with(qryFacturasProv) {
    setSelect("p.idasiento, p.idpartida, p.codsubcuenta, s.idcuentaesp, f.codigo");
    setWhere(whereFacturas);
  }
  debug(qryFacturasProv.sql());

  if (!qryFacturasProv.exec()) {
    return false;
  }
  var casilla;
  var codSubcuenta;
  totalPasos = qryFacturasProv.size();
  paso = 0;
  AQUtil.createProgressDialog(sys.translate("Procesando facturas de proveedor"), totalPasos);
  while (qryFacturasProv.next()) {
    AQUtil.setProgress(++paso);
    codSubcuenta = qryFacturasProv.value("p.codsubcuenta");
    idCuentaEsp = qryFacturasProv.value("s.idcuentaesp");
    switch (idCuentaEsp) {
      case "IVARSE": {
        casilla = "[01]-[09]";
        break;
      }
      case "IVARUE": {
        casilla = "[19]-[20]";
        //casilla = "[10]-[11]";
        break;
      }
      case "IVASOP":
      case "IVASSE": {
        var tipoBienes = _i.dameTipoBienes(qryFacturasProv.value("p.idasiento"));
        if (!tipoBienes) {
          sys.AQTimer.singleShot(0, AQUtil.destroyProgressDialog);
          return false;
        }
        switch (tipoBienes) {
          case "corrientes": {
            //casilla = "[22]-[23]";
            casilla = "[28]-[29]";
            break;
          }
          case "inversion": {
            //casilla = "[24]-[25]";
            casilla = "[30]-[31]";
            break;
          }
          case "indefinido": {
            MessageBox.warning(sys.translate("No se ha podido determinar si la factura %1 corresponde a la compra de bienes corrientes o de inversión.\nLa factura no será incluida de forma automática en el modelo").arg(qryFacturasProv.value("f.codigo")), MessageBox.Ok, MessageBox.NoButton);
            continue;
          }
        }
        break;
      }
      case "IVASIM": {
        var tipoBienes = _i.dameTipoBienes(qryFacturasProv.value("p.idasiento"));
        if (!tipoBienes) {
          sys.AQTimer.singleShot(0, AQUtil.destroyProgressDialog);
          return false;
        }
        switch (tipoBienes) {
          case "corrientes": {
            casilla = "[26]-[27]";
            break;
          }
          case "inversion": {
            casilla = "[28]-[29]";
            break;
          }
          case "indefinido": {
            MessageBox.warning(sys.translate("No se ha podido determinar si la factura %1 corresponde a la compra de bienes corrientes o de inversión.\nLa factura no será incluida de forma automática en el modelo").arg(qryFacturasProv.value("f.codigo")), MessageBox.Ok, MessageBox.NoButton);
            continue;
          }
        }
        break;
      }
      case "IVASUE": {
        var tipoBienes = _i.dameTipoBienes(qryFacturasProv.value("p.idasiento"));
        if (!tipoBienes) {
          sys.AQTimer.singleShot(0, AQUtil.destroyProgressDialog);
          return false;
        }
        switch (tipoBienes) {
          case "corrientes": {
            //casilla = "[30]-[31]";
            casilla = "[36]-[37]";
            break;
          }
          case "inversion": {
            //casilla = "[32]-[33]";
            casilla = "[38]-[39]";
            break;
          }
          case "indefinido": {
            MessageBox.warning(sys.translate("No se ha podido determinar si la factura %1 corresponde a la compra de bienes corrientes o de inversión.\nLa factura no será incluida de forma automática en el modelo").arg(qryFacturasProv.value("f.codigo")), MessageBox.Ok, MessageBox.NoButton);
            continue;
          }
        }
        break;
      }
      case "IVASRA": {
        //casilla = "[34]";
        casilla = "[42]";
        break;
      }
      default: {
        continue;
      }
    }

    if (!_i.actualizarCasilla303Partida(qryFacturasProv.value("p.idpartida"), casilla)) {
      sys.AQTimer.singleShot(0, AQUtil.destroyProgressDialog);
      return false;
    }
  }
  sys.AQTimer.singleShot(0, AQUtil.destroyProgressDialog);

  return true;
}

function oficial_dameTipoBienes(idAsiento)
{
  var _i = this.iface;

  var qryTB = new FLSqlQuery;
  qryTB.setTablesList("co_partidas");
  qryTB.setSelect("codsubcuenta");
  qryTB.setFrom("co_partidas");
  qryTB.setWhere("idasiento = " + idAsiento);
  qryTB.setForwardOnly(true);
  if (!qryTB.exec()) {
    return false;
  }
  var corrientes = false;
  var inversion = false;
  var codSubcuenta;
  while (qryTB.next()) {
    codSubcuenta = qryTB.value("codsubcuenta");
    if ((codSubcuenta.toString().startsWith("5") && !codSubcuenta.toString().startsWith("523")) || codSubcuenta.toString().startsWith("6")) {
      corrientes = true;
    } else if (codSubcuenta.toString().startsWith("2")) {
      inversion = true;
    }
  }
  var valor = "indefinido";
  if (corrientes && !inversion) {
    valor = "corrientes";
  } else if (!corrientes && inversion) {
    valor = "inversion";
  }
  return valor;
}

function oficial_conectarDetalles()
{
  var _i = this.iface;
  connect(this.child("pbnDatosRG1"), "clicked()", _i, "partidasDatosRG1");
  connect(this.child("pbnDatosRG2"), "clicked()", _i, "partidasDatosRG2");
  connect(this.child("pbnDatosRG3"), "clicked()", _i, "partidasDatosRG3");
  connect(this.child("pbnDatosRE1"), "clicked()", _i, "partidasDatosRE1");
  connect(this.child("pbnDatosRE2"), "clicked()", _i, "partidasDatosRE2");
  connect(this.child("pbnDatosRE3"), "clicked()", _i, "partidasDatosRE3");
  connect(this.child("pbnDatosIVADevAI"), "clicked()", _i, "partidasDatosIVADevAI");

  connect(this.child("pbnDatosDedOIBC"), "clicked()", _i, "partidasDatosIVADedOIBC");
  connect(this.child("pbnDatosDedOIBI"), "clicked()", _i, "partidasDatosIVADedOIBI");
  connect(this.child("pbnDatosDedImBC"), "clicked()", _i, "partidasDatosIVADedImBC");
  connect(this.child("pbnDatosDedImBI"), "clicked()", _i, "partidasDatosIVADedImBI");
  connect(this.child("pbnDatosDedAIBC"), "clicked()", _i, "partidasDatosIVADedAIBC");
  connect(this.child("pbnDatosDedAIBI"), "clicked()", _i, "partidasDatosIVADedAIBI");
  connect(this.child("pbnDatosComRe"), "clicked()", _i, "partidasDatosIVAComRe");

  connect(this.child("pbnDatosEUE"), "clicked()", _i, "partidasDatosEUE");
  connect(this.child("pbnDatosRXP"), "clicked()", _i, "partidasDatosRXP");
  connect(this.child("pbnDatosREX"), "clicked()", _i, "partidasDatosREX");
}

function oficial_partidasDatosRG1()
{
  var _i = this.iface;
  var cursor = this.cursor();

  var porcentajes = "";
  var fechaLimite = new Date(2010, 6, 30);
  if (AQUtil.daysTo(cursor.valueBuffer("fechafin"), fechaLimite) >= 0) {
    porcentajes = cursor.valueBuffer("tiporg1");
  } else {
    var arrayPorcentajes: Array = [];
    porcentajes = AQUtil.sqlSelect("co_datosfiscales", "porcentajes123", "1 = 1");
    if (!porcentajes || porcentajes == "")
      return;

    arrayPorcentajes = porcentajes.split(",");
    porcentajes = "";
    for (var p = 0; p < arrayPorcentajes.length; p++) {
      if (porcentajes != "")
        porcentajes += ",";
      porcentajes += "'" + arrayPorcentajes[p] + "'";
    }
  }

  _i.mostrarPartidas("((casilla303 = '[01]-[09]' AND iva IN (" + porcentajes + ")) OR casilla303 = '[01]-[03]')");
}

function oficial_partidasDatosRG2()
{
  var _i = this.iface;
  var cursor = this.cursor();

  var porcentajes = "";
  var fechaLimite: Date = new Date(2010, 6, 30);
  if (AQUtil.daysTo(cursor.valueBuffer("fechafin"), fechaLimite) >= 0) {
    porcentajes = cursor.valueBuffer("tiporg2");
  } else {
    var arrayPorcentajes: Array = [];
    porcentajes = AQUtil.sqlSelect("co_datosfiscales", "porcentajes456", "1 = 1");
    if (!porcentajes || porcentajes == "")
      return;

    arrayPorcentajes = porcentajes.split(",");
    porcentajes = "";
    for (var p = 0; p < arrayPorcentajes.length; p++) {
      if (porcentajes != "")
        porcentajes += ",";
      porcentajes += "'" + arrayPorcentajes[p] + "'";
    }
  }

  _i.mostrarPartidas("((casilla303 = '[01]-[09]' AND iva IN (" + porcentajes + ")) OR casilla303 = '[04]-[06]')");
}

function oficial_partidasDatosRG3()
{
  var _i = this.iface;
  var cursor = this.cursor();

  var porcentajes = "";
  var fechaLimite = new Date(2010, 6, 30);
  if (AQUtil.daysTo(cursor.valueBuffer("fechafin"), fechaLimite) >= 0) {
    porcentajes = cursor.valueBuffer("tiporg3");
  } else {
    var arrayPorcentajes: Array = [];
    porcentajes = AQUtil.sqlSelect("co_datosfiscales", "porcentajes789", "1 = 1");
    if (!porcentajes || porcentajes == "")
      return;

    arrayPorcentajes = porcentajes.split(",");
    porcentajes = "";
    for (var p = 0; p < arrayPorcentajes.length; p++) {
      if (porcentajes != "")
        porcentajes += ",";
      porcentajes += "'" + arrayPorcentajes[p] + "'";
    }
  }

  _i.mostrarPartidas("((casilla303 = '[01]-[09]' AND iva IN (" + porcentajes + ")) OR casilla303 = '[07]-[09]')");
}

function oficial_partidasDatosRE1()
{
  var _i = this.iface;
  var cursor = this.cursor();

  //_i.mostrarPartidas("casilla303 = '[10]-[18]' AND recargo = " + cursor.valueBuffer("tipore1"));
  _i.mostrarPartidas("casilla303 = '[16]-[24]' AND recargo = " + cursor.valueBuffer("tipore1"));
}

function oficial_partidasDatosRE2()
{
  var _i = this.iface;
  var cursor = this.cursor();

  //_i.mostrarPartidas("casilla303 = '[10]-[18]' AND recargo = " + cursor.valueBuffer("tipore2"));
  _i.mostrarPartidas("casilla303 = '[16]-[24]' AND recargo = " + cursor.valueBuffer("tipore2"));
}

function oficial_partidasDatosRE3()
{
  var _i = this.iface;
  var cursor = this.cursor();

  //_i.mostrarPartidas("casilla303 = '[10]-[18]' AND recargo = " + cursor.valueBuffer("tipore3"));
  _i.mostrarPartidas("casilla303 = '[16]-[24]' AND recargo = " + cursor.valueBuffer("tipore3"));
}

function oficial_partidasDatosIVADevAI()
{
  var _i = this.iface;
  //_i.mostrarPartidas("casilla303 = '[19]-[20]'");
  _i.mostrarPartidas("casilla303 = '[10]-[11]'");
}

function oficial_partidasDatosIVADedOIBC()
{
  var _i = this.iface;

  // _i.mostrarPartidas("casilla303 = '[22]-[23]'");
  _i.mostrarPartidas("casilla303 = '[28]-[29]'");
}

function oficial_partidasDatosIVADedOIBI()
{
  var _i = this.iface;

  // _i.mostrarPartidas("casilla303 = '[24]-[25]'");
  _i.mostrarPartidas("casilla303 = '[30]-[31]'");
}

function oficial_partidasDatosIVADedImBC()
{
  var _i = this.iface;

  _i.mostrarPartidas("casilla303 = '[26]-[27]'");
}

function oficial_partidasDatosIVADedImBI()
{
  var _i = this.iface;

  _i.mostrarPartidas("casilla303 = '[28]-[29]'");
}

function oficial_partidasDatosIVADedAIBC()
{
  var _i = this.iface;

  //_i.mostrarPartidas("casilla303 = '[30]-[31]'");
  _i.mostrarPartidas("casilla303 = '[36]-[37]'");
}

function oficial_partidasDatosIVADedAIBI()
{
  var _i = this.iface;

  // _i.mostrarPartidas("casilla303 = '[32]-[33]'");
  _i.mostrarPartidas("casilla303 = '[38]-[39]'");
}

function oficial_partidasDatosIVAComRe()
{
  var _i = this.iface;

  //_i.mostrarPartidas("casilla303 = '[34]'");
  _i.mostrarPartidas("casilla303 = '[42]'");
}

function oficial_partidasDatosEUE()
{
  var _i = this.iface;

  //_i.mostrarPartidas("casilla303 = '[42]'");
  _i.mostrarPartidas("casilla303 = '[59]'");
}
function oficial_partidasDatosRXP()
{
  var _i = this.iface;

  // _i.mostrarPartidas("casilla303 = '[43]'");
  _i.mostrarPartidas("casilla303 = '[60]'");
}

function oficial_partidasDatosREX()
{
  var _i = this.iface;

  //_i.mostrarPartidas("casilla303 = '[44]'");
  _i.mostrarPartidas("casilla303 = '[61]'");
}

function oficial_mostrarPartidas(filtro)
{
  var _i = this.iface;
  var cursor = this.cursor();

  var f = new FLFormSearchDB("co_partidas303");
  var curPartidas = f.cursor();
  debug(filtro + " AND idasiento IN (SELECT idasiento FROM co_asientos a WHERE " + _i.whereFechas_ + ")");
  curPartidas.setMainFilter(filtro + " AND idasiento IN (SELECT idasiento FROM co_asientos a WHERE " + _i.whereFechas_ + ")");

  f.setMainWidget();
  var idPartida = f.exec("idpartida");
  if (f.accepted()) {
    return false;
  }
  return true;
}

function oficial_actualizarCasilla303Partida(idPartida, casilla303)
{
  var _i = this.iface;
  debug("oficial_actualizarCasilla303Partida " + idPartida + " " + casilla303);
  if (!_i.curPartida_) {
    _i.curPartida_ = new FLSqlCursor("co_partidas");
    _i.curPartida_.setActivatedCommitActions(false);
  }
  _i.curPartida_.select("idpartida = " + idPartida);
  if (!_i.curPartida_.first()) {
    return false;
  }
  _i.curPartida_.setModeAccess(_i.curPartida_.Edit);
  _i.curPartida_.refreshBuffer();
  if (casilla303 == "NULL") {
    _i.curPartida_.setNull("casilla303");
  } else {
    _i.curPartida_.setValueBuffer("casilla303", casilla303);
  }
  if (!_i.curPartida_.commitBuffer()) {
    return false;
  }
  debug("oficial_actualizarCasilla303Partida " + idPartida + " " + casilla303 + " OK ");
  return true;
}

function oficial_limpiarValores()
{
  this.child("fdbBaseImponibleRG1").setValue("");
  this.child("fdbBaseImponibleRG2").setValue("");
  this.child("fdbBaseImponibleRG3").setValue("");
  this.child("fdbTipoRG1").setValue("");
  this.child("fdbTipoRG2").setValue("");
  this.child("fdbTipoRG3").setValue("");
  this.child("fdbCuotaRG1").setValue("");
  this.child("fdbCuotaRG2").setValue("");
  this.child("fdbCuotaRG3").setValue("");
  this.child("fdbBaseImponibleRE1").setValue("");
  this.child("fdbBaseImponibleRE2").setValue("");
  this.child("fdbBaseImponibleRE3").setValue("");
  this.child("fdbTipoRE1").setValue("");
  this.child("fdbTipoRE2").setValue("");
  this.child("fdbTipoRE3").setValue("");
  this.child("fdbCuotaRE1").setValue("");
  this.child("fdbCuotaRE2").setValue("");
  this.child("fdbCuotaRE3").setValue("");
  this.child("fdbBaseImponibleAI").setValue("");
  this.child("fdbCuotaAI").setValue("");
  this.child("fdbCuotaDevTotal").setValue("");
  this.child("fdbBaseDedoibc").setValue("");
  this.child("fdbCuotaDedOI").setValue("");
  this.child("fdbBaseDedoibi").setValue("");
  this.child("fdbCuotaDedIm").setValue("");
  this.child("fdbBaseDedimc").setValue("");
  this.child("fdbCuotaDedimbc").setValue("");
  this.child("fdbBaseDedimbi").setValue("");
  this.child("fdbCuotaDedimbi").setValue("");
  this.child("fdbBaseDedaibc").setValue("");
  this.child("fdbCuotaDedaibc").setValue("");
  this.child("fdbBaseDedaibi").setValue("");
  this.child("fdbCuotaDedaibi").setValue("");
  this.child("fdbCuotaComRE").setValue("");
  this.child("fdbCuotaRegIn").setValue("");
  this.child("fdbCuotaRegApli").setValue("");
  this.child("fdbCuotaDedTotal").setValue("");
  this.child("fdbCuotaDif").setValue("");

  return true;

}
function oficial_limpiarValores2014()
{
  this.child("fdbInscritoRegDev").setValue(false);
  this.child("fdbTributaExcSimp").setValue(false);
  this.child("fdbTributaExcGen").setValue(false);
  this.child("fdbAutoliqConjunta").setValue(false);
  this.child("fdbConcursoAcre").setValue(false);
  this.child("fdbFechaConcurso").setValue("");
  this.child("fdbTipoDecConcurso").setValue("No");
  this.child("fdbCriterioCaja").setValue(false);
  this.child("fdbDestCriterioCaja").setValue(false);
  this.child("fdbProrrataEspecial").setValue(false);
  this.child("fdbRevocacionProrrata").setValue(false);
  this.child("fdbBaseImponibleRG1").setValue("");
  this.child("fdbBaseImponibleRG2").setValue("");
  this.child("fdbBaseImponibleRG3").setValue("");
  this.child("fdbTipoRG1").setValue("");
  this.child("fdbTipoRG2").setValue("");
  this.child("fdbTipoRG3").setValue("");
  this.child("fdbCuotaRG1").setValue("");
  this.child("fdbCuotaRG2").setValue("");
  this.child("fdbCuotaRG3").setValue("");
  this.child("fdbBaseImponibleAI").setValue("");
  this.child("fdbCuotaAI").setValue("");
  this.child("fdbBaseImponibleOO").setValue("");
  this.child("fdbCuotaOO").setValue("");
  this.child("fdbBaseImponibleMBC").setValue("");
  this.child("fdbCuotaMBC").setValue("");
  this.child("fdbBaseImponibleRE1").setValue("");
  this.child("fdbBaseImponibleRE2").setValue("");
  this.child("fdbBaseImponibleRE3").setValue("");
  this.child("fdbTipoRE1").setValue("");
  this.child("fdbTipoRE2").setValue("");
  this.child("fdbTipoRE3").setValue("");
  this.child("fdbCuotaRE1").setValue("");
  this.child("fdbCuotaRE2").setValue("");
  this.child("fdbCuotaRE3").setValue("");
  this.child("fdbBaseImponibleMBCRE").setValue("");
  this.child("fdbCuotaMBCRE").setValue("");
  this.child("fdbCuotaDevTotal").setValue("");
  this.child("fdbBaseDedoibc").setValue("");
  this.child("fdbCuotaDedOI").setValue("");
  this.child("fdbBaseDedoibi").setValue("");
  this.child("fdbCuotaDedIm").setValue("");
  this.child("fdbBaseDedimc").setValue("");
  this.child("fdbCuotaDedimbc").setValue("");
  this.child("fdbBaseDedimbi").setValue("");
  this.child("fdbCuotaDedimbi").setValue("");
  this.child("fdbBaseDedaibc").setValue("");
  this.child("fdbCuotaDedaibc").setValue("");
  this.child("fdbBaseDedaibi").setValue("");
  this.child("fdbCuotaDedaibi").setValue("");
  this.child("fdbBaseRecDed").setValue("");
  this.child("fdbCuotaRecDed").setValue("");
  this.child("fdbCuotaComRE").setValue("");
  this.child("fdbCuotaRegIn").setValue("");
  this.child("fdbCuotaRegApli").setValue("");
  this.child("fdbCuotaDedTotal").setValue("");
  this.child("fdbBaseEntregasCC").setValue("");
  this.child("fdbCuotaEntregasCC").setValue("");
  this.child("fdbBaseAdquisicionesCC").setValue("");
  this.child("fdbCuotaAdquisicionesCC").setValue("");
  this.child("fdbSumaResultados").setValue("");
  this.child("fdbSumaResultados").setValue("");
  this.child("fdbCuotaDif").setValue("");

  this.child("fdbCuotaAnterior").setValue("");
  this.child("fdbSujetosPasivos").setValue("");
  this.child("fdbImporteAdeducir").setValue("");
  this.child("fdbImporteCompensar").setValue("");
  this.child("fdbNumJustificante").setValue("");


  return true;

}
function oficial_actualizarWhereFechas()
{
  var _i = this.iface;
  var cursor = this.cursor();

  var fechaDesde = this.child("fdbFechaInicio").value();
  var fechaHasta = this.child("fdbFechaFin").value();
  var codEjercicio = this.child("fdbCodEjercicio").value();

  if (!fechaHasta || fechaHasta == "" || !fechaDesde || fechaDesde == "") {
    _i.whereFechas_ = "1 = 2";
  } else {
    _i.whereFechas_ = "a.codejercicio = '" + codEjercicio + "' AND a.fecha BETWEEN '" + fechaDesde + "' AND '" + fechaHasta + "'";
  }
}
function oficial_calcularCasillas12a13()
{

  var _i = this.iface;
  var cursor = this.cursor();
  var baseImponible = 0;
  var cuota = 0;

  this.child("fdbBaseImponibleOO").setValue(baseImponible);
  this.child("fdbCuotaOO").setValue(cuota);

  return true;
}
function oficial_calcularCasillas14a15()
{

  var _i = this.iface;
  var cursor = this.cursor();
  var baseImponible = 0;
  var cuota = 0;

  this.child("fdbBaseImponibleMBC").setValue(baseImponible);
  this.child("fdbCuotaMBC").setValue(cuota);

  return true;
}
function oficial_calcularCasillas25a26()
{

  var _i = this.iface;
  var cursor = this.cursor();
  var baseImponible = 0;
  var cuota = 0;

  this.child("fdbBaseImponibleMBCRE").setValue(baseImponible);
  this.child("fdbCuotaMBCRE").setValue(cuota);

  return true;
}
//// OFICIAL /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////

//// DESARROLLO /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
