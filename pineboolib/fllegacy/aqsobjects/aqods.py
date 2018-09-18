# -*- coding: utf-8 -*-
from pineboolib import decorators


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

    def __init__(self, sheet):
        self.sheet_ = sheet
        from odf import table, style
        self.row_ = table.TableRow()
        self.cells_list_ = []
        self.new_cell_ = True
        self.temp_cell_ = None
        self.style_row_ = style.Style(name="stylerow%s" % self.sheet_.rowsCount(), family="table-cell")

    def addBgColor(self, color):
        self.checkNewCell()
        import odf
        if isinstance(color, odf.element.Element):
            self.style_row_.addElement(color)

    def opIn(self, opt):
        self.checkNewCell()
        if isinstance(opt, str):
            from odf.text import P
            self.temp_cell_.addElement(P(text="%s" % opt))
            self.cells_list_.append(self.temp_cell_)
            self.temp_cell_ = None

        # FIXME: Añadir bordes, cursiva

    def checkNewCell(self):
        if self.temp_cell_ is None:
            from odf.table import TableCell
            self.temp_cell_ = TableCell(valuetype='string', stylename=self.style_row_)

    def close(self):
        for cell in self.cells_list_:
            self.row_.addElement(cell)

        self.sheet_.num_rows_ += 1
        self.sheet_.spread_sheet_parent_.automaticstyles.addElement(self.style_row_)
        self.sheet_.sheet_.addElement(self.row_)

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
        self.Align_center = None
        self.Text_bold = None
        self.Text_italic = None

        self.Border_right = None
        self.Border_bottom = None
        self.Border_lext = None


AQOdsStyle = AQOdsStyle_class()
AQOdsGenerator = AQOdsGenerator_class()
