from Algebraic_model.algebraic_expression import AlgebraicExpression, put_brackets
from Algebraic_model.algebraic_expression_type import AlgebraicExpressionType
from Algebraic_model.constant_fraction import ConstantFraction


# Product of at least two algebraic expressions
class Product(AlgebraicExpression):

    def __init__(self, factors, coefficient = ConstantFraction(1)):
        super().__init__(AlgebraicExpressionType.PRODUCT, coefficient)
        self.factors = factors

    def __str__(self):
        string_expression = put_brackets(self.factors[0])
        for factor in self.factors[1:]:
            string_expression += " * " + put_brackets(factor)
        return self.string_add_coefficient(string_expression)
