from Algebraic_model.expression import Expression, put_brackets
from Algebraic_model.expression_type import ExpressionType


class Product(Expression):

    def __init__(self, factors):
        super().__init__(ExpressionType.PRODUCT)
        self.factors = factors

    def __str__(self):
        string_expression = put_brackets(self.factors[0])
        for factor in self.factors[1:]:
            string_expression += " * " + put_brackets(factor)
        return string_expression
