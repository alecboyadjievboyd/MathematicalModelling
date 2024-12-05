from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.product import Product


# Cosine of an expression
class Exp(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.EXP)
        self.argument = argument
        self.isConstant = None
        
    def __str__(self):
        return f'exp({self.argument})'
    
    def __eq__(self, other):
        if (self.expression_type != other.expression_type):
            return False
        if (str(self) == str(other)):
            return True
        else: return False

    # I assume here that this class is meant to represent e^f(x)?
    def isConstant(self):
        if self.isConstant == None: 
            if self.argument.isConstant():
                self.isConstant = True
            else:
                self.isConstant = False
        return self.isConstant
                
    
    def derivative(self, differential):
        return Product((Exp(self.argument), self.argument.derivative(differential)))

    def genarg(self):#needed for constant simplification (consim)
        return (self.argument,)