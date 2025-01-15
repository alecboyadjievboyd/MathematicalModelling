import random
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

    if (depth == 0):
        num = random.randint(0, 3)
        if num == 0:
            return Variable(1)
        if num == 1:
            return Integer(random.randint(0,9))
        if num == 2:
            return Euler()
        if num == 3:
            return Pi()

    operation = random.choice([
    "Product",
    "Sum",
    "Exponential",
    "Logarithm",
    "Exp",
    "Arctangent",
    "Tangent",
    "Sine",
    "Arcsine",
    "Cosine",
    "Arccosine",
    "Variable",
    "Integer"
    ])

    depth2 = random.randint(0, n)

    if operation == "Product":
        obj = Product([...])  # Replace [...] with appropriate arguments
    elif operation == "Sum":
        obj = Sum([...])  # Replace [...] with appropriate arguments
    elif operation == "Exponential":
        obj = Exponential(base, exponent)  # Replace base, exponent with actual values
    elif operation == "Logarithm":
        obj = Logarithm(base, argument)  # Replace base, argument with actual values
    elif operation == "Exp":
        obj = Exp(argument)  # Replace argument with actual value
    elif operation == "Arctangent":
        obj = Arctangent(argument)  # Replace argument with actual value
    elif operation == "Tangent":
        obj = Tangent(argument)  # Replace argument with actual value
    elif operation == "Sine":
        obj = Sine(argument)  # Replace argument with actual value
    elif operation == "Arcsine":
        obj = Arcsine(argument)  # Replace argument with actual value
    elif operation == "Cosine":
        obj = Cosine(argument)  # Replace argument with actual value
    elif operation == "Arccosine":
        obj = Arccosine(argument)  # Replace argument with actual value
    elif operation == "Variable":
        obj = Variable(name)  # Replace name with the variable's name
    elif operation == "Integer":
        obj = Integer(value)  # Replace value with the integer's value