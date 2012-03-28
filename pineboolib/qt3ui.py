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
    for xmlimage in root.xpath("images/image"):
        loadIcon(xmlimage)
        
    for xmlwidget in root.xpath("widget"):
        loadWidget(xmlwidget,widget)

def createWidget(classname):
    cls =  getattr(flcontrols, classname, None) or getattr(QtGui, classname, None)
    if cls is None: 
        print "WARN: Class name not found in QtGui:" , classname
        w = QtGui.QWidget()
        w.setStyleSheet("* { background-color: #fa3; } ")
        return w
    return cls()
    
def loadWidget(xml, widget = None):
    translate_properties = {
        "caption" : "windowTitle",
        "name" : "objectName",
        "icon" : "windowIcon",
        "iconSet" : "icon",
        "accel" : "shortcut",
    }
    if widget is None: 
        raise ValueError
        
    def process_property(xmlprop, widget = widget):
        pname = xmlprop.get("name")
        if pname in translate_properties: pname = translate_properties[pname]
        setpname = "set" + pname[0].upper() + pname[1:]
        set_fn = getattr(widget, setpname, None)
        if set_fn is None: 
            print "Missing property", pname, " for ", widget.__class__.__name__
            return
        #print "Found property", pname 
        value = loadVariant(xmlprop)
        try: set_fn(value)
        except Exception, e: print e, repr(value)

    def process_layout_box(xmllayout, widget = widget):
        for c in xmllayout:
            if c.tag == "property":
                process_property(c,widget.layout)
            elif c.tag == "widget":
                new_widget = createWidget(c.get("class"))
                loadWidget(c,new_widget)
                new_widget.show()
                widget.layout.addWidget(new_widget)
            elif c.tag == "spacer":
                widget.layout.addStretch()
            else:
                print "Unknown layout xml tag", repr(c.tag)
        
        widget.setLayout(widget.layout)
    
    for c in xml:
        if c.tag == "property":
            process_property(c)
            continue
        if c.tag == "vbox":
            widget.layout = QtGui.QVBoxLayout()
            process_layout_box(c)
            continue
        if c.tag == "hbox":
            widget.layout = QtGui.QHBoxLayout()
            process_layout_box(c)
            continue
        print "Unknown widget xml tag", repr(c.tag)
    
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
        libs = [Qt,QtGui.QFrame]
        for lib in [Qt,QtGui.QFrame]:
            v = getattr(lib,text,None)
            if v is not None: return v
        
        
    print "Unknown variant:", etree.tostring(variant)
        
    
