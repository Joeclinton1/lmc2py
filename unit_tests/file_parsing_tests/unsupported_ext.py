f"""
# Enter assembler code here
#
# To add comments begin lines with #
# Code lines have 3 entries separated by tabs
# > First an optional label,
# > second an instruction mnemonic, and
# > third an address label if required.
#
# Valid mnemonics are:
# HLT, ADD, SUB, STO, LDA,
# BR, BRZ, BRP, IN, OUT, DAT

IN  # comment to ignore 1
OUT
ADD
5
LDA
LDA
DAT  # comment to ignore 2
SUB
5
STO
DAT
BRZ
LDA
BRP
LDA
BR
HLT

# This is skipped
# this is also skipped

HLT
HLT
5
DAT
005
DAT
DAT
"""
