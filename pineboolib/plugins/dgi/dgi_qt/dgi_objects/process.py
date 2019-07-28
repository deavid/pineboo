# -*- coding: utf-8 -*-

from PyQt5 import QtCore  # type: ignore
from PyQt5.QtCore import pyqtSignal
import sys
from typing import Any, List, cast, Optional, Iterable
from pineboolib.core import decorators


class Process(QtCore.QProcess):

    stderr = None
    stdout = None

    def __init__(self, *args) -> None:
        super(Process, self).__init__()
        cast(pyqtSignal, self.readyReadStandardOutput).connect(self.stdoutReady)
        cast(pyqtSignal, self.readyReadStandardError).connect(self.stderrReady)
        self.stderr = None
        self.normalExit = self.NormalExit
        self.crashExit = self.CrashExit

        if args:
            self.setProgram(args[0])
            argumentos = args[1:]
            self.setArguments(argumentos)

    def start(self, *args: Any) -> None:
        super(Process, self).start()

    def stop(self) -> None:
        super(Process, self).stop()

    def writeToStdin(self, stdin_) -> None:
        encoding = sys.getfilesystemencoding()
        stdin_as_bytes = stdin_.encode(encoding)
        self.writeData(stdin_as_bytes)
        # self.closeWriteChannel()

    @decorators.pyqtSlot()
    def stdoutReady(self) -> None:
        self.stdout = str(self.readAllStandardOutput())

    @decorators.pyqtSlot()
    def stderrReady(self) -> None:
        self.stderr = str(self.readAllStandardError())

    def readStderr(self) -> Any:
        return self.stderr

    def readStdout(self) -> Any:
        return self.stdout

    def getWorkingDirectory(self) -> Any:
        return super(Process, self).workingDirectory()

    def setWorkingDirectory(self, wd) -> None:
        super(Process, self).setWorkingDirectory(wd)

    def getIsRunning(self) -> bool:
        return self.state() in (self.Running, self.Starting)

    def exitcode(self) -> Any:
        return self.exitCode()

    @staticmethod
    def executeNoSplit(
        comando: list, stdin_buffer
    ) -> None:  # FIXME: aquí hay otro problema parecido a File, que se llama inicializado y sin inicializar

        list_ = []
        for c in comando:
            list_.append(c)

        pro = QtCore.QProcess()
        programa = list_[0]
        arguments = list_[1:]
        pro.setProgram(programa)
        pro.setArguments(arguments)
        pro.start()
        encoding = sys.getfilesystemencoding()
        stdin_as_bytes = stdin_buffer.encode(encoding)
        pro.writeData(stdin_as_bytes)
        pro.waitForFinished(30000)
        Process.stdout = pro.readAllStandardOutput().data().decode(encoding)
        Process.stderr = pro.readAllStandardError().data().decode(encoding)

    @staticmethod
    def execute(
        comando: str, arguments: Optional[Iterable[str]] = None
    ) -> int:  # FIXME: aquí hay otro problema parecido a File, que se llama inicializado y sin inicializar
        import sys

        encoding = sys.getfilesystemencoding()
        pro = QtCore.QProcess()
        from pineboolib.application import types

        comando_: List[str] = []
        if isinstance(comando, list):
            comando_ = comando

        if isinstance(comando, types.Array):
            comando = str(comando)

        if isinstance(comando, str):
            comando_ = comando.split(" ")

        programa = comando_[0]
        argumentos = comando_[1:]
        pro.setProgram(programa)
        pro.setArguments(argumentos)
        pro.start()
        pro.waitForFinished(30000)
        Process.stdout = pro.readAllStandardOutput().data().decode(encoding)
        Process.stderr = pro.readAllStandardError().data().decode(encoding)
        return 0  # FIXME: Probably we need to return the exit code

    running = property(getIsRunning)
    workingDirectory = property(
        getWorkingDirectory, setWorkingDirectory
    )  # type: ignore
