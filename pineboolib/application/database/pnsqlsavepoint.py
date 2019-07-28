# -*- coding: utf-8 -*-

# Completada Si
from pineboolib.core import decorators
from typing import Any, List


"""
Información sobre una operación.

La información de una operación es;
la clave primaria,
operacion realizada (0 = insertar, 1 = editar, 2 = borrar),
buffer con el contenido del registro afectado por la operación,
posición del registro actual del cursor,
orden del cursor,
filtro del cursor,
nombre del cursor (de la tabla),
cursor asociado.
"""


class opInfo:

    primaryKey = None
    op = None
    buffer = None
    at = None
    sort = None
    filter = None
    name = None
    cursor = None
    autoDelete_ = None

    def __init__(self, *args, **kwargs) -> None:
        if len(args) > 0:

            self.opInfo2(*args)

        else:

            self.opInfo1()

        self.setAutoDelete(False)

    def opInfo1(self) -> None:
        return

    def opInfo2(self, pK, o, b, a, s, f, n, c) -> None:  # * c:
        self.primaryKey = pK
        self.op = o
        self.buffer = b
        self.at = a
        self.sort = s
        self.filter = f
        self.name = n
        self.cursor = c

        # c.destroyed.connect(self.cursorDestroyed())

    def __del__(self) -> None:
        pass

    # @decorators.pyqtSlot()
    # def cursorDestroyed(self):
    #    self.cursor = None

    def setAutoDelete(self, b) -> None:
        self.autoDelete_ = b

    """
    Punto de salvaguarda de un conjunto de operaciones básicas
    sobre cursores (insertar, editar y borrar).

    Mediante esta clase se puede guardar un grupo de operaciones básicas
    sobre cursores (insertar, editar y borrar).
    Deshacer un punto de salvaguarda, significa que todas las operaciones
    almacenadas son canceladas realizando las acciones necesarias para que
    no tengan efecto.

    Para el correcto funcionamiento hay que ir guardando los buffer's (QSqlRecord)
    con el contenido de los registros a modificar o modificados por una operación,
    indicando el nombre de la clave primaria y el cursor al que pertenece.

    Ejemplo:
      \\code
      FLSqlCursor cur( "articulos" );
      FLSqlSavePoint savePoint();

      QSqlRecord * buffer = cur.primeInsert();
      buffer->setValue( "id",    53981 );
      buffer->setValue( "name",  "Thingy" );
      buffer->setValue( "price", 105.75 );
      cur.insert();
      savePoint.saveInsert( "id", buffer, &cur );

      cur.first();
      buffer = cur.primeUpdate();
      savePoint.saveEdit( "id", buffer, &cur );
      buffer->setValue( "name",  "Pepe" );
      cur.update();

      cur.last();
      buffer = cur.primeDelete();
      savePoint.saveDel( "id", buffer, &cur );
      cur.del();

      savePoint.undo(); // Deshace todas las operaciones anteriores
      \\endcode

    @author InfoSiAL S.L.
    """


class PNSqlSavePoint:

    """
    Pila para almacenar informacion de las operaciones.
    """

    opInfos: List[opInfo] = []

    """
    Identificador del punto de salvaguarda
    """
    id_ = None
    countRefSavePoint = 0
    """
    constructor.



    @param id Identificador para el punto de salvaguarda.
    """

    def __init__(self, _id=None) -> None:

        self.opInfos.append(opInfo())
        self.opInfos[0].setAutoDelete(True)

        if _id:
            self.id_ = _id
        else:
            self.id_ = self.opInfos[0]

        self.countRefSavePoint = self.countRefSavePoint + 1

    """
    destructor.
    """

    def __del__(self) -> None:
        if self.opInfos:
            self.opInfos = []

        self.countRefSavePoint = self.countRefSavePoint - 1

    """
    Establece el identificador del punto de salvaguarda.
    """

    def setId(self, id_) -> None:
        self.id_ = id_

    """
    Obtiene el identificador del punto de salvaguarda.
    """

    def id(self) -> Any:
        return self.id_

    """
    Limpia el punto de salvaguarda.

    Todas las operaciones almacenadas son eliminadas, por lo tanto, despues de
    invocar a este método ya no se podrán deshacer.
    """

    def clear(self) -> None:
        self.opInfos.clear()

    """
    Deshace el punto de salvaguarda.
    """

    @decorators.BetaImplementation
    def undo(self):

        while self.opInfos:
            opInf = self.opInfos.pop()
            if opInf.op == 0:
                self.undoInsert(opInf)
            if opInf.op == 1:
                self.undoEdit(opInf)
            if opInf.op == 2:
                self.undoDel(opInf)
            del opInf
        self.clear()

    """
    Guarda el buffer con el contenido del registro insertado.

    @param primaryKey Nombre del campo que es clave primaria.
    @param buffer buffer con el contenido del registro.
    @param cursor Cursor asociado.
    """

    @decorators.BetaImplementation
    def saveInsert(self, primaryKey, buffer, cursor):
        if not cursor or not buffer:
            return
        self.opInfos.append(
            opInfo(
                primaryKey,
                0,
                buffer,
                cursor.at(),
                cursor.sort(),
                cursor.filter(),
                cursor.name,
                cursor,
            )
        )

    """
    Guarda el buffer con el contenido del registro a editar.

    @param primaryKey Nombre del campo que es clave primaria.
    @param buffer buffer con el contenido del registro.
    @param cursor Cursor asociado.
    """

    def saveEdit(self, primaryKey, buffer, cursor) -> None:
        if not cursor or not buffer:
            return

        self.opInfos.append(
            opInfo(
                primaryKey,
                1,
                buffer,
                cursor.at(),
                cursor.sort(),
                cursor.filter(),
                cursor.name,
                cursor,
            )
        )

    """
    Guarda el buffer con el contenido del registro a borrar.

    @param primaryKey Nombre del campo que es clave primaria.
    @param buffer buffer con el contenido del registro.
    @param cursor Cursor asociado.
    """

    @decorators.BetaImplementation
    def saveDel(self, primaryKey, buffer, cursor):
        if not cursor or not buffer:
            return
        self.opInfos.append(
            opInfo(
                primaryKey,
                2,
                buffer,
                cursor.at(),
                cursor.sort(),
                cursor.filter(),
                cursor.name,
                cursor,
            )
        )

    """
    Deshace una operacion de insertar.

    @param opInf Información de la operación.
    """

    @decorators.BetaImplementation
    def undoInsert(self, opInf):

        cursor_ = opInf.cursor
        owner = False
        if not cursor_:
            from . import pnsqlcursor

            cursor_ = pnsqlcursor.PNSqlCursor(opInf.name)
            cursor_.setForwardOnly(True)
            owner = True

        if not cursor_:
            return

        if opInf.buffer.contains(opInf.primaryKey) and not opInf.buffer.isNull(
            opInf.primaryKey
        ):
            valuePrimaryKey = str(
                opInf.buffer.value(opInf.primaryKey)
            )  # FIXME: (deavid) plz add notes on what needs to be fixed here.
            ok = cursor_.select(opInf.primaryKey + "='" + valuePrimaryKey + "'")
            if ok and cursor_.next():
                cursor_.primeDelete()

        if not owner:
            cursor_.select(opInf.filter, opInf.sort)
            cursor_.seek(opInf.at)

    """
    Deshace una operacion de editar.

    @param opInf Información de la operación.
    """

    @decorators.BetaImplementation
    def undoEdit(self, opInf):
        cursor_ = opInf.cursor
        owner = False

        if not cursor_:
            from . import pnsqlcursor

            cursor_ = pnsqlcursor.PNSqlCursor(opInf.name)
            cursor_.setForwardOnly(True)
            owner = True

        if not cursor_:
            return
        valuePrimaryKey = str(opInf.buffer.value(opInf.primaryKey))
        ok = cursor_.select(opInf.primaryKey + "='" + valuePrimaryKey + "'")
        if ok and cursor_.next():
            # buf = cursor_.primeUpdate()
            # buf = opInf.buffer
            cursor_.primeUpdate()
            cursor_.update()

        if not owner:
            cursor_.select(opInf.filter, opInf.sort)
            cursor_.seek(opInf.at)
        else:
            del cursor_

    """
    Deshace una operacion de borrar.

    @param opInf Información de la operación.
    """

    @decorators.BetaImplementation
    def undoDel(self, opInf):
        cursor_ = opInf.cursor
        owner = False
        if not cursor_:
            from . import pnsqlcursor

            cursor_ = pnsqlcursor.PNSqlCursor(opInf.name)
            cursor_.setForwardOnly(True)
            owner = True

        if not cursor_:
            return

        # buf = cursor_.primeInsert()
        # buf = opInf.buffer
        cursor_.primeInsert()
        cursor_.insert()

        if not owner:
            cursor_.select(opInf.filter, opInf.sort)
            cursor_.seek(opInf.at)
        else:
            del cursor_
