from enum import Enum


# Enumerator for types of expressions
class RationalExpressionType(Enum):
    MONOMIAL = 1
    SUM = 2
    PRODUCT = 3
    QUOTIENT = 4
    POLYNOMIAL = 5
