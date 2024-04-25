# UVSim - Simple CPU Simulator

## Overview
UVSim is a simple CPU simulator that emulates a hypothetical machine language. It includes a basic CPU class, a memory module, and a UVSim class for running programs. Additionally, a GUI has been implemented for a more user-friendly experience.

## Files
1. `CPU.py`: Defines the CPU class with basic arithmetic operations (ADD, SUBTRACT, MULTIPLY, DIVIDE).
2. `memory.py`: Implements the Memory class for managing memory operations (READ, WRITE, LOAD, STORE).
3. `uvsim.py`: Contains the UVSim class, which serves as a simulator for running programs loaded into memory.
4. `main.py`: An example script demonstrating how to use the UVSim class to load and run a program.
5. `gui.py`: Implements the GUI class for a user-friendly interface to interact with UVSim.
6. `line_validator.py`: Contains the `LineValidator` class, which validates program lines based on the program type.
7. `file_formatter.py`: Provides classes for converting files into a common format for UVSim processing.

## Usage Instructions
### Running the Program
1. Navigate to the directory containing the source code (`'.\Milestone 5\src\'`).
2. Ensure you have Python 3 or later installed on your system.
3. Run the program by executing the `gui.py` script:
   - `python3 gui.py`

### Using the Simulator
Once the GUI window pops up, follow these steps:
   1. Click `Load Program` to select a program file and load it into the simulator. The loaded program will be displayed in the "Log" window.
   2. Click `Save Program` when you're ready to save the program file to a location you choose.
   3. Click `Run Program` after loading a program to execute it. You will be prompted to input a 4-digit word, and the program will execute, displaying the output in the "Log" window.
   4. Click `Step Program` to execute one line at a time, waiting for your input after each step.
   5. Click `Stop Program` to halt the program.
   6. Click `Reinitialize UVSim` to clear the memory and reset the program state without closing the application.
   7. Click `Clear Output` to clear the output in the output field.
   8. Use `Change Color Scheme` to customize the color scheme using hex codes for primary and secondary colors.
   9. Click `Reset to Default Colors` to set the color scheme back to UVU colors.
   10. Click `Change Version` to switch between versions of 6-bit files and 4-bit files.

If your program is a 4-bit file or a 6-bit file, ensure to choose the correct version using the `Change Version` button.

You can also edit the loaded program by modifying the Memory Contents field. Remember to press "Ctrl + s" to save your edits before clicking `Run Program` to execute the program.

### To run multiple files:
   - Reinitialize the UVSim program using the `Reinitialize UVSim` button to clear the memory.
   - Or add a tab using the `+` button in the top right corner to run another file.
   - You can clear the output section by clicking the `Clear Output` button.
   - Customize the color scheme using the `Change Color Scheme` and `Reset to Default Colors` buttons.

## Program Structure
- `CPU`: Defines basic arithmetic operations.
- `Memory`: Manages memory operations such as reading, writing, loading, and storing values.
- `UVSim`: The main class for running programs. It loads programs into memory and executes the instructions within either by stepping through the program or running through it.
- `GUI`: The GUI class provides an intuitive user interface to interact with the UVSim in multiple ways.
- `LineValidator`: Validates program lines based on the program type.
- `FileFormatter`: Abstract class for file formatters in UVSim. It defines a method for converting different file formats into a common format for UVSim processing.
- `TxtFormatter`: Handles the conversion of .txt files into a common format for UVSim processing.

## Program Instructions
Programs are stored in plain text files where each line represents an instruction. There are two types of versions of instructions UVSim supports: 4-bit and 6-bit. For the 4-bit version, the first two digits represent the opcode, while the last two digits represent the location in memory used in the operation. For example, `1036` performs a READ operation (`10`) and stores the value at index `36` in memory. For the 6-bit version, the first 3 digits are the opcode, and the last 3 digits are the location in memory used in the operation. For example, `010036` would perform the READ operation and store the value at index `036` (equivalent to `36`) in memory.

The UVSim class recognizes the following opcodes:

| Opcode    | Instruction   | 
| --------- | ------------- | 
| 10 or 010 | READ          |
| 11 or 011 | WRITE         |
| 20 or 020 | LOAD          | 
| 21 or 021 | STORE         | 
| 30 or 030 | ADD           |
| 31 or 031 | SUBTRACT      |
| 32 or 032 | DIVIDE        |
| 33 or 033 | MULTIPLY      |
| 40 or 040 | BRANCH        | 
| 41 or 041 | BRANCHNEG     |
| 42 or 042 | BRANCHZERO    |
| 43 or 043 | HALT          |

## Error Handling
The program includes basic error handling for file-related issues, invalid addresses, and unrecognized opcodes.

## Authors
- Tate Thomas
- Noah Sorenson
- Thomas Chappell
- Ty Didericksen
