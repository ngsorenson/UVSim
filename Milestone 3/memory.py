MEMORY_SIZE = 100

class Memory:
	def __init__(self, memory_size=MEMORY_SIZE):
		self.min = 0

		if memory_size < 1:
			memory_size = MEMORY_SIZE

		self.max = memory_size
		self.memory_array = [None] * (self.max )


	def READ(self, address, value = None):
		"""Reads a word from the keyboard to somewhere in memory. 

		Args:
			address (_type_): Address to put thze user input into in memory. 
		"""
		# TODO: Make this use STORE but checking the user input. 
		try: 
			address_int = int(address)
			if value:
				user_input = value
			else:
				user_input = input(f"Input an integer value to go in memory address {address_int}: ")
			while True:
				try:
					input_int = int(user_input)
					self.memory_array[address_int] = input_int
					break
				except ValueError:
					raise ValueError("Input is not a valid integer.")

		except ValueError:
			raise ValueError("Error: Address value is not a valid integer")



	def WRITE(self, address):
		"""Takes a memory address (int) and prints the value at that address. 

		Args:
			address (_type_): input string
		"""
		# Note: A raised error is automatically propagated up the stack.
		value = self.LOAD(address=address)
		return f"At memory address {address} is {value}"



	def LOAD(self, address): 
		"""If a valid address, returns the value at that address.

		Args:
			address (_int_): The memory address in the array

		Returns:
			_int_: The value at that address. 
		"""
		try:
			address_int = int(address)
			# if address is not in the right range raise an error. 
			if address_int < self.min or address_int > self.max:
				raise IndexError(f"Error: Memory address {address_int} is not valid. It must be between {self.min} and {self.max} inclusive.")
			else:
				value_at_address_int = self.memory_array[address_int]
				return value_at_address_int
		except ValueError:
			raise ValueError(f"Error: Address value {address} is not a valid integer")


	def STORE(self, accumulator, address):
		"""Stores the accumulator value in the address in memory, if both are valid.

		Args:
			accumulator (int): 
			address (int): address in memory
		"""
		# See if address is valid. 
		try:
			address_int = int(address)
			# see if address is in range. 
			if address_int < self.min or address_int > self.max:
				raise IndexError(
					f"Memory address {address_int} is not valid. "
					f"It must be between {self.min} and {self.max} inclusive. "
					f"Not added to memory. "
				)

			acc_int = int(accumulator)  # See if accumulator is valid.  
			self.memory_array[address_int] = acc_int
		except ValueError:
			raise ValueError(
				f"Invalid value: {accumulator} or {address}"
				f"Both accumulator and address must be integers. "
				f"Not added to memory. "
			)


			

def main(): 
	memory = Memory()

	memory.memory_array[10] = 15
	memory.memory_array[25] = 32
	memory.memory_array[50] = 65
	memory.memory_array[75] = 89
	memory.memory_array[90] = 97
	memory.memory_array[99] = 100



	# for i in range(memory.min, memory.max + 1):
	# 	print(f"{i}: {memory.memory_array[i]}")



	# user_input = input("Integer to read in: ")
	address1 = 20
	memory.READ(address1)

	address2 = 99
	memory.WRITE(address2)



if __name__ == "__main__":
    main()



