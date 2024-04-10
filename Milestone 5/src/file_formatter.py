from abc import ABC, abstractmethod

class FileFormatter(ABC):
    """An abstract class to convert files into a common format for UVSim processing.
    
    Attributes:
        None
    
    Methods:
        format_file (file=file input specific to the formatter class): Abstract static method that converts a file format to a list of strings with whitespace and newlines removed (blank lines are valid)
    """

    @staticmethod
    @abstractmethod
    def format_file(file):
        """Converts a file format to a list of strings with whitespace and newlines removed (blank lines are valid).
        
        Args:
            file (file input specific to the formatter class): Input that identifies or is a file for the file converter to access and process
        
        Returns:
            _list_[_string_]: A list of strings representing a program (which has not been validated, only converted to a common format)
        """
        pass

class TxtFormatter(FileFormatter):
    """A class to handle the conversion of txt files into a common format for UVSim processing.
    
    Attributes:
        None
    
    Methods:
        format_file (file_location=_string_): Static method that converts a txt file to a list of strings with whitespace and newlines removed (blank lines are valid)
    """

    @staticmethod
    def format_file(file_location):
        """Converts a txt file to a list of strings with whitespace and newlines removed (blank lines are valid).
        
        Args:
            file_location (_string_): Location in directory where the txt file to be formatted is
        
        Returns:
            _list_[_string_]: A list of strings representing a program (which has not been validated, only converted to a common format)
        """
        
        if not isinstance(file_location, str):
            raise TypeError(f"File location must be a string representing where the txt file is located in the directory, not a {type(file_location)}")
        file_type = file_location.split(".")[-1]
        if file_type != "txt":
            raise TypeError(f"File is not a txt file, or file name was given without file extension (input recieved: {file_type})")

        lines = []
        
        # open file and convert lines into list
        with open(file_location, "r") as file:
            for line in file.readlines():
                lines.append(line.replace("\n", "").replace(" ", ""))
        
        return lines
