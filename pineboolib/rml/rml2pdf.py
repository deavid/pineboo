# -*- coding: utf-8 -*-

from z3c.rml import document, rml2pdf
from xml import etree
import sys


class parsepdf(object):

    def parse(self, xml, filename):
        res_ = rml2pdf.parseString(xml).read()
        print(xml)
        with open(filename, 'wb') as w:
            w.write(res_)

        w.close()
