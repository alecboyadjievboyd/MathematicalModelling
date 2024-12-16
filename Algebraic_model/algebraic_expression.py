import abc
from Algebraic_model.algebraic_expression_type import AlgebraicExpressionType
from Algebraic_model.constant_fraction import ConstantFraction


# Abstract class of expression
def put_brackets(expression):
    if expression.expression_type == AlgebraicExpressionType.SUM or expression.expression_type == AlgebraicExpressionType.PRODUCT:
        return "(" + str(expression) + ")"
    else:
        return str(expression)


class AlgebraicExpression(abc.ABC):

    def __init__(self, expression_type, coefficient = ConstantFraction(1)):
        if type(coefficient) == int:
            # Turning integer coefficient into constant fraction type
            coefficient = ConstantFraction(coefficient)
        elif type(coefficient) != ConstantFraction:
            # Coefficient can only be integer of ConstantFraction
            raise TypeError("Coefficient must be of type int or ConstantFraction")

        self.expression_type = expression_type
        self.coefficient = coefficient

    @abc.abstractmethod
    def __str__(self):
        # This method must be implemented in subclasses
        pass

    # Append coefficient to string representing the expression
    def string_add_coefficient(self, string_expression):
        if self.coefficient == ConstantFraction(1):
            return string_expression
        elif self.expression_type == AlgebraicExpressionType.MONOMIAL:
            return f'{self.coefficient}{string_expression}'
        else:
            return f'{self.coefficient}({string_expression})'