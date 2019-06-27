"""
Contiene Información de cada action del mainForm
"""


class XMLMainFormAction(XMLStruct):
    name = "unnamed"
    text = ""
    mainform = None
    mod = None
    prj = None
    slot = None
    logger = logging.getLogger("main.XMLMainFormAction")

    """
    Lanza la action
    """

    def run(self):
        self.logger.debug("Running: %s %s %s", self.name, self.text, self.slot)
        try:
            action = self.mod.actions[self.name]
            getattr(action, self.slot, "unknownSlot")()
        finally:
            self.logger.debug("END of Running: %s %s %s", self.name, self.text, self.slot)


"""
Contiene información de las actions especificadas en el .xml del módulo
"""


class XMLAction(XMLStruct):
    logger = logging.getLogger("main.XMLAction")

    """
    Constructor
    """

    def __init__(self, *args, **kwargs) -> None:
        super(XMLAction, self).__init__(*args, **kwargs)
        self.form = self._v("form")
        self.name = self._v("name")
        self.script = self._v("script")  # script_form_record
        self.table = self._v("table")
        self.mainform = self._v("mainform")
        self.mainscript = self._v("mainscript")  # script_form
        self.formrecord = self._v("formrecord")  # form_record
        self.mainform_widget = None
        self.formrecord_widget = None
        self._loaded = False

    """
    Carga FLFormRecordDB por defecto
    @param cursor. Asigna un cursor al FLFormRecord
    @return widget con form inicializado
    """

    def loadRecord(self, cursor: None) -> FLFormRecordDB:
        self._loaded = getattr(self.formrecord_widget, "_loaded", False)
        if not self._loaded:
            if getattr(self.formrecord_widget, "widget", None):
                self.formrecord_widget.widget.doCleanUp()
                # self.formrecord_widget.widget = None

            self.logger.debug("Loading record action %s . . . ", self.name)
            if pineboolib.project._DGI.useDesktop():
                self.formrecord_widget = pineboolib.project.conn.managerModules().createFormRecord(self, None, cursor, None)
            else:
                # self.script = getattr(self, "script", None)
                # if isinstance(self.script, str) or self.script is None:
                self.load_script(self.scriptformrecord, None)
                self.formrecord_widget = self.script.form
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

    def load(self) -> FLFormDB:
        self._loaded = getattr(self.mainform_widget, "_loaded", False)
        if not self._loaded:
            if getattr(self.mainform_widget, "widget", None):
                self.mainform_widget.widget.doCleanUp()
            self.logger.debug("Loading action %s . . . ", self.name)
            if pineboolib.project._DGI.useDesktop() and hasattr(pineboolib.project.main_window, "w_"):
                self.mainform_widget = pineboolib.project.conn.managerModules().createForm(self, None, pineboolib.project.main_window.w_, None)
            else:
                self.scriptform = getattr(self, "scriptform", None)
                self.load_script(self.scriptform, None)
                self.mainform_widget = self.script.form
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

    def execMainScript(self, name):
        a = pineboolib.project.conn.manager().action(name)
        if not a:
            self.logger.warning("No existe la acción %s", name)
            return True
        pineboolib.project.call("%s.main" % a.name(), [], None, False)

    """
    Retorna el widget del formRecord. Esto es necesario porque a veces no hay un FLformRecordDB inicialidado todavía
    @return wigdet del formRecord.
    """

    def formRecordWidget(self) -> FLFormRecordDB:
        if not getattr(self.formrecord_widget, "_loaded", None):
            self.loadRecord(None)

        return self.formrecord_widget

    """
    Abre el FLFormRecordDB por defecto
    @param cursor. Cursor a usar por el FLFormRecordDB
    """

    def openDefaultFormRecord(self, cursor):
        self.logger.info("Opening default formRecord for Action %s", self.name)
        w = self.loadRecord(cursor)
        # w.init()
        if w:
            if pineboolib.project._DGI.localDesktop():
                w.show()

    def openDefaultForm(self):
        self.logger.info("Opening default form for Action %s", self.name)
        w = self.load()

        if w:
            if pineboolib.project._DGI.localDesktop():
                w.show()

    """
    Ejecuta el script por defecto
    """

    def execDefaultScript(self):
        self.logger.info("Executing default script for Action %s", self.name)
        self.scriptform = getattr(self, "scriptform", None)
        self.load_script(self.scriptform, None)

        self.mainform_widget = self.script.form
        if self.mainform_widget.iface:
            self.mainform_widget.iface.main()
        else:
            self.mainform_widget.main()

    """
    Convierte un script qsa en .py y lo carga
    @param scriptname. Nombre del script a convertir
    @param parent. Objecto al que carga el script, si no se especifica es a self.script
    """

    def load_script(self, scriptname: str, parent: Optional[Union[FLFormDB, FLFormRecordDB]] = None) -> None:
        from importlib import machinery

        if scriptname:
            scriptname = scriptname.replace(".qs", "")
        # if scriptname:
        #    self.logger.info("Cargando script %s de %s accion %s", scriptname, parent, self.name)

        parent_ = parent
        if parent is None:
            parent = self
            action_ = self
        else:
            action_ = parent._action if hasattr(parent, "_action") else self

            # import aqui para evitar dependencia ciclica
        from pineboolib.utils import convertFLAction

        if not isinstance(action_, XMLAction):
            action_ = convertFLAction(action_)

        python_script_path = None
        # primero default, luego sobreescribimos
        from pineboolib import emptyscript

        parent.script = emptyscript

        if scriptname is None:
            parent.script.form = parent.script.FormInternalObj(action=action_, project=pineboolib.project, parent=parent)
            parent.widget = parent.script.form
            parent.iface = parent.widget.iface
            return

        script_path_py = pineboolib.project._DGI.alternative_script_path("%s.py" % scriptname)

        if script_path_py is None:
            script_path_qs = _path("%s.qs" % scriptname, False)
            script_path_py = coalesce_path("%s.py" % scriptname, "%s.qs.py" % scriptname, None)

        mng_modules = pineboolib.project.conn.managerModules()
        if mng_modules.staticBdInfo_ and mng_modules.staticBdInfo_.enabled_:
            from pineboolib.fllegacy.flmodulesstaticloader import FLStaticLoader

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
                self.logger.info("Cargando %s : %s ", scriptname, script_path.replace(pineboolib.project.tmpdir, "tempdata"))
                parent.script = machinery.SourceFileLoader(scriptname, script_path).load_module()
            except Exception:
                self.logger.exception("ERROR al cargar script PY para la accion %s:", action_.name)

        elif script_path_qs:
            script_path = script_path_qs
            pineboolib.project.parseScript(script_path)
            self.logger.info("Loading script QS %s . . . ", scriptname)
            python_script_path = (script_path + ".xml.py").replace(".qs.xml.py", ".qs.py")
            try:
                self.logger.info("Cargando %s : %s ", scriptname, python_script_path.replace(pineboolib.project.tmpdir, "tempdata"))
                parent.script = machinery.SourceFileLoader(scriptname, python_script_path).load_module()
            except Exception:
                self.logger.exception("ERROR al cargar script QS para la accion %s:", action_.name)

        parent.script.form = parent.script.FormInternalObj(action_, pineboolib.project, parent_)
        if parent_:
            parent.widget = parent.script.form
            if getattr(parent.widget, "iface", None):
                parent.iface = parent.widget.iface

        return

    def unknownSlot(self):
        self.logger.error("Executing unknown script for Action %s", self.name)
