from enum import Enum

# Enumerator for types of expressions
class ExpressionType(Enum):
    VARIABLE = 1
    CONSTANT = 2
    SUM = 3
    PRODUCT = 4
    EXPONENTIAL = 5
    NATURALLOG = 6
    GENERALMULTIVAR = 7
    GENERALSINGLEVAR = 8