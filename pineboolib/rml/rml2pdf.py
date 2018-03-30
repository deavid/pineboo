# -*- coding: utf-8 -*-

from z3c.rml import rml2pdf
import sys


class rml2pdf(object):

    def parse(self, text, filename):
        pdf = parseString(text)

        with open(filename, 'w') as pdfFile:
            pdfFile.write(pdf.read())
