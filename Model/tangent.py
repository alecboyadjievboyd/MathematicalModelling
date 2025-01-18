from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.fraction import Frac
from Model.pi import Pi
from Model.product import Product
from Model.cosine import Cosine
from Model.exponential import Exponential
from Model.integer import Integer
from Model.sum import Sum


# Tangent of an expression
class Tangent(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.TANGENT)
        self.argument = argument
        self.isconstant = None
        self.primaryOrder = 5 # Single Function
        self.secondaryOrder = 4 # Tan
        
    def __str__(self):
        return f'tan({self.argument})'
    
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
            if (self.secondaryOrder == other.secondaryOrder): # Both tan
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
        return Product({Exponential(Cosine(self.argument), Integer(-2)), self.argument.derivative(differential)}).pfsf(safeMode)

    def genarg(self):#needed for constant simplification (consim)
        return (self.argument,)
    
    def consim(self, safeMode = False): #simplified form

        sa = self.argument.consim(safeMode) #simplify the arg first


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
            a = Frac(-1)*( Frac(-1)*(a + Frac(1)) % Frac(2) ) + Frac(1) #this is a but with 2 added/subtracted to it until a is in (-1,1].
            
            if a<Frac(0):
                a = a + Frac(1)
            
            if a>Frac(1,2) or a==Frac(1,2):
                return Product((
                    Frac(-1),
                    Tangent(Product((
                        Frac(1)+(Frac(-1)*a),
                        Pi()
                    )))
                    )).consim()

            if a==Frac(0):
                return Frac(0)
            elif a==Frac(1,12):
                return Sum((
                    Product((
                        Frac(-1), 
                        Frac(3).root(2)
                    )),
                    Frac(2)
                ))
            elif a==Frac(1,6):
                return Product((Frac(1,3), Exponential(Frac(3), Frac(1,2))))
            elif a==Frac(1,4):
                return Frac(1)
            elif a==Frac(1,3):
                return Frac(3).root(2)
            elif a==Frac(5,12):
                return Sum((
                    Frac(3).root(2),
                    Frac(2)
                ))
            elif a==Frac(1,2):
                raise "MATH ERROR: tan(pi/2) is undefined (1/0)"
            elif a==Frac(7,12):
                return Product((Frac(-1), Tangent(Product((Frac(5,12), Pi()))))).consim(safeMode)
            elif a==Frac(2,3):
                return Product((Frac(-1), Frac(3).root(2)))
            elif a==Frac(3,4):
                return Frac(-1)
            elif a==Frac(5,6):
                return Product((Frac(-1,3), Exponential(Frac(3), Frac(1,2))))
            elif a==Frac(11,12):
                return Product((Frac(-1), Tangent(Product((Frac(1,12), Pi()))))).consim(safeMode)
            elif a==Frac(1):
                return Frac(0)        

        if sa.expression_type == ExpressionType.ARCTANGENT:
            return sa.argument # tan(arctan(f(x))) = f(x)
        else:
            return Tangent(sa) 
    
    def pfsf(self, safeMode = False): #simplified form

        argPfsf = self.argument.pfsf(safeMode) #simplify the arg first

        if argPfsf.expression_type == ExpressionType.ARCTANGENT:
            return argPfsf.argument # tan(arctan(f(x))) = f(x)
        else:
            return Tangent(argPfsf) 

        # Otherwise, ignore for now as we are not doing identities
