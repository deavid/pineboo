import pineboolib
import logging

from pineboolib.application.xmlaction import XMLAction
from pineboolib.fllegacy.flaction import FLAction

logger = logging.getLogger("application.utils.convert_flaction")


def convertFLAction(action: FLAction) -> XMLAction:
    if action.name() in pineboolib.project.actions.keys():
        return pineboolib.project.actions[action.name()]
    else:
        return None


def convert2FLAction(action: XMLAction) -> FLAction:
    name = None
    if isinstance(action, str):
        name = str
    else:
        name = action.name

    from pineboolib.pncontrolsfactory import aqApp

    logger.trace("convert2FLAction: Load action from db manager")
    action = aqApp.db().manager().action(name)
    logger.trace("convert2FLAction: done")
    return action
