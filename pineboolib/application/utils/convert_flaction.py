"""Converter to and from FLAction."""

from pineboolib.core.utils import logging

from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.application.xmlaction import XMLAction
    from pineboolib.fllegacy.flaction import FLAction

logger = logging.getLogger("application.utils.convert_flaction")


def convertFLAction(action: "FLAction") -> "XMLAction":
    """
    Convert a FLAction to XMLAction.

    @param action. FLAction object.
    @return XMLAction object.
    """

    from pineboolib.application import project

    if action.name() not in project.actions.keys():
        raise KeyError("Action %s not loaded in current project" % action.name())
    return project.actions[action.name()]


def convert2FLAction(action: Union[str, "XMLAction"]) -> "FLAction":
    """
    Convert a XMLAction to FLAction.

    @param action. XMLAction object.
    @return FLAction object.
    """

    if isinstance(action, str):
        name = action
    else:
        name = action.name

    from pineboolib.application import project

    if project.conn is None:
        raise Exception("Project is not connected yet")

    logger.trace("convert2FLAction: Load action from db manager")
    flaction = project.conn.manager().action(name)
    logger.trace("convert2FLAction: done")
    return flaction
