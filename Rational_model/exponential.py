from Rational_model.rational_expression import RationalExpression
from Rational_model.constant_fraction import ConstantFraction
from Rational_model.rational_expression_type import RationalExpressionType
from Rational_model.polynomial_utils import make_monomial
from Rational_model.fraction import Fraction


class Exponential(RationalExpression):
    def __init__(self, base, exponent, coefficient = ConstantFraction(1)):
        if not isinstance(base, RationalExpression):
            raise TypeError("Exponential base must be of type RationalExpression")
        if not isinstance(exponent, int):
            raise TypeError("Exponential exponent must be an integer")

        super().__init__(RationalExpressionType.EXPONENTIAL, coefficient)
        self.base = base
        self.exponent = exponent

    def __str__(self):
        return f'({self.base})^{self.exponent}'

    def put_brackets(self):
        return str(self)

    def simplify(self):
        from Rational_model.product import Product

        if self.exponent == 0:
            return make_monomial(0, 1)
        elif self.exponent == 1:
            return self.base
        elif self.exponent == -1:
            return Fraction(make_monomial(0, 1), self.base)

        factors = [self.base] * abs(self.exponent)
        product = Product(factors, self.coefficient)

        if self.exponent > 0:
            return product.simplify()
        else:
            return Fraction(make_monomial(0, 1), product).simplify()