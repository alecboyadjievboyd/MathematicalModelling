from Algebraic_model.expression import Expression, put_brackets
from Algebraic_model.expression_type import ExpressionType


class Fraction(Expression):

    def __init__(self, numerator, denominator):
        super().__init__(ExpressionType.QUOTIENT)
        self.numerator = numerator
        self.denominator = denominator

    def __str__(self):
        return f'{put_brackets(self.numerator)}/{put_brackets(self.denominator)}'
