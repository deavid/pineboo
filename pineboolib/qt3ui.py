# encoding: UTF-8
from lxml import etree
from PyQt4 import QtGui, QtCore, uic
Qt = QtCore.Qt

def loadUi(path, widget):
    parser = etree.XMLParser(
                    ns_clean=True,
                    encoding="UTF-8",
                    remove_blank_text=True,
                    )
    tree = etree.parse(path, parser)
    root = tree.getroot()
    
    for xmlwidget in root.xpath("widget"):
        loadWidget(xmlwidget,widget)

def loadWidget(xml, widget = None):
    translate_properties = {
        "caption" : "windowTitle",
        "name" : "objectName",
        "icon" : "windowIcon",
    }
    if widget is None: 
        raise ValueError
    for xmlprop in xml.xpath("property"):
        pname = xmlprop.get("name")
        if pname in translate_properties: pname = translate_properties[pname]
        setpname = "set" + pname[0].upper() + pname[1:]
        set_fn = getattr(widget, setpname, None)
        if set_fn is None: 
            print "Missing property", pname 
            continue
        print "Found property", pname 
        value = loadVariant(xmlprop)
        try: set_fn(value)
        except Exception, e: print e, repr(value)
        
    
    

def loadVariant(xml):
    for variant in xml:
        return _loadVariant(variant)

def loadProperty(xml):
    for variant in xml:
        return (xml.get("name"), _loadVariant(variant))

def u(x):
    if type(x) is unicode: return x
    if type(x) is str: return x.decode("UTF-8","replace")
    return str(x)
    

def _loadVariant(variant):
    text = variant.text or ""
    text = text.strip()
    if variant.tag == "cstring": return text
    if variant.tag == "string": return u(text)
    if variant.tag == "rect": 
        k = {}
        for c in variant:
            k[c.tag] = int(c.text.strip())
        return QtCore.QRect(k['x'],k['y'],k['width'],k['height'])
        
    
