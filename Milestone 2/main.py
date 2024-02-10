import sys
from uvsim import UVSim


def main():
    file = sys.argv[1]

    uvsim = UVSim()
    uvsim.store_program_in_memory(file)
    uvsim.run_program()

if __name__=="__main__":
    main()

