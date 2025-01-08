from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.product import Product
from Model.cosine import Cosine
from Model.exponential import Exponential
from Model.integer import Integer


# Tangent of an expression
class Tangent(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.TANGENT)
        self.argument = argument
        self.isconstant = None
        self.primaryOrder = 5 # Single Function
        self.secondaryOrder = 4 # Tan
        
    def __str__(self):
        return f'tan({self.argument})'
    
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
            if (self.secondaryOrder == other.secondaryOrder): # Both tan
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
        return Product({Exponential(Cosine(self.argument), Integer(-2)), self.argument.derivative(differential)})

    def genarg(self):#needed for constant simplification (consim)
        return (self.argument,)
    
    def consim(self): #simplified form

        sa = self.argument.consim() #simplify the arg first

        if sa.expression_type == ExpressionType.ARCTANGENT:
            return sa.argument # tan(arctan(f(x))) = f(x)
        else:
            return Tangent(sa) 
    
    def pfsf(self, safeMode = False): #simplified form

        argPfsf = self.argument.pfsf(safeMode) #simplify the arg first

        if argPfsf.expression_type == ExpressionType.ARCTANGENT:
            return argPfsf.argument # tan(arctan(f(x))) = f(x)
        else:
            return Tangent(argPfsf) 

        # Otherwise, ignore for now as we are not doing identities
