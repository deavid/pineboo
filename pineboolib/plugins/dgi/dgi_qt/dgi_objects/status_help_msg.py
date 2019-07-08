class StatusHelpMsg(object):
    def send(self, text_):
        from pineboolib.fllegacy.flapplication import aqApp

        aqApp.statusHelpMsg(text_)
