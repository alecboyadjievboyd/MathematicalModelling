from Rational_model.fraction import Fraction
from Rational_model.polynomial import Polynomial
from Rational_model.rational_expression import RationalExpression, put_brackets
from Rational_model.rational_expression_type import RationalExpressionType
from Rational_model.constant_fraction import ConstantFraction


# Product of at least two algebraic expressions
class Product(RationalExpression):

    def __init__(self, factors, coefficient = ConstantFraction(1)):
        super().__init__(RationalExpressionType.PRODUCT, coefficient)
        self.factors = factors

    def __str__(self):
        string_expression = put_brackets(self.factors[0])
        for factor in self.factors[1:]:
            string_expression += " * " + put_brackets(factor)
        return self.string_add_coefficient(string_expression)

    def pull_out_constants(self):
        for factor in self.factors:
            self.coefficient *= factor.coefficient
            factor.coefficient = ConstantFraction(1)

    # Simplifies a product of rational expressions to a fraction of polynomials
    def simplify(self):

        for factor in self.factors:
            factor.simplify()
        self.pull_out_constants()

        numerator = Polynomial([1])
        denominator = Polynomial([1])
        for factor in self.factors:
            if factor.expression_type == RationalExpressionType.POLYNOMIAL:
                numerator *= factor
            else:
                numerator *= factor.numerator
                denominator = factor.denominator

        result = Fraction(numerator, denominator, self.coefficient)
        result = result.simplify()
        return result