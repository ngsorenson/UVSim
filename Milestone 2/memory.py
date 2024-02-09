class Memory:
	def __init__(self):
		self.min = 0
		self.max = 99
		memory_array = []

		for i in range(self.min, self.max + 1):
			memory_array.append(0)

		self.memory_array = memory_array


	def READ(self, address):
		"""Reads a word from the keyboard to somewhere in memory. 

		Args:
			address (_type_): Address to put the user input into in memory. 
		"""
		try: 
			address_int = int(address)
			user_input = input(f"Input an integer value to go in memory address {address_int}: ")
			while True:
				try:
					input_int = int(user_input)
					self.memory_array[address_int] = input_int
					break
				except ValueError:
					print("Input is not a valid integer.")

		except ValueError:
			print("Error: Address value is not a valid integer")




	def WRITE(self, address):
		"""Takes a memory address (int) and prints the value at that address. 

		Args:
			address (_type_): input string
		"""
		try: 
			address_int = int(address)
			if address_int not in range(self.min, self.max + 1):
				print(f"Error: Memory address {address_int} is not valid. It must be between {self.min} and {self.max}.")
			else:
				print(f"At memory address {address_int} is {self.memory_array[address_int]}")
		except ValueError:
			print("Error: Address value is not a valid integer")



	def LOAD(self, address): 
		"""If a valid address, returns the value at that address.

		Args:
			address (_int_): The memory address in the array

		Returns:
			_int_: The value at that address
		"""
		try:
			address_int = int(address)
		# if address is not in the right range return None. 
			if address not in range (self.min, self.max + 1):
				print(f"Error: Memory address_int {address_int} is not valid. It must be between {self.min} and {self.max}.")
			else:
				value_at_address_int = self.memory_array[address_int]
				return value_at_address_int
		except ValueError:
			print("Error: Address value is not a valid integer")





	def STORE(self, accumulator, address):
		try:
			address_int = int(address)
			if address_int not in range (self.min, self.max + 1):
				print(f"Error: Memory address_int {address_int} is not valid. It must be between {self.min} and {self.max}.")
				print("Not added to memory.")
			else:
				# Error check if accumulator is not an int. 
				try:
					acc_int = int(accumulator)
				except ValueError:
					print("Error: Accumulator value is not an integer.")
					print("Not added to memory.")
				# take accumulator value and set as value at memory address_int int. 
				self.memory_array[address_int] = acc_int
		except ValueError:
			print("Error: Address value is not a valid integer")


			

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






# def main():
# 	user_input = input("Place input here: ")
# 	WRITE(user_input)



