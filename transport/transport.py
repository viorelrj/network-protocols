from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from packet import encode_packet, decode_packet
from connection import Connection

class Transport:
    __core = None
    __addr = None
    __timeout = None
    __buffsize = None

    def __init__(self, buffsize=128*1024, timeout=5):
        self.__core = socket(AF_INET, SOCK_DGRAM)
        self.__buffsize = buffsize
        self.__timeout = timeout

    def accept_connection(self, host, port):
        self.__addr = (host, port)
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
        response_addr = ()
        while not response or response['ack'] != syn:
            (packet_r, addr) = self.__core.recvfrom(self.__buffsize)
            response = decode_packet(packet_r)
            respomse_addr = addr
        
        return Connection(self.__core, respomse_addr, syn, ack, self.__buffsize)

    def connect(self, host, port):
        addr = (host, port)
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

        return Connection(self.__core, addr, syn, ack, self.__buffsize)


