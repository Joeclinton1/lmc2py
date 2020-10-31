import unittest
import file_parser
import os
import json


# TODO: Test that the correct errors are raised when files are improperly formatted
class TestMailboxesFromFile(unittest.TestCase):
    def setUp(self):
        self.correct_mailboxes = ['901', '902', '110', '511', '210', '311', '703', '803', '609', '000', '005']
        self.correct_mailboxes += ['000'] * 89

    def test_lmc(self):
        lmc_filepath = "unit_tests/file_parsing_tests/test_all_functions.lmc"
        mailboxes, num_mailboxes = file_parser.get_mailboxes_from_file(lmc_filepath)
        self.assertEqual(mailboxes, self.correct_mailboxes)
        os.chdir(os.path.dirname(__file__))

    def test_txt(self):
        txt_file_path = "unit_tests/file_parsing_tests/test_all_functions.txt"
        mailboxes, num_mailboxes = file_parser.get_mailboxes_from_file(txt_file_path)
        self.assertEqual(mailboxes, self.correct_mailboxes)
        os.chdir(os.path.dirname(__file__))


class TestParseBatch(unittest.TestCase):
    def setUp(self):
        with open('correct_outputs/correct_batch_tests.json') as json_file:
            self.correct_batch_test = [tuple(sub_list) for sub_list in json.load(json_file)]
        self.correct_potential_values = [0, 1, 60, 512, 360, 720, 840, 837, 899, 979, 997]

    def test_parse_batch_file(self):
        batch_tests, potential_values = file_parser.parse_batch_test_file("file_parsing_tests/test_batch_test.txt")
        self.assertEqual(self.correct_batch_test, batch_tests)
        self.assertEqual(self.correct_potential_values, potential_values)
