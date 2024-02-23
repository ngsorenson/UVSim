# UVSim - Simple CPU Simulator

## Overview:
UVSim is a simple CPU simulator that emulates a hypothetical machine language. It includes a basic CPU class, a memory module, and a UVSim class for running programs. Additionally, a GUI has been implemented for a more user-friendly experience. 

## Files:
1. `CPU.py`: Defines the CPU class with basic arithmetic operations (ADD, SUBTRACT, MULTIPLY, DIVIDE).
2. `memory.py`: Implements the Memory class for managing memory operations (READ, WRITE, LOAD, STORE).
3. `uvsim.py`: Contains the UVSim class, which serves as a simulator for running programs loaded into memory.
4. `main.py`: An example script demonstrating how to use the UVSim class to load and run a program.
5. `gui.py`: Implements the GUI class for a user-friendly interface to interact with UVSim. 

## Usage:
1. Ensure you have Python 3 or later installed on your system.
2. Run the program by executing the `gui.py` script:
   - `python3 gui.py`
3. In the GUI window, you will find three buttons:
   - `Load Program`: Click this button to select a program file and load it into the simulator. The loaded program will be displayed in the "Log" window.
   - `Run Program`: After loading a program, click this button to run the program. You will be prompted to input a 4-digit word, and the program will execute, displaying the output in the "Log" window.
   - `Show Memory`: Click this button to open a new window displaying the contents of the memory, showing the words stored in different memory addresses.
  
4. Running Another File:
   - You can load and run another program file without closing the application. Simply click the "Load Program" button again, select a new file, and proceed to run the program.
  
5. Clearing Memory:
   - To completely clear the memory close the UVSim application and run it again.

## Program Structure:
- `CPU`: Defines basic arithmetic operations.
- `Memory`: Manages memory operations such as reading, writing, loading, and storing values.
- `UVSim`: The main class for running programs. It loads programs into memory and executes the instructions.
- `GUI`: The GUI class provides an intuitive user interface to interact with the UVSim. Run the program with the GUI for an enhanced user experience.

## Program Instructions:
- Programs are stored in plain text files where each line represents an instruction.
- The UVSim class recognizes the following opcodes:
  - READ (10)
  - WRITE (11)
  - LOAD (20)
  - STORE (21)
  - ADD (30)
  - SUBTRACT (31)
  - DIVIDE (32)
  - MULTIPLY (33)
  - BRANCH (40)
  - BRANCHNEG (41)
  - BRANCHZERO (42)
  - HALT (43)

## Error Handling:
- The program includes basic error handling for file-related issues, invalid addresses, and unrecognized opcodes.

## Authors:
- Tate Thomas
- Noah Sorenson
- Thomas Chappell
- Ty Didericksen
