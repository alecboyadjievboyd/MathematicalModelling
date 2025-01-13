from Rational_model.rational_expression_type import RationalExpressionType
from Rational_model.rational_expression import RationalExpression
from Rational_model.constant_fraction import ConstantFraction


# Puts brackets around a sum expression to preserve hierarchy, when outputting sum of sums
def put_brackets(expression):
    if expression.expression_type == RationalExpressionType.SUM:
        return f'({expression})'
    else:
        return str(expression)

# Sum of at least two algebraic expressions
class Sum(RationalExpression):

    def __init__(self, terms, coefficient = ConstantFraction(1)):
        super().__init__(RationalExpressionType.SUM, coefficient)
        self.terms = terms

    def __str__(self):
        string_expression = put_brackets(self.terms[0])
        for term in self.terms[1:]:
            string_expression += ' + ' + put_brackets(term)
        return self.string_add_coefficient(string_expression)
