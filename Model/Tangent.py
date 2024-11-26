from Expression import Expression
from expression_type import ExpressionType
from Product import Product
from Cosine import Cosine
from Exponential import Exponential
from Constant import Constant

# Tangent of an expression
class Tangent(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.TANGENT)
        self.argument = argument
        
    def __str__(self):
        return f'tan({self.argument})'
    
    def __eq__(self, other):
        return self.argument == other.argument
    
    def derivative(self, differential):
        return Product({Exponential(Cosine(self.argument), Constant(-2)), self.argument.derivative(differential)})