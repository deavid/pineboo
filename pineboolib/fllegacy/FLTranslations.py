# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.Qt import qWarning, QTranslator, QFile, QTextStream, QDir

from pineboolib import decorators
from pineboolib.fllegacy import FLUtil
from pineboolib.flcontrols import ProjectClass
from pineboolib.utils import filedir


class FLTranslations(ProjectClass):
  
    TML = None
    
    def __init__(self):
        super(FLTRanslations, self).__init__()
    
    @decorators.BetaImplementation  
    def loadTsFile( self, tor, tsFileName, verbose):
        qmFileName = tsFileName
        qmFileName = qmFileName.replace(".ts", "")
        qmFileName = "%n.qm" % qmFileName
        
        ok = tor.load(tsFileName)
        
        if not ok:
            print("lrelease warning: For some reason, I cannot laod '%s'" % tsFileName)
        
        return ok 
    
    @decorators.BetaImplementation   
    def releaseMetaTranslator( self, tor, qmFileName, verbose, stripped):
        if verbose:
            print("Updating '%s'..." % qmFileName)
        
        if not tor.release(qmFileName, verbose, stripped if QTranslator.Stripped else QTranslator.Everything):
            print("lrelease warning: For some reason, i cannot save '%s'" % qmFileName)
        
    
    @decorators.BetaImplementation
    def releaseTsFile( self, tsFileName, verbose, stripped):
        tor = None
        if self.loadTsFile(tor, tsFileName, verbose):
            qmFileName = tsFileName
            qmFileName = qmFileName.replace(".ts", "")
            qmFileName = "%s.qm" % qmFileName
            self.releaseMetaTranslator(tor, qmFileName, verbose, stripped)
            

    @decorators.BetaImplementation
    def lrelease( self, tsInputFile, qmOutputFile, stripped = True):
        util = FLUtil()
        verbose = False
        metTranslations = False
        tor = None
        
        f = QFile(tsInputFile)
        if not f.open(QtCore.QIODevice.ReadOnly):
            print("lrelease error: Cannot open file '%s'" % tsInputFile)
            return
        
        t = QTextStream(f)
        fullText = t.readAll()
        f.close()
        
        if fullText.find("<!DOCTYPE TS>") >= 0:
            if qmOutputFile.isEmpty():
                self.releaseTsFile(tsInputFile, verbose, stripped)
            else:
                self.loadTsFile(tor, tsFileName, verbose)
        
        else:
            modId = self.db_.managerModules().idModuleOfFile(tsInputFile)
            key = util.sqlSelect("flfiles","sha","nombre ='%s'" % tsInputFile)
            dir = filedir("../tempdata/cache/%s/%s/file.ts/%s" %(self.db_.db_name, modId, key))
            tagMap = fullText
            #TODO: hay que cargar todo el contenido del fichero en un diccionario
            for key, value in tagMap:
                toks = value.split(" ")
                
                for t in toks:
                    if key == "TRANSLATIONS":
                        metTranslations = True
                        self.releaseTsFile(t , verbose, stripped)
            
            if not metTranslations:
                print("lrelease warning: Met no 'TRANSLATIONS' entry in project file '%s'" %tsInputFile)
                
            
            if qmOutputFile:
                self.releaseMetaTranslator(tor, qmOutputFile, verbose, stripped)
            
    
    
    
    
    
    
    
    
"""    
****************************************************************************
**
** Copyright (C) 1992-2007 Trolltech ASA. All rights reserved.
**
** This file is part of the Qt Linguist of the Qt Toolkit.
**
** This file may be used under the terms of the GNU General Public
** License version 2.0 as published by the Free Software Foundation
** and appearing in the file LICENSE.GPL included in the packaging of
** this file.  Please review the following information to ensure GNU
** General Public Licensing requirements will be met:
** http://www.trolltech.com/products/qt/opensource.html
**
** If you are unsure which license is appropriate for your use, please
** review the following information:
** http://www.trolltech.com/products/qt/licensing.html or contact the
** sales department at sales@trolltech.com.
**
** This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
** WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
**
****************************************************************************
"""