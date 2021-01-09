from transport.socket_wrapper import SocketWrapper
from transport.descriptor_listener import DescriptorListener
from transport.io_wrapper import IOWrapper
from application.cli import FTPCLI
import os

class FTPClient:
    __core = None
    __control_sock = None
    __data_sock = None
    __listener = None
    __io_wraper = None

    def __init__(self, data_ip, data_port):
        self.__data_ip = data_ip
        self.__data_port = data_port
        self.__core = SocketWrapper()
        self.__data_sock = SocketWrapper()
        self.__control_sock = SocketWrapper()
        self.__listener = DescriptorListener()
        self.__io_wraper = IOWrapper()

        self.__data_sock.bind(data_ip, data_port)

    def __handle_command(self, command):
        pass
    
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

        data_addr = self.__data_sock.get_core().getsockname()
        data_ip = data_addr[0]
        data_port = str(data_addr[1])
        self.__control_sock.send('port' + ' ' + data_ip + ' ' + data_port)

        for descriptor in self.__listener.run():
            if descriptor == None:
                continue
            
            if self.__listener.get_state()  == 'read':
                if descriptor == self.__data_sock:
                    self.__data_sock.accept_connections()
                    message = self.__data_sock.recvfrom()
                    if (message == None):
                        continue
                    print('data: ' + message)

                if descriptor == self.__control_sock:
                    print(self.__control_sock.recvfrom())

                if descriptor.get_type() == 'io':
                    io_input = descriptor.read().strip()

                    if not FTPCLI.validate(io_input):
                        print('Invalid input')
                        continue
                    
                    self.__control_sock.send(io_input)







