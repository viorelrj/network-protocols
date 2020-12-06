import transport.packet as packet

class Connection:
    __syn = None
    __ack = None
    __core = None
    __buff = None
    __addr = None
    __connected = False
    __max_tries = 5
    __addr = None

    def is_conected(self):
        return self.__connected

    def __reset(self):
        self.__syn = 0
        self.__ack = None
        self.__connected = False
        self.__addr = None

    def __init__(self, core, buff):
        self.__core = core
        self.__buff = buff
        self.__syn = 0
        self.__ack = None

    def connect_client(self, addr):
        if self.__connected:
            return True

        self.__addr = addr
        if self.__syn == 0:
            response = {}

            tries = 0
            while not (response or ('ack' in response and response['ack'] != self.__syn)) and tries < self.__max_tries:
                self.__core.sendto(packet.encode_packet(
                    syn=self.__syn), self.__addr)
                tries += 1
                (response_raw, addr) = self.__core.recvfrom(self.__buff)
                response = packet.decode_packet(response_raw)
            self.__syn += 1

            if tries >= self.__max_tries:
                self.__reset()
                raise Exception("Couldn't establish first conneciton")

            self.__ack = response['syn'] + 1
            self.__core.sendto(packet.encode_packet(
                ack=self.__ack, syn=self.__syn), addr)
            self.__connected = True

    def connect_server(self):
        if self.__connected:
            return True

        raw_response, addr = self.__core.recvfrom(self.__buff)
        response = packet.decode_packet(raw_response)

        if (self.__addr != None and addr != self.__addr):
            return None

        if (not 'ack' in response or response['ack'] == self.__syn):
            self.__addr = addr
            self.__ack = response['syn'] + 1
            self.__core.sendto(
                packet.encode_packet(syn=self.__syn, ack=self.__ack),
                addr
            )
            return None
        self.__syn = 1

        if (response['ack'] == self.__syn):
            self.__connected = True
            self.__addr = addr
            return True
        else:
            self.__reset()

    def close_client(self):
        pack = packet.encode_packet(fin=True, syn=self.__syn)
        self.__syn += 1

        tries = 0
        response = {}
        print('closing')
        while not response or not 'fin' in response or response['ack'] != self.__syn:
            self.__core.sendto(pack, self.__addr)
            tries += 1
            (response_raw, addr) = self.__core.recvfrom(self.__buff)
            response = packet.decode_packet(response_raw)
            if tries >= self.__max_tries:
                self.__reset()
                raise Exception("Closing failed")
        self.__reset()

    def close_server(self, data: None):
        if (data != None):
            self.__ack += 1
            pack = packet.encode_packet(
                fin=True, ack=self.__ack, syn=self.__syn)
            self.__syn += 1

            self.__core.sendto(pack, self.__addr)
            self.__reset()

    def send(self, message):
        if (self.__addr == None or not self.__connected):
            return False

        data_len = len(packet.encode_data(message))
        encoded = packet.encode_packet(
            ack=self.__ack, syn=self.__syn, data=message, data_len=data_len)
        self.__syn += data_len
        self.__core.sendto(encoded, self.__addr)

        data, addr = self.__core.recvfrom(self.__buff)
        data = packet.decode_packet(data)
        while data['ack'] != self.__syn or addr != self.__addr:
            self.__core.sendto(encoded, self.__addr)
            data, addr = self.__core.recvfrom(self.__buff)
            data = packet.decode_packet(data)

    def read_connection(self):
        data, addr = self.__core.recvfrom(self.__buff)
        if (addr != self.__addr):
            return None
        data = packet.decode_packet(data)
        if ('fin' in data):
            self.close_server(data)
            return None
        self.__ack += data['data_len']

        pack = packet.encode_packet(ack=self.__ack)
        self.__core.sendto(pack, self.__addr)
        return data['data']
