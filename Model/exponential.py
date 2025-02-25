from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.product import Product
from Model.sum import Sum
from Model.integer import Integer
from Model.variable import Variable
from Model.vartocon import Vartocon


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
        return "(" + self.put_brackets(self.base) + "^" + self.put_brackets(self.argument) + ")"
    
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

                if (
                    (self.base.expression_type == ExpressionType.VARIABLE and self.argument.isConstant())  #monomial
                    and 
                    other.base.expression_type != ExpressionType.VARIABLE): #not monomial
                    
                    return False

                if (
                    (other.base.expression_type == ExpressionType.VARIABLE and other.argument.isConstant())  #monomial
                    and 
                    self.base.expression_type != ExpressionType.VARIABLE): #not monomial  

                    return True

                if (
                    (other.base.expression_type == ExpressionType.VARIABLE and other.argument.isConstant())  #monomial
                    and 
                    self.base.expression_type == ExpressionType.VARIABLE and self.argument.isConstant()): # also monomial   

                        if self.base == other.base: # if the base is the same variable
                            return self.argument > other.argument #compare exponents  
                        else:
                            return self.base > other.base
                
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
    
    def derivative(self, differential, safeMode = False):
        from Model.natural_logarithm import NaturalLogarithm
        simpSelf = self.pfsf(safeMode)
        if simpSelf == self: # if no change
            return Product([self, 
                        Sum(( Product([self.argument.derivative(differential), NaturalLogarithm(self.base)]),
                            Product([self.argument, Exponential(self.base, Integer(-1)), self.base.derivative(differential)])
                            ))
                        ]).pfsf(safeMode)
        else:
            return simpSelf.derivative(differential, safeMode)

    def genarg(self):#needed for constant simplification (consim)
        return (self.base, self.argument) #return (self.base, self.exponent)
    
    def consim(self, safeMode = False):
        #todo: (ab)^c vs a^c * b^c. We want (ab)^c. Issue probably lies at Alec.
        #todo: 
        # Product((Frac(1,2), Frac(2).root(2))
        # (Frac(1,2).root(2)
        # do not consim to the same thing and their ratio does not consim to 1.

        def AskAlec(x, safeMode = False):
            try:
                # y = x.pfsf(safeMode)
                # print(f"Exponential.consim asks Alec: {x}")
                # print(f"Alec says: {y}")
                # return y
                return x.pfsf(safeMode)
            except:
                # print(f"Exponential.consim asks Alec: {x}")
                # print("Alec doesn't know")
                return x
        
        from Model.fraction import Frac

        old = self #not sure if this is necessary

        #simplifying the arguments
        sb = self.base.consim(safeMode) #sb = simplified base
        se = self.argument.consim(safeMode) #se = simplified exponent(somehow we use .argument instead of .exponent)
        
        if se == Frac(0):#a^0=0
            return Frac(1) 
        elif sb == Frac(1):
            return Frac(1)
        elif sb == Frac(0):#0^a=0, but undefined for a<0
            if se.expression_type == ExpressionType.FRACTION:
                if se.num.value < 0: #
                    # print(f"MATH ERROR: Zero to negative power: {Exponential(sb, se)}")
                    raise Exception(f"MATH ERROR: Zero to negative power: {Exponential(sb, se)}")
            return Frac(0) #0^(negative function) returns 0. If se<0, the original domain was the empty set and now is all of R.
        #consider 0^a. Assuming a is not identified by us to be Frac(0), this returns 0. However, this assumes we can identify when a is equal to 0. 


        if se.expression_type == ExpressionType.LOGARITHM:
            if se.base == sb:
                return se.argument#.consim(safeMode) #consim maybe not necessary if logarithm consims its arguments

        #simplifying frac^frac
        if sb.expression_type == se.expression_type == ExpressionType.FRACTION:
            return sb.fracpow(se)
        

        elif sb.expression_type == ExpressionType.SUM:
            #sums to integer or frac power
            if se.expression_type == ExpressionType.FRACTION:
                varterms = ()
                for term in sb.terms:
                    varterms += (Variable(term),)

                #is this a desired simplified form? 
                #e.g. (3+x)^(5/2) -> (3+x)^2 * (3+x)^(1/2)
                #e.g. (3+x)^(-5/2) -> (3+x)^-2 * (3+x)^(-1/2)
                if se.squo() != Integer(0):
                    if se.srem() != Integer(0):
                        varsim = AskAlec(
                            Product(( Exponential(Sum(varterms), se.squo()), Exponential(Sum(varterms), Frac(se.srem(),se.den)) ))
                        , safeMode)
                    else:
                        varsim = AskAlec(Exponential(Sum(varterms), se.squo()), safeMode)
                else:
                    if se.srem()!= Integer(0):
                        varsim = AskAlec(Exponential(Sum(varterms), Frac(se.srem(),se.den)), safeMode)
                    else:
                        return Frac(1)
                    
                new = Vartocon(varsim)
                if old == new: #recall "old = Exponential(sb, se)"
                    return new
                else:
                    return new.consim(safeMode)

            #generalisation of sum^frac: sum^(frac + stuff) -> sum^frac * sum^stuff
            elif se.expression_type == ExpressionType.SUM:
                # print("sum^sum")
                fracsum = Frac(0) 
                nonfracterms = ()
                for term in se.terms:
                    if term.expression_type == ExpressionType.FRACTION: #There should be at most one fraction in the sum though.
                        fracsum += term
                    else:
                        nonfracterms += (term, )
                if fracsum.squo() == Integer(0):
                    return Exponential(sb, se)
                else:
                    return Product((
                        Exponential(sb, fracsum.squo()),
                        Exponential(sb, Sum( nonfracterms + (Frac(fracsum.srem(), fracsum.den), ) ))
                    )).consim(safeMode)
                        
        elif se.expression_type == ExpressionType.SUM:
            #as we are here, we know sb.expression_type != ExpressionType.SUM
            if sb.expression_type == ExpressionType.FRACTION:
                fracsum = Frac(0) 
                nonfracterms = ()
                for term in se.terms:
                    if term.expression_type == ExpressionType.FRACTION: #There should be at most one fraction in the sum though.
                        fracsum += term
                    else:
                        nonfracterms += (term, )
                if fracsum == Frac(0):
                    return Exponential(sb, se)
                else:
                    if fracsum == Frac(0):
                        return Exponential(sb, se)
                    else:
                        return Product((
                            sb.fracpow(fracsum),
                            Exponential(sb, Sum(nonfracterms))#.consim(safeMode)
                        )).consim(safeMode)
                    # if fracsum.squo() == Integer(0):
                    #     return Exponential(sb, se)
                    # else:
                    #     return Product((
                    #         sb**(fracsum.squo()), 
                    #         Exponential(sb, Sum( nonfracterms + (Frac(fracsum.srem(), fracsum.den),) ))
                    #     )).consim(safeMode)

          

        #Collapsing towers
        if sb.expression_type == ExpressionType.EXPONENTIAL:
            #we could additionally check if sb.base is an exponential with base != 0 and power even (or even Frac), such that sb.base is positive and all other powers may be collapsed.
            if sb.base.expression_type == ExpressionType.FRACTION:
                if sb.base.num.value>0:
                    return Exponential(sb.base, Product((sb.argument,se)) ).consim(safeMode) #(a^b)^c -> a^(b*c) but that only holds for a>0
                else: #sb.base.num.value <0: (if sb.base==0, then sb would have been simplified to Frac(0) and we wouldn't be here)
                    # if safeMode:
                    return Exponential(sb, se)
                    # else:
                    #     #shouldnt we do Exponential(sb, se) here as well? We know we cannot collapse the tower. Yes, implemented as of now
                    #     print(f"Warning: Safe Mode Off! Applying (a^b)^c -> a^(bc), Expression May no longer be well defined. Simplifying {Exponential(sb, se)} into {Exponential(sb.base, Product((sb.argument, se)))}")
                    #     return Exponential(sb.base, Product((sb.argument,se)) ).consim(safeMode)
            elif sb.base.expression_type == ExpressionType.EULER or sb.base.expression_type == ExpressionType.PI:
                return Exponential(sb.base, Product((sb.argument,se)) ).consim(safeMode) #(a^b)^c -> a^(b*c) but that only holds for a>0
            else:
                if safeMode:
                    return Exponential(sb, se)
                else:
                    print(f"Warning: Safe Mode Off! Applying (a^b)^c -> a^(bc), Expression may no longer be well defined. Simplifying {Exponential(sb, se)} into {Exponential(sb.base, Product((sb.argument, se)))}")
                    return Exponential(
                        sb.base,
                        Product((
                            sb.argument,
                            se
                        ))
                    ).consim(safeMode)


        if sb.expression_type == ExpressionType.PRODUCT:
            takenout = () #factors taken out of the exponential, already exponentiated
            keptin = () #factors kept in the exponential, not exponentiated
            sgnin = 1 #new factor for inside the exponential
            if se.expression_type == ExpressionType.FRACTION and se.den.value % 2 == 1:
                for factor in sb.factors:
                    takenout += (Exponential(factor, se),)
            else:
                for factor in sb.factors:
                    if factor.expression_type == ExpressionType.FRACTION:
                        if factor > Frac(0):
                            takenout += (Exponential(factor, se),)
                        else: #factor < Frac(0), as factor==Frac(0) would have simplified the product to 0 and we wouldnt be here
                            if factor == Frac(-1): #this also prevents inf recursion
                                keptin += (factor,)
                            else:
                                takenout += (Exponential(Frac(-1)*factor, se),)
                                sgnin *= -1
                    elif factor.expression_type == ExpressionType.PI or factor.expression_type == ExpressionType.EULER:
                        takenout += (Exponential(factor, se),)
                    else:
                        if safeMode:
                            keptin += (factor,)
                        else:
                            print(f"Warning: Safe Mode Off! Applying (ab)^c = a^c b^c, Expression may no longer be well defined. Taking {Exponential(factor, se)} out of {Exponential(sb, se)} ")
                            takenout += (Exponential(factor, se),)
            if len(takenout) == 0: #this also prevents infinite recursion
                return Exponential(sb, se)
            else:
                return Product(
                    takenout
                    + (Exponential(
                        Product(
                            (Frac(sgnin),) +
                            keptin
                        ),
                        se
                    ),)
                ).consim(safeMode)
                

             
        # # (ab)^c = (a)^c (b)^c case
        # if basePfsf.expression_type == ExpressionType.PRODUCT:
        #     print("Warning: Safe Mode Off! Applying (ab)^c = a^c b^c, Domain Issues May Emerge")
        #     newFactors = []
        #     for factor in basePfsf.factors:
        #         newFactors.append(Exponential(factor, argPfsf))
        #     return Product(newFactors)
        
        #if nothing is returned yet
        return Exponential(sb, se)
    
    def pfsf(self, safeMode = False):
        from Model.logarithm import Logarithm
        # Possible rules
        # If the exponent is a logarithm with the same base, consolidate
        # If the base is an exponent, consolidate with the top factor.
        # If the exponent is an integer AND the base a sum, turn it into a product
        # so that we can later distribute when simplifying the product

        # Simplify innards first

        argPfsf = self.argument.pfsf(safeMode)
        basePfsf = self.base.pfsf(safeMode)

        # Exponent one case nad 0 case
        if argPfsf.expression_type == ExpressionType.INTEGER:
            if ( argPfsf.value == 1):
                return basePfsf
        
            if (argPfsf.value == 0):
                return Integer(1)
            
        # Integer Exponent case
        if (basePfsf.expression_type == ExpressionType.SUM) and (argPfsf.expression_type == ExpressionType.INTEGER and  argPfsf.value >= 2): # will always be a sum with one or more terms because it has been pfsf iffied
            terms = []
            for i in range(0, argPfsf.value, 1): 
                terms.append(basePfsf) # Should work even though they are duplicates? I cannot forsee issues

            return Product(terms).pfsf(safeMode)

        # THE FOLLOWING CAUSE DOMAIN ISSUES
        if(not safeMode): 
            # Logarithm case
            if argPfsf.expression_type == ExpressionType.LOGARITHM:
                if basePfsf == argPfsf.base: #bases are the same
                    print("Warning: Safe Mode Off! Applying b^(log_b(a)) = a, Domain Issues May Emerge")
                    return argPfsf.argument
                
                # If the bases are not the same, it is trickier
                else: 
                    if argPfsf.argument > basePfsf: 
                        print("Warning: Safe Mode Off! Applying y^log_b(x) -> x^log_b(y), Domain Issues May Emerge")
                        # if the argument inside the upper logarithm is more complex, 
                        # swap the base and that argument
                        return Exponential(argPfsf.argument, Logarithm(argPfsf.base, basePfsf)) 
                        # This essentially is y^log_b(x) -> x^log_b(y) iff x is more compelex than y

                    # If the argument is less complex or identical, we do nothing
    
            # Exponential case
            if basePfsf.expression_type == ExpressionType.EXPONENTIAL:
                print("Warning: Safe Mode Off! Applying (y^a)^b = y^ba, Domain Issues May Emerge")
                return Exponential(basePfsf.base, Product([argPfsf, basePfsf.argument]).pfsf(safeMode)) # (y^a)^b = y^ba
                # Note that here we pfsf the product after creating it to ensure that the order is good.

            # (ab)^c = (a)^c (b)^c case
            if basePfsf.expression_type == ExpressionType.PRODUCT:
                print("Warning: Safe Mode Off! Applying (ab)^c = a^c b^c, Domain Issues May Emerge")
                newFactors = []
                for factor in basePfsf.factors:
                    newFactors.append(Exponential(factor, argPfsf))
                return Product(newFactors)
        
        # If none of these hold, simply return itself with simplified base and argument
        return Exponential(basePfsf, argPfsf)

        