from transport.socket_wrapper import SocketWrapper
import pyDH
from cryptography.fernet import Fernet
import base64

class SessionWrapper(SocketWrapper):
    __dh = None
    __public = None
    __shared = None
    __encrypter = None
    __peer = None

    def __init__(self):
        super().__init__()

    def __encrypt(self, message):
        return self.__encrypter.encrypt(message)

    def __decrypt(self, message):
        return self.__encrypter.decrypt(message)

    def connect(self, ip, port):
        super().connect(ip, port)
        self.__dh = pyDH.DiffieHellman()

        self.__public = self.__dh.gen_public_key()
        super().send(str(self.__public))


        peer_key = int(super().recvfrom())

        self.__shared = self.__dh.gen_shared_key(peer_key).encode()
        self.__shared = base64.urlsafe_b64encode(self.__shared)
        self.__encrypter = Fernet(self.__shared)


    def recvfrom_noblock(self):
        result = super().recvfrom_noblock()

        if result != None and self.__peer == None:
            self.__peer = int(result)

            self.__dh = pyDH.DiffieHellman()
            self.__public = self.__dh.gen_public_key()
            self.__shared = int(self.__dh.gen_shared_key(self.__peer)).to_bytes(32, 'big')
            self.__encrypter = Fernet(self.__shared)

            return None
        return result

    def server(self):
        
        self.setblocking(False)

