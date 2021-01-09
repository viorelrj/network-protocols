
from transport.descriptor_listener import DescriptorListener
from transport.io_wrapper import IOWrapper
from transport.socket_wrapper import SocketWrapper
from application.server_connection import FTPServerConnection
import random

class FTPServer:
    __core_socket = None
    __ip = None
    __main_port = None
    __ephemeral_ports = [49152, 65535]
    __listener = None
    __ports = []
    

    def get_ephemeral_port(self):
        rand = random.randint(self.__ephemeral_ports[0], self.__ephemeral_ports[1])
        if rand in self.__ports:
            return self.__ephemeral_ports()
        else:
            self.__ports.append(rand)
            return rand

    def __create_connection(self):
        control_port = self.get_ephemeral_port()
        data_port = self.get_ephemeral_port()

        connection = FTPServerConnection(self.__ip, control_port, data_port)
        connection_sockets = connection.get_sockets()

        for sock in connection_sockets:
            self.__listener.add_descriptor(sock)

        return str(control_port) + ' ' + str(data_port)

    def __init__(self, ip, port):
        self.__listener = DescriptorListener()
        self.__ip = ip
        self.__main_port = port

    def __handle_core(self, sock_wrapper, action):
        sock_wrapper.accept_connections()
        if self.__listener.get_state() == 'read':
            message = sock_wrapper.recvfrom_noblock()

            if (sock_wrapper == self.__core_socket and sock_wrapper.is_connected()):
                sock_wrapper.send(self.__create_connection())


    def run(self):
        self.__core_socket = SocketWrapper()
        self.__core_socket.bind(self.__ip, self.__main_port)
        self.__listener.add_descriptor(self.__core_socket)

        for descriptor in self.__listener.run():
            if (descriptor == None):
                continue

            if (descriptor != self.__core_socket):
                descriptor.response(self.__listener.get_state())
                continue

            self.__handle_core(descriptor, self.__listener.get_state())
