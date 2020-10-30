"""
Handles the high-level running of LMC programs.
"""

from lmc import LMC
import importlib.util
import ntpath
import sys
import os
import re
import plot


class LMCWrapper:
    def __init__(self, _filepath, _potential_values, max_cycles=50000, args=None):
        self.args = args
        self.lmc = None
        self.checker = None
        self.batch_tests = None
        self.filename = ntpath.basename(_filepath)
        self.inputs_and_cycles = {}
        self.feedback = ""
        self.mailboxes = []
        self.potential_values = _potential_values
        self.max_cycles = max_cycles
        self.total_cycles = 0
        self.unexpected_outputs = []

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

        self.setup(_filepath, args.checker, args.batch)

    def setup(self, filepath, _checker_filepath, _batch_filepath):
        # checks the extension and converts the file to mailbox machine code

        # read checker file
        if _batch_filepath:
            self.setup_batch(_batch_filepath)
            self.checker = self.get_batch_outputs
        elif _checker_filepath:
            self.checker = self.get_checker(_checker_filepath)

        # read lmc file
        f = open(filepath).readlines()
        os.chdir(ntpath.dirname(filepath) or '.')
        ext = filepath[-3:]
        self.mailboxes = self.get_mailboxes_from_file(f, ext)
        print("Compiled program uses %d/100 mailboxes." % len(self.mailboxes))
        self.lmc = LMC(self.potential_values, self.mailboxes, self.max_cycles)

    @staticmethod
    def get_checker(checker_filepath):
        # gets the checker function at the given file_path.
        os.chdir(os.path.dirname(__file__))
        spec = importlib.util.spec_from_file_location("divisors.py", checker_filepath)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        return foo.checker

    def setup_batch(self, batch_filepath):
        with open(batch_filepath) as f:
            lines = (line for line in f.readlines() if len(line.strip()) != 0)

        self.batch_tests = []
        for line in lines:
            try:
                label, inputs, outputs, cycles = line.strip().split(';')
                inputs = [int(val) for val in inputs.split(',')]
                outputs = [int(val) for val in outputs.split(',')]
                cycles = int(cycles)

                self.potential_values += inputs
            except ValueError:
                raise SyntaxError("Test file is not formatted correctly, please check it and try again.")
            self.batch_tests.append((label, inputs, outputs, cycles))

    def get_batch_outputs(self, _inputs):
        return self.batch_tests.pop(0)[2]

    def get_mailboxes_from_file(self, file, ext):
        mailboxes = []
        if ext.lower() == 'lmc':
            mailboxes = file[1].split('%')[2].split(',')[:-1]
        elif ext.lower() in ['txt', 'asm']:
            assembly = [[s.strip() for s in re.split('\\s+', re.sub('#.*', '', line))][:3]
                        for line in file if line.strip() != '' and line.strip()[0] != '#']

            # ensure that there are no more than 100 registers
            if len(assembly) > 100:
                raise IndexError("More than 100 registers used")

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
                    if val in pointers:
                        machine_code = self.assembly_codes[opcode] + pointers[val].zfill(2)
                    else:
                        raise NameError(f"No variable of name '{val}' initiated with DAT")
                mailboxes.append(machine_code)
        else:
            sys.exit('LMC2PY requires a .lmc or assembly .txt or .asm file.')
        return mailboxes

    def print_mailboxes(self):
        print(self.mailboxes)

    def run_batch(self):
        if len(self.potential_values) == 0:
            self.run_once()

        # run the program repeatedly for multiple input values
        while len(self.potential_values) > 0:
            self.run_program()

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

        if self.args.graph:
            plot.plot_graph(self.inputs_and_cycles)

    def run_once(self):
        # run the program once, without resetting
        self.run_program()
        self.write_feedback()

    def run_program(self):
        if self.batch_tests:
            self.feedback += f"Attempting to run test {self.batch_tests[0][0]}:\n"
            self.lmc.max_cycles = self.batch_tests[0][3]

        inputs, outputs, num_cycles = self.lmc.run_cycles()
        self.lmc.reset()
        self.total_cycles += num_cycles
        self.store_feedback_msg(inputs, outputs, num_cycles)

    def store_feedback_msg(self, inputs, outputs, num_cycles):
        expect_output_msg = ''
        if self.checker:
            expected_outputs = self.checker(inputs)
            expect_output_msg = f"Expected Outputs(s):\t{', '.join(str(val) for val in expected_outputs)}"
            if outputs != expected_outputs:
                self.unexpected_outputs.append((inputs, expected_outputs, outputs))

        msg = (f"Input(s):\t\t{', '.join(str(val) for val in inputs)}\n"
               f"{expect_output_msg}\n"
               f"Actual Output(s):\t{', '.join(str(val) for val in outputs)}\n"
               f"Program executed in {num_cycles} cycles, cumulative {self.total_cycles}.\n\n")
        self.feedback += msg

        # matches inputs with number of cycles taken for that input
        if len(inputs) == 1:
            self.inputs_and_cycles[inputs[0]] = num_cycles
        elif len(inputs) > 1:
            self.inputs_and_cycles[tuple(inputs)] = num_cycles

        if not self.args.quiet:
            print(msg)

    def write_feedback(self):
        # write feedback to a txt file
        if self.args.feedback is not None:
            with open(self.args.feedback or f"feedback_{self.filename}", 'w') as f:
                f.write(self.feedback)
