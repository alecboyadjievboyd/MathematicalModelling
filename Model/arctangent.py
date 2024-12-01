from expression import Expression
from expression_type import ExpressionType
from product import Product
from sum import Sum
from constant import Constant
from exponential import Exponential

class Arctangent(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.ARCTANGENT)
        self.argument=argument
        self.isConstant = None
    
    def __str__(self):
        return f"arctan({self.argument})"
    
    # THIS ONLY CHECKS PFSF FORM EQUIVALENCE
    def __eq__(self, other):
        if (self.expression_type != other.expression_type):
            return False
        if (str(self) == str(other)):
            return True
        else: return False

    def isConstant(self):
        if self.isConstant == None: 
            if self.argument.isConstant() == True:
                self.isConstant = True
            else:
                self.isConstant = False
        return self.isConstant

    def derivative(self, differential):
        return Product((
            Exponential(Sum((Constant(1), Exponential(self.argument, Constant(2)))),Constant(-1)), self.argument.derivative(differential)))
    