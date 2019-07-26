from pineboolib.core.utils import logging
import os.path

from pineboolib.core.utils.struct import XMLStruct
from .utils.path import _path, coalesce_path

from typing import Optional, Any, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.fllegacy.flaction import FLAction  # noqa: F401
    from pineboolib.plugins.dgi.dgi_qt.dgi_objects.flformdb import FLFormDB
    from pineboolib.plugins.dgi.dgi_qt.dgi_objects.flformrecorddb import FLFormRecordDB
    from .moduleactions import ModuleActions  # noqa: F401
    from .database.pnsqlcursor import PNSqlCursor  # noqa: F401


class XMLAction(XMLStruct):
    """
    Contiene información de las actions especificadas en el .xml del módulo
    """

    logger = logging.getLogger("main.XMLAction")
    mod: Optional["ModuleActions"]
    alias: str

    def __init__(self, *args, project, name=None, **kwargs) -> None:
        """
        Constructor
        """
        super(XMLAction, self).__init__(*args, **kwargs)
        self.mod = None
        self.project = project
        if not self.project:
            raise ValueError("XMLActions must belong to a project")
        self.form = self._v("form")
        self.name = name or self._rv("name")  # Mandatory
        self.description = self._v("description")
        self.scriptform = self._v("scriptform")
        self.table = self._v("table")
        self.mainform = self._v("mainform")
        self.mainscript = self._v("mainscript")
        self.formrecord = self._v("formrecord")
        self.scriptformrecord = self._v("scriptformrecord")
        self.mainform_widget: Optional[FLFormDB] = None
        self.formrecord_widget: Optional[FLFormRecordDB] = None
        self._loaded = False

    """
    Carga FLFormRecordDB por defecto
    @param cursor. Asigna un cursor al FLFormRecord
    @return widget con form inicializado
    """

    def loadRecord(self, cursor: Optional["PNSqlCursor"]) -> "FLFormRecordDB":
        self._loaded = getattr(self.formrecord_widget, "_loaded", False)
        if not self._loaded:
            if self.formrecord_widget and getattr(self.formrecord_widget, "widget", None):
                self.formrecord_widget.widget.doCleanUp()
                # self.formrecord_widget.widget = None

            self.logger.debug("Loading record action %s . . . ", self.name)
            if self.project.DGI.useDesktop():
                # FIXME: looks like code duplication. Bet both sides of the IF do the same.
                self.formrecord_widget = self.project.conn.managerModules().createFormRecord(self, None, cursor, None)
            else:
                # self.script = getattr(self, "script", None)
                # if isinstance(self.script, str) or self.script is None:
                script = self.load_script(self.scriptformrecord, None)
                self.formrecord_widget = script.form
                if self.formrecord_widget is None:
                    raise Exception("After loading script, no form was loaded")
                self.formrecord_widget.widget = self.formrecord_widget
                self.formrecord_widget.iface = self.formrecord_widget.widget.iface
                self.formrecord_widget._loaded = True
            # self.formrecord_widget.setWindowModality(Qt.ApplicationModal)
            self.logger.debug(
                "End of record action load %s (iface:%s ; widget:%s)",
                self.name,
                getattr(self.formrecord_widget, "iface", None),
                getattr(self.formrecord_widget, "widget", None),
            )
        if self.formrecord_widget is None:
            raise Exception("Unexpected: No formrecord loaded")

        if cursor:
            self.formrecord_widget.setCursor(cursor)

        return self.formrecord_widget

    def load(self) -> "FLFormDB":
        self._loaded = getattr(self.mainform_widget, "_loaded", False)
        if not self._loaded:
            if self.mainform_widget is not None and getattr(self.mainform_widget, "widget", None):
                self.mainform_widget.widget.doCleanUp()
            if self.project.DGI.useDesktop() and hasattr(self.project.main_window, "w_"):
                self.logger.info("Loading action %s (createForm). . . ", self.name)
                self.mainform_widget = self.project.conn.managerModules().createForm(action=self, parent=self.project.main_window.w_)
            else:
                self.logger.info("Loading action %s (load_script %s). . . ", self.name, self.scriptform)
                script = self.load_script(self.scriptform, None)
                self.mainform_widget = script.form  # FormDBWidget FIXME: Add interface for types
                if self.mainform_widget is None:
                    raise Exception("After loading script, no form was loaded")
                self.mainform_widget.widget = self.mainform_widget
                self.mainform_widget.iface = self.mainform_widget.widget.iface
                self.mainform_widget._loaded = True

            self.logger.debug(
                "End of action load %s (iface:%s ; widget:%s)",
                self.name,
                getattr(self.mainform_widget, "iface", None),
                getattr(self.mainform_widget, "widget", None),
            )
        if self.mainform_widget is None:
            raise Exception("Unexpected: No form loaded")

        return self.mainform_widget

    """
    Llama a la función main de una action
    """

    def execMainScript(self, name) -> None:
        a = self.project.conn.manager().action(name)
        if not a:
            self.logger.warning("No existe la acción %s", name)
            return
        self.project.call("%s.main" % a.name(), [], None, False)

    """
    Retorna el widget del formRecord. Esto es necesario porque a veces no hay un FLformRecordDB inicialidado todavía
    @return wigdet del formRecord.
    """

    def formRecordWidget(self) -> "FLFormRecordDB":
        if not getattr(self.formrecord_widget, "_loaded", None):
            self.loadRecord(None)

        if self.formrecord_widget is None:
            raise Exception("Unexpected: No form loaded")
        return self.formrecord_widget

    """
    Abre el FLFormRecordDB por defecto
    @param cursor. Cursor a usar por el FLFormRecordDB
    """
    # FIXME: cursor is FLSqlCursor but should be something core, not "FL". Also, an interface
    def openDefaultFormRecord(self, cursor: "PNSqlCursor", wait: bool = True) -> None:
        self.logger.info("Opening default formRecord for Action %s", self.name)
        w = self.loadRecord(cursor)
        # w.init()
        if w:
            if self.project.DGI.localDesktop():
                if wait:
                    w.show_and_wait()
                else:
                    w.show()

    def openDefaultForm(self) -> None:
        self.logger.info("Opening default form for Action %s", self.name)
        w = self.load()

        if w:
            if self.project.DGI.localDesktop():
                w.show()

    """
    Ejecuta el script por defecto
    """

    def execDefaultScript(self) -> None:
        self.logger.info("Executing default script for Action %s", self.name)
        script = self.load_script(self.scriptform, None)

        self.mainform_widget = script.form
        if self.mainform_widget is None:
            raise Exception("Unexpected: No form loaded")

        if self.mainform_widget.iface:
            self.mainform_widget.iface.main()
        else:
            self.mainform_widget.main()

    """
    Convierte un script qsa en .py y lo carga
    @param scriptname. Nombre del script a convertir
    @param parent. Objecto al que carga el script, si no se especifica es a self.script
    """

    def load_script(self, scriptname: Optional[str], parent: Optional["FLFormDB"] = None) -> Any:  # returns loaded script
        # FIXME: Parent logic is broken. We're loading scripts to two completely different objects.
        from importlib import machinery

        if scriptname:
            scriptname = scriptname.replace(".qs", "")
            self.logger.debug("Loading script %s of %s for action %s", scriptname, parent, self.name)
        else:
            self.logger.info("No script to load on %s for action %s", parent, self.name)

        parent_object = parent
        action_: Union[XMLAction, "FLAction"]  # XMLAction / FLAction
        if parent is None:
            action_ = self
        else:
            possible_flaction_ = getattr(parent, "_action", None)
            if not isinstance(possible_flaction_, XMLAction):
                from .utils.convert_flaction import convertFLAction  # type: ignore

                action_ = convertFLAction(possible_flaction_)
            elif possible_flaction_ is not None:
                action_ = possible_flaction_

        python_script_path = None
        # primero default, luego sobreescribimos
        from pineboolib.qsa import emptyscript  # type: ignore

        script_loaded: Any = emptyscript

        if scriptname is None:
            script_loaded.form = script_loaded.FormInternalObj(action=action_, project=self.project, parent=parent_object)
            if parent:
                parent.widget = script_loaded.form
                parent.iface = parent.widget.iface
            return script_loaded

        script_path_py = self.project.DGI.alternative_script_path("%s.py" % scriptname)

        if script_path_py is None:
            script_path_qs = _path("%s.qs" % scriptname, False)
            script_path_py = coalesce_path("%s.py" % scriptname, "%s.qs.py" % scriptname, None)

        mng_modules = self.project.conn.managerModules()
        if mng_modules.staticBdInfo_ and mng_modules.staticBdInfo_.enabled_:
            from pineboolib.fllegacy.flmodulesstaticloader import FLStaticLoader  # FIXME

            ret_py = FLStaticLoader.content("%s.qs.py" % scriptname, mng_modules.staticBdInfo_, True)  # Con True solo devuelve el path
            if ret_py:
                script_path_py = ret_py
            else:
                ret_qs = FLStaticLoader.content("%s.qs" % scriptname, mng_modules.staticBdInfo_, True)  # Con True solo devuelve el path
                if ret_qs:
                    script_path_qs = ret_qs

        if script_path_py is not None:
            script_path = script_path_py
            self.logger.info("Loading script PY %s . . . ", scriptname)
            if not os.path.isfile(script_path):
                raise IOError
            try:
                self.logger.debug("Cargando %s : %s ", scriptname, script_path.replace(self.project.tmpdir, "tempdata"))
                loader = machinery.SourceFileLoader(scriptname, script_path)
                script_loaded = loader.load_module()  # type: ignore
            except Exception:
                self.logger.exception("ERROR al cargar script PY para la accion %s:", action_.name)

        elif script_path_qs:
            script_path = script_path_qs
            self.project.parseScript(script_path)
            self.logger.info("Loading script QS %s . . . ", scriptname)
            python_script_path = (script_path + ".xml.py").replace(".qs.xml.py", ".qs.py")
            try:
                self.logger.debug("Cargando %s : %s ", scriptname, python_script_path.replace(self.project.tmpdir, "tempdata"))
                loader = machinery.SourceFileLoader(scriptname, python_script_path)
                script_loaded = loader.load_module()  # type: ignore
            except Exception:
                self.logger.exception("ERROR al cargar script QS para la accion %s:", action_.name)

        script_loaded.form = script_loaded.FormInternalObj(action_, self.project, parent_object)
        if parent_object and parent:
            parent_object.widget = script_loaded.form
            if getattr(parent_object.widget, "iface", None):
                parent_object.iface = parent.widget.iface

        return script_loaded

    def unknownSlot(self) -> None:
        self.logger.error("Executing unknown script for Action %s", self.name)
