"""
Main controller of lmc2py. From here lmc_wrapper and parsing is called.
"""

from arg_parsing import args
from lmc_wrapper import LMCWrapper


filepath = args.file

if args.input is not None:
    potential_values = [int(value) % 1000 for value in args.input]
elif args.all:
    potential_values = [value for value in range(1000)]
else:
    potential_values = []

lmc_wrapper = LMCWrapper(filepath, potential_values, 50000,
                         quiet =args.quiet,
                         verbose = args.verbose,
                         batch_fp = args.batch,
                         checker_fp =  args.checker,
                         graph = args.graph,
                         feedback=args.feedback
                         )
# lmc.print_mailboxes()
lmc_wrapper.run_batch()
