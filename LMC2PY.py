import re
import sys


class LMC:
    def __init__(self, file_path, max_cycles):
        self.mailboxes = []
        self.calc_reg = 0
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

    def setup(self, file_path):
        # checks the extension and converts the file to mailbox machine code

        f = open(file_path).readlines()
        ext = file_path[-3:]
        if ext == 'lmc':
            self.mailboxes = f[1].split('%')[2].split(',')[:-1]
        elif ext == 'txt':
            assembly = [[s.strip() for s in re.split('[\t ]',re.sub('#.*','',line))][:3] for line in f if line.strip() != '' and line.strip()[0] != '#']

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
            (self.opcodes[instruction[0]])(int(instruction[1:]))
        print("Program executed in %d cycles." % self.num_cycles)

    def hlt(self, x):
        self.halted = 1

    def add(self, x):
        n = int(self.mailboxes[x])
        self.calc_reg = (self.calc_reg + n) % 1000

    def sub(self, x):
        n = int(self.mailboxes[x])
        if n > self.calc_reg:
            self.neg_flag = 1
        self.calc_reg = (self.calc_reg - n) % 1000

    def sto(self, x):
        self.mailboxes[x] = str(self.calc_reg)

    def lda(self, x):
        self.neg_flag = 0
        self.calc_reg = int(self.mailboxes[x])

    def br(self, x):
        self.counter = x

    def brz(self, x):
        if self.calc_reg == 0:
            self.counter = x

    def brp(self, x):
        if not self.neg_flag:
            self.counter = x

    def in_out(self, x):
        if x == 1:
            self.neg_flag = 0
            self.calc_reg = int(input('Enter value'))
        if x == 2:
            print(self.calc_reg)


file_path = ''
lmc = LMC(file_path, 50000)
lmc.print_mailboxes()
lmc.run_program()