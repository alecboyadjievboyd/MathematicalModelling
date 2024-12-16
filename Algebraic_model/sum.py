from Algebraic_model.algebraic_expression_type import AlgebraicExpressionType
from Algebraic_model.algebraic_expression import AlgebraicExpression
from Algebraic_model.constant_fraction import ConstantFraction


# Puts brackets around a sum expression to preserve hierarchy, when outputting sum of sums
def put_brackets(expression):
    if expression.expression_type == AlgebraicExpressionType.SUM:
        return f'({expression})'
    else:
        return str(expression)

# Sum of at least two algebraic expressions
class Sum(AlgebraicExpression):

    def __init__(self, terms, coefficient = ConstantFraction(1)):
        super().__init__(AlgebraicExpressionType.SUM, coefficient)
        self.terms = terms

    def __str__(self):
        string_expression = put_brackets(self.terms[0])
        for term in self.terms[1:]:
            string_expression += ' + ' + put_brackets(term)
        return self.string_add_coefficient(string_expression)
