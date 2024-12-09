from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.constant import Constant
from Model.sum import Sum
from Model.product import Product
from Model.exponential import Exponential

class Frac(Expression):
    def __init__(self, num: Constant, den: Constant = 1): #num=numerator, den=denominator
        super().__init__(ExpressionType.FRACTION)
        if type(num) == int:
            num = Constant(num)
        if type(den) == int:
            den = Constant(den)

        if den.value == 0:
            raise Exception("division by zero")
        elif den.value < 0:
            den.value = -den.value
            num.value = -num.value
        
        self.num = num
        self.den = den

        # (Doubly commented out means that the comment is commented out, i.e. the comment is irrelevant)
        # #I want them to be initialy simplified (otherwise exponentiation of fractions in constant_simplify needs to have .simplify after the thing it returns)
        # #The method of simplification however is described below, so requires an initialised instance of Frac. 
        # #To circumnavigate this we initialise it unsimplified, simplify that and then use that for our initialisation.
        # #Perhaps it is possible to move the method simplify to the initialisation, as (maybe, we would have to check that) we now have to call it anytime we create a new instance of Frac.
        # #Maybe we should think about whether we want to simplify every time or just a few times or only at the end.
        # if simp: 
        #     x = Frac(num, den, False).simplify()
        #     self.num = x.num
        #     self.den = x.den
        # else: 
        #     self.num=num
        #     self.den=den



    def __str__(self):
        if self.den.value==1:
            return f"{self.num}"
        else:
            return f"{self.num}/{self.den}"#does put_brackets like this? a^(b/c) would become what?
    
    def __add__(self, other):
        new_frac = Frac(self.num.value * other.den.value + self.den.value * other.num.value, self.den.value * other.den.value)
        return new_frac.simplify()
    
    def __mul__(self, other):
        new_frac = Frac(self.num.value * other.num.value, self.den.value * other.den.value)
        return new_frac.simplify()
    
    def __pow__(self, exponent):
        if exponent.expression_type != ExpressionType.CONSTANT:
            if exponent.expression_type != ExpressionType.FRACTION:
                raise Exception("Exponent is not an integer")
            elif exponent.den.value != 1:
                raise Exception("Exponent is not an integer")
        else:
            exponent = Frac(exponent) #if exponent is Constant, now it is Frac
        exponent = exponent.num.value #before exponent was Frac, now it is int

        if exponent==0:
            return Frac(1)
        elif exponent>0:
            return Frac( self.num.value**exponent, self.den.value**exponent ).simplify()
        else: #exponent.num.value<0:
            return Frac( self.den.value**-exponent, self.num.value**-exponent ).simplify()

    
    def __eq__(self, other):
        selfsimp = self.simplify()#maybe it is more efficient to check whether the numerator of the difference is zero
        othersimp = other.simplify()
        if selfsimp.num == othersimp().num and selfsimp().den == othersimp().den:
            return True
        else:
            return False

    def simplify(self): #probably more efficent ways exist
        num=self.num.value
        den=self.den.value
        small=min(num, den)
        i=2
        while i <= small:#could restict this to only primes.
            while num%i==0 and den%i==0:
                num = num//i
                den = den//i
                small = min(num, den)
            i+=1
        return Frac(num, den)
    
    def derivative(self, differential):
        return Constant(0)

    def genarg(self):#needed for constant simplification (consim)
        return (self.num, self.den)
    
    def consim(self):
        return self.simplify()