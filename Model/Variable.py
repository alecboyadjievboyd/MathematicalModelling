from expression_type import ExpressionType
from Expression import Expression
from Constant import Constant

# Singular variables, without constants or exponents. Terminal expression.
class Variable(Expression):

    def __init__(self, index):
        super().__init__(ExpressionType.VARIABLE)
        self.index = index

    def __str__(self):
        return "x" + str(self.index)
    
    def __eq__(self, other):
        return (self.index == other.index)
    
    def derivative(self, differential):
        if self.index == differential.index:
            return Constant(1)
        else:
            return Constant(0)
        
    def pfsf(self):
        return Variable(self.index) 