from transport.socket_wrapper import SocketWrapper

socket = SocketWrapper()

socket.connect('127.0.0.1', 1234)
socket.send('Hennlo')
result = socket.recvfrom()
socket.close()

print(result)