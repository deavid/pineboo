import logging
from optparse import OptionParser


def parse_options():
    """Load and parse options."""

    parser = OptionParser()
    parser.add_option("-l", "--load", dest="project", help="load projects/PROJECT.xml and run it", metavar="PROJECT")
    parser.add_option(
        "-c",
        "--connect",
        dest="connection",
        help="connect to database with user and password.",
        metavar="user:passwd:driver_alias@host:port/database",
    )
    parser.add_option(
        "-v", "--verbose", action="count", default=0, help="increase verbosity level"
    )  # default a 2 para ver los logger.info, 1 no los muestra
    parser.add_option("-q", "--quiet", action="count", default=0, help="decrease verbosity level")
    parser.add_option(
        "--trace-debug", action="store_true", dest="trace_debug", default=False, help="Write lots of trace information to stdout"
    )
    parser.add_option("--log-time", action="store_true", dest="log_time", default=False, help="Add timestamp to logs")
    parser.add_option(
        "--trace-signals",
        action="store_true",
        dest="trace_signals",
        default=False,
        help="Wrap up every signal, connect and emit, and give useful tracebacks",
    )
    parser.add_option("-a", "--action", dest="action", help="load action", metavar="ACTION")
    parser.add_option("--no-python-cache", action="store_true", dest="no_python_cache", default=False, help="Always translate QS to Python")
    parser.add_option(
        "--preload", action="store_true", dest="preload", default=False, help="Load everything. Then exit. (Populates Pineboo cache)"
    )
    parser.add_option(
        "--force-load",
        dest="forceload",
        default=None,
        metavar="ACTION",
        help="Preload actions containing string ACTION without caching. Useful to debug pythonyzer",
    )
    parser.add_option("--dgi", dest="dgi", default="qt", help="Change the gdi mode by default", metavar="DGI")
    parser.add_option("--dgi_parameter", dest="dgi_parameter", help="Change the gdi mode by default", metavar="DGIPARAMETER")
    parser.add_option("--test", action="store_true", dest="test", default=False, help="Launch all test")
    parser.add_option("--dbadmin", action="store_true", dest="enable_dbadmin", default=False, help="Enables DBAdmin mode")
    parser.add_option("--quick", action="store_true", dest="enable_quick", default=False, help="Enables Quick mode")

    (options, args) = parser.parse_args()

    # ---- OPTIONS POST PROCESSING -----
    if options.forceload:
        options.no_python_cache = True
        options.preload = True

    options.loglevel = 30 + (options.quiet - options.verbose) * 5
    options.debug_level = 200  # 50 - (options.quiet - options.verbose) * 25

    # ---- LOGGING -----
    log_format = "%(levelname)s: %(name)s: %(message)s"

    if options.log_time:
        log_format = "%(asctime)s - %(levelname)s: %(name)s: %(message)s"

    # FIXME: Logging configuration is not part of options parsing.
    from pineboolib.loader.utils import addLoggingLevel

    addLoggingLevel("TRACE", logging.DEBUG - 5)
    addLoggingLevel("NOTICE", logging.INFO - 5)
    addLoggingLevel("HINT", logging.INFO - 2)
    addLoggingLevel("MESSAGE", logging.WARN - 5)

    logging.basicConfig(format=log_format, level=options.loglevel)
    # logger.debug("LOG LEVEL: %s  DEBUG LEVEL: %s", options.loglevel, options.debug_level)

    disable_loggers = ["PyQt5.uic.uiparser", "PyQt5.uic.properties"]
    for loggername in disable_loggers:
        modlogger = logging.getLogger(loggername)
        modlogger.setLevel(logging.WARN)

    return options
