from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.integer import Integer
from Model.sum import Sum
from Model.product import Product
from Model.exponential import Exponential

class Frac(Expression):
    def __init__(self, num: Integer, den: Integer = 1): #num=numerator, den=denominator
        super().__init__(ExpressionType.FRACTION)
        self.primaryOrder = 1 # Constant, lowest order #I(Tim) just copy pasted these from constant
        self.secondaryOrder = None # No secondary order

        if type(num) == int:
            num = Integer(num)
        if type(den) == int:
            den = Integer(den)

        if den.value == 0:
            raise Exception("division by zero")
        if num.value == 0:
            den.value = 1
        if den.value < 0:
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

    def srem(self): #srem = signed remainder
        #e.g. (-3)/2 = -1 + -1/2 instead of -2 + 1/2
        if self.num.value>=0:
            srem = self.num.value % self.den.value
        else: #self.num.value<0:
            srem = - ( (-self.num.value) % self.den.value)
        return Integer(srem)
            
    def rem(self): #rem = remainder
        return Integer(self.num.value % self.den.value)
    
    def squo(self): #squo = signed quotient
        if self.num.value>=0:
            squo = self.num.value // self.den.value
        else: # self.num.value<0:
            squo = - ( (-self.num.value) // self.den.value)
        return Integer(squo)
    
    def quo(self): #quo = quotient
        return Integer(self.num.value // self.den.value)

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
        if exponent.expression_type != ExpressionType.INTEGER:
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
        else: #exponent<0:
            return Frac( self.den.value**-exponent, self.num.value**-exponent ).simplify()

    
    def __eq__(self, other):
        #equality in terms of representation(?)
        if other.expression_type == ExpressionType.INTEGER:
            other = Frac(other)
        if other.expression_type != ExpressionType.FRACTION:
            return False

        #equality in terms of mathematical equality(?)
        selfsimp = self.simplify()#maybe it is more efficient to check whether the numerator of the difference is zero
        # if other.expression_type == ExpressionType.INTEGER:
        #     othersimp = Frac(other)
        # else:
        othersimp = other.simplify()
        
        if selfsimp.num == othersimp.num and selfsimp.den == othersimp.den:
            return True
        else:
            return False
    
    def __gt__(self,other):
        if other.expression_type == ExpressionType.INTEGER: #not sure if this is necessairy
            other = Frac(other)

        if other.expression_type != ExpressionType.FRACTION: #now we use > in the sense of complexity
            return False

        dif = self + Frac(-1)*other #now in the sense of math
        if dif.num.value > 0:
            return True
        else:
            return False
        
    def __mod__(self, other): #necessary for sin, cos, tan .consim
        if self > other or self == other:
            return (self + Frac(-other.num.value, other.den.value)) % other
        elif self < Frac(0):
            return (self + other) % other
        else:
            return self

    def isConstant(self):
        return True

    def simplify(self): #probably more efficent ways exist
        num=self.num.value
        den=self.den.value
        if num == 0:
            return Frac(0)
        
        if num<0:
            sgn = -1
            num = - num
        else:
            sgn = 1

        small=min(num, den)
        i=2
        while i <= small:#could restict this to only primes.
            while num%i==0 and den%i==0:
                num = num//i
                den = den//i
                small = min(num, den)
            i+=1
        return Frac(sgn*num, den)
    
    def derivative(self, differential, safeMode = False):
        return Integer(0)

    def genarg(self):#needed for constant simplification (consim)
        return (self.num, self.den)
    
    def consim(self, safemode = False):
        return self.simplify()
    
    def pfsf(self, safeMode=False):
        return Frac(self.num, self.den).simplify()
    
    def primefac(self, AsExpr = True):
        npf = self.num.primefac(False) #numerator prime factorisation
        dpf = self.den.primefac(False) #denominator prime factorisation

        UnionOfPrimes = ()
        for prime in npf:
            UnionOfPrimes += (prime,)
        for prime in dpf:
            if prime not in UnionOfPrimes:
                UnionOfPrimes += (prime,)
        UnionOfPrimes = sorted(UnionOfPrimes)

        fpf = {} #factor prime factorisation
        for prime in UnionOfPrimes:
            a = npf.setdefault(prime, 0)
            b = dpf.setdefault(prime, 0)
            c = a-b
            if c != 0:
                fpf[prime] = a-b
        
        if AsExpr:
            if len(fpf)==0:
                return Integer(1)
            elif len(fpf)==1:
                for prime in fpf:
                    return Exponential(Integer(prime), Integer(fpf[prime]))
            else:
                factors = ()
                for prime in fpf:
                    factors += (Exponential(Integer(prime), Integer(fpf[prime])), )
                return Product(factors)
        else:
            return fpf
    


    def root(self, n, AsExpr=True): #self^(1/n)
        if type(n) != int:
            if n.expression_type == ExpressionType.FRACTION:
                if n.den.value != 1:
                    raise "n needs to be an integer"
                n = n.num.value
            elif n.expression_type == ExpressionType.INTEGER:
                n = n.value
            else:
                raise "n needs to be an integer"

        S = self

        if S == Frac(0):
            return Frac(0)
        elif S < Frac(0):
            if n%2 == 0:
                raise "Cannot take even root of negative value"
            else:
                sgn = -1
                S = Frac(-1)*S
        else:
            sgn = 1

        primedic = S.primefac(False)

        powerdic = {}
        for prime in primedic:
            f = Frac(primedic[prime], n).simplify()
            powerdic[prime] = f

        takeoutdic = {}
        for prime in powerdic:
            a = Frac(prime) ** powerdic[prime].quo()
            b = Frac(prime) ** powerdic[prime].rem()
            m = powerdic[prime].den.value
            takeoutdic[prime] = (a, b, m)

        coefficient = Frac(1)
        mdic = {}
        for prime in takeoutdic: #this defines the ordering: m associated to the first prime comes first, then m associated to the second prime with different m, etc. That is quite silly, lets change that
            mdic.setdefault(takeoutdic[prime][2], Frac(1))
            mdic[takeoutdic[prime][2]] *= takeoutdic[prime][1]
            coefficient *= takeoutdic[prime][0] 

        nooned = {}
        for m in mdic:
            if mdic[m] != Frac(1):
                nooned[m] = mdic[m]

        #sorted them in order of increasing m, so decreasing power
        d = {}
        for m in sorted(nooned):
            d[m] = nooned[m]
          
        coefficient = Frac(sgn)*coefficient
        if AsExpr:
            if len(d) == 0:
                return coefficient
            elif len(d) == 1:
                if coefficient == Frac(1):
                    for m in d:
                        return Exponential(d[m], Frac(1,m))
                else:
                    for m in d:
                        return Product((coefficient, Exponential(d[m], Frac(1,m))))
            else:
                factors = ()
                if coefficient != Frac(1):
                    factors += (coefficient, )
                for m in d:
                    factors += ( Exponential(d[m], Frac(1,m)) ,)
                return Product(factors)
        return (coefficient, d)

    def fracpow(self, power): #self^power
        if power.expression_type == ExpressionType.INTEGER:
            power = Frac(power)
        elif power.expression_type != ExpressionType.FRACTION:
            raise "power needs to be a fraction"
        power = power.simplify()   
        # return (self**power.num).root(power.den) #it would probably be more efficient to first take the root and then the power, but that takes more time to code

        #to increase efficiency as compared to the above:
        if power.squo() == Integer(0):
            return (self**power.num).root(power.den)
        else:
            return Product((
                self**(power.quo()),
                (self**power.rem()).root(power.den)
            )).consim(True) #consim to do the multiplication of self**(power.squo()) with the coefficient of the root