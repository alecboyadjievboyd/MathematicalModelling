from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.product import Product
from Model.constant import Constant


# Cosine of an expression
class Exp(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.EXP)
        self.argument = argument
        self.isConstant = None
        self.primaryOrder = 5 # Single Function
        self.secondaryOrder = 8 # Exp (top priority) 
        
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
    
    def __gt__(self, other):

        if (self.isConstant() == False) and other.isConstant():
            return True
        
        if (self.primaryOrder == other.primaryOrder): # Both functions
            if (self.secondaryOrder == other.secondaryOrder): # Both exp
                
                # We must check if the other one is exponential or exp

                if other.expressionType == self.ExpressionType: # both exp
                    return self.argument > other.argument
                else:
                    if other.base == Constant("e"): # If the other base is equal
                        return self.exponent > other.argument
                    else:
                        return Constant("e") > other.base
                    

            else:
                return self.secondaryOrder > other.secondaryOrder # Ordering of functions
        else: 
            return self.primaryOrder > other.primaryOrder # Ordering classes
                
    
    def derivative(self, differential):
        return Product((Exp(self.argument), self.argument.derivative(differential)))

    def genarg(self):#needed for constant simplification (consim)
        return (self.argument,)