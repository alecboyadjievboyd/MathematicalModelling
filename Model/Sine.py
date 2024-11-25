from expression import Expression
from expression_type import ExpressionType
from product import Product

# Sine of an expression
class Sine(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.SINE)
        self.argument = argument
        
    def __str__(self):
        return f'sin({self.argument})'
    
    def derivative(self, differential):
        from cosine import Cosine
        return Product({Cosine(self.argument), self.argument.derivative(differential)})