import os
import re
import sys
import ntpath
import argparse
from importlib import import_module
import importlib.util

# streamlining the CLI
parser = argparse.ArgumentParser(usage='%(prog)s [-h] file [options]',
                                 description="this is a single file python script which runs the 'Little Minion Computer' .lmc and .txt files in python, to save you having to wait for it to run")
parser.add_argument("file",
                    help="the file to execute; can be either LMC assembly (.txt or .asm) or compiled LMC machine code (.lmc)")

# input arguments
igroup = parser.add_mutually_exclusive_group()
igroup.add_argument("-a", "--all", action="store_true",
                    help="run the program for all inputs between 0 and 999 (recommend also using -q)")
# not implemented yet
# group.add_argument("-b", "--batch", help="a batch process file to test the program against")
igroup.add_argument("-i", "--input", nargs="*", metavar="VAL",
                    help="one or more inputs to supply to the program, in order")

# verbosity arguments
vgroup = parser.add_mutually_exclusive_group()
vgroup.add_argument("-v", "--verbose", action="store_true", help="run the program with high verbosity")
vgroup.add_argument("-q", "--quiet", action="store_true",
                    help="run the program with minimum terminal output; setting this flag without one of the following will result in no output at all")

# output arguments
# not implemented yet
# parser.add_argument("-o", "--compile", nargs="?", default=None, const="", metavar="FILE", help="output the compiled LMC machine code to a file")
# not implemented yet
# parser.add_argument("-c", "--csv", nargs="?", default=None, const="", metavar="FILE", help="save the process results to a .csv file")
parser.add_argument("-f", "--feedback", nargs="?", default=None, const="", metavar="FILE",
                    help="save the process results to a .txt file")

parser.add_argument("-ch", "--checker", help="filepath to file containing checker function")
args = parser.parse_args()


class LMC:

    def __init__(self, _filepath, potential_values, max_cycles=50000, checker_file_path=None):
        self.checker = None
        self.filename = ntpath.basename(_filepath)
        self.inputs = []
        self.outputs = []
        self.feedback = ""
        self.mailboxes = []
        self.accumulator = 0
        self.neg_flag = 0
        self.counter = 0
        self.potential_values = potential_values
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

        self.setup(_filepath, checker_file_path)

    def setup(self, _filepath, checker_file_path):
        # checks the extension and converts the file to mailbox machine code

        # read checker file
        if checker_file_path:
            checker_name = ntpath.basename(checker_file_path)
            #abs_path = os.path.abspath(checker_file_path)
            spec = importlib.util.spec_from_file_location(checker_name, checker_file_path)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            self.checker = foo.checker

        # read lmc file
        f = open(_filepath).readlines()
        os.chdir(ntpath.dirname(_filepath) or '.')

        ext = file_path[-3:]
        if ext.lower() == 'lmc':
            self.mailboxes = f[1].split('%')[2].split(',')[:-1]
        elif ext.lower() in ['txt', 'asm']:
            assembly = [[s.strip() for s in re.split('\\s+', re.sub('#.*', '', line))][:3] for line in f if
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
                print("The program failed %d tests."%len(self.unexpected_outputs))
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
            expect_output_msg = f"Expected Outputs(s):  {', '.join(str(val) for val in expected_outputs)}\n"
            if self.outputs != expected_outputs:
                self.unexpected_outputs.append((self.inputs,  expected_outputs, self.outputs))

        msg = (f"Input(s):  {', '.join(str(val) for val in self.inputs)}\n"
               f"Output(s): {', '.join(str(val) for val in self.outputs)}\n"
               f"{expect_output_msg}"
               f"Program executed in {self.num_cycles} cycles, cumulative {self.total_cycles}.\n")
        self.feedback += msg
        if not args.quiet:
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
        if args.feedback != None:
            with open(args.feedback or f"feedback_{self.filename}", 'w') as f:
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


file_path = args.file
checker_file_path = args.checker

# moved this out here to avoid parsing args inside the class as much as possible
# also, as much as I like the generator syntax, I need to be able to see if there's any left
if args.input != None:
    potential_values = [int(value) % 1000 for value in args.input]
elif args.all:
    potential_values = [value for value in range(1000)]
else:
    potential_values = []

lmc = LMC(file_path, potential_values, 50000, checker_file_path)
# lmc.print_mailboxes()
lmc.run_batch()