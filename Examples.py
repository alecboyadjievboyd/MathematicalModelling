from Model.constant import Constant
from Model.variable import Variable
from Model.sum import Sum
from Model.product import Product
from Model.exponential import Exponential
from Model.general_multivar import GeneralMultivar
from Model.general_singlevar import GeneralSinglevar
from Model.natural_logarithm import NaturalLogarithm
from Model.logarithm import Logarithm
from Model.exp import Exp


def D(function, differential = Variable(1)):
    return function.derivative(differential)


print(Exp(GeneralMultivar("f")).derivative(Variable(1)))

print('Constants:')
# 8
expr1 = Constant(8)
# e
expr2 = Constant('e')
# pi
expr3 = Constant('pi')
print(expr1, expr2, expr3)

# x
expr2 = Variable(1)
print(expr2)

# 2x + 4
expr3 = Sum([Product([Constant(2), Variable(1)]), Constant(4)])
print(expr3)

# 3x * 2x
expr4 = Product([Product([Constant(3), Variable(1)]), Product([Constant(2), Variable(1)])])
print(expr4)

# x^2
expr5 = Exponential(Variable(1), Constant(2))
print(expr5)

# 0x^4
expr6 = Product([Constant(0), Exponential(Variable(1), Constant(4))])
print(expr6)

# (8 + 7) * 3
expr7 = Product([Sum([Constant(8), Constant(7)]), Constant(3)])
print(expr7)

# x * ( x * (x * (x+1))) 
expr8 = Product([ Variable(1), Product([ Variable(1), Product([ Variable(1), Sum([ Variable(1), Variable(1) ]) ]) ]) ])
print(expr8)

# dx/dy
print( Variable(1).derivative(Variable(2)))

# dx/dx
print( Variable(1).derivative(Variable(1)))

# derivative of constant
print(Constant(23).derivative(Variable(1)))

# general multivariable functions
genf = GeneralMultivar('f')
geng = GeneralMultivar('g')
genh = GeneralMultivar('h')
print(genf)
print(Exponential(genf, Sum((geng, genh))))
print(genf.derivative(Variable(1)))
print(genf.derivative(Variable(1)).derivative(Variable(2)))

# the function D
print(D(genf, Variable(1)))
print(D(D(genf, Variable(1)), Variable(2)))
print(D(genf))


# Derivative of sum
print(D(Sum((genf, geng, genh))))

# Derivative of Product
print(D(Product((genf, geng, genh))))

# Derivative of Exponential
print(D(Exponential(genf, genh)))
print(D(Exponential(Variable(1), Constant(-1))))
print(D(Exponential(Variable(1),Variable(1))))

# Problem with derivative of exponential
print(D(Exponential(Constant(0), Variable(1))))

# ln
print( NaturalLogarithm(Variable(1)) )
print( D(NaturalLogarithm(genf)))
print( D(NaturalLogarithm(Variable(1))))

print('Logarithm:')
# log_8((x+1)^2)
expr1 = Logarithm(Constant(8), Exponential(Sum([Variable(1), Constant(1)]), Constant(2)))
# log_e(pi)
expr2 = Logarithm(Constant('e'), Constant('pi'))
print(expr1, expr2)

# general single variable function
print(GeneralSinglevar('cot', Variable(1)))
print(D(GeneralSinglevar('cot', genf)))