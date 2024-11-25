import Expression
import ExpressionType
import Product
import Cosine

class Sine(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.SINE)
        self.argument = argument
        
    def __str__(self):
        return f'sin({self.argument})'
    
    def derivative(self, differential):
        return Product({Cosine(self.argument), self.argument.derivative(differential)})