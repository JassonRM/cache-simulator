class Memory:
    size = 16
    read_latency = 3
    write_latency = 5

    def __init__(self, bus):
        self.bus = bus
        self.data = ['0x0000'] * self.size
        self.address = None
        self.latency = 0
        self.input = None

    def clock(self):
        if self.latency != 0:
            self.latency -= 1
            if self.latency == 0:
                if self.input is None:
                    self.bus.memRead(self.data[self.address])
                else:
                    self.data[self.address] = self.input

    def read_request(self, address):
        self.address = address
        self.latency = self.read_latency

    def write_request(self, address, data):
        self.address = address
        self.latency = self.write_latency
        self.input = data
