from optparse import OptionParser
from optparse import Values
from typing import Optional, List


def parse_options(custom_argv: Optional[List] = None) -> Values:
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
        "--profile-time",
        action="store_true",
        dest="enable_profiler",
        default=False,
        help="Write profile information about CPU load after running",
    )
    parser.add_option(
        "--trace-debug", action="store_true", dest="trace_debug", default=False, help="Write lots of trace information to stdout"
    )
    parser.add_option("--trace-loggers", dest="trace_loggers", default="", help="Comma separated list of modules to enable TRACE output")
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
    parser.add_option("--no-x", action="store_false", dest="enable_gui", default=True, help="Disables graphical interface")

    if custom_argv is None:
        (options, args) = parser.parse_args()
    else:
        (options, args) = parser.parse_args(custom_argv)

    # ---- OPTIONS POST PROCESSING -----
    if options.forceload:
        options.no_python_cache = True
        options.preload = True

    options.loglevel = 30 + (options.quiet - options.verbose) * 5
    options.debug_level = 200  # 50 - (options.quiet - options.verbose) * 25

    return options
