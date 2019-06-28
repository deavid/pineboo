import pineboolib


def convertFLAction(action):
    if action.name() in pineboolib.project.actions.keys():
        return pineboolib.project.actions[action.name()]
    else:
        return None


def convert2FLAction(action):
    name = None
    if isinstance(action, str):
        name = str
    else:
        name = action.name

    from pineboolib.pncontrolsfactory import aqApp

    return aqApp.db().manager().action(name)
