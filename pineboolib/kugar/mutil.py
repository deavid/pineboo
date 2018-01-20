import math
from enum import Enum

from PyQt5.QtCore import Qt

from pineboolib import decorators
from pineboolib.flcontrols import ProjectClass


class MUtil(ProjectClass):

    class DateFormatType(Enum):
        MDY_SLASH = 0
        MDY_DASH = 1
        MMDDY_SLASH = 2
        MMDDY_DASH = 3
        MDYYYY_SLASH = 4
        MDYYYY_DASH = 5
        MMDDYYYY_SLASH = 6
        MMDDYYYY_DASH = 7
        YYYYMD_SLASH = 8
        YYYYMD_DASH = 9
        DDMMYY_PERIOD = 10
        DDMMYYYY_PERIOD = 11
        DMY_SLASH = 12
        DMY_DASH = 13
        DDMMY_SLASH = 14
        DDMMY_DASH = 15
        DMYYYY_SLASH = 16
        DMYYYY_DASH = 17
        DDMMYYYY_SLASH = 18
        DDMMYYYY_DASH = 19
        DD = 20
        MM = 21
        Month = 22
        YYYY = 23
        YY = 24
        Y = 25

    @decorators.BetaImplementation
    def formatDate(self, value, dformat):
        string = ""
        month = str(value.month())
        day = str(value.day())
        year = str(value.year())

        if value.month() < 10:
            month = "0" + month
        if value.day() < 10:
            day = "0" + day

        year = year[-2:]

        if dformat == MUtil.DateFormatType.MDY_SLASH:
            string = "{}/{}/{}".format(value.month(), value.day(), year)
        elif dformat == MUtil.DateFormatType.MDY_DASH:
            string = "{}-{}-{}".format(value.month(), value.day(), year)
        elif dformat == MUtil.DateFormatType.MMDDY_SLASH:
            string = "{}/{}/{}".format(month, day, year)
        elif dformat == MUtil.DateFormatType.MMDDY_DASH:
            string = "{}-{}-{}".format(month, day, year)
        elif dformat == MUtil.DateFormatType.MDYYYY_SLASH:
            string = "{}/{}/{}".format(value.month(),
                                       value.day(), value.year())
        elif dformat == MUtil.DateFormatType.MDYYYY_DASH:
            string = "{}-{}-{}".format(value.month(),
                                       value.day(), value.year())
        elif dformat == MUtil.DateFormatType.MMDDYYYY_SLASH:
            string = "{}/{}/{}".format(month, day, value.year())
        elif dformat == MUtil.DateFormatType.MMDDYYYY_DASH:
            string = "{}-{}-{}".format(month, day, value.year())
        elif dformat == MUtil.DateFormatType.YYYYMD_SLASH:
            string = "{}/{}/{}".format(value.year(),
                                       value.month(), value.day())
        elif dformat == MUtil.DateFormatType.YYYYMD_DASH:
            string = "{}-{}-{}".format(value.year(),
                                       value.month(), value.day())
        elif dformat == MUtil.DateFormatType.DDMMYY_PERIOD:
            string = "{}.{}.{}".format(day, month, year)
        elif dformat == MUtil.DateFormatType.DDMMYYYY_PERIOD:
            string = "{}.{}.{}".format(day, month, value.year())
        elif dformat == MUtil.DateFormatType.DMY_SLASH:
            string = "{}/{}/{}".format(value.day(), value.month(), year)
        elif dformat == MUtil.DateFormatType.DMY_DASH:
            string = "{}-{}-{}".format(value.day(), value.month(), year)
        elif dformat == MUtil.DateFormatType.DDMMY_SLASH:
            string = "{}/{}/{}".format(day, month, year)
        elif dformat == MUtil.DateFormatType.DDMMY_DASH:
            string = "{}-{}-{}".format(day, month, year)
        elif dformat == MUtil.DateFormatType.DMYYYY_SLASH:
            string = "{}/{}/{}".format(value.day(),
                                       value.month(), value.year())
        elif dformat == MUtil.DateFormatType.DMYYYY_DASH:
            string = "{}-{}-{}".format(value.day(),
                                       value.month(), value.year())
        elif dformat == MUtil.DateFormatType.DDMMYYYY_SLASH:
            string = "{}/{}/{}".format(day, month, value.year())
        elif dformat == MUtil.DateFormatType.DDMMYYYY_DASH:
            string = "{}-{}-{}".format(day, month, value.year())
        elif dformat == MUtil.DateFormatType.DD:
            string = "{}".format(day)
        elif dformat == MUtil.DateFormatType.MM:
            string = "{}".format(month)
        elif dformat == MUtil.DateFormatType.Month:
            string = Qt.QDate.longMonthName(value.month())
        elif dformat == MUtil.DateFormatType.YYYY:
            string = "{}".format(value.year())
        elif dformat == MUtil.DateFormatType.YY:
            string = year[-2:]
        elif dformat == MUtil.DateFormatType.Y:
            string = year[-1:]
        else:
            string = value.toString()

        return string

    @decorators.BetaImplementation
    def count(self, values):
        return values.size()

    @decorators.BetaImplementation
    def sum(self, values):
        tmpSum = 0.0
        size = self.count(values)

        for i in range(size):
            tmpSum = tmpSum + values.at(i)

        return tmpSum

    @decorators.BetaImplementation
    def average(self, values):
        return self.sum(values) / self.count(values)

    @decorators.BetaImplementation
    def variance(self, values):
        tmpVar = 0.0
        tmpAvg = self.average(values)
        size = self.count(values)

        for i in range(size):
            tmpVar = tmpVar + pow(values.at(i) - tmpAvg, 2) / size

        return tmpVar

    @decorators.BetaImplementation
    def stdDeviation(self, values):
        return math.sqrt(self.variance(values))
