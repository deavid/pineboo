# -*- coding: utf-8 -*-

from PyQt5 import QtXml, QtCore  # type: ignore
from pineboolib import logging
from typing import Any

_TMetaTranslatorMessage = "MetaTranslatorMessage"


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

    def load(self, filename) -> Any:
        f = QtCore.QFile(filename)
        if not f.open(QtCore.QIODevice.ReadOnly):
            return False

        # t = Qt.QTextStream(f)
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

    def release(self, file_name, verbose, mode) -> bool:
        from pineboolib.translator.qtranslator import QTranslator

        tor = QTranslator(None)
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

                        tor.insert(m)
                    else:
                        tor.insert(MetaTranslatorMessage(context, source_text, "", translation))

        saved = tor.save_qm(file_name, mode)
        if saved and verbose:
            self.logger.warning("%d finished, %d unfinished and %d untranslated messages" % finished, unfinished, untranslated)

        return saved

    def contains(self, context, source_text, comment) -> bool:
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

    def insert(self, m) -> None:

        self.mm[m] = m


def encoding_is_utf8(atts) -> Any:
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

    def __init__(self, translator) -> None:
        super(tsHandler, self).__init__()

        self.tor = translator
        self.type_ = MetaTranslatorMessage.Finished
        self.in_message = False
        self.ferror_count = 0
        self.context_is_utf8 = False
        self.message_is_utf8 = False
        self.accum = ""

    def startElement(self, name_space_uri, local_name, qname, atts) -> bool:
        if qname == "byte":
            for i in range(atts.length()):
                if atts.qName(i) == "value":
                    value = atts.value(i)
                    base = 10
                    if value.startswith("x"):
                        base = 16
                        value = value[1:]

                    n = int(base)
                    if n != 0:
                        self.accum += str(n)

        elif qname == "context":
            self.context = ""
            self.source = ""
            self.comment = ""
            self.translation = ""
            # context.truncate( 0 );
            # source.truncate( 0 );
            # comment.truncate( 0 );
            # translation.truncate( 0 );
            self.context_is_utf8 = encoding_is_utf8(atts)
        elif qname == "message":
            self.in_message = True
            self.type_ = MetaTranslatorMessage.Finished
            self.source = ""
            self.comment = ""
            self.translation = ""
            # source.truncate( 0 );
            # comment.truncate( 0 );
            # translation.truncate( 0 );
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

        # accum.truncate( 0 )
        self.accum = ""
        return True

    def endElement(self, name_space_uri, local_name, qname) -> bool:
        context_comment = None  # FIXME: De donde sale esta variable?
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
                    self.tor.insert(
                        MetaTranslatorMessage(
                            self.context.decode("utf-8"),
                            context_comment,
                            self.accum.encode("UTF-8"),
                            None,
                            True,
                            MetaTranslatorMessage.Unfinished,
                        )
                    )
                else:
                    self.tor.insert(
                        MetaTranslatorMessage(self.context, context_comment, self.accum, None, True, MetaTranslatorMessage.Unfinished)
                    )

        elif qname == "translation":
            self.translation = self.accum
        elif qname == "message":
            if self.message_is_utf8:
                self.tor.insert(
                    MetaTranslatorMessage(
                        self.context.encode("UTF-8"),
                        self.source.encode("UTF-8"),
                        self.comment.encode("UTF-8"),
                        self.translation,
                        True,
                        self.type_,
                    )
                )
            else:
                self.tor.insert(MetaTranslatorMessage(self.context, self.source, self.comment, self.translation, True, self.type_))

            self.in_message = False

        return True

    def characters(self, ch: str) -> bool:
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

    def __init__(self, context, source_text=None, comment=None, translation=None, utf8=False, type_=1) -> None:

        super(MetaTranslatorMessage, self).__init__()

        if isinstance(context, metaTranslator):
            self.mm = context.m.mm
            self.codec_name = context.tor.codec_name
            self.codec = context.tor.codec
            return

        self.context_ = context
        self.source_text_ = source_text
        self.comment_ = comment
        self.translation_ = translation

        self.utf8_ = False
        self.ty_ = type_

    def setType(self, nt) -> None:
        self.ty_ = nt

    def translation(self) -> Any:
        return self.translation_

    def sourceText(self) -> Any:
        return self.source_text_

    def comment(self) -> Any:
        return self.comment_

    def context(self) -> Any:
        return self.context_

    def type_(self) -> Any:
        return self.ty_

    def utf8(self) -> Any:
        return self.utf8_

    def operator_is(self: _TMetaTranslatorMessage, m) -> _TMetaTranslatorMessage:
        if isinstance(m, metaTranslator):
            self.mm = m.mm
            self.codec_name = m.codec_name
            self.codec = m.codec
        else:
            self.utf8_ = m.utf8_
            self.ty_ = m.ty_

        return self

    def operator_isequal(self, m) -> Any:
        return self.context() == m.context() and self.source_text() == m.source_text() and self.comment() == m.comment()

    def operator_minus(self, m) -> Any:
        delta = self.context() == m.context()
        if delta:
            delta = self.source_text() == m.source_text()
        if delta:
            delta = self.comment() == m.comment()

        return delta
