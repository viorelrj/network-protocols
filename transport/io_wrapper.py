import sys

class IOWrapper:
    __core = None

    def get_type(self):
        return 'io'

    def __init__(self):
        self.__core = sys.stdin

    def read(self):
        return self.__core.readline()

    def get_core(self):
        return self.__core
    
    def get_hash(self):
        return self.get_type() + '_' + str(self.__core.fileno())
