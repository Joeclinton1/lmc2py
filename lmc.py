import importlib.util
import ntpath
import sys
import os
import re


class LMC:
    def __init__(self, _potential_values, mailboxes, max_cycles=50000):
        self.inputs = []
        self.outputs = []
        self.mailboxes = mailboxes
        self.accumulator = 0
        self.neg_flag = 0
        self.counter = 0
        self.potential_values = _potential_values
        self.max_cycles = max_cycles
        self.num_cycles = 0
        self.total_cycles = 0
        self.address_reg = 0
        self.halted = 0
        self.unexpected_outputs = []
        self.opcodes = {
            '0': self.hlt,
            '1': self.add,
            '2': self.sub,
            '3': self.sto,
            '5': self.lda,
            '6': self.br,
            '7': self.brz,
            '8': self.brp,
            '9': self.in_out,
        }

    def run_cycles(self):
        while self.num_cycles <= self.max_cycles and not self.halted:
            self.num_cycles += 1
            self.address_reg = self.counter
            self.counter += 1
            instruction = self.mailboxes[self.address_reg]
            self.opcodes[instruction[0]](int(instruction[1:]))
        return self.inputs, self.outputs, self.num_cycles

    def reset(self):
        # reset all registers (but not mailboxes)
        self.inputs = []
        self.outputs = []
        self.accumulator = 0
        self.neg_flag = 0
        self.counter = 0
        self.num_cycles = 0
        self.address_reg = 0
        self.halted = 0

    def hlt(self, _x):
        self.halted = 1

    def add(self, x):
        n = int(self.mailboxes[x])
        self.accumulator = (self.accumulator + n) % 1000

    def sub(self, x):
        n = int(self.mailboxes[x])
        if n > self.accumulator:
            self.neg_flag = 1
        self.accumulator = (self.accumulator - n) % 1000

    def sto(self, x):
        self.mailboxes[x] = str(self.accumulator)

    def lda(self, x):
        self.neg_flag = 0
        self.accumulator = int(self.mailboxes[x])

    def br(self, x):
        self.counter = x

    def brz(self, x):
        if self.accumulator == 0:
            self.counter = x

    def brp(self, x):
        if not self.neg_flag:
            self.counter = x

    def in_out(self, x):
        if x == 1:
            self.neg_flag = 0
            self.accumulator = (self.potential_values or [None]).pop(0)
            if self.accumulator is None:
                self.accumulator = int(input("Enter value: ")) % 1000
            self.inputs.append(self.accumulator)
        elif x == 2:
            self.outputs.append(self.accumulator)
