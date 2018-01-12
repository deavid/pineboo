from PyQt5.QtCore import Qt

from pineboolib import decorators
from pineboolib.flcontrols import ProjectClass

from pineboolib.kugar.mreportengine import MReportEngine


class MPageCollection(ProjectClass):

    @decorators.BetaImplementation
    def __init__(self, *args):
        if isinstance(args[0], MPageCollection):
            self.copy(args[0])
        else:
            super(MPageCollection, self).__init__(*args)

            self.pages_ = Qt.QPtrList()
            self.pages_.setAutoDelete(True)
            self.size_ = MReportEngine.PageSize.Letter
            self.orientation_ = MReportEngine.PageOrientation.Portrait
            self.dimensions_ = Qt.QSize()
            self.dimensions_.setWidth(0)
            self.dimensions_.setHeight(0)
            self.printToPos_ = False
            self.topMargin_ = None
            self.leftMargin_ = None
            self.bottomMargin_ = None
            self.rightMargin_ = None

    @decorators.BetaImplementation
    def clear(self):
        self.pages_.clear()

    @decorators.BetaImplementation
    def appendPage(self):
        self.pages_.append(Qt.QPicture())

    @decorators.BetaImplementation
    def copy(self, mpc):
        self.pages_ = mpc.pages_
        self.dimensions_ = mpc.dimensions_
        self.size_ = mpc.size_
        self.orientation_ = mpc.orientation_

    @decorators.BetaImplementation
    def getCurrentPage(self):
        return self.pages_.current()

    @decorators.BetaImplementation
    def getFirstPage(self):
        return self.pages_.first()

    @decorators.BetaImplementation
    def getPreviousPage(self):
        return self.pages_.prev()

    @decorators.BetaImplementation
    def getNextPage(self):
        return self.pages_.next()

    @decorators.BetaImplementation
    def getLastPage(self):
        return self.pages_.last()

    @decorators.BetaImplementation
    def getPageAt(self, i):
        return self.pages_.at(i)

    @decorators.BetaImplementation
    def getCurrentIndex(self):
        return self.pages_.at()

    @decorators.BetaImplementation
    def setCurrentPage(self, idx):
        self.pages_.at(idx)

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
        return self.topMargin_, self.leftMargin_, self.bottomMargin_, self.rightMargin_
