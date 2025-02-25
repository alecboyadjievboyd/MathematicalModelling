from Model.integer import Integer
from Model.expression import Expression
from Model.expression_type import ExpressionType


# Constant e = 2.718... Terminal expression.
class Euler(Expression):

    def __init__(self):
        super().__init__(ExpressionType.EULER)
        self.primaryOrder = 1
        self.secondaryOrder = None

    def __str__(self):
        return 'e'

    def __eq__(self, other):
        return self.expression_type == other.expression_type
    
    def __gt__(self, other):
        return False ##euler is least complex

    def isConstant(self):
        return True

    def derivative(self, differential, safeMode = False):
        return Integer(0)

    def genarg(self):
        return None
    
    def consim(self, safeMode = False):
        return Euler()
    
    def pfsf(self, safeMode = False):
        return Euler()
    