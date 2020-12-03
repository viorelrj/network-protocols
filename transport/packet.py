import json

encoding = 'utf-8'

def encode_packet(ack=None, syn=None, fin=None, data=None, data_len=None):
    content = {}

    def add_notnull(var, display):
        if var != None:
            content[display] = var

    add_notnull(ack, 'ack')
    add_notnull(syn, 'syn')
    add_notnull(fin, 'fin')
    add_notnull(data, 'data')
    add_notnull(data_len, 'data_len')
    
    return json.dumps(content).encode(encoding)

def decode_packet(packet):
    return json.loads(packet.decode(encoding))

def null_packet():
    return json.dumps("{}").encode(encoding)

def encode_data(data):
    return str(data).encode(encoding)