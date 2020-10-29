import importlib.util
import ntpath
import sys
import os
import re


class LMC:
    def __init__(self, _filepath, _potential_values, max_cycles=50000, _checker_filepath=None, args=None):
        self.args = args
        self.checker = None
        self.filename = ntpath.basename(_filepath)
        self.inputs = []
        self.outputs = []
        self.feedback = ""
        self.mailboxes = []
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

        self.setup(_filepath, _checker_filepath)

    def setup(self, _filepath, _checker_filepath):
        # checks the extension and converts the file to mailbox machine code

        # read checker file
        if _checker_filepath:
            os.chdir(os.path.dirname(__file__))
            # abs_path = os.path.abspath(checker_file_path)
            spec = importlib.util.spec_from_file_location("divisors.py", _checker_filepath)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            self.checker = foo.checker

        # read lmc file
        f = open(_filepath).readlines()
        os.chdir(ntpath.dirname(_filepath) or '.')

        ext = _filepath[-3:]
        if ext.lower() == 'lmc':
            self.mailboxes = f[1].split('%')[2].split(',')[:-1]
        elif ext.lower() in ['txt', 'asm']:
            assembly = [[s.strip() for s in re.split('\\s+', re.sub('#.*', '', line))][:3]
                        for line in f if line.strip() != '' and line.strip()[0] != '#']

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
                    machine_code = '000' if val == '' else val.zfill(3)
                elif opcode in ["IN", "OUT", "HLT"]:
                    machine_code = self.assembly_codes[opcode]
                else:
                    machine_code = self.assembly_codes[opcode] + pointers[val].zfill(2)
                self.mailboxes.append(machine_code)
        else:
            sys.exit('LMC2PY requires a .lmc or assembly .txt or .asm file.')

    def print_mailboxes(self):
        print(self.mailboxes)

    def run_batch(self):
        if len(self.potential_values) == 0:
            self.run_once()

        # run the program repeatedly for multiple input values
        while len(self.potential_values) > 0:
            self.run_program()
            self.reset()

        if self.checker:
            if len(self.unexpected_outputs) == 0:
                print("The program passed all tests.")
            else:
                print("The program failed %d tests." % len(self.unexpected_outputs))
                for inputs, expected_outputs, outputs in self.unexpected_outputs:
                    inputs = ', '.join(str(val) for val in inputs)
                    expected_outputs = ', '.join(str(val) for val in expected_outputs)
                    outputs = ', '.join(str(val) for val in outputs)
                    print("inputs: %s, expected_output: %s, output: %s" % (inputs, expected_outputs, outputs))
        self.write_feedback()

    def run_once(self):
        # run the program once, without resetting
        self.run_program()
        self.write_feedback()

    def run_program(self):
        while self.num_cycles <= self.max_cycles and not self.halted:
            self.num_cycles += 1
            self.address_reg = self.counter
            self.counter += 1
            instruction = self.mailboxes[self.address_reg]
            self.opcodes[instruction[0]](int(instruction[1:]))

        self.total_cycles += self.num_cycles

        expect_output_msg = ''
        if self.checker:
            expected_outputs = self.checker(self.inputs)
            expect_output_msg = f"Expected Outputs(s):\t{', '.join(str(val) for val in expected_outputs)}"
            if self.outputs != expected_outputs:
                self.unexpected_outputs.append((self.inputs,  expected_outputs, self.outputs))

        msg = (f"Input(s):\t\t{', '.join(str(val) for val in self.inputs)}\n"
               f"{expect_output_msg}\n"
               f"Actual Output(s):\t{', '.join(str(val) for val in self.outputs)}\n"
               f"Program executed in {self.num_cycles} cycles, cumulative {self.total_cycles}.\n\n")
        self.feedback += msg
        if not self.args.quiet:
            print(msg)

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

    def write_feedback(self):
        # write feedback to a txt file
        if self.args.feedback is not None:
            with open(self.args.feedback or f"feedback_{self.filename}", 'w') as f:
                f.write(self.feedback)

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
