# -*- coding: utf-8 -*-
import time
import os
import logging


import pineboolib
from pineboolib.utils import XMLStruct, parseTable, _path, coalesce_path, _dir

# from pineboolib.fllegacy.flutil import FLUtil  # FIXME: Not allowed at this level yet
# from pineboolib.fllegacy.flsettings import FLSettings

# Solo para tipos de dato
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.flformdb import FLFormDB
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.flformrecorddb import FLFormRecordDB
from typing import Callable, Optional, Union
