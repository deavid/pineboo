# -*- coding: utf-8 -*-
from pineboolib.utils import checkDependencies, filedir, load2xml
import pineboolib
from pineboolib.fllegacy.flsettings import FLSettings
from xml import etree
import logging
import datetime
import re
from concurrent.futures import process

"""
Conversor de kuts a pyFPDF
"""


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
    _avalible_fonts = None
    _unavalible_fonts = None
    design_mode = None
    _actual_data_line = None
    _no_print_footer = False
    _actual_section_size = None
    increase_section_size = None
    last_detail = False
    actual_data_level = None
    last_data_processed = None
    drawif_values = None

    def __init__(self):

        self.logger = logging.getLogger("kut2rml")
        checkDependencies({"fpdf": "pyfpdf"})
        from pineboolib.plugins.kugar.parsertools import parsertools
        self._parser_tools = parsertools()
        self._avalible_fonts = []
        self._unavalible_fonts = []
        self.design_mode = FLSettings().readBoolEntry("ebcomportamiento/kugar_debug_mode")
        self._actual_data_line = None
        self._no_print_footer = False
        self.increase_section_size = 0
        self.actual_data_level = 0
        self.drawif_values = {}

    """
    Convierte una cadena de texto que contiene el ".kut" en un pdf y retorna la ruta a este último.
    @param name. Nombre de ".kut".
    @param kut. Cadena de texto que contiene el ".kut".
    @param data. Cadena de texto que contiene los datos para ser rellenados en el informe.
    @return Ruta a fichero pdf.
    """

    def parse(self, name, kut, data):

        try:
            self._xml = self._parser_tools.loadKut(kut)
        except Exception:
            self.logger.exception(
                "KUT2FPDF: Problema al procesar %s.kut", name)
            return False

        try:
            self._xml_data = load2xml(data)
        except Exception:
            self.logger.exception("KUT2FPDF: Problema al procesar xml_data")
            return False

        self.setPageFormat(self._xml)
        # self._page_orientation =
        # self._page_size =

        from fpdf import FPDF
        self._document = FPDF(self._page_orientation, "pt", self._page_size)
        
        # Seteamos rutas a carpetas con tipos de letra ...

        # Cargamos las fuentes disponibles
        for f in self._document.core_fonts:
            self.logger.debug("KUT2FPDF :: Adding font %s", f)
            self._avalible_fonts.append(f)

        self.newPage(0)
        self.processDetails()

        pdfname = FLSettings().readEntry("ebcomportamiento/kugar_temp_dir",pineboolib.project.getTempDir())
        pdfname += "/%s_%s.pdf" % (name, datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

        # Datos del creador del documento
        self._document.set_title(name)
        self._document.set_author("Pineboo - kut2fpdf plugin")

        self._document.output(pdfname, 'F')

        return pdfname

    """
    Indica el techo para calcular la posición de los objetos de esa sección.
    @return Número con el techo de la página actual.
    """

    def topSection(self):
        return self._page_top[str(self._document.page_no())]

    """
    Actualiza el valor del techo de la página actual. Se suele actualizar al procesar una sección.
    @param value. Numero que elspecifica el nuevo techo.
    """

    def setTopSection(self, value):
        self._actual_section_size = value - self.topSection()
        self._page_top[str(self._document.page_no())] = value

    """
    Añade una nueva página al documento.
    """

    def newPage(self, data_level = None):
        self._document.add_page(self._page_orientation)
        self._page_top[str(self._document.page_no())] = self._top_margin
        self._document.set_margins(self._left_margin, self._top_margin, self._right_margin)  # Lo dejo pero no se nota nada
        self.last_detail = False
        self._no_print_footer = False
        if self.design_mode:
            self.draw_margins()
        # Corta con el borde inferior ...
        # self._document.set_auto_page_break(
        #    True, self._document.h - self._bottom_margin)
        self._actual_section_size = 0
        self.processSection("PageHeader")
        
        if data_level is not None:
            for l in range(data_level):
                self.processSection("AddOnHeader", str(l))

        
    """
    Procesa las secciones details con sus correspondientes detailHeader y detailFooter.
    """

    def processDetails(self):
        # Procesamos la cabecera si procede ..
        prev_level = 0
        level = 0
        
        rows_array = self._xml_data.findall("Row")
        actual_top_level = 0
        for data in self._xml_data.findall("Row"):
            self._actual_data_line = data
            level = int(data.get("level"))
            if prev_level > level:
                if not self._no_print_footer:
                    self.processData("DetailFooter", data, prev_level)
            elif actual_top_level <= level:
                self.processData("DetailHeader",  data, level)
                actual_top_level = level
            
            if rows_array[len(rows_array) - 1] is data:
                self.last_detail = True
            

            self.processData("Detail", data, level)

            prev_level = level
            self.last_data_processed = data
            
            

        if level:
            if not self._no_print_footer:
                for l in reversed(range(level + 1)):
                    self.processData("DetailFooter", data, l)

        if self._xml.find("PageFooter"):
            self.processSection("PageFooter")
        #elif self._xml.find("AddOnFooter"):
        #    self.processSection("AddOnFooter")

    """
    Paso intermedio que calcula si detailHeader + detail + detailFooter entran en el resto de la ṕagina. Si no es así crea nueva página.
    @param section_name. Nombre de la sección a procesar.
    @param data. Linea de datos a procesar.
    @param data_level. Nivel de seccion.
    """

    def processData(self, section_name, data, data_level):
        self.actual_data_level = data_level
        listDF = self._xml.findall(section_name)
        data_size = len(listDF)      
        
        for dF in listDF:
            draw_if = dF.get("DrawIf")
            show = True
            if draw_if:
                show = data.get(draw_if)
                
            if dF.get("Level") == str(data_level) and show not in ("None", "False"):
                #Si el valor previo de draw_if de esta section y este level es el mismo no se pinta
                if show is not True:
                    if section_name not in self.drawif_values.keys():
                        self.drawif_values[section_name] = {}
                    
                    if str(data_level) not in self.drawif_values[section_name].keys():
                        self.drawif_values[section_name][str(data_level)] = None
                        
                
                
                    if self.drawif_values[section_name][str(data_level)] == show:
                        return
                    else:
                        self.drawif_values[section_name][str(data_level)] = show
                
                if section_name == "DetailHeader":
                    heightCalculated = self._parser_tools.getHeight(dF) + self.topSection()
                    for detail in self._xml.findall("Detail"):
                        if detail.get("Level") == str(data_level):
                            heightCalculated += self._parser_tools.getHeight(detail)
                            
                    for dFooter in self._xml.findall("DetailFooter"):
                        if dFooter.get("Level") == str(data_level):
                            heightCalculated += self._parser_tools.getHeight(dFooter)
                    
                    #for addFooter in self._xml.findall("AddOnFooter"):
                    #    if addFooter.get("Level") == str(data_level):
                    #        heightCalculated += self._parser_tools.getHeight(addFooter)
                    
                    pageFooter = self._xml.get("PageFooter")
                    if pageFooter:
                        if self._document.page_no() == 1 or pageFooter.get("PrintFrecuency") == "1":
                            heightCalculated += self._parser_tools.getHeight(pageFooter)

                    heightCalculated += self._bottom_margin

                    if heightCalculated > self._document.h:  # Si nos pasamos
                        self._no_print_footer = True
                        #Vemos el tope por abajo 
                        limit_bottom = self._document.h - self._parser_tools.getHeight(self._xml.get("AddOnFooter"))
                        actual_size = self._parser_tools.getHeight(dF) + self.topSection()
                        if (actual_size > limit_bottom) or self.last_detail:
                            self.processSection("AddOnFooter", str(data_level))
                            #self.processSection("PageFooter")  # Pie de página
                            self.newPage(data_level)

                    
                self.processXML(dF, data)

    """
    Procesa las secciones fuera de detail
    @param name. Nombre de la sección a procesar.
    """

    def processSection(self, name, level = None):
        sec_ = self._xml.find(name)
            
        if sec_:
            if level is not None and sec_.get("Level") != level:
                return
            
            if sec_.get("PrintFrequency") == "1" or self._document.page_no() == 1 or name is "AddOnFooter" or (self._document.page_no() > 1 and name is "AddOnHeader"):
                if name is "PageFooter":
                    self.setTopSection(self._document.h - int(sec_.get("Height")))
                    
                data = None
                if name in ("AddOnFooter", "AddOnHeader"):
                    data = self._actual_data_line
                    
                self.processXML(sec_, data)

    """
    Procesa un elemento de xml.
    @param xml: El elemento a procesar.
    @param. data: Linea de datos afectada.
    """

    def processXML(self, xml, data=None):
        fix_height = True
        if xml.tag == "DetailFooter":
            if xml.get("PlaceAtBottom") == "true":
                self.setTopSection(self._document.h - self._parser_tools.getHeight(xml))
        
               
        if xml.tag == "PageFooter":
            fix_height = False

        self.fix_extra_size()
        
        #labels, fields, clculatedFields, Lineas
        
            
        for label in xml.iter("Label"):
            self.processText(label, data, fix_height)
        
        for field in xml.iter("Field"):
            self.processText(field, data, fix_height)
        
        for special in xml.iter("Special"):
            self.processText(special, data, fix_height)
        
        for calculated in xml.iter("CalculatedField"):
            self.processText(calculated, data, fix_height)
        
        #for child in xml.iter():
        #    if child.tag in ("Label", "Field", "Special", "CalculatedField"):
        #        self.processText(child, data, fix_height)
        #    elif child.tag == "Line":
        #        self.processLine(child, fix_height)
        for line in xml.iter("Line"):
            self.processLine(line, fix_height)

        if xml.get("PlaceAtBottom") != "true":
            self.setTopSection(self.topSection() + self._parser_tools.getHeight(xml))
        
        
                    

    
    def fix_extra_size(self):
        if self.increase_section_size > 0:
            self.setTopSection(self.topSection() + self.increase_section_size)
            self.increase_section_size = 0    
    """
    Procesa una linea.
    @param xml. Sección de xml a procesar.
    @param fix_height. Ajusta la altura a los .kut originales, excepto el pageFooter.
    """

    def processLine(self, xml, fix_height=True):

        color = xml.get("Color")
        r = 0 if not color else int(color.split(",")[0])
        g = 0 if not color else int(color.split(",")[1])
        b = 0 if not color else int(color.split(",")[2])

        style = int(xml.get("Style"))
        width = int(xml.get("Width"))
        X1 = self.calculateLeftStart(xml.get("X1"))
        X1 = self.calculateRightEnd(X1)
        X2 = self.calculateLeftStart(xml.get("X2"))
        X2 = self.calculateRightEnd(X2)
        # Ajustar altura a secciones ya creadas
        Y1 = int(xml.get("Y1")) + self.topSection()
        Y2 = int(xml.get("Y2")) + self.topSection()
        if fix_height:
            Y1 = self._parser_tools.heightCorrection(Y1)
            Y2 = self._parser_tools.heightCorrection(Y2)
        
          
            
        
        self._document.set_line_width(width)
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
        #else:
        #    self._document.line(X1, Y1, X2, Y2)

    """
    Comprueba si excedemos el margen izquierdo de la página actual
    @param x. Posición a comprobar.
    @return Valor corregido, si procede.
    """

    def calculateLeftStart(self, x):
        x = int(x)
        ret_ = x
        if x < self._left_margin:
            ret_ = self._left_margin

        return ret_

    """
    Comprueba si excedemos el margen derecho de la página actual
    @param x. Posición a comprobar.
    @return Valor corregido, si procede.
    """

    def calculateRightEnd(self, x):
        x = int(x)
        ret_ = x
        if x > (self._document.w - self._right_margin):
            ret_ = self._document.w - self._right_margin

        return ret_

    """
    Procesa una etiqueta. Esta peude ser un campo calculado, una etiqueta, un campo especial o una imagen.
    @param xml. Sección de xml a procesar.
    @param fix_height. Ajusta la altura a los .kut originales, excepto el pageFooter.
    """

    def processText(self, xml, data_row=None, fix_height=True):
        is_image = False
        is_barcode = False
        text = xml.get("Text")
        borderColor = xml.get("BorderColor")
        field_name = xml.get("Field")
        
        # x,y,W,H se calcula y corrigen aquí para luego estar correctos en los diferentes destinos posibles
        W = int(xml.get("Width"))
        H = self._parser_tools.getHeight(xml)

        x = int(xml.get("X"))
        y = int(xml.get("Y")) + self.topSection()  # Añade la altura que hay ocupada por otras secciones
        if fix_height:
            y = self._parser_tools.heightCorrection(y)  # Corrige la posición con respecto al kut original

        data_type = xml.get("DataType")
        
        if xml.tag == "Field" and data_row is not None:
            text = data_row.get(field_name)

        elif xml.tag == "Special":
            if text == "":
                if xml.get("Type") == "1":
                    text = "PageNo"
            text = self._parser_tools.getSpecial( text, self._document.page_no())

        elif xml.tag == "CalculatedField":
            calculation_type = xml.get("CalculationType")
            
            if calculation_type == "6":
                function_name = xml.get("FunctionName")
                try:
                    nodo = self._parser_tools.convertToNode(data_row)
                    from pineboolib.pncontrolsfactory import aqApp
                    ret_ = aqApp.call(function_name, [nodo, field_name])
                    if ret_ is False:
                        return
                    else:
                        text = str(ret_)                       
                        
                except Exception:
                    self.logger.exception(
                        "KUT2FPDF:: Error llamando a function %s", function_name)
                    return
            elif calculation_type == "1":
                text = self._parser_tools.calculate_sum(field_name, self.last_data_processed, self._xml_data, self.actual_data_level)
            
            elif calculation_type in ("5"):
                if data_row is None:
                    data_row = self._xml_data[0]
                
                text = data_row.get(field_name)
            
        if data_type is not None:
            text = self._parser_tools.calculated(text, int(data_type), int(xml.get("Precision")), data_row)
            
        if data_type == "5":
            is_image = True
        
        elif data_type == "6":
            is_barcode = True
            
        
        if xml.get("BlankZero") == "1" and text is not None:
            res_ = re.findall(r'\d+', text)
            res_ = "".join(res_)
            if int(res_) == 0:
                return
            
            

        if text is not None and text.startswith(filedir("../tempdata")):
            is_image = True

        negValueColor = xml.get("NegValueColor")
        Currency = xml.get("Currency")

        commaSeparator = xml.get("CommaSeparator")
        dateFormat = xml.get("DateFormat")

        if is_image:
            self.draw_image(x, y, W, H, xml, text)
        elif is_barcode:
            self.draw_barcode(x, y, W, H, xml, text)
        else:
            self.drawText(x, y, W, H, xml, text)


    """
    Dibuja un campo texto en la página.
    @param x. Pos x de la etiqueta.
    @param y. Pos y de la etiqueta.
    @param W. Anchura de la etiqueta.
    @param H. Altura de la etiqueta.
    @param xml. Sección del xml afectada.
    @param txt. Texto calculado de la etiqueta a crear.
    """

    def drawText(self, x, y, W, H, xml, txt):

        if txt in ("None", None):
            return
        
        height_resized = False
        orig_x = x
        orig_y = y
        orig_W = W
        orig_H = H
        # Corregimos margenes:
        x = self.calculateLeftStart(x)
        dif_orig_x = x - orig_x
        W = self.calculateRightEnd((x + orig_W) - dif_orig_x) - x
        
        dif_orig_w = W - orig_W
        
        #bg_color = xml.get("BackgroundColor").split(",")
        fg_color = self.get_color(xml.get("ForegroundColor"))
        self._document.set_text_color(fg_color[0], fg_color[1], fg_color[2])
        
        
        
        #self._document.set_draw_color(255, 255, 255)

        #if xml.get("BorderStyle") == "1":
            # FIXME: Hay que ajustar los margenes
        
        #font_name, font_size, font_style
        font_style = ""
        font_size = int(xml.get("FontSize"))
        font_name = xml.get("FontFamily").lower()

        font_w = xml.get("FontWeight")
        
        if font_w is None:
            font_w = 100
        else:
            font_w = int(font_w) #Ajuste de streching en pyfpdf
            factor = (100 -font_w) / 13
            font_w = 100 - (5 * factor)
        
        
        fontI = xml.get("FontItalic")
        fontU = xml.get("FontUnderlined")  # FIXME: hay que ver si es así

        background_color = self.get_color(xml.get("BackgroundColor"))
        if background_color != [255,255,255]: #Los textos que llevan fondo no blanco van en negrita
            font_style += "B"

        if fontI == "1":
            font_style += "I"

        if fontU == "1":
            font_style += "U"

        font_full_name = "%s%s" % (font_name, font_style)

        if font_full_name not in self._avalible_fonts:
            font_found = self._parser_tools.find_font(font_full_name)            
            if font_found:
                self.logger.warn("KUT2FPDF::Añadiendo el tipo de letra %s (%s)", font_full_name, font_found)
                self._document.add_font(font_full_name, "", font_found, True)
                self._avalible_fonts.append(font_full_name)

            else:
                if font_full_name not in self._unavalible_fonts:
                    self.logger.warning("KUT2FPDF:: No se encuentra el tipo de letra %s. Sustituido por helvetica%s." %(font_full_name, font_style))
                    self._unavalible_fonts.append(font_full_name)
                font_name = "helvetica"
                    
        
        self._document.set_font(font_name, font_style, font_size)
        self._document.set_stretching(font_w)
        # Corregir alineación
        VAlignment = xml.get("VAlignment")  # 0 izquierda, 1 centrado,2 derecha
        HAlignment = xml.get("HAlignment")
        
        start_section_size = self._actual_section_size
        result_section_size = 0
        #Miramos si el texto sobrepasa el ancho
        str_width = self._document.get_string_width(txt)
        array_text = []
        if str_width > W and xml.tag !="Label":
            height_resized = True
            array_text = self.split_text(txt, W)
        else:
            
            array_text.append(txt)
        
        calculated_h = orig_H * len(array_text)
        self.drawRect(orig_x, orig_y, orig_W, calculated_h, xml)
        
        processed_lines = 0
        extra_size = 0
        for actual_text in array_text:
            
            if dif_orig_x > 0:
                x += 2

            
            processed_lines += 1
            
            if processed_lines > 1:
                extra_size += orig_H - (orig_H - font_size) / 2
            
            if HAlignment == "1":  # sobre X
                # Centrado
                x = x + (W / 2) - (self._document.get_string_width(actual_text) / 2)
                #x = x + (W / 2) - (str_width if not height_resized else W / 2)
            elif HAlignment == "2":
                # Derecha
                x = x + W - self._document.get_string_width(actual_text) - 2 # -2 de margen
                #x = x + W - str_width if not height_resized else W
            else:
                # Izquierda
                x = orig_x + dif_orig_x + 2

                
            if VAlignment == "1":  # sobre Y
                # Centrado
                #y = (y + ((H / 2) / processed_lines)) + (((self._document.font_size_pt / 2) / 2) * processed_lines) 
                y = ( orig_y  + ( orig_H / 2))+ ((self._document.font_size_pt / 2) /2)
            elif VAlignment == "2":
                # Abajo
                y = orig_y + orig_H - font_size
            else:
                # Arriba
                y = orig_y
        
            y = y + extra_size
            
            if self.design_mode:
                self.write_debug(self.calculateLeftStart(orig_x), y, "Hal:%s, Val:%s, T:%s st:%s" % (HAlignment, VAlignment, txt, font_w), 6, "green")
                if xml.tag == "CalculatedField":
                    self.write_debug(self.calculateLeftStart(orig_x), y, "CalculatedField:%s, Field:%s" % (xml.get("FunctionName"), xml.get("Field")), 3, "blue")
            
            
            
            
            self._document.text(x, y, actual_text)
            result_section_size += start_section_size
        
        result_section_size = result_section_size - start_section_size
        
        if self.increase_section_size < extra_size: #Si algun incremento extra hay superior se respeta
            self.increase_section_size = extra_size

    
    def split_text(self, texto, limit_w):
        list_ = []
        linea_ = None   
        
        for t in texto.split(" "):
            if linea_  is None and t == "":
                continue
            
            if linea_ is not None:
                if self._document.get_string_width(linea_ + t) > limit_w:
                    list_.append(linea_)
                    linea_ = ""
            else:
                linea_ = ""
            
            linea_ += "%s " % t
        
        list_.append(linea_)
        
        return list_
                
            
                   
        
    """
    Dibuja un cuadrado en la página actual.
    @param x. Pos x del cuadrado.
    @param y. Pos y del cuadrado.
    @param W. Anchura del cuadrado.
    @param H. Altura del cuadrado.
    """
    def get_color(self, value):
        value = value.split(",")
        r = None
        g = None
        b = None
        if len(value) == 3:
            r = int(value[0])
            g = int(value[1])
            b = int(value[2])
        else:
            r = int(value[0:2])
            g = int(value[3:5])
            b = int(value[6:8])
        
        return [r,g,b]

    def drawRect(self, x, y, W, H, xml = None):
        style_ = ""
        border_color = None
        bg_color = None
        line_width = self._document.line_width
        border_width = 0.2
        #Calculamos borde  y restamos del ancho
        orig_x = x
        orig_y = y
        orig_w = W
        x = self.calculateLeftStart(orig_x)
        dif_orig_x = x - orig_x
        
        
        
        W = self.calculateRightEnd((x + orig_w) - dif_orig_x) - x
        
        dif_orig_w = orig_w -W
        #W = W - dif_orig_x
        
        if xml is not None and not self.design_mode:
            if xml.get("BorderStyle") == "1":
                
                border_color = self.get_color(xml.get("BorderColor"))
                self._document.set_draw_color(border_color[0], border_color[1], border_color[2])
                style_ += "D"
                    
            
            bg_color = self.get_color(xml.get("BackgroundColor"))
            self._document.set_fill_color(bg_color[0], bg_color[1], bg_color[2])
            style_ =  "F" + style_
            
            border_width = int(xml.get("BorderWidth") if xml.get("BorderWidth") else 0.2)
        else:
            self.write_cords_debug(x,y,W,H, orig_x, orig_w)
            style_ = "D"
            self._document.set_draw_color(0, 0, 0)
            
        if style_ is not "":
            self._document.set_line_width(border_width)
            if dif_orig_x is not 0: # Corrige el relleno cuando 
                x += 2
            
            if dif_orig_w is not 0:
                W -= 2

            self._document.rect(x, y, W, H, style_)
            self._document.set_line_width(line_width)
            
            self._document.set_xy(orig_x, orig_y)
        #self._document.set_draw_color(255, 255, 255)
        #self._document.set_fill_color(0, 0, 0)
    
    def write_cords_debug(self, x, y, w, h, ox, ow):
        self.write_debug(x,y,"X:%s Y:%s W:%s H:%s orig_x:%s, orig_W:%s" % (round(x, 2),round(y, 2),round(w, 2),round(h, 2), round(ox, 2), round(ow, 2)), 2, "red")
        
    
    def write_debug(self, x,y,text, h, color = None):
        orig_color = self._document.text_color
        r = None
        g = None
        b = None
        current_font_family = self._document.font_family
        current_font_size = self._document.font_size_pt
        current_font_style = self._document.font_style
        if color is "red":
            r = 255
            g = 0
            b = 0
        elif color is "green":
            r = 0
            g = 255
            b = 0
        elif color is "blue":
            r = 0
            g = 0
            b = 255
        
        self._document.set_text_color(r,g,b)
        self._document.set_font_size(4)
        self._document.text(x, y + h, text) 
        self._document.text_color = orig_color
        #self._document.set_xy(orig_x, orig_y)
        self._document.set_font(current_font_family, current_font_style, current_font_size)
        
    """
    Inserta una imagen en la página actual.
    @param x. Pos x de la imagen.
    @param y. Pos y de la imagen.
    @param W. Anchura de la imagen.
    @param H. Altura de la imagen.
    @param xml. Sección del xml afectada.
    @param file_name. Nombr del fichero de tempdata a usar
    """

    def draw_image(self, x, y, W, H, xml, file_name):
        import os
        if not file_name.lower().endswith(".png"):
            file_name = self._parser_tools.parseKey(file_name)
            
        if os.path.exists(file_name):            
            limit_right = self.calculateRightEnd(x + W)
            orig_x = x
            x = self.calculateLeftStart(orig_x)
            x = x + (x -orig_x)
            W = W - ((x + W) - limit_right )
            
            
            self._document.image(file_name, x, y, W, H, "PNG")
    
    def draw_barcode(self, x, y, W, H, xml, text):
        from pineboolib.fllegacy.flcodbar import FLCodBar
        bar_code = FLCodBar(text) #Code128
        pix = bar_code.pixmap()
        if not pix.isNull():
            file_name = FLSettings().readEntry("ebcomportamiento/kugar_temp_dir",pineboolib.project.getTempDir())
            file_name += "/%s_%s.png" % (text, datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            pix.save(file_name, "PNG")
            self.draw_image(x , y, W, H, xml, file_name)
            
            
            
 
        
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
            custom_size = [int(xml.get("CustomHeightMM")), int(xml.get("CustomWidthMM"))]

        self._page_orientation = "P" if page_orientation == "0" else "L"
        self._page_size = self._parser_tools.converPageSize(
            page_size, int(page_orientation), custom_size)  # devuelve un array
        
        
    
    def draw_margins(self):
        self.draw_debug_line(0 + self._left_margin , 0, 0+ self._left_margin  , self._page_size[1]) #Vertical derecha
        self.draw_debug_line(self._page_size[0] - self._right_margin , 0, self._page_size[0] - self._right_margin  , self._page_size[1])#Vertical izquierda
        self.draw_debug_line(0, 0 + self._top_margin, self._page_size[0], 0 + self._top_margin) #Horizontal superior
        self.draw_debug_line(0, self._page_size[1] - self._bottom_margin, self._page_size[0], self._page_size[1] - self._bottom_margin) #Horizontal inferior
    def draw_debug_line(self, X1, Y1, X2, Y2, title= None, color="GREY"):
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
