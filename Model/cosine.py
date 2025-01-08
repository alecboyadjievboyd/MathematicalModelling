from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.product import Product
from Model.integer import Integer


# Cosine of an expression
class Cosine(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.COSINE)
        self.argument = argument
        self.isconstant = None
        self.primaryOrder = 5 # Single Function
        self.secondaryOrder = 5 # Cos
        
    def __str__(self):
        return f'cos({self.argument})'
    
    # THIS ONLY CHECKS PFSF FORM EQUIVALENCE
    def __eq__(self, other):
        if (self.expression_type != other.expression_type):
            return False
        if (str(self) == str(other)):
            return True
        else: return False

    def __gt__(self, other):

        if (self.isConstant() == False) and other.isConstant():
            return True
        
        if (self.primaryOrder == other.primaryOrder): # Both functions
            if (self.secondaryOrder == other.secondaryOrder): # Both cos
                return self.argument > other.argument
            else:
                return self.secondaryOrder > other.secondaryOrder # Ordering of functions
        else: 
            return self.primaryOrder > other.primaryOrder # Ordering classes

    def isConstant(self):
        if self.isconstant == None: 
            if self.argument.isConstant() == True:
                self.isconstant = True
            else:
                self.isconstant = False
        return self.isconstant
    
    def derivative(self, differential):
        from Model.sine import Sine
        return Product({Integer(-1), Sine(self.argument), self.argument.derivative(differential)})
    
    def genarg(self):#needed for constant simplification (consim)
        return (self.argument,)
    
    def consim(self):
        sa = self.argument.consim()

        if sa.expression_type == ExpressionType.ARCCOSINE:
            return sa.argument # cos(arccos(f(x))) = f(x)
        else:
            return Cosine(sa)         

    def pfsf(self, safeMode = False): #simplified form

        argPfsf = self.argument.pfsf(safeMode)

        if argPfsf.expression_type == ExpressionType.ARCCOSINE:
            return argPfsf.argument # cos(arccos(f(x))) = f(x)
        else:
            return Cosine(argPfsf) 

        # Otherwise, ignore for now as we are not doing identities