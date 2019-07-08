from xml.etree.ElementTree import Element, ElementTree
from .struct import TableStruct
from .utils_base import one


def getTableObj(tree: ElementTree, root: Element) -> TableStruct:
    table = TableStruct()
    table.xmltree = tree
    table.xmlroot = root
    elem_query = table.xmlroot.find("query")
    query_name = elem_query and one(elem_query.text, None)
    elem_name = table.xmlroot.find("name")
    if elem_name is None:
        raise ValueError("XML Tag for <name> not found!")
    name = elem_name.text
    table.tablename = name
    if query_name:
        table.name = query_name
        table.query_table = name
    else:
        table.name = name
        table.query_table = None
    table.fields = []
    table.pk = []
    table.fields_idx = {}
    return table
