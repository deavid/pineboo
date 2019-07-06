class ProgressDialogManager(object):
    progress_dialog_stack = None

    def __init__(self):
        self.progress_dialog_stack = []

    def create(self, title, steps, id_):

        from pineboolib import project
        from PyQt5 import QtCore

        pd_widget = project._DGI.QProgressDialog(str(title), str(project._DGI.QApplication.translate("scripts", "Cancelar")), 0, steps)
        pd_widget.setObjectName(id_)
        pd_widget.setWindowModality(QtCore.Qt.WindowModal)
        pd_widget.setWindowTitle(str(title))
        self.progress_dialog_stack.append(pd_widget)
        pd_widget.setMinimumDuration(100)

        return pd_widget

    def destroy(self, id_):
        pd_widget = self.progress_dialog_stack[-1]

        if id_ != "default":
            for w in self.progress_dialog_stack:
                if w.objectName() == id_:
                    pd_widget = w
                    break

        pd_widget.close()
        self.progress_dialog_stack.remove(pd_widget)

    def setProgress(self, step_number, id_):
        pd_widget = self.progress_dialog_stack[-1]

        if id_ != "default":
            for w in self.progress_dialog_stack:
                if w.objectName() == id_:
                    pd_widget = w
                    break

        pd_widget.setValue(step_number)

    def setLabelText(self, l, id_):
        pd_widget = self.progress_dialog_stack[-1]

        if id_ != "default":
            for w in self.progress_dialog_stack:
                if w.objectName() == id_:
                    pd_widget = w
                    break

        pd_widget.setLabelText(str(l))

    def setTotalSteps(self, tS, id_):
        pd_widget = self.progress_dialog_stack[-1]

        if id_ != "default":
            for w in self.progress_dialog_stack:
                if w.objectName() == id_:
                    pd_widget = w
                    break

        pd_widget.setRange(0, tS)
