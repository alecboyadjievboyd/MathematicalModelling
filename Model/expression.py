import abc
from expression_type import ExpressionType

# Abstract class of expression
class Expression(abc.ABC):

    def __init__(self, type):
        self.expression_type = type
    
    def put_brackets(self, expression):
        if (expression.expression_type == ExpressionType.SUM or expression.expression_type == ExpressionType.PRODUCT):
            return "(" + str(expression) + ")"
        else:
            return str(expression)
    
    @abc.abstractmethod
    def __str__(self):
        pass

    @abc.abstractmethod
    def __eq__(self, other):
        pass
