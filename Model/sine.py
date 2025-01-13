from Model.exponential import Exponential
from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.pi import Pi
from Model.product import Product
from Model.integer import Integer
from Model.sum import Sum


# Sine of an expression
class Sine(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.SINE)
        self.argument = argument
        self.isconstant = None
        self.primaryOrder = 5 # Single Function
        self.secondaryOrder = 6 # Sin 
        
    def __str__(self):
        return f'sin({self.argument})'
    
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
            if (self.secondaryOrder == other.secondaryOrder): # Both sin
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
        from Model.cosine import Cosine
        return Product({Cosine(self.argument), self.argument.derivative(differential)}).pfsf(safeMode)

    def genarg(self):#needed for constant simplification (consim)
        return (self.argument,)
    
    # def consim(self):
    #     simarg = self.argument.consim() #simplified argument
        
    #     if simarg == Frac('pi'):
    #         return Frac(-1)
        
    #     simvar = AskAlec(Sine(simarg))

    def pfsf(self, safeMode = False): #simplified form

        argPfsf = self.argument.pfsf(safeMode) #simplify the arg first

        if argPfsf.expression_type == ExpressionType.ARCSINE:
            return argPfsf.argument # sin(arcsin(f(x))) = f(x)
        else:
            return Sine(argPfsf) 

        # Otherwise, ignore for now as we are not doing identities

    def consim(self, safeMode = False):
        from Model.fraction import Frac

        sa = self.argument.consim(safeMode)

        #sin(a pi) for some values of a.
        evalexact = False
        if sa == Frac(0):
            return Frac(0)
        elif sa.expression_type == ExpressionType.PI:
            a = Frac(1)
            evalexact = True
        elif sa.expression_type == ExpressionType.PRODUCT:
            if len(sa.factors) == 2:
                if sa.factors[0].expression_type == ExpressionType.FRACTION:
                    if sa.factors[1].expression_type == ExpressionType.PI:
                        a = sa.factors[0]
                        evalexact = True
                elif sa.factors[0].expression_type == ExpressionType.PI:
                    if sa.factors[1].expression_type == ExpressionType.FRACTION:
                        a = sa.factors[1]
                        evalexact = True

        if evalexact:
            a = Frac(-1)*( Frac(-1)*(a + Frac(1)) % Frac(2) ) + Frac(1) #this is a but with 2 added/subtracted to it untill a is in (-1,1].

            # if a>Frac(1): 
            #     return Sine(Product((a+Frac(-2), Pi()))).consim()
            # elif a<Frac(-1):
            #     return Sine(Product((a+Frac(2), Pi()))).consim()
            
            # if Frac(-1)<a<Frac(0): #equivalent to next thing, as we have reduced a with %.
            if a<Frac(0):
                return Product((
                    Frac(-1),
                    Sine(Product((
                        a*Frac(-1),
                        Pi()
                    )))
                )).consim()

            if a==Frac(0):
                return Frac(0)
            elif a==Frac(1,12):
                return Sum((
                    Product((
                        Frac(1,4), 
                        Frac(6).root(2)
                    )),
                    Product((
                        Frac(-1,4),
                        Frac(2).root(2)
                    ))
                ))
            elif a==Frac(1,6):
                return Frac(1,2)
            elif a==Frac(1,4):
                return Product((Frac(1,2), Exponential(Frac(2), Frac(1,2))))
            elif a==Frac(1,3):
                return Product((Frac(1,2), Exponential(Frac(3), Frac(1,2))))
            elif a==Frac(5,12):
                return Sum((
                    Product((
                        Frac(1,4), 
                        Frac(6).root(2)
                    )),
                    Product((
                        Frac(1,4),
                        Frac(2).root(2)
                    ))
                ))
            elif a==Frac(1,2):
                return Frac(1)
            elif a==Frac(7,12):
                return Sum((
                    Product((
                        Frac(1,4), 
                        Frac(6).root(2)
                    )),
                    Product((
                        Frac(1,4),
                        Frac(2).root(2)
                    ))
                ))
            elif a==Frac(2,3):
                return Product((Frac(1,2), Exponential(Frac(3), Frac(1,2))))
            elif a==Frac(3,4):
                return Product((Frac(1,2), Exponential(Frac(2), Frac(1,2))))
            elif a==Frac(5,6):
                return Frac(1,2)
            elif a==Frac(11,12):
                return Sum((
                    Product((
                        Frac(1,4), 
                        Frac(6).root(2)
                    )),
                    Product((
                        Frac(-1,4),
                        Frac(2).root(2)
                    ))
                ))
            elif a==Frac(1):
                return Frac(0)
            
        if sa.expression_type == ExpressionType.ARCSINE:
            return sa.argument        
        else:
            return Sine(sa)