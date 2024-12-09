from Algebraic_model.expression_type import ExpressionType
from Algebraic_model.expression import Expression


class Monomial(Expression):

    def __init__(self, coefficient, exponents):
        super().__init__(ExpressionType.MONOMIAL)
        self.coefficient = coefficient
        self.exponents = exponents

    def __str__(self):

        # Computing sum of all exponents of the monomial
        sum_of_exponents = 0
        for exponent in self.exponents:
            sum_of_exponents += exponent

        string_expression = str(self.coefficient) if self.coefficient != 1 or sum_of_exponents == 0 else ""

        for i, exponent in enumerate(self.exponents):
            match exponent:
                case 0:
                    pass
                case 1:
                    string_expression += f'x{i}'
                case _:
                    string_expression += f'x{i}^{exponent}'

        return string_expression
