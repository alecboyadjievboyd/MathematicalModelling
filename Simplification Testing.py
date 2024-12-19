from Model.product import Product
from Model.sum import Sum
from Model.exponential import Exponential
from Model.logarithm import Logarithm
from Model.integer import Integer
from Model.exp import Exp
from Model.arctangent import Arctangent
from Model.tangent import Tangent
from Model.sine import Sine
from Model.arcsine import Arcsine
from Model.cosine import Cosine
from Model.arccosine import Arccosine
from Model.natural_logarithm import NaturalLogarithm
from Model.variable import Variable
from Model.general_multivar import GeneralMultivar
from Model.general_singlevar import GeneralSinglevar
from Model.expression import Expression
from Model.expression_type import ExpressionType

## CONSTANTS
print(" ")
print("-------------------------------------------- ")
print(" ")
print("TESTING CONSTANTS...")

current = Integer(2)
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

# works as expected

# VARIABLES
print(" ")
print("-------------------------------------------- ")
print(" ")
print("TESTING VARIABLES...")

current = Variable(2)
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

# EXPONENTIALS
print(" ")
print("-------------------------------------------- ")
print(" ")
print("TESTING EXPONENTIALS...")

print(" ")
print("Already Simplified Case:")
print(" ")

current = Exponential(Variable(1), Integer(2))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

print(" ")
print("Exponent = 1 Case:")
print(" ")

current = Exponential(Variable(1), Integer(1))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

print(" ")
print("Exponent = 0 Case:")
print(" ")

current = Exponential(Variable(1), Integer(0))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

print(" ")
print("Base is sum, Exponent = 2 Case:")
print(" ")

current = Exponential(Sum([Variable(1), Variable(2)]), Integer(2))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

print(" ")
print("Base is exponent case:")
print(" ")

current = Exponential(Exponential(Variable(1), Variable(2)), Integer(2))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf())) 

print(" ")
print("Logarithm case, same base:")
print(" ")

current = Exponential(Integer(2), Logarithm(Integer(2), Variable(1)))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

print(" ")
print("Logarithm case with expression, same base:")
print(" ")

current = Exponential(Variable(2), Logarithm(Variable(2), Variable(1)))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

print(" ")
print("Logarithm case, different bases:")
print(" ")

current = Exponential(Integer(2), Logarithm(Integer(3), Variable(1)))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

print(" ")
print("Logarithm case, different bases, more complex already the base:")
print(" ")

current = Exponential(Variable(1), Logarithm(Integer(3), Integer(2)))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

print(" ")
print("Basic Exponenital, only simplification can happen in the arg and base")
print(" ")

current = Exponential(Sum([Variable(1), Product([Integer(2), Variable(1)])]), Product([Sum([Variable(1), Integer(1)]), Variable(1)]))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))


# Arccos
print(" ")
print("-------------------------------------------- ")
print(" ")
print("TESTING ARCCOSINE...")

print(" ")
print("Basic Arccos, only simplification can happen in the arg")
print(" ")

current = Arccosine(Sum([Variable(1), Variable(1)]))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

print(" ")
print("Arccos with cos on inside (should not reduce)")
print(" ")

current = Arccosine(Cosine(Variable(1)))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

# ARCSIN    
print(" ")
print("-------------------------------------------- ")
print(" ")
print("TESTING ARCSINE...")

print(" ")
print("Basic Arcsin, only simplification can happen in the arg")
print(" ")

current = Arcsine(Sum([Variable(1), Variable(1)]))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

print(" ")
print("Arcsin with sin on inside (should not reduce)")
print(" ")

current = Arcsine(Sine(Variable(1)))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

# ARCTAN    
print(" ")
print("-------------------------------------------- ")
print(" ")
print("TESTING ARCTANGENT...")

print(" ")
print("Basic Arctan, only simplification can happen in the arg")
print(" ")

current = Arctangent(Sum([Variable(1), Variable(1)]))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

print(" ")
print("Arctan with tan on inside (should not reduce)")
print(" ")

current = Arctangent(Tangent(Variable(1)))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

# Sine    
print(" ")
print("-------------------------------------------- ")
print(" ")
print("TESTING SINE...")

print(" ")
print("Basic sine, only simplification can happen in the arg")
print(" ")

current = Sine(Sum([Variable(1), Variable(1)]))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

print(" ")
print("Sine with arcsine on inside (should reduce)")
print(" ")

current = Sine(Arcsine(Variable(1)))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

# COSINE    
print(" ")
print("-------------------------------------------- ")
print(" ")
print("TESTING COSINE...")

print(" ")
print("Basic cosine, only simplification can happen in the arg")
print(" ")

current = Cosine(Sum([Variable(1), Variable(1)]))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

print(" ")
print("cos with arcosine on inside (should reduce)")
print(" ")

current = Cosine(Arccosine(Variable(1)))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

# TAN    
print(" ")
print("-------------------------------------------- ")
print(" ")
print("TESTING TANGENT...")

print(" ")
print("Basic tan, only simplification can happen in the arg")
print(" ")

current = Tangent(Sum([Variable(1), Variable(1)]))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

print(" ")
print("tangent with arctan on inside (should reduce)")
print(" ")

current = Tangent(Arctangent(Variable(1)))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

# LOGARITHM    
print(" ")
print("-------------------------------------------- ")
print(" ")
print("TESTING LOGARITHM...")

print(" ")
print("Basic logarithm, only simplification can happen in the base and arg")
print(" ")

current = Logarithm(Sum([Variable(1), Variable(1)]),Sum([Variable(2), Variable(2)])) # NOTE this would normally not be possible bc base cannot be non-constant but I am using it as example that the simplification transfers down
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

print(" ")
print("logarithm with identical base and argument (should reduce)")
print(" ")

current = Logarithm(Integer(2), Integer(2)) # NOTE this would normally not be possible bc base cannot be non-constant but I am using it as example that the simplification transfers down
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

print(" ")
print("logarithm with exponential argumen with identical base(should reduce)")
print(" ")

current = Logarithm(Integer(2), Exponential(Integer(2), Variable(1))) # NOTE this would normally not be possible bc base cannot be non-constant but I am using it as example that the simplification transfers down
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

# SUM AND PRODUCT TESTING    
print(" ")
print("-------------------------------------------- ")
print(" ")
print("TESTING SUM AND PRODUCT IN ONE GIANT EXPRESSION...")


current = Sum([Logarithm(Integer(2), Exponential(Integer(3), Variable(1))), Product([Logarithm(Integer(2), Exponential(Integer(3), Variable(1))), Sum([Variable(1), Integer(1)])])]) # NOTE this would normally not be possible bc base cannot be non-constant but I am using it as example that the simplification transfers down
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

'''def rt(x,n=2):
    return Exponential(Integer(x), Exponential(Integer(n), Integer(-1)))

current = Product((Exponential(rt(2),rt(3)), Exponential(Exponential(rt(2),rt(3)),rt(5))))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

current = Sum([Integer(0)])
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

def rt(x,n=2):
    return Exponential(Integer(x), Exponential(Integer(n), Integer(-1)))

def x(n=1):
    return Variable(n)

def C(x):
    return Integer(x)

# rtx = Exponential(Exponential(x(), C(2)), C(-1))

print(
    Exponential(Exponential(Exponential(x(), C(2)), C(-1)), rt(3)).pfsf()
)'''

current = Product([Exponential(Variable(1), Integer(2)), Exponential(Variable(1), Integer(2))])
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

current = Exponential(Exponential(Variable(1), Integer(2)), Integer(2))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))






