from ftp.server import FTPServer

server = FTPServer('127.0.0.1')
server.run()
