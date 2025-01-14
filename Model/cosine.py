from Model.exponential import Exponential
from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.pi import Pi
from Model.product import Product
from Model.integer import Integer
from Model.fraction import Frac
from Model.sum import Sum


# Cosine of an expression
class Cosine(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.COSINE)
        self.argument = argument
        self.isconstant = None
        self.primaryOrder = 5 # Single Function
        self.secondaryOrder = 5 # Cos
        
    def __str__(self):
        return f'cos({self.argument})'
    
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
            if (self.secondaryOrder == other.secondaryOrder): # Both cos
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
        from Model.sine import Sine
        return Product({Integer(-1), Sine(self.argument), self.argument.derivative(differential)}).pfsf(safeMode)
    
    def genarg(self):#needed for constant simplification (consim)
        return (self.argument,)
    
    def consim(self, safeMode = False):
        sa = self.argument.consim(safeMode)

        #cos(a pi) for some values of a.
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
            if a < Frac(0):
                a = Frac(-1)*Frac(a)

            a = a % Frac(2)
            if a > Frac(1):
                a = Frac(2) + Frac(-1)*a

            if a==Frac(0):
                return Frac(1)
            elif a==Frac(1,12):
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
            elif a==Frac(1,6):
                return Product((Frac(1,2), Exponential(Frac(3), Frac(1,2))))
            elif a==Frac(1,4):
                return Product((Frac(1,2), Exponential(Frac(2), Frac(1,2))))
            elif a==Frac(1,3):
                return Frac(1,2)
            elif a==Frac(5,12):
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
            elif a==Frac(1,2):
                return Frac(0)
            elif a==Frac(7,12):
                return Product((Frac(-1), Cosine(Product((Frac(5,12), Pi()))))).consim(safeMode)
            elif a==Frac(2,3):
                return Frac(-1,2)
            elif a==Frac(3,4):
                return Product((Frac(-1,2), Exponential(Frac(2), Frac(1,2))))
            elif a==Frac(5,6):
                return Product((Frac(-1,2), Exponential(Frac(3), Frac(1,2))))
            elif a==Frac(11,12):
                return Product((Frac(-1), Cosine(Product((Frac(1,12), Pi()))))).consim(safeMode)
            elif a==Frac(1):
                return Frac(-1)        

        if sa.expression_type == ExpressionType.ARCCOSINE:
            return sa.argument # cos(arccos(f(x))) = f(x)
        else:
            return Cosine(sa)         

    def pfsf(self, safeMode = False): #simplified form

        argPfsf = self.argument.pfsf(safeMode)

        if argPfsf.expression_type == ExpressionType.ARCCOSINE:
            return argPfsf.argument # cos(arccos(f(x))) = f(x)
        else:
            return Cosine(argPfsf) 

        # Otherwise, ignore for now as we are not doing identities