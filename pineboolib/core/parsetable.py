from pineboolib import logging
from .utils.utils_base import getTableObj

from pineboolib.core.utils.utils_base import Struct

logger = logging.getLogger("core.parsetable")


def parseTable(nombre: str, contenido: str, encoding: str = "UTF-8", remove_blank_text: bool = True) -> Struct:
    # FIXME: parseTable is something too specific to be in utils.py
    from io import StringIO
    from xml import etree

    file_alike = StringIO(contenido)
    try:
        tree = etree.ElementTree.parse(file_alike)
    except Exception:
        logger.exception("Error al procesar tabla: %s", nombre)
        return None

    root = tree.getroot()
    obj_name = root.find("name")
    query = root.find("query")
    if query:
        if query.text != nombre:
            logger.warning(
                "WARN: Nombre de query %s no coincide con el nombre declarado en el XML %s (se prioriza el nombre de query)"
                % (obj_name.text, nombre)
            )
            query.text = nombre
    elif obj_name.text != nombre:
        logger.warning(
            "WARN: Nombre de tabla %s no coincide con el nombre declarado en el XML %s (se prioriza el nombre de tabla)"
            % (obj_name.text, nombre)
        )
        obj_name.text = nombre
    return getTableObj(tree, root)
