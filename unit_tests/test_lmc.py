import unittest
from unittest.mock import patch
from lmc import LMC


class TestInput(unittest.TestCase):
    def setUp(self):
        self.lmc = LMC([], [])

    @patch('lmc.get_input', return_value='5')
    def test_in(self, input):
        self.lmc.in_out(1)
        self.assertEqual(self.lmc.accumulator, 5)
        self.assertEqual(self.lmc.inputs, [5])
        self.assertFalse(self.lmc.neg_flag)

    @patch('lmc.get_input', return_value='-1')
    def test_in_less_than_0(self, input):
        self.lmc.in_out(1)
        self.assertEqual(self.lmc.accumulator, 999)

    @patch('lmc.get_input', return_value='1000')
    def test_in_greater_than_999(self, input):
        self.lmc.in_out(1)
        self.assertEqual(self.lmc.accumulator, 0)

    def in_potential_values(self):
        lmc = LMC([1,5,3], [])
        lmc.in_out(1)
        self.assertEqual(lmc.accumulator, 1)
        lmc.in_out(1)
        self.assertEqual(lmc.accumulator, 5)
        lmc.in_out(1)
        self.assertEqual(lmc.accumulator, 3)


class TestLda(unittest.TestCase):
    def setUp(self):
        self.lmc = LMC([], [555])

    def test_lda(self):
        self.lmc.lda(0)
        self.assertEqual(self.lmc.accumulator, 555)
        self.assertFalse(self.lmc.neg_flag)


class TestBrz(unittest.TestCase):
    def setUp(self):
        self.lmc = LMC([], [])

    def test_0(self):
        self.lmc.accumulator = 0
        self.lmc.brz(5)
        self.assertEqual(self.lmc.counter, 5)

    def test_not_0(self):
        self.lmc.accumulator = 1
        self.lmc.brz(5)
        self.assertEqual(self.lmc.counter, 0)


class TestBrp(unittest.TestCase):
    def setUp(self):
        self.lmc = LMC([], [])

    def test_0(self):
        self.lmc.accumulator = 0
        self.lmc.brp(5)
        self.assertEqual(self.lmc.counter, 5)

    def test_greater_than_0(self):
        self.lmc.accumulator = 1
        self.lmc.brp(5)
        self.assertEqual(self.lmc.counter, 5)

    def test_neg_flag(self):
        self.lmc.neg_flag = 1
        self.lmc.brp(5)
        self.assertEqual(self.lmc.counter, 0)


class TestSub(unittest.TestCase):
    def setUp(self):
        self.lmc = LMC([], [555])

    def test_b_less_than_a(self):
        self.lmc.accumulator = 999
        self.lmc.sub(0)
        self.assertEqual(self.lmc.accumulator, 444)
        self.assertFalse(self.lmc.neg_flag)

    def test_b_greater_than_a(self):
        self.lmc.accumulator = 100
        self.lmc.sub(0)
        self.assertEqual(self.lmc.accumulator, 545)
        self.assertTrue(self.lmc.neg_flag)


class TestAdd(unittest.TestCase):
    def setUp(self):
        self.lmc = LMC([], [555])

    def test_add(self):
        self.lmc.accumulator = 100
        self.lmc.add(0)
        self.assertEqual(self.lmc.accumulator, 655)

    def test_add_overflow(self):
        self.lmc.accumulator = 999
        self.lmc.add(0)
        self.assertEqual(self.lmc.accumulator, 554)


class TestRunCycles(unittest.TestCase):
    def setUp(self):
        self.lmc = LMC([55], [901, 902, 105, 902,000, 100])

    def TestExampleProgram(self):
        inputs, outputs, num_cycles = self.lmc.run_cycles()
        self.assertEqual(inputs, [55])
        self.assertEqual(outputs, [55,155])
        self.assertEqual(num_cycles, 5)
        self.assertEqual(self.lmc.address_reg, 5)
        self.assertEqual(self.lmc.counter, 6)
        self.assertEqual(self.lm.accumulator, 5)
        self.assertTrue(self.lmc.halted)

if __name__ == '__main__':
    unittest.main()
