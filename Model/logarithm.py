from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.exponential import Exponential
from Model.product import Product
from Model.constant import Constant


class Logarithm(Expression):
    def __init__(self, base, argument):
        super().__init__(ExpressionType.LOGARITHM)
        self.base = base
        self.argument = argument
        self.isConstant = None
        self.primaryOrder = 5 # Single Function
        self.secondaryOrder = 7 # Log

    def __str__(self):
        return f'log_{self.base}({str(self.argument)})'

    def __eq__(self, other):
        if self.expression_type != other.expression_type:
            return False
        if str(self) == str(other):
            return True
        else:
            return False
        
    def __gt__(self, other):

        if (self.isConstant() == False) and other.isConstant():
            return True
        
        if (self.primaryOrder == other.primaryOrder): # Both functions
            if (self.secondaryOrder == other.secondaryOrder): # Both log
                if other.base == self.base: # If the other base is equal
                    return self.argument > other.argument
                else:
                    return self.base > other.base                  
            else:
                return self.secondaryOrder > other.secondaryOrder # Ordering of functions
        else: 
            return self.primaryOrder > other.primaryOrder # Ordering classes

    def derivative(self, differential):
        return Product([
            self.argument.derivative(differential),
            Exponential(Logarithm(Constant('e'), self.base), -1),
            Exponential(self, -1)
        ])

    def genarg(self):#needed for constant simplification (consim)
        return (self.base, self.argument)