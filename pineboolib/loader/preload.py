from pineboolib import logging
from typing import Container, Any

logger = logging.getLogger("loader.preload_actions")


def preload_actions(project: Any, forceload: Container = None) -> None:
    """
    Preload actions for warming up the pythonizer cache.

    forceload: When passed an string, it filters and loads all
        actions that match "*forceload*". If None, all actions
        are loaded.
    """
    logger.info("Precarga ...")
    for action in project.actions:
        if forceload and action not in forceload:
            continue
        logger.debug("* * * Cargando acción %s . . . " % action)
        try:
            project.actions[action].load()
        except Exception:
            logger.exception("Failure trying to load action %s", action)
            project.conn.conn.rollback()  # FIXME: Proper transaction handling using with context
        try:
            project.actions[action].loadRecord(None)
        except Exception:
            logger.exception("Failure trying to loadRecord action %s", action)
            project.conn.conn.rollback()  # FIXME: Proper transaction handling using with context
