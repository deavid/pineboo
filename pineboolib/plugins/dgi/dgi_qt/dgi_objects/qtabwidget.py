# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

class QTabWidget(QtWidgets.QTabWidget):

    def setTabEnabled(self, tab, enabled):

        idx = self.indexByName(tab)
        if idx is None:
            return

        #if pineboolib.project._DGI.localDesktop():
        return QtWidgets.QTabWidget.setTabEnabled(self, idx, enabled)
        #else:
        #    pineboolib.project._DGI._par.addQueque("%s_setTabEnabled" % self.objectName(), [idx, enabled])

            # try:
            #     for idx in range(self.count()):
            #         if self.widget(idx).objectName() == tab.lower():
            #             if not pineboolib.project._DGI.localDesktop():
            #                 pineboolib.project._DGI._par.addQueque("%s_setTabEnabled" % self.objectName(), [idx, enabled])
            #             return QtWidgets.QTabWidget.setTabEnabled(self, idx, enabled)

            # except ValueError:
            #     print("ERROR: Tab not found:: QTabWidget::setTabEnabled %r : %r" % (tab, enabled))
            #     return False
        # print("ERROR: Unknown type for 1st arg:: QTabWidget::setTabEnabled %r : %r" % (tab, enabled))

    def showPage(self, tab):

        idx = self.indexByName(tab)
        if idx is None:
            return

        if pineboolib.project._DGI.localDesktop():
            return QtWidgets.QTabWidget.setCurrentIndex(self, idx)
        else:
            pass
            # pineboolib.project._DGI._par.addQueque("%s_setTabEnabled" % self.objectName(), [idx, enabled])

    def indexByName(self, tab):

        idx = None
        if isinstance(tab, int):
            return tab
        elif not isinstance(tab, str):
            logger.error("ERROR: Unknown type tab name or index:: QTabWidget %r", tab)
            return None

        try:
            for idx in range(self.count()):
                if self.widget(idx).objectName() == tab.lower():
                    return idx
        except ValueError:
            logger.error("ERROR: Tab not found:: QTabWidget, tab name = %r", tab)
        return None

    def removePage(self, idx):
        if isinstance(idx, int):
            self.removeTab(idx)