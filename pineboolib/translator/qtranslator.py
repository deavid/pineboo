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
        """
        for ( ;; ) {
            QTranslatorMessage m( s );
            if ( m.hash() == 0 )
                break;
            d->messages->insert( m, (void *) 0 );
            }
        """

    def squeeze(self, mode):
        """
        {
    if ( !d->messages ) {
    if ( mode == Stripped )
        unsqueeze();
    else
        return;
    }

    QMap<QTranslatorMessage, void *> * messages = d->messages;

    d->messages = 0;
    clear();

    d->messageArray = new QByteArray;
    d->offsetArray = new QByteArray;

    QMap<QTranslatorPrivate::Offset, void *> offsets;

    QDataStream ms( *d->messageArray, IO_WriteOnly );
    QMap<QTranslatorMessage, void *>::Iterator it = messages->begin(), next;
    int cpPrev = 0, cpNext = 0;
    for ( it = messages->begin(); it != messages->end(); ++it ) {
    cpPrev = cpNext;
    next = it;
    ++next;
    if ( next == messages->end() )
        cpNext = 0;
    else
        cpNext = (int) it.key().commonPrefix( next.key() );
    offsets.replace( QTranslatorPrivate::Offset(it.key(),
             ms.device()->at()), (void*)0 );
    it.key().write( ms, mode == Stripped,
            (QTranslatorMessage::Prefix) QMAX(cpPrev, cpNext + 1) );
    }

    d->offsetArray->resize( 0 );
    QMap<QTranslatorPrivate::Offset, void *>::Iterator offset;
    offset = offsets.begin();
    QDataStream ds( *d->offsetArray, IO_WriteOnly );
    while ( offset != offsets.end() ) {
    QTranslatorPrivate::Offset k = offset.key();
    ++offset;
    ds << (Q_UINT32)k.h << (Q_UINT32)k.o;
    }

    if ( mode == Stripped ) {
    QAsciiDict<int> contextSet( 1511 );
    int baudelaire;

    for ( it = messages->begin(); it != messages->end(); ++it )
        contextSet.replace( it.key().context(), &baudelaire );

    Q_UINT16 hTableSize;
    if ( contextSet.count() < 200 )
        hTableSize = ( contextSet.count() < 60 ) ? 151 : 503;
    else if ( contextSet.count() < 2500 )
        hTableSize = ( contextSet.count() < 750 ) ? 1511 : 5003;
    else
        hTableSize = 15013;

    QIntDict<char> hDict( hTableSize );
    QAsciiDictIterator<int> c = contextSet;
    while ( c.current() != 0 ) {
        hDict.insert( (long) (elfHash(c.currentKey()) % hTableSize),
              c.currentKey() );
        ++c;
    }

    /*
      The contexts found in this translator are stored in a hash
      table to provide fast lookup. The context array has the
      following format:

          Q_UINT16 hTableSize;
          Q_UINT16 hTable[hTableSize];
          Q_UINT8  contextPool[...];

      The context pool stores the contexts as Pascal strings:

          Q_UINT8  len;
          Q_UINT8  data[len];

      Let's consider the look-up of context "FunnyDialog".  A
      hash value between 0 and hTableSize - 1 is computed, say h.
      If hTable[h] is 0, "FunnyDialog" is not covered by this
      translator. Else, we check in the contextPool at offset
      2 * hTable[h] to see if "FunnyDialog" is one of the
      contexts stored there, until we find it or we meet the
      empty string.
    */
    d->contextArray = new QByteArray;
    d->contextArray->resize( 2 + (hTableSize << 1) );
    QDataStream t( *d->contextArray, IO_WriteOnly );
    Q_UINT16 *hTable = new Q_UINT16[hTableSize];
    memset( hTable, 0, hTableSize * sizeof(Q_UINT16) );

    t << hTableSize;
    t.device()->at( 2 + (hTableSize << 1) );
    t << (Q_UINT16) 0; // the entry at offset 0 cannot be used
    uint upto = 2;

    for ( int i = 0; i < hTableSize; i++ ) {
        const char *con = hDict.find( i );
        if ( con == 0 ) {
        hTable[i] = 0;
        } else {
        hTable[i] = (Q_UINT16) ( upto >> 1 );
        do {
            uint len = (uint) qstrlen( con );
            len = QMIN( len, 255 );
            t << (Q_UINT8) len;
            t.writeRawBytes( con, len );
            upto += 1 + len;
            hDict.remove( i );
        } while ( (con = hDict.find(i)) != 0 );
        do {
            t << (Q_UINT8) 0; // empty string (at least one)
            upto++;
        } while ( (upto & 0x1) != 0 ); // offsets have to be even
        }
    }
    t.device()->at( 2 );
    for ( int j = 0; j < hTableSize; j++ )
        t << hTable[j];
    delete [] hTable;

    if ( upto > 131072 ) {
        qWarning( "QTranslator::squeeze: Too many contexts" );
        delete d->contextArray;
        d->contextArray = 0;
    }
    }
    delete messages;
}
        """
        pass

    def save_qm(self, file_name, mode):

        magic = {0x3c, 0xb8, 0x64, 0x18, 0xca, 0xef, 0x9c, 0x95, 0xcd, 0x21, 0x1c, 0xbf, 0x60, 0xa1, 0xbd, 0xdd}

        f = QtCore.QFile(file_name)
        if f.open(QtCore.QIODevice.WriteOnly):
            self.squeeze(mode)

        s = QtCore.QDataStream(f)
        # s.writeRawData(magic)

        tag = None

        """
        qtranslator.cpp
        {
    QFile f( filename );
    if ( f.open( IO_WriteOnly ) ) {
    squeeze( mode );

    QDataStream s( &f );
    s.writeRawBytes( (const char *)magic, MagicLength );
    Q_UINT8 tag;

    if ( d->offsetArray != 0 ) {
        tag = (Q_UINT8) QTranslatorPrivate::Hashes;
        Q_UINT32 oas = (Q_UINT32) d->offsetArray->size();
        s << tag << oas;
        s.writeRawBytes( d->offsetArray->data(), oas );
    }
    if ( d->messageArray != 0 ) {
        tag = (Q_UINT8) QTranslatorPrivate::Messages;
        Q_UINT32 mas = (Q_UINT32) d->messageArray->size();
        s << tag << mas;
        s.writeRawBytes( d->messageArray->data(), mas );
    }
    if ( d->contextArray != 0 ) {
        tag = (Q_UINT8) QTranslatorPrivate::Contexts;
        Q_UINT32 cas = (Q_UINT32) d->contextArray->size();
        s << tag << cas;
        s.writeRawBytes( d->contextArray->data(), cas );
    }
    return TRUE;
    }
    return FALSE;
}
        """
        return True

    def findMessage(self, context, source_text, comment):
        pass
        """
QTranslatorMessage QTranslator::findMessage( const char* context,
                         const char* sourceText,
                         const char* comment ) const
{
    if ( context == 0 )
    context = "";
    if ( sourceText == 0 )
    sourceText = "";
    if ( comment == 0 )
    comment = "";

#ifndef QT_NO_TRANSLATION_BUILDER
    if ( d->messages ) {
    QMap<QTranslatorMessage, void *>::ConstIterator it;

    it = d->messages->find( QTranslatorMessage(context, sourceText,
                           comment) );
    if ( it != d->messages->end() )
        return it.key();

    if ( comment[0] ) {
        it = d->messages->find( QTranslatorMessage(context, sourceText,
                               "") );
        if ( it != d->messages->end() )
        return it.key();
    }
    return QTranslatorMessage();
    }
#endif

    if ( !d->offsetArray )
    return QTranslatorMessage();

    /*
      Check if the context belongs to this QTranslator.  If many translators are
      installed, this step is necessary.
    */
    if ( d->contextArray ) {
    Q_UINT16 hTableSize = 0;
    QDataStream t( *d->contextArray, IO_ReadOnly );
    t >> hTableSize;
    uint g = elfHash( context ) % hTableSize;
    t.device()->at( 2 + (g << 1) );
    Q_UINT16 off;
    t >> off;
    if ( off == 0 )
        return QTranslatorMessage();
    t.device()->at( 2 + (hTableSize << 1) + (off << 1) );

    Q_UINT8 len;
    char con[256];
    for ( ;; ) {
        t >> len;
        if ( len == 0 )
        return QTranslatorMessage();
        t.readRawBytes( con, len );
        con[len] = '\0';
        if ( qstrcmp(con, context) == 0 )
        break;
    }
    }

    size_t numItems = d->offsetArray->size() / ( 2 * sizeof(Q_UINT32) );
    if ( !numItems )
    return QTranslatorMessage();

    if ( systemWordSize == 0 )
    qSysInfo( &systemWordSize, &systemBigEndian );

    for ( ;; ) {
    Q_UINT32 h = elfHash( QCString(sourceText) + comment );

    char *r = (char *) bsearch( &h, d->offsetArray->data(), numItems,
                    2 * sizeof(Q_UINT32),
                    systemBigEndian ? cmp_uint32_big
                    : cmp_uint32_little );
    if ( r != 0 ) {
        // go back on equal key
        while ( r != d->offsetArray->data() &&
            cmp_uint32_big(r - 8, r) == 0 )
        r -= 8;

        QDataStream s( *d->offsetArray, IO_ReadOnly );
        s.device()->at( r - d->offsetArray->data() );

        Q_UINT32 rh, ro;
        s >> rh >> ro;

        QDataStream ms( *d->messageArray, IO_ReadOnly );
        while ( rh == h ) {
        ms.device()->at( ro );
        QTranslatorMessage m( ms );
        if ( match(m.context(), context)
            && match(m.sourceText(), sourceText)
            && match(m.comment(), comment) )
            return m;
        if ( s.atEnd() )
            break;
        s >> rh >> ro;
        }
    }
    if ( !comment[0] )
        break;
    comment = "";
    }
    return QTranslatorMessage();
}
        """


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
