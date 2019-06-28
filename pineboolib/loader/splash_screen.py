def show_splashscreen(project):
    """Show a splashscreen to inform keep the user busy while Pineboo is warming up."""
    from PyQt5 import QtGui, QtCore, QtWidgets
    from pineboolib.core.utils.utils_base import filedir

    splash_path = filedir("../share/splashscreen/splash_%s.png" % project.dbname)
    if not os.path.exists(splash_path):
        splash_path = filedir("../share/splashscreen/splash.png")

    splash_pix = QtGui.QPixmap(splash_path)
    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())

    frameGm = splash.frameGeometry()
    screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
    centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
    frameGm.moveCenter(centerPoint)
    splash.move(frameGm.topLeft())
    splash.show()

    return splash
