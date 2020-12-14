from transport.socket_wrapper import SocketWrapper
from transport.descriptor_listener import DescriptorListener

class FTPClient:
    __control_sock = None
    __data_sock = None
    __listener = None

    def __init__(self):
        self.__control_sock = SocketWrapper()
        self.__data_sock = SocketWrapper()
        self.__listener = DescriptorListener()
    
    def connect(self, ip, port):
        self.__control_sock.connect(ip, port)
        message = self.__control_sock.recvfrom()
        print(message)
        [control_port, data_port] = list(map(lambda x: int(x), message.split(' ')))




