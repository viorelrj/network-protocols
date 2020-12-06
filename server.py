# from ftp.server import FTPServer

from transport.socket_listener import SocketListener
from transport.socket_wrapper import SocketWrapper

listener = SocketListener()

sock1 = SocketWrapper()
sock1.bind('127.0.0.1', 1234)
listener.add_socket(sock1)

listener.run()