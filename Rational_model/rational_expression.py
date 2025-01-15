import abc

from Rational_model.rational_expression_type import RationalExpressionType
from Rational_model.constant_fraction import ConstantFraction


# Abstract class of expression
class RationalExpression(abc.ABC):

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

    @abc.abstractmethod
    def put_brackets(self):
        pass

    # Append coefficient to string representing the expression
    def string_add_coefficient(self, string_expression):
        if self.coefficient == ConstantFraction(1):
            return string_expression
        elif self.expression_type == RationalExpressionType.MONOMIAL:
            return f'{self.coefficient}{string_expression}'
        else:
            return f'{self.coefficient}({string_expression})'

    def simplify(self):
        """
        Simplifies any rational expression to a fraction of polynomials
        :return: simplified expression
        """
        return NotImplemented

    def get_standard_form(self):
        """
        Returns the standard form of the rational expression - fraction of simplified and factorized polynomials
        in numerator and denominator
        :return: exression in the standard form
        """

        simplified_expression = self.simplify()
        factorized_expression = simplified_expression.factorize()
        return factorized_expression