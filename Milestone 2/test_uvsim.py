import pytest
from uvsim import UVSim
import sys

# Test load_program_into_memory using Test1.txt
def test_load_program_into_memory_success():
    """
    Testing load_program_into_memory function
    """
    uvsim = UVSim()
    uvsim.load_program_into_memory("testuvsim/Test1.txt")
    assert uvsim.memory.LOAD(0) == 1007

    # test load_program_into_memory failure
def test_load_program_into_memory_failure():
    """
    Testing load_program_into_memory function
    """
    uvsim = UVSim()
    with pytest.raises(FileNotFoundError):
        uvsim.load_program_into_memory("Failure.txt")

# Test run_program using Test1.txt
def test_run_program_success():
    """
    Testing run_program function
    """
    uvsim = UVSim()
    uvsim.load_program_into_memory("testuvsim/Test1.txt")
    uvsim.run_program()
    assert uvsim.memory.LOAD(0) == 1007

    # test run_program failure
def test_run_program_failure():
    """
    Testing run_program function
    """
    uvsim = UVSim()
    with pytest.raises(EOFError):
        uvsim.run_program()


#test HALT instruction success
def test_HALT_success():
    """
    Testing HALT instruction
    """
    uvsim = UVSim()
    uvsim.memory.STORE(4300, 0)
    uvsim.run_program()
    assert uvsim.memory.LOAD(0) == 4300

