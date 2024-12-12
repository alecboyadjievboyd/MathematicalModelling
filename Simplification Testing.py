from Model.product import Product
from Model.sum import Sum
from Model.exponential import Exponential
from Model.logarithm import Logarithm
from Model.constant import Constant
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

current = Constant(2)
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

current = Exponential(Variable(1), Constant(2))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

print(" ")
print("Exponent = 1 Case:")
print(" ")

current = Exponential(Variable(1), Constant(1))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

print(" ")
print("Exponent = 0 Case:")
print(" ")

current = Exponential(Variable(1), Constant(0))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))

print(" ")
print("Base is sum, Exponent = 2 Case:")
print(" ")

current = Exponential(Sum([Variable(1), Variable(2)]), Constant(2))
print("Initial: " + str(current))
print("Simplified: " + str(current.pfsf()))


