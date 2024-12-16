import math

from Algebraic_model.algebraic_expression import AlgebraicExpression
from Algebraic_model.algebraic_expression_type import AlgebraicExpressionType
from Algebraic_model.constant_fraction import ConstantFraction
from Algebraic_model.monomial import Monomial
from Algebraic_model.sum import Sum


# Polynomial expression with integer coefficients of monomials and constant fraction coefficient for the whole
# polynomial
class Polynomial(AlgebraicExpression):
    def __init__(self, monomial_coefficients, coefficient = ConstantFraction(1)):
        super().__init__(AlgebraicExpressionType.POLYNOMIAL, coefficient)
        self.monomial_coefficients = monomial_coefficients
        self.degree = len(monomial_coefficients) - 1

        self.normalize()

    # Polynomial is in the normal form when the coefficient of highest degree monomial is strictly positive and
    # coefficients of monomials are relatively prime integers
    def normalize(self):
        # Deleting leading monomials with zero coefficient
        while self.degree > 0 and self.monomial_coefficients[self.degree] == 0:
            self.monomial_coefficients.pop(self.degree)
            self.degree -= 1

        # Taking -1 to coefficient of the polynomial if coefficient of the leading monomial is negative
        if self.monomial_coefficients[self.degree] < 0:
            for coefficient in self.monomial_coefficients:
                coefficient *= -1
            self.coefficient *= -1

        if self.degree == 0 and self.monomial_coefficients[0] == 0:
            # Zero polynomial
            self.coefficient = ConstantFraction(0)
        else:
            # Factoring out common divisor
            gcd = 0
            for coefficient in self.monomial_coefficients:
                gcd = math.gcd(gcd, coefficient)

            for coefficient in self.monomial_coefficients:
                coefficient //= gcd
            self.coefficient *= gcd

    def to_sum(self):
        monomials = []
        for i, coefficient in enumerate(self.monomial_coefficients):
            if coefficient != 0:
                monomials.append(Monomial(i, coefficient))
        return Sum(monomials, self.coefficient)

    def __str__(self):
        return str(self.to_sum())

    def get_value(self, root):
        value = self.monomial_coefficients[self.degree]
        for i in range(self.degree - 1, -1, -1):
            value = value * root + self.monomial_coefficients[i]
        return value

    def check_root(self, root):
        return self.get_value(root) == 0