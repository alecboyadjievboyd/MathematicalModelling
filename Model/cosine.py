from expression import Expression
from expression_type import ExpressionType
from product import Product
from constant import Constant
from sine import Sine

# Cosine of an expression
class Cosine(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.COSINE)
        self.argument = argument
        self.isConstant = None
        
    def __str__(self):
        return f'cos({self.argument})'
    
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
        
        return Product({Constant(-1), Sine(self.argument), self.argument.derivative(differential)})