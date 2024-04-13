import pytest
from CPU import CPU

def test_add_success():
    cpu = CPU(9999)
    assert cpu.ADD(1010, 101) == 1111


def test_add_fail():
    cpu = CPU(9999)
    with pytest.raises(TypeError):
        cpu.ADD("1010", 101)  # accumulator is not int


def test_subtract_success():
    cpu = CPU(9999)
    assert cpu.SUBTRACT(1111, 101) == 1010


def test_subtract_fail():
    cpu = CPU(9999)
    with pytest.raises(TypeError):
        cpu.SUBTRACT(1111, 101.1)  # value is not int


def test_multiply_success():
    cpu = CPU(9999)
    assert cpu.MULTIPLY(1010, 5) == 5050


def test_multiply_fail():
    cpu = CPU(9999)
    with pytest.raises(TypeError):
        cpu.MULTIPLY(1010, "5")  # value is not int


def test_divide_success():
    cpu = CPU(9999)
    assert cpu.DIVIDE(5050, 5) == 1010


def test_divide_fail():
    cpu = CPU(9999)
    with pytest.raises(TypeError):
        cpu.DIVIDE(5050.3, 5)  # accumulator is not an int

def test_divide_by_zero():
    cpu = CPU(9999)
    with pytest.raises(ZeroDivisionError):
        cpu.DIVIDE(1010, 0)
