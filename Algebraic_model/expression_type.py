from enum import Enum


# Enumerator for types of expressions
class ExpressionType(Enum):
    MONOMIAL = 1
    SUM = 2
    PRODUCT = 3
    QUOTIENT = 4
