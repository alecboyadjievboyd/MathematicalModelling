from Expression import Expression
from expression_type import ExpressionType
from Product import Product
from Constant import Constant

# Cosine of an expression
class Exp(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.EXP)
        self.argument = argument
        
    def __str__(self):
        return f'exp({self.argument})'
    
    def __eq__(self, other):
        if (self.expression_type != other.expression_type):
            return False
        if (str(self) == str(other)):
            return True
        else: return False
    
    def derivative(self, differential):
        return Product((Exp(self.argument), self.argument.derivative(differential)))