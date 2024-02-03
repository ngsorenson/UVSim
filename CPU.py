from uvsim import UVSim

class CPU:
    def ADD(self, operand, accumulator):
        if isinstance(accumulator, UVSim) and isinstance(operand, int):
            return accumulator + operand
        raise ValueError("Invalid parameter(s)")

    def SUBTRACT(self, operand, accumulator):
        if isinstance(accumulator, UVSim) and isinstance(operand, int):
            return accumulator - operand
        raise ValueError("Invalid parameter(s)")
    
    def MULTIPLY(self, operand, accumulator):
        if isinstance(accumulator, UVSim) and isinstance(operand, int):
            return accumulator * operand
        raise ValueError("Invalid parameter(s)")
    
    def DIVIDE(self, operand, accumulator):
        if isinstance(accumulator, UVSim) and isinstance(operand, int):
            return accumulator // operand
        raise ValueError("Invalid parameter(s)")