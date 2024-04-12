from CPU import CPU
from memory import Memory
from program import Program, FourBitProgram, SixBitProgram
import tkinter.simpledialog

class UVSim:
    """A simple virtual machine that emulates a hypothetical machine language, 'BasicML'.
    
    Attributes:
        program_versions (_dict_{_int_: _Program_}): A class attribute that keeps track of what UVSim version corresponds to what program class
        version (_int_): An attribute letting UVSim and other outside sources know what version UVSim is currently running in
        gui (_bool_): A flag that lets UVSim know that a GUI is connected so it can interact with it during program execution
        program_class (_class_): An attribute holding the class to base programs on, correlated with what the current UVSim version is
        current_program (_Program_ or None): The current program in UVSim that is represented in a universal format
        memory (_Memory_): An instance of the memory class, a core component of UVSim
        cpu (_CPU_): An instance of the CPU class, a core component of UVSim
        accumulator (_int_ or None): A register that holds an arbitrary word, which can be changed or used for various operations during program execution
        address (_int_ or None): A register that holds a word representing a memory address for some operations to use
        program_counter (_int_): A register that keeps track of where program execution is in memory throughout program execution. It is always located 1 address before the next line to be executed
        is_running (_bool_): A boolean that keeps track of if a program is currently running
        output (_string_ or None): A register to write program output, where UVSim and a GUI communicate
    
    Methods:
        change_version (new_version=_int_): Changes the UVSim version and reformats the current program
        store_program_in_memory (file_lines=_list_[_str_], starting_line=_int_, skip_identification=_bool_): Stores a given program (represented as a list of strings) in memory
        run_program (start_location=_int_ or None): Either starts or continues program execution and runs until a halt, crash, or EOF flag is detected
        step_program (start_location=_int_ or None): Runs the next line in program execution
    """

    # versions of UVSim corresponding to different program classes
    program_versions = {
        FourBitProgram.UV_SIM_VERSION: FourBitProgram,
        SixBitProgram.UV_SIM_VERSION: SixBitProgram
    }

    def __init__(self, version = SixBitProgram.UV_SIM_VERSION, gui = False):
        """
        Args:
            version (_int_): Version to instantiate UVSim in
            gui (_bool_): A flag that lets UVSim know that a GUI is connected so it can interact with it during program execution
        """
    
        if not isinstance(version, int):
            raise TypeError(f"UVSim version must be an integer, not {type(version)}")
        if version not in UVSim.program_versions.keys():
            raise ValueError(f"UVSim Version {version} does not exist (can be one of the following: {UVSim.program_versions.keys()})")
        self.version = version

        if not isinstance(gui, bool):
            raise TypeError("GUI flag must be a boolean")
        self.gui = gui

        self.program_class = UVSim.program_versions[self.version]       # program type class
        self.current_program = None      # current instance of the current program class
        self._set_components()

        self.accumulator = 0             # current word
        self.op_code = None              # current instruction
        self.address = None              # current address for instruction
        self.program_counter = 0         # current address in program
        self.is_running = False          # is a program currently running
        self.output = None               # holds program output
    
    def _set_components(self):
        """Sets/resets UVSim memory and cpu.
        
        Args:
            None
        
        Returns:
            None
        """
        self.memory = Memory(self.program_class.MAX_PROGRAM_LENGTH)     # memory instance
        self.cpu = CPU(10**self.program_class.MAX_LINE_LENGTH - 1)      # cpu instance

    def change_version(self, new_version):
        """Changes the UVSim version and reformats the current program (locally).
        
        Args:
            new_version (_int_): Version number to switch to
        
        Returns:
            None
        """

        if not isinstance(new_version, int):
            raise TypeError(f"New version must be an integer, not {type(new_version)}")
        if new_version not in UVSim.program_versions.keys():
            raise ValueError(f"UVSim Version {new_version} does not exist (can be one of the following: {UVSim.program_versions.keys()})")
        if new_version == self.version:
            return
        
        self.version = new_version
        self.program_class = UVSim.program_versions[self.version]
        self._set_components()

        if self.current_program is not None:
            self.current_program = self.program_class(self.current_program)
            self.memory.import_program(self.current_program)

    def store_program_in_memory(self, file_lines, starting_line = 0, skip_identification = False):
        """Stores a program represented as a list of strings starting at a given line in memory.
        
        Args:
            file_lines (_list_[_str_]): A list of strings representing a program (it is best to use a FileFormatter class to do this for you to ensure correct formatting)
            starting_line (_int_): Line in memory where the start of the program is stored (defaults to 0)
            skip_identification (_bool_): Optional parameter to skip the identification of the program type of the given file and the request to change version if True (defauts to False)
        
        Returns:
            None
        """

        self.is_running = False

        if not isinstance(file_lines, list):
            raise TypeError(f"File lines must be a list of strings, not {type(file_lines)}")
        if len(file_lines) >= self.memory.max:
            raise ValueError(f"Program length exceeds the maximum length ({len(file_lines)} was given, max is {self.memory.max})")
        if not isinstance(starting_line, int):
            raise TypeError(f"Starting line must be an integer, not {type(starting_line)}")
        if (starting_line < 0) or (starting_line >= self.memory.max):
            raise ValueError(f"Starting line is not a valid address in memory ({starting_line} was given)")
        if not isinstance(skip_identification, bool):
            raise TypeError(f"Skip identification must be a boolean, not {type(skip_identification)}")
        
        if not skip_identification:
            identified_type = Program.program_type(file_lines)
            if identified_type is None:
                raise SyntaxError("Invalid syntax for UVSim program")
            if identified_type != self.program_class:
                user_input = tkinter.messagebox.askyesno("UVSim Version Change", f"This program may be best suited for UVSim Version {identified_type.UV_SIM_VERSION}. If you do not switch to this version, the program may be corrupted while loading into memory. \n \n Would you like to switch to UVSim Version {identified_type.UV_SIM_VERSION}")
                if user_input:
                    self.change_version(identified_type.UV_SIM_VERSION)
        
        self.current_program = self.program_class(file_lines, starting_line)
        self.memory.import_program(self.current_program)

    def run_program(self, start_location = None):
        """Either starts or continues program execution and runs until a halt, crash, or EOF flag is detected.
        
        Args:
            start_location (_int_ or None): Location in memory where to begin program execution (does not have an effect if program is already running), defaults to start of program
        
        Returns:
            None
        """
        
        if start_location is None:
            start_location = self.current_program.start_location
        if not isinstance(start_location, int):
            raise TypeError(f"Start location must be an integer, not {type(start_location)}")
        if (start_location < self.current_program.start_location) or (start_location >= self.current_program.end_location):
            raise ValueError(f"Start location is outside of program bounds ({start_location} was given)")

        self.step_program(start_location)   # note: this line is neccessary to make sure self.is_running is true before starting the while loop (still works as expected when halt is reached on this line)
        while self.is_running:
            self.step_program()
                
    def step_program(self, start_location = None):
        """Runs the next line in program execution.
        
        Args:
            start_location (_int_ or None): Location to begin program execution if program is not currently running (does not have an effect if program is already running), defaults to start of program
        
        Returns:
            None
        """

        if start_location is None:
            start_location = self.current_program.start_location
        if not isinstance(start_location, int):
            raise TypeError(f"Start location must be an integer, not {type(start_location)}")
        if (start_location < self.current_program.start_location) or (start_location >= self.current_program.end_location):
            raise ValueError(f"Start location is outside of program bounds ({start_location} was given)")

        # reset attributes before starting program execution
        if not self.is_running:
            self.accumulator = 0
            self.output = None
            self.program_counter = start_location - 1
            self.is_running = True

        # try catch block is here to stop program execution when an error is raised
        try:
            self.program_counter += 1
            current_line = self.memory.LOAD(self.program_counter)

            if current_line is None:
                raise SyntaxError(f"Line {self.program_counter} cannot be read because it is empty")
            if current_line == self.program_class.EOF_FLAG():
                raise EOFError("End of file flag reached")
        
            self.op_code = self.program_class.get_op_code(current_line)
            self.address = self.program_class.get_address(current_line)

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
                
        except Exception as e:
            self.is_running = False
            raise Exception(e)
