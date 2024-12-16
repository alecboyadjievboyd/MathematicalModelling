from Algebraic_model.constant_fraction import ConstantFraction
from Algebraic_model.fraction import Fraction
from Algebraic_model.polynomial import Polynomial
from Algebraic_model.product import Product
from Algebraic_model.monomial import Monomial
from Algebraic_model.sum import Sum

# Examples of monomials
mon1 = Monomial(3)
print(mon1)
mon2 = Monomial(1)
print(mon2)
mon3 = Monomial(2, 7)
print(mon3)
mon4 = Monomial(0)
print(mon4)
mon5 = Monomial(0, 4)
print(mon5)
mon6 = Monomial(18, 0)
print(mon6)
mon7 = Monomial(2, ConstantFraction(15, -7))
print(mon7)

# Examples of sums and products
print()
sum1 = Sum([mon2, mon3])
print(sum1)
sum2 = Sum([Sum([mon1, mon2]), mon4])
print(sum2)
product1 = Product([Sum([mon4, mon4]), mon2], ConstantFraction(13, 8))
print(product1)
product2 = Product([mon1, mon2, mon3])
print(product2)

# Examples of fractions
print()
frac1 = Fraction(sum1, sum2)
print(frac1)
frac2 = Fraction(Sum([sum1, product1]), product2)
print(frac2)
expr1 = Sum([frac1, frac2, mon3, product1], ConstantFraction(6, 9))
print(expr1)

# Examples of constant fractions
print()
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
print()
print(constFrac1 + constFrac2)
print(constFrac1 - constFrac4)
print(constFrac1 * constFrac4)
print(constFrac1 / constFrac5)
print(constFrac1 ** 4)

# Examples of polynomials
print()
poly1 = Polynomial([2, 0, 3, 0, 0])
print(poly1)
print(poly1.get_value(3))
print(poly1.get_value(ConstantFraction(2, 7)))
poly2 = Polynomial([6, 1, -1], ConstantFraction(1))
print(poly2)
print(poly2.check_root(2))
print(poly2.check_root(3))
print(poly2.check_root(-2))