from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.fllegacy.flformdb import FLFormDB
    from PyQt5 import QtWidgets


def AQFormDB(action_name: str, parent: "QtWidgets.QWidget") -> "FLFormDB":
    """Return a FLFormDB instance."""

    from pineboolib.application.utils.convert_flaction import convertFLAction
    from pineboolib.application import project

    if project.conn is None:
        raise Exception("Project is not connected yet")

    ac_flaction = project.conn.manager().action(action_name)
    ac_xml = convertFLAction(ac_flaction)
    ac_xml.load()
    ret_ = ac_xml.mainform_widget
    if ret_ is None:
        raise Exception("mainform_widget is emtpy!")
    return ret_
