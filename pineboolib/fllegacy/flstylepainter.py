import math
from enum import Enum

from PyQt5 import QtGui  # type: ignore
from PyQt5 import QtCore  # type: ignore
from PyQt5 import QtXml  # type: ignore
from PyQt5.QtCore import Qt  # type: ignore
from pineboolib.core import decorators
from pineboolib.application import project

from typing import Dict, List, Any, Union


class FLStylePainter(object):

    Q_PI = math.pi
    deg2rad = 0.017453292519943295769

    class ErrCode(Enum):
        NoError = 0
        IdNotFound = 1

    class ElementType(Enum):
        InvalidElement = 0
        AnchorElement = 1
        CircleElement = 2
        ClipElement = 3
        CommentElement = 4
        DescElement = 5
        EllipseElement = 6
        GroupElement = 7
        ImageElement = 8
        LineElement = 9
        PolylineElement = 10
        PolygonElement = 11
        PathElement = 12
        RectElement = 13
        SvgElement = 14
        TextElement = 15
        TitleElement = 16
        TSpanElement = 17
        SectionElement = 18
        SetStyleElement = 19

    class FLStylePainterPrivate(object):

        svgMode_ = False

        @decorators.BetaImplementation
        def __init__(self):
            self.painter_ = QtGui.QPainter()
            self.styleName_ = ""

            self.lastLabelRect_ = QtCore.QRect()
            self.text_ = ""
            self.tf_ = None
            self.pix_ = QtGui.QPixmap()
            self.sx_ = 0
            self.sy_ = 0
            self.sw_ = -1
            self.sh_ = -1
            self.saves_ = 0
            self.transStack_ = QtCore.QStringListModel().stringList()

            self.doc_ = QtXml.QDomDocument()
            self.objNodesMap_: Dict[str, Any] = {}  # QMAP FIXME

            self.stack_: List[Dict[str, Any]] = []
            self.curr_ = {"textx": None, "texty": None, "textalign": None}
            self.svgTypeMap_: Dict[str, int] = {}  # QMAP FIXME
            self.svgColMap_: Dict[Union[int, str], Union[int, str]] = {}  # QMAP FIXME
            self.clipPathTable_: Dict[str, QtCore.QRegion] = {}  # QMAP FIXME

            self.relDpi_ = 0.0

        @decorators.BetaImplementation
        def setObjNodesMap(self, elem):
            n = QtXml.QDomNode(elem.firstChild())
            while not n.isNull():
                e = QtXml.QDomElement(n.toElement())
                self.setObjNodesMap(e)
                if e.attribute("id").startswith("_##"):
                    self.objNodesMap_.insert(e.attribute("id"), e)
                n = n.nextSibling()

        @decorators.BetaImplementation
        def paramsTransform(self, tr):
            t = tr.simplifyWhiteSpace()
            reg = QtCore.QRegExp("\\s*([\\w]+)\\s*\\(([^\\(]*)\\)")
            res = QtCore.QStringListModel().stringList()
            index = 0
            index = reg.search(t, index)
            while index >= 0:
                command = reg.cap(1)
                params = reg.cap(2)
                plist = QtCore.QStringList.split(QtCore.QRegExp("[,\\s]"), params)
                res += command
                res += plist
                index += reg.matchedLength()
                index = reg.search(t, index)
            return res

        @decorators.BetaImplementation
        def normalizeTranslates(self, node, isRoot):
            nl = node.childNodes()
            for i in range(nl.count()):
                itNod = nl.item(i)
                if not itNod.attribute.contains("id"):
                    e = itNod.toElement()
                    e.setAttribute(
                        "id", node.attribute().namedItem("id").nodeValue() + "-" + str(i)
                    )
                self.normalizeTranslates(itNod, False)

            elem = node.toElement()
            if not isRoot and elem.hasAttribute("transform"):
                dadNode = QtXml.QDomElement(elem.parentNode().toElement())
                if dadNode.tagName() != "g":
                    return

                if not dadNode.hasAttribute("transform"):
                    dadNode.setAttribute("transform", elem.attribute("transform"))
                    dadNode.setAttribute("aqnorm", "true")
                    elem.removeAttribute("transform")
                elif dadNode.attribute("aqnorm") == "true":
                    dadTrans = dadNode.attribute("transform")
                    if dadTrans != elem.attribute("transform"):
                        tx1 = 0.0
                        tx2 = 0.0
                        ty1 = 0.0
                        ty2 = 0.0

                        params = self.paramsTransform(dadNode.attribute("transform"))
                        if params[0] == "translate":
                            tx1 = float(params[1])
                            ty1 = float(params[2])

                        params = self.paramsTransform(elem.attribute("transform"))
                        if params[0] == "translate":
                            tx2 = float(params[1])
                            ty2 = float(params[2])
                            s = "translate({},{})".format(tx2 - tx1, ty2 - ty1)
                            elem.setAttribute("transform", s)
                        elif params[0] == "matrix":
                            m: List[float] = []
                            for i in range(6):
                                m[i] = float(params[i + 1])
                            s = "matrix({},{},{},{},{},{})"
                            s.format(m[0], m[1], m[2], m[3], m[4] - tx1, m[5] - ty1)
                            elem.setAttribute("transform", s)
                    else:
                        elem.removeAttribute("transform")

            elem.removeAttribute("aqnorm")

        @decorators.BetaImplementation
        def parseDomDoc(self):
            st = self.styleName_
            if st and st != "" and st != "_mark" and st != "_simple":
                errMsg = ""
                errLine = None
                errColumn = None

                if self.styleName_.lower().startswith("abanq:"):
                    content = project.conn.managerModules().contentCached(self.styleName_[6:])
                    if not self.doc_.setContent(content, errMsg, errLine, errColumn):
                        return
                elif self.styleName_.lower().startswith("file:"):
                    file = QtCore.QFile(self.styleName_[5:])
                    if not file.open(Qt.IO_ReadOnly):
                        return
                    if not self.doc_.setContent(file, errMsg, errLine, errColumn):
                        return

                self.setObjNodesMap(self.doc_.documentElement())

                if len(self.svgTypeMap_.keys()) == 0:
                    etab = {
                        "a": FLStylePainter.ElementType.AnchorElement,
                        "#comment": FLStylePainter.ElementType.CommentElement,
                        "circle": FLStylePainter.ElementType.CircleElement,
                        "clipPath": FLStylePainter.ElementType.ClipElement,
                        "desc": FLStylePainter.ElementType.DescElement,
                        "ellipse": FLStylePainter.ElementType.EllipseElement,
                        "g": FLStylePainter.ElementType.GroupElement,
                        "image": FLStylePainter.ElementType.ImageElement,
                        "line": FLStylePainter.ElementType.LineElement,
                        "polyline": FLStylePainter.ElementType.PolylineElement,
                        "polygon": FLStylePainter.ElementType.PolygonElement,
                        "path": FLStylePainter.ElementType.PathElement,
                        "rect": FLStylePainter.ElementType.RectElement,
                        "svg": FLStylePainter.ElementType.SvgElement,
                        "text": FLStylePainter.ElementType.TextElement,
                        "tspan": FLStylePainter.ElementType.TSpanElement,
                        "title": FLStylePainter.ElementType.TitleElement,
                        0: FLStylePainter.ElementType.InvalidElement,
                    }

                    for k, v in etab.items():
                        self.svgTypeMap_[k] = v

                st = {"textx": 0, "texty": 0, "textalign": Qt.AlignLeft}
                self.stack_.append(st)
                self.curr_ = self.stack_[-1]

        @decorators.BetaImplementation
        def saveAttributes(self):
            self.painter_.save()
            st = self.curr_
            self.stack_.append(st)
            self.curr_ = self.stack_.last()

        @decorators.BetaImplementation
        def restoreAttributes(self):
            self.painter_.restore()
            self.stack_.remove(self.stack_.fromLast())
            self.curr_ = self.stack_.last()

        @decorators.BetaImplementation
        def parseColor(self, col):
            if len(self.svgColMap_.keys()) == 0:
                coltab = {
                    "black": "#000000",
                    "silver": "#c0c0c0",
                    "gray": "#808080",
                    "white": "#ffffff",
                    "maroon": "#800000",
                    "red": "#ff0000",
                    "purple": "#800080",
                    "fuchsia": "#ff00ff",
                    "green": "#008000",
                    "lime": "#00ff00",
                    "olive": "#808000",
                    "yellow": "#ffff00",
                    "navy": "#000080",
                    "blue": "#0000ff",
                    "teal": "#008080",
                    "aqua": "#00ffff",
                    0: 0,  # WHY 0 (zero) as an integer??
                }

                for k, v in coltab.items():
                    self.svgColMap_.insert(k, v)

            if self.svgColMap_.contains(col):
                return QtGui.QColor(self.svgColMap_[col])

            c = col
            c.replace(QtCore.QRegExp("\\s*"), "")
            reg = QtCore.QRegExp("^rgb\\((\\d+)(%?),(\\d+)(%?),(\\d+)(%?)\\)$")
            if reg.search(c) >= 0:
                comp: List[int] = []
                for i in range(3):
                    comp[i] = int(reg.cap(2 * i + 1))
                    cap2 = reg.cap(2 * i + 1)
                    if cap2 and cap2 != "":
                        comp[i] = int(float(255 * comp[i]) / 100.0)
                return QtGui.QColor(comp[0], comp[1], comp[2])
            return QtGui.QColor(col)

        @decorators.BetaImplementation
        def setStyleProperty(self, prop, val, pen, font, talign):
            if prop == "stroke":
                if val == "none":
                    pen.setStyle(Qt.NoPen)
                else:
                    pen.setColor(self.parseColor(val))
                    if pen.style() == Qt.NoPen:
                        pen.setStyle(Qt.SolidLine)
                    if pen.width() == 0:
                        pen.setWidth(1)
            elif prop == "stroke-width":
                w = self.parseLen(val)
                if w > 0.0001:
                    pen.setWidth(int(w))
                else:
                    pen.setStyle(Qt.NoPen)
            elif prop == "stroke-linecap":
                if val == "butt":
                    pen.setCapStyle(Qt.FlatCap)
                elif val == "round":
                    pen.setCapStyle(Qt.RoundCap)
                elif val == "square":
                    pen.setCapStyle(Qt.SquareCap)
            elif prop == "stroke-linejoin":
                if val == "mitel":
                    pen.setJoinStyle(Qt.MiterJoin)
                elif val == "round":
                    pen.setJoinStyle(Qt.RoundJoin)
                elif val == "bevel":
                    pen.setJoinStyle(Qt.BevelJoin)
            elif prop == "stroke-dasharray":
                if val == "18,6":
                    pen.setStyle(Qt.DashLine)
                elif val == "3":
                    pen.setStyle(Qt.DotLine)
                elif val == "9,6,3,6" or val == "4,2,1,2":
                    pen.setStyle(Qt.DashDotLine)
                elif val == "8,2,1,2" or val == "2,1,0.5,1":
                    pen.setStyle(Qt.DashDotLine)
                elif val == "9,3,3":
                    pen.setStyle(Qt.DashDotDotLine)
                elif val == "none":
                    pen.setStyle(Qt.DotLine)
            elif prop == "fill":
                if val == "none":
                    self.painter_.setBrush(Qt.NoBrush)
                else:
                    self.painter_.setBrush(self.parseColor(val))
            elif prop == "font-size":
                font.setPointSizeFloat(float(self.parseLen(val)))
            elif prop == "font-family":
                font.setFamily(val)
            elif prop == "font-style":
                if val == "normal":
                    font.setItalic(False)
                elif val == "italic":
                    font.setItalic(True)
                else:
                    QtCore.qWarning(
                        "FLStylePainterPrivate.setStyleProperty: unhandled " "font-style: {}", val
                    )
            elif prop == "font-weight":
                w = font.weight()
                if val == "100" or val == "200":
                    w = QtGui.QFont.Light
                elif val == "300" or val == "400" or val == "normal":
                    w = QtGui.QFont.Normal
                elif val == "500" or val == "600":
                    w = QtGui.QFont.DemiBold
                elif val == "700" or val == "bold" or val == "800":
                    w = QtGui.QFont.Bold
                elif val == "900":
                    w = QtGui.QFont.Black
                font.setWeight(w)
            elif prop == "text-anchor":
                # if val == "middle":
                #     talign = Qt.AlignHCenter
                # elif val == "end":
                #     talign = Qt.AlignRight
                # else:
                #     talign = Qt.AlignLeft
                pass
            elif prop == "clip-path":
                if val.startswith("url(#"):
                    clipName = val[5:6]
                    if clipName and clipName != "":
                        clipRegion = self.clipPathTable_[clipName]
                        if not clipRegion.isEmpty():
                            cp = QtGui.QPainter.CoordPainter
                            self.painter_.setClipRegion(self.painter_.clipRegion() & clipRegion, cp)
            # return talign #FIXME?

        @decorators.BetaImplementation
        def parseLen(self, string, ok=False, horiz=True):
            strreg = "([+-]?\\d*\\.*\\d*[Ee]?[+-]?\\d*)"
            strreg += "(em|ex|px|%|pt|pc|cm|mm|in|)$"
            reg = QtCore.QRegExp(strreg)
            if reg.search(string) == -1:
                QtCore.qWarning("FLStylePainterPrivate::parseLen: couldn't parse " + string)
                if ok:
                    ok = False
                return 0.0

            dbl = float(reg.cap(1))
            u = reg.cap(2)
            if u and u != "" and u != "px":
                m = self.painter_.device()
                if u == "em":
                    fi = QtGui.QFontInfo(self.painter_.font())
                    dbl *= fi.pixelSize()
                elif u == "ex":
                    fi = QtGui.QFontInfo(self.painter_.font())
                    dbl *= 0.5 * fi.pixelSize()
                elif u == "%":
                    fact = self.painter_.window().height()
                    if horiz:
                        fact = self.painter_.window().width()
                    dbl *= fact
                elif u == "cm":
                    dbl *= m.logicalDpiX() / 2.54
                elif u == "mm":
                    dbl *= m.logicalDpiX() / 25.4
                elif u == "in":
                    dbl *= m.logicalDpiX()
                elif u == "pt":
                    dbl *= m.logicalDpiX() * 72.0
                elif u == "pc":
                    dbl *= m.logicalDpiX() * 6.0
                else:
                    Qt.qWarning("FLStylePainterPrivate::parseLen: Unknown unit " + u)

            if ok:
                ok = True
            return dbl

        @decorators.BetaImplementation
        def lenToInt(self, aqmap, attr, aqdef=0):
            if aqmap.contains(attr):
                ok = None
                dbl = self.parseLen(aqmap.namedItem(attr).nodeValue(), ok)
                # if ok: #FIXME
                if dbl and dbl > 0:
                    return QtCore.qRound(dbl)
            return aqdef

        @decorators.BetaImplementation
        def lenToDouble(self, aqmap, attr, aqdef=0):
            if aqmap.contains(attr):
                ok = None
                dbl = self.parseLen(aqmap.namedItem(attr).nodeValue(), ok)
                # if ok: #FIXME
                if dbl and dbl > 0:
                    return dbl
            return aqdef

        @decorators.BetaImplementation
        def setStyle(self, s):
            rules = QtCore.QStringList.split(";", s)
            pen = self.painter_.pen()
            font = self.painter_.font()

            for it in rules:
                col = it.find(":")
                if col > 0:
                    prop = it[col:].simplifyWhiteSpace()
                    val = it[-(it.length() - col - 1) :]
                    val = val.lower().stripWhiteSpace()
                    self.setStyleProperty(prop, val, pen, font, self.curr_["textalign"])

            self.painter_.setPen(pen)
            self.painter_.setFont(font)

        @decorators.BetaImplementation
        def setTransform(self, tr):
            t = tr.simplifyWhiteSpace()
            reg = QtCore.QRegExp("\\s*([\\w]+)\\s*\\(([^\\(]*)\\)")
            index = 0
            index = reg.search(t, index)
            while index >= 0:
                command = reg.cap(1)
                params = reg.cap(2)
                plist = QtCore.QStringList.split(QtCore.QRegExp("[,\\s]"), params)

                if command == "translate":
                    tx = float(plist[0])
                    ty = 0.0
                    if plist.count() >= 2:
                        ty = float(plist[1])
                    self.painter_.translate(tx, ty)
                elif command == "rotate":
                    self.painter_.rotate(float(plist[0]))
                elif command == "scale":
                    sx = sy = float(plist[0])
                    if plist.count() >= 2:
                        sy = float(plist[1])
                    self.painter_.scale(sx, sy)
                elif command == "matrix" and plist.count() >= 6:
                    m: List[float] = []
                    for i in range(6):
                        m[i] = float(plist[i])
                    wm = QtCore.QWMatrix(m[0], m[1], m[2], m[3], m[4], m[5])
                    self.painter_.setWorldMatrix(wm, True)
                elif command == "skewX":
                    self.painter_.shear(0.0, math.tan(float(plist[0]) * self.deg2rad))
                elif command == "skewY":
                    self.painter_.shear(math.tan(float(plist[0]) * self.deg2rad), 0.0)

                index += reg.matchedLength()
                index = reg.search(t, index)

        @decorators.BetaImplementation
        def applyTransforms(self):
            for it in self.transStack_:
                if it != "void":
                    self.setTransform(it.section(":", 1, 1))

        @decorators.BetaImplementation
        def play(self, node, elm):
            if isinstance(node, str):
                objName = node
                if objName in self.objNodesMap_:
                    node = self.objNodesMap_[objName]
                if node.isNull():
                    self.errCode_ = FLStylePainter.ErrCode.IdNotFound
                    QtCore.qWarning("FLStylePainter.play: Object id " + objName + " not found.")
                    return False
                return self.play(node, elm)

            le = FLStylePainter.ElementType.LineElement
            se = FLStylePainter.ElementType.SectionElement
            sse = FLStylePainter.ElementType.SetStyleElement
            svge = FLStylePainter.ElementType.SvgElement
            ple = FLStylePainter.ElementType.PolylineElement
            plyge = FLStylePainter.ElementType.PolygonElement
            ge = FLStylePainter.ElementType.GroupElement
            ae = FLStylePainter.ElementType.AnchorElement
            ce = FLStylePainter.ElementType.CommentElement
            re = FLStylePainter.ElementType.RectElement
            cire = FLStylePainter.ElementType.CircleElement
            elle = FLStylePainter.ElementType.EllipseElement
            pe = FLStylePainter.ElementType.PathElement
            tse = FLStylePainter.ElementType.TSpanElement
            te = FLStylePainter.ElementType.TextElement
            ie = FLStylePainter.ElementType.ImageElement
            de = FLStylePainter.ElementType.DescElement
            tite = FLStylePainter.ElementType.TitleElement
            clie = FLStylePainter.ElementType.ClipElement
            inve = FLStylePainter.ElementType.InvalidElement

            pre = node.previousSibling().toElement()
            if not pre.isNull() and not pre.attribute("id").startswith("_##"):
                self.play(pre, se)

            if elm != sse:
                self.saveAttributes()

            t = self.svgTypeMap_[node.nodeName()]

            if t == le and self.painter_.pen().style() == Qt.NoPen:
                p = self.painter_.pen()
                p.setStyle(Qt.SolidLine)
                self.painter_.setPen(p)

            attr = node.attributes()
            if attr.contains("style"):
                self.setStyle(attr.namedItem("style").nodeValue())

            if elm != sse and t != svge:
                self.applyTransforms()
                if attr.contains("transform"):
                    self.setTransform(attr.namedItem("transform").nodeValue())

            i = attr.length()
            if i > 0:
                pen = self.painter_.pen()
                font = self.painter_.font()
                i -= 1
                while i > 0:
                    n = attr.item(i)
                    a = n.nodeName()
                    val = n.nodeValue().lower().stripWhiteSpace()
                    self.setStyleProperty(a, val, pen, font, self.curr_["textalign"])
                    i -= 1

                self.painter_.setPen(pen)
                self.painter_.setFont(font)

            if elm == sse:
                return

            idObj = attr.namedItem("id").nodeValue()
            isSectionDraw = False
            if elm == se:
                isSectionDraw = not idObj.startswith("_##")

            if t == ce:
                pass
            elif t == re:
                if elm == re or isSectionDraw:
                    rx = ry = 0
                    x1 = self.lenToInt(attr, "x")
                    y1 = self.lenToInt(attr, "y")
                    w = self.lenToInt(attr, "width")
                    h = self.lenToInt(attr, "height")
                    if w != 0 and h != 0:
                        x2 = int(attr.contains("rx"))
                        y2 = int(attr.contains("ry"))

                        if x2:
                            rx = self.lenToInt(attr, "rx")
                        if y2:
                            ry = self.lenToInt(attr, "ry")
                        if x2 and not y2:
                            ry = rx
                        elif not x2 and y2:
                            rx = ry
                        rx = int(200.0 * float(rx) / float(w))
                        ry = int(200.0 * float(ry) / float(h))
                        if rx == 0 and ry == 0:
                            QtCore.QwtPainter.drawRect(self.painter_, x1, y1, w, h)
                        else:
                            self.painter_.drawRoundRect(x1, y1, w, h, rx, ry)
                        if not isSectionDraw:
                            self.lastLabelRect_ = self.painter_.xForm(QtCore.QRect(x1, y1, w, h))
            elif t == cire:
                cx1 = self.lenToDouble(attr, "cx") + 0.5
                cy1 = self.lenToDouble(attr, "cy") + 0.5
                crx = self.lenToDouble(attr, "r")
                QtCore.QwtPainter.drawEllipse(
                    self.painter_,
                    QtCore.QRect(int(cx1 - crx), int(cy1 - crx), int(2 * crx), int(2 * crx)),
                )
            elif t == elle:
                cx1 = self.lenToDouble(attr, "cx") + 0.5
                cy1 = self.lenToDouble(attr, "cy") + 0.5
                crx = self.lenToDouble(attr, "rx")
                cry = self.lenToDouble(attr, "ry")
                QtCore.QwtPainter.drawEllipse(
                    self.painter_,
                    QtCore.QRect(int(cx1 - crx), int(cy1 - cry), int(2 * crx), int(2 * cry)),
                )
            elif t == le:
                if elm == le or isSectionDraw:
                    x1 = self.lenToInt(attr, "x1")
                    x2 = self.lenToInt(attr, "x2")
                    y1 = self.lenToInt(attr, "y1")
                    y2 = self.lenToInt(attr, "y2")
                    p = self.painter_.pen()
                    w = p.width()
                    p.setWidth(
                        int(
                            w
                            * (
                                math.fabs(self.painter_.worldMatrix().m11())
                                + math.fabs(self.painter_.worldMatrix().m22())
                            )
                            / 2
                        )
                    )
                    self.painter_.setPen(p)
                    QtCore.QwtPainter.drawLine(self.painter_, x1, y1, x2, y2)
                    p.setWidth(w)
                    self.painter_.setPen(p)
            elif t == ple or t == plyge:
                pts = attr.namedItem("points").nodeValue()
                pts = pts.simplifyWhiteSpace()
                sl = QtCore.QStringList.split(QtCore.QRegExp("[ ,]"), pts)
                ptarr = QtCore.QPointArray(int(sl.count() / 2))
                for i in range(int(sl.count() / 2)):
                    dx = float(sl[2 * i])
                    dy = float(sl[2 * i + 1])
                    ptarr.setPoint(i, int(dx), int(dy))
                if t == ple:
                    if self.painter_.brush().style() != Qt.NoBrush:
                        pn = self.painter_.pen()
                        self.painter_.setPen(Qt.NoPen)
                        self.painter_.drawPolygon(ptarr)
                        self.painter_.setPen(pn)
                    QtCore.QwtPainter.drawPolyline(self.painter_, ptarr)
                else:
                    QtCore.QwtPainter.drawPolygon(self.painter_, ptarr)
            elif t == svge or t == ge or t == ae:
                backStack = QtCore.QStringListModel().stringList()
                if t != svge:
                    backStack = self.transStack_
                    self.transStack_.clear()
                child = node.firstChild()
                while not child.isNull():
                    self.play(child, elm)
                    child = child.nextSibling()
                if t != svge:
                    self.transStack_ = backStack
            elif t == pe:
                self.drawPath(attr.namedItem("d").nodeValue())
            elif t == tse or t == te:
                if elm == te or isSectionDraw:
                    if self.relDpi_ != 1.0:
                        fnt = self.painter_.font()
                        fnt.setPointSizeFloat(fnt.pointSizeFloat() * self.relDpi_)
                        self.painter_.setFont(fnt)
                    null = self.lastLabelRect_.isNull()
                    wb = (self.tf_ & QtGui.QPainter.WordBreak) != 0
                    if not isSectionDraw and not null and wb:
                        pn = self.painter_.pen()
                        pcolor = pn.color()
                        bcolor = self.painter_.brush().color()
                        pn.setColor(bcolor)
                        self.painter_.setPen(pn)
                        QtCore.QwtPainter.drawText(
                            self.painter_,
                            self.painter_.xFormDev(self.lastLabelRect_),
                            self.curr_["textalign"] | self.tf_,
                            self.text_,
                        )
                        pn.setColor(pcolor)
                        self.painter_.setPen(pn)
                        self.lastLabelRect_.setSize(QtCore.QSize(0, 0))
                    else:
                        if attr.contains("x"):
                            self.curr_["textx"] = self.lenToInt(attr, "x")
                        if attr.contains("y"):
                            self.curr_["texty"] = self.lenToInt(attr, "y")
                        if t == tse:
                            self.curr_["textx"] += self.lenToInt(attr, "dx")
                            self.curr_["texty"] += self.lenToInt(attr, "dy")

                        pn = self.painter_.pen()
                        pcolor = pn.color()
                        bcolor = self.painter_.brush().color()
                        c = node.firstChild()
                        while not c.isNull():
                            tgnspan = c.toElement().tagName() == "tspan"
                            if c.isText():
                                pn.setColor(bcolor)
                                self.painter_.setPen(pn)
                                text = self.text_
                                if isSectionDraw:
                                    text = c.toText().nodeValue()
                                w = self.painter_.fontMetrics().width(text)
                                if self.curr_["textalign"] == Qt.AlignHCenter:
                                    self.curr_["textx"] -= w / 2
                                elif self.curr_["textalign"] == Qt.AlignRight:
                                    self.curr_["textx"] -= w
                                QtCore.QwtPainter.drawText(
                                    self.painter_, self.curr_["textx"], self.curr_["texty"], text
                                )
                                pn.setColor(pcolor)
                                self.painter_.setPen(pn)
                                self.curr_["textx"] += w
                            elif c.isElement() and tgnspan:
                                self.play(c, elm)
                            c = c.nextSibling()
                        if t == tse:
                            it = self.stack_[-1]
                            it["textx"] = self.curr_["textx"]
                            it["texty"] = self.curr_["texty"]
            elif t == ie:
                if elm == ie or isSectionDraw:
                    x1 = self.lenToInt(attr, "x")
                    y1 = self.lenToInt(attr, "y")
                    if isSectionDraw:
                        w = self.lenToInt(attr, "width")
                        h = self.lenToInt(attr, "height")
                        href = attr.namedItem("xlink:href").nodeValue()
                        if href and href != "":
                            pix = QtGui.QPixmap()
                            if not pix.load(href):
                                QtCore.qWarning(
                                    "FLStylePainterPrivate::play:" " Couldn't load image " + href
                                )
                            else:
                                self.painter_.drawPixmap(QtCore.QRect(x1, y1, w, h), pix)
                    else:
                        self.painter_.drawPixmap(
                            x1, y1, self.pix_, self.sx_, self.sy_, self.sw_, self.sh_
                        )
            elif t == de or t == tite:
                pass
            elif t == clie:
                child = node.firstChild()
                region = QtCore.QRegion()

                while not child.isNull():
                    childAttr = child.attributes()
                    if child.nodeName() == "rect":
                        r = QtCore.QRect()
                        r.setX(self.lenToInt(childAttr, "x"))
                        r.setY(self.lenToInt(childAttr, "y"))
                        r.setWidth(self.lenToInt(childAttr, "width"))
                        r.setHeight(self.lenToInt(childAttr, "height"))
                        region |= r
                    elif child.nodeName() == "ellipse":
                        r = QtCore.QRect()
                        x = self.lenToInt(childAttr, "cx")
                        y = self.lenToInt(childAttr, "cy")
                        width = self.lenToInt(childAttr, "rx")
                        height = self.lenToInt(childAttr, "ry")
                        r.setX(x - width)
                        r.setY(y - height)
                        r.setWidth(width * 2)
                        r.setHeight(height * 2)
                        rgn = QtCore.QRegion(r, QtCore.QRegion.Ellipse)
                        region |= rgn
                    child = child.nextSibling()
                if idObj and idObj != "":
                    self.clipPathTable_[idObj] = region
            elif t == inve:
                QtCore.qWarning(
                    "FLStylePainterPrivate::play:" " unknown element type " + node.nodeName()
                )

            self.restoreAttributes()
            return True

        @decorators.BetaImplementation
        def pathArcSegment(self, path, pcount, xc, yc, th0, th1, rx, ry, xar):
            # xar = xAxisRotation
            sinTh = math.sin(xar * (self.Q_PI / 180.0))
            cosTh = math.cos(xar * (self.Q_PI / 180.0))

            a00 = cosTh * rx
            a01 = -sinTh * ry
            a10 = sinTh * rx
            a11 = cosTh * ry

            thHalf = 0.5 * (th1 - th0)
            t = (8.0 / 3.0) * math.sin(thHalf * 0.5) * math.sin(thHalf * 0.5) / math.sin(thHalf)
            x1 = xc + math.cos(th0) - t * math.sin(th0)
            y1 = yc + math.sin(th0) + t * math.cos(th0)
            x3 = xc + math.cos(th1)
            y3 = yc + math.sin(th1)
            x2 = x3 + t * math.sin(th1)
            y2 = y3 - t * math.cos(th1)

            ptarr = QtCore.QPointArray(4)
            ptarr.setPoint(0, path.point(pcount - 1))
            ptarr.setPoint(1, a00 * x1 + a01 * y1, a10 * x1 + a11 * y1)
            ptarr.setPoint(2, a00 * x2 + a01 * y2, a10 * x2 + a11 * y2)
            ptarr.setPoint(3, a00 * x3 + a01 * y3, a10 * x3 + a11 * y3)

            bezier = ptarr.cubicBezier()
            if bezier.size() > path.size() - pcount:
                path.resize(path.size() - pcount + bezier.size())
            for k in range(bezier.size()):
                path.setPoint(pcount, bezier[k])
                pcount += 1
            return pcount

        @decorators.BetaImplementation
        def pathArc(
            self,
            path,
            pcount,
            rx,
            ry,
            x_axis_rotation,
            large_arc_flag,
            sweep_flag,
            x,
            y,
            curx,
            cury,
        ):
            rx = math.fabs(rx)
            ry = math.fabs(ry)

            sin_th = math.sin(x_axis_rotation * (self.Q_PI / 180.0))
            cos_th = math.cos(x_axis_rotation * (self.Q_PI / 180.0))

            dx = (curx - x) / 2.0
            dy = (cury - y) / 2.0
            dx1 = cos_th * dx + sin_th * dy
            dy1 = -sin_th * dx + cos_th * dy
            Pr1 = rx * rx
            Pr2 = ry * ry
            Px = dx1 * dx1
            Py = dy1 * dy1

            check = Px / Pr1 + Py / Pr2
            if check > 1:
                rx = rx * math.sqrt(check)
                ry = ry * math.sqrt(check)

            a00 = cos_th / rx
            a01 = sin_th / rx
            a10 = -sin_th / ry
            a11 = cos_th / ry
            x0 = a00 * curx + a01 * cury
            y0 = a10 * curx + a11 * cury
            x1 = a00 * x + a01 * y
            y1 = a10 * x + a11 * y

            d = (x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0)
            sfactor_sq = 1.0 / d - 0.25
            if sfactor_sq < 0:
                sfactor_sq = 0
            sfactor = math.sqrt(sfactor_sq)
            if sweep_flag == large_arc_flag:
                sfactor = -sfactor
            xc = 0.5 * (x0 + x1) - sfactor * (y1 - y0)
            yc = 0.5 * (y0 + y1) + sfactor * (x1 - x0)

            th0 = math.atan2(y0 - yc, x0 - xc)
            th1 = math.atan2(y1 - yc, x1 - xc)

            th_arc = th1 - th0
            if th_arc < 0 and sweep_flag:
                th_arc += 2 * self.Q_PI
            elif th_arc > 0 and not sweep_flag:
                th_arc -= 2 * self.Q_PI

            n_segs = int(math.ceil(math.fabs(th_arc / (self.Q_PI * 0.5 + 0.001))))

            for i in range(n_segs):
                pcount = self.pathArcSegment(
                    path,
                    pcount,
                    xc,
                    yc,
                    th0 + i * th_arc / n_segs,
                    th0 + (i + 1) * th_arc / n_segs,
                    rx,
                    ry,
                    x_axis_rotation,
                )

            return pcount

        @decorators.BetaImplementation
        def drawPath(self, data):
            x0 = 0
            y0 = 0
            x = 0
            y = 0
            controlX = 0
            controlY = 0
            path = QtCore.QPointArray(500)
            subIndex = QtCore.QValueList()
            quad = QtCore.QPointArray(4)
            pcount = 0
            idx = 0
            mode = 0
            lastMode = 0
            relative = False
            commands = "MZLHVCSQTA"
            cmdArgs = [2, 0, 2, 1, 1, 6, 4, 4, 2, 7]
            reg = QtCore.QRegExp("\\s*,?\\s*([+-]?\\d*\\.?\\d*)")

            subIndex.append(0)

            while idx < data.length():
                ch = data[int(idx)]
                idx += 1
                if ch.isSpace():
                    continue
                chUp = ch.upper()
                cmd = commands.find(chUp)
                if cmd >= 0:
                    mode = cmd
                    relative = ch != chUp
                else:
                    if mode and not ch.isLetter():
                        cmd = mode
                        idx -= 1
                    else:
                        QtCore.qWarning("FLStylePainterPrivate::drawPath: Unknown command")
                        return

                arg: List[float] = []
                numArgs = cmdArgs[cmd]
                for i in range(numArgs):
                    pos = reg.search(data, idx)
                    if pos == -1:
                        QtCore.qWarning(
                            "FLStylePainterPrivate::drawPath:" " Error parsing arguments"
                        )
                        return
                    arg[i] = float(reg.cap(1))
                    idx = pos + reg.matchedLength()

                offsetX = x if relative else 0
                offsetY = y if relative else 0

                if mode == 0:
                    if x != x0 or y != y0:
                        path.setPoint(pcount, int(x0), int(y0))
                        pcount += 1
                    x = x0 = int(arg[0] + offsetX)
                    y = y0 = int(arg[1] + offsetY)
                    subIndex.append(pcount)
                    path.setPoint(pcount, int(x0), int(y0))
                    pcount += 1
                    mode = 2
                elif mode == 1:
                    path.setPoint(pcount, int(x0), int(y0))
                    pcount += 1
                    x = x0
                    y = y0
                    mode = 0
                elif mode == 2:
                    x = int(arg[0] + offsetX)
                    y = int(arg[1] + offsetY)
                    path.setPoint(pcount, int(x), int(y))
                    pcount += 1
                elif mode == 3:
                    x = int(arg[0] + offsetX)
                    path.setPoint(pcount, int(x), int(y))
                    pcount += 1
                elif mode == 4:
                    y = int(arg[0] + offsetY)
                    path.setPoint(pcount, int(x), int(y))
                    pcount += 1
                elif mode == 5 or mode == 6 or mode == 7 or mode == 8:
                    quad.setPoint(0, int(x), int(y))
                    if mode == 6 or mode == 8:
                        mlm = mode == lastMode
                        m56 = mode == 6 and lastMode == 5
                        m78 = mode == 8 and lastMode == 7
                        cont = mlm or m56 or m78
                        x = 2 * x - controlX if cont else x
                        y = 2 * y - controlY if cont else y
                        quad.setPoint(1, int(x), int(y))
                        quad.setPoint(2, int(x), int(y))
                    for j in range(numArgs // 2):
                        x = int(arg[2 * j] + offsetX)
                        y = int(arg[2 * j + 1] + offsetY)
                        quad.setPoint(j + 4 - numArgs / 2, int(x), int(y))

                    controlX = quad[2].x()
                    controlY = quad[2].y()

                    if mode == 7 or mode == 8:
                        x31 = quad[0].x() + int(2.0 * (quad[2].x() - quad[0].x()) / 3.0)
                        y31 = quad[0].y() + int(2.0 * (quad[2].y() - quad[0].y()) / 3.0)
                        x32 = quad[2].x() + int(2.0 * (quad[3].x() - quad[2].x()) / 3.0)
                        y32 = quad[2].y() + int(2.0 * (quad[3].y() - quad[2].y()) / 3.0)
                        quad.setPoint(1, x31, y31)
                        quad.setPoint(2, x32, y32)

                    bezier = quad.cubicBezier()
                    if bezier.size() > path.size() - pcount:
                        path.resize(path.size() - pcount + bezier.size())
                    for k in range(bezier.size()):
                        path.setPoint(pcount, bezier[k])
                        pcount += 1
                elif mode == 9:
                    rx = arg[0]
                    ry = arg[1]
                    xAxisRotation = arg[2]
                    largeArcFlag = arg[3]
                    sweepFlag = arg[4]
                    ex = arg[5] + offsetX
                    ey = arg[6] + offsetY
                    curx = x
                    cury = y
                    pcount = self.pathArc(
                        path,
                        pcount,
                        rx,
                        ry,
                        xAxisRotation,
                        int(largeArcFlag),
                        int(sweepFlag),
                        ex,
                        ey,
                        curx,
                        cury,
                    )
                    pcount += 1
                    x = int(ex)
                    y = int(ey)

                lastMode = mode
                if pcount >= path.size() - 4:
                    path.resize(2 * path.size())

            subIndex.append(pcount)
            if self.painter_.brush().style() != Qt.NoBrush:
                if x != x0 or y != y0:
                    path.setPoint(pcount, int(x0), int(y0))
                    pcount += 1
                pen = self.painter_.pen()
                self.painter_.setPen(Qt.NoPen)
                poly = QtCore.QwtPolygon(pcount)
                for i in range(pcount):
                    poly.setPoint(i, path.point(i))
                QtCore.QwtPainter.drawPolygon(self.painter_, poly)
                self.painter_.setPen(pen)

            start = 0
            j = 0
            for it in subIndex:
                inext = j + 1
                polcount = inext - start
                poly = QtCore.QwtPolygon(polcount)
                for i in range(polcount):
                    poly.setPoint(i, path.point(start + i))
                QtCore.QwtPainter.drawPolyline(self.painter_, poly)
                start = inext
                j += 1

    @decorators.BetaImplementation
    def __init__(self):
        self.d_ = self.FLStylePainterPrivate()
        self.d_.painter_ = QtGui.QPainter()
        self.relDpi_ = 1.0
        # self.d_.painter_.setWorldXForm(True) #FIXME
        self.saves_ = 0
        self.d_.lastLabelRect_.setSize(QtCore.QSize(0, 0))
        self.d_.errCode_ = self.ErrCode.NoError

    @decorators.BetaImplementation
    def painter(self):
        return self.d_.painter_

    @decorators.BetaImplementation
    def styleName(self):
        return self.d_.styleName_

    @decorators.BetaImplementation
    def relDpi(self):
        return self.d_.relDpi_

    @decorators.BetaImplementation
    def setStyleName(self, style):
        self.d_.styleName_ = style
        self.d_.parseDomDoc()

    @decorators.BetaImplementation
    def setRelDpi(self, relDpi):
        self.d_.relDpi_ = relDpi

    @decorators.BetaImplementation
    def beginMark(self, x, y, obj):
        st = self.d_.styleName_
        if st == "_mark" or st == "_simple" or st == "":
            self.d_.saves_ += 1
            self.d_.painter_.save()
            self.d_.painter_.translate(x, y)
        if self.d_.styleName_ == "_mark":
            self.d_.painter_.setBrush(Qt.NoBrush)
            self.d_.painter_.setPen(Qt.blue)
            self.d_.painter_.setFont(QtGui.QFont("Arial", 6))
            self.d_.painter_.drawText(0, 0, obj.name())

    @decorators.BetaImplementation
    def endMark(self):
        if self.d_.saves_ > 0:
            self.d_.painter_.restore()
            self.d_.saves_ -= 1

    @decorators.BetaImplementation
    def beginSection(self, x, y, w, h, obj):
        st = self.d_.styleName_
        if st == "_mark" or st == "_simple" or st == "":
            self.d_.saves_ += 1
            self.d_.painter_.save()
            self.d_.painter_.translate(x, y)
        if self.d_.styleName_ == "_mark":
            self.d_.painter_.setBrush(Qt.NoBrush)
            self.d_.painter_.setFont(QtGui.QFont("Arial", 6))
            self.d_.painter_.drawText(0, 0, obj.name())
            self.d_.painter_.setPen(QtGui.QPen(Qt.red, 0, Qt.DotLine))
            self.d_.painter_.drawRect(0, 0, w, h)
        elif obj and st and st != "" and self.d_.doc_.hasChildNodes():
            objName = obj.name()
            node = self.d_.objNodesMap_[objName]

            if node.attributes().contains("transform"):
                xx = x
                yy = y
                tx = 0.0
                ty = 0.0

                if self.d_.objBasesMap_.contains(objName):
                    pa = self.d_.objBasesMap_[objName]
                    xx = pa.first
                    yy = pa.second
                else:
                    self.d_.objBasesMap_.insert(objName, self.qMakePair(xx, yy))

                params = self.d_.paramsTransform(node.attribute("transform"))
                if params[0] == "translate":
                    tx = float(params[1])
                    ty = float(params[2])
                    s = "translate({},{})".format(tx + x - xx, ty + y - yy)
                    self.d_.transStack_.push_back(objName + ":" + s)
                elif params[0] == "matrix":
                    m: List[float] = []
                    for i in range(6):
                        m[i] = float(params[i + 1])
                    s = "matrix({},{},{},{},{},{})"
                    s.format(m[0], m[1], m[2], m[3], m[4] + x - xx, m[5] + y - yy)
                    self.d_.transStack.push_back(objName + ":" + s)
            else:
                self.d_.transStack_.push_back("void")

    @decorators.BetaImplementation
    def endSection(self):
        if self.d_.saves_ > 0:
            self.d_.painter_.restore()
            self.d_.saves_ -= 1

        if self.d_.transStack_ and self.d_.transStack_ != "":
            if self.d_.transStack_.back() != "void":
                objName = self.d_.transStack_.back().section(":", 0, 0)
                last = self.d_.objNodesMap_[objName].lastChild().toElement()
                if not last.attribute("id").startswith("_##"):
                    self.d_.play(last, self.ElementType.SectionElement)
            self.d_.transStack_.pop_back()

    @decorators.BetaImplementation
    def drawPixmap(self, pixmap, sx=0, sy=0, sw=-1, sh=-1, obj=0):
        self.d_.errCode_ = self.ErrCode.NoError
        st = self.d_.styleName_

        if not st or st == "":
            return False

        if st == "_simple" and obj.name().startswith("_##Label"):
            return True

        if self.d_.styleName_ == "_mark" or not self.d_.doc_.hasChildNodes():
            return False

        self.d_.pix_ = pixmap
        self.d_.sx_ = sx
        self.d_.sy_ = sy
        self.d_.sw_ = sw
        self.d_.sh_ = sh

        return self.d_.play(obj.name(), self.ElementType.ImageElement)

    @decorators.BetaImplementation
    def drawText(self, text, tf, obj):
        self.d_.errCode_ = self.ErrCode.NoError
        st = self.d_.styleName_

        if self.d_.svgMode_ and self.d_.relDpi_ != 1.0:
            fnt = QtGui.QFont(self.d_.painter_.font())
            fnt.setPointSizeFloat(fnt.pointSizeFloat() / self.d_.relDpi_)
            oldAscent = self.d_.painter_.fontMetrics().ascent()
            self.d_.painter_.setFont(fnt)
            self.d_.painter_.translate(0, oldAscent - self.d_.painter_.fontMetrics().ascent())

        if not st or st == "":
            return False

        if st == "_simple" and obj.name().startswith("_##Label"):
            return True

        if st == "_mark" or not self.d_.doc_.hasChildNodes():
            return False

        self.d_.text_ = text
        self.d_.tf_ = tf

        return self.d_.play(obj.name(), self.ElementType.TextElement)

    @decorators.BetaImplementation
    def drawLine(self, obj):
        self.d_.errCode_ = self.ErrCode.NoError
        st = self.d_.styleName_

        if not st or st == "":
            return False

        if st == "_simple" and obj.name().startswith("_##Line"):
            return True

        return (
            st != "_mark"
            and self.d_.doc_.hasChildNodes()
            and self.d_.play(obj.name(), self.ElementType.LineElement)
        )

    @decorators.BetaImplementation
    def drawRect(self, obj):
        self.d_.errCode_ = self.ErrCode.NoError
        st = self.d_.styleName_

        if not st or st == "":
            return False

        if st == "_simple" and obj.name().startswith("_##Label"):
            return True

        return (
            st != "_mark"
            and self.d_.doc_.hasChildNodes()
            and self.d_.play(obj.name(), self.ElementType.RectElement)
        )

    @decorators.BetaImplementation
    def setStyle(self, obj):
        self.d_.errCode_ = self.ErrCode.NoError
        st = self.d_.styleName_

        if not st or st == "":
            return False

        nla = obj.name().startswith("_##Label")
        nli = obj.name().startswith("_##Line")
        if st == "_simple" and (nla or nli):
            return True

        return (
            st != "_mark"
            and self.d_.doc_.hasChildNodes()
            and self.d_.play(obj.name(), self.ElementType.SetStyleElement)
        )

    @decorators.BetaImplementation
    def applyTransforms(self):
        self.d_.applyTransforms()

    @decorators.BetaImplementation
    def errCode(self):
        return self.d_.errCode_

    @decorators.BetaImplementation
    def normalizeSVGFile(self, fileName, fileNames):
        doc = QtXml.QDomDocument("svgdoc")
        docRes = QtXml.QDomDocument("svg")
        docElemRes = QtXml.QDomElement()
        file = QtCore.QFile()
        idList = QtCore.QStringListModel().stringList()
        errMsg = ""
        errLine = None
        errColumn = None

        for it in fileNames:
            file.setName(it)

            if not file.open(Qt.IO_ReadOnly):
                continue

            if not doc.setContent(file, errMsg, errLine, errColumn):
                file.close()
                return

            file.close()

            if it == fileNames[0]:
                docRes = doc.cloneNode(False).toDocument()
                docElemRes = doc.documentElement().cloneNode(False).toElement()

            n = QtXml.QDomNode(doc.documentElement().firstChild())
            while not n.isNull():
                e = QtXml.QDomElement(n.toElement())
                if not e.isNull():
                    eid = e.attribute("id")
                    if not idList.contains(eid):
                        idList.append(eid)
                        self.d_.normalizeTranslates(e, True)
                        docElemRes.appendChild(e.cloneNode())
                n = n.nextSibling()

        file.setName(fileName)
        if not file.open(Qt.IO_WriteOnly):
            return

        docElemRes.setAttributeNS(
            "http://www.w3.org/2000/svg", "xmlns:xlink", "http://www.w3.org/1999/xlink"
        )
        docRes.appendChild(docElemRes)
        s = QtCore.QTextStream(file)
        s.setEncoding(QtCore.QTextStream.UnicodeUTF8)
        s << docRes

    @decorators.BetaImplementation
    def setSVGMode(self, mode):
        self.d_.svgMode_ = mode
        QtCore.QwtPainter.setSVGMode(mode)
