# -*- coding: utf-8 -*-

from PyQt5 import QtCore

class Process(QtCore.QProcess):

    stderr = None
    stdout = None

    def __init__(self, *args):
        super(Process, self).__init__()
        self.readyReadStandardOutput.connect(self.stdoutReady)
        self.readyReadStandardError.connect(self.stderrReady)
        self.stderr = None
        self.normalExit = self.NormalExit
        self.crashExit = self.CrashExit
        
        if args:
            self.setProgram(args[0])
            argumentos = args[1:]
            self.setArguments(argumentos)

    def start(self):
        super(Process, self).start()

    def stop(self):
        super(Process, self).stop()

    def writeToStdin(self, stdin_):
        import sys
        encoding = sys.getfilesystemencoding()
        stdin_as_bytes = stdin_.encode(encoding)
        self.writeData(stdin_as_bytes)
        # self.closeWriteChannel()

    def stdoutReady(self):
        self.stdout = str(self.readAllStandardOutput())

    def stderrReady(self):
        self.stderr = str(self.readAllStandardError())

    def readStderr(self):
        return self.stderr

    def getWorkingDirectory(self):
        return super(Process, self).workingDirectory()

    def setWorkingDirectory(self, wd):
        super(Process, self).setWorkingDirectory(wd)

    def getIsRunning(self):
        return self.state() in (self.Running, self.Starting)
    
    def exitcode(self):
        return self.exitCode()

    def execute(comando):
        import sys
        encoding = sys.getfilesystemencoding()
        pro = QtCore.QProcess()
        if isinstance(comando, str):
            comando = comando.split(" ")

        programa = comando[0]
        argumentos = comando[1:]
        pro.setProgram(programa)
        pro.setArguments(argumentos)
        pro.start()
        pro.waitForFinished(30000)
        Process.stdout = pro.readAllStandardOutput().data().decode(encoding)
        Process.stderr = pro.readAllStandardError().data().decode(encoding)

    running = property(getIsRunning)
    workingDirectory = property(getWorkingDirectory, setWorkingDirectory)