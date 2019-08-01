"""
SysQs Module.

Emulate sys.qs in a class
"""
import traceback


class SysQs(object):
    """
    Emulate sys.qs from share
    """

    @staticmethod
    def execQSA(fileQSA=None, args=None):
        """
            Execute a QS file.
        """
        from pineboolib.qsa import debug, File, Function

        file = File(fileQSA)
        try:
            file.open(File.ReadOnly)
        except Exception:
            e = traceback.format_exc()
            debug(e)
            return

        fn = Function(str(file.read()))
        fn(args)
