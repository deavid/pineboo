from typing import Any, List


class ProgressDialogManager(object):
    progress_dialog_stack: List[Any] = []

    def __init__(self):
        self.progress_dialog_stack = []

    def create(self, title, steps, id_) -> Any:

        from pineboolib.application import project
        from PyQt5 import QtCore  # type: ignore

        if project._DGI:
            pd_widget = project.DGI.QProgressDialog(str(title), str(project.DGI.QApplication.translate("scripts", "Cancelar")), 0, steps)
            if pd_widget is not None:
                pd_widget.setObjectName(id_)
                pd_widget.setWindowModality(QtCore.Qt.WindowModal)
                pd_widget.setWindowTitle(str(title))
                self.progress_dialog_stack.append(pd_widget)
                pd_widget.setMinimumDuration(100)

                return pd_widget

        return None

    def destroy(self, id_) -> None:
        pd_widget = self.progress_dialog_stack[-1]

        if id_ != "default":
            for w in self.progress_dialog_stack:
                if w.objectName() == id_:
                    pd_widget = w
                    break

        pd_widget.close()
        self.progress_dialog_stack.remove(pd_widget)

    def setProgress(self, step_number, id_) -> None:
        pd_widget = self.progress_dialog_stack[-1]

        if id_ != "default":
            for w in self.progress_dialog_stack:
                if w.objectName() == id_:
                    pd_widget = w
                    break

        pd_widget.setValue(step_number)

    def setLabelText(self, l, id_) -> None:
        pd_widget = self.progress_dialog_stack[-1]

        if id_ != "default":
            for w in self.progress_dialog_stack:
                if w.objectName() == id_:
                    pd_widget = w
                    break

        pd_widget.setLabelText(str(l))

    def setTotalSteps(self, tS, id_) -> None:
        pd_widget = self.progress_dialog_stack[-1]

        if id_ != "default":
            for w in self.progress_dialog_stack:
                if w.objectName() == id_:
                    pd_widget = w
                    break

        pd_widget.setRange(0, tS)
