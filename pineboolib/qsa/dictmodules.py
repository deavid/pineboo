from typing import Any


def from_project(scriptname: str) -> Any:
    """Get script from project."""
    from pineboolib.application.qsadictmodules import QSADictModules

    return QSADictModules.from_project(scriptname)


class Application:
    """
    Emulate QS Application class.

    El modulo "Datos" usa "Application.formRecorddat_procesos" para leer el módulo.
    """

    def __getattr__(self, name: str) -> Any:
        """Emulate any method and retrieve application action module specified."""
        from pineboolib.application.qsadictmodules import QSADictModules

        return QSADictModules.from_project(name)
