from Rational_model.rational_expression import RationalExpression
from Rational_model.rational_expression_type import RationalExpressionType
from Rational_model.constant_fraction import ConstantFraction
from Rational_model.polynomial_utils import polynomial_gcd, make_monomial
from Rational_model.polynomial_utils import divide_with_remainder


# Simplifies
def polynomial_fraction_simplify(fraction):
    if (fraction.numerator.expression_type != RationalExpressionType.POLYNOMIAL
            or fraction.denominator.expression_type != RationalExpressionType.POLYNOMIAL):
        raise TypeError('Given fraction is not a fraction of polynomials')

    gcd = polynomial_gcd(fraction.numerator, fraction.denominator)
    quotient, remainder = divide_with_remainder(fraction.numerator, gcd)
    fraction.numerator = quotient
    quotient, remainder = divide_with_remainder(fraction.denominator, gcd)
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
        string_expression = f'{self.numerator.put_brackets()} / {self.denominator.put_brackets()}'
        return self.string_add_coefficient(string_expression)

    def put_brackets(self):
        return str(self)

    def copy(self):
        return Fraction(self.numerator.copy(), self.denominator.copy(), self.coefficient.copy())

    def pull_out_constant(self):
        self.coefficient *= self.numerator.coefficient / self.denominator.coefficient
        self.numerator.coefficient = ConstantFraction(1)
        self.denominator.coefficient = ConstantFraction(1)

    # Simplifies a fraction of rational expressions to a fraction of polynomials
    def simplify(self):
        if (self.numerator.expression_type != RationalExpressionType.POLYNOMIAL
                or self.denominator.expression_type != RationalExpressionType.POLYNOMIAL):

            self.numerator = self.numerator.simplify()
            self.denominator = self.denominator.simplify()

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

        result = self.copy()
        polynomial_fraction_simplify(result)

        # Remove the denominator if it is 1
        if self.denominator == make_monomial(0, 1):
            result = result.numerator * result.coefficient

        return result