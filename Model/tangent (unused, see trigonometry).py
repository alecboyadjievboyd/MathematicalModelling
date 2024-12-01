from expression import Expression
from expression_type import ExpressionType
from product import Product
from cosine import Cosine
from exponential import Exponential
from constant import Constant

# Tangent of an expression
class Tangent(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.TANGENT)
        self.argument = argument
        
    def __str__(self):
        return f'tan({self.argument})'
    
    def __eq__(self, other):
        if (self.expression_type != other.expression_type):
            return False
        
        return self.argument == other.argument
    
    def derivative(self, differential):
        return Product({Exponential(Cosine(self.argument), Constant(-2)), self.argument.derivative(differential)})