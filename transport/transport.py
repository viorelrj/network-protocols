import logging

from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from packet import encode_packet, decode_packet

class Transport:
    __core = None
    __addr = None
    __logger = None
    __timeout = 5
    __is_listening = False
    __buffsize = 128*1024

    def __init__(self, host, port, name=''):
        self.__logger = logging.getLogger(name)
        self.__core = socket(AF_INET, SOCK_DGRAM)
        self.__addr = (host, port)
    
    def __sendByte(self, msg, addr):
        self.__core.sendto(msg, addr)

    def listen(self, cb):
        self.__is_listening = True
        self.__core.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.__core.bind(self.__addr)
        while self.__is_listening:
            (data, addr) = self.__core.recvfrom(128*1024)
            cb(data, addr, self.__sendByte)

    def send_bytes(self, message):
        result = ''
        try:
            sent = self.__core.sendto(message, self.__addr)
            data, server = self.__core.recvfrom(4096)
            result = data
        finally:
            return result

    def receive_bytes(self):
        (data, addr) = self.__core.recvfrom(128*1024)

    def accept_connection(self):
        syn = 0
        ack = None

        self.__is_listening = True
        self.__core.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.__core.bind(self.__addr)
        
        (packet_r, addr) = self.__core.recvfrom(self.__buffsize)
        response = decode_packet(packet_r)
        ack = response['syn'] + 1
        self.__core.sendto(encode_packet(syn=syn, ack=ack), addr)
        syn += 1

        response = {}
        while not response or response['ack'] != syn:
            (packet_r, addr) = self.__core.recvfrom(self.__buffsize)
            response = decode_packet(packet_r)





    def connect(self, addr):
        syn = 0
        ack = None

        packet_s = encode_packet(syn=syn)
        self.__core.sendto(packet_s, addr)
        syn += 1

        response = {}
        while not response or response['ack'] != syn:
            (packet_r, addr) = self.__core.recvfrom(self.__buffsize)
            response = decode_packet(packet_r)

        ack = response['syn'] + 1
        self.__core.sendto(encode_packet(ack=ack, syn=syn), addr)

        return [addr, syn, ack]

    
    def close(self):
        self.__is_listening = False
        self.__core.close()


