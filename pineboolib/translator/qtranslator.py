# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from pineboolib import logging
from typing import Any, Sized, Tuple, List


class QTranslator(QtCore.QObject):
    d = None

    def __init__(self, parent, name=None) -> None:
        self.logger = logging.getLogger(__name__)
        super(QTranslator, self).__init__(parent)
        if name:
            self.setObjectName(name)

        self.d = QTranslatorPrivate(self)

    def insert(self, message) -> None:
        self.unsquezze()
        for m in self.d.messages:
            if m == message:
                del m
                break

        self.d.messages.append(message)

    def unsquezze(self) -> None:

        if self.d.messages:
            return

        self.d.messages = []
        if not self.d.messageArray:
            return

        s = QtCore.QDataStream(self.d.messageArray, QtCore.QIODevice.ReadOnly)

        while True:
            if s.__hash__() == 0:
                break

            # self.d.messages.append(m)  # noqa: FIXME: undefined m

    def elfHash(self, name: Sized) -> int:

        k = None
        h = 0
        g = None

        if name:
            for k in range(len(name)):
                h = (h << 4) + (k + 1)
                g = h & 0xF0000000
                if g != 0:
                    h ^= g >> 24

                h &= ~g

        if not h:
            h = 1

        return h

    def squeeze(self, mode) -> None:
        if not self.d.messages:
            if mode == "Stripped":
                self.unsquezze()
            else:
                return

        self.clear()

        self.d.messageArray = QtCore.QByteArray()
        self.d.offsetArray = QtCore.QByteArray()
        self.d.contextArray = QtCore.QByteArray()

        ds = QtCore.QDataStream(self.d.offsetArray, QtCore.QIODevice.WriteOnly)
        t = QtCore.QDataStream(self.d.contextArray, QtCore.QIODevice.WriteOnly)
        ms = QtCore.QDataStream(self.d.messageArray, QtCore.QIODevice.WriteOnly)

        messages = []
        offsets = {}
        contexts: List[Any] = []

        for m in self.d.messages:

            if m.type_() > 0 and m.sourceText() != "":  # Si Terminada
                # print("mensaje", m.context(), m.sourceText(), m.translation(), len(m.sourceText()), m.sourceText() == "", m.type_())
                messages.append(m)  # Añado mensaje

                if m.context() not in contexts:  # Si el context es nuevo
                    contexts.append(m.context())  # Añado context
                    offsets[m.context()] = obj_()
                    offsets[m.context()].k = 0
                    offsets[m.context()].o = 0

        # Aquí creamos offsets
        # | h 32       | o 32        |
        # | 00 00 00 00| 00 00 00 00 |

        for key in offsets.keys():
            ds.writeUInt32(offsets[key].h)  # Marca
            ds.writeUInt32(offsets[key].o)  # Incremental!!

        # | Init| len source  | sourceText (16 *char)         | len ctx (32) | context              | espacio | suma flag
        #   | value offset_context 32 bits | fin |
        # | 03  | 00 00 00 10 | 00 01 00 02 00 03 00 04 00 05 | 00 00 00 08  | 51 44 69 61 6C 6F 67 | 00      | 05
        #   | 00 00 00 00                  | 01  |

        # Aquí creamos msg
        for msg in messages:
            ms.writeUInt8(3)  # Nuevo msg
            ms.writeUInt32(len(msg.translation() * 2))
            for st in msg.translation():
                # print("***", st , type(st))
                ms.writeUInt8(0x0)
                ms.writeUInt8(st if isinstance(st, int) else ord(st))
                # if not msg.translation():
                #    ms.writeUInt8(0x07)
                # else:
                #    continue
                # Meter traduccion
            # ms.writeUInt32(len(m.context()) + 1)
            # for cc in m.context():
            # print(cc, type(cc), m.context(), len(m.context()) + 1)
            #    ms.writeUInt8(cc if isinstance(cc, int) else ord(cc))

            # ms.writeUInt8(0)
            ms.writeUInt8(5)

            ms.writeUInt32(offsets[m.context()].h)  # Aqui se mete el offset al que pertenece
            # ms.writeUInt32(0)
            ms.writeUInt8(1)

        # | len(ctx) | ctx 8 * char  | espacio |
        # | 05       | 01 02 03 04 05| 00 |

        # Aquí creamos contexts
        h_table_size = 0
        if len(contexts) < 200:
            h_table_size = 151 if len(contexts) < 60 else 503
        elif len(contexts) < 2500:
            h_table_size = 1511 if len(contexts) < 750 else 5003
        else:
            h_table_size = 15013

        t.writeUInt16(h_table_size)  # 1º table size
        t.device().seek(2 + (h_table_size << 1))  # 2º posicionado
        t.writeUInt16(0)  # Primer offset tiene q ser cero

        # Aumentamos tamaño de context hasta _table_size:
        # ampliar_context = h_table_size - len(contexts)
        # for i in range(ampliar_context):
        #    contexts.append(False)

        for ctx in contexts:
            if ctx is not False:
                t.writeInt8(len(ctx) if len(ctx) < 255 else 255)
                if len(ctx) == 255:
                    ctx = ctx[0:254]

                for c in ctx:
                    t.writeInt8(c if isinstance(c, int) else ord(c))

            t.writeInt8(0x0)

        del messages

    def clear(self) -> None:
        pass

    def save_qm(self, file_name, mode) -> bool:

        magic = [0x3C, 0xB8, 0x64, 0x18, 0xCA, 0xEF, 0x9C, 0x95, 0xCD, 0x21, 0x1C, 0xBF, 0x60, 0xA1, 0xBD, 0xDD]

        f = QtCore.QFile(file_name)
        if f.open(QtCore.QIODevice.WriteOnly):
            self.squeeze(mode)

            s = QtCore.QDataStream(f)
            for m in magic:
                s.writeUInt8(m)

            tag = None

            # print("*** context ", self.d.contextArray.data(), self.d.contextArray.size())
            # print("*** ofsets ", self.d.offsetArray.data(), self.d.offsetArray.size())
            # print("*** messages ", self.d.messageArray.data(), self.d.messageArray.size())

            if self.d.offsetArray is not None:
                tag = QTranslatorPrivate.Hashes
                oas = self.d.offsetArray.size()  # 42
                s.writeUInt8(tag)
                s.writeUInt32(oas)
                if self.d.offsetArray.size() > 0:
                    s.writeBytes(self.d.offsetArray.data())

            if self.d.messageArray is not None:
                tag = QTranslatorPrivate.Messages  # 69
                # mas = self.d.messageArray.size()
                s.writeUInt8(tag)
                # s.writeUInt32(mas)
                if self.d.messageArray.size() > 0:
                    s.writeBytes(self.d.messageArray.data())

            if self.d.contextArray is not None:
                tag = QTranslatorPrivate.Contexts  # 2f
                # cas = self.d.contextArray.size()
                s.writeUInt8(tag)
                # s.writeUInt32(cas)
                if self.d.contextArray.size() > 0:
                    s.writeBytes(self.d.contextArray.data())

            # s.writeUInt8(0x0)
            return True

        return False

    """
    def findMessage(self, context, source_text, comment):

        if context == 0:
            context = ""
        if source_text == 0:
            source_text = ""
        if comment == 0:
            comment = ""

        if self.d.messages:

            it = self.d.messages.find([context, source_text, comment])

            if it != self.d.messages[len(self.d.messages) -1 ]:
                return it.key()

            if (comment[0]):
                it = self.d.messages.find([context, source_text, comment])

                if it != self.d.messages[len(self.d.messages) -1]:
                    return it.key()

            return None

        if not self.d.offsetArray:
            return None


        if self.d.contextArray:
            h_table_size = 0
            t = QtCore.QDataStream(self.d.contextArray, QtCore.QIODevice.ReadOnly)
            t >> h_table_size
            g = elfHash(context) % h_table_size
            t.device().at(2 + (g << 1))
            off = None
            t >> off
            if off == 0:
                return None

            t.device().at(2 + (h_table_size << 1 ) + (off << 1))

            len = None
            con = []
            while True:
                t >> len
                if (len == 0):
                    return None
                t.readUInt8()
                con[len] = "\0"
                if con == context:
                    break

        number_items = len(self.d.offsetArray) / (2 * sizeof(Q_UINT32))
        if not number_items:
            return None

        if systemWordSize == 0:
            qSysInfo( systemWordSize, systemBigEndian )


        while True:
            h = elfHash(source_text + comment)

            r = bsearch(h, self.d.offsetArray.data(), numItems, 2 * sizeof(Q_UINT32),
             cmp_uint32_big if systemBigEndian else cmp_uint32_lite)

            if r != 0:
                while r != self.d.offsetArray.data() and cmp_uint32_big(r -8, r) == 0:
                    r -= 8


                s = QtCore.QDataStream(self.d.offsetArray, QtCore.QIODevice.ReadOnly)
                s.device().at(r - self.d.offsetArray.data())

                rh = None
                ro = None

                s >> rh >> ro

                ms = QtCore.QDataStream(self.d.messageArray, QtCore.QIODevice.ReadOnly)
                while rh == h:
                    ms.device().at(ro)
                    m = ms
                    if m.context() == context and m.sourceText() == source_text and m.comment() == comment:
                        return m

                    if s.atEnd():
                        break

                    s >> rh >> ro

            if not comment[0]:
                break

            comment = ""

        return None
    """


class QTranslatorPrivate(QtCore.QObject):

    Contexts = 0x2F
    Hashes = 0x42
    Messages = 0x69

    def __init__(self, parent) -> None:
        super(QTranslatorPrivate, self).__init__(parent)

        self.messageArray = QtCore.QByteArray()
        self.offsetArray = QtCore.QByteArray()
        self.contextArray = QtCore.QByteArray()

        self.unmapPointer = 0
        self.unmapLength = 0

        self.messages: List[Any] = []
        self.oldPermissionLookup = 0

    def Offset(*args) -> Tuple[Any, Any]:
        h = None
        o = None

        if len(args) == 0:
            h = 0
            o = 0

        if len(args) == 2:
            h = args[0].hash()
            o = args[1]

        return h, o  # FIXME: Cual es el proposito y firma de esta función?


class obj_(object):
    k = 0
    h = 0
    o = 0
