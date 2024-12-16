from Algebraic_model.algebraic_expression_type import AlgebraicExpressionType
from Algebraic_model.algebraic_expression import AlgebraicExpression
from Algebraic_model.constant_fraction import ConstantFraction


class Monomial(AlgebraicExpression):

    def __init__(self, exponent, coefficient = ConstantFraction(1)):
        super().__init__(AlgebraicExpressionType.MONOMIAL, coefficient)
        self.exponent = exponent

    def __str__(self):

        if self.exponent == 0:
            if self.coefficient == 1:
                string_expression = "1"
            else:
                string_expression = ""
        elif self.exponent == 1:
            string_expression = "x"
        else:
            string_expression = f'x^{self.exponent}'

        return self.string_add_coefficient(string_expression)
