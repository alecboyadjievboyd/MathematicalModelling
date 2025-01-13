import math

from Rational_model.rational_expression import RationalExpression
from Rational_model.rational_expression_type import RationalExpressionType
from Rational_model.constant_fraction import ConstantFraction


def find_divisors(n):
    """
    Finds all positive integer divisors of n != 0

    :param n: integer to find divisors for.
    :return: list of divisors of n.
    """

    # Every natural number is divisor of zero, so can't return all divisors
    if n == 0:
        raise ValueError("Can't list divisors of 0")

    # Check if n is integer
    if not isinstance(n, int):
        raise TypeError("n must be an integer")

    # We are interested only in positive divisors
    n = abs(n)

    # Find divisors by checking for all numbers i from 1 to sqrt(n) if they divide n
    divisors = set()
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.add(i)
            # If i divides n, then also n/i divides n
            divisors.add(n // i)
    return list(divisors)

# Polynomial expression with integer coefficients of monomials and constant fraction coefficient for the whole
# polynomial
class Polynomial(RationalExpression):
    def __init__(self, monomial_coefficients, coefficient = ConstantFraction(1)):
        # Check that polynomial coefficient and each monomial coefficient is either integer or constant fraction
        if type(coefficient) != int and type(coefficient) != ConstantFraction:
            raise TypeError("Polynomial coefficient must be of type int or ConstantFraction")
        for coef in monomial_coefficients:
            if type(coef) != int and type(coef) != ConstantFraction:
                raise TypeError("All monomial coefficients must be of type int or ConstantFraction")

        # Turn integer coefficients into constant fractions
        if type(coefficient) == int:
            coefficient = ConstantFraction(coefficient)
        for i, coef in enumerate(monomial_coefficients):
            if type(coef) == int:
                monomial_coefficients[i] = ConstantFraction(coef)

        super().__init__(RationalExpressionType.POLYNOMIAL, coefficient)
        self.monomial_coefficients = monomial_coefficients

        self.normalize()

    # Polynomial is in the normal form when the coefficient of highest degree monomial is strictly positive and
    # coefficients of monomials are relatively prime integers
    def normalize(self):

        # Changing polynomial with the zero coefficient into a proper zero polynomial
        if self.coefficient == 0:
            self.monomial_coefficients = [0]

        # Deleting leading monomials with zero coefficient
        while self.degree() > 0 and self.monomial_coefficients[self.degree()] == 0:
            self.monomial_coefficients.pop(self.degree())

        # Taking -1 to coefficient of the polynomial if coefficient of the leading monomial is negative
        if self.monomial_coefficients[self.degree()] < 0:
            for i in range(self.degree() + 1):
                self.monomial_coefficients[i] *= -1
            self.coefficient *= -1

        if self.degree() == 0 and self.monomial_coefficients[0] == 0:
            # Zero polynomial gets zero polynomial coefficient
            self.coefficient = ConstantFraction(0)
        else:
            # Factoring out common divisor of numerators of monomial coefficients into the polynomial coefficient
            gcd = 0
            for coefficient in self.monomial_coefficients:
                gcd = math.gcd(gcd, coefficient.numerator)
            for i in range(len(self.monomial_coefficients)):
                self.monomial_coefficients[i] /= gcd
            self.coefficient *= gcd

            # Factoring out common multiple of denominators of monomial coefficients into the polynomial coefficient
            lcm = 1
            for coefficient in self.monomial_coefficients:
                lcm = math.lcm(lcm, coefficient.denominator)
            for i in range(len(self.monomial_coefficients)):
                self.monomial_coefficients[i] = (self.monomial_coefficients[i].numerator
                                                  * (lcm // self.monomial_coefficients[i].denominator))
            self.coefficient /= lcm

    # Get the degree of polynomial.
    # Degree of a zero polynomial is defined 0
    def degree(self):
        return len(self.monomial_coefficients) - 1

    # Converts polynomial into a string
    def __str__(self):
        if self.degree() > 0:
            result = ''

            if self.monomial_coefficients[self.degree()] < 0:
                result += '-'
            if abs(self.monomial_coefficients[self.degree()]) != 1:
                result += str(abs(self.monomial_coefficients[self.degree()]))

            if self.degree() > 1:
                result += f'x^{self.degree()}'
            else:
                result += 'x'

            for i in range(self.degree() - 1, -1, -1):
                if self.monomial_coefficients[i] == 0:
                    continue
                elif self.monomial_coefficients[i] > 0:
                    result += ' + '
                else:
                    result += ' - '

                if abs(self.monomial_coefficients[i]) != 1 or i == 0:
                    result += str(abs(self.monomial_coefficients[i]))

                if i > 1:
                    result += f'x^{i}'
                elif i == 1:
                    result += 'x'

            number_of_monomials = 0
            for coefficient in self.monomial_coefficients:
                if coefficient != 0:
                    number_of_monomials += 1
            if number_of_monomials > 1 and self.coefficient != 1:
                result = f'({result})'

            if self.coefficient == -1:
                result = f'-{result}'
            elif self.coefficient != 1:
                result = f'{self.coefficient}{result}'

            return result
        else:
            return str(self.coefficient)

    def __eq__(self, other):
        if not isinstance(other, Polynomial):
            return NotImplemented

        if self.coefficient != other.coefficient:
            return False
        if self.degree() != other.degree():
            return False
        for i in range(self.degree() + 1):
            if self.monomial_coefficients[i] != other.monomial_coefficients[i]:
                return False
        return True

    # Adds two polynomials
    def __add__(self, other):
        if not isinstance(other, Polynomial):
            return NotImplemented

        sum_monomial_coefficients = []
        n = max(len(other.monomial_coefficients), len(self.monomial_coefficients))
        for i in range(n):
            sum_monomial_coefficients.append(ConstantFraction(0))
            if i < len(self.monomial_coefficients):
                sum_monomial_coefficients[i] += self.monomial_coefficients[i] * self.coefficient
            if i < len(other.monomial_coefficients):
                sum_monomial_coefficients[i] += other.monomial_coefficients[i] * other.coefficient
        return Polynomial(sum_monomial_coefficients)

    # Subtracts polynomial from another polynomial
    def __sub__(self, other):
        if not isinstance(other, Polynomial):
            return NotImplemented

        return self + (-1) * other

    # Multiplies the polynomial by another polynomial, integer or a constant fraction
    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, ConstantFraction):
            return Polynomial(self.monomial_coefficients, self.coefficient * other)
        if isinstance(other, Polynomial):
            product_monomial_coefficients = [0] * (self.degree() + other.degree() + 1)
            for i, coefficient1 in enumerate(self.monomial_coefficients):
                for j, coefficient2 in enumerate(other.monomial_coefficients):
                    product_monomial_coefficients[i + j] += coefficient1 * coefficient2
            return Polynomial(product_monomial_coefficients, self.coefficient * other.coefficient)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, int):
            other = ConstantFraction(other)
        elif not isinstance(other, ConstantFraction):
            return NotImplemented

        self.coefficient /= other
        return self

    def copy(self):
        return Polynomial(self.monomial_coefficients.copy(), self.coefficient)

    def get_value(self, x):
        """
        Compute the value of this polynomial in rational point x.
        :param x: point to find the value in.
        :return: the value of this polynomial in point x.
        """
        value = self.monomial_coefficients[self.degree()]
        for i in range(self.degree() - 1, -1, -1):
            value = value * x + self.monomial_coefficients[i]
        return value


    def is_root(self, root):
        """
        Check if root is a root of this polynomial

        :param root: root to check
        :return: if root is a root of this polynomial, return True
        """
        return self.get_value(root) == 0

    def find_rational_roots(self):
        """
        Computes all rational roots of this polynomial.
        :return: list of rational roots of this polynomial.
        """

        rational_roots = []

        if self.is_root(0):
            rational_roots.append(ConstantFraction(0))

        first_coefficient = 0
        while self.monomial_coefficients[first_coefficient] == 0:
            first_coefficient += 1

        divisors_leading_coefficient = find_divisors(self.monomial_coefficients[self.degree()])
        divisors_constant_term = find_divisors(self.monomial_coefficients[first_coefficient])


        for p in divisors_constant_term:
            for q in divisors_leading_coefficient:
                candidate_root = ConstantFraction(p, q)
                if self.is_root(candidate_root):
                    rational_roots.append(candidate_root)
                if self.is_root(candidate_root * (-1)):
                    rational_roots.append(candidate_root * (-1))
        return rational_roots

    def divide_with_remainder(self, dividend):
        remainder = self.copy()
        quotient = Polynomial([0])

        while remainder.degree() >= dividend.degree() and remainder != Polynomial([0]):
            from Rational_model.polynomial_utils import make_monomial
            multiplier = make_monomial(remainder.degree() - dividend.degree(),
                                        remainder.coefficient * remainder.monomial_coefficients[remainder.degree()]
                                       / dividend.coefficient / dividend.monomial_coefficients[dividend.degree()])
            quotient += multiplier
            remainder -= dividend * multiplier

        return [quotient, remainder]

    def factorize(self):
        rational_roots = self.find_rational_roots()
        factors = []
        polynomial = self.copy()

        for root in rational_roots:
            factor = Polynomial([(-1) * root, 1])
            factors.append(factor)

            quotient, remainder = polynomial.divide_with_remainder(factor)
            if remainder != Polynomial([0]):
                raise Exception("Division of polynomial by (x - [root]) gives nonzero remainder")
            polynomial = quotient

        if polynomial.degree() > 0:
            factors.append(polynomial)
        from Rational_model.product import Product
        return Product(factors, polynomial.coefficient)

    # Polynomial is always stored in a standard form, so no simplification needed
    def simplify(self):
        pass