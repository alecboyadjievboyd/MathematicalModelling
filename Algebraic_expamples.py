from Algebraic_model.product import Product
from Algebraic_model.monomial import Monomial
from Algebraic_model.fraction import Fraction
from Algebraic_model.sum import Sum

# Examples of monomials
mon1 = Monomial(1, [2, 3, 4])
print(mon1)
mon2 = Monomial(0, [0, 0, 2])
print(mon2)
mon3 = Monomial(5, [6, 0, 1])
print(mon3)
mon4 = Monomial(3, [1])
print(mon4)

# Examples of sums and products
sum1 = Sum([mon2, mon3])
print(sum1)
sum2 = Sum([Sum([mon1, mon2]), mon4])
print(sum2)
product1 = Product([Sum([mon4, mon4]), mon2])
print(product1)
product2 = Product([mon1, mon2, mon3])
print(product2)

# Examples of fractions
frac1 = Fraction(sum1, sum2)
print(frac1)
frac2 = Fraction(Sum([sum1, product1]), product2)
print(frac2)
expr1 = Sum([frac1, frac2, mon3, product1])
print(expr1)