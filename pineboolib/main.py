# encoding: UTF-8
import sys
from lxml import etree
from optparse import OptionParser
import psycopg2
import os.path
from PyQt4 import QtGui, QtCore, uic
Qt = QtCore.Qt

def filedir(*path): return os.path.realpath(os.path.join(os.path.dirname(__file__), *path))

class DlgConnect(QtGui.QWidget):
    def load(self):
        self.ui = uic.loadUi(filedir('forms/dlg_connect.ui'), self)

def one(x, default = None):
    try:
        return x[0]
    except IndexError:
        return default
        
class Struct(object):
    "Dummy"

class XMLStruct(Struct):
    def __init__(self, xmlobj):
        if xmlobj is not None:
            self.__name__ = xmlobj.tag
            for child in xmlobj:
                text = child.text
                key = child.tag
                if text: text = text.strip()
                setattr(self, key, text)
                print self.__name__, key, text
    
class Project(object):
    def load(self, filename):
        self.parser = etree.XMLParser(
                        ns_clean=True,
                        encoding="UTF-8",
                        remove_blank_text=True,
                        )
        self.tree = etree.parse(filename, self.parser)
        self.root = self.tree.getroot()
        self.dbserver = XMLStruct(one(self.root.xpath("database-server")))
        self.dbauth = XMLStruct(one(self.root.xpath("database-credentials")))
        self.dbname = XMLStruct(one(self.root.xpath("database-name")))
        self.apppath = one(self.root.xpath("application-path/text()"))
    
    def run(self):
        pass
        
            
def main():
    
    parser = OptionParser()
    parser.add_option("-l", "--load", dest="project",
                      help="load projects/PROJECT.xml and run it", metavar="PROJECT")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")

    (options, args) = parser.parse_args()    
    if not options.project:
        app = QtGui.QApplication(sys.argv)
        w = DlgConnect()
        w.load()
        w.show()
        sys.exit(app.exec_())
    else:
        if not options.project.endswith(".xml"): 
            options.project += ".xml"
        prjpath = filedir("../projects", options.project)
        if not os.path.isfile(prjpath):
            raise ValueError("el proyecto %s no existe." % options.project)
            
        project = Project()
        project.load(prjpath)
        project.run()

