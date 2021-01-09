from transport.socket_wrapper import SocketWrapper
from application.cli import FTPCLI

class FTPServerConnection:
    def __init__(self, ip, control_port, data_port):
        self.__conn_ip = ip

        self.__control_sock = SocketWrapper()
        self.__control_sock.bind(ip, control_port)
        self.__control_sock.set_response(self.handle_control)

        self.__data_sock = SocketWrapper()

    def get_sockets(self):
        return [self.__control_sock, self.__data_sock]

    def handle_data(self, socket_wrapper, action):
        pass

    def handle_control(self, socket_wrapper, action):
        socket_wrapper.accept_connections()

        if action == 'read':
            message = socket_wrapper.recvfrom_noblock()
            if (message == None):
                return

            split = message.split()
            if (split[0] == 'port'):
                ip = message.split()[1]
                port = message.split()[2]
                self.__data_sock.connect(ip, int(port))
                return

            result = FTPCLI.execute(message)
            dest = result['dest']
            content = result['content']

            if dest == 'control':
                self.__control_sock.send(content)
            elif dest == 'data':
                for chunk in content():
                    self.__data_sock.send(chunk)
