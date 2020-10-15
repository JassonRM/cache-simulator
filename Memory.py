import threading


class Memory:
    size = 16
    read_latency = 3
    write_latency = 5

    def __init__(self):
        self.data = ['0x0000'] * self.size
        self.address = None
        self.latency = 0
        self.input = None
        self.running = True
        self.finished = threading.Event()
        self.busy = threading.Lock()
        self.output = None

    def run(self, clock):
        while self.running:
            clock.wait()
            if self.latency != 0:
                self.latency -= 1
                if self.latency == 0:
                    if self.input is None:
                        self.output = self.data[self.address]
                    else:
                        self.data[self.address] = self.input
                    self.finished.set()

    def read_request(self, address):
        self.busy.acquire()
        self.address = address
        self.latency = self.read_latency
        self.finished.wait()
        self.finished.clear()
        self.busy.release()
        return self.output

    def write_request(self, address, data):
        self.busy.acquire()
        self.address = address
        self.latency = self.write_latency
        self.input = data
        self.finished.wait()
        self.finished.clear()
        self.busy.release()
