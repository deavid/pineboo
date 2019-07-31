# -*- coding: utf-8 -*-
"""
AQOds package.

Generate .ods files (Opendocument Spreadsheet)
"""
from typing import Union, List, Any, Tuple, Optional

from odf.opendocument import OpenDocumentSpreadsheet  # type: ignore

import odf  # type: ignore
from odf import table, style  # type: ignore

from pineboolib import logging


logger = logging.getLogger("AQOds")

"""
Generador de ficheros ODS
"""


class AQOdsGenerator_class(object):
    """AQOdsGenerator_class Class."""

    doc_: Any = None
    """
    Constructor
    """

    def __init__(self):
        """
        Initialize the class by checking dependencies.
        """

        from pineboolib.application.utils.check_dependencies import check_dependencies

        check_dependencies({"odf": "odfpy"})

    def generateOds(self, file_name: str) -> None:
        """
        Generate the ODS file.

        @param file_name. File name to generate.
        """
        if self.doc_ is None:
            raise Exception("Document not set, cannot generate")
        file_name = file_name.replace(".ods", "")
        self.doc_.save(file_name, True)

    def set_doc_(self, document) -> None:
        """
        Assign the contents of the file.

        @param document. Data to add to the file
        """

        self.doc_ = document


class AQOdsSpreadSheet(object):
    """
    AQOdsSpreadSheet Class.

    Generate ODS document.
    """

    spread_sheet: "OpenDocumentSpreadsheet"
    generator_: "AQOdsGenerator_class"

    def __init__(self, generator: AQOdsGenerator_class) -> None:
        """
        Initialize the file generator.

        @param generator. File generator.
        """

        self.generator_ = generator
        self.spread_sheet = OpenDocumentSpreadsheet()
        self.generator_.set_doc_(self.spread_sheet)

    def close(self) -> None:
        """
        Close the document.
        """

        pass


class AQOdsImage(object):
    """AQOdsImage Class."""

    name_: str
    width_: float
    height_: float
    x_: int
    y_: int
    link_: str

    def __init__(self, name: str, width: float, height: float, x: int, y: int, link: str) -> None:
        """
        Initialize the Image.

        @param name. Image Name
        @param width. Width.
        @param height. Tall.
        @param x. X position.
        @param me. Position and.
        @param link. Image link.
        """

        self.name_ = name
        self.width_ = width
        self.height_ = height
        self.x_ = x
        self.y_ = y
        self.link_ = link


class AQOdsSheet(object):
    """
    AQOdsSheet Class.

    Sheet inside the document.
    """

    num_rows_: int
    spread_sheet_parent_: "OpenDocumentSpreadsheet"
    sheet_: table.Table

    def __init__(self, spread_sheet: AQOdsSpreadSheet, sheet_name: str) -> None:
        """
        Initialize the sheet.

        @param spread_sheet. Spreadsheet.
        @param sheet_name. Name of the sheet.
        """

        self.spread_sheet_parent_ = spread_sheet.spread_sheet
        self.num_rows_ = 0

        self.sheet_ = table.Table(name=sheet_name)

    def rowsCount(self) -> int:
        """
        Return number of lines.

        @return Number of lines.
        """

        return self.num_rows_

    def close(self) -> None:
        """Close the sheet."""

        self.spread_sheet_parent_.spreadsheet.addElement(self.sheet_)


class AQOdsRow(object):
    """AQOdsRow."""

    sheet_: AQOdsSheet
    row_: table.TableRow
    cells_list_: List[table.TableCell]
    style_cell_text_: Optional[str]
    fix_precision_: Optional[int]
    row_color_: Optional[str]
    property_cell_: List[Any]

    def __init__(self, sheet: AQOdsSheet) -> None:
        """
        Initialize a line inside a sheet.

        @param sheet. Parent Document Sheet.
        """

        self.sheet_ = sheet

        self.row_ = table.TableRow()
        self.cells_list_ = []
        self.fix_precision_ = None
        self.row_color_ = None
        self.property_cell_ = []

    def addBgColor(self, color) -> None:
        """
        Specify the background color of the line.

        @param color. It is specified in hex (color) format [2:]
        """

        self.row_color_ = color

    def opIn(self, opt: Union[float, str, "odf.element.Element", List, "AQOdsImage"]):
        """
        Add options to the line.

        @param opt. Line options, each cell ends with the value assignment
        """

        from odf.text import P, Span  # type: ignore
        from odf.draw import Frame, Image  # type: ignore

        if isinstance(opt, float):
            if self.fix_precision_ is not None:
                opt = "%s" % round(opt, self.fix_precision_)
            else:
                opt = "%s" % opt
        if isinstance(opt, str):  # Último paso
            cell, style = self.__newCell__()

            if self.style_cell_text_:
                text_elem = P(text="")
                txt_ = Span(stylename=self.style_cell_text_, text=opt)
                text_elem.addElement(txt_)
            else:
                text_elem = P(text=opt)

            self.sheet_.spread_sheet_parent_.automaticstyles.addElement(style)
            cell.addElement(text_elem)
            self.cells_list_.append(cell)
            self.fix_precision_ = None
            self.style_cell_text_ = None

        else:
            if isinstance(opt, list):  # Si es lista , Insertamos todos los parámetros uno a uno
                for l in opt:
                    self.opIn(l)

            elif isinstance(opt, AQOdsImage):

                href = self.sheet_.spread_sheet_parent_.addPictureFromFile(opt.link_)
                cell, style = self.__newCell__()

                # p = P()
                frame = Frame(width="%spt" % opt.width_, height="%spt" % opt.height_, x="%spt" % opt.x_, y="%spt" % opt.y_)
                frame.addElement(Image(href=href))
                # p.addElement(frame)
                cell.addElement(frame)
                self.cells_list_.append(cell)
                # self.coveredCell()
                # self.opIn(href)
                # print("FIXME:: Vacio", href)
            elif isinstance(opt, odf.element.Element):
                if opt.tagName in ("style:paragraph-properties", "style:table-cell-properties"):
                    import copy

                    prop = copy.copy(opt)
                    self.property_cell_.append(prop)
                elif opt.tagName == "style:style":
                    self.sheet_.spread_sheet_parent_.automaticstyles.addElement(opt)
                    self.style_cell_text_ = opt
                else:
                    logger.warning("%s:Parámetro desconocido %s", __name__, opt.tagName)

    def __newCell__(self) -> Tuple[table.TableCell, style.Style]:
        """
        Return new cell This is created by assigning the value to the previous one.

        @return Tuple(TableCell, Style)
        """

        style_cell = style.Style(name="stylecell_%s_%s" % (len(self.cells_list_), self.sheet_.rowsCount()), family="table-cell")
        if self.row_color_:  # Guardo color si hay
            style_cell.addElement(style.TableCellProperties(backgroundcolor="#%s" % self.row_color_))

        for prop in self.property_cell_:  # Guardo prop cell si hay
            style_cell.addElement(prop)

        self.property_cell_ = []
        return table.TableCell(valuetype="string", stylename=style_cell), style_cell

    def close(self) -> None:
        """
        Close the line.
        """

        for cell in self.cells_list_:  # Meto las celdas en la linea
            self.row_.addElement(cell)

        self.sheet_.num_rows_ += 1  # Especifico cunatas lineas tiene ya la hoja
        self.sheet_.sheet_.addElement(self.row_)  # Meto la nueva linea en la hoja

    def coveredCell(self) -> None:
        """
        Field is filled with empty data.
        """

        self.opIn(" ")

    def setFixedPrecision(self, n: Optional[int]) -> None:
        """
        Specify the precision of number decimals.

        @param n. Decimal precision.
        """
        if n is not None:
            self.fix_precision_ = n


def AQOdsColor(color: int) -> str:
    """
    Returnsa color from a hexadecimal value.

    @param color. Hexadecimal value.
    """
    return hex(color)[2:]


class AQOdsStyle_class(object):
    """AQOdsStyle_class."""

    def alignCenter(self) -> style.ParagraphProperties:
        """
        Align a cell to the center property.

        @return Style Property.
        """

        return style.ParagraphProperties(textalign="center")

    def alignRight(self) -> style.ParagraphProperties:
        """
        Align a cell to the right property.

        @return Style Property.
        """

        return style.ParagraphProperties(textalign="right")

    def alignLeft(self) -> style.ParagraphProperties:
        """
        Align a cell to the left property.

        @return Style Property.
        """

        return style.ParagraphProperties(textalign="left")

    def textBold(self) -> style.Style:
        """
        Return text bold property.

        @return Style Property.
        """

        bold_style = style.Style(name="Bold", family="text")
        bold_style.addElement(style.TextProperties(fontweight="bold"))
        return bold_style

    def textItalic(self) -> style.Style:
        """
        Return italic text.

        @return Style Property.
        """

        italic_style = style.Style(name="Italic", family="text")
        italic_style.addElement(style.TextProperties(fontstyle="italic"))
        return italic_style

    def borderBottom(self) -> style.TableCellProperties:
        """
        Return the property of the lower edge of a cell.

        @return Table cell property.
        """

        return style.TableCellProperties(borderbottom="1pt solid #000000")

    def borderLeft(self) -> style.TableCellProperties:
        """
        Return the property of the left edge of a cell.

        @return Table cell property.
        """

        from odf import style  # type: ignore

        return style.TableCellProperties(borderleft="1pt solid #000000")

    def borderRight(self) -> style.TableCellProperties:
        """
        Return the property of the right edge of a cell.

        @return Table cell property.
        """

        from odf import style  # type: ignore

        return style.TableCellProperties(borderright="1pt solid #000000")

    def borderTop(self) -> style.TableCellProperties:
        """
        Return the property of the upper edge of a cell.

        @return Table cell property.
        """

        from odf import style  # type: ignore

        return style.TableCellProperties(bordertop="1pt solid #000000")

    Align_center = property(alignCenter, None)
    Align_right = property(alignRight, None)
    Align_left = property(alignLeft, None)
    Text_bold = property(textBold, None)
    Text_italic = property(textItalic, None)
    Border_bottom = property(borderBottom, None)
    Border_top = property(borderTop, None)
    Border_right = property(borderRight, None)
    Border_left = property(borderLeft, None)


AQOdsStyle = AQOdsStyle_class()
AQOdsGenerator = AQOdsGenerator_class()
