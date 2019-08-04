# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING
from pineboolib.qsa.qsa import *  # noqa: F403
from pineboolib.qsa import qsa

# /** @file */


# /** @class_declaration FormInternalObj */
class FormInternalObj(qsa.FormDBWidget):

    # /** @class_definition FormInternalObj */
    def _class_init(self):
        pass

    # /** @class_definition main */
    def main(self):
        util = qsa.FLUtil()
        if not qsa.sys.isTestEnabled():
            qsa.MessageBox.warning(
                util.translate(
                    "scripts", "La aplicación no se compiló en modo test, por lo que esta opoción no está disponible"
                ),
                qsa.MessageBox.Ok,
                qsa.MessageBox.NoButton,
            )
            return
        util.sqlSelect("tt_test", "idtest", "1 = 1", "tt_test")
        util.sqlSelect("tt_step", "idstep", "1 = 1", "tt_step")
        util.sqlSelect("tt_session", "idsession", "1 = 1", "tt_session")
        dialog = qsa.Dialog()
        dialog.caption = util.translate("scripts", "Lanzar sesión de pruebas")
        dialog.okButtonText = util.translate("scripts", "Lanzar")
        dialog.cancelButtonText = util.translate("scripts", "Cancelar")
        bd = qsa.LineEdit()
        bd.label = util.translate("scripts", "Base de datos")
        dialog.add(bd)
        if not dialog.exec_():
            return
        listaSesiones = qsa.sys.testSessionsList(bd.text)
        if not listaSesiones or listaSesiones == "":
            qsa.MessageBox.critical(
                util.translate("scripts", "Error al obtener la lista de sesiones para la base de datos ") + bd.text,
                qsa.MessageBox.Ok,
                qsa.MessageBox.NoButton,
            )
            return
        sesiones = listaSesiones.split("**")
        sesion = qsa.Input.getItem(util.translate("scripts", "Seleccione sesión"), sesiones)
        if sesion:
            datosSesion = sesion.split("//")
            qsa.sys.startTest(datosSesion[1], datosSesion[0], bd.text)


if TYPE_CHECKING:
    form: FormInternalObj = FormInternalObj()
    iface = form.iface
else:
    form = None
