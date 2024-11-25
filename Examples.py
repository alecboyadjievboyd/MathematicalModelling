# import sys
# import os

# project_root = os.path.dirname(os.path.abspath(__file__))
# model_folder_path = os.path.join(project_root, "Model")
# sys.path.insert(0, model_folder_path)

# for path in sys.path:
#     print(path)


from Model import Constant
from Model import Variable
from Model import Sum
from Model import Product
from Model import Exponential
from Model import GeneralMultivar
from Model import GeneralSinglevar
from Model import NaturalLogarithm

def D(function, differential = Variable(1)):
    return function.derivative(differential)


# 8
expr1 = Constant(8)
print(expr1)

# x
expr2 = Variable(1)
print(expr2)

# 2x + 4
expr3 = Sum([ Product([ Constant(2), Variable(1) ]), Constant(4) ])
print(expr3)

# 3x * 2x
expr4 = Product([ Product([Constant(3), Variable(1)]), Product([ Constant(2), Variable(1) ]) ])
print(expr4)

# x^2
expr5 = Exponential(Variable(1), Constant(2))
print(expr5)

# 0x^4
expr6 = Product([ Constant(0), Exponential(Variable(1), Constant(4)) ])
print(expr6)

# (8 + 7) * 3
expr7 = Product([ Sum([ Constant(8), Constant(7) ]), Constant(3) ])
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

# Derivative of product
print(D(Product((genf, geng, genh))))

# Derivative of exponential
print(D(Exponential(genf, genh)))
print(D(Exponential(Variable(1),Constant(-1))))
print(D(Exponential(Variable(1),Variable(1))))

# Problem with derivative of exponential
print(  D(Exponential(Constant(0),Variable(1)))  )

# ln
print( NaturalLogarithm(Variable(1)) )
print( D(NaturalLogarithm(genf)))
print( D(NaturalLogarithm(Variable(1))))

# general singlevariable function
print( GeneralSinglevar('cot', Variable(1)) )
print( D(GeneralSinglevar('cot', genf)) )