import socket

class UDPClient:
    __core = None
    __addr = None

    def __init__(self, host, port, timeout = 5):
        self.__core = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__core.settimeout(timeout)
        self.__addr = (host, port)

    def sendBytes(self, message, once=False):
        result = ''
        try:
            sent = self.__core.sendto(message, self.__addr)
            data, server = self.__core.recvfrom(4096)
            result = data
        finally:
            return result
    
    def close(self):
        self.__core.close()
