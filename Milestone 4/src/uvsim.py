from CPU import CPU
from memory import Memory
import tkinter.simpledialog

MEMORY_SIZE = 100

def is_EOF(value):
    return abs(int(value)) >= 10**4

class UVSim:
    """passing anything into the constructor for gui will change
    the behavior of some functions to allow them to work with gui, 
    self.output is a list of outputs returned py run_program"""

    def __init__(self, gui = None):

        self.gui = gui
        self.accumulator = 0             # current word
        self.op_code = None              # current instruction
        self.address = None              # current address for instruction
        self.program_counter = 0         # current address in program
        self.is_running = False          # is a program currently running
        self.cpu = CPU()
        self.memory = Memory(MEMORY_SIZE)
        self.output = None

    def store_program_in_memory(self, arg):
        """ Writes data from file (specified by file_name) starting at memory address 0. """

        self.is_running = False

        if isinstance(arg, str):

            file_name = arg

            with open(file_name, "r") as file:

                # write to memory, making sure to not go over the memory size. 
                for i, line in enumerate(file):
                    if (len(line) > 0) and (line != "\n"):
                        self.accumulator = line
                        self.address = i
                        self.memory.STORE(self.accumulator, self.address)
                    else:
                        self.address = i
                        self.memory.DELETE(self.address)

                # write EOF flag as a way to end execution w/o a HALT cmd.
                if not is_EOF(self.accumulator):
                    self.memory.STORE(99999, (self.address + 1))

                self.accumulator = 0
        
        elif isinstance(arg, list):

            # write to memory, making sure to not go over the memory size. 
            for i, line in enumerate(arg):
                if len(line) > 0:
                    self.accumulator = int(line)
                    self.address = i
                    # print(self.address, ":", self.accumulator)
                    self.memory.STORE(self.accumulator, self.address)
                else:
                    self.address = i
                    self.memory.DELETE(self.address)

            self.accumulator = 0


    def run_program(self, start_location = 0):
        """ Runs program starting at a given memory address (defaults to 0). """

        self.step_program(start_location)   # note: this line is neccessary to make sure self.is_running is true before starting the while loop (still works as expected when halt is reached on this line)
        while self.is_running:
            self.step_program()
                
    def step_program(self, start_location = 0):

        if not self.is_running:
            self.accumulator = 0
            self.output = None
            self.program_counter = start_location - 1
            self.is_running = True

        self.program_counter += 1
        current_line = self.memory.LOAD(self.program_counter)
        if current_line is None:
            self.is_running = False
            raise SyntaxError(f"Line {self.program_counter} does not match any valid instructions.")
        if is_EOF(current_line):   # check for end of file value
            self.is_running = False
            raise EOFError("End of file flag reached.")
        self.op_code = int(current_line / 100)  # extracts first 2 digits from current line
        self.address = current_line - (self.op_code * 100)  # extracts last 2 digits from current line

        match self.op_code:
            case 10:
                if self.gui:
                    value = tkinter.simpledialog.askinteger("Input value:", "Input 4 digit word to read into memory (prepending a negative is allowed)")
                    self.memory.READ(self.address, value)
                else:
                    self.memory.READ(self.address)
            case 11:
                if self.gui:
                    self.output = self.memory.WRITE(self.address)
                else: 
                    print(self.memory.WRITE(self.address))
            case 20:
                result = self.memory.LOAD(self.address)
                self.accumulator = result if result is not None else self.accumulator
            case 21:
                self.memory.STORE(self.accumulator, self.address)
            case 30:
                self.accumulator = self.cpu.ADD(self.accumulator, self.memory.LOAD(self.address))
            case 31:
                self.accumulator = self.cpu.SUBTRACT(self.accumulator, self.memory.LOAD(self.address))
            case 32:
                self.accumulator = self.cpu.DIVIDE(self.accumulator, self.memory.LOAD(self.address))
            case 33:
                self.accumulator = self.cpu.MULTIPLY(self.accumulator, self.memory.LOAD(self.address))
            case 40:    # BRANCH
                self.program_counter = self.address - 1
            case 41:    # BRANCHNEG
                self.program_counter = self.address - 1 if self.accumulator < 0 else self.program_counter
            case 42:    # BRANCHZERO
                self.program_counter = self.address - 1 if self.accumulator == 0 else self.program_counter
            case 43:    # HALT
                self.is_running = False 
            case _:
                self.is_running = False
                raise SyntaxError(f"Line {self.program_counter} does not match any valid instructions.")
