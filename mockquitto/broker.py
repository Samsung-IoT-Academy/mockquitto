import errno
import socket


class BrokerConfig:
    def __init__(self, proto='tcp', domain='localhost', port=1883, max_conns=10, interval=10):
        self.__proto = proto
        self.__domain = domain
        self.__port = self.broker_port(port)
        self.__max_conns = max_conns
        self.__interval = interval


    def get_config(self):
        return {
            'listeners': {
                'default': {
                    'type': self.__proto,
                    'bind': self.__domain + ':' + str(self.__port),
                    'max_connections': self.__max_conns,
                }
            },
            'sys_interval': self.__interval
        }

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        self.__port = value

    @property
    def domain(self):
        return self.__domain

    def broker_port(self, port=1883):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                s.bind(('localhost', port))
            except OSError as err:
                if err.errno == errno.EADDRINUSE:
                    port += 1
                continue
            break
        addr, port = s.getsockname()
        s.close()
        return port