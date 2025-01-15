import random
import math

from Model.product import Product
from Model.sum import Sum
from Model.exponential import Exponential
from Model.logarithm import Logarithm
from Model.exp import Exp
from Model.arctangent import Arctangent
from Model.tangent import Tangent
from Model.sine import Sine
from Model.arcsine import Arcsine
from Model.cosine import Cosine
from Model.arccosine import Arccosine
from Model.variable import Variable
from Model.euler import Euler
from Model.pi import Pi
from Model.integer import Integer
from Model.expression_type import ExpressionType



def generate(depth, maxElements):

    if depth == 0:
        num = random.randint(0, 11)
        if num < 5:
            return Variable(1)
        if num > 7:
            return Integer(random.randint(-9,9))
        if num == 6:
            return Euler()
        if num == 7:
            return Pi()

    tryy = random.randint(0, 10)
    if tryy < 8:
        operation = random.choice([
            "Product",
            "Sum",
            "Exponential",
            "Logarithm"
            ])
    else:
        operation = random.choice([ 
            "Arctangent",
            "Tangent",
            "Sine",
            "Arcsine",
            "Cosine",
            "Arccosine"
        ])

    elementNum = random.randint(2, maxElements)

    if depth == 0:
        depth = 1

    if operation == "Product":
        factors = []
        i = 1
        while i <= elementNum:
            factors.append(generate(random.randint(0, depth - 1), maxElements)) 
            i = i+1
        
        return Product(factors)  # Replace [...] with appropriate arguments

    elif operation == "Sum":
        terms = []
        i = 1
        while i <= elementNum:
            terms.append(generate(random.randint(0, depth - 1), maxElements))
            i = i+1

        return Sum(terms)  # Replace [...] with appropriate arguments

    elif operation == "Exponential":
        return Exponential(generate(random.randint(0, depth - 1), maxElements), generate(random.randint(0, depth - 1), maxElements))  # Replace base, exponent with actual values

    elif operation == "Logarithm":
        return Logarithm(generate(random.randint(0, depth - 1), maxElements), generate(random.randint(0, depth - 1), maxElements))  # Replace base, argument with actual values

    elif operation == "Arctangent":
        return Arctangent(generate(random.randint(0, depth - 1), maxElements))  # Replace argument with actual value

    elif operation == "Tangent":
        return Tangent(generate(random.randint(0, depth - 1), maxElements))  # Replace argument with actual value

    elif operation == "Sine":
        return Sine(generate(random.randint(0, depth - 1), maxElements))  # Replace argument with actual value

    elif operation == "Arcsine":
        return Arcsine(generate(random.randint(0, depth - 1), maxElements))  # Replace argument with actual value

    elif operation == "Cosine":
        return Cosine(generate(random.randint(0, depth - 1), maxElements))  # Replace argument with actual value

    elif operation == "Arccosine":
        return Arccosine(generate(random.randint(0, depth - 1), maxElements))  # Replace argument with actual value

def evaluate(f, x):

    if f.expression_type == ExpressionType.INTEGER:
        return f.value
    
    if f.expression_type == ExpressionType.EULER:
        return 2.71828

    if f.expression_type == ExpressionType.PI:
        return 3.14159

    if f.expression_type == ExpressionType.VARIABLE:
        return x

    if f.expression_type == ExpressionType.FRACTION: # FRACTIONS ONLY CONTAIN INTEGERS
        from Model.fraction import Frac

        if f.num == 'undefined' or f.den == 'undefined' or f.den == Integer(0):
            return 'undefined'

        try:
            return (f.num / f.den)
        except Exception:
            return 'undefined'

    if f.expression_type == ExpressionType.PRODUCT:
        value = 1
        for factor in f.factors:
            ev = evaluate(factor, x)
            if ev == 'undefined':
                return 'undefined'
            value = value * ev

        try:
            return value
        except Exception:
            return 'undefined'

    if f.expression_type == ExpressionType.SUM:
        value = 0
        for term in f.terms:
            ev = evaluate(term, x)
            if ev == 'undefined':
                return 'undefined'
            value = value + ev
        
        try:
            return value
        except Exception:
            return 'undefined'

    if f.expression_type == ExpressionType.EXPONENTIAL:
        baseEv = evaluate(f.base, x)
        argEv = evaluate(f.argument, x)

        try:
            return math.pow(baseEv, argEv)
        except Exception:
            return 'undefined'

    if f.expression_type == ExpressionType.LOGARITHM:
        baseEv = evaluate(f.base, x)
        argEv = evaluate(f.argument, x)

        try:
            return math.log(argEv, baseEv)
        except Exception:
            return 'undefined'

    if f.expression_type == ExpressionType.ARCTANGENT:
        
        argEv = evaluate(f.argument, x)

        try:
            return math.atan(argEv)
        except Exception:
            return 'undefined'

    if f.expression_type == ExpressionType.TANGENT:
        
        argEv = evaluate(f.argument, x)

        try:
            return math.tan(argEv)
        except Exception:
            return 'undefined'

    if f.expression_type == ExpressionType.SINE:
        
        argEv = evaluate(f.argument, x)

        try:
            return math.sin(argEv)
        except Exception:
            return 'undefined'

    if f.expression_type == ExpressionType.ARCSINE:
        
        argEv = evaluate(f.argument, x)

        try:
            return math.asin(argEv)
        except Exception:
            return 'undefined'

    if f.expression_type == ExpressionType.COSINE:
        
        argEv = evaluate(f.argument, x)

        try:
            return math.cos(argEv)
        except Exception:
            return 'undefined'

    if f.expression_type == ExpressionType.ARCCOSINE:
        
        argEv = evaluate(f.argument, x)

        try:
            return math.acos(argEv)
        except Exception:
            return 'undefined'

    else: 
        print("WHY THE FUCK")
    








count = 0
while True:
    obj = generate(3,3)
    count = count + 1
    
    try:
        print("NOW TESTING: " + str(obj))
        print(evaluate(obj, 1))
        '''print("Simplified safe mode: " + str(obj.pfsf(True)))
        print("Simplified not safe mode: " + str(obj.pfsf()))'''
    except RecursionError:
        print("Recursion Error, Skip")
    except MathError:
        print("Math Error, This Expression is Not Valid")
    print(" ")
    print(count)
    print(" ")

(((3 + x1 + x1)^log_(arctan(x1))(x1))^(-3))


