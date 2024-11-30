from expression_type import ExpressionType
from Expression import Expression
from constant import Constant

# Singular variables, without constants or exponents. Terminal expression.
class Variable(Expression):

    def __init__(self, index):
        super().__init__(ExpressionType.VARIABLE)
        self.index = index

    def __str__(self):
        return "x" + str(self.index)
    
    def __eq__(self, other):
        if (self.expression_type != other.expression_type):
            return False
        
        return (self.index == other.index)
    
    def derivative(self, differential):
        if self.index == differential.index:
            return Constant(1)
        else:
            return Constant(0)
        
    def isConstant(self):
        return False
        
    def pfsf(self):
        return Variable(self.index) 