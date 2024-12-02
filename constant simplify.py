from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.constant import Constant
from Model.sum import Sum
from Model.product import Product
from Model.exponential import Exponential

#There are two cool things in this file: the class Frac and the function constant_simplify, the latter referencing the former.

class Frac(Expression):
    def __init__(self, num:Constant, den:Constant=1): #num=numerator, den=denominator
        super().__init__(ExpressionType.FRACTION)
        if type(num)==int:
            num=Constant(num)
        if type(den)==int:
            den=Constant(den)

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
    


# def constant_simplify(expression: Expression):
#     if expression.expression_type == ExpressionType.FRACTION:
#         return expression.simplify()
#     elif expression.expression_type == ExpressionType.SUM:
#         new_terms = ()
#         for term in expression.terms:
#             old = term
#             new = constant_simplify(term)
#             if old==new:
#                 new_terms += (new,)
#             else:
#                 new_term = constant_simplify(new)
#                 new_terms += (new_term,)
#         s = Frac(0) #s for sum, but we already defined both sum and Sum
#         for term in new_terms:
#             s += term
#         return s
#     elif expression.expression_type == ExpressionType.PRODUCT: #compare to previous elif, == ExpressionType.SUM
#         new_factors = ()
#         for factor in expression.factors:
#             old = factor
#             new = constant_simplify(factor)
#             if old==new:
#                 new_factors += (new,)
#             else:
#                 new_factor = constant_simplify(new)
#                 new_factors += (new_factor,)
#         p = Frac(1) #p for product, but we already defined both product and Product
#         for factor in new_factors:
#             p *= factor
#         return p
#     elif expression.expression_type == ExpressionType.EXPONENTIAL:
#         base = constant_simplify(expression.base)
#         exponent = constant_simplify(expression.exponent)
#         return base**exponent
        
#     else:
#         raise Exception("You are asking me to simplify something really scary")

def constant_simplify(expression: Expression):
    if expression.expression_type == ExpressionType.CONSTANT:
        return Frac(expression)
    elif expression.expression_type == ExpressionType.FRACTION:#all below should eventually end up calling this
        return expression.simplify()
    elif expression.expression_type == ExpressionType.SUM:
        new_terms = ()
        for term in expression.terms:
            new_terms+= (constant_simplify(term),) #These should all be Frac
        s = Frac(0) #s for sum, but we already defined both sum and Sum
        for term in new_terms:
            s += term
        return s.simplify()
    elif expression.expression_type == ExpressionType.PRODUCT: #compare to previous elif, == ExpressionType.SUM
        new_factors = ()
        for factor in expression.factors:
            new_factors += (constant_simplify(factor),) #These should all be Frac
        p = Frac(1) #p for product, but we already defined both product and Product
        for factor in new_factors:
            p *= factor
        return p.simplify()
    elif expression.expression_type == ExpressionType.EXPONENTIAL:
        base = constant_simplify(expression.base) #This should be Frac
        exponent = constant_simplify(expression.exponent) #This should be Frac
        returnable = base**exponent
        return returnable.simplify()
        
    else:
        raise Exception("You are asking me to simplify something really scary")


you_like_examples = False
if you_like_examples: #that aren't illustrative due to lack of formatting 
    y = Frac(1040,2100)
    print(y)
    print(Frac(1023,6).simplify())

    print(Frac(2,3)+Frac(1,4))
    print(Frac(2,3)*Frac(1,4))
    print(  constant_simplify(Sum((Frac(1,4), Frac(3,2), Frac(5),Frac(1,4))))  )
    print(  constant_simplify(Product((Frac(1,4), Frac(3,2), Frac(5),Frac(1,4))))  )
    print(  constant_simplify(
        Product((
            Frac(1,4), Frac(3,2), Sum((Frac(5),Frac(1,4)))
            ))
        )  )
    print(  constant_simplify(
        Sum((
            Frac(1,4), Frac(3,2), Product((Frac(5),Frac(1,4)))
            ))
        )  )
    print(Frac(5) ** Constant(-2))
    print(Frac(5)**Frac(-2))
    print(Frac(5) ** Constant(0))
    print(Frac(5)**Frac(0))
    print(Frac(5) ** Constant(3))
    print(Frac(5)**Frac(3))
    print(Frac(3,-2) ** Constant(-2))
    print(Frac(3,-2) ** Constant(-3))

    print(  (Frac(3,5)+Frac(4,6))*Frac(5,2)**Frac(3)  )

    print(  constant_simplify(Sum((Frac(1,4), Frac(3,2), Frac(5),Frac(1,4))))  )
    print(  constant_simplify(Exponential(Sum((Frac(1,4), Frac(3,2), Frac(5),Frac(1,4))),Frac(3)))  )

    print(constant_simplify(Exponential(Constant(5), Constant(-1))))
