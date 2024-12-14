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
        self.isconstant = None
        self.primaryOrder = 5 # Single Function
        self.secondaryOrder = 2 # Arccos 
    
    def __str__(self):
        return f"arccos({self.argument})"
    
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
            if (self.secondaryOrder == other.secondaryOrder): # Both arccos
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
        return Product((Constant(-1),
                        Exponential(Sum((Constant(1), Product((Constant(-1), Exponential(self.argument, Constant(2))))))
                                    , Product((Constant(-1), Exponential(Constant(2), Constant(-1))))),
                        self.argument.derivative(differential)))
    
    def genarg(self): #needed for constant simplification (consim)
        return (self.argument,)

    def pfsf(self): #simplified form

        argPfsf = self.argument.pfsf()

        #if argPfsf.expression_type == ExpressionType.COSINE:
            #return argPfsf.argument # arccos(cos(f(x))) = f(x)
        #else:
            #return Arccosine(argPfsf) 

        return Arccosine(argPfsf)

        # Otherwise, ignore for now as we are not doing identities
