from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.product import Product
from Model.integer import Integer
from Model.exponential import Exponential
from Model.euler import Euler


# Exp (e^x)
class Exp(Exponential):
    def __init__(self, argument):
        super().__init__(Euler(), argument)
        
    def __str__(self):
        return f'exp({self.argument})'
    
    # I assume here that this class is meant to represent e^f(x)?
    def isConstant(self):
        if self.isConstant is None: 
            if self.argument.isConstant():
                self.isConstant = True
            else:
                self.isConstant = False
        return self.isConstant
    
    # Should pull GT and EQ from super
    
    def derivative(self, differential, safeMode = False):
        return Product((Exp(self.argument), self.argument.derivative(differential))).pfsf(safeMode)

    def genarg(self):#needed for constant simplification (consim)
        return (self.argument,)