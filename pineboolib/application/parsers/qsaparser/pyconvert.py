"""
PyConvert module.

Converts QS projects into Python packages that can be parsed with MyPy
"""
import sys
import os
import os.path
import codecs
import xml.etree.ElementTree as ET
from multiprocessing import Pool
from typing import List, Tuple, TypeVar, cast, Dict, Optional
from pineboolib.core.utils import logging
from pineboolib.core.utils.struct import ActionStruct
from pineboolib.application.parsers.qsaparser import postparse
from pineboolib.application.parsers.qsaparser import pytnyzer


class Action(ActionStruct):
    """Represent actions from XML."""

    modname: str = ""


logger = logging.getLogger("pyconvert")

ModPath = TypeVar("ModPath", bound=str)
ModName = TypeVar("ModName", bound=str)
ModList = List[Tuple[ModPath, ModName]]

CPU_COUNT: int = os.cpu_count() or 1


def _touch(path: str) -> bool:
    """Create a file if does not exist."""
    if not os.path.exists(path):
        logger.info("Creating empty file %r", path)
        open(path, "a").close()
        return True
    return False


def _touch_dir(path: str) -> bool:
    """Create a folder if does not exist."""
    if not os.path.exists(path):
        logger.info("Creating folder %r", path)
        os.mkdir(path)
        return True
    return False


def get_modules(frompath: str = ".") -> ModList:
    """Read folders ignoring anything suspiciuos."""
    rootdir: str = os.path.abspath(frompath)
    module_files: ModList = []
    for root, subFolders, files in os.walk(rootdir):
        for n, subf in reversed(list(enumerate(subFolders))):
            if subf[0] < "a" or subf[0] > "z":
                del subFolders[n]
        root = root.replace(rootdir, "")
        if root.startswith("/"):
            root = root[1:]
        # qs_files = [fname for fname in files if fname.endswith(".qs")]
        modlist = [(root, fname.replace(".mod", "")) for fname in files if fname.endswith(".mod")]
        module_files += cast(ModList, modlist)
    return module_files


def mod_xml_parse(path: str, modname: str) -> Optional[Dict[str, Action]]:
    """Parse Module XML and retrieve actions."""
    try:
        tree = ET.parse(source=codecs.open(path, "r", encoding="iso-8859-15"))
    except Exception:
        logger.exception("Error trying to parse %r", path)
        return None
    root = tree.getroot()
    actions: Dict[str, Action] = {}
    for xmlaction in root:
        action = Action(xmlaction)
        action.modname = modname
        if action.name in actions:
            logger.warning("Found duplicate action in %r for %r. Will override.", path, action.name)
        actions[action.name] = action
    return actions


class PythonifyItem(object):
    """Give multiprocessing something to pickle."""

    src_path: str = ""
    dst_path: str = ""
    n: int = 0
    len: int = 1
    known: Dict[str, Tuple[str, str]] = {}

    def __init__(self, src: str, dst: str, n: int, len: int, known: Dict[str, Tuple[str, str]]):
        """Create object just from args."""
        self.src_path = src
        self.dst_path = dst
        self.n = n
        self.len = len
        self.known = known


def pythonify_item(o: PythonifyItem) -> bool:
    """Parse QS into Python. For multiprocessing.map."""
    logger.info("(%.2f%%) Parsing QS %r", 100 * o.n / o.len, o.src_path)
    try:
        pycode = postparse.pythonify2(o.src_path, known_refs=o.known)
    except Exception:
        logger.exception("El fichero %s no se ha podido convertir", o.src_path)
        return False
    with open(o.dst_path, "w") as f1:
        f1.write(pycode)

    return True


def main() -> None:
    """Get options and start conversion."""
    filter_mod = sys.argv[1] if len(sys.argv) > 1 else None
    filter_file = sys.argv[2] if len(sys.argv) > 2 else None

    pytnyzer.STRICT_MODE = False
    log_format = "%(levelname)s: %(name)s: %(message)s"
    logging.basicConfig(format=log_format, level=0)
    blib_logger = logging.getLogger("blib2to3.pgen2.driver")
    blib_logger.setLevel(logging.WARNING)
    logger.info("Cpu count %d", CPU_COUNT)
    source_folder = "."
    package_name = "pymodules"
    src_path = os.path.abspath(source_folder)
    dst_path = os.path.abspath(os.path.join(src_path, package_name))
    # Step 1 - Create base package path
    _touch_dir(dst_path)
    _touch(os.path.join(dst_path, "__init__.py"))
    mypy_ini = os.path.join(src_path, "mypy.ini")
    if not os.path.exists(mypy_ini):
        with open(mypy_ini, "w") as f1:
            f1.write("[mypy]\n")
            f1.write("python_version = 3.7\n")
            f1.write("check_untyped_defs = True\n")

    # Step 2 - Create module folders
    module_files_in: ModList = get_modules(src_path)
    known_modules: Dict[str, Tuple[str, str]] = {}
    module_files_ok: ModList = []
    for mpath, mname in module_files_in:
        xml_name = os.path.join(mpath, "%s.xml" % mname)
        if not os.path.exists(os.path.join(src_path, xml_name)):
            logger.warn("File not found %r. Ignoring module." % xml_name)
            continue
        if os.sep in mpath:
            mpath_list = mpath.split(os.sep)
            if len(mpath_list) > 2:
                logger.warn("Path %r is not supported, maximum is depth 2" % mpath)
                continue
            mpath_parent = mpath_list[0]
            _touch_dir(os.path.join(dst_path, mpath_parent))
            _touch(os.path.join(dst_path, mpath_parent, "__init__.py"))

        _touch_dir(os.path.join(dst_path, mpath))
        _touch(os.path.join(dst_path, mpath, "__init__.py"))
        known_modules[mname] = (package_name + "." + mpath.replace(os.sep, "."), mname)
        module_files_ok.append((mpath, mname))

    # Step 3 - Read module XML and identify objects
    for mpath, mname in module_files_ok:
        xml_name = os.path.join(mpath, "%s.xml" % mname)
        actions = mod_xml_parse(os.path.join(src_path, xml_name), mname)
        if actions is None:
            continue
        for action in actions.values():
            if action.scriptform:
                module_pubname = "form%s" % action.name
                known_modules[module_pubname] = (
                    package_name + "." + mpath.replace(os.sep, "."),
                    action.scriptform,
                )
            if action.scriptformrecord:
                module_pubname = "formRecord%s" % action.name
                known_modules[module_pubname] = (
                    package_name + "." + mpath.replace(os.sep, "."),
                    action.scriptformrecord,
                )

    if filter_mod is not None:
        for alias, (path, name) in known_modules.items():
            if filter_mod not in path and filter_mod not in name:
                continue
            logger.debug("from %s import %s as %s", path, name, alias)

    # Step 4 - Retrieve QS file list for conversion
    logger.info("Retrieving QS File list...")
    qs_files: List[Tuple[str, str]] = []
    for mpath, mname in module_files_ok:
        if filter_mod is not None and filter_mod not in mpath and filter_mod not in mname:
            continue
        rootdir = os.path.join(src_path, mpath)
        for root, subFolders, files in os.walk(rootdir):

            def get_fname_pair(fname: str) -> Tuple[str, str]:
                src_filename = os.path.join(root, fname)
                dst_filename = os.path.join(dst_path, mpath, fname.replace(".qs", ".py"))
                return src_filename, dst_filename

            if filter_file is not None:
                files = [fname for fname in files if filter_file in fname]
            qs_files += [get_fname_pair(fname) for fname in files if fname.endswith(".qs")]

    # Step 5 - Convert QS into Python
    logger.info("Converting %d QS files...", len(qs_files))

    itemlist = [
        PythonifyItem(src=src, dst=dst, n=n, len=len(qs_files), known=known_modules)
        for n, (src, dst) in enumerate(qs_files)
    ]
    with Pool(CPU_COUNT) as p:
        # TODO: Add proper signatures to Python files to avoid reparsing
        pycode_list: List[bool] = p.map(pythonify_item, itemlist, chunksize=2)
        if not all(pycode_list):
            raise Exception("Conversion failed for some files")
