import pytest
from uvsim import UVSim
from memory import Memory


# Test store_program_in_memory using Test1.txt
def test_store_program_in_memory_success():
    """
    Testing store_program_in_memory function
    """
    uvsim = UVSim()
    uvsim.store_program_in_memory("Test1.txt")
    assert uvsim.memory.LOAD(0) == 1007

    # test store_program_in_memory failure
def test_store_program_in_memory_failure():
    """
    Testing store_program_in_memory function
    """
    uvsim = UVSim()
    with pytest.raises(FileNotFoundError):
        uvsim.store_program_in_memory("Failure.txt")

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
