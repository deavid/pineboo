# -*- coding: utf-8 -*-
from pineboolib.utils import checkDependencies, filedir
import pineboolib

from xml import etree
import logging
import datetime


class kut2fpdf(object):

    _document = None  # Aquí se irán guardando los datos del documento
    logger = None
    _xml = None
    _xml_data = None
    _page_orientation = None
    _page_size = None
    _bottom_margin = None
    _left_margin = None
    _right_margin = None
    _top_margin = None
    _page_top = {}
    _data_row = None  # Apunta a la fila actual en data
    _parser_tools = None
    _avalible_fonts = []

    def __init__(self):

        self.logger = logging.getLogger("kut2rml")
        checkDependencies({"fpdf": "fpdf"})
        from pineboolib.plugins.kugar.parsertools import parsertools
        self._parser_tools = parsertools()

    def parse(self, name, kut, data):

        try:
            self._xml = self._parser_tools.loadKut(kut)
        except Exception:
            self.logger.exception(
                "KUT2FPDF: Problema al procesar %s.kut", name)
            return False

        try:
            self._xml_data = etree.ElementTree.fromstring(data)
        except Exception:
            self.logger.exception("KUT2FPDF: Problema al procesar xml_data")
            return False

        self.setPageFormat(self._xml)
        # self._page_orientation =
        # self._page_size =

        from fpdf import FPDF
        self._document = FPDF(self._page_orientation, "pt", self._page_size)

        # Cargamos las fuentes disponibles
        for f in self._document.core_fonts:
            self.logger.debug("KUT2FPDF :: Adding font %s", f)
            self._avalible_fonts.append(f)

        self.newPage()
        self.processDetails()

        pdfname = pineboolib.project.getTempDir()
        pdfname += "/%s_%s.pdf" % (name,
                                   datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

        # Datos del creador del documento
        self._document.set_title(name)
        self._document.set_author("Pineboo - kut2fpdf plugin")

        self._document.output(pdfname, 'F')

        return pdfname

    def topSection(self):
        return self._page_top[str(self._document.page_no())]

    def setTopSection(self, value):
        self._page_top[str(self._document.page_no())] = value

    """
    Añade una nueva página al documento.
    """

    def newPage(self):
        self._document.add_page(self._page_orientation)
        self._page_top[str(self._document.page_no())] = self._top_margin
        # self._document.set_margins(
        #    self._left_margin, self._top_margin, self._right_margin)
        # Corta con el borde inferior ...
        # self._document.set_auto_page_break(
        #    True, self._document.h - self._bottom_margin)

        self.processSection("PageHeader")

        # para sacar el número de página se puede usar self._document.page_no()
    """
    def pageFooter(self, xml, parent):
        frecuencia = int(self.getOption(xml, "PrintFrequency"))
        if frecuencia == 1 or self._document.page_no() == 1:  # Siempre o si es primera pagina
            #self.actualVSize[str(self.pagina)] = self.maxVSize[str(self.pagina)] + (self.getHeight(xml) - self.pageSize_["BM"]) * self.correcionAltura_
            self.actualVSize[str(self.pagina)] = self.maxVSize[str(self.pagina)] + self.getHeight(xml) * self.correcionAltura_
            #self.logger.warn("PAGE_FOOTER BOTTON %s" % self.actualVSize[str(self.pagina)])
            self.processXML(xml, parent)
    """
    """
    Procesa la cabecera del documento
    """

    def processDetails(self):
        # Procesamos la cabecera si procede ..
        prevLevel = 0
        for data in self._xml_data.findall("Row"):
            level = int(data.get("level"))
            if prevLevel > level:
                self.processData("DetailFooter", data, prevLevel)
            elif prevLevel < level:
                self.processData("DetailHeader",  data, level)

            self.processData("Detail", data, level)

            prevLevel = level

        for l in reversed(range(level + 1)):
            self.processData("DetailFooter", data, l)

        if self._xml.find("PageFooter"):
            self.processSection("PageFooter")
        elif self._xml.find("AddOnFooter"):
            self.processSection("AddOnFooter")

    def processData(self, section_name, data, data_level):
        listDF = self._xml.findall(section_name)
        for dF in listDF:
            if dF.get("Level") == str(data_level):
                if section_name == "Detail" and (not dF.get("DrawIf") or data.get(dF.get("DrawIf"))):
                    heightCalculated = self._parser_tools.getHeight(
                        dF) + self.topSection()
                    for dFooter in self._xml.findall("DetailFooter"):
                        if dFooter.get("Level") == str(data_level):
                            heightCalculated += self._parser_tools.getHeight(
                                dFooter)
                    pageFooter = self._xml.get("PageFooter")
                    if pageFooter:
                        if self._document.page_no() == 1 or pageFooter.get("PrintFrecuency") == "1":
                            heightCalculated += self._parser_tools.getHeight(
                                pageFooter)

                    heightCalculated += self._bottom_margin

                    if heightCalculated > self._document.h:  # Si nos pasamos
                        self.processSection("PageFooter")  # Pie de página
                        self.newPage()

                if not dF.get("DrawIf") or data.get(dF.get("DrawIf")):
                    self.processXML(dF, data)
                    #self.logger.debug("%s_BOTTON = %s" % (name.upper(), self.actualVSize[str(self.pagina)]))

    def processSection(self, name):
        sec_ = self._xml.find(name)
        if sec_:
            # Siempre o si es primera pagina
            if sec_.get("PrintFrequency") == "1" or self._document.page_no() == 1:
                if sec_.tag == "PageFooter":
                    self.setTopSection(self._document.h -
                                       int(sec_.get("Height")))
                self.processXML(sec_)

    """
    Procesa un elemento de xml
    @param xml: El elemento a procesar
    """

    def processXML(self, xml, data=None):
        fix_height = True
        if xml.tag == "DetailFooter":
            if xml.get("PlaceAtBottom") == "true":
                self.setTopSection(self.topSection() +
                                   self._parser_tools.getHeight(xml))

        if xml.tag == "PageFooter":
            fix_height = False

        for child in xml.iter():
            if child.tag in ("Label", "Field", "Special", "CalculatedField"):
                self.processText(child, data, fix_height)
            elif child.tag == "Line":
                self.processLine(child, fix_height)

        if xml.get("PlaceAtBottom") != "true":
            self.setTopSection(self.topSection() +
                               self._parser_tools.getHeight(xml))

    def processLine(self, xml, fix_height=True):

        color = xml.get("Color")
        r = 0 if not color else int(color.split(",")[0])
        g = 0 if not color else int(color.split(",")[1])
        b = 0 if not color else int(color.split(",")[2])

        style = int(xml.get("Style"))
        width = int(xml.get("Width"))
        X1 = self.calculateLeftStart(xml.get("X1"))
        X2 = self.calculateRightEnd(xml.get("X2"))
        # Ajustar altura a secciones ya creadas
        Y1 = int(xml.get("Y1")) + self.topSection()
        Y2 = int(xml.get("Y2")) + self.topSection()
        if fix_height:
            Y1 = self._parser_tools.heightCorrection(Y1)
            Y2 = self._parser_tools.heightCorrection(Y2)
        self._document.set_line_width(width)
        self._document.set_draw_color(r, g, b)
        self._document.line(X1, Y1, X2, Y2)

    def calculateLeftStart(self, x):
        x = int(x)
        ret_ = x
        if x < self._left_margin:
            ret_ = self._left_margin

        return ret_

    def calculateRightEnd(self, y):
        y = int(y)
        ret_ = y
        if y > (self._document.w - self._right_margin):
            ret_ = self._document.w - self._right_margin

        return ret_

    def processText(self, xml, data_row=None, fix_height=True):
        isImage = False
        text = xml.get("Text")
        BorderWidth = int(xml.get("BorderWidth"))
        borderColor = xml.get("BorderColor")

        W = int(xml.get("Width"))
        H = self._parser_tools.getHeight(xml)

        x = int(xml.get("X"))
        # Añade la altura que hay ocupada por otras secciones
        y = int(xml.get("Y")) + self.topSection()
        if fix_height:
            y = self._parser_tools.heightCorrection(y)

        dataType = xml.get("Datatype")

        if xml.tag == "Field" and data_row is not None:
            text = data_row.get(xml.get("Field"))

        elif xml.tag == "Special":
            text = self._parser_tools.getSpecial(
                text[1:len(text) - 1], self._document.page_no())

        elif xml.tag == "CalculatedField":
            if xml.get("FunctionName"):
                function_name = xml.get("FunctionName")
                try:
                    nodo = self._parser_tools.convertToNode(data_row)
                    text = str(pineboolib.project.call(function_name, [nodo]))
                except Exception:
                    self.logger.exception(
                        "KUT2FPDF:: Error llamando a function %s", function_name)
                    return
            else:
                if data_row is None:
                    data_row = self._xml_data[0]
                if xml.get("Field"):
                    text = data_row.get(
                        xml.get("Field")) if not "None" else ""

            if text and dataType is not None:
                text = self._parser_tools.calculated(text, int(dataType), xml.get("Precision"), data_row)

            if dataType == "5":
                isImage = True

        if text and text.startswith(filedir("../tempdata")):
            isImage = True

        precision = xml.get("Precision")
        negValueColor = xml.get("NegValueColor")
        Currency = xml.get("Currency")

        commaSeparator = xml.get("CommaSeparator")
        dateFormat = xml.get("DateFormat")

        if not isImage:

            self.drawText(x, y, W, H, xml, text)
        else:
            self.drawImage(x, y, W, H, xml, text)

    def drawText(self, x, y, W, H, xml, txt):

        if txt in ("None", None):
            return

        # Corregimos margenes:
        x = self.calculateLeftStart(x)
        W = self.calculateRightEnd(x + W) - x

        bg_color = xml.get("BackgroundColor").split(",")
        fg_color = xml.get("ForegroundColor").split(",")

        self._document.set_text_color(
            int(fg_color[0]), int(fg_color[1]), int(fg_color[2]))
        self._document.set_fill_color(
            int(bg_color[0]), int(bg_color[1]), int(bg_color[2]))

        if xml.get("BorderStyle") == "1":
            # FIXME: Hay que ajustar los margenes
            self.drawRect(x, y, W, H)
            # FIXME: Hay que recalcular la posición para dejarlo centrado al
            # rectangulo

        #font_name, font_size, font_style
        font_style = ""
        font_size = int(xml.get("FontSize"))
        font_name = xml.get("FontFamily").lower()

        fontW = int(xml.get("FontWeight"))
        fontI = xml.get("FontItalic")
        fontU = xml.get("FontUnderlined")  # FIXME: hay que ver si es así

        if fontW > 60 and font_size > 10:
            font_style += "B"

        if fontI == "1":
            font_style += "I"

        if fontU == "1":
            font_style += "U"

        while font_name not in self._avalible_fonts:
            self.logger.warning(
                "KUT2PDF:: Falta el tipo de letra %s", font_name)
            font_name = "helvetica"

        self._document.set_font(font_name, font_style, font_size)

        # Corregir alineación
        VAlignment = xml.get("VAlignment")  # 0 izquierda, 1 centrado,2 derecha
        HAlignment = xml.get("HAlignment")

        if HAlignment == "1":  # sobre X
            # Centrado
            x = x + (W / 2) - (self._document.get_string_width(txt) / 2)
        elif HAlignment == "2":
            # Derecha
            x = x + W - self._document.get_string_width(txt)
        else:
            # Izquierda
            x = x

        if VAlignment == "1":  # sobre Y
            # Centrado
            y = (y + H / 2) + (self._document.font_size_pt / 2)
        elif VAlignment == "2":
            # Abajo
            y = y + W - font_size
        else:
            # Arriba
            y = y

        self._document.text(x, y, txt)

    def drawRect(self, x, y, W, H):
        self._document.rect(x, y, W, H, "DF")

    def drawImage(self, x, y, W, H, xml, file_name):

        self._document.image(file_name, x, y, W, H, "PNG")

    # def addFont(self, name, style, fname, uni):
    #    self._document.add_font(name, style, fname, uni)

    """
    Define los parámetros de la página
    @param xml: Elemento xml con los datos del fichero .kut a procesar
    """

    def setPageFormat(self, xml):
        custom_size = None

        self._bottom_margin = int(xml.get("BottomMargin"))
        self._left_margin = int(xml.get("LeftMargin"))
        self._right_margin = int(xml.get("RightMargin"))
        self._top_margin = int(xml.get("TopMargin"))

        page_size = int(xml.get("PageSize"))
        page_orientation = xml.get("PageOrientation")

        if page_size in [30, 31]:
            custom_size = [int(xml.get("CustomHeightMM")),
                           int(xml.get("CustomWidthMM"))]

        self._page_orientation = "P" if page_orientation == "0" else "L"

        self._page_size = self._parser_tools.converPageSize(
            page_size, int(page_orientation), custom_size)  # devuelve un array
