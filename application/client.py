from transport.transport import SocketWrapper
from transport.socket_listener import SocketListener
import sys.stdin as stdin

class FTPClient:
    __control_sock = None
    __data_sock = None
    __listener = None

    __init__(self):
        self.__control_sock = SocketWrapper()
        self.__data_sock = SocketWrapper()
        self.__listener = SocketListener()
    
    connect(ip, port):
        self.__control_sock.connect(ip, port)
        message = socket.recvfrom()
        [control_port, data_port] = list(map(lambda x: int(x), message.split(' ')))




