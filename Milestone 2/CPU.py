class CPU:
    def ADD(self, accumulator, value):
        '''returns accumulator + value if both are ints'''
        if isinstance(accumulator, int) and isinstance(value, int):
            return accumulator + value
        raise TypeError("Invalid parameter type(s)")

    def SUBTRACT(self, accumulator, value):
        '''returns accumulator - value if both are ints'''
        if isinstance(accumulator, int) and isinstance(value, int):
            return accumulator - value
        raise TypeError("Invalid parameter type(s)")
    
    def MULTIPLY(self, accumulator, value):
        '''returns accumulator * value if both are ints'''
        if isinstance(accumulator, int) and isinstance(value, int):
            return accumulator * value
        raise TypeError("Invalid parameter type(s)")
    
    def DIVIDE(self, accumulator, value):
        '''returns accumulator // value if both are ints (truncated so that return value is an int)'''
        if isinstance(accumulator, int) and isinstance(value, int):
            if value != 0:
                return accumulator // value
            raise ZeroDivisionError
        raise TypeError("Invalid parameter type(s)")