from Model.expression import Expression
from Model.expression_type import ExpressionType
from enum import Enum


# Constant integer expression. Terminal expression.
class Integer(Expression):

    def __init__(self, value):
        super().__init__(ExpressionType.INTEGER)
        self.value = value
        self.primaryOrder = 1 # Constant, lowest order
        self.secondaryOrder = None # No secondary order

    def __str__(self):
        if self.value >= 0:
            return str(self.value)
        else:
            return f'({str(self.value)})'

    def __eq__(self, other):
        if self.expression_type != other.expression_type:
            return False
        if str(self) == str(other):
            return True
        else:
            return False

    def __gt__(self, other):
        if other.primaryOrder == self.primaryOrder: # Both simple constants
            return self.value > other.value # Compare based on value (NOTE: I AM NOT SURE IF THIS WILL WORK WIHT PI AND E)
        else:
            return False # Other is a more complex form (NOT NECESSARILY NUMERICALLY LARGER)
                             # Eventually we may want to replace this with a comparison based on evaluation
                             # Right now x^(2+1) will be seen as "greater in priority" to x^100, for example

            

    def isConstant(self):
        return True

    def derivative(self, differential):
        return Integer(0)

    def pfsf(self):
        return Integer(self.value)

    def genarg(self):#needed for constant simplification (consim)
        return (self.value,)
        
    def consim(self):
        from Model.fraction import Frac
        return Frac(self)