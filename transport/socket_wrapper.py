import socket
from queue import Queue
import transport.packet as packet
from transport.connection import Connection

class SocketWrapper:
    __core = None
    __ip = None
    __port = None
    __buff = 4096
    __connection = None
    __cached_message = None
    __response = None

    def set_response(self, response):
        self.__response = response

    def response(self, action):
        if (self.__response != None):
            self.__response(self, action)

    def is_connected(self):
        return self.__connection.is_conected()

    def get_type(self):
        return 'sock'

    def __init__(self):
        self.__core = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def get_core(self):
        return self.__core
    
    def get_hash(self):
        return self.get_type() + '_' + str(self.__core.getsockname())

    # What if binds twice?
    def bind(self, ip, port, buff=1024):
        self.__core.bind((ip, port))
        self.__ip = ip
        self.__port = port
        self.__buff = buff

    def sendto(self, message, addr):
        self.__core.sendto(message, addr)

    def cache_message(self, message):
        self.__cached_message = message

    def send_cached_ifany(self):
        if (self.__cached_message != None):
            self.send(self.__cached_message)
            self.__cached_message = None

    def send(self, message):
        return self.__connection.send(message)

    def settimeout(self, timeout):
        self.__core.settimeout(timeout)

    def setblocking(self, val):
        self.__core.setblocking(val)

    def recvfrom(self):
        return self._handle_recvfrom()

    def fileno(self):
        return self.__core.fileno()

    def recvfrom_noblock(self):
        self.__core.setblocking(False)
        result = self._handle_recvfrom()
        self.__core.setblocking(True)
        return result

    def _handle_recvfrom(self):
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

