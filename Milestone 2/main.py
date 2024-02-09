import sys
from uvsim import UVSim


def main():
    file = sys.argv[1]

    uvsim = UVSim()
    #print(uvsim.memory.memory_array)
    uvsim.load_program_into_memory(file)
    #print(uvsim.memory.memory_array)
    uvsim.run_program()
    #print(uvsim.memory.memory_array)

if __name__=="__main__":
    main()

