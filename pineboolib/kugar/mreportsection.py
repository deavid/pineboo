from enum import Enum

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.Qt import QObject

from pineboolib import decorators

from pineboolib.kugar.mutil import MUtil
from pineboolib.kugar.mfieldobject import MFieldObject
from pineboolib.kugar.mcalcobject import MCalcObject
from pineboolib.kugar.mspecialobject import MSpecialObject

from PyQt5.QtXml import QDomNode as FLDomNodeInterface  # FIXME


class MReportSection(QObject):

    idSecGlob_ = 0

    class PrintFrequency(Enum):
        FirstPage = 0
        EveryPage = 1
        LastPage = 2

    @decorators.BetaImplementation
    def __init__(self, *args):

        if len(args) and isinstance(args[0], MReportSection):
            self.copy(args[0])
        else:
            super(MReportSection, self).__init__()

            self.strIdSec_ = args[0] if len(args) else ""
            self.idSec_ = self.idSecGlob_
            self.height_ = 1
            self.width_ = 584
            self.level_ = 0

            self.frequency_ = self.PrintFrequency.EveryPage

            self.reportDate_ = QtCore.QDate.currentDate()
            self.pageNumber_ = 0

            self.lines_ = []
            # self.lines_.setAutoDelete(True) #FIXME

            self.labels_ = []
            # self.labels_.setAutoDelete(True) #FIXME

            self.specialFields_ = []
            # self.specialFields_.setAutoDelete(True) #FIXME

            self.fields_ = []
            # self.fields_.setAutoDelete(True) #FIXME

            self.calculatedFields_ = []
            # self.calculatedFields_.setAutoDelete(True) #FIXME

    @decorators.NotImplementedWarn
    # def operator=(self, mrs): #FIXME
    def operator(self, mrs):
        return self

    @decorators.BetaImplementation
    def clear(self):
        self.lines_.clear()
        self.labels_.clear()
        self.specialFields_.clear()
        self.calculatedFields_.clear()
        self.fields_.clear()

    @decorators.BetaImplementation
    def addLine(self, line):
        self.lines_.append(line)

    @decorators.BetaImplementation
    def addLabel(self, label):
        self.labels_.append(label)
        label.setSectionIndex(self.labels_.at())

    @decorators.BetaImplementation
    def addSpecialField(self, special):
        self.specialFields_.append(special)
        special.setSectionIndex(self.specialFields_.at())

    @decorators.BetaImplementation
    def addCalculatedField(self, calc):
        self.calculatedFields_.append(calc)
        calc.setSectionIndex(self.calculatedFields_.at())

    @decorators.BetaImplementation
    def addField(self, field):
        self.fields_.append(field)
        field.setSectionIndex(self.fields_.at())

    @decorators.BetaImplementation
    def setFieldData(self, idx, data, record=0, fRec=False):
        field = self.fields_.at()
        field.setText(data)
        if record and fRec:
            ft = field.getDataType()

            date = MFieldObject.DataType.Date
            px = MFieldObject.DataType.Pixmap
            cb = MFieldObject.DataType.CodBar
            if ft != date and ft != px and ft != cb:
                fn = field.getFieldName()
                record.toElement().setAttribute(
                    self.strIdSec_ + int(self.level_) + "_" + fn,
                    field.getText()
                )

    @decorators.BetaImplementation
    def setCalcFieldData(self, values=0, values2=0, record=0, fRec=False):
        if isinstance(values, int) and isinstance(values2, str):
            self.calculatedFields_.at(values).setText(values2)
            return

        i = 0
        value = ""

        for field in self.calculatedFields_:
            if field != 0:
                if field.getFromGrandTotal():
                    continue

                calcType = field.getCalculationType()

                if calcType == MCalcObject.CalculationType.NoOperation:
                    if values2:
                        value = values2[i]
                    self.calculateField(field, 0, value, record, fRec)
                elif calcType == MCalcObject.CalculationType.CallFunction:
                    self.calculateField(field, 0, value, record, fRec)
                else:
                    if values:
                        self.calculateField(field, values.at(
                            i), value, record, fRec)
            i += 1

    @decorators.BetaImplementation
    def setCalcFieldDataGT(self, values, record=0, fRec=False):
        for field in self.calculatedFields_:
            if field != 0:
                if not field.getFromGrandTotal() and self.level_ > -1:
                    continue

                grandTotalIndex = field.getSectionIndex()

                if grandTotalIndex != -1:
                    self.calculateField(field, values.at(
                        grandTotalIndex), "", record, fRec)

    @decorators.BetaImplementation
    def calculateField(self, field, values, values2="", record=0, fRec=False):
        calcType = field.getCalculationType()
        fn = field.getFieldName()

        if calcType == MCalcObject.CalculationType.Count:
            if values:
                field.setText(int(MUtil.count(values)))
                if record and fRec:
                    record.toElement().setAttribute(
                        self.strIdSec_ + int(self.level_) + "_" + fn,
                        field.getText()
                    )
        elif calcType == MCalcObject.CalculationType.Sum:
            if values:
                field.setText(int(MUtil.sum(values), 'f'))
                if record and fRec:
                    record.toElement().setAttribute(
                        self.strIdSec_ + int(self.level_) + "_" + fn,
                        field.getText()
                    )
        elif calcType == MCalcObject.CalculationType.Average:
            if values:
                field.setText(int(MUtil.average(values), 'f'))
                if record and fRec:
                    record.toElement().setAttribute(
                        self.strIdSec_ + int(self.level_) + "_" + fn,
                        field.getText()
                    )
        elif calcType == MCalcObject.CalculationType.Variance:
            if values:
                field.setText(int(MUtil.variance(values), 'f'))
                if record and fRec:
                    record.toElement().setAttribute(
                        self.strIdSec_ + int(self.level_) + "_" + fn,
                        field.getText()
                    )
        elif calcType == MCalcObject.CalculationType.StandardDeviation:
            if values:
                field.setText(int(MUtil.stdDeviation(values), 'f'))
                if record and fRec:
                    record.toElement().setAttribute(
                        self.strIdSec_ + int(self.level_) + "_" + fn,
                        field.getText()
                    )
        elif calcType == MCalcObject.CalculationType.NoOperation:
            field.setText(values2)
            if fRec and values2 != "":
                record.toElement().setAttribute(
                    self.strIdSec_ + int(self.level_) + "_" + fn,
                    field.getText()
                )
        elif calcType == MCalcObject.CalculationType.CallFunction:
            if record and field.getCalculationFunction() != "":
                dni = FLDomNodeInterface(record)
                argList = QtCore.QSArgumentList()
                argList << dni
                argList << fn

                v = field.getCalculationFunction()(*argList)

                if v and str(v).upper() != "NAN":
                    field.setText(str(v))

                    px = MCalcObject.CalculationType.Pixmap
                    if fRec and field.getDataType() != px:
                        cf = field.getCalculationFunction()
                        record.toElement().setAttribute(
                            self.strIdSec_ + int(self.level_) + "_" + cf,
                            field.getText()
                        )
                del dni

        if record:
            field.setDomNodeData(record)

    @decorators.BetaImplementation
    def mustBeDrawed(self, record):
        fields = record.attributes()
        drawIfField = self.getDrawIf()

        if drawIfField != "":
            n = fields.namedItem(drawIfField)

            if n.isNull():
                return False

            value = n.toAttr().value()

            if not value or value == "" or value == "false":
                return False

            f = float(value)
            if not f or f == 0:
                return False

        return True

    @decorators.BetaImplementation
    def getCalcFieldIndex(self, field):
        i = 0
        for tmpField in self.calculatedFields_:
            if tmpField != 0:
                if tmpField.getFieldName() == field:
                    return i
            i += 1
        return i

    @decorators.BetaImplementation
    def getFieldIndex(self, field):
        i = 0
        for tmpField in self.fields_:
            if tmpField != 0:
                if tmpField.getFieldName() == field:
                    return i
            i += 1
        return i

    @decorators.BetaImplementation
    def draw(self, p, xoffset, yoffset, newHeight):
        self.drawObjects(p, xoffset, yoffset, newHeight)
        self.lastXOffset_ = xoffset
        self.lastYOffset_ = yoffset

    @decorators.BetaImplementation
    def drawHeaderObjects(self, p, pages, header):
        xcalc = header.getLastXOffset()
        ycalc = header.getLastYOffset()

        currentPage = p.painter().device()
        lastPage = header.onPage()
        currentPageCopy = 0
        lastPageCopy = 0

        if currentPage != lastPage:
            p.painter().end()
            currentPageCopy = QtGui.QPicture(currentPage)
            lastPageCopy = QtGui.QPicture(lastPage)
            p.painter().begin(lastPage)
            lastPageCopy.play(p.painter())

        self.setName("_##H{}-{}".format(self.strIdSec_, str(self.level_)))
        p.beginSection(xcalc, ycalc, self.width_, self.height_, self)
        countObj = 0

        for calcField in self.calculatedFields_:
            if calcField != 0:
                if calcField.getDrawAtHeader():
                    if calcField.getObjectId():
                        calcField.setName(
                            "_##H{}-Calc.{}-{}".format(
                                self.idSec_,
                                calcField.fieldName_,
                                calcField.getObjectId()
                            )
                        )
                    else:
                        calcField.setName(
                            "_##H{}-Calc.{}-{}".format(
                                self.idSec_,
                                calcField.fieldName_,
                                countObj
                            )
                        )
                        countObj += 1
                p.beginMark(calcField.getX(), calcField.getY(), calcField)
                calcField.draw(p)
                p.endMark()

        p.endSection()

        if currentPage != lastPage:
            p.painter().end()
            p.painter().begin(currentPage)
            currentPageCopy.play(p.painter())
            del lastPageCopy
            del currentPageCopy

    @decorators.BetaImplementation
    def drawObjects(self, p, xoffset, yoffset, newHeight):
        xcalc = xoffset
        ycalc = yoffset

        modifiedHeight = 0

        self.setName("_##{}-{}".format(self.strIdSec_, str(self.level_)))
        p.beginSection(xcalc, ycalc, self.width_, self.height_, self)
        countObj = 0
        yObjectPos = 0

        for line in self.lines_:
            if line != 0:
                if line.getObjectId():
                    line.setName(
                        "_##Line{}-{}".format(self.idSec_, line.getObjectId()))
                else:
                    line.setName("_##Line{}-{}".format(self.idSec_, countObj))
                    countObj += 1
                p.beginMark(line.xpos1_, line.ypos1_, line)
                line.draw(p)
                p.endMark()

        for label in self.labels_:
            if label != 0:
                if label.getObjectId():
                    label.setName(
                        "_##Label{}-{}".format(
                            self.idSec_,
                            label.getObjectId()
                        )
                    )
                else:
                    label.setName(
                        "_##Label{}-{}".format(self.idSec_, countObj)
                    )
                    countObj += 1
                ly = label.getY()
                lh = label.getHeight()
                ldab = label.getDrawAtBottom()
                yObjectPos = newHeight - lh if ldab else ly
                p.beginMark(label.getX(), yObjectPos, label)
                modifiedHeight = label.draw(p)
                p.endMark()

                if modifiedHeight and (ly + modifiedHeight) > self.height_:
                    newHeight = label.getY() + modifiedHeight

        for calcfield in self.calculatedFields_:
            if calcfield != 0:
                if calcfield.getObjectId():
                    calcfield.setName(
                        "_##{}-Calc.{}-{}".format(
                            self.idSec_,
                            calcfield.fieldName_,
                            calcfield.getObjectId()
                        )
                    )
                else:
                    calcfield.setName(
                        "_##{}-Calc.{}-{}".format(
                            self.idSec_,
                            calcfield.fieldName_,
                            countObj
                        )
                    )
                    countObj += 1
                ch = calcfield.getHeight()
                cy = calcfield.getY()
                cdab = calcfield.getDrawAtBottom()
                yObjectPos = newHeight - ch if cdab else cy
                p.beginMark(calcfield.getX(), yObjectPos, calcfield)
                modifiedHeight = calcfield.draw(p)
                p.endMark()

                if modifiedHeight and (cy + modifiedHeight) > self.height_:
                    newHeight = calcfield.getY() + modifiedHeight

        for special in self.specialFields_:
            if special != 0:
                if special.getObjectId():
                    special.setName(
                        "_##SpecialField{}-{}".format(
                            self.idSec_,
                            special.getObjectId()
                        )
                    )
                else:
                    special.setName(
                        "_##SpecialField{}-{}".format(self.idSec_, countObj))
                    countObj += 1
                sh = special.getHeight()
                sdab = special.getDrawAtBottom()
                sy = special.getY()
                yObjectPos = newHeight - sh if sdab else sy
                p.beginMark(special.getX(), yObjectPos, special)

                spType = special.getType()
                if spType == MSpecialObject.DataType.Date:
                    special.setText(self.reportDate_)
                elif spType == MSpecialObject.DataType.pageNumber:
                    special.setText(self.pageNumber_)

                special.draw(p)
                p.endMark()

        for field in self.fields_:
            if field != 0:
                if field.getObjectId():
                    field.setName(
                        "_##{}.{}-{}".format(
                            self.idSec_,
                            field.fieldName_,
                            field.getObjectId()
                        )
                    )
                else:
                    field.setName(
                        "_##{}.{}-{}".format(
                            self.idSec_,
                            field.fieldName_,
                            countObj
                        )
                    )
                    countObj += 1
                fh = field.getHeight()
                fy = field.getY()
                fdab = field.getDrawAtBottom()
                yObjectPos = newHeight - fh if fdab else fy
                p.beginMark(field.getX(), yObjectPos, field)
                modifiedHeight = field.draw(p)
                p.endMark()

                if modifiedHeight and (fy + modifiedHeight) > self.height_:
                    newHeight = field.getY() + modifiedHeight

        p.endSection()

    @decorators.BetaImplementation
    def csvData(self):
        csvData = ""

        for calcfield in self.calculatedFields_:
            if calcfield != 0:
                calcType = calcfield.getCalculationType()
                no = MCalcObject.CalculationType.NoOperation
                cf = MCalcObject.CalculationType.CallFunction
                if calcType == no or calcType == cf:
                    fieldValue = calcfield.getText()
                    fieldValue.replace("\n", "-")
                    csvData = csvData + "|" + fieldValue

        for field in self.fields_:
            if field != 0:
                fieldValue = field.getText()
                fieldValue.replace("\n", "-")
                csvData = csvData + "|" + fieldValue

    @decorators.BetaImplementation
    def getHeight(self, p=None):
        if p is None:
            return self.height_

        modifiedHeight = 0
        newHeight = self.height_

        for label in self.labels_:
            if label != 0:
                modifiedHeight = label.calcHeight(p)
                ly = label.getY()
                if modifiedHeight and (ly + modifiedHeight) > self.height_:
                    newHeight = label.getY() + modifiedHeight

        for calcfield in self.calculatedFields_:
            if calcfield != 0:
                if not calcfield.getDrawAtHeader():
                    modifiedHeight = calcfield.calcHeight(p)
                    cy = calcfield.getY()
                    if modifiedHeight and (cy + modifiedHeight) > self.height_:
                        newHeight = calcfield.getY() + modifiedHeight

        for field in self.fields_:
            if field != 0:
                modifiedHeight = field.calcHeight(p)
                fy = field.getY()
                if modifiedHeight and (fy + modifiedHeight) > self.height_:
                    newHeight = field.getY() + modifiedHeight

        return newHeight

    @classmethod
    @decorators.BetaImplementation
    def resetIdSecGlob(cls):
        cls.idSecGlob_ = 0

    @decorators.BetaImplementation
    def copy(self, mrs):
        self.clear()

        self.strIdSec_ = mrs.strIdSec_
        self.idSec_ = mrs.idSec_

        self.height_ = mrs.height_
        self.frequency_ = mrs.frequency_

        self.lines_ = mrs.lines_
        self.labels_ = mrs.labels_
        self.specialFields_ = mrs.specialFields_
        self.calculatedFields_ = mrs.calculatedFields_
        self.fields_ = mrs.fields_

    @decorators.BetaImplementation
    def setIdSec(self, id):
        self.idSec_ = id

    @decorators.BetaImplementation
    def idSec(self):
        return self.idSec_

    @decorators.BetaImplementation
    def getWidth(self):
        return self.width_

    @decorators.BetaImplementation
    def setHeight(self, h):
        self.height_ = h

    @decorators.BetaImplementation
    def setWidth(self, w):
        self.width_ = w

    @decorators.BetaImplementation
    def setDrawIf(self, dI):
        self.drawIf_ = dI

    @decorators.BetaImplementation
    def getDrawIf(self):
        return self.drawIf_

    @decorators.BetaImplementation
    def setLevel(self, l):
        self.level_ = l

    @decorators.BetaImplementation
    def getLevel(self):
        return self.level_

    @decorators.BetaImplementation
    def setNewPage(self, b):
        self.newPage_ = b

    @decorators.BetaImplementation
    def setPlaceAtBottom(self, b):
        self.placeAtBottom_ = b

    @decorators.BetaImplementation
    def setDrawAllPages(self, b):
        self.drawAllPages_ = b

    @decorators.BetaImplementation
    def newPage(self):
        return self.newPage_

    @decorators.BetaImplementation
    def placeAtBottom(self):
        return self.placeAtBottom_

    @decorators.BetaImplementation
    def drawAllPages(self):
        return self.drawAllPages_

    @decorators.BetaImplementation
    def setPageNumber(self, page):
        self.pageNumber_ = page

    @decorators.BetaImplementation
    def setReportDate(self, date):
        self.reportDate_ = date

    @decorators.BetaImplementation
    def setPrintFrequency(self, printFrequency):
        self.frequency_ = printFrequency

    @decorators.BetaImplementation
    def printFrequency(self):
        return self.frequency_

    @decorators.BetaImplementation
    def getLastXOffset(self):
        return self.lastXOffset_

    @decorators.BetaImplementation
    def getLastYOffset(self):
        return self.lastYOffset_

    @decorators.BetaImplementation
    def getLastPageIndex(self):
        return self.lastPageIndex_

    @decorators.BetaImplementation
    def onPage(self):
        return self.onPage_

    @decorators.BetaImplementation
    def setLastPageIndex(self, i):
        self.lastPageIndex_ = i

    @decorators.BetaImplementation
    def setOnPage(self, page):
        self.onPage_ = page

    @decorators.BetaImplementation
    def getCalcFieldCount(self):
        return len(self.calculatedFields_)

    @decorators.BetaImplementation
    def getFieldCount(self):
        return self.fields_.count()

    @decorators.BetaImplementation
    def getFieldName(self, idx):
        return self.fields_.at(idx).getFieldName()

    @decorators.BetaImplementation
    def getCalcFieldName(self, idx):
        return self.calculatedFields_.at(idx).getFieldName()

    @decorators.BetaImplementation
    def getField(self, idx):
        return self.fields_.at(idx)

    @decorators.BetaImplementation
    def getCalcField(self, idx):
        return self.calculatedFields_.at(idx)

    @decorators.BetaImplementation
    def setName(self, name):
        self.objectName = name

    @decorators.BetaImplementation
    def name(self):
        return self.objectName
