from Model.integer import Integer
from Model.sine import Sine
from Model.cosine import Cosine
from Model.tangent import Tangent
from Model.arcsine import Arcsine
from Model.arccosine import Arccosine
from Model.arctangent import Arctangent
from Model.variable import Variable, Hypervariable
from Model.sum import Sum
from Model.product import Product
from Model.exponential import Exponential
from Model.general_multivar import GeneralMultivar
from Model.general_singlevar import GeneralSinglevar
from Model.natural_logarithm import NaturalLogarithm
from Model.logarithm import Logarithm
from Model.exp import Exp
from Model.make_expression import MakeExpression
from Model.expression_type import ExpressionType
from Model.fraction import Frac
from Model.simplifying_fractions import frac_constant_simplify
from Model.vartocon import Vartocon
from Model.euler import Euler
from Model.pi import Pi


def rt(x,n=2):
    return Exponential(Integer(x), Exponential(Integer(n), Integer(-1)))

def x(n=1):
    return Variable(n)

def h(n=-1):
    return Hypervariable(n)

def C(x):
    return Integer(x)

print(
    Tangent(Product((Frac(4,6), Pi())))
    .consim()
)


# print(
#     Exponential(
#         Frac(5,3),
#         Sum((
#             Frac(5,2),
            
#         ))
#     ).consim()
# )

# print(
#     Product((
#         Exponential(
#             Frac(5,3),
#             Sum((
#                 Frac(5,2),
#                 h()
#             ))
#         ).consim(),
#         Exponential(
#             Exponential(
#                 Frac(5,3),
#                 Sum((
#                     Frac(5,2),
                    
#                 ))
#             ).consim(),
#             C(-1)
#         )

#     )).consim()
# )

# print(
#     Product((
#         Exponential(
#             h(1),
#             Sum((
#                 C(2),
#                 h(2)
#             ))
#         ),
#         Exponential(
#             Exponential(h(1), C(-1)),
#             C(1)
#         )
#     )).consim(True)
# )

# print(
#     Product((
#         Frac(25,9),
#         Exponential(
#             Frac(5,3),
#             Sum((
#                 Sine(C(1)),
#                 Frac(1,2)
#             ))
#         ),
#         Exponential(
#             Frac(25,9),
#             C(-1)
#         )
#     )).consim()
# )

# print(
#     Product((
#         Frac(2),
#         Exponential(
#             Product((
#                 Frac(2),
#                 Exponential(Frac(3), Frac(1,4))
#             )),
#             C(-1)
#         )
#     )).consim()
# )

# print(
#     Product((
#         x(1),
#         Exponential(
#             Product((
#                 x(1),
#                 x(2)
#             )),
#             C(-1)
#         )
#     )).pfsf()
# )

# print(
# Product((C(7), Exponential(Sum((x(), C(1))), C(-2)))).pfsf()
# )

# print(Sum((x(), C(1))).pfsf())

# print(
#     Exponential(x(), C(-1)).pfsf()
# )

# print(
#     Exponential(Sum((x(), x(2), C(4))), C(-1)).pfsf()
# )

# print(
#     Exponential(C(0), x()).derivative(x())
# )

# print(
#     Exponential(C(0), x()).pfsf()
# )

# log_(1 + arcsin(1) + x1)((arctan(x1)^arccos(x1)))


# raise 'awareness'

# print(
# Product((
#     Product((h(1), h(2))),
#     h(3)
# )).consim()
# )

# print(
#     Product((
#         Euler(),
#         Euler()
#     )).consim()
# )

# print(
#     Exponential(
#         x(1),
#         Sum((x(2), x(3)))
#     ).pfsf()
# )

# print(
#     Exponential(
#         Product((
#             x(1),
#             x(2)
#         )),
#         x(3)
#     ).pfsf()
# )

# print(
#     Product((
#         Exponential(x(1), x(3)),
#         Exponential(x(2), x(3))
#     )).pfsf()
# )




# print(
#     x(1)
# )

# print(
#     Vartocon(
#         Sum((
#             h(2),
#             h(3)
#         ))
#     )
# )

# print(
#     Exponential(Exponential(x(), C(2)), Exponential(C(2), C(-1))).derivative(x())
# )

# print(
#     Exponential(Sum((C(1),Hypervariable(C(3)))), C(2)).consim()
# )

# print(
#     Exponential(Sum((Sine(C(1)),C(1))), Frac(2)).consim()
# )

# print(
#     Exponential( Sum((x(h(1)), x(Frac(1)))), C(2)).pfsf()
# )

# print("xxxxxxx")
# print(
#     Product((
#         Exponential(rt(2), rt(3)), Exponential(Exponential(rt(2),rt(3)),rt(4))
#     ))
# .consim())
# print("------")

# print(
#     Product((
#         Exponential(rt(2), rt(3)), Exponential(Exponential(rt(2),rt(3)),rt(4))
#     ))
# .pfsf()
# )

# print( Sum((rt(3),Product((Integer(2),rt(3))))).consim() )

# print( Sum(( Variable(Exponential(Frac(5), Frac(1,2))), Variable(Exponential(Frac(6),Frac(1,2))) )).pfsf() )

# print(
#     Product(( rt(2), Integer(1),Exponential( rt(2), rt(3))   )).consim()
#     )

# print(
#     Product(( Sum((rt(1), rt(2))), Sum((Frac(3),Frac(4))))).consim()
#     )


# y = Sum(( Sum((rt(3),rt(4))) , Sum(( Sum((rt(5), rt(6))), rt(7) )) )).consim()      
# print(y.expression_type)
# print(y)
# for i in y.terms:
#     print(i)
# print(y.terms)

# print( Sum((Variable(rt(3)), Product((Frac(2), Variable(rt(3)))))).pfsf() )

# print((Product((Sum((C(3),)), Exponential(C(4),C(5))))))


# for arg in (C(1), Sum((C(2), C(4)))):
#     print(arg)

# for i in range(4):
#     print(i)
#     i=0
#     print(i)



# x = MakeExpression(ExpressionType.LOGARITHM, (C(4),C(3),C(4)))
# print(x)

# def D(function, differential = Variable(1)):
#     return function.derivative(differential)

# print(Sine(Variable(1)))


# # print(Exp(GeneralMultivar("f")).derivative(Variable(1)))

# print('Constants:')
# # 8
# expr1 = C(8)
# # e
# expr2 = Euler()
# # pi
# expr3 = Pi()
# print(expr1, expr2, expr3)

# x
# expr2 = Variable(1)
# print(expr2)

# # 2x + 4
# expr3 = Sum([Product([C(2), Variable(1)]), C(4)])
# print(expr3)

# # 3x * 2x
# expr4 = Product([Product([C(3), Variable(1)]), Product([C(2), Variable(1)])])
# print(expr4)

# # x^2
# expr5 = Exponential(Variable(1), C(2))
# print(expr5)

# # 0x^4
# expr6 = Product([C(0), Exponential(Variable(1), C(4))])
# print(expr6)

# # (8 + 7) * 3
# expr7 = Product([Sum([C(8), C(7)]), C(3)])
# print(expr7)

# # x * ( x * (x * (x+1))) 
# expr8 = Product([ Variable(1), Product([ Variable(1), Product([ Variable(1), Sum([ Variable(1), Variable(1) ]) ]) ]) ])
# print(expr8)

# # dx/dy
# print( Variable(1).derivative(Variable(2)))

# # dx/dx
# print( Variable(1).derivative(Variable(1)))

# # derivative of constant
# print(C(23).derivative(Variable(1)))

# # # general multivariable functions
# # genf = GeneralMultivar('f')
# # geng = GeneralMultivar('g')
# # genh = GeneralMultivar('h')
# # print(genf)
# # print(Exponential(genf, Sum((geng, genh))))
# # print(genf.derivative(Variable(1)))
# # print(genf.derivative(Variable(1)).derivative(Variable(2)))

# # # the function D
# # print(D(genf, Variable(1)))
# # print(D(D(genf, Variable(1)), Variable(2)))
# # print(D(genf))


# # # Derivative of sum
# # print(D(Sum((genf, geng, genh))))

# # # Derivative of Product
# # print(D(Product((genf, geng, genh))))

# # # Derivative of Exponential
# # print(D(Exponential(genf, genh)))
# print(D(Exponential(Variable(1), C(-1))))
# print(D(Exponential(Variable(1),Variable(1))))

# # Problem with derivative of exponential
# print(D(Exponential(C(0), Variable(1))))

# # ln
# print( NaturalLogarithm(Variable(1)) )
# # print( D(NaturalLogarithm(genf)))
# print( D(NaturalLogarithm(Variable(1))))

# print('Logarithm:')
# # log_8((x+1)^2)
# expr1 = Logarithm(C(8), Exponential(Sum([Variable(1), C(1)]), C(2)))
# # log_e(pi)
# expr2 = Logarithm(Euler(), Pi())
# print(expr1, expr2)

# # general single variable function
# # print(GeneralSinglevar('cot', Variable(1)))
# # print(D(GeneralSinglevar('cot', genf)))