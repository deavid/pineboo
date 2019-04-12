# -*- coding: utf-8 -*-




def wiki_error(e):
    from pineboolib.pncontrolsfactory import SysType as sys
    text = sys.translate("scripts", "Error ejecutando un script")
    text += ":\n%s" % e
    text += process_error(e)
    
    return text

def process_error(error_str):
    from pineboolib.pncontrolsfactory import SysType as sys
    ret = "\n=========== Wiki error =============\n\n"
    
    if "AttributeError: 'dict' object has no attribute" in error_str:
        error = "AttributeError: 'dict' object has no attribute"
        var = error_str[error_str.find(error) + len(error):]
        var = var.replace("\n","")
        ret += sys.translate("scripts", "La forma correcta de acceder a .%s es [%s]") % (var, var)
        
    elif "'builtin_function_or_method' object has no attribute" in error_str:
        error = "'builtin_function_or_method' object has no attribute"
        var = error_str[error_str.find(error) + len(error) + 1:]
        var = var.replace("\n","")
        var = var.replace("'", "")
        ret += sys.translate("scripts", "La forma correcta de acceder a .%s es ().%s") % (var, var)
    
    else:
        "Información no disponible."
    
    return ret   
    