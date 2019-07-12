from pineboolib.core.utils import logging
import os.path

from pineboolib.core.utils.struct import XMLStruct
from .utils.path import _path, coalesce_path

from typing import Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.interfaces import IFormDB, IFormRecordDB


class XMLMainFormAction(XMLStruct):
    """
    Contiene Información de cada action del mainForm
    """

    name = "unnamed"
    text = ""
    mainform = None
    mod: Any = None
    prj = None
    slot = None
    logger = logging.getLogger("main.XMLMainFormAction")

    def run(self) -> None:
        """
        Lanza la action
        """
        if self.mod is None:
            raise Exception("No module set")
        self.logger.debug("Running: %s %s %s", self.name, self.text, self.slot)
        try:
            action = self.mod.actions[self.name]
            getattr(action, self.slot, "unknownSlot")()
        finally:
            self.logger.debug("END of Running: %s %s %s", self.name, self.text, self.slot)


class XMLAction(XMLStruct):
    """
    Contiene información de las actions especificadas en el .xml del módulo
    """

    logger = logging.getLogger("main.XMLAction")

    def __init__(self, *args, project, name=None, **kwargs) -> None:
        """
        Constructor
        """
        super(XMLAction, self).__init__(*args, **kwargs)
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
        self.mainform_widget: IFormDB = None
        self.formrecord_widget: IFormDB = None
        self._loaded = False

    """
    Carga FLFormRecordDB por defecto
    @param cursor. Asigna un cursor al FLFormRecord
    @return widget con form inicializado
    """

    def loadRecord(self, cursor: None) -> "IFormRecordDB":
        self._loaded = getattr(self.formrecord_widget, "_loaded", False)
        if not self._loaded:
            if getattr(self.formrecord_widget, "widget", None):
                self.formrecord_widget.widget.doCleanUp()
                # self.formrecord_widget.widget = None

            self.logger.debug("Loading record action %s . . . ", self.name)
            if self.project._DGI.useDesktop():
                # FIXME: looks like code duplication. Bet both sides of the IF do the same.
                self.formrecord_widget = self.project.conn.managerModules().createFormRecord(self, None, cursor, None)
            else:
                # self.script = getattr(self, "script", None)
                # if isinstance(self.script, str) or self.script is None:
                script = self.load_script(self.scriptformrecord, None)
                self.formrecord_widget = script.form
                self.formrecord_widget.widget = self.formrecord_widget
                self.formrecord_widget.iface = self.formrecord_widget.widget.iface
                self.formrecord_widget._loaded = True
            # self.formrecord_widget.setWindowModality(Qt.ApplicationModal)
            if self.formrecord_widget:
                self.logger.debug(
                    "End of record action load %s (iface:%s ; widget:%s)",
                    self.name,
                    getattr(self.formrecord_widget, "iface", None),
                    getattr(self.formrecord_widget, "widget", None),
                )

        if cursor and self.formrecord_widget:
            self.formrecord_widget.setCursor(cursor)

        return self.formrecord_widget

    def load(self) -> "IFormDB":
        self._loaded = getattr(self.mainform_widget, "_loaded", False)
        if not self._loaded:
            if getattr(self.mainform_widget, "widget", None):
                self.mainform_widget.widget.doCleanUp()
            if self.project._DGI.useDesktop() and hasattr(self.project.main_window, "w_"):
                self.logger.info("Loading action %s (createForm). . . ", self.name)
                self.mainform_widget = self.project.conn.managerModules().createForm(action=self, parent=self.project.main_window.w_)
            else:
                self.logger.info("Loading action %s (load_script %s). . . ", self.name, self.scriptform)
                script = self.load_script(self.scriptform, None)
                self.mainform_widget = script.form  # FormDBWidget FIXME: Add interface for types
                self.mainform_widget.widget = self.mainform_widget
                self.mainform_widget.iface = self.mainform_widget.widget.iface
                self.mainform_widget._loaded = True

            self.logger.debug(
                "End of action load %s (iface:%s ; widget:%s)",
                self.name,
                getattr(self.mainform_widget, "iface", None),
                getattr(self.mainform_widget, "widget", None),
            )

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

    def formRecordWidget(self) -> "IFormRecordDB":
        if not getattr(self.formrecord_widget, "_loaded", None):
            self.loadRecord(None)

        return self.formrecord_widget

    """
    Abre el FLFormRecordDB por defecto
    @param cursor. Cursor a usar por el FLFormRecordDB
    """
    # FIXME: cursor is FLSqlCursor but should be something core, not "FL". Also, an interface
    def openDefaultFormRecord(self, cursor: Any, wait: bool = True) -> None:
        self.logger.info("Opening default formRecord for Action %s", self.name)
        w = self.loadRecord(cursor)
        # w.init()
        if w:
            if self.project._DGI.localDesktop():
                if wait:
                    w.show_and_wait()
                else:
                    w.show()

    def openDefaultForm(self) -> None:
        self.logger.info("Opening default form for Action %s", self.name)
        w = self.load()

        if w:
            if self.project._DGI.localDesktop():
                w.show()

    """
    Ejecuta el script por defecto
    """

    def execDefaultScript(self) -> None:
        self.logger.info("Executing default script for Action %s", self.name)
        script = self.load_script(self.scriptform, None)

        self.mainform_widget = script.form
        if self.mainform_widget.iface:
            self.mainform_widget.iface.main()
        else:
            self.mainform_widget.main()

    """
    Convierte un script qsa en .py y lo carga
    @param scriptname. Nombre del script a convertir
    @param parent. Objecto al que carga el script, si no se especifica es a self.script
    """

    def load_script(self, scriptname: str, parent: Optional["IFormDB"] = None) -> Any:  # returns loaded script
        # FIXME: Parent logic is broken. We're loading scripts to two completely different objects.
        from importlib import machinery

        if scriptname:
            scriptname = scriptname.replace(".qs", "")
            self.logger.debug("Loading script %s of %s for action %s", scriptname, parent, self.name)
        else:
            self.logger.info("No script to load on %s for action %s", parent, self.name)

        parent_object = parent
        if parent is None:
            action_ = self
        else:
            action_ = parent._action if hasattr(parent, "_action") else self

        # import aqui para evitar dependencia ciclica
        from .utils.convert_flaction import convertFLAction  # type: ignore

        if not isinstance(action_, XMLAction):
            action_ = convertFLAction(action_)

        python_script_path = None
        # primero default, luego sobreescribimos
        from pineboolib.qsa import emptyscript  # type: ignore

        script_loaded = emptyscript

        if scriptname is None:
            script_loaded.form = script_loaded.FormInternalObj(action=action_, project=self.project, parent=parent_object)
            if parent:
                parent.widget = script_loaded.form
                parent.iface = parent.widget.iface
            return script_loaded

        script_path_py = self.project._DGI.alternative_script_path("%s.py" % scriptname)

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
        if parent_object:
            parent_object.widget = script_loaded.form
            if getattr(parent_object.widget, "iface", None):
                parent_object.iface = parent.widget.iface

        return script_loaded

    def unknownSlot(self) -> None:
        self.logger.error("Executing unknown script for Action %s", self.name)
