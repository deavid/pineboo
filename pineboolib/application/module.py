class Module(object):
    """
    Esta clase almacena la información de los módulos cargados
    """

    """
    Constructor
    @param areaid. Identificador de area.
    @param name. Nombre del módulo
    @param description. Descripción del módulo
    @param icon. Icono del módulo
    """

    def __init__(self, areaid: str, name: str, description: str, icon: str) -> None:
        self.areaid = areaid
        self.name = name
        self.description = description  # En python2 era .decode(UTF-8)
        self.icon = icon
        self.files = {}
        self.tables = {}
        self.loaded = False
        self.path = pineboolib.project.path
        self.logger = logging.getLogger("main.Module")

    """
    Añade ficheros al array que controla que ficehros tengo.
    @param fileobj. Objeto File con información del fichero
    """

    def add_project_file(self, fileobj: File) -> None:
        self.files[fileobj.filename] = fileobj

    """
    Carga las acciones pertenecientes a este módulo
    @return Boolean. True si ok, False si hay problemas
    """

    def load(self) -> bool:
        pathxml = _path("%s.xml" % self.name)
        # pathui = _path("%s.ui" % self.name)
        if pathxml is None:
            self.logger.error("módulo %s: fichero XML no existe", self.name)
            return False
        # if pathui is None:
        #    self.logger.error("módulo %s: fichero UI no existe", self.name)
        #    return False
        if pineboolib.project._DGI.useDesktop() and pineboolib.project._DGI.localDesktop():
            tiempo_1 = time.time()
        try:
            self.actions = ModuleActions(self, pathxml, self.name)
            self.actions.load()
        except Exception:
            self.logger.exception("Al cargar módulo %s:", self.name)
            return False

        # TODO: Load Main Script:
        self.mainscript = None
        # /-----------------------
        if pineboolib.project._DGI.useDesktop() and pineboolib.project._DGI.localDesktop():
            tiempo_2 = time.time()

        for tablefile in self.files:
            if not tablefile.endswith(".mtd") or tablefile.find("alteredtable") > -1:
                continue
            name, ext = os.path.splitext(tablefile)
            try:
                contenido = str(open(_path(tablefile), "rb").read(), "ISO-8859-15")
            except UnicodeDecodeError as e:
                self.logger.error("Error al leer el fichero %s %s", tablefile, e)
                continue
            tableObj = parseTable(name, contenido)
            if tableObj is None:
                self.logger.warning("No se pudo procesar. Se ignora tabla %s/%s ", self.name, name)
                continue
            self.tables[name] = tableObj
            pineboolib.project.tables[name] = tableObj

        if pineboolib.project._DGI.useDesktop() and pineboolib.project._DGI.localDesktop():
            tiempo_3 = time.time()
            if tiempo_3 - tiempo_1 > 0.2:
                self.logger.debug("Carga del módulo %s : %.3fs ,  %.3fs", self.name, tiempo_2 - tiempo_1, tiempo_3 - tiempo_2)

        self.loaded = True
        return True
