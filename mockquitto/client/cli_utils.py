import argparse

def _get_package_info():
    from mockquitto.version import __version__
    from mockquitto import __name__
    return (__name__, __version__)

def client_parser(args):
    parser = argparse.ArgumentParser(prog=_get_package_info()[0], description=_("Generator of MQTT messages"))
    parser.add_argument('-p', '--port', help=_("Broker's port to connect"), action="store", default=1883)
    parser.add_argument('--period', help=_("Period of message generation"), action="store", default=1)
    parser.add_argument('--log_file', nargs='?', help=_("File for logging"), action="store", const="log.log",
                        default=None)
    parser.add_argument('-c', '--case', help=_("Case number"), nargs='+', type=int)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', help=_("Verbose output (up to 3 repetitions)"), action="count", default=0)
    group.add_argument('-q', help=_("Quieter output (up to 2 repetitions)"), action="count", default=0)

    parser.add_argument('-V', '--version', help=_("Print version and exit"), action="version",
                        version="%(prog)s {}".format(_get_package_info()[1]))

    options = parser.parse_args(args[1:])

    if options.case and not all(isinstance(obj, int) for obj in options.case):
        raise NotImplementedError

    return options


