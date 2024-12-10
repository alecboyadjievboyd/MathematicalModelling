from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.exponential import Exponential
from Model.product import Product
from Model.constant import Constant


class Logarithm(Expression):
    def __init__(self, base, argument):
        super().__init__(ExpressionType.LOGARITHM)
        self.base = base
        self.argument = argument
        self.isConstant = None
        self.primaryOrder = 5 # Single Function
        self.secondaryOrder = 7 # Log

    def __str__(self):
        return f'log_{self.base}({str(self.argument)})'

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

    def derivative(self, differential):
        return Product([
            self.argument.derivative(differential),
            Exponential(Logarithm(Constant('e'), self.base), -1),
            Exponential(self, -1)
        ])

    def genarg(self):#needed for constant simplification (consim)
        return (self.base, self.argument)
    
    def pfsf(self):
        # We want to do the following:
        # Consolidate if arg is an exponent with the same base.
        # move y to the front if arg is an exponent with not the same base (log(x^y) = ylog(x))
        # that is all I can think of so far. 

        # Simplify innards first

        argPfsf = self.argument.pfsf()
        basePfsf = self.base.pfsf()

        if argPfsf == basePfsf: # If the argument is exactly the base
            return Constant(1)

        if argPfsf.expression_type == ExpressionType.EXPONENTIAL: # If the argument is an exponential 
            
            # If bases are the same
            if argPfsf.base == basePfsf:
                return argPfsf.arg # Return just the argument of the exponential 
            
            # If bases are not the same
            else: 
                return Product(argPfsf.arg, Logarithm(basePfsf, argPfsf.base)).pfsf() # To make sure that it is simplified
            
        # If none of these hold
        return Logarithm(basePfsf, argPfsf)
            