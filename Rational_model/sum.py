from Rational_model.fraction import Fraction
from Rational_model.polynomial import Polynomial
from Rational_model.polynomial_utils import make_monomial
from Rational_model.rational_expression_type import RationalExpressionType
from Rational_model.rational_expression import RationalExpression
from Rational_model.constant_fraction import ConstantFraction


# Puts brackets around a sum expression to preserve hierarchy, when outputting sum of sums
def put_brackets(expression):
    if expression.expression_type == RationalExpressionType.SUM:
        return f'({expression})'
    else:
        return str(expression)

# Sum of at least two algebraic expressions
class Sum(RationalExpression):

    def __init__(self, terms, coefficient = ConstantFraction(1)):
        super().__init__(RationalExpressionType.SUM, coefficient)
        self.terms = terms

    def __str__(self):
        string_expression = put_brackets(self.terms[0])
        for term in self.terms[1:]:
            string_expression += ' + ' + put_brackets(term)
        return self.string_add_coefficient(string_expression)

    # Simplifies a sum of rational expressions to a fraction of polynomials
    def simplify(self):
        # Simplify every term of the sum to a polynomial fraction first
        for term in self.terms:
            term.simplify()

        # Construct denominator of the simplified expression
        denominator = make_monomial(0, 1)
        for term in self.terms:
            if term.expression_type == RationalExpressionType.FRACTION:
                denominator *= term.denominator

        numerator = make_monomial(0, 0)
        for term in self.terms:
            add = None
            if term.expression_type == RationalExpressionType.POLYNOMIAL:
                add = term * denominator
            else:
                add = term.coefficient * term.numerator * denominator
                q, rem = add.divide_with_remainder(term.denominator)
                if rem != Polynomial([0]):
                    raise ValueError('Polynomial is not divisible exactly')
                add = q
            numerator += add

        result = Fraction(numerator, denominator, self.coefficient)
        result = result.simplify()
        return result

