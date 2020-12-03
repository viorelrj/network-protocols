import json
from typing import Literal

# keys = Literal('')

encoding = 'utf-8'

def encode_packet(ack=None, syn=None, fin=None):
    content = {}

    def add_notnull(var, display):
        if var != None:
            content[display] = var

    add_notnull(ack, 'ack')
    add_notnull(syn, 'syn')
    add_notnull(fin, 'fin')
    
    return json.dumps(content).encode(encoding)

def decode_packet(packet):
    return json.loads(packet.decode(encoding))