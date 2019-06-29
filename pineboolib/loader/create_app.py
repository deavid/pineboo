from PyQt5.QtWidgets import QApplication
from optparse import Values
from pineboolib.plugins.dgi.dgi_qt.dgi_qt import dgi_qt


def create_app(DGI: dgi_qt, options: Values) -> QApplication:
    """Create a MainForm using the DGI or the core."""

    if not DGI.useMLDefault():
        return DGI.alternativeMain(options)

    from pineboolib.core.utils.utils_base import filedir

    app = DGI.create_app()

    if DGI.localDesktop():
        from PyQt5 import QtGui

        noto_fonts = ["NotoSans-BoldItalic.ttf", "NotoSans-Bold.ttf", "NotoSans-Italic.ttf", "NotoSans-Regular.ttf"]
        for fontfile in noto_fonts:
            QtGui.QFontDatabase.addApplicationFont(filedir("../share/fonts/Noto_Sans", fontfile))

        from pineboolib.fllegacy.flsettings import FLSettings

        sett_ = FLSettings()

        styleA = sett_.readEntry("application/style", None)
        if styleA is None:
            styleA = "Fusion"

        app.setStyle(styleA)

        fontA = sett_.readEntry("application/font", None)
        if fontA is None:
            if DGI.mobilePlatform():
                font = QtGui.QFont("Noto Sans", 14)
            else:
                font = QtGui.QFont("Noto Sans", 9)
            font.setBold(False)
            font.setItalic(False)
        else:
            font = QtGui.QFont(fontA[0], int(fontA[1]), int(fontA[2]), fontA[3] == "true")

        app.setFont(font)
    return app
