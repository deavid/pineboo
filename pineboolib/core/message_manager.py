"""
Crea una conexión con el interface adecuado del DGI usado para mostrar mensajes
"""


class manager(object):

    _dgi = None

    def __init__(self, dgi):
        self._dgi = dgi

    def send(self, type_, function_=None, data_=None):
        obj_ = getattr(self._dgi, type_, None)
        if obj_:
            attr_ = getattr(obj_, function_, None)
            if attr_ is not None:
                if data_ is not None:
                    attr_(data_)
                else:
                    attr_()

            self._dgi.processEvents()

        print("**", type_, function_, data_)

    # if DGI.localDesktop():
    #     splash.showMessage("Listo ...", QtCore.Qt.AlignLeft, QtCore.Qt.white)
    #     DGI.processEvents()
    #     # main_window.w_.activateWindow()
    # QtCore.QTimer.singleShot(1000, splash.hide)
