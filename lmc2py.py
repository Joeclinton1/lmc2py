from parsing import args
from lmc_wrapper import LMCWrapper


filepath = args.file
checker_filepath = args.checker

if args.input is not None:
    potential_values = [int(value) % 1000 for value in args.input]
elif args.all:
    potential_values = [value for value in range(1000)]
else:
    potential_values = []

lmc_wrapper = LMCWrapper(filepath, potential_values, 50000, checker_filepath, args)
# lmc.print_mailboxes()
lmc_wrapper.run_batch()
