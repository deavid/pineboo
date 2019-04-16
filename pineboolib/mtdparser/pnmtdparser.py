# -*- coding: utf-8 -*-
from pineboolib.utils import _dir

def mtd_parse(fileobj):
    mtd_file = _dir("cache", fileobj.filekey)
    metadata_name = fileobj.filename[:-4]
    dest_file = "%s_model.py" % mtd_file[:-4]
    from pineboolib.pncontrolsfactory import aqApp
    
    mtd = aqApp.db().manager().metadata(metadata_name)
    
    lines = generate_model(dest_file, mtd)
    
    f = open(dest_file, "w")
    for line in lines:
        f.write("%s\n" % line)
    f.close()
    


def generate_model( dest_file, mtd_table):
    data = []
    data.append("# -*- coding: utf-8 -*-")
    data.append("from sqlalchemy.ext.declarative import declarative_base")
    data.append("from sqlalchemy import Column, Integer, Numeric, String, BigInteger, Boolean, DateTime")
    data.append("from pineboolib.pnobjectsfactory import Calculated")
    data.append("")
    data.append("Base = declarative_base()")
    data.append("")
    data.append("")
    data.append("class %s%s(Base):" % (mtd_table.name()[0].upper(), mtd_table.name()[1:]))
    data.append("    __tablename__ = '%s'" % mtd_table.name())
    data.append("")
    
    for field in mtd_table.fieldList(): #Crea los campos y relaciones 1:M
        field_data = []
        field_data.append("    ")
        field_data.append(field.name())
        field_data.append(" = Column(")
        field_data.append(field_type(field))
        field_data.append(")")
        
        data.append("".join(field_data))
    
    data.append("")
    
    for field in mtd_table.fieldList(): #Relaciones M:1
        if field.relationList():
            rel_data = []
            for r in field.relationList():
                if r.cardinality() == r.RELATION_1M:
                    rel_data.append("    %s = relationship('%s', backref='parent')\n" % (r.foreignTable(), r.foreignTable()))
                
            data.append("".join(rel_data))
            
    return data  
 
def field_type(field):
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
    
    elif field.type() in ("time, date"):
        ret = "DateTime"
    
    else:
        ret = "Desconocido %s" % field.type()
    
    if field.isPrimaryKey() or field.isCompoundKey():
        ret += ", primary_key=True"
    
    if (not field.isPrimaryKey() and not field.isCompoundKey()) and field.type() == "serial":
        ret += ", autoincrement=True"
    
    if field.isUnique():
        ret += ", unique=True"
    
    
    if not field.allowNull():
        ret += ", nullable=False"
    
    if field.defaultValue() is not None:
        value = field.defaultValue()
        if isinstance(value, str):
            value = "'%s'" % value
        ret += ", default=%s" % value
        
    if field.relationM1() is not None:
        rel = field.relationM1()
        ret += ", ForeignKey('%s.%s' %s )" % (rel.foreignTable(), rel.foreignField(), ", cascade='all,delete', backref='%s'" % (rel.foreignTable()) if rel.deleteCascade() else "")
    
    return ret    
