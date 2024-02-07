from CPU import CPU
from memory import Memory

class UVSim:

    def __init__(self):

        self.accumulator = None          # current word
        self.op_code = None              # current instruction
        self.address = None              # current address for instruction
        self.program_counter = None      # current address in program
        self.cpu = CPU()
        self.memory = Memory()

    def read_program(self, file_name):
        """ Writes data from file (specified by file_name) starting at memory address 0. """

        with open(file_name, "r") as file:
            for i, line in enumerate(file):
                self.accumulator = int(line)
                self.address = i
                self.memory.STORE(self.accumulator, self.address)

    def run_program(self):
        """ Runs program starting at memory address 0. """

        self.program_counter = -1   # increments by 1 at start of while loop, hence the -1 (to start program at line 0)

        while True:

            self.program_counter += 1
            current_line = self.memory.LOAD(self.program_counter)
            if abs(current_line) >= 10**4:   # check for end of file value
                raise EOFError
            self.op_code = int(current_line / 100)  # extracts first 2 digits from current line
            self.address = current_line - (self.op_code * 100)  # extracts last 2 digits from current line

            match self.op_code:
                case 10:
                    self.memory.READ(self.address)
                case 11:
                    self.memory.WRITE(self.address)
                case 20:
                    self.accumulator = self.memory.LOAD(self.address)
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
                    if self.accumulator < 0:
                        self.program_counter = self.address - 1
                case 42:    # BRANCHZERO
                    if self.accumulator == 0:
                        self.program_counter = self.address - 1
                case 43:    # HALT
                    return 0   
                case _:
                    raise SyntaxError("Unrecognized opcode.", f"Opcode {self.op_code} on line {self.program_counter} does not match any valid instructions.")
