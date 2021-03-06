from enum import Enum


class Cache:
    size = 2

    def __init__(self):
        self.data1 = ['0x0000'] * self.size
        self.data2 = ['0x0000'] * self.size
        self.tags1 = [0] * self.size
        self.tags2 = [0] * self.size
        self.states1 = [State.INVALID] * self.size
        self.states2 = [State.INVALID] * self.size
        self.last_used1 = [False] * self.size
        self.last_used2 = [False] * self.size
        self.input = None

    def read_request(self, address):
        set = address % self.size
        if self.tags1[set] == address // self.size:
            self.last_used1[set] = True
            self.last_used2[set] = False
            return self.data1[set], self.states1[set]
        elif self.tags2[set] == address // self.size:
            self.last_used1[set] = False
            self.last_used2[set] = True
            return self.data2[set], self.states2[set]
        else:
            return -1

    def write_request(self, address, data, state):
        set = address % self.size
        if self.tags1[set] == address // self.size:
            self.data1[set] = data
            self.states1[set] = state
            self.last_used1[set] = True
            self.last_used2[set] = False
            return 0
        elif self.tags2[set] == address // self.size:
            self.data2[set] = data
            self.states2[set] = state
            self.last_used1[set] = False
            self.last_used2[set] = True
            return 0
        elif self.last_used2[set]:
            old_data = [self.tags1[set] * self.size + set, self.data1[set],
                        self.states1[set]]
            self.tags1[set] = address // self.size
            self.data1[set] = data
            self.states1[set] = state
            self.last_used1[set] = True
            self.last_used2[set] = False
            return old_data
        elif self.last_used1[set]:
            old_data = [self.tags2[set] * self.size + set, self.data2[set],
                        self.states2[set]]
            self.tags2[set] = address // self.size
            self.data2[set] = data
            self.states2[set] = state
            self.last_used1[set] = False
            self.last_used2[set] = True
            return old_data

    def modify_state(self, address, state):
        set = address % self.size
        if self.tags1[set] == address // self.size:
            self.states1[set] = state
        elif self.tags2[set] == address // self.size:
            self.states2[set] = state
        else:
            return -1


class State(Enum):
    MODIFIED = 0
    OWNED = 1
    EXCLUSIVE = 2
    SHARED = 3
    INVALID = 4
