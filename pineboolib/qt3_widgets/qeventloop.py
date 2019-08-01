from PyQt5 import QtCore


class QEventLoop(QtCore.QEventLoop):
    def exitLoop(self) -> None:
        super().exit()

    def enterLoop(self) -> None:
        super().exec_()
