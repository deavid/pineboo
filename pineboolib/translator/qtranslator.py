# -*- coding: utf-8 -*-
from PyQt5 import QtCore
import logging



class QTranslator(QtCore.QObject):
    d = None

    def __init__(self, parent, name=None):
        self.logger = logging.getLogger(__name__)
        super(QTranslator, self).__init__(parent)
        if name:
            self.setObjectName(name)

        self.d = QTranslatorPrivate(self)

    def insert(self, message):
        self.unsquezze()
        for m in self.d.messages:
            if m == message:
                del m
                break

        self.d.messages.append(message)

    def unsquezze(self):

        if self.d.messages:
            return

        self.d.messages = []
        if not self.d.messageArray:
            return

        s = QtCore.QDataStream(self.d.messageArray, QtCore.QIODevice.ReadOnly)
        
        while True:
            if s.__hash__() == 0:
                break
            
            self.d.messages.append(m)

    def elfHash(self, name):
        
        k = None
        h = 0
        g = None
        
        if name:
            for k in range(len(name)):
                h = (h << 4 ) + (k + 1)
                g = (h & 0xf0000000)
                if g != 0:
                    h ^= g >> 24
                
                h &= ~g
        
        if not h:
            h = 1
        
        return h 



    def squeeze(self, mode):
        if not self.d.messages:
            if mode == "Stripped":
                self.unsquezze()
            else:
                return
        
        messages = []
        for m in self.d.messages:
            messages.append(m)
            
        self.d.messages.clear()
        
        self.clear()
        
        self.d.messageArray = QtCore.QByteArray()
        self.d.offsetArray = QtCore.QByteArray()
        print("Control 1-1. Squeeze", messages)
        offsets = {}
        
        ms = QtCore.QDataStream(self.d.messageArray, QtCore.QIODevice.WriteOnly)
        
        cp_prev = 0
        cp_next = 0
        

        for i in range(len(messages)):
            it = messages[i]
            cp_prev = cp_next
            next = it
            
            if i == len(messages) -1:
                cp_next = 0
            else:
                cp_next = i
                offsets[i] = cp_prev if cp_prev > (cp_next + 1) else cp_next + 1
            
        self.d.offsetArray.resize(0)
        
        ds = QtCore.QDataStream(self.d.offsetArray, QtCore.QIODevice.WriteOnly)
        for key in offsets.keys():
            offset = offsets[key]
            ds.writeUInt32(key)
            ds.writeUInt32(offset)
        
        if mode == "Stripped":
            context_set = {} #1511
            baudelaire = None
            
            for i in range(len(messages)):
                it = messages[i]
                context_set[i] = it.context()
                
            h_table_size = None
            
            print("Control 2 tamaño", len(context_set.keys()))
            if len(context_set.keys()) < 200:
                h_table_size = 151 if len(context_set.keys()) < 60 else 503
            elif len(context_set.keys()) < 2500:
                h_table_size = 1511 if len(context_set.keys()) < 750 else 5003
            else:
                h_table_size = 15013
        
            h_dict = [] 
                        
            print("Control 3 tamaño", len(context_set.items()))
            
            for item in context_set.items():
                h_dict.append(item)
            
            print("Control 4: %s " % (len(h_dict)))
            
            self.d.contextArray = QtCore.QByteArray()
            self.d.contextArray.resize(2 + (h_table_size << 1))
            t = QtCore.QDataStream(self.d.contextArray, QtCore.QIODevice.WriteOnly)
            h_table = {}

            for i in range(h_table_size):
                h_table[i] = 0
            
            t.writeUInt16(h_table_size)
            t.device().seek(2 + (h_table_size << 1))
            t.writeUInt16(0) 
            upto = 2
            
            print("Control 4 tamaño", h_table_size, len(h_dict))
            for i in range(h_table_size):
                if i in range(len(h_dict)):
                    print("*******", h_dict[i])
                    con = h_dict[i]
                else:
                    con = 0
                    
                if con == 0:
                    h_table[i] = 0
                else:
                    h_table[i] = (upto >> 1)
                    first = False
                    #Esta maaaaalll
                    while con != 0 or not fisrt:
                        len_ = len(con)
                        len_ = len_ if len_ < 255 else 255
                        t.writeUInt8(len_)
                        print("*", con[1])
                        t.writeQString(con[1])
                        upto += 1 + len_
                        del h_dict[i]
                        first = True
                    
                    first = False
                    while upto & 0x1 != 0 or first:
                    
                        t.writeUInt8(0)
                        upto += 1
                        first = True
            
            t.device().at(2)
            for j in h_table_size:
                t << h_table[j]
            
            h_table.clear()
            del h_table
            
            if upto > 131072:
                QtCore.qWarning("QTranslator::squeeze: Too many contexts")
                self.d.contextArray.clear()
        
        del messages
    
    def clear(self):
        pass
    
    

                
            
    def save_qm(self, file_name, mode):

        magic = {0x3c, 0xb8, 0x64, 0x18, 0xca, 0xef, 0x9c, 0x95, 0xcd, 0x21, 0x1c, 0xbf, 0x60, 0xa1, 0xbd, 0xdd}

        f = QtCore.QFile(file_name)
        if f.open(QtCore.QIODevice.WriteOnly):
            self.squeeze(mode)

            s = QtCore.QDataStream(f)
            s.writeBytes(magic)

            tag = None
        
            if self.d.offsetArray != 0:
                tag = QTranslatorPrivate.Hashes
                oas = self.d.offsetArray.size()
                s << tag << oas
                s.writeBytes(self.d.offsetArray.data())
        
            if self.d.messageArray != 0:
                tag = QTranslatorPrivate.Messages
                mas = self.d.messageArray.sizez()
                s << tag << mas
                s.writeBytes(self.d.messageArray.data())
        
            if self.d.contextArray != 0:
                tag = QTranslatorPrivate.Contexts
                cas = self.d.contextArray.size()
                s << tag << cas
                s.writeBytes(self.d.contextArray.data())
        
            return True
    
        return False

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
        
            r = bsearch(h, self.d.offsetArray.data(), numItems, 2 * sizeof(Q_UINT32), cmp_uint32_big if systemBigEndian else cmp_uint32_lite)
        
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


class QTranslatorPrivate(QtCore.QObject):

    def __init__(self, parent):
        super(QTranslatorPrivate, self).__init__(parent)

        self.messageArray = QtCore.QByteArray()
        self.offsetArray = QtCore.QByteArray()
        self.contextArray = QtCore.QByteArray()

        self.unmapPointer = 0
        self.unmapLength = 0

        self.messages = {}
        self.oldPermissionLookup = 0

        self.Contexts = 0x2f
        self.Hashes = 0x42
        self.Messages = 0x69


def Offset(*args):
    h = None
    o = None

    if len(args) == 0:
        h = 0
        o = 0

    if len(args) == 2:
        h = args[0].hash()
        o = args[1]

    else:
        return h < args[0].h if h != args[0].h else o < args[0].o
