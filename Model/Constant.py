from Expression import Expression
from expression_type import ExpressionType

# Integer constant. Terminal expression.
class Constant(Expression):

    def __init__(self, value):
        super().__init__(ExpressionType.CONSTANT)
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def __eq__(self, other):
        return (self.value == other.value)
    
    def derivative(self, differential):
        return Constant(0)
    
    def pfsf(self):
        return Constant(self.value)