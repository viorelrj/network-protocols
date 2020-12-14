
from transport.descriptor_listener import DescriptorListener
from transport.io_wrapper import IOWrapper
from transport.socket_wrapper import SocketWrapper
import random

class FTPServer:
    __ip = None
    __main_port = None
    __ephemeral_ports = [49152, 65535]
    __listener = None
    __core_socket = None
    __ports = []

    def get_ephemeral_port(self):
        rand = random.randint(self.__ephemeral_ports[0], self.__ephemeral_ports[1])
        if rand in self.__ports:
            return self.__ephemeral_ports()
        else:
            self.__ports.append(rand)
            return rand

    def __create_connection(self):
        control = self.get_ephemeral_port()
        data = self.get_ephemeral_port()

        return str(control) + ' ' + str(data)

    def __init__(self, ip, port):
        self.__listener = DescriptorListener()
        self.__ip = ip
        self.__main_port = port

    def run(self):
        self.__core_socket = SocketWrapper()
        self.__core_socket.bind(self.__ip, self.__main_port)
        self.__listener.add_descriptor(self.__core_socket)

        for descriptor in self.__listener.run():
            if (descriptor == None):
                continue

            descriptor.accept_connections()
            if self.__listener.get_state() == 'read':
                message = descriptor.recvfrom_noblock()

                if (descriptor == self.__core_socket and descriptor.is_connected()):
                    descriptor.send(self.__create_connection())

            if self.__listener.get_state() == 'write':
                descriptor.send_cached_ifany()
