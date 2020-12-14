
from transport.socket_listener import SocketListener
from transport.transport import SocketWrapper
import sys

class FTPServer:
    __ip = None
    __main_port = None
    __ephemeral_ports = [49152, 65535]
    __listener = None
    __core_socket = None

    __init__(self, ip, port):
        self.__listener = SocketListener()
        self.__ip = ip
        self.__port = port

    run(self):
        self.__core_socket = SocketWrapper()
        self.__core_socket.bind(self.__ip, self.__port)
        self.__listener.add_socket(self.__core)

        for descriptor in self.__listener.run():
            if descriptor.fileno() == sys.stdin.fileno():
                val = sys.stdin.readline()
                print('Received', val)
            else:
                descriptor.accept_connection()

                if self.__listener.get_state() == 'read':
                    message = descriptor.recvfrom_noblock()

                    if (message != None):
                        print(message)
                        descriptor.cache_message('Hello there')

                if listener.get_state() == 'write':
                    descriptor.send_cached_ifany()
