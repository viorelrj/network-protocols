from transport.transport import Transport
import random
import socket

class FTPServer:
    __ip = None
    __port = 5000
    __core = None
    __running = False
    __ephemeral_ports = (49152, 65536)
    __ports = {}

    def __get_port(self):
        candidate = random.randrange(
            self.__ephemeral_ports[0], self.__ephemeral_ports[1])
        while (candidate in self.__ports):
            candidate = random.randrange(
                self.__ephemeral_ports[0], self.__ephemeral_ports[1])
        self.__ports[candidate] = True
        return candidate

    def __init__(self, ip='127.0.0.1'):
        self.__ip = ip
        self.__core = Transport(self.__ip, self.__port)

    def run(self):
        self.__running = True
        while self.__running:
            print('listening for new connections')
            connection = self.__core.accept_connection(500)
            control = self.__get_port()
            data = self.__get_port()
            connection.send_packet(str(control) + ' ' + str(data))
            connection.close()
            self.manage(control, data)

    def manage(self, control, data):
        control_connection = Transport(self.__ip, control).accept_connection(100)
        data_connection = Transport().connect(self.__ip, data)


    def close(self):
        self.__running = False
