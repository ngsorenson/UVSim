class CPU:
    def __init__(self, max_val):
        self.max_value= max_val

    def ADD(self, accumulator, value):
        '''returns accumulator + value if both are ints'''
        if isinstance(accumulator, int) and isinstance(value, int):
            output = accumulator + value
            while abs(output) > self.max_value:
                output = output // 10
                print("Overflow on operation: truncating")
            return output

        raise TypeError("Invalid parameter type(s)")

    def SUBTRACT(self, accumulator, value):
        '''returns accumulator - value if both are ints'''
        if isinstance(accumulator, int) and isinstance(value, int):
            output = accumulator - value
            while abs(output) > self.max_value:
                output = output // 10
                print("Overflow on operation: truncating")
            return output
        raise TypeError("Invalid parameter type(s)")
    
    def MULTIPLY(self, accumulator, value):
        '''returns accumulator * value if both are ints'''
        if isinstance(accumulator, int) and isinstance(value, int):
            output = accumulator * value
            while abs(output) > self.max_value:
                output = output // 10
                print("Overflow on operation: truncating")
            return output
        raise TypeError("Invalid parameter type(s)")
    
    def DIVIDE(self, accumulator, value):
        '''returns accumulator // value if both are ints (truncated so that output = value is an int)'''
        if isinstance(accumulator, int) and isinstance(value, int):
            if value != 0:
                output = accumulator // value
                while abs(output) > self.max_value:
                    output = output // 10
                    print("Overflow on operation: truncating")
                return output
            raise ZeroDivisionError
        raise TypeError("Invalid parameter type(s)")