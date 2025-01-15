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

    def copy(self):
        return ConstantFraction(self.numerator, self.denominator)
    
    def get_numerator(self):
        return self.numerator
    
    def get_denominator(self):
        return self.denominator

    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)
        else:
            return f'{self.numerator}/{self.denominator}'

    # Comparing two constants or a constant with an integer
    def __eq__(self, other):
        if not isinstance(other, ConstantFraction) and not isinstance(other, int):
            return NotImplemented

        if type(other) == int:
            return self.denominator == 1 and self.numerator == other
        else:
            return self.numerator == other.numerator and self.denominator == other.denominator

    def __lt__(self, other):
        if isinstance(other, int):
            return self.numerator < other * self.denominator
        elif isinstance(other, ConstantFraction):
            return self.numerator * other.denominator < other.numerator * self.denominator
        else:
            return NotImplemented

    def __le__(self, other):
        if not(isinstance(other, ConstantFraction) or isinstance(other, int)):
            return NotImplemented

        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        if not (isinstance(other, ConstantFraction) or isinstance(other, int)):
            return NotImplemented

        return not self.__lt__(other)

    def __ge__(self, other):
        if not (isinstance(other, ConstantFraction) or isinstance(other, int)):
            return NotImplemented

        return not self.__gt__(other) or self.__eq__(other)

    # Add a constant or an integer to the constant
    def __add__(self, other):
        # Convert integer into a constant
        if isinstance(other, int):
            # Convert integer into a constant
            other = ConstantFraction(other)
        elif not isinstance(other, ConstantFraction):
            # Only an integer or a constant can be added to a constant
            return NotImplemented

        numerator = self.numerator * other.denominator + self.denominator * other.numerator
        denominator = self.denominator * other.denominator
        return ConstantFraction(numerator, denominator)

    # Subtract a constant or an integer from the constant
    def __sub__(self, other):
        if isinstance(other, int):
            # Convert integer into a constant
            other = ConstantFraction(other)
        elif not isinstance(other, ConstantFraction):
            # Only an integer or a constant can be added to a constant
            return NotImplemented

        numerator = self.numerator * other.denominator - self.denominator * other.numerator
        denominator = self.denominator * other.denominator
        return ConstantFraction(numerator, denominator)

    # Multiply two constants fractions or constant fraction by integer
    def __mul__(self, other):
        if type(other) == ConstantFraction:
            # ConstantFraction * ConstantFraction
            numerator = self.numerator * other.numerator
            denominator = self.denominator * other.denominator
            return ConstantFraction(numerator, denominator)
        elif type(other) == int:
            # ConstantFraction * integer
            return ConstantFraction(self.numerator * other, self.denominator)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    # Divide a constant by a constant
    def __truediv__(self, other):
        if isinstance(other, int):
            other = ConstantFraction(other)
        elif not isinstance(other, ConstantFraction):
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

    #
