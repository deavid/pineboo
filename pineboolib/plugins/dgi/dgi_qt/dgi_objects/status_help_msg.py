class StatusHelpMsg(object):
    def send(self, text_):
        from pineboolib import pncontrolsfactory

        pncontrolsfactory.aqApp.statusHelpMsg(text_)
