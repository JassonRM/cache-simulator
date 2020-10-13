from numpy.random import *
from enum import Enum


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

    def run(self, clock):
        while self.running:
            clock.wait()
            if self.nextInstruction is None:
                self.currentInstruction = Instruction(randint(0, 3))
                if self.currentInstruction == Instruction.READ:
                    self.currentAddress = bin(randint(0, 16))
                elif self.currentInstruction == Instruction.WRITE:
                    self.currentAddress = bin(randint(0, 16))
                    self.currentData = hex(randint(0, 65536))
            else:
                self.currentInstruction = self.nextInstruction
                self.currentAddress = self.nextAddress
                self.currentData = self.nextData

            if self.currentInstruction == Instruction.READ:
                self.memory_controller.pr_rd(int(self.currentAddress, 2))
            elif self.currentInstruction == Instruction.WRITE:
                # print("-------------------------------------------- address ", int(self.currentAddress, 2))
                self.memory_controller.pr_wr(int(self.currentAddress, 2), self.currentData)

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
