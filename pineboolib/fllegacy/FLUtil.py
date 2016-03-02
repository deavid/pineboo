# -*- coding: utf-8 -*-

from pineboolib.flcontrols import ProjectClass
from pineboolib import decorators

class FLUtil(ProjectClass):
    progress_dialog_stack = []
    def __getattr__(self, name): return DefFun(self, name)

    def translate(self, group, string):
        return QtCore.QString(string)

    def sqlSelect(self, table, fieldname, where):
        if where: where = "AND " + where
        cur = pineboolib.project.conn.cursor()

        cur.execute("""SELECT %s FROM %s WHERE 1=1 %s LIMIT 1""" % (fieldname, table, where))
        for ret, in cur:
            return ret

    def createProgressDialog(self, title, steps):
        pd_widget = ProgressDialog()
        pd_widget.setup(title, steps)
        self.__class__.progress_dialog_stack.append(pd_widget)

    def setProgress(self, step_number):
        pd_widget = self.__class__.progress_dialog_stack[-1]
        pd_widget.setProgress(step_number)

    def destroyProgressDialog(self):
        pd_widget = self.__class__.progress_dialog_stack[-1]
        del self.__class__.progress_dialog_stack[-1]
        pd_widget.hide()
        pd_widget.close()

    def nombreCampos(self, tablename):
        prj = pineboolib.project
        table = prj.tables[tablename]
        campos = [ field.name for field in table.fields ]
        return [len(campos)]+campos

    def addMonths(self, fecha, offset):
        if isinstance(fecha, str) or isinstance(fecha, QtCore.QString):
            fecha = QtCore.QDate.fromString(fecha)
        if not isinstance(fecha, QtCore.QDate):
            print("FATAL: FLUtil.addMonths: No reconozco el tipo de dato %r" % type(fecha))
        return fecha.addMonths(offset)
