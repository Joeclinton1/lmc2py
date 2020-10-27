class LMC:
    def __init__(self, filepath, max_cycles):
        self.calc_reg = 0
        self.neg_flag = 0
        self.mailboxes = open(filepath).readlines()[1].split('%')[2].split(',')[:-1]
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
