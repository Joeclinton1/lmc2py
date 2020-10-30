# lmc2py

This is a single file python script which runs the "Little Minion Computer" .lmc and .txt files in python, to save you having to wait for it to run.

## Features
- Interprets LMC assembly and .LMC files to python
- Test program against multiple inputs at once.
- Test program against all inputs.
- Check program outputs expected output.
- Output graph of inputs vs F/E cycles for an easy visualisation of your programs efficiency.

## Usage

This program can be executed using a command line interface, such as PowerShell or the Linux or MacOS terminal. To run the program, use something like `python path/to/program/lmc2py.py path/to/source/file.lmc --options`.
Depending on your computer, you may need to change `python` to `py` or `python3`.

The default behaviour of the program is to take the file given as an argument and execute it in the terminal. If the file contains assembly code (which is valid for Little Minion Computer) then the program will attempt to compile it first. It will also count how many fetch/execute cycles were used to run the program.

This behaviour can be changed by the use of optional flags, which are put in place of `--options` in the command above. Each option comes with a short and a long form, which can be used interchangably. If an option requires an additional parameter, the parameter should follow the flag, such as:

```python lmc2py.py code.lmc -i 997```

- `-h`, `--help`: displays this list of options, instead of doing anything else. A source file is not needed in this case.
- `-a`, `--all`: executes the program once for each value between 0 and 999.
- `-i [VAL]`, `--input [VAL]`: executes the program once for each VAL given. Multiple inputs can be given as a list, like `-i 840 961 997`.
- `-q`, `--quiet`: executes the program without any terminal output, except errors. If you use this flag without any output flags, the program may not return anything.
- `-f [FILE]`, `--feedback [FILE]`: save the results of the program to a text file. If no FILE is specified, this will be a file in the source file's directory called feedback_\<filename\>.
- `-ch CHECKER`, `--checker CHECKER`: run a checker function from a python file with the same inputs as the LMC code, to show the expected output and see if your program's output matches. Some example checker functions are included in `checks/`.
-`-g`, `--graph`: show a scatter graph relating input to the number of cycles. Helps with visualizing program efficiency.

### Something to consider

If your program requires multiple inputs, and it is passed a series of inputs using either `--all` or `--input`, it will use the next value from that series each time. If it runs out of inputs and then hits another IN statement, it will prompt you for another in the terminal.
