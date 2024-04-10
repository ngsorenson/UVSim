# from program import Program

class LineValidator:
    """A class to validate programs based on the program type.
    
    Attributes:
        program_type (_class_): Class of the program type to base validation on
    
    Methods:
        validate_lines (lines=_list_[_string_ or _int_]): Returns the valid lines in a given list of program lines.
    """

    def __init__(self, program_type):
        """
        Args:
            program_type (_class_): Class of the program type to base validation on
        """
        
        # program_type cannot currently be validated, due to a circular import from importing program.py (program.py imports line_validator.py)
        # could be fixed with better architecture, potentially

        # if not issubclass(program_type, Program):
        #     raise TypeError("Program type must be the class of a program type")
        # if isinstance(program_type, Program):
        #     raise TypeError("Program type must be the class of a program type, not an instance of it")

        self.program_type = program_type

    def _validate_length(self, line):
        """Validates if a given line conforms to the line length in the program format that initialized this validator.
        
        Args:
            line (_string_): A line of a program represented as a string
        
        Returns:
            _bool_: True if this line is a valid length, False otherwise
        """
        if not isinstance(line, str):
            raise TypeError(f"Line must be a string, not {type(line)}")
        return (len(line) > 0) and ((len(line) <= self.program_type.MAX_LINE_LENGTH) or (((line[0] == '+') or (line[0] == '-')) and ((len(line)-1) <= self.program_type.MAX_LINE_LENGTH)))
    
    def _validate_chars(self, line):
        """Validates if a given line conforms to the allowed characters in the program format that initialized this validator.
        
        Args:
            line (_string_): A line of a program represented as a string
        
        Returns:
            _bool_: True if this line contains valid characters, False otherwise
        """
        if not isinstance(line, str):
            raise TypeError(f"Line must be a string, not {type(line)}")
        return line.isnumeric() or (((line[0] == '+') or (line[0] == '-')) and (line[1:].isnumeric()))
    
    def validate_lines(self, lines):
        """Returns the valid lines in a given list of program lines.
        
        Args:
            lines (_list_[_string_ or _int_]): A list of strings or integers representing the program to be validated
        
        Returns:
            _list_[_int_ or None]: A list of integers for valid lines in the given program, or None if that line is invalid (leaves a blank space in a program)
        """

        if not isinstance(lines, list):
            raise TypeError(f"Program lines must be represented in a list, not {type(lines)}")

        # check if length of program is valid
        if len(lines) > self.program_type.MAX_PROGRAM_LENGTH:
            raise MemoryError(f"Program has more lines than available addresses in memory ({len(lines)} lines out of {self.program_type.MAX_PROGRAM_LENGTH} addresses)")
        
        final_lines = []

        # validate lines in the program
        for line in lines:
            if not (isinstance(line, str) or isinstance(line, int)):
                raise TypeError(f"Lines in the program list must be either a string or an integer, not {type(line)}")
            line_str = str(line)    # ensure the line is a string (it could be an int) for validation functions to work
            if self._validate_length(line_str) and self._validate_chars(line_str):
                final_lines.append(int(line_str))   # line is valid, append the integer representation to the final lines list
                continue
            if line_str == str(self.program_type.EOF_FLAG()):
                break   # EOF flag reached, so no further lines should be read
            final_lines.append(None)    # line is invalid, append None to leave a blank space in the program

        return final_lines
