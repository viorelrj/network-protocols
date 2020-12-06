from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from transport.connection import Connection
from transport.socket_wrapper import SocketWrapper
import transport.packet as packet


class Transport:
    __core = None
    __addr = None
    __timeout = None
    __buffsize = None

    def __init__(self, host=None, port=None, buffsize=128*1024, timeout=5):
        self.__core = SocketWrapper()
        self.__addr = (host, port)
        if host != None and port != None:
            self.__core.bind(host, port)
        self.__buffsize = buffsize
        self.__timeout = timeout

    def accept_connection(self, timeout):
        syn = 0
        ack = None
        self.__core.settimeout(timeout)
        
        (packet_r, addr) = self.__core.recvfrom()
        response = packet.decode_packet(packet_r)
        ack = response['syn'] + 1
        self.__core.sendto(packet.encode_packet(syn=syn, ack=ack), addr)
        syn += 1

        response = {}
        response_addr = ()
        while not response or response['ack'] != syn:
            (packet_r, addr) = self.__core.recvfrom()
            response = packet.decode_packet(packet_r)
            response_addr = addr
        
        return Connection(self.__core, response_addr, syn, ack, self.__buffsize)

    def connect(self, host, port):
        addr = (host, port)
        syn = 0
        ack = None

        packet_s = packet.encode_packet(syn=syn)
        self.__core.sendto(packet_s, addr)
        syn += 1

        response = {}
        while not response or response['ack'] != syn:
            (packet_r, addr) = self.__core.recvfrom()
            response = packet.decode_packet(packet_r)

        ack = response['syn'] + 1
        self.__core.sendto(packet.encode_packet(ack=ack, syn=syn), addr)

        return Connection(self.__core, addr, syn, ack, self.__buffsize)


