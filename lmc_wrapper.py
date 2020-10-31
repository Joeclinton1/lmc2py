"""
Handles the high-level running of LMC programs.
"""

import file_parser
from lmc import LMC
import plot

import importlib.util
import ntpath
import os
import re
import sys


class LMCWrapper:
    def __init__(self, _filepath, _potential_values, max_cycles=50000, **kwargs):

        self.is_quiet = kwargs.get('quiet', None)
        self.is_verbose = kwargs.get('verbose', None)
        self.batch_fp = kwargs.get('batch_fp', None)
        self.checker_fp = kwargs.get('checker_fp', None)
        self.has_graph = kwargs.get('graph', None)
        self.has_feedback = kwargs.get('feedback', None)

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

        self.setup(_filepath)

    def setup(self, filepath):
        """Checks the extension and converts the file into mailbox machine code."""

        # Adds checker function from file or from batch
        if self.batch_fp:
            self.batch_tests, self.potential_values = file_parser.parse_batch_test_file(self.batch_fp)
            self.checker = self.get_batch_outputs
        elif self.checker_fp:
            self.checker = self.get_checker(self.checker_fp)

        # compiles mailboxes from file
        self.mailboxes, num_mailboxes = file_parser.get_mailboxes_from_file(filepath)
        print("Compiled program uses %d/100 mailboxes." % num_mailboxes)
        self.lmc = LMC(self.potential_values, self.mailboxes, self.max_cycles)

        # change working directory to filepath so that feedback outputs in right location.
        os.chdir(ntpath.dirname(filepath) or '.')

    @staticmethod
    def get_checker(checker_filepath):
        """Gets the checker function at the given file_path."""
        os.chdir(os.path.dirname(__file__))
        spec = importlib.util.spec_from_file_location("divisors.py", checker_filepath)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        return foo.checker

    def get_batch_outputs(self, _inputs):
        return self.batch_tests.pop(0)[2]

    def print_mailboxes(self):
        print(self.mailboxes)

    def run_batch(self):
        """
        Runs lmc program with given inputs (if any), until all inputs have been used.
        Checks the outputs to ensure they match those expected (--checker used).
        Plots a graph of input against cycles taken (--graph used).
        """
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

        if self.has_graph:
            plot.plot_graph(self.inputs_and_cycles)

    def run_once(self):
        """Runs the program once, without resetting."""
        self.run_program()
        self.write_feedback()

    def run_program(self):
        """Runs the lmc program."""
        if self.batch_tests:
            self.feedback += f"Attempting to run test {self.batch_tests[0][0]}:\n"
            self.lmc.max_cycles = self.batch_tests[0][3]

        inputs, outputs, num_cycles = self.lmc.run_cycles()
        self.lmc.reset()
        self.total_cycles += num_cycles
        self.store_feedback_msg(inputs, outputs, num_cycles)

        # matches inputs with number of cycles taken for that input
        if len(inputs) == 1:
            self.inputs_and_cycles[inputs[0]] = num_cycles
        elif len(inputs) > 1:
            self.inputs_and_cycles[tuple(inputs)] = num_cycles

    def store_feedback_msg(self, inputs, outputs, num_cycles):
        """Generates a report mentioning inputs, expected outputs (with checker) and actual outputs."""
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

        if not self.is_quiet:
            print(msg)

    def write_feedback(self):
        """Write feedback to a txt file."""
        if self.has_feedback is not None:
            with open(self.feedback or f"feedback_{self.filename}", 'w') as f:
                f.write(self.feedback)
