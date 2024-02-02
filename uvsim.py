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
                self.memory.STORE()

    def run_program(self):
        """ Runs program starting at memory address 0. """

        self.program_counter = -1

        while True:

            self.program_counter += 1
            self.memory.LOAD(self.program_counter)
            self.op_code = int(self.accumulator / 100)  # extracts first 2 digits from accumulator
            self.address = self.accumulator - (self.op_code * 100)  # extracts last 2 digits from accumulator

            match self.op_code:
                case 10:
                    self.memory.READ()
                case 11:
                    self.memory.WRITE()
                case 20:
                    self.memory.LOAD()
                case 21:
                    self.memory.STORE()
                case 30:
                    self.cpu.ADD()
                case 31:
                    self.cpu.SUBTRACT()
                case 32:
                    self.cpu.DIVIDE()
                case 33:
                    self.cpu.MULTIPLY()
                case 40:
                    self.processor.BRANCH()
                case 41:
                    self.processor.BRANCHNEG()
                case 42:
                    self.processor.BRANCHZERO()
                case 42:
                    break   
                case _:
                    raise SyntaxError("Incorrect opcode.", f"Opcode {self.op_code} on line {self.program_counter} does not match any valid instructions.")
