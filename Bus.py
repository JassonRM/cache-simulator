from Cache import State


class Bus:
    def __init__(self, cores, memory):
        self.cores = cores
        self.memory = memory

    def rd(self, identifier, address):
        for core in self.cores:
            if core.id != identifier:
                response = core.memoryController.bus_rd(address)
                if response != -1:
                    return response
        return self.memory.read_request(address), State.EXCLUSIVE

    def rd_x(self, identifier, address):
        for core in self.cores:
            if core.id != identifier:
                core.memoryController.bus_rd_x(address)

    def upgr(self, identifier, address):
        for core in self.cores:
            if core.id != identifier:
                core.memoryController.bus_upgr(address)

    def flush_wb(self, address, data):
        self.memory.write_request(address, data)
