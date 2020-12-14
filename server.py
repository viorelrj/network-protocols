from application.server import FTPServer

server = FTPServer('127.0.0.1', 1234)
server.run()



# from transport.descriptor_listener import DescriptorListener
# from transport.io_wrapper import IOWrapper
# from transport.socket_wrapper import SocketWrapper
# import sys

# listener = DescriptorListener()

# sock1 = SocketWrapper()
# sock1.bind('127.0.0.1', 1234)
# listener.add_descriptor(sock1)

# terminal_input = IOWrapper(sys.stdin)
# listener.add_descriptor(terminal_input)

# for descriptor in listener.run():
#     if (descriptor == None):
#         continue

#     if descriptor.get_type() == 'io':
#         result = descriptor.get_core().readline()
#     else:
#         descriptor.accept_connections()

#         if listener.get_state() == 'read':
#             message = descriptor.recvfrom_noblock()

#             if (message != None):
#                 print(message)
        
#         if listener.get_state() == 'write':
#             descriptor.send_cached_ifany()
