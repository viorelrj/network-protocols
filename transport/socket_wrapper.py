import socket
from queue import Queue

class SocketWrapper:
    __core = None
    __ip = None
    __port = None
    __buff = None
    __subscribers = None
    __peer = None

    def __init__(self):
        self.__core = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def get_core(self):
        return self.__core
    
    def get_hash(self):
        return str(self.__core.getsockname())

    # What if binds twice?
    def bind(self, ip, port, buff=1024):
        self.__core.bind((ip, port))
        self.__core.setblocking(False)
        self.__ip = ip
        self.__port = port
        self.__buff = buff

    def sendto(self, message, addr):
        self.__core.sendto(message, addr)

    def handle_recv(self, listener):
        data, addr = self.__core.recvfrom(self.__buff)
        name = self.__core.getsockname()
        new_sock = SocketWrapper()
        print(data)
