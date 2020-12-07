import select
from typing import Type
from threading import Thread
from transport.socket_wrapper import SocketWrapper

class SocketListener:
    __sockets = {}
    __state = None

    def get_state(self):
        return self.__state

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
            read, write, __ = select.select(socket_list, [], socket_list, 5)

            self.__state = 'read'
            for socket in read:
                sock_hash = str(socket.getsockname())
                if sock_hash in self.__sockets:
                    yield self.__sockets[sock_hash]
            self.__state = 'write'

            for socket in self.__sockets.values():
                yield self.__sockets[sock_hash]
