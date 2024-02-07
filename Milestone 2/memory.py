class Memory:
	def __init__(self):
		self.min = 0
		self.max = 99
		memory_array = []

		for i in range(self.min, self.max + 1):
			memory_array.append(0)

		self.memory_array = memory_array


	def READ(self, location_int):
		"""Reads a word from the keyboard to somewhere in memory. 

		Args:
			location (_type_): _description_
		"""
		user_input = input(f"Input an integer value to go in memory location {location_int}: ")
		while True:
			try:
				input_int = int(user_input)
				self.memory_array[location_int] = input_int
				break
			except ValueError:
				print("Input is not a valid integer.")
		print(f"Success! {input_int} was added at memory location {location_int}. ")





	def WRITE(self, location_int):
		"""Takes a memory location (int) and prints the value at that location. 

		Args:
			location (_type_): input string
		"""
		if location_int not in range(self.min, self.max + 1):
			print(f"Error: Memory location {location_int} is not valid. It must be between {self.min} and {self.max}.")
		else:
			print(f"At memory location {location_int} is {self.memory_array[location_int]}")




	def LOAD(self, location_int): 
		"""If a valid location, returns the value at that location.

		Args:
			location_int (_int_): The memory location in the array

		Returns:
			_int_: The value at that location
		"""
		# if address is not in the right range return None. 
		if location_int not in range (self.min, self.max + 1):
			print(f"Error: Memory location {location_int} is not valid. It must be between {self.min} and {self.max}.")
		else:
			value_at_location = self.memory_array[location_int]
			print(f"At memory location {location_int} is {value_at_location}")
			return value_at_location




	def STORE(self, accumulator, location_int):
		if location_int not in range (self.min, self.max + 1):
			print(f"Error: Memory location {location_int} is not valid. It must be between {self.min} and {self.max}.")
			print("Not added to memory.")
		else:
			# Error check if accumulator is not an int. 
			try:
				acc_int = int(accumulator)
			except ValueError:
				print("Error: Accumulator value is not an integer.")
				print("Not added to memory.")
			# take accumulator value and set as value at memory location int. 
			self.memory_array[location_int] = acc_int
			print("Added to memory!")
			print(f"At memory location {location_int} is {acc_int}")

			

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
	location1 = 20
	memory.READ(location1)

	location2 = 99
	memory.WRITE(location2)



if __name__ == "__main__":
    main()






# def main():
# 	user_input = input("Place input here: ")
# 	WRITE(user_input)



