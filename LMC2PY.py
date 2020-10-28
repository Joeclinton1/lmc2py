import os
import re
import sys
import ntpath


class LMC:
    potential_values = (int(value) for value in sys.argv[2:])

    def __init__(self, _filepath, max_cycles):
        self.filename = ntpath.basename(file_path)
        self.inputs = []
        self.outputs = []
        self.mailboxes = []
        self.accumulator = 0
        self.neg_flag = 0
        self.counter = 0
        self.max_cycles = max_cycles
        self.num_cycles = 0
        self.address_reg = 0
        self.halted = 0
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

        self.assembly_codes = {
            'HLT': '000',
            'ADD': '1',
            'SUB': '2',
            'STO': '3',
            'LDA': '5',
            'BR': '6',
            'BRZ': '7',
            'BRP': '8',
            'IN': '901',
            'OUT': '902'
        }

        self.setup(file_path)

    def setup(self, _filepath):
        # checks the extension and converts the file to mailbox machine code

        f = open(file_path).readlines()
        file_dir = ntpath.dirname(_filepath)
        os.chdir(file_dir or '.')
        ext = file_path[-3:]
        if ext == 'lmc':
            self.mailboxes = f[1].split('%')[2].split(',')[:-1]
        elif ext == 'txt':
            assembly = [[s.strip() for s in re.split('[\t ]', re.sub('#.*', '', line))][:3] for line in f if
                        line.strip() != '' and line.strip()[0] != '#']

            # get pointers
            pointers = {'': ''}
            for box_num, cmd in enumerate(assembly):
                if cmd[0] != '':
                    pointers[cmd[0]] = str(box_num)

            # convert assembly to machine code
            for cmd in assembly:
                opcode = cmd[1]
                val = cmd[2] if len(cmd) == 3 else ''
                if opcode == 'DAT':
                    machine_code = '000' if val == '' else val
                else:
                    machine_code = self.assembly_codes[opcode] + pointers[val]
                self.mailboxes.append(machine_code)
        else:
            sys.exit('LMC2PY requires a .lmc or assembly .txt file.')

    def print_mailboxes(self):
        print(self.mailboxes)

    def run_program(self):
        while self.num_cycles <= self.max_cycles and not self.halted:
            self.num_cycles += 1
            self.address_reg = self.counter
            self.counter += 1
            instruction = self.mailboxes[self.address_reg]
            self.opcodes[instruction[0]](int(instruction[1:]))

        with open(f"feedback_{self.filename}", 'w') as f:
            msg = (f"Input(s):  {', '.join(str(val) for val in self.inputs)}\n"
                   f"Output(s): {', '.join(str(val) for val in self.outputs)}\n"
                   f"Program executed in {self.num_cycles} cycles.")
            f.write(msg)
            print(msg)

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
            self.accumulator = next(self.potential_values, None)
            if self.accumulator is None:
                self.accumulator = int(input("Enter value: "))
            self.inputs.append(self.accumulator)
        elif x == 2:
            self.outputs.append(self.accumulator)


if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    file_path = input("Enter path: ")

lmc = LMC(file_path, 50000)
# lmc.print_mailboxes()
lmc.run_program()
