from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.product import Product
from Model.sum import Sum
from Model.constant import Constant


# Exponential function with an expression as a base and exponent
class Exponential(Expression):

    def __init__(self, base, argument):
        super().__init__(ExpressionType.EXPONENTIAL)
        self.base = base
        self.argument = argument
        self.isConstant = None
        self.primaryOrder = 5 # Single Function
        self.secondaryOrder = 8 # Exp (top priority) 
    
    def __str__(self):
        return self.put_brackets(self.base) + "^" + self.put_brackets(self.exponent)
    
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
            if (self.secondaryOrder == other.secondaryOrder): # Both exp
                if other.base == self.base: # If the other base is equal
                    return self.argument > other.argument
                else:
                    return self.base > other.base                  
            else:
                return self.secondaryOrder > other.secondaryOrder # Ordering of functions
        else: 
            return self.primaryOrder > other.primaryOrder # Ordering classes

    def isConstant(self):
        if self.isConstant == None: 
            if self.argument.isConstant() and self.base.isConstant():
                self.isConstant = True
            else:
                self.isConstant = False
        return self.isConstant
    
    def derivative(self, differential):
        from Model.natural_logarithm import NaturalLogarithm
        return Product((self, 
                      Sum(( Product((self.exponent.derivative(differential), NaturalLogarithm(self.base))),
                          Product((self.exponent, Exponential(self.base, Constant(-1)), self.base.derivative(differential)))
                         ))
                      ))

    def genarg(self):#needed for constant simplification (consim)
        return (self.base, self.exponent)
    
    def pfsf(self):
        from Model.logarithm import Logarithm
        # Possible rules
        # If the exponent is a logarithm with the same base, consolidate
        # If the base is an exponent, consolidate with the top factor.
        # If the exponent is an integer AND the base a sum, turn it into a product
        # so that we can later distribute when simplifying the product

        # Simplify innards first

        argPfsf = self.argument.pfsf()
        basePfsf = self.base.pfsf()

        # Logarithm case
        if argPfsf.expression_type == ExpressionType.LOGARITHM:
            if basePfsf == argPfsf.base: #bases are the same
                return argPfsf.argument()
            
            # If the bases are not the same, it is trickier
            else: 
                if argPfsf.argument() > basePfsf: 
                    # if the argument inside the upper logarithm is more complex, 
                    # swap the base and that argument
                    return Exponential(argPfsf.argument(), Logarithm(argPfsf.base, basePfsf)) 
                    # This essentially is y^log_b(x) -> x^log_b(y) iff x is more compelex than y

                # If the argument is less complex or identical, we do nothing
 
        # Exponential case
        if basePfsf.expression_type == ExpressionType.EXPONENTIAL:
            return Exponential(basePfsf.base, Product(argPfsf, basePfsf.arg).pfsf()) # (y^a)^b = y^ba
            # Note that here we pfsf the product after creating it to ensure that the order is good. 

        # Integer Exponent case
        if (basePfsf.expression_type == ExpressionType.SUM) and (argPfsf.expression_type == Constant() and isinstance(argPfsf.value, int)):
            terms = []
            for i in range[argPfsf.value - 1]: 
                terms.append(basePfsf) # Should work even though they are duplicates? I cannot forsee issues

            return Product(terms) # no need to simplify since all terms are identical. 
        
        # If none of these hold, simply return itself (a copy)
        return Exponential(basePfsf, argPfsf)

        