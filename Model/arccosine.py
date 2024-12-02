from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.product import Product
from Model.exponential import Exponential
from Model.sum import Sum
from Model.constant import Constant

class Arccosine(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.ARCCOSINE)
        self.argument=argument
        self.isConstant = None
    
    def __str__(self):
        return f"arccos({self.argument})"
    
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
        return Product((Constant(-1),
                        Exponential(Sum((Constant(1), Product((Constant(-1), Exponential(self.argument, Constant(2))))))
                                    , Product((Constant(-1), Exponential(Constant(2), Constant(-1))))),
                        self.argument.derivative(differential)))
