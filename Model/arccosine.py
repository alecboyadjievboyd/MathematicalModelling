from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.product import Product
from Model.exponential import Exponential
from Model.sum import Sum
from Model.integer import Integer

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

    def derivative(self, differential, safeMode = False):
        simpSelf = self.pfsf(safeMode)
        if simpSelf == self: # if no change
            return Product((Integer(-1),
                        Exponential(Sum((Integer(1), Product((Integer(-1), Exponential(self.argument, Integer(2))))))
                                    , Product((Integer(-1), Exponential(Integer(2), Integer(-1))))),
                        self.argument.derivative(differential))).pfsf(safeMode)
        else:
            return simpSelf.derivative(differential, safeMode)
        
    
    def genarg(self): #needed for constant simplification (consim)
        return (self.argument,)
    
    def consim(self, safeMode = False):
        from Model.cosine import Cosine
        from Model.fraction import Frac
        from Model.pi import Pi

        x = self.argument.consim(safeMode)
        for b in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12):
            if Cosine(Product((Frac(b, 12), Pi()))).consim(safeMode) == x:
                return Product((Frac(b, 12), Pi())).consim(safeMode)


        return Arccosine(self.argument.consim(safeMode)) 

    def pfsf(self, safeMode = False): #simplified form
        #if this is updated, consim should probably also be updated

        argPfsf = self.argument.pfsf(safeMode)

        #if argPfsf.expression_type == ExpressionType.COSINE:
            #return argPfsf.argument # arccos(cos(f(x))) = f(x)
        #else:
            #return Arccosine(argPfsf) 

        return Arccosine(argPfsf)

        # Otherwise, ignore for now as we are not doing identities
