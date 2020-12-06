import socket
from queue import Queue
import transport.packet as packet
from transport.connection import Connection

class SocketWrapper:
    __core = None
    __ip = None
    __port = None
    __buff = 1024
    __connection = None

    def __init__(self):
        self.__core = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def get_core(self):
        return self.__core
    
    def get_hash(self):
        return str(self.__core.getsockname())

    # What if binds twice?
    def bind(self, ip, port, buff=1024):
        self.__core.bind((ip, port))
        self.__ip = ip
        self.__port = port
        self.__buff = buff

    def sendto(self, message, addr):
        self.__core.sendto(message, addr)

    def send(self, message):
        return self.__connection.send(message)

    def settimeout(self, timeout):
        self.__core.settimeout(timeout)

    def recvfrom(self):
        return self.__handle_recvfrom()

    def recvfrom_noblock(self):
        self.__core.setblocking(False)
        result = self.__handle_recvfrom()
        self.__core.setblocking(True)
        return result

    def __handle_recvfrom(self):
        if self.__connection.is_conected():
            return self.__connection.read_connection()
        else:
            self.__connection.connect_server()
            return None

    def accept_connections(self):
        if (self.__connection != None):
            return
        self.__connection = Connection(self.__core, self.__buff)

    def connect(self, ip, port):
        self.__connection = Connection(self.__core, self.__buff)
        self.__connection.connect_client((ip, port))
    
    def close(self):
        self.__connection.close_client()

