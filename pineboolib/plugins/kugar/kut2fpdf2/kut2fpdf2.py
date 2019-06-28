# -*- coding: utf-8 -*-

from pineboolib.utils import check_dependencies
import logging

from pineboolib.plugins.kugar.kut2fpdf.kut2fpdf import kut2fpdf


class kut2fpdf2(kut2fpdf):
    def __init__(self):
        super().__init__()

        self.logger = logging.getLogger("kut2fpdf2")
        check_dependencies({"fpdf": "fpdf2"})
