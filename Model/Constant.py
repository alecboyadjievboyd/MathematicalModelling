from Expression import Expression
from expression_type import ExpressionType

# Integer constant. Terminal expression.
class Constant(Expression):

    def __init__(self, value:int):
        if type(value) != int:
            raise Exception("Constants need to be integers") #I wrote this, however it feels a bit weird (I imagine Constant("Pi") could become relevant). If you want to remove it, please have Frac.__init__ check whether the Constants have int values and send a Whatsapp informing about this to Tim.
        super().__init__(ExpressionType.CONSTANT)
        self.value = value
        self.isConstant = True 

    def __str__(self):
        return str(self.value)
    
    def __eq__(self, other):
        if (self.expression_type != other.expression_type):
            return False
        if (str(self) == str(other)):
            return True
        else: return False

    def isConstant(self):
        return True
    
    def derivative(self, differential):
        return Constant(0)
    
    def pfsf(self):
        return Constant(self.value)