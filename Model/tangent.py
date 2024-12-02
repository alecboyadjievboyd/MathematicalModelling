from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.product import Product
from Model.cosine import Cosine
from Model.exponential import Exponential
from Model.constant import Constant


# Tangent of an expression
class Tangent(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.TANGENT)
        self.argument = argument
        self.isConstant = None
        
    def __str__(self):
        return f'tan({self.argument})'
    
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
        return Product({Exponential(Cosine(self.argument), Constant(-2)), self.argument.derivative(differential)})
