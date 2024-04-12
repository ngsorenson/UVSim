from abc import ABC, abstractmethod
from line_validator import LineValidator

class Program(ABC):
    """An abstract class representing a program.

    Attributes:
        OP_CODES (_tuple_(_int_)): A class attribute that is a tuple of currently recognized opcodes
        validator (_LineValidator_): A line validator object specific for the program type
        program_list (_list_[_int_ or None]): A list of integers or None (for a blank line) representing a program
        start_location (_int_): The starting location where the program is supposed to reside in memory
        end_location (_int_): The ending location where the EOF flag is located
    
    Methods:
        EOF_FLAG (cls=_class_): Abstract class method to create EOF flags for a given class
        get_op_code (line=_int_, opcode_start_bit=_int_): Abstract static method that extracts an opcode from a given line based on what bit the opcode starts at
        get_address (line=_int_, opcode_start_bit=_int_): Abstract static method that returns the address of a given line based on what bit the opcode starts at
        adjust_op_code (line=_int_, from_bit=_int_, to_bit=_int_): Static method that moves an opcode to a new starting bit if one is detected.
        program_type (program=_list_[_string_]): Static method that returns the class that is most likely the program type of the given program.
    """

    OP_CODES = (10, 11, 20, 21, 30, 31, 32, 33, 40, 41, 42, 43)     # currently recognized opcodes

    def __init__(self, program, start_location):
        """
        Args:
            program (_list_[_string_]): The program represented in a form of a list of strings
            start_location (_int_): The starting location where the program is supposed to reside in memory
            end_location (_int_): The ending location where the EOF flag is located
        """
        
        self.validator = LineValidator(type(self))  # sets up validator custom to the inheriting class
        
        if not isinstance(program, list):
            raise TypeError(f"Conversion to program must start from list type, not {type(program)}")
        self.program_list = self.validator.validate_lines(program)  # create list consisting of valid program lines
        self.program_list.append(type(self).EOF_FLAG())

        if not isinstance(start_location, int):
            raise TypeError(f"Program location in memory must be an integer, not {type(start_location)}")
        if (start_location < 0) or (start_location >= type(self).MAX_PROGRAM_LENGTH):
            raise ValueError(f"Program location must be a valid location in memory ({start_location} was given)")
        self.start_location = start_location
        self.end_location = self.start_location + len(self.program_list) - 1

    @classmethod
    @abstractmethod
    def EOF_FLAG(cls):
        """Returns the EOF flag value for a corresponding class.
        
        Args:
            cls (_class_): The class that is creating the EOF flag
        
        Returns:
            _int_: Defaults to a set of 9's that is 1 digit longer than the max line length
        """
        if not issubclass(cls, Program):
            raise TypeError(f"Class must inherit from Program class (given class is {type(cls)})")
        return int("9" * (cls.MAX_LINE_LENGTH + 1))
    
    @staticmethod
    @abstractmethod
    def get_op_code(line, opcode_start_bit):
        """Returns the opcode of a given line, based on what bit the opcode starts at.
        
        Args:
            line (_int_): The line of a program represented as an integer
            opcode_start_bit (_int_): The bit the opcode starts at (starting from 0, going right to left in base 10)
        
        Returns:
            _int_: The extracted opcode from the given line
        """
        if not isinstance(line, int):
            raise TypeError(f"Line must be an integer, not {type(line)}")
        if not isinstance(opcode_start_bit, int):
            raise TypeError(f"Opcode start bit must be an integer, not {type(line)}")
        if opcode_start_bit < 0:
            raise ValueError(f"Opcode start bit must be a positive integer ({opcode_start_bit} was given)")
        return int(line / 10**opcode_start_bit)     # move the decimal to the opcode start bit, remove digits after decimal
    
    @staticmethod
    @abstractmethod
    def get_address(line, opcode_start_bit):
        """Returns the address of a given line (assuming that this is an instruction line), based on what bit the opcode starts at.
        
        Args:
            line (_int_): The line of a program represented as an integer
            opcode_start_bit (_int_): The bit the opcode starts at (starting from 0, going right to left in base 10)
        
        Returns:
            _int_: The extracted address from the given line
        """
        if not isinstance(line, int):
            raise TypeError(f"Line must be an integer, not {type(line)}")
        if not isinstance(opcode_start_bit, int):
            raise TypeError(f"Opcode start bit must be an integer, not {type(line)}")
        if opcode_start_bit < 0:
            raise ValueError(f"Opcode start bit must be a positive integer ({opcode_start_bit} was given)")
        return line - (Program.get_op_code(line, opcode_start_bit) * 10**opcode_start_bit)  # extract opcode, move it to the correct position, subtract it from original line

    @staticmethod
    def adjust_op_code(line, from_bit, to_bit):
        """If an opcode starting at a given bit is detected in a given line, that opcode is moved to start at a new bit. Useful for conversions to different program types.
        
        Args:
            line (_int_): The line of a program represented as an integer
            from_bit (_int_): The bit the opcode starts at (starting from 0, going right to left in base 10)
            to_bit (_int_): The bit the opcode is to be moved to (once again, starting from 0, going right to left in base 10)
        
        Returns:
            _int_: If there is an opcode detected, a new line is returned with the opcode placement adjusted. If not, the line is returned unchanged
        """
        
        if not isinstance(line, int):
            raise TypeError(f"Line must be an integer, not {type(line)}")
        if not isinstance(from_bit, int):
            raise TypeError(f"Opcode bit start location must be an integer, not {type(from_bit)}")
        if not isinstance(to_bit, int):
            raise TypeError(f"Opcode bit end location must be an integer, not {type(to_bit)}")
        if from_bit < 0:
            raise ValueError(f"Opcode bit start location must be a positive integer ({from_bit} was given)")
        if to_bit < 0:
            raise ValueError(f"Opcode bit end location must be a positive integer ({to_bit} was given)")
        
        new_line = line
        op_code = Program.get_op_code(line, from_bit)
        if op_code in Program.OP_CODES:
            new_line += op_code * (10**to_bit - 10**from_bit)   # mathematically reduces to 'new_line - opcode*10**from_bit + opcode*10**to_bit', i.e. subtracts old op code, adds new one
        
        return new_line

    @staticmethod
    def program_type(program):
        """Given a program in the form of a list of strings, it will return the most likely program type.
        
        Args:
            program (_list_[_string_]): A list of strings representing a program.
        
        Returns:
            _Program_ or None: The detected program class or None, if the program format does not match any current program types.
        """

        def remove_sign(line):
            """Removes the sign from a given line (along with removing leading zeros). Used for string length comparisons (since sign should not matter)"""
            return str(abs(int(line)))
        
        if not isinstance(program, list):
            raise TypeError(f"Program must be represented as a list of strings, not {type(program)} (try using a file formatter class)")
        
        program_types = (FourBitProgram, SixBitProgram)     # program types to be checked in a order sorted by how many bits possible in a line
        identified_type = None

        for program_type in program_types:

            program_lines = program     # copy program (to remove EOF flags if there are any)
            max_line = max(program_lines, key=len)  # get longest line

            # detect if this line is valid for the program type being tested
            if (len(remove_sign(max_line)) > program_type.MAX_LINE_LENGTH) and (max_line != str(program_type.EOF_FLAG())):
                continue

            # remove EOF flags
            while max_line == str(program_type.EOF_FLAG()):
                program_lines.remove(max_line)
                max_line = max(program_lines, key=len)
            
            # detect if this longest line is valid for the program type being tested
            if len(remove_sign(max_line)) <= program_type.MAX_LINE_LENGTH:
                identified_type = program_type  # since it is valid, it is most likely to be this program type, so you can break from loop
                break
        
        return identified_type

class FourBitProgram(Program):
    """A four bit UVSim Version 1 program.

    Attributes:
        MAX_LINE_LENGTH (_int_): A class attribute that is the max length of a 4 bit program (4 bits)
        MAX_PROGRAM_LENGTH (_int_): A class attribute that is the max length of a program (100 lines)
        UV_SIM_VERSION (_int_): A class attribute that is the corresponding UVSim version for this program (Version 1)
        validator (_LineValidator_): A line validator object specific to four bit programs
        program_list (_list_[_int_ or None]): A list of integers or None (for a blank line) representing a program
        start_location (_int_): The starting location where the program is supposed to reside in memory
        end_location (_int_): The ending location where the EOF flag is located
    
    Methods:
        EOF_FLAG (cls=_class_): Class method that returns the EOF flag of this program type (99999)
        get_op_code (line=_int_, opcode_start_bit=_int_): Static method that extracts an opcode from a given line
        get_address (line=_int_, opcode_start_bit=_int_): Static method that returns the address of a given line
        to_four_bit: Returns the program lines of this program, since it is already four bits
        to_six_bit: Converts this four bit program to six bits
    """

    MAX_LINE_LENGTH = 4
    MAX_PROGRAM_LENGTH = 100
    UV_SIM_VERSION = 1

    def __init__(self, program, start_location=0):
        """
        Args:
            program (_list_[_string_] or _Program_): The program represented in a form of a list of strings, or an instance of an already existing program
            start_location (_int_): The starting location where the program is supposed to reside in memory, defaulting to 0
        """
        if isinstance(program, list):   # program is not formatted yet, so it is new
            super().__init__(program, start_location)
        elif isinstance(program, Program):  # program is already a program, just wanting to be converted to a new program type
            try:
                if start_location != 0:
                    prog_loc = start_location
                else:
                    prog_loc = program.start_location
                super().__init__(program.to_four_bit(), prog_loc)
            except AttributeError:
                raise NotImplementedError(f"{type(program).__name__} does not support conversions to {type(self).__name__}.")
        else:
            raise TypeError(f"To create a new program object, a list or program object must be used, not {type(program)}")

    @classmethod
    def EOF_FLAG(cls):
        """Returns the EOF flag value for a four bit program.
        
        Args:
            cls (_FourBitProgram_): The four bit program class
        
        Returns:
            _int_: The EOF flag for a four bit program (99999)
        """
        return super().EOF_FLAG()

    @staticmethod
    def get_op_code(line):
        """Returns the opcode of a given line, assuming the opcode starts at bit 2.
        
        Args:
            line (_int_): The line of a program represented as an integer
        
        Returns:
            _int_: The extracted opcode from the given line
        """
        return Program.get_op_code(line, 2)
    
    @staticmethod
    def get_address(line):
        """Returns the address of a given line (assuming that this is an instruction line), assuming the opcode starts at bit 2.
        
        Args:
            line (_int_): The line of a program represented as an integer
        
        Returns:
            _int_: The extracted address from the given line
        """
        return Program.get_address(line, 2)

    def to_four_bit(self):
        """Returns the program list of this program (since it is already four bit).
        
        Args:
            None
        
        Return:
            _list_[_int_ or None]: The program represented as a list of integers or None (for a blank line) in four bit format
        """
        return self.program_list

    def to_six_bit(self):
        """Converts this four bit program to six bits.
        
        Args:
            None
        
        Return:
            _list_[_int_ or None]: The program represented as a list of integers or None (for a blank line) in six bit format
        """
        new_program_list = []
        for line in self.program_list:
            new_program_list.append(Program.adjust_op_code(line, 2, 3))     # adjust opcode if it is detected, add it to new program list
        return new_program_list[:-1]    # return new program list excluding the last line, since it is an EOF flag and a new one will be added later

class SixBitProgram(Program):
    """A six bit UVSim Version 2 program.

    Attributes:
        MAX_LINE_LENGTH (_int_): A class attribute that is the max length of a 4 bit program (6 bits)
        MAX_PROGRAM_LENGTH (_int_): A class attribute that is the max length of a program (100 lines)
        UV_SIM_VERSION (_int_): A class attribute that is the corresponding UVSim version for this program (Version 2)
        validator (_LineValidator_): A line validator object specific to six bit programs
        program_list (_list_[_int_ or None]): A list of integers or None (for a blank line) representing a program
        start_location (_int_): The starting location where the program is supposed to reside in memory
        end_location (_int_): The ending location where the EOF flag is located
    
    Methods:
        EOF_FLAG (cls=_class_): Class method that returns the EOF flag of this program type (9999999)
        get_op_code (line=_int_, opcode_start_bit=_int_): Static method that extracts an opcode from a given line
        get_address (line=_int_, opcode_start_bit=_int_): Static method that returns the address of a given line
        to_four_bit: Converts this six bit program to four bits
        to_six_bit: Returns the program lines of this program, since it is already four bits
    """

    MAX_LINE_LENGTH = 6
    MAX_PROGRAM_LENGTH = 250
    UV_SIM_VERSION = 2

    def __init__(self, program, start_location=0):
        """
        Args:
            program (_list_[_string_] or _Program_): The program represented in a form of a list of strings, or an instance of an already existing program
            start_location (_int_): The starting location where the program is supposed to reside in memory, defaulting to 0
        """
        if isinstance(program, list):   # program is not formatted yet, so it is new
            super().__init__(program, start_location)
        elif isinstance(program, Program):  # program is already a program, just wanting to be converted to a new program type
            try:
                if start_location != 0:
                    prog_loc = start_location
                else:
                    prog_loc = program.start_location
                super().__init__(program.to_six_bit(), prog_loc)
            except AttributeError:
                raise NotImplementedError(f"{type(program).__name__} does not support conversions to {type(self).__name__}.")
        else:
            raise TypeError(f"To create a new program object, a list or program object must be used, not {type(program)}")

    @classmethod
    def EOF_FLAG(cls):
        """Returns the EOF flag value for a six bit program.
        
        Args:
            cls (_SixBitProgram_): The six bit program class
        
        Returns:
            _int_: The EOF flag for a six bit program (9999999)
        """
        return super().EOF_FLAG()

    @staticmethod
    def get_op_code(line):
        """Returns the opcode of a given line, assuming the opcode starts at bit 3.
        
        Args:
            line (_int_): The line of a program represented as an integer
        
        Returns:
            _int_: The extracted opcode from the given line
        """
        return Program.get_op_code(line, 3)
    
    @staticmethod
    def get_address(line):
        """Returns the address of a given line (assuming that this is an instruction line), assuming the opcode starts at bit 3.
        
        Args:
            line (_int_): The line of a program represented as an integer
        
        Returns:
            _int_: The extracted address from the given line
        """
        return Program.get_address(line, 3)

    def to_four_bit(self):
        """Converts this six bit program to four bits (note: some information may be lost).
        
        Args:
            None
        
        Return:
            _list_[_int_ or None]: The program represented as a list of integers or None (for a blank line) in four bit format
        """
        new_program_list = []
        for line in self.program_list:
            new_program_list.append(Program.adjust_op_code(line, 3, 2))     # adjust opcode if it is detected, add it to new program list
        return new_program_list[:-1]    # return new program list excluding the last line, since it is an EOF flag and a new one will be added later
    
    def to_six_bit(self):
        """Returns the program list of this program (since it is already six bit).
        
        Args:
            None
        
        Return:
            _list_[_int_ or None]: The program represented as a list of integers or None (for a blank line) in six bit format
        """
        return self.program_list
