# encoding: UTF-8
from lxml import etree
from PyQt4 import QtGui, QtCore, uic
import flcontrols
from binascii import unhexlify
Qt = QtCore.Qt
ICONS = {}

def loadUi(path, widget):
    global ICONS
    parser = etree.XMLParser(
                    ns_clean=True,
                    encoding="UTF-8",
                    remove_blank_text=True,
                    )
    tree = etree.parse(path, parser)
    root = tree.getroot()
    ICONS = {}
    formname = widget._action.form # TODO: MAL! el nombre del formulario es segun el UI
    # TODO: cuando conectamos en UI un control a una función QS usamos de 
    # receptor el formulario padre, por lo que la conexión recibirá el nombre del form padre.
    # TODO: Aunque es poco usual, es posible realizar una conexión a un slot que propiamente 
    # pertenece al formulario padre, por lo que ambos sistemas deben convivir, dar preferencia
    # al slot QS y si no existe intentar buscarlo en el UI.
    
    for xmlimage in root.xpath("images/image"):
        loadIcon(xmlimage)
        
    for xmlwidget in root.xpath("widget"):
        loadWidget(xmlwidget,widget)

    for xmlconnection in root.xpath("connections/connection"):
        sender_name = xmlconnection.xpath("sender/text()")[0]
        signal_name = xmlconnection.xpath("signal/text()")[0]
        receiv_name = xmlconnection.xpath("receiver/text()")[0]
        slot_name = xmlconnection.xpath("slot/text()")[0]
        sender = widget.findChild(QtGui.QWidget, sender_name)
        if sender is None: print "Connection sender not found:", sender_name
        if receiv_name == formname:
            print "Conectando de UI a QS: (%r.%r -> %r.%r)" % (sender_name, signal_name, receiv_name, slot_name)
        receiver = widget.findChild(QtGui.QWidget, receiv_name)
        if receiver is None: print "Connection receiver not found:", receiv_name
        if sender is None or receiver is None: continue
        try: QtCore.QObject.connect(sender, QtCore.SIGNAL(signal_name), receiver, QtCore.SLOT(slot_name))
        except Exception, e: 
            print "Error connecting:", sender, QtCore.SIGNAL(signal_name), receiver, QtCore.SLOT(slot_name)
            print "Error:", e.__class__.__name__, e


def createWidget(classname,parent = None):
    cls =  getattr(flcontrols, classname, None) or getattr(QtGui, classname, None)
    if cls is None: 
        print "WARN: Class name not found in QtGui:" , classname
        w = QtGui.QWidget(parent)
        w.setStyleSheet("* { background-color: #fa3; } ")
        return w
    return cls(parent)
    
def loadWidget(xml, widget = None):
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
        
    def process_property(xmlprop, widget = widget):
        pname = xmlprop.get("name")
        if pname in translate_properties: pname = translate_properties[pname]
        setpname = "set" + pname[0].upper() + pname[1:]
        if pname == "layoutSpacing":
            set_fn = widget.layout.setSpacing
        else:
            set_fn = getattr(widget, setpname, None)
        if set_fn is None: 
            print "Missing property", pname, " for ", widget.__class__.__name__
            return
        #print "Found property", pname 
        if pname == "contentsMargins" or pname == "layoutSpacing":
            try:
                value = int(xmlprop.get("stdset"))
            except Exception,e: value = 0
            if pname == "contentsMargins":
                value = QtCore.QMargins(value, value, value, value)
        else:
            value = loadVariant(xmlprop)

        try: set_fn(value)
        except Exception, e: 
            print e, repr(value)
            print etree.tostring(xmlprop)

    def process_layout_box(xmllayout, widget = widget, mode = "box"):
        for c in xmllayout:
            try:
                row = int(c.get("row"))
                col = int(c.get("column"))
            except Exception: row = col = None
            if c.tag == "property":
                process_property(c,widget.layout)
            elif c.tag == "widget":
                new_widget = createWidget(c.get("class"), parent=widget)
                loadWidget(c,new_widget)
                new_widget.show()
                if mode == "box":
                    widget.layout.addWidget(new_widget)
                elif mode == "grid":
                    widget.layout.addWidget(new_widget, row, col)
            elif c.tag == "spacer":
                properties = {}
                for p in c.xpath("property"):
                    k,v = loadProperty(p)
                    properties[k] = v
                if mode == "box":
                    widget.layout.addStretch()
                elif mode == "grid":
                    if properties["orientation"] == "Horizontal":
                        widget.layout.columnStretch(col)
                    else:
                        widget.layout.rowStretch(row)
            else:
                print "Unknown layout xml tag", repr(c.tag)
        
        widget.setLayout(widget.layout)
    properties = []
    for c in xml:
        if c.tag == "property":
            properties.append(c)
            continue
        if c.tag == "vbox":
            widget.layout = QtGui.QVBoxLayout()
            process_layout_box(c)
            continue
        if c.tag == "hbox":
            widget.layout = QtGui.QHBoxLayout()
            process_layout_box(c)
            continue
        if c.tag == "grid":
            widget.layout = QtGui.QGridLayout()
            process_layout_box(c,mode = "grid")
            continue
        if c.tag == "item":
            prop1 = {}
            for p in c.xpath("property"):
                k,v = loadProperty(p)
                prop1[k] = v
            widget.addItem(prop1["text"])
            continue
        print "Unknown widget xml tag", repr(c.tag)
    for c in properties:
        process_property(c)
    
def loadIcon(xml):
    global ICONS
    name = xml.get("name")
    xmldata = xml.xpath("data")[0]
    img_format = xmldata.get("format")
    data = unhexlify(xmldata.text.strip())
    pixmap = QtGui.QPixmap()
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
    if type(x) is unicode: return x
    if type(x) is str: return x.decode("UTF-8","replace")
    return unicode(str(x))

def b(x):
    x = x.lower()
    if x[0] == "t": return True
    if x[0] == "f": return False
    if x[0] == "1": return True
    if x[0] == "0": return False
    if x == "on": return True
    if x == "off": return False
    print "Bool?:", repr(x)
    return None
        

def _loadVariant(variant):
    text = variant.text or ""
    text = text.strip()
    if variant.tag == "cstring": return text
    if variant.tag == "iconset": 
        global ICONS
        return ICONS.get(text,text)
    if variant.tag == "string": return u(text)
    if variant.tag == "number": 
        if text.find('.') >= 0: return float(text)
        return int(text)
    if variant.tag == "bool": return b(text)
    if variant.tag == "rect": 
        k = {}
        for c in variant:
            k[c.tag] = int(c.text.strip())
        return QtCore.QRect(k['x'],k['y'],k['width'],k['height'])
        
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
                else: print "unknown font style type" ,repr(c.tag)
            except Exception, e:
                print e
        return p
    if variant.tag == "enum": 
        v = None
        libs = [Qt,QtGui.QFrame,QtGui.QSizePolicy]
        for lib in libs:
            v = getattr(lib,text,None)
            if v is not None: return v
        
        
    print "Unknown variant:", etree.tostring(variant)
        
    
