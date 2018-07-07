from pineboolib import decorators
from pineboolib.flcontrols import ProjectClass

from pineboolib.kugar.mreportsection import MReportSection


class MReportDetail(ProjectClass, MReportSection):

    @decorators.BetaImplementation
    def __init__(self, *args):
        super(MReportDetail, self).__init__(*args)

    @decorators.NotImplementedWarn
    # def operator=(self, mrd): #FIXME
    def operator(self, mrd):
        return self
