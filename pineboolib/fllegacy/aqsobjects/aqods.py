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
    new_cell_ = None
    temp_cell_ = None
    style_row_ = None
    style_cell_ = None
    styles_list_ = None
    cell_paragraph_properties_ = None
    style_cell_text_ = None
    row_color_ = None

    def __init__(self, sheet):
        self.sheet_ = sheet
        from odf import table, style
        self.row_ = table.TableRow()
        self.cells_list_ = []
        self.new_cell_ = True
        self.temp_cell_ = None
        self.row_color_ = None
        self.style_next_text_ = None
        self.styles_list_ = []
        self.style_row_ = style.Style(name="stylerow%s" % self.sheet_.rowsCount(), family="table-cell")

    def addBgColor(self, color):
        import odf
        if isinstance(color, odf.element.Element):
            self.row_color_ = color

    def opIn(self, opt):
        self.checkNewCell()
        if isinstance(opt, str):
            from odf.text import P, Span
            elem = P(text="")
            sp = Span(stylename=self.style_cell_text_, text=opt)
            elem.addElement(sp)
            self.temp_cell_.addElement(elem)
            self.cells_list_.append(self.temp_cell_)
            self.styles_list_.append(self.style_cell_)
            self.temp_cell_ = None

        else:
            import odf

            if isinstance(opt, odf.element.Element):
                if opt.tagName == "style:paragraph-properties":
                    self.style_cell_.addElement(opt)

                elif opt.tagName == "style:style":
                    self.styles_list_.append(opt)
                    self.style_cell_text_ = opt

            elif isinstance(opt, list):  # Si es lista , Insertamos todos los parámetros uno a uno
                for l in opt:
                    self.opIn(l)

        # FIXME: Añadir bordes, cursiva

    def checkNewCell(self):
        if self.temp_cell_ is None:
            self.style_cell_ = None
            from odf.table import TableCell
            from odf import style
            self.style_cell_ = style.Style(name="stylecell_%s_%s" % (self.sheet_.rowsCount(), len(self.cells_list_)), family="table-cell")
            if self.row_color_:
                self.style_cell_.addElement(self.row_color_)
            self.temp_cell_ = TableCell(valuetype='string', stylename=self.style_cell_)
            self.style_cell_text_ = None

    def close(self):
        for cell in self.cells_list_:
            self.row_.addElement(cell)

        self.sheet_.num_rows_ += 1
        self.sheet_.sheet_.addElement(self.row_)
        for style in self.styles_list_:
            self.sheet_.spread_sheet_parent_.automaticstyles.addElement(style)

    @decorators.NotImplementedWarn
    def coveredCell(self):
        pass


def AQOdsColor(color):
    from odf.style import TableCellProperties
    return TableCellProperties(backgroundcolor="#%s" % hex(color)[2:])


class AQOdsStyle_class(object):

    Align_center = None
    Text_bold = None
    Text_italic = None
    Border_bottom = None
    Border_right = None
    Border_lext = None

    def __init__(self):
        self.Align_center = self.alignCenter()
        self.Text_bold = self.textBold()
        self.Text_italic = self.textItalic()

        self.Border_right = None
        self.Border_bottom = None
        self.Border_lext = None

    def alignCenter(self):
        from odf import style
        return style.ParagraphProperties(textalign='center')

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


AQOdsStyle = AQOdsStyle_class()
AQOdsGenerator = AQOdsGenerator_class()
