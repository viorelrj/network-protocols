from transport.transport import Transport

class FTPClient:
    __core = None

    def __init__(self):
        self.__core = Transport()

    def request_connection(self, ip):
        connection = self.__core.connect(ip, 5000)
        for msg in connection.subscribe():
            print(msg)