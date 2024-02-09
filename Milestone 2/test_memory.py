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


def test_write_success():
    pass

def test_write_fail():
    pass

def test_load_success():
    pass

def test_load_fail():
    pass


def test_store_success():
    pass

def test_store_fail():
    pass
