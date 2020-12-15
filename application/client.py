from transport.socket_wrapper import SocketWrapper
from transport.descriptor_listener import DescriptorListener
from transport.io_wrapper import IOWrapper

class FTPClient:
    __core = None
    __control_sock = None
    __data_sock = None
    __listener = None
    __io_wraper = None

    def __init__(self):
        self.__core = SocketWrapper()
        self.__data_sock = SocketWrapper()
        self.__control_sock = SocketWrapper()
        self.__listener = DescriptorListener()
        self.__io_wraper = IOWrapper()
    
    def connect(self, ip, port):
        self.__core.connect(ip, port)
        message = self.__core.recvfrom()
        [control_port, data_port] = list(map(lambda x: int(x), message.split(' ')))
        self.__core.close()

        self.__control_sock.connect(ip, control_port)
        self.__run()

    def __run(self):
        self.__listener.add_descriptor(self.__control_sock)
        self.__listener.add_descriptor(self.__data_sock)
        self.__listener.add_descriptor(self.__io_wraper)

        for descriptor in self.__listener.run():
            if descriptor == None:
                continue
            
            if self.__listener.get_state()  == 'read':
                if descriptor.get_type() == 'sock':
                    pass

                if descriptor.get_type() == 'io':
                    result = descriptor.read().strip()
                    pass








