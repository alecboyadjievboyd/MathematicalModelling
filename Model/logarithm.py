from expression import Expression
from expression_type import ExpressionType
from exponential import Exponential
from product import Product
from constant import Constant


class Logarithm(Expression):
    def __init__(self, base, argument):
        super().__init__(ExpressionType.LOGARITHM)
        self.base = base
        self.argument = argument
        self.isConstant = None

    def __str__(self):
        return f'log_{self.base}({str(self.argument)})'

    def __eq__(self, other):
        if self.expression_type != other.expression_type:
            return False
        if str(self) == str(other):
            return True
        else:
            return False

    def derivative(self, differential):
        return Product([
            self.argument.derivative(differential),
            Exponential(Logarithm(Constant('e'), self.base), -1),
            Exponential(self, -1)
        ])
