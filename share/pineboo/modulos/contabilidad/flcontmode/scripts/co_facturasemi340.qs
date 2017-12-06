var form = this;
/***************************************************************************
                 co_facturasemi340.qs  -  description
                             -------------------
    begin                : mar ene 30 2012
    copyright            : (C) 2012 by InfoSiAL S.L.
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
  function habilitaPorClave()
  {
    return this.ctx.oficial_habilitaPorClave();
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
function interna_init()
{
  var _i = this.iface;
  var util = new FLUtil;
  var cursor = this.cursor();

  connect(cursor, "bufferChanged(QString)", _i, "bufferChanged");

  _i.habilitaPorClave();
}

function interna_calculateField(fN): String {
  var util = new FLUtil;
  var cursor = this.cursor();
  var valor;
  switch (fN)
  {
    case "X": {
      break;
    }
  }
  return valor;
}

function interna_validateForm()
{
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
  switch (fN) {
    case "operacion": {
      _i.habilitaPorClave();
      break;
    }
  }
}

function oficial_habilitaPorClave()
{
  var _i = this.iface;
  var cursor = this.cursor();
  switch (cursor.valueBuffer("operacion")) {
    case "R": {
      this.child("gbxInmueble").enabled = true;
      break;
    }
    case "Z":
    case "1":
    case "2":
    case "3":
    case "4":
    case "5":
    case "6":
    case "7":
    case "8": {
      this.child("gbxCriterioCaja").enabled = true;
      break;
    }
    default: {
      this.child("gbxInmueble").enabled = false;
      this.child("fdbRefCatastral").setValue("");
      this.child("fdbCodSituInmueble").setValue("");

      this.child("gbxCriterioCaja").enabled = false;
      this.child("fdbFechaCobro").setValue("");
      this.child("fdbImporteCobrado").setValue(0);
      this.child("fdbMedioCobro").setValue("");
      this.child("fdbCuentaBancaria").setValue("");
    }
  }
}
//// OFICIAL /////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

/** @class_definition head */
/////////////////////////////////////////////////////////////////
//// DESARROLLO /////////////////////////////////////////////////

//// DESARROLLO /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
