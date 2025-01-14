from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.exponential import Exponential
from Model.product import Product
from Model.integer import Integer
from Model.euler import Euler
from Model.fraction import Frac

class Logarithm(Expression):
    def __init__(self, base, argument):
        super().__init__(ExpressionType.LOGARITHM)
        self.base = base
        self.argument = argument
        self.isconstant = None
        self.primaryOrder = 5 # Single Function
        self.secondaryOrder = 7 # Log

    def __str__(self):
        return f'log_{self.base}({str(self.argument)})'
    
    def isConstant(self):
        if self.isconstant is None:
            if self.argument.isConstant() and self.base.isConstant():
                self.isconstant = True
            else:
                self.isconstant = False
        return self.isconstant

    def __eq__(self, other):
        if self.expression_type != other.expression_type:
            return False
        if str(self) == str(other):
            return True
        else:
            return False
        
    def __gt__(self, other):

        if (self.isConstant() == False) and other.isConstant():
            return True
        
        if (self.primaryOrder == other.primaryOrder): # Both functions
            if (self.secondaryOrder == other.secondaryOrder): # Both log
                if other.base == self.base: # If the other base is equal
                    return self.argument > other.argument
                else:
                    return self.base > other.base                  
            else:
                return self.secondaryOrder > other.secondaryOrder # Ordering of functions
        else: 
            return self.primaryOrder > other.primaryOrder # Ordering classes

    def derivative(self, differential, safeMode = False):
        return Product([
            self.argument.derivative(differential),
            Exponential(Logarithm(Euler(), self.base), -1),
            Exponential(self, -1)
        ]).pfsf(safeMode)

    def genarg(self):#needed for constant simplification (consim)
        return (self.base, self.argument)
    
    def consim(self, safeMode = False):
        #todo: find out if log_frac1(frac2) is an integer (or 1/integer) and if so, return that integer
        sb = self.base.consim(safeMode)
        sa = self.argument.consim(safeMode)

        if sa==sb:
            return Frac(1)
        elif sa.expression_type == ExpressionType.EXPONENTIAL:
            if sa.base == sb:
                return sa.argument
        
        return Logarithm(sb, sa)
    
    def pfsf(self, safeMode = False):
        # We want to do the following:
        # Consolidate if arg is an exponent with the same base.
        # move y to the front if arg is an exponent with not the same base (log(x^y) = ylog(x))
        # that is all I can think of so far. 

        # Simplify innards first

        argPfsf = self.argument.pfsf(safeMode)
        basePfsf = self.base.pfsf(safeMode)

        # All of these break if base is negative
        if (not safeMode):
            if argPfsf == basePfsf: # If the argument is exactly the base
                print("Warning: Safe Mode Off! Applying log_b(b) -> 1, Domain Issues May Emerge")
                return Integer(1)

            if argPfsf.expression_type == ExpressionType.EXPONENTIAL: # If the argument is an exponential 
                
                # If bases are the same
                if argPfsf.base == basePfsf:
                    print("Warning: Safe Mode Off! Applying log_b(b^a) = a, Domain Issues May Emerge")
                    return argPfsf.argument # Return just the argument of the exponential 
                
                # If bases are not the same # NOTE might want to check if this is always preferable in complexity. IT IS NOT BECAUSE PROD FUCNTIONS IS MORE COMPLEX THAN SINGLE FUCNTION
                #else: 
                    #return Product(argPfsf.argument, Logarithm(basePfsf, argPfsf.base)).pfsf() # To make sure that it is simplified
            
        # If none of these hold
        return Logarithm(basePfsf, argPfsf)
            