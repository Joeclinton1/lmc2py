import argparse


# streamlining the CLI
parser = argparse.ArgumentParser(
    usage='%(prog)s [-h] file [options]',
    description="this is a single file python script which runs the 'Little Minion Computer' "
                ".lmc and .txt files in python, to save you having to wait for it to run")

parser.add_argument("file",
                    help="the file to execute; can be either LMC assembly (.txt or .asm) "
                         "or compiled LMC machine code (.lmc)")

# input arguments; commented code is not yet implemented
i_group = parser.add_mutually_exclusive_group()
i_group.add_argument("-a", "--all", action="store_true",
                     help="run the program for all inputs between 0 and 999 (recommend also using -q)")
# i_group.add_argument("-b", "--batch",
#                      help="a batch process file to test the program against")
i_group.add_argument("-i", "--input", nargs="*", metavar="VAL",
                     help="one or more inputs to supply to the program, in order")

# verbosity arguments
v_group = parser.add_mutually_exclusive_group()
v_group.add_argument("-v", "--verbose", action="store_true",
                     help="run the program with high verbosity")
v_group.add_argument("-q", "--quiet", action="store_true",
                     help="run the program with minimum terminal output; setting this flag without one of the "
                          "following will result in no output at all")

# output arguments; commented code is not yet implemented
# parser.add_argument("-o", "--compile", nargs="?", default=None, const="", metavar="FILE",
#                     help="output the compiled LMC machine code to a file")
# parser.add_argument("-c", "--csv", nargs="?", default=None, const="", metavar="FILE",
#                     help="save the process results to a .csv file")
parser.add_argument("-f", "--feedback", nargs="?", default=None, const="", metavar="FILE",
                    help="save the process results to a .txt file")

parser.add_argument("-ch", "--checker", help="filepath to file containing checker function")

parser.add_argument("-g", "--graph", action="store_true",
                    help="generate graph matching input to number of cycles")
args = parser.parse_args()
