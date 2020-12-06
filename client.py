# from ftp.client import FTPClient

# client = FTPClient()
# [control, data] = client.request_connection('127.0.0.1')

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b'1234', ('127.0.0.1', 1234))
