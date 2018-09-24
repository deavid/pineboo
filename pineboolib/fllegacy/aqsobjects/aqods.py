# -*- coding: utf-8 -*-
from pineboolib import decorators
import logging

logger = logging.getLogger("AQOds")


class AQOdsGenerator_class(object):

    doc_ = None

    def __init__(self):
        from pineboolib.utils import checkDependencies
        checkDependencies({"odf": "odfpy"})

    def generateOds(self, file_name):
        file_name = file_name.replace(".ods", "")
        self.doc_.save(file_name, True)

    def set_doc_(self, document):
        self.doc_ = document


class AQOdsSpreadSheet(object):
    spread_sheet = None

    def __init__(self, generator):
        from odf.opendocument import OpenDocumentSpreadsheet
        self.generator_ = generator
        self.spread_sheet = OpenDocumentSpreadsheet()
        self.generator_.set_doc_(self.spread_sheet)

    def close(self):
        pass


class AQOdsSheet(object):
    sheet_ = None
    spread_sheet_parent = None
    num_rows_ = None

    def __init__(self, spread_sheet, sheet_name):
        self.spread_sheet_parent_ = spread_sheet.spread_sheet
        self.num_rows_ = 0
        from odf.table import Table
        self.sheet_ = Table(name=sheet_name)

    def rowsCount(self):
        return self.num_rows_

    def close(self):
        self.spread_sheet_parent_.spreadsheet.addElement(self.sheet_)


class AQOdsRow(object):
    sheet_ = None
    row_ = None
    cells_list_ = None
    style_cell_text_ = None
    fix_precision_ = None
    row_color_ = None
    property_cell_ = None

    def __init__(self, sheet):
        self.sheet_ = sheet
        from odf import table
        self.row_ = table.TableRow()
        self.cells_list_ = []
        self.fix_precision_ = None
        self.row_color_ = None
        self.property_cell_ = []

    def addBgColor(self, color):
        self.row_color_ = color

    def opIn(self, opt):
        if isinstance(opt, float):
            if self.fix_precision_ is not None:
                opt = "%s" % round(opt, self.fix_precision_)
            else:
                opt = "%s" % opt
        if isinstance(opt, str):  # Último paso
            cell, style = self.__newCell__()
            from odf.text import P, Span
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
            import odf

            if isinstance(opt, odf.element.Element):
                if opt.tagName in ("style:paragraph-properties", "style:table-cell-properties"):
                    import copy
                    prop = copy.copy(opt)
                    self.property_cell_.append(prop)
                elif opt.tagName == "style:style":
                    self.sheet_.spread_sheet_parent_.automaticstyles.addElement(opt)
                    self.style_cell_text_ = opt
                else:
                    logger.warn("%s:Parámetro desconocido %s", __name__, opt.tagName)

            elif isinstance(opt, list):  # Si es lista , Insertamos todos los parámetros uno a uno
                for l in opt:
                    self.opIn(l)

    def __newCell__(self):
        from odf import table, style
        style_cell = style.Style(name="stylecell_%s_%s" % (
            len(self.cells_list_), self.sheet_.rowsCount()), family="table-cell")
        if self.row_color_:  # Guardo color si hay
            style_cell.addElement(style.TableCellProperties(backgroundcolor="#%s" % self.row_color_))

        for prop in self.property_cell_:  # Guardo prop cell si hay
            style_cell.addElement(prop)

        self.property_cell_ = []
        return table.TableCell(valuetype='string', stylename=style_cell), style_cell

    def close(self):
        for cell in self.cells_list_:  # Meto las celdas en la linea
            self.row_.addElement(cell)

        self.sheet_.num_rows_ += 1  # Especifico cunatas lineas tiene ya la hoja
        self.sheet_.sheet_.addElement(self.row_)  # Meto la nueva linea en la hoja

    def coveredCell(self):
        self.opIn(" ")

    def setFixedPrecision(self, n):
        self.fix_precision_ = n


def AQOdsColor(color):
    return hex(color)[2:]


class AQOdsStyle_class(object):

    def alignCenter(self):
        from odf import style
        return style.ParagraphProperties(textalign='center')

    def alignRight(self):
        from odf import style
        return style.ParagraphProperties(textalign='right')

    def alignLeft(self):
        from odf import style
        return style.ParagraphProperties(textalign='left')

    def textBold(self):
        from odf.style import Style, TextProperties
        bold_style = Style(name="Bold", family="text")
        bold_style.addElement(TextProperties(fontweight="bold"))
        return bold_style

    def textItalic(self):
        from odf.style import Style, TextProperties
        italic_style = Style(name="Italic", family="text")
        italic_style.addElement(TextProperties(fontstyle="italic"))
        return italic_style

    def borderBottom(self):
        from odf import style
        return style.TableCellProperties(borderbottom="1pt solid #000000")

    def borderLeft(self):
        from odf import style
        return style.TableCellProperties(borderleft="1pt solid #000000")

    def borderRight(self):
        from odf import style
        return style.TableCellProperties(borderright="1pt solid #000000")

    def borderTop(self):
        from odf import style
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
