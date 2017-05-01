# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from binascii import unhexlify

from lxml import etree
from PyQt4 import QtGui, QtCore, uic

from pineboolib import flcontrols
from pineboolib.fllegacy import FLTableDB
from pineboolib.fllegacy import FLFieldDB

import zlib

Qt = QtCore.Qt
ICONS = {}

class Options:
    DEBUG_LEVEL = 100


# TODO: Refactorizar este fichero como una clase. ICONS es la lista de iconos
#      para un solo formulario. Debe existir una clase LoadUI y que ICONS sea
#      una variable de ésta. Para cada nuevo formulario se debería instanciar
#      una nueva clase.

def loadUi(path, widget, parent = None):
    global ICONS
    parser = etree.XMLParser(
        ns_clean=True,
        encoding="UTF-8",
        remove_blank_text=True,
        )
    tree = etree.parse(path, parser)
    root = tree.getroot()
    ICONS = {}
    widget.hide()
    if parent is None: parent = widget
    for xmlimage in root.xpath("images/image"):
        loadIcon(xmlimage)

    for xmlwidget in root.xpath("widget"):
        loadWidget(xmlwidget, widget, parent)

    formname = widget.objectName() # Debe estar despues de loadWidget porque queremos el valor del UI de Qt3
    if Options.DEBUG_LEVEL > 0: print("form:", formname)
    for xmlconnection in root.xpath("connections/connection"):
        sender_name = xmlconnection.xpath("sender/text()")[0]
        signal_name = xmlconnection.xpath("signal/text()")[0]
        receiv_name = xmlconnection.xpath("receiver/text()")[0]
        slot_name = xmlconnection.xpath("slot/text()")[0]
        if sender_name == formname:
            sender = widget
        else:
            sender = widget.findChild(QtGui.QWidget, sender_name)
        receiver = None
        if sender is None: 
            if Options.DEBUG_LEVEL > 50: print("Connection sender not found:", sender_name)
        if receiv_name == formname:
            receiver = widget
            fn_name = slot_name.rstrip("()")
            if Options.DEBUG_LEVEL > 50: print("Conectando de UI a QS: (%r.%r -> %r.%r)" % (sender_name, signal_name, receiv_name, fn_name))
            #print dir(widget.iface)
            if hasattr(widget.iface, fn_name):
                try: QtCore.QObject.connect(sender, QtCore.SIGNAL(signal_name), getattr(widget.iface, fn_name))
                except Exception as e:
                    if Options.DEBUG_LEVEL > 50: 
                        print("Error connecting:",
                          sender, QtCore.SIGNAL(signal_name),
                          receiver, QtCore.SLOT(slot_name),
                          getattr(widget.iface, fn_name))
                    if Options.DEBUG_LEVEL > 50: print("Connect Error:", e.__class__.__name__, e)
                continue

        if receiver is None: receiver = widget.findChild(QtGui.QWidget, receiv_name)
        if receiver is None: print("Connection receiver not found:", receiv_name)
        if sender is None or receiver is None: continue
        try: QtCore.QObject.connect(sender, QtCore.SIGNAL(signal_name), receiver, QtCore.SLOT(slot_name))
        except Exception as e:
            if Options.DEBUG_LEVEL > 50: print("Error connecting:", sender, QtCore.SIGNAL(signal_name), receiver, QtCore.SLOT(slot_name))
            if Options.DEBUG_LEVEL > 50: print("Error:", e.__class__.__name__, e)
    widget.show()

def createWidget(classname, parent=None):
    cls = getattr(flcontrols, classname, None) or \
            getattr(QtGui, classname, None) or \
            getattr(FLTableDB, classname, None) or \
            getattr(FLFieldDB, classname, None)
    if cls is None:
        print("WARN: Class name not found in QtGui:", classname)
        widgt = QtGui.QWidget(parent)
        widgt.setStyleSheet("* { background-color: #fa3; } ")
        return widgt
    return cls(parent)

def loadWidget(xml, widget=None, parent=None):
    translate_properties = {
        "caption" : "windowTitle",
        "name" : "objectName",
        "icon" : "windowIcon",
        "iconSet" : "icon",
        "accel" : "shortcut",
        "layoutMargin" : "contentsMargins",
    }
    if widget is None:
        raise ValueError
    if parent is None:
        parent = widget

    def process_property(xmlprop, widget=widget):
        pname = xmlprop.get("name")
        if pname in translate_properties: pname = translate_properties[pname]
        setpname = "set" + pname[0].upper() + pname[1:]
        if pname == "layoutSpacing":
            set_fn = widget.layout.setSpacing
        else:
            set_fn = getattr(widget, setpname, None)
        if set_fn is None:
            if Options.DEBUG_LEVEL > 50: print("qt3ui: Missing property", pname, " for %r" % widget.__class__)
            return
        #print "Found property", pname
        if pname == "contentsMargins" or pname == "layoutSpacing":
            try:
                value = int(xmlprop.get("stdset"))
                value /= 2
            except Exception as e: value = 0
            if pname == "contentsMargins":
                value = QtCore.QMargins(value, value, value, value)
        else:
            value = loadVariant(xmlprop)

        try: set_fn(value)
        except Exception as e:
            if Options.DEBUG_LEVEL > 50: print(e, repr(value))
            if Options.DEBUG_LEVEL > 50: print(etree.tostring(xmlprop))

    def process_layout_box(xmllayout, widget=widget, mode="box"):
        for c in xmllayout:
            try:
                row = int(c.get("row"))
                col = int(c.get("column"))
            except Exception: row = col = None
            if c.tag == "property":
                process_property(c, widget.layout)
            elif c.tag == "widget":
                new_widget = createWidget(c.get("class"), parent=widget)
                loadWidget(c, new_widget, parent)
                new_widget.show()
                if mode == "box":
                    widget.layout.addWidget(new_widget)
                elif mode == "grid":
                    widget.layout.addWidget(new_widget, row, col)
            elif c.tag == "spacer":
                properties = {}
                for p in c.xpath("property"):
                    k, v = loadProperty(p)
                    properties[k] = v
                if mode == "box":
                    widget.layout.addStretch()
                elif mode == "grid":
                    if properties["orientation"] == "Horizontal":
                        widget.layout.columnStretch(col)
                    else:
                        widget.layout.rowStretch(row)
            else:
                if Options.DEBUG_LEVEL > 50: print("qt3ui: Unknown layout xml tag", repr(c.tag))

        widget.setLayout(widget.layout)
        widget.layout.setMargin(1)
        widget.layout.setSpacing(1)
        widget.layout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)


    layouts_pending_process = []
    properties = []
    unbold_fonts = []
    for c in xml:
        if c.tag == "property":
            properties.append(c)
            continue
        if c.tag == "vbox":
            # TODO: layout se solapa con el layout de FormInternalObj
            if isinstance(getattr(widget,"layout", None),QtGui.QLayout):
                if Options.DEBUG_LEVEL > 50: print("qt3ui: Trying to replace layout. Ignoring.", repr(c.tag), widget.layout)
                continue
            widget.layout = QtGui.QVBoxLayout()
            widget.layout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
            widget.layout.setSpacing(3)
            widget.layout.setMargin(3)

            layouts_pending_process += [(c,"box")]
            #process_layout_box(c, mode="box")
            continue
        if c.tag == "hbox":
            if isinstance(getattr(widget,"layout", None),QtGui.QLayout):
                if Options.DEBUG_LEVEL > 50: print("qt3ui: Trying to replace layout. Ignoring.", repr(c.tag), widget.layout)
                continue
            widget.layout = QtGui.QHBoxLayout()
            widget.layout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
            widget.layout.setSpacing(3)
            widget.layout.setMargin(3)
            layouts_pending_process += [(c,"box")]
            #process_layout_box(c, mode="box")
            continue
        if c.tag == "grid":
            if isinstance(getattr(widget,"layout", None),QtGui.QLayout):
                if Options.DEBUG_LEVEL > 50: print("qt3ui: Trying to replace layout. Ignoring.", repr(c.tag), widget.layout)
                continue
            widget.layout = QtGui.QGridLayout()
            widget.layout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
            widget.layout.setSpacing(3)
            widget.layout.setMargin(3)
            layouts_pending_process += [(c,"grid")]
            #process_layout_box(c, mode="grid")
            continue
        if c.tag == "item":
            prop1 = {}
            for p in c.xpath("property"):
                k, v = loadProperty(p)
                prop1[k] = v
            widget.addItem(prop1["text"])
            continue
        if c.tag == "attribute":
            k = c.get("name")
            v = loadVariant(c)
            attrs = getattr(widget, "_attrs", None)
            if attrs is not None:
                attrs[k] = v
                #print("qt3ui: attribute %r => %r" % (k,v), widget.__class__, repr(c.tag))
            else:
                print("qt3ui: [NOT ASSIGNED] attribute %r => %r" % (k,v), widget.__class__, repr(c.tag))
            continue
        if c.tag == "widget":
            # Si dentro del widget hay otro significa que estamos dentro de un contenedor.
            # Según el tipo de contenedor, los widgets se agregan de una forma u otra.
            new_widget = createWidget(c.get("class"), parent=parent)
            new_widget.hide()
            new_widget._attrs = {}
            loadWidget(c, new_widget, parent)
            new_widget.setContentsMargins(0,0,0,0)
            new_widget.show()
            if isinstance(widget, QtGui.QTabWidget):
                title = new_widget._attrs.get("title","UnnamedTab")
                widget.addTab(new_widget,title)
            else:
                if Options.DEBUG_LEVEL > 50: print("qt3ui: Unknown container widget xml tag", widget.__class__, repr(c.tag))
            unbold_fonts.append(new_widget)
            continue

        if Options.DEBUG_LEVEL > 50: print("qt3ui: Unknown widget xml tag", widget.__class__, repr(c.tag))
    for c in properties:
        process_property(c)
    for c,m in layouts_pending_process:
        process_layout_box(c,mode=m)
    for new_widget in unbold_fonts:
        f = new_widget.font()
        f.setBold(False)
        f.setItalic(False)
        new_widget.setFont(f)

def loadIcon(xml):
    global ICONS
    name = xml.get("name")
    xmldata = xml.xpath("data")[0]
    img_format = xmldata.get("format")
    data = unhexlify(xmldata.text.strip())
    pixmap = QtGui.QPixmap()
    if img_format == "XPM.GZ":
        data = zlib.decompress(data,15)
        img_format = "XPM"
    pixmap.loadFromData(data, img_format)
    icon = QtGui.QIcon(pixmap)
    ICONS[name] = icon


def loadVariant(xml):
    for variant in xml:
        return _loadVariant(variant)

def loadProperty(xml):
    for variant in xml:
        return (xml.get("name"), _loadVariant(variant))

def u(x):
    if isinstance(x,str): return x
    return str(x)

def b(x):
    x = x.lower()
    if x[0] == "t": return True
    if x[0] == "f": return False
    if x[0] == "1": return True
    if x[0] == "0": return False
    if x == "on": return True
    if x == "off": return False
    print("Bool?:", repr(x))
    return None


def _loadVariant(variant):
    text = variant.text or ""
    text = text.strip()
    if variant.tag == "cstring": return text
    if variant.tag == "iconset":
        global ICONS
        return ICONS.get(text, text)
    if variant.tag == "string": return u(text)
    if variant.tag == "number":
        if text.find('.') >= 0: return float(text)
        return int(text)
    if variant.tag == "bool": return b(text)
    if variant.tag == "rect":
        k = {}
        for c in variant:
            k[c.tag] = int(c.text.strip())
        return QtCore.QRect(k['x'], k['y'], k['width'], k['height'])

    if variant.tag == "sizepolicy":
        p = QtGui.QSizePolicy()
        for c in variant:
            value = int(c.text.strip())
            if c.tag == "hsizetype": p.setHorizontalPolicy(value)
            if c.tag == "vsizetype": p.setVerticalPolicy(value)
            if c.tag == "horstretch": p.setHorizontalStretch(value)
            if c.tag == "verstretch": p.setVerticalStretch(value)
        return p
    if variant.tag == "size":
        p = QtCore.QSize()
        for c in variant:
            value = int(c.text.strip())
            if c.tag == "width": p.setWidth(value)
            if c.tag == "height": p.setHeight(value)
        return p
    if variant.tag == "font":
        p = QtGui.QFont()
        for c in variant:
            value = c.text.strip()
            bv = b(value)
            try:
                if c.tag == "bold": p.setBold(bv)
                elif c.tag == "italic": p.setItalic(bv)
                elif c.tag == "family": p.setFamily(value)
                else: print("unknown font style type", repr(c.tag))
            except Exception as e:
                if Options.DEBUG_LEVEL > 50: print(e)
        return p

    if variant.tag =="set":
        v = None
        text = variant.text
        libs = [QtCore.Qt]
        if text=="WordBreak|AlignVCenter": text="AlignVCenter"
        for lib in libs:
            v = getattr(lib,text,None)
        if v is not None: return v
    
    if variant.tag == "enum":
        v = None
        libs = [Qt, QtGui.QFrame, QtGui.QSizePolicy]
        for lib in libs:
            v = getattr(lib, text, None)
            if v is not None: return v            
        if text == "GroupBoxPanel": return QtGui.QFrame.StyledPanel

    if Options.DEBUG_LEVEL > 50: print("qt3ui: Unknown variant:", etree.tostring(variant))


