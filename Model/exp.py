from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.product import Product
from Model.constant import Constant
from Model.exponential import Exponential


# Exp (e^x)
class Exp(Exponential):
    def __init__(self, argument):
        super().__init__(Constant('e'), argument)
        
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
    
    def derivative(self, differential):
        return Product((Exp(self.argument), self.argument.derivative(differential)))

    def genarg(self):#needed for constant simplification (consim)
        return (self.argument,)