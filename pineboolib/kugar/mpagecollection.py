from PyQt5 import QtCore
from PyQt5 import QtGui

from pineboolib import decorators
from pineboolib.flcontrols import ProjectClass


class MPageCollection(ProjectClass):

    @decorators.BetaImplementation
    def __init__(self, *args):
        if len(args) and isinstance(args[0], MPageCollection):
            self.copy(args[0])
        else:
            from pineboolib.kugar.mreportengine import MReportEngine

            super(MPageCollection, self).__init__()

            self.pages_ = []
            # self.pages_.setAutoDelete(True) #FIXME
            self.size_ = MReportEngine.PageSize.Letter
            self.orientation_ = MReportEngine.PageOrientation.Portrait
            self.dimensions_ = QtCore.QSize()
            self.dimensions_.setWidth(0)
            self.dimensions_.setHeight(0)
            self.printToPos_ = False
            self.topMargin_ = None
            self.leftMargin_ = None
            self.bottomMargin_ = None
            self.rightMargin_ = None
            self.pageIdx_ = None

    @decorators.BetaImplementation
    def clear(self):
        self.pages_.clear()
        self.pageIdx_ = None

    @decorators.BetaImplementation
    def appendPage(self):
        self.pageIdx_ = self.pageIdx_ if self.pageIdx_ else 0
        self.pages_.append(QtGui.QPicture())

    @decorators.BetaImplementation
    def copy(self, mpc):
        self.pages_ = mpc.pages_
        self.pageIdx_ = mpc.pageIdx_
        self.dimensions_ = mpc.dimensions_
        self.size_ = mpc.size_
        self.orientation_ = mpc.orientation_

    @decorators.BetaImplementation
    def getCurrentPage(self):
        return self.pages_[self.pageIdx_]

    @decorators.BetaImplementation
    def getFirstPage(self):
        self.pageIdx_ = 0
        return self.pages_[self.pageIdx_]

    @decorators.BetaImplementation
    def getPreviousPage(self):
        self.pageIdx_ -= 1
        return self.pages_[self.pageIdx_]

    @decorators.BetaImplementation
    def getNextPage(self):
        self.pageIdx_ += 1
        return self.pages_[self.pageIdx_]

    @decorators.BetaImplementation
    def getLastPage(self):
        self.pageIdx_ = len(self.pages_) - 1 if len(self.pages_) else 0
        return self.pages_[self.pageIdx_]

    @decorators.BetaImplementation
    def getPageAt(self, i):
        self.pageIdx_ = i
        return self.pages_[self.pageIdx_]

    @decorators.BetaImplementation
    def getCurrentIndex(self):
        return self.pageIdx_

    @decorators.BetaImplementation
    def setCurrentPage(self, idx):
        self.pageIdx_ = idx

    @decorators.BetaImplementation
    def setPageSize(self, s):
        self.size_ = s

    @decorators.BetaImplementation
    def setPageOrientation(self, o):
        self.orientation_ = o

    @decorators.BetaImplementation
    def setPageDimensions(self, dim):
        self.dimensions_ = dim

    @decorators.BetaImplementation
    def pageSize(self):
        return self.size_

    @decorators.BetaImplementation
    def pageOrientation(self):
        return self.orientation_

    @decorators.BetaImplementation
    def pageDimensions(self):
        return self.dimensions_

    @decorators.BetaImplementation
    def pageCount(self):
        return self.pages_.count()

    @decorators.BetaImplementation
    def printToPos(self):
        return self.printToPos_

    @decorators.BetaImplementation
    def setPrintToPos(self, ptp):
        self.printToPos_ = ptp

    @decorators.BetaImplementation
    def setPageMargins(self, top, left, bottom, right):
        self.topMargin_ = top
        self.leftMargin_ = left
        self.bottomMargin_ = bottom
        self.rightMargin_ = right

    @decorators.BetaImplementation
    def pageMargins(self):
        tm = self.topMargin_
        lm = self.leftMargin_
        bm = self.bottomMargin_
        rm = self.rightMargin_
        return tm, lm, bm, rm
