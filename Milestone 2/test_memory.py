import pytest
from memory import *
from unittest.mock import patch

"""
READ:
- negative test
- positive test

WRITE
- negative test
- positive test

LOAD
- negative test
- positive test
"""

# TODO: add memory size here. 

def test_read_success():
    """asserts that when "1337" is entered, 1337 is added to memory."""
    memory = Memory()
    address = 99
    user_input = "1337\n"
    with pytest.raises(StopIteration):
        user_input_gen = (char for char in user_input)

        with patch('builtins.input', side_effect=user_input_gen):
            memory.READ(address)

    assert memory.memory_array[address] == 1337


def test_read_fail():
    """asserts that when "1337" is entered, 1337 is added to memory."""
    memory = Memory()
    address = 10
    user_input = "not an integer\n"
    with pytest.raises(SystemExit):
        user_input_gen = (char for char in user_input)

        with patch('builtins.input', side_effect=user_input_gen):
            memory.READ(address)


def test_write_success(capfd):
    memory = Memory()
    address = 10
    value = 1337
    memory.STORE(value, address)
    memory.WRITE(10)
    captured = capfd.readouterr()
    assert captured.out == f"At memory address {address} is {value}"
    assert captured.err == ""


def test_write_fail_index():
    # TODO: out of bounds. 
    memory = Memory()
    address = 1000
    with pytest.raises(IndexError):
        memory.WRITE(address)

def test_write_fail_value():
    memory = Memory()
    address = "muffins"
    with pytest.raises(ValueError):
        memory.write(address)


def test_store_success():
    memory = Memory()

    # before insertion
    assert memory.memory_array[address] == None
    assert memory.LOAD(address) == None
    assert memory.memory_array[address+1] == None
    assert memory.LOAD(address+1) == None


    value = 42
    address = 75
    memory.STORE(value, address)

    # after insertion
    assert memory.memory_array[address] == value
    assert memory.LOAD(address) == value
    assert memory.memory_array[address+1] == None
    assert memory.LOAD(address+1) == None

    # TODO: Print the whole array to make sure no funny business happened. 

def test_store_fail_index():
    memory = Memory()
    address = 1000
    with pytest.raises(IndexError):
        memory.WRITE(address)


def test_store_fail_value():
    memory = Memory()
    address = "muffins"
    with pytest.raises(ValueError):
        memory.write(address)


def test_load_success():
    pass

def test_load_fail():
    pass

