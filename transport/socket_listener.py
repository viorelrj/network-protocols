import select
from typing import Type
from threading import Thread
from transport.socket_wrapper import SocketWrapper

class SocketListener:
    __sockets = {}

    def __init__(self):
        pass

    def add_socket(self, socket: Type[SocketWrapper]):
        self.__sockets[socket.get_hash()] = socket

    def remove_socket(self, socket: Type[SocketWrapper]):
        self.__sockets.pop(socket.get_hash())

    def run(self):
        while True:
            socket_list = map(
                lambda wrapper: wrapper.get_core(), self.__sockets.values())
            socket_list = list(socket_list)
            read, _, __ = select.select(socket_list, [], socket_list, 5)
            for read_socket in read:
                sock_hash = str(read_socket.getsockname())
                if sock_hash in self.__sockets:
                    yield self.__sockets[sock_hash]
