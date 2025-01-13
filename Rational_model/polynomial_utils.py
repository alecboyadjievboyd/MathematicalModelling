from Rational_model.constant_fraction import ConstantFraction
from Rational_model.polynomial import Polynomial


def make_monomial(degree, coefficient = ConstantFraction(1)):
    monomial_coefficients = [0] * degree
    monomial_coefficients.append(1)
    return Polynomial(monomial_coefficients, coefficient)

def polynomial_gcd(p, q):
    if p == Polynomial([0]):
        return q
    if q == Polynomial([0]):
        return p

    p1 = None
    q1 = None
    if p.degree() > q.degree():
        p1 = p.copy()
        q1 = q.copy()
    else:
        p1 = q.copy()
        q1 = p.copy()

    while q1 != Polynomial([0]):
        quotient, p1 = p1.divide_with_remainder(q1)
        p1, q1 = q1, p1


    p1 /= p1.coefficient
    return p1