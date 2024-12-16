from Algebraic_model.algebraic_expression import AlgebraicExpression, put_brackets
from Algebraic_model.algebraic_expression_type import AlgebraicExpressionType
from Algebraic_model.constant_fraction import ConstantFraction


# Fraction of algebraic expression over algebraic expression
class Fraction(AlgebraicExpression):

    def __init__(self, numerator, denominator, coefficient = ConstantFraction(1)):
        super().__init__(AlgebraicExpressionType.QUOTIENT, coefficient)
        self.numerator = numerator
        self.denominator = denominator

    def __str__(self):
        string_expression = f'{put_brackets(self.numerator)}/{put_brackets(self.denominator)}'
        return self.string_add_coefficient(string_expression)
