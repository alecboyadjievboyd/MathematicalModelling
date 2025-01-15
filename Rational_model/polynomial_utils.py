from Rational_model.constant_fraction import ConstantFraction


def make_monomial(degree, coefficient = ConstantFraction(1)):
    from Rational_model.polynomial import Polynomial

    monomial_coefficients = [0] * degree
    monomial_coefficients.append(1)
    return Polynomial(monomial_coefficients, coefficient)

def divide_with_remainder(dividend, divider):
    """
    Divide dividend by divider with remainder.
    :param dividend: dividend - to be divided.
    :param divider: divider - to divide with.
    :return: A list of two elements. The first one is the quotient and the second one is the remainder.
    """
    from Rational_model.polynomial import Polynomial

    remainder = dividend.copy()
    quotient = Polynomial([0])

    while remainder.degree() >= divider.degree() and remainder != Polynomial([0]):
        multiplier = make_monomial(remainder.degree() - divider.degree(),
                                    remainder.coefficient * remainder.monomial_coefficients[remainder.degree()]
                                   / divider.coefficient / divider.monomial_coefficients[divider.degree()])
        quotient += multiplier
        remainder -= divider * multiplier

    return [quotient, remainder]

def polynomial_gcd(p, q):
    from Rational_model.polynomial import Polynomial

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
        quotient, p1 = divide_with_remainder(p1, q1)
        p1, q1 = q1, p1


    p1 /= p1.coefficient
    return p1