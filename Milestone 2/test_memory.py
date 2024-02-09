import pytest
from memory import *
from unittest.mock import patch


def test_memory_init():
    memory = Memory()
    for item in memory:
        assert item == None
    assert len(memory.memory_array) == 99
    assert len(memory.memory_array) == 100    

    memory = Memory(0)
    assert len(memory.memory_array) == 99
    assert len(memory.memory_array) == 100



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

    # TODO: Should I switch this one to StopIteration or switch the other one to SystemExit??


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
    memory = Memory()
    address = 1000
    with pytest.raises(IndexError):
        memory.WRITE(address)


def test_write_fail_value():
    memory = Memory()
    address = "muffins"
    with pytest.raises(ValueError):
        memory.WRITE(address)


def test_store_success():
    memory = Memory()
    address = 22

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
    # print(memory.memory_array)


def test_store_fail_index():
    memory = Memory()
    address = 1000
    with pytest.raises(IndexError):
        memory.WRITE(address)


def test_store_fail_value():
    memory = Memory()
    address = "muffins"
    with pytest.raises(ValueError):
        memory.WRITE(address)


def test_load_success():
    memory = Memory()
    # Test 1. 
    # Test w/o having stored first. 
    address1 = 99
    in_array1 = memory.memory_array[address1]
    from_load1 = memory.LOAD(address1)
    assert in_array1 == None
    assert in_array1 == from_load1

    # Test 2. 
    # Test w/ having stored first.
    address2 = 44
    value2 = 10999
    memory.STORE(value2, address2)
    in_array2 = memory.memory_array[address2]
    from_load2 = memory.LOAD(address1)
    assert value2 == in_array2
    assert in_array2 == from_load2


def test_load_fail_index():
    memory = Memory()
    address = 1000
    with pytest.raises(IndexError):
        memory.LOAD(address)


def test_load_fail_value():
    memory = Memory()
    address = "muffins"
    with pytest.raises(ValueError):
        memory.LOAD(address)

