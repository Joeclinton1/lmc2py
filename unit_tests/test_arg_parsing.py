import sys, os
sys.path.append(os.path.abspath(""))

import unittest
from arg_parsing import parse_args

class TestHelp(unittest.TestCase):
    def test_short_form(self):
        inp = ["-h"]
        with self.assertRaises(SystemExit) as cm:
            args = parse_args(inp)
        self.assertEqual(cm.exception.code,0)
    
    def test_long_form(self):
        inp = ["--help"]
        with self.assertRaises(SystemExit) as cm:
            args = parse_args(inp)
        self.assertEqual(cm.exception.code,0)

class TestFile(unittest.TestCase):
    def test_nothing(self):
        inp = []
        with self.assertRaises(SystemExit) as cm:
            args = parse_args(inp)
        self.assertEqual(cm.exception.code,2)
    
    def test_missing(self):
        inp = ["-a"]
        with self.assertRaises(SystemExit) as cm:
            args = parse_args(inp)
        self.assertEqual(cm.exception.code,2)

class TestAll(unittest.TestCase):
    def test_short_form(self):
        inp = ["FILE","-a"]
        args = parse_args(inp)
        self.assertTrue(args.all)
    
    def test_long_form(self):
        inp = ["FILE","--all"]
        args = parse_args(inp)
        self.assertTrue(args.all)
    
    def test_missing(self):
        inp = ["FILE"]
        args = parse_args(inp)
        self.assertFalse(args.all)
    
    def test_too_many_vals(self):
        inp = ["FILE","-a","TEXT"]
        with self.assertRaises(SystemExit) as cm:
            args = parse_args(inp)
        self.assertEqual(cm.exception.code,2)

class TestBatch(unittest.TestCase):
    def test_short_form(self):
        inp = ["FILE","-b","PATH"]
        args = parse_args(inp)
        self.assertEqual(args.batch,"PATH")
    
    def test_long_form(self):
        inp = ["FILE","--batch","PATH"]
        args = parse_args(inp)
        self.assertEqual(args.batch,"PATH")
    
    def test_missing(self):
        inp = ["FILE"]
        args = parse_args(inp)
        self.assertEqual(args.batch,None)

    def test_not_enough_vals(self):
        inp = ["FILE","-b"]
        with self.assertRaises(SystemExit) as cm:
            args = parse_args(inp)
        self.assertEqual(cm.exception.code,2)
    
    def test_too_many_vals(self):
        inp = ["FILE","-b","PATH","TEXT"]
        with self.assertRaises(SystemExit) as cm:
            args = parse_args(inp)
        self.assertEqual(cm.exception.code,2)

class TestInput(unittest.TestCase):
    def test_short_form(self):
        inp = ["FILE","-i","100"]
        args = parse_args(inp)
        self.assertEqual(args.input,[100])

    def test_long_form(self):
        inp = ["FILE","--input","100"]
        args = parse_args(inp)
        self.assertEqual(args.input,[100])
    
    def test_missing(self):
        inp = ["FILE"]
        args = parse_args(inp)
        self.assertEqual(args.input,None)

    def test_many(self):
        inp = ["FILE","-i","100","200","300"]
        args = parse_args(inp)
        self.assertEqual(args.input,[100,200,300])
    
    def test_not_enough_vals(self):
        inp = ["FILE","-i"]
        with self.assertRaises(SystemExit) as cm:
            args = parse_args(inp)
        self.assertEqual(cm.exception.code,2)
    
    def test_wrong_type_string(self):
        inp = ["FILE","-i","TEXT"]
        with self.assertRaises(SystemExit) as cm:
            args = parse_args(inp)
        self.assertEqual(cm.exception.code,2)
    
    def test_wrong_type_float(self):
        inp = ["FILE","-i","10.1"]
        with self.assertRaises(SystemExit) as cm:
            args = parse_args(inp)
        self.assertEqual(cm.exception.code,2)

class TestVerbose(unittest.TestCase):
    def test_short_form(self):
        inp = ["FILE","-v"]
        args = parse_args(inp)
        self.assertTrue(args.verbose)
    
    def test_long_form(self):
        inp = ["FILE","--verbose"]
        args = parse_args(inp)
        self.assertTrue(args.verbose)
    
    def test_missing(self):
        inp = ["FILE"]
        args = parse_args(inp)
        self.assertFalse(args.verbose)
    
    def test_too_many_vals(self):
        inp = ["FILE","-v","TEXT"]
        with self.assertRaises(SystemExit) as cm:
            args = parse_args(inp)
        self.assertEqual(cm.exception.code,2)

class TestQuiet(unittest.TestCase):
    def test_short_form(self):
        inp = ["FILE","-q"]
        args = parse_args(inp)
        self.assertTrue(args.quiet)
    
    def test_long_form(self):
        inp = ["FILE","--quiet"]
        args = parse_args(inp)
        self.assertTrue(args.quiet)
    
    def test_missing(self):
        inp = ["FILE"]
        args = parse_args(inp)
        self.assertFalse(args.quiet)
    
    def test_too_many_vals(self):
        inp = ["FILE","-q","TEXT"]
        with self.assertRaises(SystemExit) as cm:
            args = parse_args(inp)
        self.assertEqual(cm.exception.code,2)

class TestFeedback(unittest.TestCase):
    def test_short_form(self):
        inp = ["FILE","-f"]
        args = parse_args(inp)
        self.assertEqual(args.feedback,"")

    def test_long_form(self):
        inp = ["FILE","--feedback"]
        args = parse_args(inp)
        self.assertEqual(args.feedback,"")
    
    def test_missing(self):
        inp = ["FILE"]
        args = parse_args(inp)
        self.assertEqual(args.feedback,None)

    def test_with_path(self):
        inp = ["FILE","-f","PATH"]
        args = parse_args(inp)
        self.assertEqual(args.feedback,"PATH")

    def test_too_many_vals(self):
        inp = ["FILE","-f","PATH","TEXT"]
        with self.assertRaises(SystemExit) as cm:
            args = parse_args(inp)
        self.assertEqual(cm.exception.code,2)

class TestChecker(unittest.TestCase):
    def test_short_form(self):
        inp = ["FILE","-ch","PATH"]
        args = parse_args(inp)
        self.assertEqual(args.checker,"PATH")

    def test_long_form(self):
        inp = ["FILE","--checker","PATH"]
        args = parse_args(inp)
        self.assertEqual(args.checker,"PATH")
    
    def test_missing(self):
        inp = ["FILE"]
        args = parse_args(inp)
        self.assertEqual(args.checker,None)

    def test_not_enough_vals(self):
        inp = ["FILE","-ch"]
        with self.assertRaises(SystemExit) as cm:
            args = parse_args(inp)
        self.assertEqual(cm.exception.code,2)
    
    def test_too_many_vals(self):
        inp = ["FILE","-ch","PATH","TEXT"]
        with self.assertRaises(SystemExit) as cm:
            args = parse_args(inp)
        self.assertEqual(cm.exception.code,2)

class TestGraph(unittest.TestCase):
    def test_short_form(self):
        inp = ["FILE","-g"]
        args = parse_args(inp)
        self.assertTrue(args.graph)

    def test_long_form(self):
        inp = ["FILE","--graph"]
        args = parse_args(inp)
        self.assertTrue(args.graph)
    
    def test_missing(self):
        inp = ["FILE"]
        args = parse_args(inp)
        self.assertFalse(args.graph)
    
    def test_too_many_vals(self):
        inp = ["FILE","-g","TEXT"]
        with self.assertRaises(SystemExit) as cm:
            args = parse_args(inp)
        self.assertEqual(cm.exception.code,2)

class TestCombined(unittest.TestCase):
    def test_many(self):
        inp = ["FILE","-aqf"]
        args = parse_args(inp)
        self.assertTrue(args.all)
        self.assertTrue(args.quiet)
        self.assertEqual(args.feedback,"")
    
    def test_many_with_val(self):
        inp = ["FILE","-aqf","PATH"]
        args = parse_args(inp)
        self.assertTrue(args.all)
        self.assertTrue(args.quiet)
        self.assertEqual(args.feedback,"PATH")
    
    def test_exclusive_ai(self):
        inp = ["FILE","-a","-i","100"]
        with self.assertRaises(SystemExit) as cm:
            args = parse_args(inp)
        self.assertEqual(cm.exception.code,2)
    
    def test_exclusive_ab(self):
        inp = ["FILE","-a","-b","PATH"]
        with self.assertRaises(SystemExit) as cm:
            args = parse_args(inp)
        self.assertEqual(cm.exception.code,2)
    
    def test_exclusive_bi(self):
        inp = ["FILE","-b","PATH","-i","100"]
        with self.assertRaises(SystemExit) as cm:
            args = parse_args(inp)
        self.assertEqual(cm.exception.code,2)

    def test_exclusive_vq(self):
        inp = ["FILE","-v","-q"]
        with self.assertRaises(SystemExit) as cm:
            args = parse_args(inp)
        self.assertEqual(cm.exception.code,2)

if __name__ == '__main__':
    unittest.main()
