UVSim - Simple CPU Simulator

Overview:
----------
UVSim is a simple CPU simulator that emulates a hypothetical machine language. It includes a basic CPU class, a memory module, and a UVSim class for running programs.

Files:
------
1. CPU.py: Defines the CPU class with basic arithmetic operations (ADD, SUBTRACT, MULTIPLY, DIVIDE).
2. memory.py: Implements the Memory class for managing memory operations (READ, WRITE, LOAD, STORE).
3. uvsim.py: Contains the UVSim class, which serves as a simulator for running programs loaded into memory.
4. main.py: An example script demonstrating how to use the UVSim class to load and run a program.

Usage:
------
1. Ensure you have Python 3 or later installed on your system.

2. Run the program by executing the main.py script:
   - python3 main.py<filename>
   - Replace '<filename>' with the name of the program file containing the instructions for the simulator.
   - Example: python3 main.py Test1.txt
  
3. The program will load the specified file into memory and execute the instructions. Check the output for the results

Program Structure:
------------------
- `CPU`: Defines basic arithmetic operations.
- `Memory`: Manages memory operations such as reading, writing, loading, and storing values.
- `UVSim`: The main class for running programs. It loads programs into memory and executes the instructions.

Program Instructions:
---------------------
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

Error Handling:
---------------
- The program includes basic error handling for file-related issues, invalid addresses, and unrecognized opcodes.


Authors:
-------
Tate Thomas, Noah Sorenson, Thomas Chappell, Ty Didericksen
