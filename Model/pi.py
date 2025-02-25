from Model.integer import Integer
from Model.expression import Expression
from Model.expression_type import ExpressionType


# Constant pi = 3.141592653589793238... Terminal expression.
class Pi(Expression):

    def __init__(self):
        super().__init__(ExpressionType.PI)
        self.primaryOrder = 1
        self.secondaryOrder = None

    def __str__(self):
        return 'pi'

    def __eq__(self, other):
        return self.expression_type == other.expression_type
    
    def __gt__(self, other):
        if other.expression_type == ExpressionType.EULER:
            return True ## More complex than euler
        return False ## less complex than everything else

    def isConstant(self):
        return True

    def derivative(self, differential, safeMode):
        return Integer(0)

    def genarg(self):
        return None
    
    def consim(self, safeMode = False):
        return self
    
    def pfsf(self, safeMode = False):
        return Pi()