from Model.expression import Expression
from Model.expression_type import ExpressionType


class GeneralMultivar(Expression):
    def __init__(self, symbol:str):
        super().__init__(ExpressionType.GENERALMULTIVAR)
        self.symbol = symbol
    
    def __str__(self):
        return self.symbol + "(x)"
    
    def __eq__(self, other):
        if (self.expression_type != other.expression_type):
            return False
        if (str(self) == str(other)):
            return True
        else: return False

    def isConstant(self):
        return False
    
    def derivative(self, differential):
        return GeneralMultivar(f"d{self.symbol}/d{differential}") # df/dx1
    
    def genarg(self):#needed for constant simplification (consim)
        return (self.symbol,)