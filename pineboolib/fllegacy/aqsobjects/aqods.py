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
    temp_cell_ = None
    style_row_ = None
    styles_list_ = None
    style_cell_text_ = None
    style_cell_ = None
    fix_precision_ = None

    def __init__(self, sheet):
        self.sheet_ = sheet
        from odf import table, style
        self.row_ = table.TableRow()
        self.cells_list_ = []
        self.temp_cell_ = None
        self.style_cell_ = None
        self.fix_precision_ = None
        self.styles_list_ = []

        self.style_row_ = style.Style(name="stylecell_%s_%s" % (
            len(self.cells_list_), self.sheet_.rowsCount()), family="table-cell")

    def addBgColor(self, color):
        import odf
        if isinstance(color, odf.element.Element):
            self.style_row_.addElement(color)

    def opIn(self, opt):
        self.__checkNewCell__()
        if isinstance(opt, float):
            if self.fix_precision_ is not None:
                opt = "%s" % round(opt, self.fix_precision_)
            else:
                opt = "%s" % opt

        if isinstance(opt, str):
            from odf.text import P, Span
            if self.style_cell_text_:
                elem = P(text="")
                txt_ = Span(stylename=self.style_cell_text_, text=opt)
                elem.addElement(txt_)
            else:
                elem = P(text=opt)

            self.sheet_.spread_sheet_parent_.automaticstyles.addElement(self.style_cell_)
            self.temp_cell_.addElement(elem)
            self.cells_list_.append(self.temp_cell_)
            self.temp_cell_ = None  # El siguiente opIn
            self.fix_precision_ = None

        else:
            import odf

            if isinstance(opt, odf.element.Element):
                if opt.tagName in ("style:paragraph-properties", "style:table-cell-properties"):
                    # FIXME:Esto se aplica luego a toda la linea
                    self.style_cell_.addElement(opt)
                elif opt.tagName == "style:style":
                    self.sheet_.spread_sheet_parent_.automaticstyles.addElement(opt)
                    self.style_cell_text_ = opt
                else:
                    logger.warn("%s:Parámetro desconocido %s", __name__, opt.tagName)

            elif isinstance(opt, list):  # Si es lista , Insertamos todos los parámetros uno a uno
                for l in opt:
                    self.opIn(l)

        # FIXME: Añadir bordes, cursiva

    def __checkNewCell__(self):
        if self.temp_cell_ is None:
            self.style_cell_text_ = None
            self.style_cell_ = None
            from odf import table
            self.style_cell_ = self.style_row_
            self.temp_cell_ = table.TableCell(valuetype='string', stylename=self.style_cell_)

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
    from odf.style import TableCellProperties
    return TableCellProperties(backgroundcolor="#%s" % hex(color)[2:])


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
    Align_rigth = property(alignRight, None)
    Align_left = property(alignLeft, None)
    Text_bold = property(textBold, None)
    Text_italic = property(textItalic, None)
    Border_bottom = property(borderBottom, None)
    Border_top = property(borderTop, None)
    Border_right = property(borderRight, None)
    Border_left = property(borderLeft, None)


AQOdsStyle = AQOdsStyle_class()
AQOdsGenerator = AQOdsGenerator_class()
