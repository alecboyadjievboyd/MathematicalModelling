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
