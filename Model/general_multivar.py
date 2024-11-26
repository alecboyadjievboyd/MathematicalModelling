from Expression import Expression
from expression_type import ExpressionType

class GeneralMultivar(Expression):
    def __init__(self, symbol:str):
        super().__init__(ExpressionType.GENERALMULTIVAR)
        self.symbol = symbol
    
    def __str__(self):
        return self.symbol + "(x)"
    
    def __eq__(self, other):
        return self.symbol == other.symbol
    
    def derivative(self, differential):
        return GeneralMultivar(f"d{self.symbol}/d{differential}") # df/dx1