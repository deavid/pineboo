from enum import Enum

from pineboolib import decorators
from pineboolib.flcontrols import ProjectClass

from pineboolib.kugar.mfieldobject import MFieldObject
from pineboolib.kugar.mreportobject import MReportObject


class MCalcObject(ProjectClass, MFieldObject):

    class CalculationType(Enum):
        Count = 0
        Sum = 1
        Average = 2
        Variance = 3
        StandardDeviation = 4
        NoOperation = 5
        CallFunction = 6

    @decorators.BetaImplementation
    def __init__(self, *args):
        if len(args) and isinstance(args[0], MCalcObject):
            self.copy(args[0])
        else:
            super(MCalcObject, self).__init__()

            self.calcType_ = self.CalculationType.Count
            self.calcFunction_ = None
            self.drawAtHeader_ = None
            self.fromGrandTotal_ = None

    @decorators.BetaImplementation
    def copy(self, mco):
        self.calcType_ = mco.calcType_

    @decorators.BetaImplementation
    def RTTI(self):
        return MReportObject.ReportObjectType.Calc

    @decorators.BetaImplementation
    def setCalculationType(self, cType):
        self.calcType_ = cType

    @decorators.BetaImplementation
    def setCalculationFunction(self, cFunc):
        self.calcFunction_ = cFunc

    @decorators.BetaImplementation
    def setDrawAtHeader(self, dah):
        self.drawAtHeader_ = dah

    @decorators.BetaImplementation
    def setFromGrandTotal(self, fgt):
        self.fromGrandTotal_ = fgt

    @decorators.BetaImplementation
    def getCalculationType(self):
        return self.calcType_

    @decorators.BetaImplementation
    def getCalculationFunction(self):
        return self.calcFunction_

    @decorators.BetaImplementation
    def getDrawAtHeader(self):
        return self.drawAtHeader_

    @decorators.BetaImplementation
    def getFromGrandTotal(self):
        return self.fromGrandTotal_
