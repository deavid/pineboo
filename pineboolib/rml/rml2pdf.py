# -*- coding: utf-8 -*-
import pineboolib
from xml import etree
import sys


class parsepdf(object):

    def parse(self, xml, filename):
        print(pineboolib.project._DGI.isDeployed())
        if not pineboolib.project._DGI.isDeployed():
            from z3c.rml import document, rml2pdf
        else:
            return

        res_ = rml2pdf.parseString(xml).read()
        with open(filename, 'wb') as w:
            w.write(res_)

        w.close()
