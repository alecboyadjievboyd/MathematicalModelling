from Rational_model.constant_fraction import ConstantFraction
from Rational_model.exponential import Exponential
from Rational_model.fraction import Fraction, polynomial_fraction_simplify
from Rational_model.polynomial import Polynomial
from Rational_model.product import Product
from Rational_model.sum import Sum
from Rational_model.polynomial_utils import polynomial_gcd, make_monomial, divide_with_remainder
from parsing_algebra import express_alg

# Examples of monomials
print('\nMonomials:')
mon1 = make_monomial(3)
print(mon1)
mon2 = make_monomial(1)
print(mon2)
mon3 = make_monomial(2, 7)
print(mon3)
mon4 = make_monomial(0, 0)
print(mon4)
mon5 = make_monomial(0, 4)
print(mon5)
mon6 = make_monomial(18, 0)
print(mon6)
mon7 = make_monomial(2, ConstantFraction(15, -7))
print(mon7)

# Examples of sums and products
print('\nSums and products:')
sum1 = Sum([mon2, mon3])
print(sum1)
sum2 = Sum([Sum([mon1, mon2]), mon4])
print(sum2)
product1 = Product([Sum([mon4, mon4]), mon2], ConstantFraction(13, 8))
print(product1)
product2 = Product([mon1, mon2, mon3])
print(product2)

# Examples of fractions
print('\nFractions:')
frac1 = Fraction(sum1, sum2)
print(frac1)
frac2 = Fraction(Sum([sum1, product1]), product2)
print(frac2)
expr1 = Sum([frac1, frac2, mon3, product1], ConstantFraction(6, 9))
print(expr1)

# Examples of constant fractions
print('\nConstant fractions:')
constFrac1 = ConstantFraction(1, 2)
print(constFrac1)
constFrac2 = ConstantFraction(8)
print(constFrac2)
constFrac3 = ConstantFraction(0, 15)
print(constFrac3)
constFrac4 = ConstantFraction(27, -8)
print(constFrac4)
constFrac5 = ConstantFraction(-9, -3)
print(constFrac5)

# Examples of operations with constant fractions
print('\nOperations with constants:')
print(constFrac1 + constFrac2)
print(constFrac1 - constFrac4)
print(constFrac1 * constFrac4)
print(constFrac1 / constFrac5)
print(constFrac1 ** 4)

# Examples of polynomials
print('\nPolynomials:')
# 1/2x^3 + 3x^2 + 2
poly1 = Polynomial([2, 0, 3, ConstantFraction(1, 2), 0])
print(poly1)
# -x^2 + x + 6
poly2 = Polynomial([6, 1, -1], ConstantFraction(1))
print(poly2)
# 4x^2 - 1
poly3 = Polynomial([-1, 0, 4])
print(poly3)
# 2x^2 + 2x + 2
poly4 = Polynomial([2, 2, 2])
print(poly4)
# x + 3
poly5 = Polynomial([ConstantFraction(3, 2), ConstantFraction(1, 2)], 2)
print(poly5)
# 0
poly6 = Polynomial([1, 2, 3], 0)
print(poly6)
# 2/3
poly7 = Polynomial([ConstantFraction(2, 3)], 1)
print(poly7)
# -x^2 - 7
poly8 = Polynomial([ConstantFraction(-1), 0, ConstantFraction(-7)], 1)
print(poly8)


#Working with polynomials
print('\nWorking with polynomials:')
print(poly1.get_value(3))
print(poly1.get_value(ConstantFraction(2, 7)))

print(poly2.is_root(2))
print(poly2.is_root(3))
print(poly2.is_root(-2))
for i in poly2.find_rational_roots():
    print(i, end=' ')
print()
for i in poly3.find_rational_roots():
    print(i, end=' ')
print()

# Algebraic operations on polynomials
print('\nOperations on polynomials:')
print(poly1 + poly2)
print(poly1 - poly2)
print(poly1 * poly2)
quot, rem = divide_with_remainder(poly2, Polynomial([-3, 1]))
print(quot, rem, sep=', ')
quot, rem = divide_with_remainder(poly2, Polynomial([2, 1]))
print(quot, rem, sep=', ')
quot, rem = divide_with_remainder(poly1, poly4)
print(quot, rem, sep=', ')

# Factorization
print('\nFactorization:')
print(poly2.factorize())
print(poly1. factorize())

# GCD
print('\nGCD:')
gcd_poly1 = Polynomial([-6, -1, 1], ConstantFraction(4, 3))
print(gcd_poly1)
gcd_poly2 = Polynomial([-2, -3, -1])
print(gcd_poly2)
print(polynomial_gcd(gcd_poly1, gcd_poly2))

#Simplification
print('\nSimplification:')
fr1 = Fraction(gcd_poly1, gcd_poly2, ConstantFraction(3, 5))
print(fr1)
print(polynomial_fraction_simplify(fr1))
fr2 = Fraction(poly1, poly2)
print(fr2)
print(fr2.factorize())

fr3 = Fraction(fr1, fr2)
print(fr3)
fr3 = fr3.simplify()
print(fr3)

sum3 = Sum([fr1, poly1, make_monomial(0, 0), make_monomial(2, 2)], ConstantFraction(1, 7))
print(sum3)
sum3 = sum3.simplify()
print(sum3)

product3 = Product([fr1, poly1, make_monomial(0, ConstantFraction(4, 3)), make_monomial(2, 2)])
print(product3)
print(product3.simplify())
print(product3.get_standard_form())

p = Polynomial([0, 0, 2, 3])
print(p)
print(p.factorize())
q = Polynomial([1, 3, 3, 1])
print(q)
print(q.factorize())

print('\nExponentials:')
exp1 = Exponential(make_monomial(0, 0), 30)
print(exp1)
print(exp1.simplify())
exp2 = Exponential(make_monomial(1, 1), 2)
print(exp2)
print(exp2.simplify())
exp3 = Exponential(Polynomial([3, 1]), -2)
print(exp3)
print(exp3.simplify())

print('\nShow representation:')
print(expr1.show_representation())
print(expr1)

print()
expr2_1 = express_alg('((x^2+2)/(x+3))*((x^2+4x+3)/(x^2+2))')
print(expr2_1)
print(expr2_1.show_representation())
print(expr2_1.simplify())