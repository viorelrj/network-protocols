from transport.packet import encode_packet, decode_packet, null_packet, encode_data
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR

class Connection:
    __syn = None
    __ack = None
    __core = None
    __addr = None
    __timeout = 0.5
    __buffsize = None
    __max_count = 5

    def __init__(self, core, addr, syn, ack, buff):
        self.__syn = 0
        self.__core = core
        self.__core.settimeout(self.__timeout)
        self.__addr = addr
        self.__syn = syn
        self.__ack = ack
        self.__buffsize = buff

    def send_packet(self, data):
        data_len = len(data)

        packet = encode_packet(
            data = data,
            data_len = data_len,
            syn = self.__syn,
        )
        self.__syn += data_len

        response = {}
        counter = 0
        while not response or response['ack'] != self.__syn:
            try:
                packet_r = null_packet()
                self.__core.sendto(packet, self.__addr)
                (packet_r, _) = self.__core.recvfrom(self.__buffsize)
                response = decode_packet(packet_r)
            except:
                counter += 1

                if counter < self.__max_count:
                    continue
        return True

    def receive_packet(self):
        fin = None
        response = {}
        counter = 0
        addr = None
        while (not response or response['syn'] != self.__ack):
            try:
                packet_r, addr = self.__core.recvfrom(self.__buffsize)
                response = decode_packet(packet_r)
                if 'fin' in response:
                    fin = response['fin']
                    ack = self.__ack + 1
                else:
                    ack = self.__ack + response['data_len']
                self.__core.sendto(
                    encode_packet(
                        ack=ack,
                        fin=fin
                    ),addr
                )
                if fin != None:
                    break
            except:
                counter += 1
                if counter < self.__max_count:
                    continue
        if (fin != None):
            packet_r, addr = self.__core.recvfrom(self.__buffsize)
            response = decode_packet(packet_r)
            return None

        self.__ack += response['data_len'] or 1
        return response['data']

    def subscribe(self):
        response = self.receive_packet()
        while response != None:
            yield response
            response = self.receive_packet()

    def close(self):
        packet = encode_packet(
            syn = self.__syn,
            fin = True
        )
        self.__syn += 1

        response = {}
        counter = 0
        while not response or response['ack'] != self.__syn or not response['fin']:
            try:
                packet_r = null_packet()
                self.__core.sendto(packet, self.__addr)
                (packet_r, _) = self.__core.recvfrom(self.__buffsize)
                response = decode_packet(packet_r)
            except:
                if counter < self.__max_count:
                    continue

        self.__ack += 1
        self.__core.sendto(
            encode_packet(ack=self.__ack),
            self.__addr
        )