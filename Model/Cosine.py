from expression import Expression
from expression_type import ExpressionType
from product import Product
from constant import Constant

# Cosine of an expression
class Cosine(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.COSINE)
        self.argument = argument
        
    def __str__(self):
        return f'cos({self.argument})'
    
    def derivative(self, differential):
        from sine import Sine
        return Product({Constant(-1), Sine(self.argument), self.argument.derivative(differential)})