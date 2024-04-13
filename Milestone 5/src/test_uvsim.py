import pytest
from uvsim import UVSim
from file_formatter import TxtFormatter
from os import path


# Test store_program_in_memory using Test1.txt
def test_store_program_in_memory_success():
    """
    Testing store_program_in_memory function
    """
    uvsim = UVSim(1)
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "test", "Test1.txt"))
    uvsim.store_program_in_memory(TxtFormatter.format_file(filepath), skip_identification=True)
    assert uvsim.memory.LOAD(0) == 1007

    # test store_program_in_memory failure
def test_store_program_in_memory_failure():
    """
    Testing store_program_in_memory function
    """
    uvsim = UVSim(1)
    with pytest.raises(FileNotFoundError):
        uvsim.store_program_in_memory(TxtFormatter.format_file("Failure.txt"))

#test run_program success
def test_run_program_success():
    """
    Testing run_program function
    """
    uvsim = UVSim(1)
    uvsim.store_program_in_memory(["4300"], skip_identification=True)
    uvsim.run_program()
    assert uvsim.memory.LOAD(0) == 4300

def test_run_program_failure():
    """
    Testing run_program function failure scenario
    """
    uvsim = UVSim(1)
    uvsim.store_program_in_memory([""], skip_identification=True)
    with pytest.raises(Exception):
        uvsim.run_program()
