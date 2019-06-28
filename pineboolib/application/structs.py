from pineboolib.core.utils.utils_base import XMLStruct


class DBServer(XMLStruct):
    """
    Almacena los datos del serividor de la BD principal
    """

    host = None
    port = None


class DBAuth(XMLStruct):
    """
    Almacena los datos de autenticación de la BD principal
    """

    username = None
    password = None
