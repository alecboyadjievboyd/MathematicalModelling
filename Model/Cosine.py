import Expression
import ExpressionType
import Product
import Sine
import Constant

class Cosine(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.COSINE)
        self.argument = argument
        
    def __str__(self):
        return f'cos({self.argument})'
    
    def derivative(self, differential):
        return Product({Constant(-1), Sine(self.argument), self.argument.derivative(differential)})