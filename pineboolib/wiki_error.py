# -*- coding: utf-8 -*-




def wiki_error(e):
    
    text = "Error ejecutando la función:\n%s" % e
    text += process_error(e)
    
    return text

def process_error(error_str):
    ret = "\n=========== Wiki error =============\n\n"
    if "AttributeError: 'dict' object has no attribute" in error_str:
        error = "AttributeError: 'dict' object has no attribute"
        var = error_str[error_str.find(error) + len(error):]
        var = var.replace("\n","")
        ret += "La forma correcta de acceder a .%s es [%s]." % (var, var)
    else:
        "Información no disponible."
    
    return ret   
    