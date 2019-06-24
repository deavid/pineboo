# -*- coding: utf-8 -*-
from pineboolib.qsa import *

# /** @file */

# /** @class_declaration FormInternalObj */
class FormInternalObj(FormDBWidget):

    # /** @class_definition FormInternalObj */
    def _class_init(self):
        pass

    # /** @class_definition main */
    def main(self):
        util = FLUtil()
        if not sys.isTestEnabled():
            MessageBox.warning(
                util.translate("scripts", "La aplicación no se compiló en modo test, por lo que esta opoción no está disponible"),
                MessageBox.Ok,
                MessageBox.NoButton,
            )
            return
        util.sqlSelect("tt_test", "idtest", "1 = 1", "tt_test")
        util.sqlSelect("tt_step", "idstep", "1 = 1", "tt_step")
        util.sqlSelect("tt_session", "idsession", "1 = 1", "tt_session")
        dialog = Dialog()
        dialog.caption = util.translate("scripts", "Lanzar sesión de pruebas")
        dialog.okButtonText = util.translate("scripts", "Lanzar")
        dialog.cancelButtonText = util.translate("scripts", "Cancelar")
        bd = LineEdit()
        bd.label = util.translate("scripts", "Base de datos")
        dialog.add(bd)
        if not dialog.exec_():
            return
        listaSesiones = sys.testSessionsList(bd.text)
        if not listaSesiones or listaSesiones == "":
            MessageBox.critical(
                util.translate("scripts", "Error al obtener la lista de sesiones para la base de datos ") + bd.text, MessageBox.Ok, MessageBox.NoButton
            )
            return
        sesiones = listaSesiones.split("**")
        sesion = Input.getItem(util.translate("scripts", "Seleccione sesión"), sesiones)
        if sesion:
            datosSesion = sesion.split("//")
            sys.startTest(datosSesion[1], datosSesion[0], bd.text)


form = None
