from Algebraic_model.expression_type import ExpressionType
from Algebraic_model.expression import Expression


# Puts brackets around a sum expression to preserve hierarchy, when outputting sum of sums
def put_brackets(expression):
    if expression.expression_type == ExpressionType.SUM:
        return f'({expression})'
    else:
        return str(expression)


class Sum(Expression):

    def __init__(self, terms):
        super().__init__(ExpressionType.SUM)
        self.terms = terms

    def __str__(self):
        string_expression = put_brackets(self.terms[0])
        for term in self.terms[1:]:
            string_expression += ' + ' + put_brackets(term)
        return string_expression
