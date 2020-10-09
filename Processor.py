from numpy.random import *
from enum import Enum


class Processor:
    def __init__(self, memory_controller):
        self.running = True
        self.clk = False
        self.memoryController = memory_controller
        self.currentInstruction = None
        self.currentAddress = None
        self.currentData = None
        self.nextInstruction = None
        self.nextAddress = None
        self.nextData = None

    def run(self):
        while self.running:
            if self.clk:
                if self.nextInstruction is None:
                    self.currentInstruction = Instruction(randint(0, 3))
                    if self.nextInstruction == Instruction.READ:
                        self.nextAddress = bin(randint(0, 16))
                    elif self.nextInstruction == Instruction.WRITE:
                        self.nextAddress = bin(randint(0, 16))
                        self.nextData = hex(randint(0, 65536))
                else:
                    self.currentInstruction = self.nextInstruction
                    self.currentAddress = self.nextAddress
                    self.currentData = self.nextData

                if self.nextInstruction == Instruction.READ:
                    self.memory_controller.readRequest(self.currentAddress)
                elif self.nextInstruction == Instruction.WRITE:
                    self.memory_controller.writeRequest(self.currentAddress, self.currentData)
                self.clk = False

    def clock(self):
        self.clk = True

    def set_next_instruction(self, instruction):
        tokens = instruction.split()
        if tokens[0].lower() == 'calc' and len(tokens) == 1:
            self.nextInstruction = Instruction.CALC
        elif tokens[0].lower() == 'read' and len(tokens) == 2:
            self.nextInstruction = Instruction.READ
            self.nextAddress = tokens[1]
        elif tokens[0].lower() == 'write' and len(tokens) == 3:
            self.nextInstruction = Instruction.WRITE
            self.nextAddress = tokens[1]
            self.nextData = tokens[2]
        else:
            raise ValueError("Invalid instruction")


class Instruction(Enum):
    CALC = 0
    READ = 1
    WRITE = 2
