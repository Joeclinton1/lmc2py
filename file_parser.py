import os
import re


class ParseError(Exception):
    pass


class UnsupportedExtensionError(Exception):
    pass


assembly_codes = {
    'HLT': '000',
    'ADD': '1',
    'SUB': '2',
    'STO': '3',
    'LDA': '5',
    'BR': '6',
    'BRZ': '7',
    'BRP': '8',
    'IN': '901',
    'OUT': '902',
    'DAT': '000'
}


def get_mailboxes_from_file(filepath):
    ext = filepath[-3:]
    if ext.lower() == 'lmc':
        mailboxes = parse_lmc_file(filepath)
        num_mailboxes = len(mailboxes)
    elif ext.lower() in ['txt', 'asm']:
        mailboxes, num_mailboxes = parse_assembly_file(filepath)
    else:
        raise UnsupportedExtensionError('LMC2PY requires a .lmc or assembly .txt or .asm file.')
    return mailboxes, num_mailboxes


def read_file_lines(filepath):
    # Change working directory to lmc2py.py directory.
    os.chdir(os.path.dirname(__file__))

    # read lmc file
    return open(filepath).readlines()


def parse_lmc_file(filepath):
    """Generates mailboxes from lmc machine code file and returns them."""

    file = read_file_lines(filepath)
    try:
        mailboxes = file[1].split('%')[2].split(',')[:-1]
    except Exception:
        raise ParseError("Lmc file is not formatted correctly, please check it and try again.")
    return mailboxes


def parse_assembly_file(filepath):
    """Tries to parse the assembly file.
    If formatted incorrectly raises ParseError."""

    file = read_file_lines(filepath)

    assembly = []
    for line_num, line in enumerate(file):
        if line.strip() != '' and line.strip()[0] != '#':
            try:
                values = [s.strip() for s in re.split('\\s+', re.sub('#.*', '', line))][:3]
            except IndexError:
                raise ParseError("Assembly file is not formatted correctly at line %d" % line_num)

            if len(values) == 1 or (len(values) == 2 and values[1] == ''):
                raise ParseError("Assembly file is missing tab space at line %d" % line_num)

            if len(values) > 1 and values[1] not in assembly_codes.keys():
                raise ParseError(
                    "Assembly file contains unsupported assembly code at line %d: %s" % (line_num, values[1])
                )

            assembly.append(values)

    # ensure that there are no more than 100 registers
    if len(assembly) > 100:
        raise IndexError("More than 100 registers used")

    # get pointers from assembly by looking for pointers targets in
    pointers = {'': ''}
    for box_num, cmd in enumerate(assembly):
        if cmd[0] != '':
            pointers[cmd[0]] = str(box_num)

    mailboxes = assembly_to_machine_code(assembly, pointers)
    num_mailboxes = len(mailboxes)
    mailboxes += ['000'] * (100 - num_mailboxes)

    return mailboxes, num_mailboxes


def assembly_to_machine_code(assembly, pointers):
    """Converts lmc assembly into lmc machine code."""

    mailboxes = []
    # convert assembly to machine code
    for cmd in assembly:
        opcode = cmd[1]
        val = cmd[2] if len(cmd) == 3 else ''
        if opcode == 'DAT':
            machine_code = '000' if val == '' else val.zfill(3)
        elif opcode in ["IN", "OUT", "HLT"]:
            machine_code = assembly_codes[opcode]
        else:
            if val in pointers:
                machine_code = assembly_codes[opcode] + pointers[val].zfill(2)
            else:
                raise NameError(f"No variable of name '{val}' initiated with DAT")
        mailboxes.append(machine_code)
    return mailboxes


def parse_batch_test_file(batch_filepath):
    file = read_file_lines(batch_filepath)
    lines = (line for line in file if len(line.strip()) != 0)

    batch_tests = []
    potential_values = []
    for line in lines:
        try:
            label, inputs, outputs, cycles = line.strip().split(';')
            inputs = [int(val) for val in inputs.split(',')]
            outputs = [int(val) for val in outputs.split(',')]
            cycles = int(cycles)

            potential_values += inputs
        except ValueError:
            raise ParseError("Batch test file is not formatted correctly, please check it and try again.")
        batch_tests.append((label, inputs, outputs, cycles))
    return batch_tests, potential_values
