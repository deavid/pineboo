from typing import Any, Callable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt5 import QtCore


class IFormDB(object):
    _action: Any
    accept: Any
    actionName_: str
    bottomToolbar: Any
    callInitScript: Any
    child: Callable
    close: Any
    closed: Any
    cursor_: Any
    debugScript: Any
    eventloop: Any
    exportToXml: Callable
    formClosed: Any
    formReady: Any
    iconSize: Any
    idMDI_: Any
    iface: Any
    _loaded: bool
    initFocusWidget_: Any
    initScript: Any
    init_thread_script: None
    isClosing_: None
    layout: Any
    layoutButtons: None
    logger: Any
    loop: bool
    mainWidget_: Any
    name_: None
    oldCursorCtxt: Any
    oldFormObj: Any
    oldFormObjDestroyed: Any
    pushButtonCancel: Any
    pushButtonDebug: None
    reject: Any
    script: Any
    showForDocument: Any
    showed: Optional[bool]
    toolButtonClose: None
    widget: Any
    show: Callable
    main: Callable  # Just for QSA to add here the main() method for execDefaultScript

    __init__: Callable
    # def __init__(self, parent=None, action: Any = None, load=False) -> None:
    #     return

    def accepted(self) -> Any:
        return

    def action(self) -> Any:
        return

    def bindIface(self) -> None:
        return

    def closeEvent(self, e) -> None:
        return

    def cursor(self) -> Any:
        return

    def cursorDestroyed(self, obj_=...) -> None:
        return

    def emitFormClosed(self) -> None:
        return

    def emitFormReady(self) -> None:
        return

    def exec_(self) -> bool:
        return False

    def focusInEvent(self, f) -> None:
        return

    def formClassName(self) -> str:
        return ""

    def formName(self) -> str:
        return ""

    def geoName(self) -> str:
        return ""

    def hide(self) -> None:
        return

    def idMDI(self) -> Optional[str]:
        return ""

    def initForm(self) -> None:
        return

    def initMainWidget(self, w=...) -> None:
        return

    def isIfaceBind(self) -> bool:
        return False

    def load(self) -> None:
        return

    def loadControls(self) -> None:
        return

    def loaded(self) -> bool:
        return False

    def mainWidget(self) -> Any:
        return

    def name(self) -> str:
        return ""

    def saveGeometry(self) -> "QtCore.QByteArray":
        return

    def saveSnapShot(self, path_file=...) -> None:
        return

    def setCaptionWidget(self, text) -> None:
        return

    def setCursor(self, cursor=...) -> None:
        return

    def setIdMDI(self, id_) -> None:
        return

    def setMainWidget(self, w=...) -> None:
        return

    def showEvent(self, e) -> None:
        return

    def snapShot(self) -> Any:
        return

    def unbindIface(self) -> None:
        return
