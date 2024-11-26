from Expression import Expression
from expression_type import ExpressionType
from Product import Product
from Constant import Constant

class NaturalLogarithm(Expression): #Tim here, I had to add this as it is needed when differentiating Exponential. Feel free to change stuff.
    def __init__(self, argument):
        super().__init__(ExpressionType.NATURALLOG)
        self.argument = argument
        
    def __str__(self):
        return f'ln({self.argument})'
    
    def __eq__(self, other):
        return self.argument == other.argument
    
    def derivative(self, differential):
        from exponential import Exponential
        return Product((Exponential(self.argument, Constant(-1)), self.argument.derivative(differential)))