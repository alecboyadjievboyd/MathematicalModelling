from Expression import Expression
from expression_type import ExpressionType
from product import Product
from constant import Constant
from sine import Sine

# Cosine of an expression
class Cosine(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.COSINE)
        self.argument = argument
        
    def __str__(self):
        return f'cos({self.argument})'
    
    def __eq__(self, other):
        if (self.expression_type != other.expression_type):
            return False
        return self.argument == other.argument
    
    def derivative(self, differential):
        
        return Product({Constant(-1), Sine(self.argument), self.argument.derivative(differential)})