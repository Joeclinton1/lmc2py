from lmc_wrapper import LMCWrapper

import unittest
import textwrap
import sys
import os


class TestChecker(unittest.TestCase):
    def setUp(self):
        self.checker_files = [
            "divisors"
        ]

    def test_get_checkers(self):
        for file_path in self.checker_files:
            self.checker = LMCWrapper.get_checker("checks/%s.py" % file_path)
            os.chdir(os.path.dirname(__file__))
            self.assertTrue(callable(self.checker))

    def test_checkers_return_type(self):
        for file_path in self.checker_files:
            self.checker = LMCWrapper.get_checker("checks/%s.py" % file_path)
            os.chdir(os.path.dirname(__file__))
            for i in range(999):
                valid_output = isinstance(self.checker([i]), list) or (self.checker([i]) is None)
                self.assertTrue(valid_output)


class TestRunProgram(unittest.TestCase):
    def setUp(self):
        self.lmc_wrapper = LMCWrapper("unit_tests/file_parsing_tests/all_functions.lmc", [55],
                                      quiet=True)

    def test_run_program(self):
        self.lmc_wrapper.run_program()
        self.assertEqual(self.lmc_wrapper.total_cycles, 10)
        self.assertEqual(self.lmc_wrapper.inputs_and_cycles, {55: 10})


class TestRunBatch(unittest.TestCase):
    def setUp(self):
        self.lmc_wrapper = LMCWrapper("unit_tests/file_parsing_tests/all_functions.lmc", [1, 5, 19, 25, 999],
                                      quiet=True)

    def test_run_batch(self):
        self.lmc_wrapper.run_batch()
        self.assertEqual(self.lmc_wrapper.potential_values, [])
        self.assertEqual(self.lmc_wrapper.total_cycles, 4026)


class TestStoreFeedbackMessage(unittest.TestCase):
    def setUp(self):
        self.lmc_wrapper = LMCWrapper("unit_tests/file_parsing_tests/all_functions.lmc", [], quiet=True)
        self.correct_feedback = """\
        Input(s):		1, 2, 3, 4\n
        Actual Output(s):	1, 2, 3, 4
        Program executed in 123 cycles, cumulative 0.\n
        """
        self.correct_feedback = textwrap.dedent(self.correct_feedback)

    def test_store_feedback_message(self):
        self.lmc_wrapper.store_feedback_msg([1, 2, 3, 4], [1, 2, 3, 4], 123)
        self.assertEqual(self.lmc_wrapper.feedback, self.correct_feedback)


sys.path.append(os.path.abspath(""))
if __name__ == '__main__':
    unittest.main()
