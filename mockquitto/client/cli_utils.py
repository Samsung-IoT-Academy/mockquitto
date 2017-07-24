import argparse

def client_parser(args):
    parser = argparse.ArgumentParser(description="Example daemon in Python")
    parser.add_argument('-p', '--port', help="Broker's port to connect", action="store", default=1883)
    parser.add_argument('--period', help="Period of message generation", action="store", default=1)
    parser.add_argument('--log_file', nargs='?', help='File for logging', action="store", const="log.log",
                        default=None)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', help='Verbose output', action="count", default=0)
    group.add_argument('-q', help="Don't output anything", action="store_true")
    return parser.parse_args(args[1:])
