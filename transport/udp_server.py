import logging
import socket

class UDPServer:
    __core = None
    __addr = None
    __log = logging.getLogger('udp_server')

    FORMAT_CONS = '%(asctime)s %(name)-12s %(levelname)8s\t%(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT_CONS)

    def __init__(self, host, port):
        self.__core = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__addr = (host, port)

        for data in self.__run():
            self.handle_request(data)

    def __run(self):
        self.__core.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__core.bind(self.__addr)
        while True:
            (data, addr) = self.__core.recvfrom(128*1024)
            self.__core.sendto(b'ok', addr)
            yield data
    
    def handle_request(self, data):
        self.__log.debug("%r" % (data,))

