# -*- coding: utf-8 -*-

from builtins import str
from binascii import unhexlify

from lxml import etree
from PyQt5 import QtCore, QtGui, QtWidgets, uic

from pineboolib import flcontrols
from pineboolib.fllegacy import FLTableDB
from pineboolib.fllegacy import FLFieldDB

import zlib
from PyQt5.QtWidgets import QGroupBox
from PyQt5.Qt import QPalette, QSpacerItem

Qt = QtCore.Qt
ICONS = {}


class Options:
    DEBUG_LEVEL = 100


# TODO: Refactorizar este fichero como una clase. ICONS es la lista de iconos
#      para un solo formulario. Debe existir una clase LoadUI y que ICONS sea
#      una variable de ésta. Para cada nuevo formulario se debería instanciar
#      una nueva clase.

def loadUi(path, widget, parent=None):
    global ICONS
    parser = etree.XMLParser(
        ns_clean=True,
        encoding="UTF-8",
        remove_blank_text=True,
    )
    try:
        tree = etree.parse(path, parser)
    except Exception as e:
        print("Qt3Ui: Unable to read UI: %r" % path)
        raise
    root = tree.getroot()
    ICONS = {}
    widget.hide()
    if parent is None:
        parent = widget
    for xmlimage in root.xpath("images/image"):
        loadIcon(xmlimage)

    for xmlwidget in root.xpath("widget"):
        loadWidget(xmlwidget, widget, parent)

    # Debe estar despues de loadWidget porque queremos el valor del UI de Qt3
    formname = widget.objectName()
    if Options.DEBUG_LEVEL > 0:
        print("form:", formname)
    for xmlconnection in root.xpath("connections/connection"):
        sender_name = xmlconnection.xpath("sender/text()")[0]
        signal_name = xmlconnection.xpath("signal/text()")[0]
        receiv_name = xmlconnection.xpath("receiver/text()")[0]
        slot_name = xmlconnection.xpath("slot/text()")[0]

        sg_name = signal_name.replace("()", "")
        sg_name = sg_name.replace("(bool)", "")
        sg_name = sg_name.replace("(const QString&)", "")
        sl_name = slot_name.replace("()", "")
        sl_name = sl_name.replace("(bool)", "")
        sl_name = sl_name.replace("(const QString&)", "")

        #print("SG_NAME", sg_name)
        #print("SL_NAME", sl_name)

        if sender_name == formname:
            sender = widget
        else:
            sender = widget.findChild(QtWidgets.QWidget, sender_name)
        receiver = None
        if sender is None:
            if Options.DEBUG_LEVEL > 50:
                print("Connection sender not found:", sender_name)
        if receiv_name == formname:
            receiver = widget
            fn_name = slot_name.rstrip("()")
            if Options.DEBUG_LEVEL > 50:
                print("Conectando de UI a QS: (%r.%r -> %r.%r)" %
                      (sender_name, signal_name, receiv_name, fn_name))
            # print dir(widget.iface)
            if hasattr(widget.iface, fn_name):
                try:
                    getattr(sender, sg_name).connect(
                        getattr(widget.iface, fn_name))
                except Exception as e:
                    if Options.DEBUG_LEVEL > 50:
                        print("Error connecting:",
                              sender, signal_name,
                              receiver, slot_name,
                              getattr(widget.iface, fn_name))
                    if Options.DEBUG_LEVEL > 50:
                        print("Connect Error:", e.__class__.__name__, e)
                continue

        if receiver is None:
            receiver = widget.findChild(QtWidgets.QWidget, receiv_name)
        if receiver is None:
            print("Connection receiver not found:", receiv_name)
        if sender is None or receiver is None:
            continue
        try:
            getattr(sender, sg_name).connect(getattr(receiver, sl_name))
        except Exception as e:
            if Options.DEBUG_LEVEL > 50:
                print("Error connecting:", sender,
                      signal_name, receiver, slot_name)
            if Options.DEBUG_LEVEL > 50:
                print("Error:", e.__class__.__name__, e)
    widget.show()


def createWidget(classname, parent=None):
    cls = getattr(flcontrols, classname, None) or \
        getattr(QtWidgets, classname, None) or \
        getattr(FLTableDB, classname, None) or \
        getattr(FLFieldDB, classname, None)
    if cls is None:
        print("WARN: Class name not found in QtWidgets:", classname)
        widgt = QtWidgets.QWidget(parent)
        widgt.setStyleSheet("* { background-color: #fa3; } ")
        return widgt
    return cls(parent)


def loadWidget(xml, widget=None, parent=None):
    translate_properties = {
        "caption": "windowTitle",
        "name": "objectName",
        "icon": "windowIcon",
        "iconSet": "icon",
        "accel": "shortcut",
        "layoutMargin": "contentsMargins",
    }
    if widget is None:
        raise ValueError
    if parent is None:
        parent = widget

    def process_property(xmlprop, widget=widget):
        pname = xmlprop.get("name")
        if pname in translate_properties:
            pname = translate_properties[pname]
        setpname = "set" + pname[0].upper() + pname[1:]
        if pname == "layoutSpacing":
            set_fn = widget.layout.setSpacing
        elif pname == "margin":
            set_fn = widget.setContentsMargins
        elif pname in ("paletteBackgroundColor", "paletteForegroundColor"):
            set_fn = widget.setStyleSheet
        else:
            set_fn = getattr(widget, setpname, None)
        if set_fn is None:
            if Options.DEBUG_LEVEL > 50:
                print("qt3ui: Missing property", pname,
                      " for %r" % widget.__class__)
            return
        # print "Found property", pname
        if pname == "contentsMargins" or pname == "layoutSpacing":
            try:
                value = int(xmlprop.get("stdset"))
                value /= 2
            except Exception as e:
                value = 0
            if pname == "contentsMargins":
                value = QtCore.QMargins(value, value, value, value)

        elif pname == "margin":
            try:
                value = loadVariant(xmlprop)
            except:
                value = 0
            value = QtCore.QMargins(value, value, value, value)

        elif pname == "paletteBackgroundColor":
            value = 'background-color:' + loadVariant(xmlprop).name()

        elif pname == "paletteForegroundColor":
            value = 'color:' + loadVariant(xmlprop).name()
        else:
            value = loadVariant(xmlprop)

        try:
            set_fn(value)
        except Exception as e:
            if Options.DEBUG_LEVEL > 50:
                print(e, repr(value))
            if Options.DEBUG_LEVEL > 50:
                print(etree.tostring(xmlprop))

    def process_layout_box(xmllayout, widget=widget, mode="box"):
        for c in xmllayout:
            try:
                row = int(c.get("row"))
                col = int(c.get("column"))
            except Exception:
                row = col = None
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
                sH = None
                sV = None
                hPolicy = QtWidgets.QSizePolicy.Fixed
                vPolicy = QtWidgets.QSizePolicy.Fixed
                orient_ = None
                policy_ = None

                for p in c.xpath("property"):
                    pname, value = loadProperty(p)
                    if pname == "sizeHint":
                        sH = value.width()
                        sV = value.height()
                    elif pname == "orientation":
                        if value == 0:
                            orient_ = 0
                        else:
                            orient_ = 1
                    elif pname == "sizeType":
                        policy_ = QtWidgets.QSizePolicy.Policy(value)

                if orient_ == 0:
                    vPolicy = policy_
                else:
                    hPolicy = policy_

                new_spacer = QSpacerItem(sH, sV, hPolicy, vPolicy)
                widget.layout.addItem(new_spacer)

            else:
                if Options.DEBUG_LEVEL > 50:
                    print("qt3ui: Unknown layout xml tag", repr(c.tag))

        widget.setLayout(widget.layout)
        widget.layout.setContentsMargins(1, 1, 1, 1)
        widget.layout.setSpacing(1)
        widget.layout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)

    layouts_pending_process = []
    properties = []
    unbold_fonts = []
    for c in xml:
        if c.tag == "property":
            properties.append(c)
            continue
        if c.tag == "vbox":
            # TODO: layout se solapa con el layout de FormInternalObj
            if isinstance(getattr(widget, "layout", None), QtWidgets.QLayout):
                if Options.DEBUG_LEVEL > 50:
                    print("qt3ui: Trying to replace layout. Ignoring.",
                          repr(c.tag), widget.layout)
                continue
            widget.layout = QtWidgets.QVBoxLayout()
            widget.layout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
            widget.layout.setSpacing(3)
            widget.layout.setContentsMargins(3, 3, 3, 3)

            layouts_pending_process += [(c, "box")]
            #process_layout_box(c, mode="box")
            continue
        if c.tag == "hbox":
            if isinstance(getattr(widget, "layout", None), QtWidgets.QLayout):
                if Options.DEBUG_LEVEL > 50:
                    print("qt3ui: Trying to replace layout. Ignoring.",
                          repr(c.tag), widget.layout)
                continue
            widget.layout = QtWidgets.QHBoxLayout()
            widget.layout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
            widget.layout.setSpacing(3)
            widget.layout.setContentsMargins(3, 3, 3, 3)
            layouts_pending_process += [(c, "box")]
            #process_layout_box(c, mode="box")
            continue
        if c.tag == "grid":
            if isinstance(getattr(widget, "layout", None), QtWidgets.QLayout):
                if Options.DEBUG_LEVEL > 50:
                    print("qt3ui: Trying to replace layout. Ignoring.",
                          repr(c.tag), widget.layout)
                continue
            widget.layout = QtWidgets.QGridLayout()
            widget.layout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
            widget.layout.setSpacing(3)
            widget.layout.setContentsMargins(3, 3, 3, 3)
            layouts_pending_process += [(c, "grid")]
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
                print("qt3ui: [NOT ASSIGNED] attribute %r => %r" %
                      (k, v), widget.__class__, repr(c.tag))
            continue
        if c.tag == "widget":
            # Si dentro del widget hay otro significa que estamos dentro de un contenedor.
            # Según el tipo de contenedor, los widgets se agregan de una forma u otra.
            new_widget = createWidget(c.get("class"), parent=parent)
            new_widget.hide()
            new_widget._attrs = {}
            loadWidget(c, new_widget, parent)
            new_widget.setContentsMargins(0, 0, 0, 0)
            new_widget.show()
            if isinstance(widget, QtWidgets.QTabWidget):
                title = new_widget._attrs.get("title", "UnnamedTab")
                widget.addTab(new_widget, title)

            elif isinstance(widget, QtWidgets.QGroupBox) or isinstance(widget, QtWidgets.QWidget):
                lay = widget.layout()
                if not lay:
                    lay = QtWidgets.QVBoxLayout()
                    widget.setLayout(lay)

                lay.addWidget(new_widget)
            else:
                if Options.DEBUG_LEVEL > 50:
                    print("qt3ui: Unknown container widget xml tag",
                          widget.__class__, repr(c.tag))
            unbold_fonts.append(new_widget)
            continue

        if Options.DEBUG_LEVEL > 50:
            print("qt3ui: Unknown widget xml tag",
                  widget.__class__, repr(c.tag))
    for c in properties:
        process_property(c)
    for c, m in layouts_pending_process:
        process_layout_box(c, mode=m)
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
        data = zlib.decompress(data, 15)
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
    if isinstance(x, str):
        return x
    return str(x)


def b(x):
    x = x.lower()
    if x[0] == "t":
        return True
    if x[0] == "f":
        return False
    if x[0] == "1":
        return True
    if x[0] == "0":
        return False
    if x == "on":
        return True
    if x == "off":
        return False
    print("Bool?:", repr(x))
    return None


def _loadVariant(variant):
    text = variant.text or ""
    text = text.strip()
    if variant.tag == "cstring":
        return text
    if variant.tag == "iconset":
        global ICONS
        return ICONS.get(text, text)
    if variant.tag == "string":
        return u(text)
    if variant.tag == "number":
        if text.find('.') >= 0:
            return float(text)
        return int(text)
    if variant.tag == "bool":
        return b(text)
    if variant.tag == "rect":
        k = {}
        for c in variant:
            k[c.tag] = int(c.text.strip())
        return QtCore.QRect(k['x'], k['y'], k['width'], k['height'])

    if variant.tag == "sizepolicy":
        p = QtWidgets.QSizePolicy()
        for c in variant:
            value = int(c.text.strip())
            if c.tag == "hsizetype":
                p.setHorizontalPolicy(value)
            if c.tag == "vsizetype":
                p.setVerticalPolicy(value)
            if c.tag == "horstretch":
                p.setHorizontalStretch(value)
            if c.tag == "verstretch":
                p.setVerticalStretch(value)
        return p
    if variant.tag == "size":
        p = QtCore.QSize()
        for c in variant:
            value = int(c.text.strip())
            if c.tag == "width":
                p.setWidth(value)
            if c.tag == "height":
                p.setHeight(value)
        return p
    if variant.tag == "font":
        p = QtGui.QFont()
        for c in variant:
            value = c.text.strip()
            bv = False
            if not c.tag in ("family", "pointsize"):
                bv = b(value)
            try:
                if c.tag == "bold":
                    p.setBold(bv)
                elif c.tag == "italic":
                    p.setItalic(bv)
                elif c.tag == "family":
                    p.setFamily(value)
                elif c.tag == "pointsize":
                    p.setPointSize(int(value))
                else:
                    print("unknown font style type", repr(c.tag))
            except Exception as e:
                if Options.DEBUG_LEVEL > 50:
                    print(e)
        return p

    if variant.tag == "set":
        v = None
        text = variant.text
        libs = [QtCore.Qt]
        if text == "WordBreak|AlignVCenter":
            text = "AlignVCenter"
        if text == "WordBreak|AlignTop":
            text = "AlignTop"
        if text == "AlignVCenter|AlignRight":
            text = "AlignRight"
        if text == "AlignVCenter|AlignLeft":
            text = "AlignLeft"
        for lib in libs:
            v = getattr(lib, text, None)
        if v is not None:
            return v

    if variant.tag == "enum":
        v = None
        libs = [Qt, QtWidgets.QFrame,
                QtWidgets.QSizePolicy, QtWidgets.QTabWidget]
        for lib in libs:
            v = getattr(lib, text, None)
            if v is not None:
                return v
        if text == "GroupBoxPanel":
            return QtWidgets.QFrame.StyledPanel
        if text == "Single":
            return QtWidgets.QAbstractItemView.SingleSelection
        if text == "FollowStyle":
            return "QtWidgets.QTableView {selection-background-color: red;}"

    if variant.tag == "color":
        c = QtGui.QColor()
        red_ = 0
        green_ = 0
        blue_ = 0
        for color in variant:
            if color.tag == "red":
                red_ = int(color.text.strip())
            elif color.tag == "green":
                green_ = int(color.text.strip())
            elif color.tag == "blue":
                blue_ = int(color.text.strip())

        c.setRgb(red_, green_, blue_)
        return c

    if Options.DEBUG_LEVEL > 50:
        print("qt3ui: Unknown variant:", etree.tostring(variant))
