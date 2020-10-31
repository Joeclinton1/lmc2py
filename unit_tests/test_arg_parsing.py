import unittest
import arg_parsing

class TestShortForm(unittest.TestCase):
    def test_all(self):
        inp = ["FILE","-a"]
        args = arg_parsing.parse_args(inp)
        self.assertTrue(args.all)
    
    def test_quiet(self):
        inp = ["FILE","-q"]
        args = arg_parsing.parse_args(inp)
        self.assertTrue(args.quiet)
    
    def test_graph(self):
        inp = ["FILE","-g"]
        args = arg_parsing.parse_args(inp)
        self.assertTrue(args.graph)