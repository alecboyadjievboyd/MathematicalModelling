from Rational_model.rational_expression import RationalExpression, put_brackets
from Rational_model.rational_expression_type import RationalExpressionType
from Rational_model.constant_fraction import ConstantFraction
from Rational_model.polynomial_utils import polynomial_gcd, make_monomial


# Simplifies
def polynomial_fraction_simplify(fraction):
    if (fraction.numerator.expression_type != RationalExpressionType.POLYNOMIAL
            or fraction.denominator.expression_type != RationalExpressionType.POLYNOMIAL):
        raise TypeError('Given fraction is not a fraction of polynomials')

    gcd = polynomial_gcd(fraction.numerator, fraction.denominator)
    quotient, remainder = fraction.numerator.divide_with_remainder(gcd)
    fraction.numerator = quotient
    quotient, remainder = fraction.denominator.divide_with_remainder(gcd)
    fraction.denominator = quotient

    fraction.pull_out_constant()

    return fraction

def polynomial_fraction_factorize(fraction):
    if (fraction.numerator.expression_type != RationalExpressionType.POLYNOMIAL
            or fraction.denominator.expression_type != RationalExpressionType.POLYNOMIAL):
        raise TypeError('Given fraction is not a fraction of polynomials')

    result = Fraction(fraction.numerator.factorize(), fraction.denominator.factorize(), fraction.coefficient)
    return result

# Fraction of algebraic expression over algebraic expression
class Fraction(RationalExpression):

    def __init__(self, numerator, denominator, coefficient = ConstantFraction(1)):
        super().__init__(RationalExpressionType.FRACTION, coefficient)
        self.numerator = numerator
        self.denominator = denominator

    def __str__(self):
        string_expression = f'{put_brackets(self.numerator)}/{put_brackets(self.denominator)}'
        return self.string_add_coefficient(string_expression)

    def pull_out_constant(self):
        self.coefficient *= self.numerator.coefficient / self.denominator.coefficient
        self.numerator.coefficient = ConstantFraction(1)
        self.denominator.coefficient = ConstantFraction(1)

    # Simplifies a fraction of rational expressions to a fraction of polynomials
    def simplify(self):
        if (self.numerator.expression_type != RationalExpressionType.POLYNOMIAL
                or self.denominator.expression_type != RationalExpressionType.POLYNOMIAL):

            self.numerator.simplify()
            self.denominator.simplify()

            self.pull_out_constant()

            p1 = None
            q1 = None
            if self.numerator.expression_type == RationalExpressionType.POLYNOMIAL:
                p1 = self.numerator
                q1 = make_monomial(0, 1)
            else:
                p1 = self.numerator.numerator
                q1 = self.numerator.denominator

            p2 = None
            q2 = None
            if self.denominator.expression_type == RationalExpressionType.POLYNOMIAL:
                p2 = self.denominator
                q2 = make_monomial(0, 1)
            else:
                p2 = self.denominator.numerator
                q2 = self.denominator.denominator

            self.numerator = p1 * q2
            self.denominator = q1 * p2

        polynomial_fraction_simplify(self)

        return self