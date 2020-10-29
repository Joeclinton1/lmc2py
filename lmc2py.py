from parsing import args
from lmc import LMC


filepath = args.file
checker_filepath = args.checker

if args.input is not None:
    potential_values = [int(value) % 1000 for value in args.input]
elif args.all:
    potential_values = [value for value in range(1000)]
else:
    potential_values = []

lmc = LMC(filepath, potential_values, 50000, checker_filepath, args)
# lmc.print_mailboxes()
lmc.run_batch()
