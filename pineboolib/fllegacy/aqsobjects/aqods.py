# -*- coding: utf-8 -*-
from pineboolib import decorators
import logging



logger = logging.getLogger("AQOds")

"""
Generador de ficheros ODS
"""
class AQOdsGenerator_class(object):

    doc_ = None
    """
    Constructor
    """
    def __init__(self):
        from pineboolib.utils import checkDependencies
        checkDependencies({"odf": "odfpy"})

    """
    Genera el fichero ODS
    @param file_name. Nombre del fichero a generar
    """
    def generateOds(self, file_name):
        file_name = file_name.replace(".ods", "")
        self.doc_.save(file_name, True)

    """
    Asigna el contenido del fichero
    @param document. Datos a añadir al fichero
    """
    def set_doc_(self, document):
        self.doc_ = document


"""
Genera documento ODS
"""
class AQOdsSpreadSheet(object):
    spread_sheet = None

    """
    Constructor
    @param generator. Generador de ficheros
    """
    def __init__(self, generator):
        from odf.opendocument import OpenDocumentSpreadsheet
        self.generator_ = generator
        self.spread_sheet = OpenDocumentSpreadsheet()
        self.generator_.set_doc_(self.spread_sheet)

    """
    Cierra el documento
    """
    def close(self):
        pass


"""
Hoja dentro del documento
"""
class AQOdsSheet(object):
    sheet_ = None
    spread_sheet_parent = None
    num_rows_ = None

    """
    Constructor
    @param spread_sheet. Hoja de calculo.
    @param sheet_name. Nombre de la hoja
    """
    def __init__(self, spread_sheet, sheet_name):
        self.spread_sheet_parent_ = spread_sheet.spread_sheet
        self.num_rows_ = 0
        from odf.table import Table
        self.sheet_ = Table(name=sheet_name)

    """
    Numero de lineas
    """
    def rowsCount(self):
        return self.num_rows_

    """
    Cierra la hoja
    """
    def close(self):
        self.spread_sheet_parent_.spreadsheet.addElement(self.sheet_)


"""
Linea dentro de una hoja
"""
class AQOdsRow(object):
    sheet_ = None
    row_ = None
    cells_list_ = None
    style_cell_text_ = None
    fix_precision_ = None
    row_color_ = None
    property_cell_ = None

    """
    Constructor
    @param sheet. Hoja del documento
    """
    def __init__(self, sheet):
        self.sheet_ = sheet
        from odf import table
        self.row_ = table.TableRow()
        self.cells_list_ = []
        self.fix_precision_ = None
        self.row_color_ = None
        self.property_cell_ = []

    """
    Especifica el color de fondo de la linea
    @param color. Se especifica en formato hex(color)[2:]
    """
    def addBgColor(self, color):
        self.row_color_ = color

    """
    Añade opciones a la linea
    @param opt. Opciones de linea, cada celda acaba con la asignación del valor
    """
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
                    logger.warning("%s:Parámetro desconocido %s", __name__, opt.tagName)

            elif isinstance(opt, list):  # Si es lista , Insertamos todos los parámetros uno a uno
                for l in opt:
                    self.opIn(l)
                    
            elif isinstance(opt, AQOdsImage):
                from odf.text import P
                from odf.draw import Frame, Image
                href = self.sheet_.spread_sheet_parent_.addPictureFromFile(opt.link_)
                cell, style = self.__newCell__()
                
                #p = P()
                frame = Frame(width="%spt" % opt.width_, height="%spt" % opt.height_, x="%spt" % opt.x_, y="%spt" % opt.y_)
                frame.addElement(Image(href=href))
                #p.addElement(frame)
                cell.addElement(frame)
                self.cells_list_.append(cell)
                #self.coveredCell()
                #self.opIn(href)
                #print("FIXME:: Vacio", href)
                

    """
    Nueva celda. Esta se crea al asignar el valor a la anterior
    """
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

    """
    Cierra la linea
    """
    def close(self):
        for cell in self.cells_list_:  # Meto las celdas en la linea
            self.row_.addElement(cell)

        self.sheet_.num_rows_ += 1  # Especifico cunatas lineas tiene ya la hoja
        self.sheet_.sheet_.addElement(self.row_)  # Meto la nueva linea en la hoja

    """
    El campo se rellena con datos vacíos
    """
    def coveredCell(self):
        self.opIn(" ")

    """
    Especifica la precisión de los decimales del numero
    """
    def setFixedPrecision(self, n):
        self.fix_precision_ = n


"""
Especifica un color
@param color. Se especifica AQOdsColor(0xe7e7e7)
"""
def AQOdsColor(color):
    return hex(color)[2:]


"""
Estilos de los objetos de un ODS
"""
class AQOdsStyle_class(object):

    """
    Alinea al centro  una celda
    """
    def alignCenter(self):
        from odf import style
        return style.ParagraphProperties(textalign='center')

    """
    Alinea a la derecha una celda
    """
    def alignRight(self):
        from odf import style
        return style.ParagraphProperties(textalign='right')

    """
    Alinea a la izquierda una celda
    """
    def alignLeft(self):
        from odf import style
        return style.ParagraphProperties(textalign='left')

    """
    Texto negrita
    """
    def textBold(self):
        from odf.style import Style, TextProperties
        bold_style = Style(name="Bold", family="text")
        bold_style.addElement(TextProperties(fontweight="bold"))
        return bold_style

    """
    Texto cursiva
    """
    def textItalic(self):
        from odf.style import Style, TextProperties
        italic_style = Style(name="Italic", family="text")
        italic_style.addElement(TextProperties(fontstyle="italic"))
        return italic_style

    """
    Borde inferior de una celda
    """
    def borderBottom(self):
        from odf import style
        return style.TableCellProperties(borderbottom="1pt solid #000000")

    """
    Borde izquierdo de una celda
    """
    def borderLeft(self):
        from odf import style
        return style.TableCellProperties(borderleft="1pt solid #000000")

    """
    Borde derecho de una celda
    """
    def borderRight(self):
        from odf import style
        return style.TableCellProperties(borderright="1pt solid #000000")

    """
    Borde superior de una celda
    """
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

class AQOdsImage(object):
    name_ = None
    width_ = None
    height_ = None
    x_ = None
    y_ = None
    link_ = None
    def __init__(self, name, width, height, x, y, link):
        self.name_ = name
        self.width_ = width
        self.height_ = height
        self.x_ = x
        self.y_ = y
        self.link_ = link
    
        
AQOdsStyle = AQOdsStyle_class()
AQOdsGenerator = AQOdsGenerator_class()
