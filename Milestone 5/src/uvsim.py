from CPU import CPU
from memory import Memory
from program import Program, FourBitProgram, SixBitProgram
import tkinter.simpledialog

class UVSim:
    """passing anything into the constructor for gui will change
    the behavior of some functions to allow them to work with gui, 
    self.output is a list of outputs returned py run_program"""

    # versions of UVSim corresponding to different program classes
    program_versions = {
        FourBitProgram.UV_SIM_VERSION: FourBitProgram,
        SixBitProgram.UV_SIM_VERSION: SixBitProgram
    }

    def __init__(self, version = SixBitProgram.UV_SIM_VERSION, gui = False):

        self.gui = gui                  # is there a gui

        self.accumulator = 0             # current word
        self.op_code = None              # current instruction
        self.address = None              # current address for instruction
        self.program_counter = 0         # current address in program
        self.is_running = False          # is a program currently running
        self.output = None
    
        self.version = version          # uvsim version
        self.program_class = UVSim.program_versions[self.version]       # program type class
        self.memory = Memory(self.program_class.MAX_PROGRAM_LENGTH)     # memory instance
        self.cpu = CPU(10**self.program_class.MAX_LINE_LENGTH - 1)      # cpu instance 

        self.current_program = None     # current instance of the current program class

    def change_version(self, new_version):

        if not new_version in UVSim.program_versions.keys():
            raise ValueError(f"Version {new_version} does not exist")
        
        if new_version == self.version:
            return
        
        self.version = new_version
        self.program_class = UVSim.program_versions[self.version]

        if self.current_program is not None:
            self.current_program = self.program_class(self.current_program)
            self.memory.import_program(self.current_program)

    def store_program_in_memory(self, file_lines, starting_line = 0, skip_identification = False):
        """ Writes data from file (specified by file_name) starting at memory address 0. """

        self.is_running = False
        if not skip_identification:
            identified_type = Program.program_type(file_lines)
            if identified_type is None:
                raise SyntaxError("Invalid syntax for UVSim program")
            if identified_type != self.program_class:
                user_input = tkinter.messagebox.askyesno("UVSim Version Change", f"This program may be best suited for UVSim Version {identified_type.UV_SIM_VERSION}. If you do not switch to this version, you may experience data loss or need to rewrite your program. Would you like to switch versions?")
                if user_input:
                    self.program_class = identified_type
                    self.version = self.program_class.UV_SIM_VERSION
        self.current_program = self.program_class(file_lines, starting_line)
        self.memory.import_program(self.current_program)

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
            raise SyntaxError(f"Line {self.program_counter} cannot be read because it is empty")
        if current_line == self.program_class.EOF_FLAG():   # check for end of file value
            self.is_running = False
            raise EOFError("End of file flag reached")
        self.op_code = self.program_class.get_op_code(current_line)  # extracts first 2 digits from current line
        self.address = self.program_class.get_address(current_line) # extracts last 2 digits from current line

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
                raise SyntaxError(f"Line {self.program_counter} does not match any valid instructions")
