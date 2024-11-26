from Expression import Expression
from expression_type import ExpressionType
from Product import Product
from Constant import Constant
from Sine import Sine

# Cosine of an expression
class Cosine(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.COSINE)
        self.argument = argument
        
    def __str__(self):
        return f'cos({self.argument})'
    
    def __eq__(self, other):
        return self.argument == other.argument
    
    def derivative(self, differential):
        
        return Product({Constant(-1), Sine(self.argument), self.argument.derivative(differential)})