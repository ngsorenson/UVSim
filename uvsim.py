from CPU import CPU
from memory import Memory
from processing import Processor

class UVSim:

    def __init__(self):

        accumulator = None          # current word
        op_code = None              # current instruction
        address = None              # current address for instruction
        program_counter = None      # current address in program
        cpu = CPU()
        memory = Memory()
        processor = Processor()

    def write_file(self, file_name):
        """ Writes data from file (specified by file_name) starting at memory address 0. """

        with open(file_name, "r") as file:
            for i, line in enumerate(file):
                self.accumulator = int(line)
                self.address = i
                self.memory.STORE(self.accumulator, self.address)

    def run_program(self):
        """ Runs program starting at memory address 0. """

        self.program_counter = -1

        while True:

            self.program_counter += 1
            self.accumulator = self.memory.LOAD(self.program_counter)
            if abs(self.accumulator) >= 2**5:   # check for end of file value
                raise EOFError
            self.op_code = int(self.accumulator / 100)  # extracts first 2 digits from accumulator
            self.address = self.accumulator - (self.op_code * 100)  # extracts last 2 digits from accumulator

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
                    self.accumulator = self.cpu.ADD(self.accumulator, self.address)
                case 31:
                    self.accumulator = self.cpu.SUBTRACT(self.accumulator, self.address)
                case 32:
                    self.accumulator = self.cpu.DIVIDE(self.accumulator, self.address)
                case 33:
                    self.accumulator = self.cpu.MULTIPLY(self.accumulator, self.address)
                case 40:
                    self.program_counter = self.address - 1
                case 41:
                    if self.accumulator < 0:
                        self.program_counter = self.address - 1
                case 42:
                    if self.accumulator == 0:
                        self.program_counter = self.address - 1
                case 43:
                    return 0   
                case _:
                    raise SyntaxError("Unrecognized opcode.", f"Opcode {self.op_code} on line {self.program_counter} does not match any valid instructions.")
