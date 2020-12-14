from transport.socket_wrapper import SocketWrapper
from application.client import FTPClient

client = FTPClient()
client.connect('127.0.0.1', 1234)
