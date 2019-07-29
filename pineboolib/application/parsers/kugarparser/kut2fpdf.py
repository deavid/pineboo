# -*- coding: utf-8 -*-
"""
KUT2FPDF module.

Creates a pdf representation of a KUT
"""
import datetime
import re
import os
from xml.etree.ElementTree import Element
from pineboolib.application import project
from pineboolib import logging
from pineboolib.core.utils.utils_base import filedir, load2xml
from pineboolib.application.utils.check_dependencies import check_dependencies
from pineboolib.application.parsers.kugarparser.parsertools import KParserTools
from pineboolib.core.settings import config


from typing import Any, Optional, Union, List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from fpdf import FPDF  # type: ignore


class Kut2FPDF(object):
    """
    Convert kuts to pyFPDF.
    """

    _document: "FPDF"

    _xml: Element
    _xml_data: Element
    _page_orientation: str
    _page_size: List[int]
    _bottom_margin: int
    _left_margin: int
    _right_margin: int
    _top_margin: int
    _page_top: Dict[int, int]
    _data_row: Element
    _parser_tools: KParserTools
    _avalible_fonts: List[str]
    _unavalible_fonts: List[str]
    design_mode: bool
    _actual_data_line: Optional[Element]
    _no_print_footer: bool
    _actual_section_size: int
    increase_section_size: int
    last_detail: bool
    actual_data_level: int
    last_data_processed: Element
    prev_level: int
    draws_at_header: Dict[str, str]
    detailn: Dict[str, int]
    name_: str
    _actual_append_page_no: int
    reset_page_count: bool

    def __init__(self) -> None:
        """Constructor."""

        self.logger = logging.getLogger("kut2fpdf")
        check_dependencies({"fpdf": "fpdf2"})

        self._parser_tools = KParserTools()
        self._avalible_fonts = []
        self._page_top: Dict[int, int] = {}
        self._unavalible_fonts = []
        self.design_mode = config.value("ebcomportamiento/kugar_debug_mode", False)
        self._actual_data_line = None
        self._no_print_footer = False
        self.increase_section_size = 0
        self.actual_data_level = 0
        self.prev_level = -1
        self.draws_at_header = {}
        self.detailn = {}
        self.name_ = ""
        self._actual_append_page_no = -1
        self.reset_page_count = False
        self.new_page = False

    def parse(self, name: str, kut: str, data: str, report: FPDF = None, flags: List[int] = []) -> Optional[str]:
        """
        Parse string containing ".kut" file into a pdf and return its file path.

        @param name. Filename path for ".kut".
        @param kut. String with ".kut" file contents.
        @param data. String with data to be used in the report.
        @return Path to PDF file.
        """
        try:
            self._xml = self._parser_tools.loadKut(kut).getroot()
        except Exception:
            self.logger.exception("KUT2FPDF: Problema al procesar %s.kut", name)
            return None
        try:
            self._xml_data = load2xml(data).getroot()
        except Exception:
            self.logger.exception("KUT2FPDF: Problema al procesar xml_data")
            return None

        project.message_manager().send("progress_dialog_manager", "create", ["Pineboo", len(self._xml_data), "kugar"])
        project.message_manager().send("progress_dialog_manager", "setLabelText", ["Creando informe ...", "kugar"])

        self.name_ = name
        self.setPageFormat(self._xml)
        # self._page_orientation =
        # self._page_size =
        if report is None:
            from fpdf import FPDF  # type: ignore

            self._actual_append_page_no = 0
            self._document = FPDF(self._page_orientation, "pt", self._page_size)
            for f in self._document.core_fonts:
                self.logger.debug("KUT2FPDF :: Adding font %s", f)
                self._avalible_fonts.append(f)
        else:
            self._document = report
        # Seteamos rutas a carpetas con tipos de letra ...

        # Cargamos las fuentes disponibles
        next_page_break = (flags[2] == 1) if len(flags) == 3 else True
        page_append = (flags[1] == 1) if len(flags) > 1 else False
        page_display = (flags[0] == 1) if len(flags) > 0 else False

        if page_append:
            self.prev_level = -1
            self.last_detail = False

        page_break = False
        if self.new_page:
            page_break = True
            self.new_page = False

        if self.reset_page_count:
            self.reset_page_no()
            self.reset_page_count = False

        if self.design_mode:
            print("Append", page_append)
            print("Display", page_display)
            print("Page break", next_page_break)

        if next_page_break:
            self.reset_page_count = True

        if page_display:
            self.new_page = True

        self.processDetails(not page_break)

        # FIXME:Alguno valores no se encuentran
        for p in self._document.pages.keys():
            page_content = self._document.pages[p]["content"]
            for h in self.draws_at_header.keys():
                page_content = page_content.replace(h, str(self.draws_at_header[h]))

            self._document.pages[p]["content"] = page_content

        # print(self.draws_at_header.keys())
        self._document.set_title(self.name_)
        self._document.set_author("Pineboo - kut2fpdf plugin")

        return self._document

    def get_file_name(self) -> Optional[str]:
        """Retrieve file name where PDF should be saved."""
        import os

        pdf_name = project.tmpdir
        pdf_name += "/%s_%s.pdf" % (self.name_, datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        if os.path.exists(pdf_name):
            os.remove(pdf_name)
        if self._document is not None:
            self._document.output(pdf_name, "F")
            return pdf_name
        else:
            return None

    def topSection(self) -> int:
        """
        Retrieve top section margin for current page to calculate object positions.

        @return Number with ceiling for current page.
        """
        return self._page_top[int(self._document.page_no())]

    def setTopSection(self, value: int) -> None:
        """
        Update top section for current page.

        Usually updated when processing a section.
        @param value. Number specifying new ceiling.
        """
        self._actual_section_size = value - self.topSection()
        self._page_top[int(self._document.page_no())] = value

    def newPage(self, data_level: int, add_on_header: bool = True) -> None:
        """
        Add a new page to the document.
        """
        self._document.add_page(self._page_orientation)
        self._page_top[int(self._document.page_no())] = self._top_margin
        self._document.set_margins(self._left_margin, self._top_margin, self._right_margin)  # Lo dejo pero no se nota nada
        self._no_print_footer = False
        if self.design_mode:
            self.draw_margins()

        self._actual_section_size = 0
        self._actual_append_page_no += 1
        if self.design_mode:
            print("Nueva página", self.number_pages())

        # l_ini = data_level
        # l_end = self.prev_level

        # if l_ini == l_end:
        #    l_end = l_end + 1

        # if l_ini <= l_end:
        #    for l in range(l_ini , l_end):
        #        print(l)
        #        self.processSection("AddOnHeader", str(l))
        pg_headers = self._xml.findall("PageHeader")

        for ph in pg_headers:
            if self.number_pages() == 1 or ph.get("PrintFrequency") == "1":
                ph_level = ph.get("Level") if ph.get("Level") is not None else None
                self.processSection("PageHeader", int(ph_level or "0"))
                break

        if add_on_header and not self.number_pages() == 1:
            for l in range(data_level + 1):
                self.processSection("AddOnHeader", int(l))

        # Por ahora se omite detail header

    def processDetails(self, keep_page: Optional[bool] = None) -> None:
        """
        Process detail secions with their matching detailHeader and detailFooter.
        """
        # Procesamos la cabecera si procede ..

        top_level = 0
        level = 0
        first_page_created = keep_page if keep_page is not None and self._document.page_no() > 0 else False

        rows_array = self._xml_data.findall("Row")
        i = 0

        for data in rows_array:
            self._actual_data_line = data
            level_str: Optional[str] = data.get("level")
            if level_str is None:
                level_str = "0"
            level = int(level_str)
            if level > top_level:
                top_level = level

            if not first_page_created:
                self.newPage(level)
                first_page_created = True

            if rows_array[len(rows_array) - 1] is data:
                self.last_detail = True

            if level < self.prev_level:
                for l in range(level + 1, self.prev_level + 1):
                    self.processData("DetailFooter", self.last_data_processed, l)

            if not str(level) in self.detailn.keys():
                self.detailn[str(level)] = 0
            else:
                self.detailn[str(level)] += 1

            if level > self.prev_level:
                self.processData("DetailHeader", data, level)

            self.processData("Detail", data, level)

            self.last_data_processed = data

            self.prev_level = level

            project.message_manager().send("progress_dialog_manager", "setProgress", [i, "kugar"])
            i += 1

        if not self._no_print_footer:
            for l in reversed(range(top_level + 1)):
                self.processData("DetailFooter", self.last_data_processed, l)

        project.message_manager().send("progress_dialog_manager", "destroy", ["kugar"])

    def processData(self, section_name: str, data: Element, data_level: int) -> None:
        """
        Check if detailHeader + detail + detailFooter do fit in the remaining page and create a new page if not.

        @param section_name. Section name to check
        @param data. Data to check
        @param data_level. Section level
        """
        self.actual_data_level = data_level
        listDF = self._xml.findall(section_name)
        # data_size = len(listDF)

        for dF in listDF:
            draw_if = dF.get("DrawIf")
            show = True
            if draw_if:
                show = bool(data.get(draw_if))

            if dF.get("Level") == str(data_level) and show not in ("", "False", "None"):

                if section_name in ("DetailHeader", "Detail"):
                    heightCalculated = self._parser_tools.getHeight(dF) + self.topSection() + self.increase_section_size

                    if section_name == "DetailHeader":
                        for detail in self._xml.findall("Detail"):
                            if detail.get("Level") == str(data_level):
                                heightCalculated += self._parser_tools.getHeight(detail)

                    for dFooter in self._xml.findall("DetailFooter"):
                        if dFooter.get("Level") == str(data_level):
                            heightCalculated += self._parser_tools.getHeight(dFooter)

                    aof_size = 0
                    for addFooter in self._xml.findall("AddOnFooter"):
                        # if addFooter.get("Level") == str(data_level):
                        aof_size += self._parser_tools.getHeight(addFooter)
                        heightCalculated += self._parser_tools.getHeight(addFooter)

                    pageFooter: Any = self._xml.get("PageFooter")
                    if pageFooter is not None and isinstance(pageFooter, Element):
                        if self._document.page_no() == 1 or pageFooter.get("PrintFrecuency") == "1":
                            heightCalculated += self._parser_tools.getHeight(pageFooter)

                    heightCalculated += self._bottom_margin
                    if (heightCalculated + aof_size) > self._document.h:  # Si nos pasamos
                        self._no_print_footer = True
                        # Vemos el tope por abajo
                        limit_bottom = self._document.h - aof_size
                        actual_size = self._parser_tools.getHeight(dF) + self.topSection()

                        if (actual_size >= limit_bottom - 2) or self.last_detail:  # +2 se usa de margen extra
                            self.processSection("AddOnFooter", int(data_level))

                            self.newPage(data_level)

                self.processXML(dF, data)

                if dF.get("NewPage") == "true" and not self.last_detail:
                    self.newPage(data_level, False)

                break  # Se ejecuta una sola instancia

    def processSection(self, name: str, level: int = 0) -> None:
        """
        Process non-detail sections.

        @param name. Section name to process
        """
        sec_list = self._xml.findall(name)
        sec_ = None
        for s in sec_list:
            if s.get("Level") == str(level) or s.get("Level") is None:
                sec_ = s

        if sec_ is not None:
            if sec_.get("PrintFrequency") == "1" or self._document.page_no() == 1 or name in ("AddOnHeader", "AddOnFooter"):
                self.processXML(sec_)

    def processXML(self, xml: Element, data: Optional[Element] = None) -> None:
        """
        Process single XML element.

        @param xml: Element to process
        @param. data: Line affected
        """

        fix_height = True
        if data is None:
            data = self._actual_data_line

        if self.design_mode and data is not None:
            print("Procesando", xml.tag, data.get("level"))

        size_updated = False
        if xml.tag == "DetailFooter":
            if xml.get("PlaceAtBottom") == "true":
                height = self._parser_tools.getHeight(xml)
                self.setTopSection(self._document.h - height - self.increase_section_size)
                size_updated = True

        if xml.tag == "PageFooter":
            fix_height = False

        if not size_updated:
            self.fix_extra_size()  # Sirve para actualizar la altura con lineas que se han partido porque son muy largas

        for label in xml.iter("Label"):
            self.processText(label, data, fix_height)

        for field in xml.iter("Field"):
            self.processText(field, data, fix_height)

        for special in xml.iter("Special"):
            self.processText(special, data, fix_height, xml.tag)

        for calculated in xml.iter("CalculatedField"):
            self.processText(calculated, data, fix_height, xml.tag)

        # Busco draw_at_header en DetailFooter y los meto también
        if xml.tag == "DetailHeader":
            detail_level = xml.get("Level")
            if detail_level is None:
                raise Exception("Level tag not found")
            for df in self._xml.iter("DetailFooter"):
                if df.get("Level") == detail_level:
                    for cf in df.iter("CalculatedField"):
                        if cf.get("DrawAtHeader") == "true":
                            header_name = "%s_header_%s_%s" % (self.detailn[detail_level], detail_level, cf.get("Field"))
                            self.draws_at_header[header_name] = ""
                            self.processText(cf, data, fix_height, xml.tag)

        for line in xml.iter("Line"):
            self.processLine(line, fix_height)

        if not size_updated:
            self.setTopSection(self.topSection() + self._parser_tools.getHeight(xml))

    def fix_extra_size(self) -> None:
        """Increase size of the section if needed."""
        if self.increase_section_size > 0:
            self.setTopSection(self.topSection() + self.increase_section_size)
            self.increase_section_size = 0

    def processLine(self, xml: Element, fix_height: bool = True) -> None:
        """
        Process single line.

        @param xml. Sección de xml a procesar.
        @param fix_height. Ajusta la altura a los .kut originales, excepto el pageFooter.
        """

        color = xml.get("Color")
        r = 0 if not color else int(color.split(",")[0])
        g = 0 if not color else int(color.split(",")[1])
        b = 0 if not color else int(color.split(",")[2])

        style = int(xml.get("Style") or "0")
        width = int(xml.get("Width") or "0")
        X1 = self.calculateLeftStart(xml.get("X1") or "0")
        X1 = self.calculateWidth(X1, 0, False)
        X2 = self.calculateLeftStart(xml.get("X2") or "0")
        X2 = self.calculateWidth(X2, 0, False)

        # Ajustar altura a secciones ya creadas
        Y1 = int(xml.get("Y1") or "0") + self.topSection()
        Y2 = int(xml.get("Y2") or "0") + self.topSection()
        if fix_height:
            Y1 = self._parser_tools.ratio_correction_h(Y1)
            Y2 = self._parser_tools.ratio_correction_h(Y2)

        self._document.set_line_width(self._parser_tools.ratio_correction_h(width))
        self._document.set_draw_color(r, g, b)
        dash_length = 1
        space_length = 1
        if style == 2:
            dash_length = 20
            space_length = 20
        elif style == 3:
            dash_length = 10
            space_length = 10

        self._document.dashed_line(X1, Y1, X2, Y2, dash_length, space_length)
        # else:
        #    self._document.line(X1, Y1, X2, Y2)

    def calculateLeftStart(self, x: Union[str, int, float]) -> int:
        """
        Check if left margin is exceeded for current page.

        @param x. Position to check.
        @return Revised position.
        """
        return self._parser_tools.ratio_correction_w(int(x)) + self._left_margin

    def calculateWidth(self, width: int, pos_x: int, fix_ratio: bool = True) -> int:
        """
        Check if right margin is exceeded for current page.

        @param x. Position to check.
        @return Revised position.
        """
        limit = self._document.w - self._right_margin
        ret_: int

        if fix_ratio:
            width = self._parser_tools.ratio_correction_w(width)
            pos_x = self._parser_tools.ratio_correction_w(pos_x)
            ret_ = width
            if pos_x + width > limit:
                ret_ = limit - pos_x
        else:
            ret_ = width

        return ret_

    def processText(
        self, xml: Element, data_row: Optional[Element] = None, fix_height: bool = True, section_name: Optional[str] = None
    ) -> None:
        """
        Check tag (calculated, label, special or image).

        @param xml. XML section to process.
        @param fix_height. Revise height from original .kut file except pageFooter.
        """
        is_image = False
        is_barcode = False
        text: str = xml.get("Text") or ""
        # borderColor = xml.get("BorderColor")
        field_name = xml.get("Field") or ""

        # x,y,W,H se calcula y corrigen aquí para luego estar correctos en los diferentes destinos posibles
        W = int(xml.get("Width") or "0")

        H = self._parser_tools.getHeight(xml)

        x = int(xml.get("X") or "0")

        y = int(xml.get("Y") or "0") + self.topSection()  # Añade la altura que hay ocupada por otras secciones
        if fix_height:
            y = self._parser_tools.ratio_correction_h(y)  # Corrige la posición con respecto al kut original

        data_type = xml.get("DataType")

        if xml.tag == "Field" and data_row is not None:
            text = data_row.get(field_name) or ""

        elif xml.tag == "Special":
            if text == "":
                if xml.get("Type") == "1":
                    text = "PageNo"
            text = self._parser_tools.getSpecial(text, self._actual_append_page_no)

        calculation_type = xml.get("CalculationType")

        if calculation_type is not None and xml.tag != "Field":
            if calculation_type == "6":
                function_name = xml.get("FunctionName") or ""
                try:
                    nodo = self._parser_tools.convertToNode(data_row)

                    ret_ = project.call(function_name, [nodo, field_name], None, False)
                    if ret_ is False:
                        return
                    else:
                        text = str(ret_)

                except Exception:
                    self.logger.exception("KUT2FPDF:: Error llamando a function %s", function_name)
                    return
            elif calculation_type == "1":
                text = self._parser_tools.calculate_sum(field_name, self.last_data_processed, self._xml_data, self.actual_data_level)

            elif calculation_type in ("5"):
                if data_row is None:
                    data_row = self._xml_data[0]

                text = data_row.get(field_name) or ""

        if data_type is not None:
            text = self._parser_tools.calculated(text, int(data_type), xml.get("Precision"), data_row)

        if data_type == "5":
            is_image = True

        elif data_type == "6":
            is_barcode = True

        if xml.get("BlankZero") == "1" and text is not None:
            res_ = re.findall(r"\d+", text)
            if res_ == ["0"]:
                return

        if text is not None:
            if text.startswith(filedir("../tempdata")):
                is_image = True

        # negValueColor = xml.get("NegValueColor")
        # Currency = xml.get("Currency")
        #
        # commaSeparator = xml.get("CommaSeparator")
        # dateFormat = xml.get("DateFormat")

        if is_image:
            self.draw_image(x, y, W, H, xml, text)
        elif is_barcode:
            self.draw_barcode(x, y, W, H, xml, text)
        elif data_row is not None:
            level = data_row.get("level") or "0"
            if level and str(level) in self.detailn.keys():
                val = "%s_header_%s_%s" % (self.detailn[str(level)], level, field_name)

            if xml.get("DrawAtHeader") == "true" and level:
                if section_name == "DetailHeader":
                    val = ""
                    self.drawText(x, y, W, H, xml, val)

                    # print(level, section_name, val, text)

            if section_name == "DetailFooter" and xml.get("DrawAtHeader") == "true":
                self.draws_at_header[val] = text
                # print("Añadiendo a", val, text, level)

            else:
                self.drawText(x, y, W, H, xml, text)

    def drawText(self, x: int, y: int, W: int, H: int, xml: Element, txt: str) -> None:
        """
        Draw a text field onto the page.

        @param x. Label X Pos.
        @param y. Label Y Pos.
        @param W. Label Width.
        @param H. Label Height.
        @param xml. Related XML Section
        @param txt. Computed text of the label to be created.
        """

        if txt in ("None", None):
            # return
            txt = ""

        if W == 0 and H == 0:
            return

        txt = self._parser_tools.restore_text(txt)

        resizeable = False

        if xml.get("ChangeHeight") == "1":
            resizeable = True

        # height_resized = False
        orig_x = x
        orig_y = y
        orig_W = W
        orig_H = H
        # Corregimos margenes:
        x = self.calculateLeftStart(x)
        W = self.calculateWidth(W, x)

        # bg_color = xml.get("BackgroundColor").split(",")
        fg_color = self.get_color(xml.get("ForegroundColor") or "")
        self._document.set_text_color(fg_color[0], fg_color[1], fg_color[2])

        # self._document.set_draw_color(255, 255, 255)

        # if xml.get("BorderStyle") == "1":
        # FIXME: Hay que ajustar los margenes

        # font_name, font_size, font_style
        font_style = ""
        font_size = int(xml.get("FontSize") or "0")
        font_name_orig = (xml.get("FontFamily") or "").lower() if xml.get("FontFamily") is not None else "helvetica"
        font_name = font_name_orig

        font_w = int(xml.get("FontWeight") or "50")

        if font_w == 50:  # Normal
            font_w = 100
        elif font_w >= 65:
            font_style += "B"
            font_w = 100

        fontI = xml.get("FontItalic")
        fontU = xml.get("FontUnderlined")  # FIXME: hay que ver si es así

        # background_color = self.get_color(xml.get("BackgroundColor"))
        # if background_color != [255,255,255]: #Los textos que llevan fondo no blanco van en negrita
        #    font_style += "B"

        if fontI == "1":
            font_style += "I"

        if fontU == "1":
            font_style += "U"

        font_name = font_name.replace(" narrow", "")

        font_full_name = "%s%s" % (font_name, font_style)

        if font_full_name not in self._avalible_fonts:
            font_found: Union[str, bool] = False
            if font_full_name not in self._unavalible_fonts:
                font_found = self._parser_tools.find_font(font_full_name, font_style)
            if font_found:
                if self.design_mode:
                    self.logger.warning("KUT2FPDF::Añadiendo el tipo de letra %s %s (%s)", font_name, font_style, font_found)
                self._document.add_font(font_name, font_style, font_found, True)
                self._avalible_fonts.append(font_full_name)

            else:
                if font_full_name not in self._unavalible_fonts:
                    if self.design_mode:
                        self.logger.warning(
                            "KUT2FPDF:: No se encuentra el tipo de letra %s. Sustituido por helvetica%s." % (font_full_name, font_style)
                        )
                    self._unavalible_fonts.append(font_full_name)
                font_name = "helvetica"

        if font_name is not font_name_orig and font_name_orig.lower().find("narrow") > -1:
            font_w = 85

        self._document.set_font(font_name, font_style, font_size)
        self._document.set_stretching(font_w)
        # Corregir alineación
        VAlignment = xml.get("VAlignment")  # 0 izquierda, 1 centrado,2 derecha
        HAlignment = xml.get("HAlignment")

        # layout_direction = xml.get("layoutDirection")

        start_section_size = self._actual_section_size
        result_section_size = 0
        # Miramos si el texto sobrepasa el ancho

        array_text: List[str] = []
        array_n = []
        text_lines = []
        if txt.find("\n") > -1:
            for t in txt.split("\n"):
                array_n.append(t)
        if array_n:  # Hay saltos de lineas ...
            for n in array_n:
                text_lines.append(n)
        else:  # No hay saltos de lineas
            text_lines.append(txt)

        for tl in text_lines:
            if len(tl) > 1:
                if tl[0] == " " and tl[1] != " ":
                    tl = tl[1:]
            str_width = self._document.get_string_width(tl)
            if (
                str_width > W - 10 and xml.tag != "Label" and resizeable
            ):  # Una linea es mas larga que el ancho del campo(Le quito 10 al ancho maximo para que corte parecido a kugar original)
                # height_resized = True
                array_text = self.split_text(tl, W - 10)
            else:

                array_text.append(tl)

        # calculated_h = orig_H * len(array_text)
        self.drawRect(orig_x, orig_y, orig_W, orig_H, xml)

        processed_lines = 0
        extra_size = 0
        for actual_text in array_text:

            processed_lines += 1

            if processed_lines > 1:
                extra_size += font_size + 2

            if HAlignment == "1":  # sobre X
                # Centrado
                x = x + (W / 2) - (self._document.get_string_width(actual_text) / 2)
                # x = x + (W / 2) - (str_width if not height_resized else W / 2)
            elif HAlignment == "2":

                # Derecha
                x = x + W - self._document.get_string_width(actual_text) - 2  # -2 de margen
                # x = x + W - str_width if not height_resized else W
            else:
                # Izquierda
                if processed_lines == 1:
                    x = x + 2

            if VAlignment == "1":  # sobre Y
                # Centrado
                # y = (y + ((H / 2) / processed_lines)) + (((self._document.font_size_pt / 2) / 2) * processed_lines)
                y = int((orig_y + (orig_H / 2)) + ((self._document.font_size_pt / 2) / 2))

                if len(array_text) > 1:
                    y = y - (font_size // 2)

            elif VAlignment == "2":
                # Abajo
                y = orig_y + orig_H - font_size
            else:
                # Arriba
                y = orig_y + font_size

            y = y + extra_size

            if self.design_mode:
                self.write_debug(
                    self.calculateLeftStart(orig_x), y, "Hal:%s, Val:%s, T:%s st:%s" % (HAlignment, VAlignment, txt, font_w), 6, "green"
                )
                if xml.tag == "CalculatedField":
                    self.write_debug(
                        self.calculateLeftStart(orig_x),
                        y,
                        "CalculatedField:%s, Field:%s" % (xml.get("FunctionName"), xml.get("Field")),
                        3,
                        "blue",
                    )

            self._document.text(x, y, actual_text)
            result_section_size += start_section_size

        result_section_size = result_section_size - start_section_size

        if self.increase_section_size < extra_size:  # Si algun incremento extra hay superior se respeta
            self.increase_section_size = extra_size

    def split_text(self, texto: str, limit_w: int) -> List[str]:
        """Split text into lines based on visual width."""
        list_ = []
        linea_: Optional[str] = None

        for t in texto.split(" "):
            if linea_ is None and t == "":
                continue

            if linea_ is not None:
                if self._document.get_string_width(linea_ + t) > limit_w:
                    list_.append(linea_)
                    linea_ = ""
            else:
                linea_ = ""

            linea_ += "%s " % t
        if linea_ is not None:
            list_.append(linea_)
        return list_

    def get_color(self, value: str) -> List[int]:
        """Convert color text into [r,g,b] array."""
        lvalue = value.split(",")
        r: int
        g: int
        b: int
        if len(lvalue) == 3:
            r = int(lvalue[0])
            g = int(lvalue[1])
            b = int(lvalue[2])
        else:
            r = int(value[0:2])
            g = int(value[3:5])
            b = int(value[6:8])

        return [r, g, b]

    def drawRect(self, x: int, y: int, W: int, H: int, xml: Element = None) -> None:
        """
        Draw a rectangle in current page.

        @param x. left side
        @param y. top side
        @param W. width
        @param H. heigth
        """
        style_ = ""
        border_color = None
        bg_color = None
        line_width = self._document.line_width
        border_width = 0.2
        # Calculamos borde  y restamos del ancho
        orig_x = x
        orig_y = y
        orig_w = W

        x = self.calculateLeftStart(orig_x)
        W = self.calculateWidth(W, x)

        if xml is not None and not self.design_mode:
            if xml.get("BorderStyle") == "1":

                border_color = self.get_color(xml.get("BorderColor") or "")
                self._document.set_draw_color(border_color[0], border_color[1], border_color[2])
                style_ += "D"

            bg_color = self.get_color(xml.get("BackgroundColor") or "")
            self._document.set_fill_color(bg_color[0], bg_color[1], bg_color[2])
            style_ = "F" + style_

            border_width = int(xml.get("BorderWidth") or "0" if xml.get("BorderWidth") else 0.2)
        else:
            self.write_cords_debug(x, y, W, H, orig_x, orig_w)
            style_ = "D"
            self._document.set_draw_color(0, 0, 0)

        if style_ != "":
            self._document.set_line_width(border_width)

            self._document.rect(x, y, W, H, style_)
            self._document.set_line_width(line_width)

            self._document.set_xy(orig_x, orig_y)
        # self._document.set_draw_color(255, 255, 255)
        # self._document.set_fill_color(0, 0, 0)

    def write_cords_debug(
        self,
        x: Union[float, int],
        y: Union[float, int],
        w: Union[float, int],
        h: Union[float, int],
        ox: Union[float, int],
        ow: Union[float, int],
    ) -> None:
        """Debug for Kut coordinated."""
        self.write_debug(
            int(x),
            int(y),
            "X:%s Y:%s W:%s H:%s orig_x:%s, orig_W:%s" % (round(x, 2), round(y, 2), round(w, 2), round(h, 2), round(ox, 2), round(ow, 2)),
            2,
            "red",
        )

    def write_debug(self, x: int, y: int, text: str, h: int, color: Optional[str] = None) -> None:
        """Write debug data into the report."""
        orig_color = self._document.text_color
        r = None
        g = None
        b = None
        current_font_family = self._document.font_family
        current_font_size = self._document.font_size_pt
        current_font_style = self._document.font_style
        if color == "red":
            r = 255
            g = 0
            b = 0
        elif color == "green":
            r = 0
            g = 255
            b = 0
        elif color == "blue":
            r = 0
            g = 0
            b = 255

        self._document.set_text_color(r, g, b)
        self._document.set_font_size(4)
        self._document.text(x, y + h, text)
        self._document.text_color = orig_color
        # self._document.set_xy(orig_x, orig_y)
        self._document.set_font(current_font_family, current_font_style, current_font_size)

    def draw_image(self, x: int, y: int, W: int, H: int, xml: Element, file_name: str) -> None:
        """
        Draw image onto current page.

        @param x. left position
        @param y. top position
        @param W. width
        @param H. heigth
        @param xml. Related XML section
        @param file_name. filename of temp data to use
        """
        import os

        if not file_name.lower().endswith(".png"):
            file_name = self._parser_tools.parseKey(file_name)

        if os.path.exists(file_name):
            x = self.calculateLeftStart(x)
            W = self.calculateWidth(W, x)

            self._document.image(file_name, x, y, W, H, "PNG")

    def draw_barcode(self, x: int, y: int, W: int, H: int, xml: Element, text: str) -> None:
        """
        Draw barcode onto currrent page.
        """
        if text == "None":
            return
        from pineboolib import pncontrolsfactory

        file_name = project.tmpdir
        file_name += "/%s.png" % (text)
        type = xml.get("CodBarType")

        if not os.path.exists(file_name):

            bar_code = pncontrolsfactory.FLCodBar(text)  # Code128
            if type is not None:
                type = bar_code.nameToType(type.lower())
                bar_code.setType(type)

            bar_code.setText(text)

            pix = bar_code.pixmap()
            if not pix.isNull():
                pix.save(file_name, "PNG")

        self.draw_image(x + 10, y, W - 20, H, xml, file_name)

    def setPageFormat(self, xml: Element) -> None:
        """
        Define page parameters.

        @param xml: XML with KUT data
        """
        custom_size = None

        self._bottom_margin = int(xml.get("BottomMargin") or "0")
        self._left_margin = int(xml.get("LeftMargin") or "0")
        self._right_margin = int(xml.get("RightMargin") or "0")
        self._top_margin = int(xml.get("TopMargin") or "0")

        page_size = int(xml.get("PageSize") or "0")
        page_orientation = xml.get("PageOrientation") or "0"

        if page_size in [30, 31]:
            custom_size = [int(xml.get("CustomHeightMM") or "0"), int(xml.get("CustomWidthMM") or "0")]

        self._page_orientation = "P" if page_orientation == "0" else "L"
        self._page_size = self._parser_tools.converPageSize(page_size, int(page_orientation), custom_size)  # devuelve un array

    def draw_margins(self) -> None:
        """Draw margins on the report."""
        self.draw_debug_line(0 + self._left_margin, 0, 0 + self._left_margin, self._page_size[1])  # Vertical derecha
        self.draw_debug_line(
            self._page_size[0] - self._right_margin, 0, self._page_size[0] - self._right_margin, self._page_size[1]
        )  # Vertical izquierda
        self.draw_debug_line(0, 0 + self._top_margin, self._page_size[0], 0 + self._top_margin)  # Horizontal superior
        self.draw_debug_line(
            0, self._page_size[1] - self._bottom_margin, self._page_size[0], self._page_size[1] - self._bottom_margin
        )  # Horizontal inferior

    def draw_debug_line(self, X1: int, Y1: int, X2: int, Y2: int, title: Optional[str] = None, color: str = "GREY") -> None:
        """Draw a debug line on the report."""
        dash_length = 2
        space_length = 2

        r = 0
        g = 0
        b = 0
        if color == "GREY":
            r = 220
            g = 220
            b = 220
        self._document.set_line_width(1)
        self._document.set_draw_color(r, g, b)
        self._document.dashed_line(X1, Y1, X2, Y2, dash_length, space_length)

    def number_pages(self) -> int:
        """Get number of pages on the report."""
        return self._actual_append_page_no if self._actual_append_page_no > 0 else 0

    def reset_page_no(self) -> None:
        """Reset page number."""
        self._actual_append_page_no = -1
