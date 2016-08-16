# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from pineboolib.fllegacy.FLRelationMetaData import FLRelationMetaData
try:
    from future import standard_library
    standard_library.install_aliases()
except ImportError:
    print("Error al importar la libreria python future. http://python-future.org/")
    print("Esta librería sirve para que python2 se comporte más parecido a python3.")
    print("Puede que el programa funcione correctamente sin ella.")
from builtins import object
import traceback

from io import StringIO
from lxml import etree
from pineboolib.dbschema import db_postgresql as pginspect
from pineboolib.fllegacy.FLFieldMetaData import FLFieldMetaData
from PyQt4.QtCore import QString

class Struct(object):
    pass

def parseTable(nombre, contenido, encoding = "UTF-8", remove_blank_text = True):
    file_alike = StringIO(contenido)

    parser = etree.XMLParser(
                    ns_clean=True,
                    encoding=encoding,
                    recover=False,
                    remove_blank_text=remove_blank_text,
                    )
    try:
        tree = etree.parse(file_alike, parser)
    except Exception as e:
        print("Error al procesar tabla:", nombre)
        print(traceback.format_exc())
        return None
    root = tree.getroot()

    objname = root.xpath("name")[0]
    query = root.xpath("query")
    if query:
        if query[-1].text != nombre:
            print("WARN: Nombre de query %s no coincide con el nombre declarado en el XML %s (se prioriza el nombre de query)" % (objname.text,nombre))
            query[-1].text = nombre
    elif objname.text != nombre:
        print("WARN: Nombre de tabla %s no coincide con el nombre declarado en el XML %s (se prioriza el nombre de tabla)" % (objname.text,nombre))
        objname.text = nombre
    return getTableObj(tree,root)

def getTableObj(tree,root):
    table = Struct()
    table.xmltree = tree
    table.xmlroot = root
    query_name = one(table.xmlroot.xpath("query/text()"),None)
    name = table.xmlroot.xpath("name/text()")[0]
    if query_name:
        table.name = query_name
        table.query_table = name
    else:
        table.name = name
    table.fields = []
    table.pk = []
    table.fields_idx = {}
    for xmlfield in table.xmlroot.xpath("field"):
        try:
            field = Struct()
            field.name = None
            field.alias = None
            field.allowNull = False
            field.pk = False
            field.mtd_type = None
            field.length_ = 0
            field.calculated = False
            field.visible = True
            field.editable = True
            field.pI = 4
            field.pD = 0
            field.iNX = False
            field.uNI = False
            field.coun = False
            field.defValue = None
            field.oT = False
            field.rX = None
            field.vG = True
            field.gene = False
            field.iCK = False
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            field.name = xmlfield.xpath("name/text()")[0]
            field.alias = one(xmlfield.xpath("alias/text()"))
            build_field_type(field, xmlfield)
            field.length_ = one(xmlfield.xpath("length/text()"),0)
            field.allowNull = text2bool(one(xmlfield.xpath("null/text()"),"true"))
            field.pk = text2bool(one(xmlfield.xpath("pk/text()"),"false"))
            field.editable = text2bool(one(xmlfield.xpath("editable/text()"),"true"))
            field.visible = text2bool(one(xmlfield.xpath("visible/text()"),"true"))
            field.iCK = text2bool(one(xmlfield.xpath("ck/text()"),"false"))
            field.defValue = one(xmlfield.xpath("default/text()"),None)
            field.optionsList = one(xmlfield.xpath("optionslist/text()"),None)
            field.vG = text2bool(one(xmlfield.xpath("visiblegrid/text()"),"true"))
            field.rX = QString()
            field.pI = one(xmlfield.xpath("partI/text()"), 4)
            field.pD = one(xmlfield.xpath("partD/text()"), 0)
            field.calculated = text2bool(one(xmlfield.xpath("counter/text()"),"false"))
                        
            if field.pk: table.pk.append(field.name)
            if field.name in table.fields_idx: raise ValueError("La tabla %s tiene el campo %s repetido" % (table.name,field.name))
            field.number = len(table.fields)
            table.fields_idx[field.name] = field.number
            fieldMD = FLFieldMetaData(field.name, field.alias, field.allowNull, field.pk, field.mtd_type, field.length_, field.calculated, field.visible, field.editable, field.pI, field.pD, field.iNX, field.uNI, field.coun, field.defValue, field.oT, field.rX, field.vG, field.gene, field.iCK)
            relations = xmlfield.xpath("relation")
            for xmlRelation in relations:
                tableNameR = one(xmlRelation.xpath("table/text()"))
                fieldRelation = one(xmlRelation.xpath("field/text()"))
                cardR = one(xmlRelation.xpath("card/text()"))
                delC = text2bool(one(xmlRelation.xpath("delC/text()"),"false"))
                updC = text2bool(one(xmlRelation.xpath("updC/text()"),"false"))
                checkIn = one(xmlRelation.xpath("checkIn/text()"),"true")
                relation = FLRelationMetaData(tableNameR, fieldRelation, cardR, delC, updC, checkIn)
                fieldMD.addRelationMD(relation)
                
            associateds = xmlfield.xpath("associated")
            for xmlAssoc in associateds:
                aWith = one(xmlRelation.xpath("with/text()"))
                aBy = one(xmlRelation.xpath("by/text()"))
                
                fieldMD.setAssociatedField(aWith , aBy)
                
                 
            if field.optionsList:
                fieldMD.setOptionsList(field.optionsList)
            
            table.fields.append(fieldMD)
                
                
            
            #table.fields.append(fieldMD)
                
            #fieldMD.addRelationMD(relation)
            #print(relationTableNameList_)
            """
            fieldMD = FLFieldMetaData(field.name, field.alias, field.allowNull, field.pk, field.mtd_type, field.length_, field.calculated, field.visible, field.editable, field.pI, field.pD, field.iNX, field.uNI, field.coun, field.defValue, field.oT, field.rX, field.vG, field.gene, field.iCK)

            i = 0
            l = len(relationTableNameList_)
            l1 = len(relationFieldRelationList_)
            l2 = len(relationCardList_)
            while i < l:
                print("%s.%s->%s de %s ojo (%s,%s) " % (table.name, field.name, i, l, l1, l2))
                #print("%s.%s --(%s)--> %s.%s" % (table.name, field.name, relationCardList_[i],relationTableNameList_[i], relationFieldRelationList_[i]))
                if relationDelCList_[i] == "false":
                    delC = False
                else:
                    delC = True
                
                if relationupdCList_[i] == "false":
                    updC = False
                else:
                    updC = True
                
                if relationCIList_[i] == "false":
                    cI = False
                else:
                    cI = True
                
                relation = FLRelationMetaData(relationTableNameList_[i],relationFieldRelationList_[i], relationCardList_[i], delC, updC ,cI)
                fieldMD.addRelationMD(relation)
                i = i + 1
            
            
            
            
            
            
            
            table.fields.append(fieldMD)
            """
        except Exception as e:
            print("ERROR: procesando tabla %r:" % table.name,  e)
            print(traceback.format_exc())
    return table

def text2bool(text):
    text = text.strip().lower()
    if text.startswith("t"): return True
    if text.startswith("f"): return False

    if text.startswith("y"): return True
    if text.startswith("n"): return False

    if text.startswith("1"): return True
    if text.startswith("0"): return False

    if text == "on": return True
    if text == "off": return False

    if text.startswith("s"): return True
    raise ValueError("Valor booleano no comprendido '%s'" % text)

def one(listobj, default = None):
    try: return listobj[0]
    except IndexError: return default


def update_table(conn, table):
    cur = conn.cursor()
    dbfields = {}
    otable = pginspect.get_relname_oid(conn, table.name)
    print("Table:", otable.namespace, otable.name)
    for ocol in pginspect.get_table_columns(conn, otable):
        dbfields[ocol.name] = ocol

    for field in table.fields:
        ocol = dbfields.get(field.name,None)
        print("Field:", field.name, "|", field.sql_type, "|", field.sql_nullable, "|", field.default)
        if ocol is None:
            # TODO: Agregar el campo
            try:
                cur.execute("""ALTER TABLE "%s" ADD COLUMN "%s" %s """ % (otable.name, field.name, field.sql_definition))
            except Exception as e:
                print("ALTER TABLE ERROR::" , e)
            continue
        print("Column:", ocol.name, "|", ocol.format_type, "|", ocol.sql_nullable, "|", ocol.format_extra)
    print()




def create_table(conn, table):
    cur = conn.cursor()
    field_sql_list = [ "%s %s" % (field.name,field.sql_definition)
                        for field in table.fields ]
    if table.pk:
        field_sql_list.append("PRIMARY KEY (" + ", ".join(table.pk) + ")")

    cur.execute("""
    CREATE TABLE %s (
        %s
    )
    """ % (table.name, ",\n".join(field_sql_list)))


def build_field_type(field, xmlfield):
    typetr={
        'string'    : 'character varying',
        'double'    : 'double precision',
        'number'    : 'integer',
        'int'       : 'integer',
        'uint'      : 'integer',
        'unit'      : 'smallint',
        'stringlist': 'text',
        'pixmap'    : 'text',
        'unlock'    : 'boolean',
        'serial'    : 'serial',
        'bool'      : 'bool',
        'date'      : 'date',
        'time'      : 'time',
        'bytearray' : 'bytea',
    }
    field.mtd_type = one(xmlfield.xpath("type/text()"),"string")
    field.nullable = text2bool(one(xmlfield.xpath("null/text()"),"true"))
    field.length = int(one(xmlfield.xpath("length/text()"),"64"))
    field.sql_type = typetr.get(field.mtd_type,field.mtd_type)
    if field.sql_type == "character varying": field.sql_type += "(%d)" % field.length
    field.sql_nullable = "" if field.nullable else "NOT NULL"
    field.sql_definition = field.sql_type
    if field.sql_nullable: field.sql_definition+=" " + field.sql_nullable
