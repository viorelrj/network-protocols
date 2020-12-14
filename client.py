from transport.socket_wrapper import SocketWrapper


socket = SocketWrapper()

socket.connect('127.0.0.1', 1234)
socket.send('Hennlo')
# message = socket.recvfrom()
# print(message)
socket.close()