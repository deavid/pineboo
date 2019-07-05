# -*- coding: utf-8 -*-
# pytype: skip-file
# type: ignore
from typing import Tuple


pluginType = MODULE  # noqa  # La constante MODULE es parte de cómo PyQt carga los plugins. Es insertada por el loader en el namespace local


def moduleInformation() -> Tuple[str, str]:
    return "pineboolib.pncontrolsfactory", ("FLTable")
