class progress_dialog_manager(object):
    progress_dialog_stack = None

    def __init__(self):
        self.progress_dialog_stack = []

    # FIXME: PEP8: should be called "def create". Use snake_python for naming
    # https://en.wikipedia.org/wiki/Naming_convention_(programming)#Python_and_Ruby
    def Create(self, title, steps, id_):

        # FIXME: We shouldn't load from DGI -> pncontrolsfactory.
        from pineboolib import pncontrolsfactory

        # FIXME: parent unused. Do we want to use it for creating QProgressDialog?
        # if self.progress_dialog_stack:
        #    parent = self.progress_dialog_stack[-1]

        pd_widget = pncontrolsfactory.QProgressDialog(
            str(title), str(pncontrolsfactory.QApplication.translate("scripts", "Cancelar")), 0, steps
        )
        pd_widget.setObjectName(id_)
        pd_widget.setWindowTitle(str(title))
        self.progress_dialog_stack.append(pd_widget)
        pd_widget.setMinimumDuration(100)

        return pd_widget

    def Destroy(self, id_):
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
