from Rational_model.rational_expression import RationalExpression, put_brackets
from Rational_model.rational_expression_type import RationalExpressionType
from Rational_model.constant_fraction import ConstantFraction
from Rational_model.polynomial_utils import polynomial_gcd


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

    fraction.coefficient *= fraction.numerator.coefficient * fraction.denominator.coefficient
    fraction.numerator.coefficient = ConstantFraction(1)
    fraction.denominator.coefficient = ConstantFraction(1)

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
        super().__init__(RationalExpressionType.QUOTIENT, coefficient)
        self.numerator = numerator
        self.denominator = denominator

    def __str__(self):
        string_expression = f'{put_brackets(self.numerator)}/{put_brackets(self.denominator)}'
        return self.string_add_coefficient(string_expression)