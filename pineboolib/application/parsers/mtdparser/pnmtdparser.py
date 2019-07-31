# -*- coding: utf-8 -*-
"""
MTD Parser to sqlAlchemy model.

Creates a Python file side by side with the original MTD file.
Can be overloaded with a custom class to enhance/change available
functions. See pineboolib/pnobjectsfactory.py
"""

from pineboolib import logging
from typing import List, cast
from pineboolib.application.utils.path import _path
from pineboolib.application import project
from pineboolib.application.metadata.pnfieldmetadata import PNFieldMetaData
from pineboolib.application.metadata.pntablemetadata import PNTableMetaData
import os

logger = logging.getLogger(__name__)

reserved_words = ["pass"]


def mtd_parse(table_name: str) -> None:
    """
    Parse MTD into SqlAlchemy model.
    """
    if table_name.find("alteredtable") > -1 or table_name.startswith("fllarge_"):
        return

    if project.conn is None:
        raise Exception("Project is not connected yet")
    mtd_ = project.conn.manager().metadata(table_name)
    if mtd_ is None:
        return
    mtd: PNTableMetaData = cast(PNTableMetaData, mtd_)
    if mtd.isQuery():
        return

    mtd_file = _path("%s.mtd" % table_name)

    if mtd_file is None:
        logger.warning("No se encuentra %s.mtd", table_name)
        return

    dest_file = "%s_model.py" % mtd_file[: len(mtd_file) - 4]
    if dest_file.find("share/pineboo/tables") > -1:
        dest_file = dest_file.replace("share/pineboo/tables", "tempdata/cache/%s/sys/file.mtd" % project.conn.DBName())
        sys_dir = dest_file[: dest_file.find("/file.mtd")]
        if not os.path.exists(sys_dir):
            os.mkdir(sys_dir)
        if not os.path.exists("%s/file.mtd" % sys_dir):
            os.mkdir("%s/file.mtd" % sys_dir)

    if not os.path.exists(dest_file):
        lines = generate_model(dest_file, mtd)

        if lines:
            f = open(dest_file, "w")
            for line in lines:
                f.write("%s\n" % line)
            f.close()


def generate_model(dest_file: str, mtd_table: PNTableMetaData) -> List[str]:
    """
    Create a list of lines from a mtd_table (PNTableMetaData).
    """
    data = []
    pk_found = False
    data.append("# -*- coding: utf-8 -*-")
    # data.append("from sqlalchemy.ext.declarative import declarative_base")
    data.append("from sqlalchemy import Column, Integer, Numeric, String, BigInteger, Boolean, DateTime, ForeignKey, LargeBinary")
    data.append("from sqlalchemy.orm import relationship, validates")
    data.append("from pineboolib.application.parsers.mtdparser.pnormmodelsfactory import Calculated, load_model")
    data.append("from pineboolib.application import project")
    data.append("")
    # data.append("Base = declarative_base()")
    data.append("Base = project.conn.declarative_base()")
    data.append("engine = project.conn.engine()")
    data.append("")
    # for field in mtd_table.fieldList():
    #    if field.relationM1():
    #        rel = field.relationM1()
    #        data.append("load_model('%s')" % rel.foreignTable())

    data.append("")
    data.append("class %s%s(Base):" % (mtd_table.name()[0].upper(), mtd_table.name()[1:]))
    data.append("    __tablename__ = '%s'" % mtd_table.name())
    data.append("")

    validator_list: List[str] = []

    data.append("")
    data.append("# --- Fields ---> ")
    data.append("")

    for field in mtd_table.fieldList():  # Crea los campos
        if field.name() in validator_list:
            logger.warning("Hay un campo %s duplicado en %s.mtd. Omitido", field.name(), mtd_table.name())
        else:
            field_data = []
            field_data.append("    ")
            field_data.append("%s" % field.name() + "_" if field.name() in reserved_words else field.name())
            field_data.append(" = Column('%s', " % field.name())
            field_data.append(field_type(field))
            field_data.append(")")
            validator_list.append(field.name())
            if field.isPrimaryKey():
                pk_found = True

        data.append("".join(field_data))

    data.append("")
    data.append("# <--- Fields --- ")
    data.append("")

    data.append("")
    data.append("# --- Relations 1:M ---> ")
    data.append("")
    if project.conn is None:
        raise Exception("Project is not connected yet")
    manager = project.conn.manager()
    for field in mtd_table.fieldList():  # Creamos relaciones 1M
        for r in field.relationList():
            foreign_table_mtd = manager.metadata(r.foreignTable())
            # if project.conn.manager().existsTable(r.foreignTable()):
            if foreign_table_mtd:
                # comprobamos si existe el campo...
                if foreign_table_mtd.field(r.foreignField()):

                    foreign_object = "%s%s" % (r.foreignTable()[0].upper(), r.foreignTable()[1:])
                    relation_ = "    %s_%s = relationship('%s'" % (r.foreignTable(), r.foreignField(), foreign_object)
                    relation_ += ", foreign_keys='%s.%s'" % (foreign_object, r.foreignField())
                    relation_ += ")"

                    data.append(relation_)

    data.append("")
    data.append("# <--- Relations 1:M --- ")
    data.append("")
    data.append("")
    data.append("")
    data.append("    @validates('%s')" % "','".join(validator_list))
    data.append("    def validate(self, key, value):")
    data.append("        self.__dict__[key] = value #Chapuza para que el atributo ya contenga el valor")
    data.append("        self.bufferChanged(key)")
    data.append("        return value #Ahora si se asigna de verdad")
    data.append("")
    data.append("    def bufferChanged(self, fn):")
    data.append("        pass")

    data.append("")
    data.append("    def beforeCommit(self):")
    data.append("        return True")
    data.append("")
    data.append("    def afterCommit(self):")
    data.append("        return True")
    data.append("")
    data.append("    def commitBuffer(self):")
    data.append("        if not self.beforeCommit():")
    data.append("            return False")
    data.append("")
    data.append("        aqApp.db().session().commit()")
    data.append("")
    data.append("        if not self.afterCommit():")
    data.append("            return False")

    # for field in mtd_table.fieldList():  # Relaciones M:1
    #     if field.relationList():
    #         rel_data = []
    #         for r in field.relationList():
    #             if r.cardinality() == r.RELATION_1M:
    #                 obj_name = "%s%s" % (r.foreignTable()[0].upper(), r.foreignTable()[1:])
    #                 rel_data.append(
    #                     "    %s = relationship('%s', backref='parent'%s)\n"
    #                     % (r.foreignTable(), obj_name, ", cascade ='all, delete'" if r.deleteCascade() else "")
    #                 )
    #
    #         data.append("".join(rel_data))
    #
    # data.append("if not engine.dialect.has_table(engine.connect(),'%s'):" % mtd_table.name())
    # data.append("    %s%s.__table__.create(engine)" % (mtd_table.name()[0].upper(), mtd_table.name()[1:]))

    if not pk_found:
        from pineboolib.core.settings import config

        if config.value("application/isDebuggerMode", False):
            logger.warning(
                "La tabla %s no tiene definida una clave primaria. No se generará el model %s\n"
                % (mtd_table.name(), mtd_table.primaryKey())
            )
        data = []

    return data


def field_type(field: PNFieldMetaData) -> str:
    """
    Get text representation for sqlAlchemy of a field type given its PNFieldMetaData.
    """
    ret = "String"
    if field.type() in ("int, serial"):
        ret = "Integer"
    elif field.type() in ("uint"):
        ret = "BigInteger"
    elif field.type() in ("calculated"):
        ret = "Calculated"
    elif field.type() in ("double"):
        ret = "Numeric"
        ret += "(%s , %s)" % (field.partInteger(), field.partDecimal())

    elif field.type() in ("string", "stringlist", "pixmap"):
        ret = "String"
        if field.length():
            ret += "(%s)" % field.length()

    elif field.type() in ("bool", "unlock"):
        ret = "Boolean"
        ret += ", unique=False"

    elif field.type() in ("time, date"):
        ret = "DateTime"

    elif field.type() in ("bytearray"):
        ret = "LargeBinary"

    else:
        ret = "Desconocido %s" % field.type()

    if field.relationM1() is not None:
        if project.conn is None:
            raise Exception("Project is not connected yet")
        rel = field.relationM1()
        if rel and project.conn.manager().existsTable(rel.foreignTable()):
            ret += ", ForeignKey('%s.%s'" % (rel.foreignTable(), rel.foreignField())
            if rel.deleteCascade():
                ret += ", ondelete='CASCADE'"

            ret += ")"

    if field.isPrimaryKey() or field.isCompoundKey():
        ret += ", primary_key=True"

    if (not field.isPrimaryKey() and not field.isCompoundKey()) and field.type() == "serial":
        ret += ", autoincrement=True"

    if field.isUnique():
        ret += ", unique=True"

    if not field.allowNull() and field.type() not in ("bool", "unlock"):
        ret += ", nullable=False"

    if field.defaultValue() is not None:
        value = field.defaultValue()
        if isinstance(value, str):
            value = "'%s'" % value
        ret += ", default=%s" % value

    return ret
