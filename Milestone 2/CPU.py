class CPU:
    '''
    Pass in the value from UVSim or handle accessing memory to find 
    it from CPU class?
    Parameter validation correct?
    Will this work properly with UVSim class?
    '''
    def ADD(self, accumulator, value):
        if isinstance(accumulator, int) and isinstance(value, int):
            return accumulator + value
        raise TypeError("Invalid parameter type(s)")

    def SUBTRACT(self, accumulator, value):
        if isinstance(accumulator, int) and isinstance(value, int):
            return accumulator - value
        raise TypeError("Invalid parameter type(s)")
    
    def MULTIPLY(self, accumulator, value):
        if isinstance(accumulator, int) and isinstance(value, int):
            return accumulator * value
        raise TypeError("Invalid parameter type(s)")
    
    def DIVIDE(self, accumulator, value):
        if isinstance(accumulator, int) and isinstance(value, int):
            if value != 0:
                return accumulator // value
            raise ZeroDivisionError
        raise TypeError("Invalid parameter type(s)")