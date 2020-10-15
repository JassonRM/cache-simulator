from numpy import random
from enum import Enum
import threading


class Processor:
    def __init__(self, memory_controller):
        self.running = True
        self.memory_controller = memory_controller
        self.currentInstruction = None
        self.currentAddress = None
        self.currentData = None
        self.nextInstruction = None
        self.nextAddress = None
        self.nextData = None
        self.instruction_ready = threading.Event()
        self.instruction_ready.set()
        self.using_mem = False

    def run(self, clock):
        while self.running:
            clock.wait()
            if self.nextInstruction is None:
                normal = random.normal(0, 1)
                if normal < -1:
                    self.currentInstruction = Instruction.READ
                elif -1 <= normal <= 1:
                    self.currentInstruction = Instruction.CALC
                elif normal > 1:
                    self.currentInstruction = Instruction.WRITE

                if self.currentInstruction == Instruction.READ:
                    address = random.poisson(4)
                    if address > 15:
                        address == 15
                    self.currentAddress = bin(address)

                elif self.currentInstruction == Instruction.WRITE:
                    address = random.poisson(4)
                    if address > 15:
                        address == 15
                    self.currentAddress = bin(address)

                    self.currentData = hex(random.randint(0, 65536))
            else:
                self.currentInstruction = self.nextInstruction
                self.currentAddress = self.nextAddress
                self.currentData = self.nextData

            clock.clear()
            self.instruction_ready.set()

            if self.currentInstruction == Instruction.READ:
                self.using_mem = True
                self.memory_controller.pr_rd(int(self.currentAddress, 2))
                self.using_mem = False
                self.instruction_ready.set()
            elif self.currentInstruction == Instruction.WRITE:
                self.using_mem = True
                self.memory_controller.pr_wr(int(self.currentAddress, 2),
                                             self.currentData)
                self.using_mem = False
                self.instruction_ready.set()

    def set_next_instruction(self, instruction):
        tokens = instruction.split()
        if tokens[0].lower() == 'calc' and len(tokens) == 1:
            self.nextInstruction = Instruction.CALC
        elif tokens[0].lower() == 'read' and len(tokens) == 2:
            self.nextInstruction = Instruction.READ

            try:
                address = int(tokens[1], 2)
            except ValueError:
                raise ValueError("Address is not binary")

            if not 0 <= address <= 16:
                raise ValueError("Address out of bounds")

            self.nextAddress = bin(address)
        elif tokens[0].lower() == 'write' and len(tokens) == 3:
            self.nextInstruction = Instruction.WRITE

            try:
                address = int(tokens[1], 2)
            except ValueError:
                raise ValueError("Address is not binary")

            if not 0 <= address <= 16:
                raise ValueError("Address out of bounds")

            self.nextAddress = bin(address)

            try:
                value = int(tokens[2], 16)
            except ValueError:
                raise ValueError("Value is not hex")

            if not 0 <= value <= 65536:
                raise ValueError("Value is too large for 16 bits")

            self.nextData = tokens[2]
        else:
            raise ValueError("Invalid instruction name")

    def reset_next_instruction(self):
        self.nextInstruction = None


class Instruction(Enum):
    CALC = 0
    READ = 1
    WRITE = 2
