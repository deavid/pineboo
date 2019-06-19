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
        var = error_str[error_str.find(error) + len(error) + 1:]
        var = var.replace("\n","")
        ret += sys.translate("scripts", "La forma correcta de acceder a .%s es [%s].") % (var, var)
        
    elif "'builtin_function_or_method' object has no attribute" in error_str:
        error = "'builtin_function_or_method' object has no attribute"
        var = error_str[error_str.find(error) + len(error) + 1:]
        var = var.replace("\n","")
        var = var.replace("'", "")
        ret += sys.translate("scripts", "La forma correcta de acceder a .%s es ().%s.") % (var, var)
        
    elif "AttributeError: 'ifaceCtx' object has no attribute" in error_str:
        error = "AttributeError: 'ifaceCtx' object has no attribute"
        var = error_str[error_str.find(error) + len(error) + 1:] 
        var = var.replace("\n","")
        var = var.replace("'", "")
        ret += sys.translate("scripts", "No se ha traducido el script o el script está vacio.")
    elif "object is not callable" in error_str:
        error = "object is not callable"
        var = error_str[error_str.find("TypeError") + 10:error_str.find(error)] 
        ret += sys.translate("scripts", "Estas llamando a un objeto %s .Los parentesis finales hay que quitarlos." % var)
    elif "unsupported operand type(s) for" in error_str:
        error = "unsupported operand type(s) for"
        ret += sys.translate("scripts", "No puedes hacer operaciones entre dos \'Nones\' o dos tipos diferentes. Revisa el script y controla esto.")
    elif "'QDomElement' object has no attribute 'toString'" in error_str:
        error = "'QDomElement' object has no attribute 'toString'"
        ret += sys.translate("scripts", "toString() ya no está disponible , usa otro método")        
    
    else:
        ret += sys.translate("scripts", "Información no disponible.")
    
    return ret   
    