import Expression
import ExpressionType
import Product
import Cosine
import Exponential
import Constant

# Tangent of an expression
class Tangent(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.TANGENT)
        self.argument = argument
        
    def __str__(self):
        return f'tan({self.argument})'
    
    def derivative(self, differential):
        return Product({Exponential(Cosine(self.argument), Constant(-2)), self.argument.derivative(differential)})