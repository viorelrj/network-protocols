import select
from typing import Type
from threading import Thread
from transport.socket_wrapper import SocketWrapper
import sys

class DescriptorListener:
    __state = None
    __descriptors = {}
    __descriptors_inv = {}

    def get_state(self):
        return self.__state

    def __init__(self):
        pass

    def add_descriptor(self, descriptor):
        self.__descriptors[descriptor.get_core()] = descriptor

    def remove_socket(self, descriptor):
        # self.__descriptors.pop(str(descriptor))
        pass

    def run(self):
        while True:
            descriptor_list = list(self.__descriptors.keys())
            read, write, __ = select.select(descriptor_list, [], descriptor_list, 5)

            def emit_descriptor(descriptor, desc_list):
                if (descriptor) in desc_list:
                    return self.__descriptors[descriptor]

            self.__state = 'read'
            for descriptor in read:
                d = emit_descriptor(descriptor, read)
                if (d != None):
                    yield d

            self.__state = 'write'
            for descriptor in write:
                d = yield emit_descriptor(descriptor, descriptor_list)
                if (d != None):
                    yield d
