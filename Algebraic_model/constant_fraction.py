import math


# Constant fraction with integer numerator and denominator.
# Used as coefficient for all the expressions
class ConstantFraction:
    def __init__(self, numerator, denominator = 1):
        # Checking that numerator and denominator are integers
        if type(numerator) != int or type(denominator) != int:
            raise TypeError('Numerator and Denominator must be integers')

        self.numerator = numerator
        self.denominator = denominator

        self.normalize()

    # Transform fraction to the normal form - positive denominator, relatively prime numerator and denominator.
    # If numerator is zero, then denominator has to be 1.
    def normalize(self):
        if self.denominator == 0:
            raise ValueError('Denominator of a constant cannot be 0')

        if self.denominator < 0:
            self.numerator *= -1
            self.denominator *= -1

        gcd = math.gcd(self.numerator, self.denominator)
        self.numerator //= gcd
        self.denominator //= gcd

    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)
        else:
            return f'({self.numerator}/{self.denominator})'

    # Comparing
    def __eq__(self, other):
        if type(other) != ConstantFraction and type(other) != int:
            return NotImplemented

        if type(other) == int:
            return self.denominator == 1 and self.numerator == other
        else:
            return self.numerator == other.numerator and self.denominator == other.denominator

    # Add two constants
    def __add__(self, other):
        # Raise an error if adding non-constant to a constant is attempted
        if type(other) != ConstantFraction:
            return NotImplemented

        numerator = self.numerator * other.denominator + self.denominator * other.numerator
        denominator = self.denominator * other.denominator
        return ConstantFraction(numerator, denominator)

    # Subtract constant from a constant
    def __sub__(self, other):
        # Raise an error if adding non-constant to a constant is attempted
        if type(other) != ConstantFraction:
            return NotImplemented

        numerator = self.numerator * other.denominator - self.denominator * other.numerator
        denominator = self.denominator * other.denominator
        return ConstantFraction(numerator, denominator)

    # Multiply two constants
    def __mul__(self, other):
        if type(other) != ConstantFraction:
            return NotImplemented

        numerator = self.numerator * other.numerator
        denominator = self.denominator * other.denominator
        return ConstantFraction(numerator, denominator)

    # Divide a constant by a constant
    def __truediv__(self, other):
        if type(other) != ConstantFraction:
            return NotImplemented

        numerator = self.numerator * other.denominator
        denominator = self.denominator * other.numerator
        return ConstantFraction(numerator, denominator)

    # Exponentiate constant to a positive integer power
    def __pow__(self, other):
        if type(other) != int or other < 0:
            return NotImplemented

        numerator = self.numerator ** other
        denominator = self.denominator ** other
        return ConstantFraction(numerator, denominator)
