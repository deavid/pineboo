class StatusHelpMsg(object):
    def send(self, text_) -> None:
        from pineboolib.fllegacy.flapplication import aqApp

        aqApp.statusHelpMsg(text_)
