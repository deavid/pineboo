from typing import Tuple

# -*- coding: utf-8 -*-

pluginType = MODULE  # noqa  # La constante MODULE es parte de cómo PyQt carga los plugins. Es insertada por el loader en el namespace local


def moduleInformation() -> Tuple[str, str]:
    return "pineboolib.fllegacy.fltabledb", ("FLTableDB")
