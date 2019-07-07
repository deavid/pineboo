from pineboolib import logging

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.application.xmlaction import XMLAction
    from pineboolib.fllegacy.flaction import FLAction

logger = logging.getLogger("application.utils.convert_flaction")


def convertFLAction(action: "FLAction") -> "XMLAction":
    from pineboolib.application import project

    if action.name() not in project.actions.keys():
        raise KeyError("Action %s not loaded in current project" % action.name())
    return project.actions[action.name()]


def convert2FLAction(action: "XMLAction") -> "FLAction":
    name = None
    if isinstance(action, str):
        name = str
    else:
        name = action.name

    from pineboolib.application import project

    logger.trace("convert2FLAction: Load action from db manager")
    action = project.conn.manager().action(name)
    logger.trace("convert2FLAction: done")
    return action
