# from ftp.server import FTPServer

from transport.socket_listener import SocketListener
from transport.socket_wrapper import SocketWrapper

listener = SocketListener()

sock1 = SocketWrapper()
sock1.bind('127.0.0.1', 1234)
listener.add_socket(sock1)

counter = 1237

for wrapped_socket in listener.run():
    wrapped_socket.accept_connections()
    message = wrapped_socket.recvfrom_noblock()

    if (message):
        wrapped_socket.send('confirmed')
