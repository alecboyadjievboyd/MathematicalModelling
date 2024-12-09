import abc
from Algebraic_model.expression_type import ExpressionType


# Abstract class of expression
def put_brackets(expression):
    if expression.expression_type == ExpressionType.SUM or expression.expression_type == ExpressionType.PRODUCT:
        return "(" + str(expression) + ")"
    else:
        return str(expression)


class Expression(abc.ABC):

    def __init__(self, expression_type):
        self.expression_type = expression_type

    @abc.abstractmethod
    def __str__(self):
        # This method must be implemented in subclasses
        pass
