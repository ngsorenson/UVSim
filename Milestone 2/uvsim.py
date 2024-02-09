from CPU import CPU
from memory import Memory

MEMORY_SIZE = 100

def is_EOF(value):
    return abs(value) >= 10**4

class UVSim:

    def __init__(self):

        self.accumulator = None          # current word
        self.op_code = None              # current instruction
        self.address = None              # current address for instruction
        self.program_counter = None      # current address in program
        self.cpu = CPU()
        self.memory = Memory(MEMORY_SIZE)


    def load_program_into_memory(self, file_name):
        """ Writes data from file (specified by file_name) starting at memory address 0. """

        with open(file_name, "r") as file:

            # write to memory, making sure to not go over the memory size. 
            for i, line in enumerate(file):
                self.accumulator = line
                self.address = i
                self.memory.STORE(self.accumulator, self.address)
                if i == MEMORY_SIZE - 2:
                    print("WARNING: Some content from the file could not be loaded into memory.")
                    break

            # write EOF flag as a way to end execution w/o a HALT cmd. 
            self.memory.STORE(99999, (MEMORY_SIZE - 1))


    def run_program(self):
        """ Runs program starting at memory address 0. """

        self.accumulator = None     # reset accumulator before execution phase.
        self.program_counter = -1   # increments by 1 at start of while loop, hence the -1 (to start program at line 0)

        while True:

            self.program_counter += 1
            current_line = self.memory.LOAD(self.program_counter)
            if is_EOF(current_line):   # check for end of file value
                raise EOFError
            self.op_code = int(current_line / 100)  # extracts first 2 digits from current line
            self.address = current_line - (self.op_code * 100)  # extracts last 2 digits from current line

            match self.op_code:
                case 10:
                    self.memory.READ(self.address)
                case 11:
                    self.memory.WRITE(self.address)
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
                    return 0   
                case _:
                    raise SyntaxError("Unrecognized opcode.", f"Opcode {self.op_code} on line {self.program_counter} does not match any valid instructions.")
