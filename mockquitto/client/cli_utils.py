import argparse

def client_parser(args):
    parser = argparse.ArgumentParser(description="Example daemon in Python")
    parser.add_argument('-p', '--port', help="Broker's port to connect", action="store", default=1883)
    parser.add_argument('--period', help="Period of message generation", action="store", default=1)
    parser.add_argument('--log_file', nargs='?', help='File for logging', action="store", const="log.log",
                        default=None)
    parser.add_argument('-c', '--case', help="Case number", nargs='+', type=int)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', help="Verbose output", action="count", default=0)
    group.add_argument('-q', help="Don't output anything", action="count", default=0)

    options = parser.parse_args(args[1:])

    if options.case and not all(isinstance(obj, int) for obj in options.case):
        raise NotImplementedError
    else:
        return options
