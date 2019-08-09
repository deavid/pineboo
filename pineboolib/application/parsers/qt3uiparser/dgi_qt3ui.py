# -*- coding: utf-8 -*-
"""
Module dgi_qt3ui.

Loads old Qt3 UI files and creates a Qt5 UI.
"""
from importlib import import_module

from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore
from PyQt5.QtWidgets import QWidget
from xml.etree import ElementTree as ET
from binascii import unhexlify
from pineboolib import logging
import zlib
from PyQt5.QtCore import QObject  # type: ignore
from pineboolib.core.utils.utils_base import load2xml
from pineboolib.application import project
from pineboolib.application import connections

from pineboolib.qt3_widgets import qmainwindow
from pineboolib.qt3_widgets import qtoolbar
from pineboolib.qt3_widgets import qmenu
from pineboolib.qt3_widgets import qaction
from pineboolib.qt3_widgets import qspinbox

from pineboolib.core.settings import config


from typing import Optional, Tuple, Callable, List, Dict, Any, cast, Type


ICONS: Dict[str, Any] = {}
root = None
logger = logging.getLogger("pnqt3ui")


class Options:
    """
    Store module options.

    ***DEPRECATED***
    """

    DEBUG_LEVEL = 100


# TODO: Refactorizar este fichero como una clase. ICONS es la lista de iconos
#      para un solo formulario. Debe existir una clase LoadUI y que ICONS sea
#      una variable de ésta. Para cada nuevo formulario se debería instanciar
#      una nueva clase.


# FIXME: widget is QWidget type but Qt5-Stubs for findChild reports QObject instead of Optional[QObject]
def loadUi(form_path: str, widget: Any, parent: Optional[QWidget] = None) -> None:
    """
    Load Qt3 UI file from eneboo.

    widget: Provide a pre-created widget and this function will store UI contents on it.
    parent: Probably deprecated.
    """
    global ICONS, root
    # parser = etree.XMLParser(
    #    ns_clean=True,
    #    encoding="UTF-8",
    #    remove_blank_text=True,
    # )

    tree = load2xml(form_path)

    if not tree:
        return

    root = tree.getroot()
    ICONS = {}

    if parent is None:
        parent = widget

    # if project.DGI.localDesktop():
    widget.hide()

    for xmlimage in root.findall("images//image"):
        loadIcon(xmlimage)

    for xmlwidget in root.findall("widget"):
        loadWidget(xmlwidget, widget, parent)

    # print("----------------------------------")
    # for xmlwidget in root.xpath("actions"):
    #     loadWidget(xmlwidget, widget, parent)
    # print("----------------------------------")

    # Debe estar despues de loadWidget porque queremos el valor del UI de Qt3
    formname = widget.objectName()
    logger.info("form: %s", formname)

    # Cargamos actions...
    for action in root.findall("actions//action"):
        loadAction(action, widget)

    for xmlconnection in root.findall("connections//connection"):
        sender_elem = xmlconnection.find("sender")
        signal_elem = xmlconnection.find("signal")
        receiv_elem = xmlconnection.find("receiver")
        slot_elem = xmlconnection.find("slot")

        if sender_elem is None or signal_elem is None or receiv_elem is None or slot_elem is None:
            continue

        sender_name = sender_elem.text
        signal_name = signal_elem.text
        receiv_name = receiv_elem.text
        slot_name = slot_elem.text

        if sender_name is None:
            raise ValueError("no se encuentra sender_name")
        if signal_name is None:
            raise ValueError("no se encuentra signal_name")
        if receiv_name is None:
            raise ValueError("no se encuentra receiv_name")
        if slot_name is None:
            raise ValueError("no se encuentra slot_name")

        receiver = None
        if isinstance(widget, qmainwindow.QMainWindow):
            if signal_name == "activated()":
                signal_name = "triggered()"

        if sender_name == formname:
            sender = widget
        else:
            sender = widget.findChild(QObject, sender_name, QtCore.Qt.FindChildrenRecursively)

        # if not project.DGI.localDesktop():
        #    wui = hasattr(widget, "ui_") and sender_name in widget.ui_
        #    if sender is None and wui:
        #        sender = widget.ui_[sender_name]

        sg_name = signal_name

        if signal_name.find("(") > -1:
            sg_name = signal_name[: signal_name.find("(")]

        sl_name = slot_name
        if slot_name.find("(") > -1:
            sl_name = slot_name[: slot_name.find("(")]

        if sender is None:
            logger.warning("Connection sender not found:%s", sender_name)
        if receiv_name == formname:
            receiver = (
                widget
                if not isinstance(widget, qmainwindow.QMainWindow)
                else project.actions[sender_name]
                if sender_name in project.actions.keys()
                else None
            )
            fn_name = slot_name.rstrip("()")
            logger.trace(
                "Conectando de UI a QS: (%r.%r -> %r.%r)",
                sender_name,
                signal_name,
                receiv_name,
                fn_name,
            )

            ifx = widget
            # if hasattr(widget, "iface"):
            #    ifx = widget.iface
            if hasattr(ifx, fn_name):
                try:

                    # getattr(sender, sg_name).connect(
                    #    getattr(ifx, fn_name))
                    connections.connect(sender, signal_name, ifx, fn_name)
                except Exception:
                    logger.exception(
                        "Error connecting: %s %s %s %s %s",
                        sender,
                        signal_name,
                        receiver,
                        slot_name,
                        getattr(ifx, fn_name),
                    )
                continue

        if receiver is None:
            receiver = widget.findChild(QObject, receiv_name, QtCore.Qt.FindChildrenRecursively)

        if receiver is None:
            from pineboolib.application.safeqsa import SafeQSA

            receiver = SafeQSA.get_any(receiv_name)

        if receiver is None and receiv_name == "FLWidgetApplication":
            if sender_name in project.actions.keys():
                receiver = project.actions[sender_name]
            else:
                logger.warning("Sender action %s not found. Connection skiped", sender_name)
                continue

        if receiver is None:
            logger.warning("Connection receiver not found:%s", receiv_name)
        if sender is None or receiver is None:
            continue

        if hasattr(receiver, "iface"):
            iface = getattr(receiver, "iface")
            if hasattr(iface, sl_name):
                try:
                    getattr(sender, sg_name).connect(getattr(iface, sl_name))
                except Exception:
                    logger.exception(
                        "Error connecting: %s:%s %s.iface:%s",
                        sender,
                        signal_name,
                        receiver,
                        slot_name,
                    )
                continue
        if hasattr(receiver, sl_name):
            try:
                getattr(sender, sg_name).connect(getattr(receiver, sl_name))
            except Exception:
                logger.exception(
                    "Error connecting: %s:%s %s:%s", sender, signal_name, receiver, slot_name
                )
        else:
            logger.error(
                "Error connecting: %s:%s %s:%s (no candidate found)",
                sender,
                signal_name,
                receiver,
                slot_name,
            )

    # Cargamos menubar ...
    xmlmenubar = root.find("menubar")
    if xmlmenubar:
        # nameMB_ = xmlmenubar.find("./property[@name='name']/cstring").text
        # bar = widget.menuBar()
        # for itemM in xmlmenubar.findall("item"):
        #    menubar = bar.addMenu(itemM.get("text"))
        #    loadWidget(itemM, menubar, parent, widget)
        loadMenuBar(xmlmenubar, widget)

    # Cargamos toolbars ...
    for xmltoolbar in root.findall("toolbars//toolbar"):
        # nameTB_ = xmltoolbar.find("./property[@name='name']/cstring").text
        # toolbar = widget.addToolBar(nameTB_)
        loadToolBar(xmltoolbar, widget)

    if project._DGI and not project.DGI.localDesktop():
        project.DGI.showWidget(widget)
    else:
        widget.show()


def loadToolBar(xml: ET.Element, widget: QWidget) -> None:
    """
    Load UI Toolbar from XML and store it into widget.

    widget: A pre-created widget to store the toolbar.
    """
    name_elem = xml.find("./property[@name='name']/cstring")
    label_elem = xml.find("./property[@name='label']/string")
    if name_elem is None or label_elem is None:
        raise Exception("Unable to find required name and label properties")

    name = name_elem.text
    label = label_elem.text

    tb = qtoolbar.QToolBar(name)
    tb.label = label
    for a in xml:
        if a.tag == "action":
            name = a.get("name") or "action"
            ac_ = tb.addAction(name)
            ac_.setObjectName(name)
            load_action(ac_, widget)

            # FIXME!!, meter el icono y resto de datos!!
        elif a.tag == "separator":
            tb.addSeparator()

    widget.addToolBar(tb)


def loadMenuBar(xml: ET.Element, widget: QWidget) -> None:
    """
    Load a menu bar into widget.

    widget: pre-created widget to store the object.
    """

    if isinstance(widget, qmainwindow.QMainWindow):
        mB = widget.menuBar()
    else:
        mB = QtWidgets.QMenuBar(widget)
        widget._layout().setMenuBar(mB)
    for x in xml:
        if x.tag == "property":
            name = x.get("name")
            if name == "name":
                cstring = x.find("cstring")
                if cstring is not None and cstring.text is not None:
                    mB.setObjectName(cstring.text)
            elif name == "geometry":
                geo_ = x.find("rect")
                if geo_:
                    ex, ey, ew, eh = (
                        geo_.find("x"),
                        geo_.find("y"),
                        geo_.find("width"),
                        geo_.find("height"),
                    )
                    if ex is None or ey is None or ew is None or eh is None:
                        continue
                    x1 = ex.text
                    y1 = ey.text
                    w1 = ew.text
                    h1 = eh.text
                    if x1 is None or y1 is None or w1 is None or h1 is None:
                        continue
                    mB.setGeometry(int(x1), int(y1), int(w1), int(h1))
            elif name == "acceptDrops":
                bool_elem = x.find("bool")
                if bool_elem is not None:
                    mB.setAcceptDrops(bool_elem.text == "true")
            elif name == "frameShape":
                continue
            elif name == "defaultUp":
                bool_elem = x.find("bool")
                if bool_elem is not None:
                    mB.setDefaultUp(bool_elem.text == "true")
        elif x.tag == "item":
            process_item(x, mB, widget)


def process_item(xml: ET.Element, parent: QWidget, widget: QWidget) -> None:
    """
    Process random XML item.

    widget: pre-created widget to store the object.
    """
    name = xml.get("name")
    text = xml.get("text")
    # accel = xml.get("accel")

    menu_ = parent.addMenu(text)
    menu_.setObjectName(name)
    for x in xml:
        if x.tag == "action":
            name = x.get("name")
            ac_ = menu_.addAction(name)
            ac_.setObjectName(name)
            load_action(ac_, widget)
        elif x.tag == "item":
            process_item(x, menu_, widget)


def load_action(action: QtWidgets.QAction, widget: QWidget) -> None:
    """
    Load Action into widget.

    widget: pre-created widget to store the object.
    used only on loadToolBar and process_item
    """
    real_action = widget.findChild(QtWidgets.QAction, action.objectName())
    if real_action is not None:
        action.setText(real_action.text())
        action.setIcon(real_action.icon())
        action.setToolTip(real_action.toolTip())
        if real_action.statusTip():
            action.setStatusTip(real_action.statusTip())
        else:
            action.setStatusTip(real_action.whatsThis())
        action.setWhatsThis(real_action.whatsThis())
        action.triggered.connect(real_action.trigger)
        action.toggled.connect(real_action.toggle)


def loadAction(action: ET.Element, widget: QWidget) -> None:
    """
    Load Action into widget.

    widget: pre-created widget to store the object.
    """
    # FIXME: Why there are two loadAction??
    global ICONS
    act_ = QtWidgets.QAction(widget)
    for p in action.findall("property"):
        name = p.get("name")
        cstring = p.find("cstring")
        string = p.find("string")
        iconset = p.find("iconset")

        if name == "name" and cstring is not None:
            act_.setObjectName(cstring.text or "unnamed")
        elif name == "text" and string is not None:
            act_.setText(string.text or "")
        elif name == "iconSet" and iconset is not None:
            if iconset.text and iconset.text in ICONS.keys():
                act_.setIcon(ICONS[iconset.text])
        elif name == "toolTip" and string is not None:
            act_.setToolTip(string.text or "")
        elif name == "statusTip" and string is not None:
            act_.setStatusTip(string.text or "")
        elif name == "whatsThis" and string is not None:
            act_.setWhatsThis(string.text or "")


class WidgetResolver:
    """
    Resolve classnames into widgets with caching.
    """

    KNOWN_WIDGETS: Dict[str, Type[QtWidgets.QWidget]] = {}

    @classmethod
    def get_widget_class(resolver_cls, classname: str) -> Type[QtWidgets.QWidget]:
        """Get a widget class from class name."""
        if classname in resolver_cls.KNOWN_WIDGETS:
            return resolver_cls.KNOWN_WIDGETS[classname]

        cls: Optional[Type[QtWidgets.QWidget]] = None
        mod_name_full = "pineboolib.qt3_widgets.%s" % classname.lower()
        try:
            mod_ = import_module(mod_name_full)
            cls = getattr(mod_, classname, None)
        except ModuleNotFoundError:
            logger.trace("resolveObject: Module not found %s", mod_name_full)
        except Exception:
            logger.exception("resolveObject: Unable to load module %s", mod_name_full)

        if cls is None:
            mod_name_full = "pineboolib.fllegacy.%s" % classname.lower()
            try:
                mod_ = import_module(mod_name_full)
                cls = getattr(mod_, classname, None)
            except ModuleNotFoundError:
                logger.trace("resolveObject: Module not found %s", mod_name_full)
            except Exception:
                logger.exception("resolveObject: Unable to load module %s", mod_name_full)

        if cls is None:
            cls = getattr(QtWidgets, classname, None)

        if cls is None:
            raise AttributeError("Class %r not found" % classname)

        resolver_cls.KNOWN_WIDGETS[classname] = cls
        return cls


# NOTE: This function may create QAction too, which inherits from QObject, not QWidget.
def createWidget(classname: str, parent: Optional[QWidget] = None) -> QtCore.QObject:
    """
    Create a Widget for given class name.
    """
    # FIXME: Avoid dynamic imports. Also, this is slow.
    try:
        cls = WidgetResolver.get_widget_class(classname)
        return cls(parent)
    except AttributeError:
        logger.warning("WARN: Class name not found in QtWidgets:", classname)
        widgt = QtWidgets.QWidget(parent)
        widgt.setStyleSheet("* { background-color: #fa3; } ")
        return widgt


class loadWidget:
    """Load a widget."""

    translate_properties = {
        "caption": "windowTitle",
        "name": "objectName",
        "icon": "windowIcon",
        "iconSet": "icon",
        "accel": "shortcut",
        "layoutMargin": "contentsMargins",
    }
    widget: QtWidgets.QWidget
    parent: QtWidgets.QWidget
    origWidget: QtWidgets.QWidget

    def __init__(
        self,
        xml: ET.Element,
        widget: QtWidgets.QWidget,
        parent: Optional[QtWidgets.QWidget] = None,
        origWidget: Optional[QtWidgets.QWidget] = None,
    ) -> None:
        """
        Load a random widget from given XML.
        """
        logger.trace(
            "loadWidget: xml: %s widget: %s parent: %s origWidget: %s",
            xml,
            widget,
            parent,
            origWidget,
        )
        if widget is None:
            raise ValueError
        if parent is None:
            parent = widget
        if origWidget is None:
            origWidget = widget
        self.widget = widget
        self.origWidget = origWidget
        self.parent = parent
        del widget
        del origWidget
        del parent
        # if project.DGI.localDesktop():
        #    if not hasattr(origWidget, "ui_"):
        #        origWidget.ui_ = {}
        # else:
        #    origWidget.ui_ = {}

        nwidget = None
        if self.widget == self.origWidget:
            class_ = xml.get("class")
            if class_ is None:
                class_ = type(self.widget).__name__

            nwidget = createWidget(class_, parent=self.origWidget)
            self.parent = nwidget
        layouts_pending_process: List[Tuple[ET.Element, str]] = []
        properties = []
        unbold_fonts = []
        has_layout_defined = False

        for c in xml:
            if c.tag == "layout":
                # logger.warning("Trying to replace layout. Ignoring. %s, %s", repr(c.tag), widget._layout)
                classname = c.get("class")
                if classname is None:
                    raise Exception("Expected class attr")
                lay_ = getattr(QtWidgets, classname)()
                lay_.setObjectName(c.get("name"))
                self.widget.setLayout(lay_)
                continue

            if c.tag == "property":
                properties.append(c)
                continue

            if c.tag in ("vbox", "hbox", "grid"):
                if (
                    has_layout_defined
                ):  # nos saltamos una nueva definición del layout ( mezclas de ui incorrectas)
                    # El primer layout que se define es el que se respeta
                    continue

                if c.tag.find("box") > -1:
                    layout_type = "Q%s%sLayout" % (c.tag[0:2].upper(), c.tag[2:])
                else:
                    layout_type = "QGridLayout"
                _LayoutClass = getattr(QtWidgets, layout_type)
                self.widget._layout = cast(QtWidgets.QLayout, _LayoutClass())

                lay_name = None
                lay_margin_v = 2
                lay_margin_h = 2
                lay_spacing = 2
                for p in c.findall("property"):
                    p_name = p.get("name")
                    number_elem = p.find("number")

                    if p_name == "name":
                        lay_name_e = p.find("cstring")
                        if lay_name_e is not None:
                            lay_name = lay_name_e.text
                    elif p_name == "margin":
                        if number_elem is not None:
                            if number_elem.text is None:
                                raise ValueError("margin no contiene valor")
                            lay_margin = int(number_elem.text)

                        if c.tag == "hbox":
                            lay_margin_h = lay_margin
                        elif c.tag == "vbox":
                            lay_margin_v = lay_margin
                        else:
                            lay_margin_h = lay_margin_v = lay_margin

                    elif p_name == "spacing":
                        if number_elem is not None:
                            if number_elem.text is None:
                                raise ValueError("spacing no contiene valor")
                            lay_spacing = int(number_elem.text)
                    elif p_name == "sizePolicy":
                        self.widget.setSizePolicy(loadVariant(p, self.widget))

                self.widget._layout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
                self.widget._layout.setObjectName(lay_name or "layout")
                self.widget._layout.setContentsMargins(
                    lay_margin_h, lay_margin_v, lay_margin_h, lay_margin_v
                )
                self.widget._layout.setSpacing(lay_spacing)

                lay_type = "grid" if c.tag == "grid" else "box"
                layouts_pending_process += [(c, lay_type)]
                has_layout_defined = True
                continue

            if c.tag == "item":
                if isinstance(self.widget, qmenu.QMenu):
                    continue
                else:
                    prop1: Dict[str, Any] = {}
                    for p in c.findall("property"):
                        k, v = loadProperty(p)
                        prop1[k] = v

                    self.widget.addItem(prop1["text"])
                continue

            if c.tag == "attribute":
                k = c.get("name")
                v = loadVariant(c)
                attrs = getattr(self.widget, "_attrs", None)
                if attrs is not None:
                    attrs[k] = v
                else:
                    logger.warning(
                        "qt3ui: [NOT ASSIGNED] attribute %r => %r" % (k, v),
                        self.widget.__class__,
                        repr(c.tag),
                    )
                continue
            if c.tag == "widget":
                # Si dentro del widget hay otro significa
                # que estamos dentro de un contenedor.
                # Según el tipo de contenedor, los widgets
                # se agregan de una forma u otra.
                classname = c.get("class")
                if classname is None:
                    raise Exception("Expected class attr")
                new_widget = createWidget(classname, parent=self.parent)
                new_widget.hide()
                new_widget._attrs = {}
                loadWidget(c, new_widget, self.parent, self.origWidget)
                prop_name = c.find("./property[@name='name']/cstring")
                path = prop_name.text if prop_name is not None else ""
                if project._DGI and not project.DGI.localDesktop():
                    self.origWidget.ui_[path] = new_widget
                new_widget.setContentsMargins(0, 0, 0, 0)
                new_widget.show()

                gb = isinstance(self.widget, QtWidgets.QGroupBox)
                wd = isinstance(self.widget, QtWidgets.QWidget)
                if isinstance(self.widget, QtWidgets.QTabWidget):
                    title = new_widget._attrs.get("title", "UnnamedTab")
                    self.widget.addTab(new_widget, title)
                elif gb or wd:
                    lay = getattr(self.widget, "layout")()
                    if not lay and not isinstance(self.widget, qtoolbar.QToolBar):
                        lay = QtWidgets.QVBoxLayout()
                        self.widget.setLayout(lay)

                    if isinstance(self.widget, qtoolbar.QToolBar):
                        if isinstance(new_widget, QtWidgets.QAction):
                            self.widget.addAction(new_widget)
                        else:
                            self.widget.addWidget(new_widget)
                    else:
                        lay.addWidget(new_widget)
                else:
                    if Options.DEBUG_LEVEL > 50:
                        logger.warning(
                            "qt3ui: Unknown container widget xml tag",
                            self.widget.__class__,
                            repr(c.tag),
                        )
                unbold_fonts.append(new_widget)
                continue

            if c.tag == "action":
                acName = c.get("name")
                if root is None:
                    raise Exception("No se encuentra root")

                for xmlaction in root.findall("actions//action"):
                    prop_name = xmlaction.find("./property[@name='name']/cstring")
                    if prop_name is not None and prop_name.text == acName:
                        self.process_action(xmlaction, self.widget)
                        continue

                continue

            if c.tag == "separator":
                self.widget.addSeparator()
                continue

            if c.tag == "column":
                for p in c.findall("property"):
                    k, v = loadProperty(p)
                    if k == "text":
                        self.widget.setHeaderLabel(v)
                    elif k == "clickable":
                        self.widget.setClickable(bool(v))
                    elif k == "resizable":
                        self.widget.setResizable(bool(v))

                continue

            logger.info(
                "%s: Unknown widget xml tag %s %s", __name__, self.widget.__class__, repr(c.tag)
            )

        for c in properties:
            self.process_property(c)
        for c, m in layouts_pending_process:
            self.process_layout_box(c, mode=m)
        for new_widget in unbold_fonts:
            f = new_widget.font()
            f.setBold(False)
            f.setItalic(False)
            new_widget.setFont(f)

        # if not project.DGI.localDesktop():
        #    if nwidget is not None and origWidget.objectName() not in origWidget.ui_:
        #        origWidget.ui_[origWidget.objectName()] = nwidget

    def process_property(self, xmlprop: ET.Element, widget: Optional[QtCore.QObject] = None):
        """
        Process a XML property from the UI.
        """
        if widget is None:
            widget = self.widget
        set_fn: Optional[Callable] = None
        pname = xmlprop.get("name") or ""
        pname = self.translate_properties.get(pname, pname)
        setpname = "set" + pname[0].upper() + pname[1:]
        if pname == "layoutSpacing":
            set_fn = widget._layout.setSpacing
        elif pname == "margin":
            set_fn = widget.setContentsMargins
        elif pname in ("paletteBackgroundColor", "paletteForegroundColor"):
            set_fn = widget.setStyleSheet
        elif pname == "menuText":
            if isinstance(widget, qaction.QAction):
                return
            else:
                set_fn = widget.menuText
        elif pname == "movingEnabled":
            set_fn = widget.setMovable
        elif pname == "toggleAction":
            set_fn = widget.setChecked
        elif pname == "label" and isinstance(widget, qtoolbar.QToolBar):
            return
        elif pname == "maxValue" and isinstance(widget, qspinbox.QSpinBox):
            set_fn = widget.setMaximum
        elif pname == "minValue" and isinstance(widget, qspinbox.QSpinBox):
            set_fn = widget.setMinimum
        elif pname == "lineStep" and isinstance(widget, qspinbox.QSpinBox):
            set_fn = widget.setSingleStep
        elif pname == "newLine":
            set_fn = self.origWidget.addToolBarBreak
        elif pname == "functionGetColor":
            set_fn = widget.setFunctionGetColor
        elif pname == "cursor":
            # Ignore "cursor" styles, this is for blinking cursor styles
            # not needed.
            return
        else:
            set_fn = getattr(widget, setpname, None)

        if set_fn is None:
            logger.warning("qt3ui: Missing property %s for %r", pname, widget.__class__)
            return
        if pname == "contentsMargins" or pname == "layoutSpacing":
            try:
                value = int(xmlprop.get("stdset", "0"))
                value //= 2
            except Exception:
                value = 0
            if pname == "contentsMargins":
                value = QtCore.QMargins(value, value, value, value)

        elif pname == "margin":
            try:
                value = loadVariant(xmlprop)
            except Exception:
                value = 0
            value = QtCore.QMargins(value, value, value, value)

        elif pname == "paletteBackgroundColor":
            value = "background-color:" + loadVariant(xmlprop).name()

        elif pname == "paletteForegroundColor":
            value = "color:" + loadVariant(xmlprop).name()

        elif pname in ["windowIcon", "icon"]:
            value1 = loadVariant(xmlprop, widget)
            # FIXME: Not sure if it should return anyway
            if isinstance(value1, str):
                logger.warning("Icono %s.%s no encontrado." % (widget.objectName(), value1))
                return
            else:
                value = value1

        else:
            value = loadVariant(xmlprop, widget)

        try:
            set_fn(value)
        except Exception:
            logger.exception(
                "Error processing property %s with value %s. Original XML: %s",
                pname,
                value,
                ET.tostring(xmlprop).replace(b" ", b"").replace(b"\n", b""),
            )
            # if Options.DEBUG_LEVEL > 50:
            #    print(e, repr(value))
            # if Options.DEBUG_LEVEL > 50:
            #    print(etree.ET.tostring(xmlprop))

    def process_action(self, xmlaction: ET.Element, toolBar: QtWidgets.QToolBar):
        """
        Process a QAction.
        """
        action = createWidget("QAction")
        for p in xmlaction:
            pname = p.get("name")
            if pname in self.translate_properties:
                pname = self.translate_properties[pname]

            self.process_property(p, action)
        toolBar.addAction(action)
        # origWidget.ui_[action.objectName()] = action

    def process_layout_box(self, xmllayout, widget=None, mode="box"):
        """Process layouts from UI."""
        if widget is None:
            widget = self.widget
        for c in xmllayout:
            try:
                row = int(c.get("row")) or 0
                col = int(c.get("column")) or 0
            except Exception:
                row = col = 0

            if c.tag == "property":  # Ya se han procesado previamente ...
                continue
            elif c.tag == "widget":
                new_widget = createWidget(c.get("class"), parent=widget)
                # FIXME: Should check interfaces.
                from pineboolib.qt3_widgets import qbuttongroup, qtoolbutton

                if isinstance(widget, qbuttongroup.QButtonGroup):
                    if isinstance(new_widget, qtoolbutton.QToolButton):
                        widget.addButton(new_widget)
                        continue

                loadWidget(c, new_widget, self.parent, self.origWidget)
                # path = c.find("./property[@name='name']/cstring").text
                # if not project.DGI.localDesktop():
                #    origWidget.ui_[path] = new_widget
                # if project.DGI.localDesktop():
                #    new_widget.show()
                if mode == "box":
                    try:
                        widget._layout.addWidget(new_widget)
                    except Exception:
                        logger.warning(
                            "qt3ui: No se ha podido añadir %s a %s", new_widget, widget._layout
                        )

                elif mode == "grid":
                    rowSpan = c.get("rowspan") or 1
                    colSpan = c.get("colspan") or 1
                    try:
                        widget._layout.addWidget(new_widget, row, col, int(rowSpan), int(colSpan))
                    except Exception:
                        logger.warning("qt3ui: No se ha podido añadir %s a %s", new_widget, widget)
                        logger.trace("Detalle:", stack_info=True)

            elif c.tag == "spacer":
                # sH = None
                # sV = None
                hPolicy = QtWidgets.QSizePolicy.Fixed
                vPolicy = QtWidgets.QSizePolicy.Fixed
                orient_ = None
                policy_ = QtWidgets.QSizePolicy.Expanding
                rowSpan = c.get("rowspan") or 1
                colSpan = c.get("colspan") or 1
                # policy_name = None
                spacer_name = None
                for p in c.findall("property"):
                    pname, value = loadProperty(p)
                    if pname == "sizeHint":
                        width = value.width()
                        height = value.height()
                    elif pname == "orientation":
                        orient_ = 1 if value == 1 else 2  # 1 Horizontal, 2 Vertical

                    elif pname == "sizeType":
                        # print("Convirtiendo %s a %s" % (p.find("enum").text, value))
                        if config.value("ebcomportamiento/spacerLegacy", False) or orient_ == 1:
                            policy_ = QtWidgets.QSizePolicy.Policy(value)
                        else:
                            policy_ = QtWidgets.QSizePolicy.Expanding  # Siempre Expanding

                    elif pname == "name":
                        spacer_name = value  # noqa: F841

                if orient_ == 1:
                    hPolicy = policy_
                else:
                    vPolicy = policy_

                # print("Nuevo spacer %s (%s,%s,(%s,%s), %s, %s" % (spacer_name, "Horizontal" if orient_ ==
                #                                                  1 else "Vertical", policy_name, width, height, hPolicy, vPolicy))
                new_spacer = QtWidgets.QSpacerItem(width, height, hPolicy, vPolicy)
                if mode == "grid":
                    widget._layout.addItem(new_spacer, row, col, int(rowSpan), int(colSpan))
                else:
                    widget._layout.addItem(new_spacer)
                # print("Spacer %s.%s --> %s" % (spacer_name, new_spacer, widget.objectName()))
            else:
                logger.warning("qt3ui: Unknown layout xml tag", repr(c.tag))

        widget.setLayout(widget._layout)
        # widget._layout.setContentsMargins(1, 1, 1, 1)
        # widget._layout.setSpacing(1)
        # widget._layout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)


def loadIcon(xml: "ET.Element") -> None:
    """Load Icon from XML."""
    global ICONS

    name = xml.get("name")
    xmldata = xml.find("data")
    if name is None:
        logger.warning("loadIcon: provided xml lacks attr name")
        return
    if xmldata is None:
        logger.warning("loadIcon: provided xml lacks <data>")
        return
    img_format = xmldata.get("format")
    if xmldata.text is None:
        logger.warning("loadIcon: text is empty")
        return

    data = unhexlify(xmldata.text.strip())
    pixmap = QtGui.QPixmap()
    if img_format == "XPM.GZ":
        data = zlib.decompress(data, 15)
        img_format = "XPM"
    pixmap.loadFromData(data, img_format)
    icon = QtGui.QIcon(pixmap)
    ICONS[name] = icon


def loadVariant(xml: ET.Element, widget: Optional[QWidget] = None) -> Any:
    """Load Variant from XML."""
    for variant in xml:
        return _loadVariant(variant, widget)
    raise ValueError("No property in provided XML")


def loadProperty(xml: ET.Element) -> Tuple[Any, Any]:
    """Load a Qt Property from XML."""
    for variant in xml:
        return (xml.get("name"), _loadVariant(variant))
    raise ValueError("No property in provided XML")


def u(x: Any) -> str:
    """Convert x to string."""
    if isinstance(x, str):
        return x
    return str(x)


def b(x: str) -> bool:
    """Convert x to bool."""
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
    logger.warning("Bool?:", repr(x))
    return False


def _loadVariant(variant: ET.Element, widget: Optional[QWidget] = None) -> Any:
    """Load a variant from XM. Internal."""
    text = variant.text or ""
    text = text.strip()
    if variant.tag == "cstring":
        return text
    if variant.tag in ["iconset", "pixmap"]:
        global ICONS
        return ICONS.get(text, text)
    if variant.tag == "string":
        return u(text)
    if variant.tag == "number":
        if text.find(".") >= 0:
            return float(text)
        return int(text)
    if variant.tag == "bool":
        return b(text)
    if variant.tag == "rect":
        k = {}
        for c in variant:
            k[c.tag] = int((c.text or "0").strip())
        return QtCore.QRect(k["x"], k["y"], k["width"], k["height"])

    if variant.tag == "sizepolicy":

        p = QtWidgets.QSizePolicy()
        for c in variant:
            ivalue_policy = cast(QtWidgets.QSizePolicy.Policy, int((c.text or "0").strip()))
            if c.tag == "hsizetype":
                p.setHorizontalPolicy(ivalue_policy)
            if c.tag == "vsizetype":
                p.setVerticalPolicy(ivalue_policy)
            if c.tag == "horstretch":
                p.setHorizontalStretch(ivalue_policy)
            if c.tag == "verstretch":
                p.setVerticalStretch(ivalue_policy)
        return p
    if variant.tag == "size":
        p_sz = QtCore.QSize()
        for c in variant:
            ivalue = int((c.text or "0").strip())
            if c.tag == "width":
                p_sz.setWidth(ivalue)
            if c.tag == "height":
                p_sz.setHeight(ivalue)
        return p_sz
    if variant.tag == "font":
        p_font = QtGui.QFont()
        for c in variant:
            value = (c.text or "0").strip()
            bv: bool = False
            if c.tag not in ("family", "pointsize"):
                bv = b(value)
            try:
                if c.tag == "bold":
                    p_font.setBold(bv)
                elif c.tag == "italic":
                    p_font.setItalic(bv)
                elif c.tag == "family":
                    p_font.setFamily(value)
                elif c.tag == "pointsize":
                    p_font.setPointSize(int(value))
                else:
                    logger.warning("unknown font style type %s", repr(c.tag))
            except Exception as e:
                logger.warning(e)
        return p_font

    if variant.tag == "set":
        v = None
        final = 0
        text = variant.text or "0"
        libs_1: List[Any] = [QtCore.Qt]

        if text.find("WordBreak|") > -1:
            if widget is not None and hasattr(widget, "setWordWrap"):
                widget.setWordWrap(True)
            text = text.replace("WordBreak|", "")

        for lib in libs_1:
            for t in text.split("|"):
                v = getattr(lib, t, None)
                if v is not None:
                    final = final + v

            aF = QtCore.Qt.AlignmentFlag(final)

        return aF

    if variant.tag == "enum":
        v = None
        libs_2: List[Any] = [
            QtCore.Qt,
            QtWidgets.QFrame,
            QtWidgets.QSizePolicy,
            QtWidgets.QTabWidget,
        ]
        for lib in libs_2:
            v = getattr(lib, text, None)
            if v is not None:
                return v
        if text in ["GroupBoxPanel", "LineEditPanel"]:
            return QtWidgets.QFrame.StyledPanel
        if text in ("Single", "SingleRow"):
            return QtWidgets.QAbstractItemView.SingleSelection
        if text == "FollowStyle":
            return "QtWidgets.QTableView {selection-background-color: red;}"
        if text == "MultiRow":
            return QtWidgets.QAbstractItemView.MultiSelection

        att_found = getattr(widget, text, None)
        if att_found is not None:
            return att_found

    if variant.tag == "color":
        qcolor = QtGui.QColor()
        red_ = 0
        green_ = 0
        blue_ = 0
        for color in variant:
            if color.text is None:
                continue
            if color.tag == "red":
                red_ = int(color.text.strip())
            elif color.tag == "green":
                green_ = int(color.text.strip())
            elif color.tag == "blue":
                blue_ = int(color.text.strip())

        qcolor.setRgb(red_, green_, blue_)
        return qcolor

    if variant.tag == "palette":
        p = QtGui.QPalette()
        for state in variant:
            print("FIXME: Procesando palette", state.tag)
            for color in state:
                r_ = 0
                g_ = 0
                b_ = 0
                for c in color:
                    if c.text is None:
                        continue
                    if c.tag == "red":
                        r_ = int(c.text)
                    elif c.tag == "green":
                        g_ = int(c.text)
                    elif c.tag == "blue":
                        b_ = int(c.text)

                if state.tag == "active":
                    # p.setColor(p.Active, Qt.QColor(r_, g_, b_))
                    pass
                elif state.tag == "disabled":
                    # p.setColor(p.Disabled, Qt.QColor(r_, g_, b_))
                    pass
                elif state.tag == "inactive":
                    # p.setColor(p.Inactive, Qt.QColor(r_, g_, b_))
                    pass
                elif state.tag == "normal":
                    # p.setColor(p.Normal, Qt.QColor(r_, g_, b_))
                    pass
                else:
                    logger.warning("Unknown palette state %s", state.tag)
                logger.debug("pallete color: %s %s %s", r_, g_, b_)

        return p

    if variant.tag == "date":

        y_ = 2000
        m_ = 1
        d_ = 1
        for v in variant:
            if v.text is None:
                continue
            if v.tag == "year":
                y_ = int(v.text)
            elif v.tag == "month":
                m_ = int(v.text)
            elif v.tag == "day":
                d_ = int(v.text)

        d = QtCore.QDate(y_, m_, d_)
        return d

    if Options.DEBUG_LEVEL > 50:
        logger.warning("qt3ui: Unknown variant: %s --> %s ", repr(widget), ET.tostring(variant))
