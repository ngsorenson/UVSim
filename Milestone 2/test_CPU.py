import pytest
from CPU import CPU


def test_add_success():
    cpu = CPU()
    assert cpu.ADD(101, 1010) == 1111


def test_add_fail():
    cpu = CPU()
    with pytest.raises(TypeError):
        cpu.ADD(101, "1010")  # accumulator is not int


def test_subtract_success():
    cpu = CPU()
    assert cpu.SUBTRACT(101, 1111) == 1010


def test_subtract_fail():
    cpu = CPU()
    with pytest.raises(TypeError):
        cpu.SUBTRACT(101.1, 1111)  # value is not int


def test_multiply_success():
    cpu = CPU()
    assert cpu.MULTIPLY(5, 1010) == 5050


def test_multiply_fail():
    cpu = CPU()
    with pytest.raises(TypeError):
        cpu.MULTIPLY("5", 1010)  # value is not int


def test_divide_success():
    cpu = CPU()
    assert cpu.DIVIDE(5, 5050) == 1010


def test_divide_fail():
    cpu = CPU()
    with pytest.raises(TypeError):
        cpu.DIVIDE(5, 5050.3)  # accumulator is not int

def test_divide_by_zero():
    cpu = CPU()
    with pytest.raises(ZeroDivisionError):
        cpu.DIVIDE(0, 1010)
