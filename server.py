# from ftp.server import FTPServer

from transport.socket_listener import SocketListener
from session.session import SocketWrapper

listener = SocketListener()

sock1 = SocketWrapper()
sock1.bind('127.0.0.1', 1234)
listener.add_socket(sock1)

for wrapped_socket in listener.run():
    wrapped_socket.accept_connections()

    if listener.get_state() == 'read':
        message = wrapped_socket.recvfrom_noblock()

        if (message != None):
            print(message)
            wrapped_socket.cache_message('Hello there')
    
    if listener.get_state() == 'write':
        wrapped_socket.send_cached_ifany()
