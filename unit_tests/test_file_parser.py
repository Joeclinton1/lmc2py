import unittest
import file_parser
import os
import json


def reset_directory():
    os.chdir(os.path.dirname(__file__))

class TestMailboxesFromFile(unittest.TestCase):
    def test_unsupported_extension(self):
        lmc_filepath = "unit_tests/file_parsing_tests/unsupported_ext.py"
        with self.assertRaises(file_parser.UnsupportedExtensionError):
            file_parser.get_mailboxes_from_file(lmc_filepath)

class TestParseLMC(unittest.TestCase):
    def setUp(self):
        reset_directory()
        self.correct_mailboxes = ['901', '902', '110', '511', '210', '311', '703', '803', '609', '000', '005']
        self.correct_mailboxes += ['000'] * 89

    def test_lmc(self):
        lmc_file_path = "unit_tests/file_parsing_tests/all_functions.lmc"
        mailboxes= file_parser.parse_lmc_file(lmc_file_path)

        self.assertEqual(mailboxes, self.correct_mailboxes)
        os.chdir(os.path.dirname(__file__))

    def test_broken_file_lmc(self):
        lmc_file_path = "unit_tests/file_parsing_tests/broken_file.lmc"

        with self.assertRaises(file_parser.ParseError):
            file_parser.parse_lmc_file(lmc_file_path)


class TestParseAssembly(unittest.TestCase):
    def setUp(self):
        reset_directory()
        self.correct_mailboxes = ['901', '902', '110', '511', '210', '311', '703', '803', '609', '000', '005']
        self.correct_mailboxes += ['000'] * 89

    def test_txt(self):
        txt_file_path = "unit_tests/file_parsing_tests/all_functions.txt"
        mailboxes, num_mailboxes = file_parser.parse_assembly_file(txt_file_path)
        self.assertEqual(mailboxes, self.correct_mailboxes)
        os.chdir(os.path.dirname(__file__))

    def test_unsupported_assembly_code(self):
        txt_file_path = "unit_tests/file_parsing_tests/unsupported_assembly_code.txt"
        correct_error = "Assembly file contains unsupported assembly code at line 2: MULT"
        with self.assertRaisesRegex(file_parser.ParseError, correct_error):
            file_parser.parse_assembly_file(txt_file_path)

    def test_missing_tab(self):
        txt_file_path = "unit_tests/file_parsing_tests/missing_tab.txt"
        correct_error = "Assembly file is missing tab space at line 1"
        with self.assertRaisesRegex(file_parser.ParseError, correct_error):
            file_parser.parse_assembly_file(txt_file_path)


class TestParseBatch(unittest.TestCase):
    def setUp(self):
        reset_directory()
        with open('correct_outputs/correct_batch_tests.json') as json_file:
            self.correct_batch_test = [tuple(sub_list) for sub_list in json.load(json_file)]
        self.correct_potential_values = [0, 1, 60, 512, 360, 720, 840, 837, 899, 979, 997]

    def test_parse_batch_file(self):
        batch_tests, potential_values = file_parser.parse_batch_test_file("unit_tests/file_parsing_tests/batch_test.txt")
        self.assertEqual(self.correct_batch_test, batch_tests)
        self.assertEqual(self.correct_potential_values, potential_values)

    def test_broken_batch_file(self):
        batch_file_path = "unit_tests/file_parsing_tests/broken_batch_test.txt"
        with self.assertRaises(file_parser.ParseError):
            file_parser.parse_batch_test_file(batch_file_path)
