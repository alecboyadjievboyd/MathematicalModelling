import Expression
import ExpressionType
import Product
import Exponential
import Constant

class NaturalLogarithm(Expression): #Tim here, I had to add this as it is needed when differentiating Exponential. Feel free to change stuff.
    def __init__(self, argument):
        super().__init__(ExpressionType.NATURALLOG)
        self.argument = argument
        
    def __str__(self):
        return f'ln({self.argument})'
    
    def derivative(self, differential):
        return Product((Exponential(self.argument, Constant(-1)), self.argument.derivative(differential)))