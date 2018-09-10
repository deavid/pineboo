# -*- coding: utf-8 -*-
import os
import logging

from PyQt5 import QtCore, QtXml, Qt


"""
Esta clase gestiona las diferenetes trducciones de módulos y aplicación
"""


class FLTranslations(QtCore.QObject):

    TML = None
    qmFileName = None

    """
    Constructor
    """

    def __init__(self):
        super(FLTranslations, self).__init__()
        self.logger = logging.getLogger("FLTranslations")

    """
    Si no existe el .qm convierte el .ts que le damos a .qm
    @param tor. Objeto clase metatranslator.
    @param tsFileName. Nombre del fichero .ts a convertir
    @param verbose. Muestra verbose (True, False)
    @return Boolean. Proceso realizado correctamente
    """

    def loadTsFile(self, tor, ts_file_name, verbose):
        qm_file_name = "%s.qm" % ts_file_name[:-3]
        ok = True
        if not os.path.exists(qm_file_name):
            ok = tor.load(ts_file_name)
            if not ok:
                self.logger.warn("For some reason, I cannot load '%s'", ts_file_name)
            return ok

        return True

    """
    Comprueba si el .qm se ha creado
    @param tor. Metatranslator
    @param qmFileName. Nombre del fichero .qm a comprobar
    @param verbose. Muestra verbose (True, False)
    @param stripped. No usado
    """

    def releaseMetaTranslator(self, tor, qm_file_name, verbose, stripped):
        if verbose:
            self.logger.debug("Updating '%s'...", qm_file_name)

        if not tor.release(qm_file_name, verbose, "Stripped" if stripped else "Everything"):
            self.logger.warn("For some reason, i cannot save '%s'", qm_file_name)

    """
    Libera el fichero .ts
    @param tsFileName. Nombre del fichero .ts
    @param verbose. Muestra verbose (True, False)
    @param stripped. no usado
    """

    def releaseTsFile(self, ts_file_name, verbose, stripped):
        tor = None
        if self.loadTsFile(tor, ts_file_name, verbose):
            qm_file_name = "%s.qm" % ts_file_name[:-3]
            self.releaseMetaTranslator(tor, qm_file_name, verbose, stripped)

    """
    Convierte el fichero .ts en .qm
    @param tsImputFile. Nombre del fichero .ts origen
    @param qmOutputFile. Nombre del fichero .qm destino
    @param stripped. No usado
    """

    def lrelease(self, ts_input_file, qm_output_file, stripped=True):
        verbose = False
        metTranslations = False
        tor = metaTranslator()

        f = Qt.QFile(ts_input_file)
        if not f.open(QtCore.QIODevice.ReadOnly):
            self.logger.warn("Cannot open file '%s'", ts_input_file)
            return

        t = Qt.QTextStream(f)
        full_text = t.readAll()
        f.close()

        if full_text.find("<!DOCTYPE TS>") >= 0:
            if qm_output_file is None:
                self.releaseTsFile(ts_input_file, verbose, stripped)
            else:
                if not self.loadTsFile(tor, ts_input_file, verbose):
                    return

        else:
            # modId = self.db_.managerModules().idModuleOfFile(tsInputFile)
            key = self.db_.managerModules().shaOfFile(ts_input_file)
            # dir = filedir("../tempdata/cache/%s/%s/file.ts/%s" %
            #               (self._prj.conn.db_name, modId, key))
            tagMap = full_text
            # TODO: hay que cargar todo el contenido del fichero en un diccionario
            for key, value in tagMap:
                toks = value.split(" ")

                for t in toks:
                    if key == "TRANSLATIONS":
                        metTranslations = True
                        self.releaseTsFile(t, verbose, stripped)

            if not metTranslations:
                self.logger.warn("Met no 'TRANSLATIONS' entry in project file '%s'", ts_input_file)

        if qm_output_file:
            print("***", qm_output_file)
            self.releaseMetaTranslator(tor, qm_output_file, verbose, stripped)


"""
Esta clase llama al conversor  de fichero .qs
"""


class metaTranslator(object):

    mm = {}

    def __init__(self):
        self.mm = {}
        self.logger = logging.getLogger("FLTranslations.metaTranslator")
    # TODO: Esto en producción seria necesario hacerlo desde el programa.
    """
    Conversor
    @param nombre fichero origen
    """

    def load(self, filename):
        f = QtCore.QFile(filename)
        if not f.open(QtCore.QIODevice.ReadOnly):
            return False

        #t = Qt.QTextStream(f)
        in_ = QtXml.QXmlInputSource(f)
        reader = QtXml.QXmlSimpleReader()
        reader.setFeature("http://xml.org/sax/features/namespaces", False)
        reader.setFeature("http://xml.org/sax/features/namespace-prefixes", False)
        hand = tsHandler(self)
        reader.setContentHandler(hand)
        reader.setErrorHandler(hand)

        ok = reader.parse(in_)
        reader.setContentHandler(None)
        reader.setErrorHandler(None)
        del hand
        f.close()
        return ok

    def release(self, file_name, verbose, mode):
        tor = {}
        finished = 0
        unfinished = 0
        untranslated = 0

        for m in self.mm:
            if m.type_() != MetaTranslatorMessage.Obsolete:
                if m.translation() is None:
                    untranslated += 1
                else:
                    if m.type_() == MetaTranslatorMessage.Unfinished:
                        unfinished += 1
                    else:
                        finished += 1

                    context = m.context()
                    source_text = m.sourceText()
                    comment = m.comment()
                    translation = m.translation()

                    # or not tor.findMessage(context, source_text, "").translation().isNull():
                    if comment is None or self.contains(context, source_text, ""):

                        tor[m] = m
                    else:
                        tor[m] = MetaTranslatorMessage(context, source_text, "", translation)

        saved = self.save_qm(tor, file_name, mode)
        if saved and verbose:
            self.logger.warn("%d finished, %d unfinished and %d untranslated messages" %
                             finished, unfinished, untranslated)

        return saved

    def contains(self, context, source_text, comment):
        size_ = len(self.mm)
        pos = 1
        for item in self.mm.keys():
            if self.mm[item].context() == context and self.mm[item].sourceText() == source_text and self.mm[item].comment() == comment:
                if size_ > 0:
                    if size_ == pos:
                        return False
                    else:
                        return True

        return False

    def insert(self, m):

        self.mm[m] = m

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

    def save_qm(self, tor, file_name, mode):
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


def encoding_is_utf8(atts):
    for i in range(atts.length()):
        if atts.qName(i) == "utf8":
            return atts.value(i) == "true"
        elif atts.qName(i) == "encoding":
            return atts.value(i) == "UTF-8"

    return False


class tsHandler(QtXml.QXmlDefaultHandler):
    tor = None
    type_ = None
    in_message = False
    ferror_count = 0
    context_is_utf8 = False
    message_is_utf8 = False
    accum = ""

    context = None
    source = None
    comment = None
    translation = None

    def __init__(self, translator):
        super(tsHandler, self).__init__()

        self.tor = translator
        self.type_ = MetaTranslatorMessage.Finished
        self.in_message = False
        self.ferror_count = 0
        self.context_is_utf8 = False
        self.message_is_utf8 = False
        self.accum = ""

    def startElement(self, name_space_uri, local_name, qname, atts):
        if qname == "byte":
            for i in range(atts.length()):
                if atts.qName(i) == "value":
                    value = atts.value(i)
                    base = 10
                    if value.startswith("x"):
                        base = 16
                        value = value[1:]

                    n = int(0, base)
                    if n is not 0:
                        self.accum += str(n)

        elif qname == "context":
            self.context = ""
            self.source = ""
            self.comment = ""
            self.translation = ""
            #context.truncate( 0 );
            #source.truncate( 0 );
            #comment.truncate( 0 );
            #translation.truncate( 0 );
            self.context_is_utf8 = encoding_is_utf8(atts)
        elif qname == "message":
            self.in_message = True
            self.type_ = MetaTranslatorMessage.Finished
            self.source = ""
            self.comment = ""
            self.translation = ""
            #source.truncate( 0 );
            #comment.truncate( 0 );
            #translation.truncate( 0 );
            self.message_is_utf8 = encoding_is_utf8(atts)
        elif qname == "translation":
            for i in range(atts.length()):
                if atts.qName(i) == "type":
                    if atts.value(i) == "unfinished":
                        self.type_ = MetaTranslatorMessage.Unfinished
                    elif atts.value(i) == "obsolete":
                        self.type_ = MetaTranslatorMessage.Obsolete
                    else:
                        self.type_ = MetaTranslatorMessage.Finished

        #accum.truncate( 0 )
        self.accum = ""
        return True

    def endElement(self, name_space_uri, local_name, qname):
        if qname in ("codec", "defaultcodec"):
            self.tor.setCodec(self.accum)
        elif qname == "name":
            self.context = self.accum
        elif qname == "source":
            self.source = self.accum
        elif qname == "comment":
            if self.in_message:
                self.comment = self.accum
            else:
                if self.context_is_utf8:
                    self.tor.insert(MetaTranslatorMessage(self.context.decode("utf-8"), context_comment,
                                                          self.accum.encode("UTF-8"), None, True, MetaTranslatorMessage.Unfinished))
                else:
                    self.tor.insert(MetaTranslatorMessage(self.context, context_comment,
                                                          self.accum, None, True, MetaTranslatorMessage.Unfinished))

        elif qname == "translation":
            self.translation = self.accum
        elif qname == "message":
            if self.message_is_utf8:
                self.tor.insert(MetaTranslatorMessage(self.context.encode("UTF-8"), self.source.encode("UTF-8"),
                                                      self.comment.encode("UTF-8"), self.translation, True, self.type_))
            else:
                self.tor.insert(MetaTranslatorMessage(self.context, self.source,
                                                      self.comment, self.translation, True, self.type_))

            self.in_message = False

        return True

    def characters(self, ch):
        t = ch.replace("\r", "")
        self.accum += t
        return True

    # def fatalError(self, exception):
    #    print(self.ferror_count)


class MetaTranslatorMessage(QtCore.QObject):

    utf8_ = False
    ty_ = None
    Obsolete = 0
    Unfinished = 1
    Finished = 2

    translation_ = None
    context_ = None
    source_text_ = None
    comment_ = None

    def __init__(self, context, source_text=None, comment=None, translation=None, utf8=False, type_=1):

        super(MetaTranslatorMessage, self).__init__()

        if isinstance(context, metaTranslator):
            self.mm = m.mm
            self.codec_name = tor.codec_name
            self.codec = tor.codec
            return

        self.context_ = context
        self.source_text_ = source_text
        self.comment_ = comment
        self.translation_ = translation

        self.utf8_ = False
        self.ty_ = type_

    def setType(self, nt):
        self.ty_ = nt

    def translation(self):
        return self.translation_

    def sourceText(self):
        return self.source_text_

    def comment(self):
        return self.comment_

    def context(self):
        return self.context_

    def type_(self):
        return self.ty_

    def utf8(self):
        return self.utf8_

    def operator_is(self, m):
        if isinstance(m, metaTranslator):
            self.mm = m.mm
            self.codec_name = m.codec_name
            self.codec = m.codec
        else:
            self.utf8_ = m.utf8_
            self.ty_ = m.ty_

        return self

    def operator_isequal(self, m):
        return context() == m.context() and self.source_text() == m.source_text() and self.comment() == m.comment()

    def operator_minus(self, m):
        delta = self.context() == m.context()
        if delta:
            delta = self.source_text() == m.source_text()
        if delta:
            delta = self.comment() == m.comment()

        return delta


"""
Devuelve la traducción si existe
"""


class FLTranslate(QtCore.QObject):

    group_ = None
    context_ = None
    pos_ = 0

    """
    Constructor
    @param Group. Grupo al que pertenece la traducción
    @param context. Texto a traducir
    @param Translate. Boolean que indica si se traduce realmente el texto pasado
    @param pos. Posición en la que se empieza a sustituir los argumentos pasados
    """

    def __init__(self, group, context, translate=True, pos=1):
        super(FLTranslate, self).__init__()
        self.pos_ = pos
        self.group_ = group
        if translate:
            self.context_ = Qt.qApp.translate(group, context)
        else:
            self.context_ = context

    """
    Argumento pasado a la traducción
    @param value. Texto a añadir a la traducción
    """

    def arg(self, value):
        if isinstance(value, list):
            for f in value:
                self.context_ = self.context_.replace(
                    "%s" % self.pos_, str(f))
                self.pos_ = self.pos_ + 1
        else:
            self.context_ = self.context_.replace(
                "%s" % self.pos_, str(value))

        return FLTranslate(self.group_, self.context_, False, self.pos_ + 1)

    """
    Retorna el valor traducido
    @return traducción completada con los argumentos
    """

    def __str__(self):
        return self.context_
