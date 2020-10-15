from Cache import *


class Control:
    def __init__(self, identifier, cache, bus):
        self.id = identifier
        self.cache = cache
        self.bus = bus

    def pr_rd(self, address):
        value = self.cache.read_request(address)
        if value == -1 or value[1] == State.INVALID:
            response = self.bus.rd(self.id, address)
            self.cache.write_request(address, response[0], response[1])
            return response[0]
        else:
            return value[0]

    def pr_wr(self, address, data):
        value = self.cache.read_request(address)
        if value == -1 or value[1] == State.INVALID:
            self.bus.rd_x(self.id, address)
        elif value[1] == State.SHARED or value[1] == State.OWNED:
            print("Upgrading")
            self.bus.upgr(self.id, address)
        old_value = self.cache.write_request(address, data, State.MODIFIED)
        if old_value is not None and old_value != 0 and (old_value[2] == State.MODIFIED or old_value[2] == State.OWNED):
            self.bus.flush_wb(old_value[0], old_value[1])

    def bus_rd(self, address):
        value = self.cache.read_request(address)
        if value != -1 and value[1] != State.INVALID:
            if value[1] == State.EXCLUSIVE:
                self.cache.modify_state(address, State.SHARED)
                return value[0], State.SHARED
            elif value[1] == State.SHARED or value[1] == State.OWNED:
                return value[0], State.SHARED
            elif value[1] == State.MODIFIED:
                self.cache.modify_state(address, State.OWNED)
                return value[0], State.SHARED
        else:
            return -1

    def bus_rd_x(self, address):
        value = self.cache.read_request(address)
        if value != -1 and value[1] != State.INVALID:
            self.cache.modify_state(address, State.INVALID)
            if value[1] == State.EXCLUSIVE or value[1] == State.MODIFIED or value[1] == State.OWNED:
                return value[0]
            else:
                return -1

    def bus_upgr(self, address):
        value = self.cache.read_request(address)
        print("Upgrading address: ", address, " with value ", value)
        if value != -1 and value[1] != State.INVALID and (value[1] == State.SHARED or value[1] == State.OWNED):
            self.cache.modify_state(address, State.INVALID)
