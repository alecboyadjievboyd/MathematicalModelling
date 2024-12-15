from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.product import Product
from Model.sum import Sum
from Model.constant import Constant
from Model.variable import Variable


# Exponential function with an expression as a base and exponent
class Exponential(Expression):

    def __init__(self, base, argument):
        super().__init__(ExpressionType.EXPONENTIAL)
        self.base = base
        self.argument = argument
        self.isconstant = None
        self.primaryOrder = 5 # Single Function
        self.secondaryOrder = 8 # Exp (top priority) 
    
    def __str__(self):
        return self.put_brackets(self.base) + "^" + self.put_brackets(self.argument)
    
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
        if self.isconstant is None: 
            if self.argument.isConstant() and self.base.isConstant():
                self.isconstant = True
            else:
                self.isconstant = False
        return self.isconstant
    
    def derivative(self, differential):
        from Model.natural_logarithm import NaturalLogarithm
        return Product((self, 
                      Sum(( Product((self.argument.derivative(differential), NaturalLogarithm(self.base))),
                          Product((self.argument, Exponential(self.base, Constant(-1)), self.base.derivative(differential)))
                         ))
                      ))

    def genarg(self):#needed for constant simplification (consim)
        return (self.base, self.argument) #return (self.base, self.exponent)
    
    def consim(self):
        def AskAlec(x):
            print(f"Exponential.consim asks Alec: {x}")
            try:
                y = x.pfsf()
                print(f"Alec says: {y}")
                return y
            except:
                print("Alec doesn't know")
                return x
        
        return (self)
        from Model.fraction import Frac

        #simplifying the arguments
        sb = self.base.consim() #sb = simplified base
        se = self.argument.consim() #se = simplified exponent(somehow we use .argument instead of .exponent)
        
        if se == Frac(0):#a^0=0
            return Frac(1) 
        elif sb == Frac(0):#0^a=0, but undefined for a<0
            if se.expression_type == ExpressionType.FRACTION:
                if se.num.value < 0:
                    raise Exception("Zero to negative power")
            return Frac(0) #0^(negative function) returns 0

        #simplifying frac^frac
        if sb.expression_type == se.expression_type == ExpressionType.FRACTION:
            if se.den == Constant(1):
                return sb**se #recall that Frac.__pow__ outputs simplified fraction.
            else:
                if se.num.value < 0:
                    sb = Frac(sb.den, sb.num)
                    se = Frac(- se.num.value, se.den)
                #if se.num.value==0, then se.den would have been 1 and we would have not gotten here
                # se.num.value is now > 0

                if se.quo() == Constant(0):
                    return Exponential(sb, se) #sb**(Frac(se.srem(),se.den))
                else: # se.quo().value > 0:
                    return Product((sb**(se.quo), Exponential(sb, Frac(se.rem(), se.den))  ))


        if sb.expression_type == ExpressionType.EXPONENTIAL:
            if sb.base.expression_type == ExpressionType.FRACTION:
                pass
        
        if sb.expression_type == ExpressionType.SUM:
            if se.expression_type == ExpressionType.FRACTION:
                if se.den.value == 1: #i.e. the exponent is integer
                    #replacing each term by a variable
                    varterms = ()
                    for term in sb.terms:
                        varterms += (Variable(term))

                    # varsim = AskAlec(Exponential(Sum(varterms), se))



        if sb.expression_type == ExpressionType.EXPONENTIAL: 
            if sb.base.expression_type == ExpressionType.FRACTION:
                if sb.base.num.value>0:
                    return Exponential(sb.base, Product((sb.argument,se)) ).consim() #(a^b)^c -> a^(b*c) but that only holds for a>=0
                else: #sb.base.num.value <0: (if sb.base==0, then sb would have been simplified to Frac(0) and we wouldn't be here)
                    #we need 
                    if sb.argument.expression_type == ExpressionType.FRACTION:
                        pass
                    else: #
                        pass
            # else:


    
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
                return argPfsf.argument
            
            # If the bases are not the same, it is trickier
            else: 
                if argPfsf.argument > basePfsf: 
                    # if the argument inside the upper logarithm is more complex, 
                    # swap the base and that argument
                    return Exponential(argPfsf.argument, Logarithm(argPfsf.base, basePfsf)) 
                    # This essentially is y^log_b(x) -> x^log_b(y) iff x is more compelex than y

                # If the argument is less complex or identical, we do nothing
 
        # Exponential case
        if basePfsf.expression_type == ExpressionType.EXPONENTIAL:
            return Exponential(basePfsf.base, Product([argPfsf, basePfsf.argument]).pfsf()) # (y^a)^b = y^ba
            # Note that here we pfsf the product after creating it to ensure that the order is good. 

        # Exponent one case nad 0 case
        if argPfsf.expression_type == ExpressionType.CONSTANT:
            if ( argPfsf.value == 1):
                return basePfsf
        
            if (argPfsf.value == 0):
                return Constant(1)
        
        # Integer Exponent case
        if (basePfsf.expression_type == ExpressionType.SUM) and (argPfsf.expression_type == ExpressionType.CONSTANT and isinstance(argPfsf.value, int)): # will always be a sum with one or more terms because it has been pfsf iffied
            terms = []
            for i in range(0, argPfsf.value, 1): 
                terms.append(basePfsf) # Should work even though they are duplicates? I cannot forsee issues

            return Product(terms).pfsf()
        
        # If none of these hold, simply return itself with simplified base and argument
        return Exponential(basePfsf, argPfsf)

        