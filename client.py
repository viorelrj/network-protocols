from transport.socket_wrapper import SocketWrapper

from transport.transport import Transport

socket = SocketWrapper()

socket.connect('127.0.0.1', 1234)
socket.send('Hennlo')
socket.send('How ar yu')
socket.send('Can I has bred?')
socket.close()