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
    SINE = 9
    COSINE = 10
    TANGENT = 11
    ARCSINE = 12
    ARCCOSINE = 13
    ARCTANGENT = 14
    EXP = 15