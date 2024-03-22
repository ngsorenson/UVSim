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
3. The GUI window will pop up:
   In the GUI window, you will find 9 buttons:
      1. `Load Program`: Click this button to select a program file and load it into the simulator. The loaded program will be displayed in the "Log" window.
      2. `Save Program`: Click this button when you are ready to save the program file to a location you choose.
      3. `Run Program`: After loading a program, click this button to run the program. You will be prompted to input a 4-digit word, and the program will execute, displaying the output in the "Log" window.
      4. `Step Program`: This button will step through the program waiting for you to press it again for each step. 
      5. `Stop Program`: This button will stop the program.
      6. `Reinitialize UVSim`: Click this button to clear the memory and reset the program state without closing the application.
      7. `Clear Output`: Clears the output in the output field.
      8. `Change Color Scheme`: Allows the user to put hex codes for primary and secondary colors.
      9. `Reset to Default Colors`: Sets the color scheme back to UVU colors.

4. Click `Load Program`, then pick a file you would like UVSim to run.
5. Once program is loaded into UVSim, to run the program continuously click `Run Program`.
6. Or you can click `Step Program` to have UVSim execute 1 line then wait for you to click `Step Program` again.
7. You can continue to step the program until it finishes or click `Stop Program` to halt it. 
8. Regardless UVSim will follow the instructions according to the program you have loaded in. Prompting you when needed for input.
9. You can also choose to edit the program you loaded in by editing the Memory Contents field.
10. Make sure to press "Ctrl + s" to save your edits before then click `Run Program` to run the program like before.
11. Running multiple files:
   - To run another file if you would like to clear the memory, click the Reinitialize UVSim then load your new file into UVSim and run it using the `Run Program` button.
   - You can also clear the output section by clicking the `Clear Output` button
   - Also feel free to customize the color scheme by using the buttons `Change Color Scheme` and `Reset to Default Colors`

## Program Structure:
- `CPU`: Defines basic arithmetic operations.
- `Memory`: Manages memory operations such as reading, writing, loading, and storing values.
- `UVSim`: The main class for running programs. It loads programs into memory and executes the instructions within either by stepping through the program or running through it.
- `GUI`: The GUI class provides an intuitive user interface to interact with the UVSim in multiple ways.

## Program Instructions:
- Programs are stored in plain text files where each line represents an instruction. In each line, the first two digits represent the opcode, while the last two digits represent the location in memory used in the operation. For example, `1036` performs a READ operation (`10`) and stores the value at index `36` in memory. 
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
