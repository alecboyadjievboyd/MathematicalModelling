from Expression import Expression
from expression_type import ExpressionType
from Product import Product
from Cosine import Cosine

# Sine of an expression
class Sine(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.SINE)
        self.argument = argument
        
    def __str__(self):
        return f'sin({self.argument})'
    
    def __eq__(self, other):
        if (self.expression_type != other.expression_type):
            return False
        return self.argument == other.argument
    
    def derivative(self, differential):
        return Product({Cosine(self.argument), self.argument.derivative(differential)})