import pytest
from uvsim import UVSim
from memory import Memory
import sys


# Test load_program_into_memory using Test1.txt
def test_load_program_into_memory_success():
    """
    Testing load_program_into_memory function
    """
    uvsim = UVSim()
    uvsim.load_program_into_memory("Test1.txt")
    assert uvsim.memory.LOAD(0) == 1007

    # test load_program_into_memory failure
def test_load_program_into_memory_failure():
    """
    Testing load_program_into_memory function
    """
    uvsim = UVSim()
    with pytest.raises(FileNotFoundError):
        uvsim.load_program_into_memory("Failure.txt")

#test run_program success
def test_run_program_success():
    """
    Testing run_program function
    """
    uvsim = UVSim()
    uvsim.memory.STORE(4300, 0)
    uvsim.run_program()
    assert uvsim.memory.LOAD(0) == 4300

#test run_program failure (shows how uvsim is handling the EOFError)
class MockMemory(Memory):
    def LOAD(self, address):
        raise EOFError

def test_run_program_failure():
    """
    Testing run_program function failure scenario
    """
    uvsim = UVSim()
    uvsim.memory = MockMemory()

    with pytest.raises(EOFError):
        uvsim.run_program()
