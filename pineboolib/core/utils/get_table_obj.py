"""
Module for getTableObj.
"""
from xml.etree.ElementTree import Element, ElementTree
from .struct import TableStruct


def getTableObj(tree: ElementTree, root: Element) -> TableStruct:
    """Retrieve a basic table object for a given parsed XML."""
    table = TableStruct()
    table.xmltree = tree
    table.xmlroot = root
    elem_query = table.xmlroot.find("query")
    query_name = elem_query and elem_query.text or None
    elem_name = table.xmlroot.find("name")
    if elem_name is None:
        raise ValueError("XML Tag for <name> not found!")
    name = elem_name.text
    table.tablename = name or "noname"
    if query_name:
        table.name = query_name
        table.query_table = name
    else:
        table.name = name or "noname"
        table.query_table = None
    table.fields = []
    table.pk = []
    table.fields_idx = {}
    return table
