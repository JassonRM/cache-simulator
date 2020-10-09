from Cache import *

class Control:
    def __init__(self, cache):
        self.cache = cache

    def read_request(self, address):
        value = self.cache.read_request(address)
    #     if value != -1:
    #
    #
    # def write_request(self):
    #
    # def write_miss(self):
    #
    # def invalidate(self):

