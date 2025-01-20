from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.product import Product
from Model.exponential import Exponential
from Model.sum import Sum
from Model.integer import Integer

class Arcsine(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.ARCSINE)
        self.argument=argument
        self.isconstant = None
        self.primaryOrder = 5 # Single Function
        self.secondaryOrder = 3 # Arcsin 
    
    def __str__(self):
        return f"arcsin({self.argument})"
    
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
            if (self.secondaryOrder == other.secondaryOrder): # Both arcsin
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

    def derivative(self, differential, safeMode = False):
        simpSelf = self.pfsf(safeMode)
        if simpSelf == self: # if no change
            return Product((
            Exponential(Sum((Integer(1), Product((Integer(-1), Exponential(self.argument, Integer(2))))))
                        , Product((Integer(-1), Exponential(Integer(2), Integer(-1))))),
                           self.argument.derivative(differential))).pfsf(safeMode)
        else:
            return simpSelf.derivative(differential, safeMode)
        

    def genarg(self):#needed for constant simplification (consim)
        return (self.argument,)
    
    def consim(self, safeMode = False):
        return Arcsine(self.argument.consim(safeMode))
    
    def pfsf(self, safeMode = False): #simplified form
        #if this is updated, consim should probably also be updated

        argPfsf = self.argument.pfsf(safeMode) #simplify the arg first

        # if argPfsf.expression_type == ExpressionType.SINE:
            #return argPfsf.argument # arcsin(sin(f(x))) = f(x)
        #else: 
            #return Arcsine(argPfsf) 

        return Arcsine(argPfsf) 

        # Otherwise, ignore for now as we are not doing identities