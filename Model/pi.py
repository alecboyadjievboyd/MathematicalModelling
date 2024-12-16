from Model.integer import Integer
from Model.expression import Expression
from Model.expression_type import ExpressionType


# Constant pi = 3.141592653589793238... Terminal expression.
class Pi(Expression):

    def __init__(self):
        super().__init__(ExpressionType.PI)

    def __str__(self):
        return 'pi'

    def __eq__(self, other):
        return self.expression_type == other.expression_type

    def isConstant(self):
        return True

    def derivative(self, differential):
        return Integer(0)

    def genarg(self):
        return 'pi'