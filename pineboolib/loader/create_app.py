def create_app(DGI, options):
    """Create a MainForm using the DGI or the core."""

    if not DGI.useMLDefault():
        return DGI.alternativeMain(options)

    from pineboolib.utils import filedir
    import pineboolib

    app = DGI.create_app()
    pineboolib._DGI = DGI  # Almacenamos de DGI seleccionado para futuros usos

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
