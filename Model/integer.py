from Model.expression import Expression
from Model.expression_type import ExpressionType
from enum import Enum


# Constant integer expression. Terminal expression.
class Integer(Expression):

    def __init__(self, value):
        super().__init__(ExpressionType.INTEGER)
        self.value = value
        self.primaryOrder = 1 # Constant, lowest order
        self.secondaryOrder = None # No secondary order

    def __str__(self):
        if self.value >= 0:
            return str(self.value)
        else:
            return f'({str(self.value)})'

    def __eq__(self, other):
        if self.expression_type != other.expression_type:
            return False
        if str(self) == str(other):
            return True
        else:
            return False

    def __gt__(self, other):
        if other.expression_type == ExpressionType.FRACTION:
            from Model.fraction import Frac
            return Frac(self)>other


        if other.primaryOrder == self.primaryOrder: # Both simple constants
            return self.value > other.value # Compare based on value (NOTE: I AM NOT SURE IF THIS WILL WORK WIHT PI AND E)
        else:
            return False # Other is a more complex form (NOT NECESSARILY NUMERICALLY LARGER)
                             # Eventually we may want to replace this with a comparison based on evaluation
                             # Right now x^(2+1) will be seen as "greater in priority" to x^100, for example

            

    def isConstant(self):
        return True

    def derivative(self, differential):
        return Integer(0)

    def pfsf(self, safeMode = False):
        return Integer(self.value)

    def genarg(self):#needed for constant simplification (consim)
        return (self.value,)
        
    def consim(self, safeMode = False):
        from Model.fraction import Frac
        return Frac(self)
    
    def primefac(self, AsExpr = True): 
        #if AsExpr == True, returns an expression. else, returns dic {prime : exponent}, e.g. 20 -> {2:2, 5:1}
        from Model.product import Product
        from Model.exponential import Exponential
        n = self.value 
        if n<1:
            raise "cannot primefactorize integer < 1"
        dic = {}
        d = 2
        while d*d <= n:
            while n%d == 0:
                dic.setdefault(d,0)
                dic[d] += 1
                n = n//d
            d += 1
        if n>1:
            dic.setdefault(n,0)
            dic[n] += 1
        
        if AsExpr:
            if len(dic) == 0:
                return Integer(1)
            elif len(dic) == 1:
                for d in dic:
                    return Exponential(Integer(d), Integer(dic[d]))
            else:
                factors = ()
                for d in dic:
                    factors += (Exponential(Integer(d), Integer(dic[d])),)
                return Product(factors)
        else:
            return dic



    def root(self, n, AsExpr = True):
        from Model.fraction import Frac
        from Model.product import Product
        from Model.exponential import Exponential

        if type(n)!= int:
            if n.expression_type == ExpressionType.FRACTION:
                if n.den.value == 1:
                    n = n.num.value
                else:
                    raise "n should be an integer"
            elif n.expression_type == ExpressionType.INTEGER:
                n = n.value
            else:
                raise "n should be an integer"
        #now type(n) == int 
        a = self.value

        if a == 0:
            return Integer(0)
        elif a < 0:
            if n%2 == 0:
                raise "cannot take even root of negative value"
            else:
                sgn = -1
                a = -a
        else:
            sgn = 1
                

        primedic = Integer(a).primefac(False)

        powerdic = {} # = {prime: Frac(power, n)} 
        for prime in primedic:
            f = Frac(primedic[prime], n).simplify()
            powerdic[prime] = f

        # if AsExpr:
        #     if len(powerdic) == 0:
        #         return Frac(1)
        #     elif len(powerdic) == 1:
        #         for prime in powerdic:
        #             if powerdic[prime].quo() == Integer(0) and powerdic[prime].rem() == Integer(0): #I dont think this can actually happen.
        #                 return Frac(1)
        #             elif powerdic[prime].quo() == Integer(0) and powerdic[prime].rem() != Integer(0):
        #                 return Exponential(Frac(prime), Frac(f.rem(), f.den))
        #             elif powerdic[prime].quo() != Integer(0) and powerdic[prime].rem() == Integer(0):
        #                 return Frac(prime)**powerdic[prime].quo()
        #             else:
        #                 return Product((
        #                     Frac(prime)**powerdic[prime].quo(),
        #                     Exponential(Frac(prime), Frac(f.rem(), f.den))
        #                 ))
        #     else:
        #         factors = ()
        #         for prime in powerdic:
        #             if powerdic[prime].quo() == Integer(0) and powerdic[prime].rem() == Integer(0): #I dont think this can actually happen.
        #                 factors += ( Frac(1) , )
        #             elif powerdic[prime].quo() == Integer(0) and powerdic[prime].rem() != Integer(0):
        #                 factors += ( Exponential(Frac(prime), Frac(f.rem(), f.den)) , )
        #             elif powerdic[prime].quo() != Integer(0) and powerdic[prime].rem() == Integer(0):
        #                 factors += ( Frac(prime)**powerdic[prime].quo() , )
        #             else:
        #                 factors += ( Product((
        #                     Frac(prime)**powerdic[prime].quo(),
        #                     Exponential(Frac(prime), Frac(f.rem(), f.den))
        #                 )) , )
        #         return Product(factors)                
        # #this now does 10^(1/2) -> 2^(1/2) * 5^(1/2) instead of 10^(1/2) (like powers should have their bases multiplied)

        takeoutdic = {} #{prime: (a, b, m)} such that n-th root of prime^primedic[prime] = a* b^(1/m)
        # takes out the a^m from underneath the m-th root
        for prime in powerdic:
            a = prime ** powerdic[prime].quo().value
            b = prime ** powerdic[prime].rem().value
            m = powerdic[prime].den.value
            takeoutdic[prime] = (a,b,m)

        coefficient = 1
        mdic = {} # {m: B} such that the a^(1/n) = coefficient * (B_i ^ m_i)_i with m_i unique
        for prime in takeoutdic:
            mdic.setdefault(takeoutdic[prime][2], 1)
            mdic[takeoutdic[prime][2]] *= takeoutdic[prime][1]
            coefficient *= takeoutdic[prime][0]

        d = {} # same as mdic, but gets rid of mdic[m]=1
        for m in mdic:
            if mdic[m] != 1:
                d[m] = mdic[m]

        coefficient = sgn * coefficient

        if AsExpr:
            if len(d) == 0:
                return Integer(coefficient)
            elif len(d) == 1:
                if coefficient == 1:
                    for m in d:
                        return Exponential(Integer(d[m]), Frac(1,m))
                else:
                    for m in d:
                        return Product((Integer(coefficient), Exponential(Integer(d[m]), Frac(1,m))))
            else:
                factors = ()
                if coefficient != 1:
                    factors += (Integer(coefficient),)
                for m in d:
                    factors += (Exponential(Integer(d[m]), Frac(1,m)), )
                return Product(factors)

        else:
            return (coefficient, d)





        

