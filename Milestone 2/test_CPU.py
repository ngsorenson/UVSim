import pytest
import CPU
from UVSim import UVSim

def test_add_success():
    uvsim = UVSim()
    uvsim.accumulator = 1010
    assert uvsim.CPU.ADD(101, uvsim.accumulator) == 1111
def test_add_fail():
    uvsim = UVSim()
    assert uvsim.CPU.ADD(101, 1010) == TypeError

def test_subtract_success():
    uvsim = UVSim()
    uvsim.accumulator = 1111
    assert uvsim.CPU.SUBTRACT(101, uvsim.accumulator) == 1010
def test_subtract_fail():
    uvsim = UVSim()
    assert uvsim.CPU.SUBTRACT(101, 1111) == TypeError

def test_multiply_success():
    uvsim = UVSim()
    uvsim.accumulator = 1010
    assert uvsim.CPU.MULTIPLY(5, uvsim.accumulator) == 5050
def test_multiply_fail():
    uvsim = UVSim()
    assert uvsim.CPU.MULTIPLY(5, 1010) == TypeError

def test_divide_success():
    uvsim = UVSim()
    uvsim.accumulator = 5050
    assert uvsim.CPU.DIVIDE(5, uvsim.accumulator) == 1010
def test_divide_fail():
    uvsim = UVSim()
    assert uvsim.CPU.DIVIDE(5, 5050) == TypeError