from Model.expression_type import ExpressionType
from Model.constant import Constant
from Model.constant import ConstantType
from Model.exponential import Exponential
from Model.logarithm import Logarithm
from Model.sum import Sum
from Model.variable import Variable


# Here we define three minimal hollow rules that check if an expression is undefined.
# Several examples of usage of undefined check function on expressions are given.


# Checks if an expression is an undefined quotient with denominator zero. An expression is undefined if it is an
# exponential with base zero and exponent a negative integer.
def division_by_zero(expression):
    if expression.expression_type != ExpressionType.EXPONENTIAL:
        return False
    base = expression.base
    exponent = expression.exponent

    return ((base.expression_type == ExpressionType.CONSTANT and base.constant_type == ConstantType.INTEGER and
             base.value == 0) and
            (exponent.expression_type == ExpressionType.CONSTANT and exponent.constant_type == ConstantType.INTEGER and
             exponent.value <= 0))


# Check if an expression is an undefined exponential with the negative bases. An expression is undefined if it is an
# exponential with base negative integer and exponent not an integer.
def exponential_negative_base(expression):
    if expression.expression_type != ExpressionType.EXPONENTIAL:
        return False
    base = expression.base
    exponent = expression.exponent

    return (base.expression_type == ExpressionType.CONSTANT and base.constant_type == ConstantType.INTEGER and
            base.value < 0 and
            (exponent.expression_type != ExpressionType.CONSTANT or
             (exponent.expression_type == ExpressionType.CONSTANT and exponent.constant_type != ConstantType.INTEGER)))


# Checks if an expression is undefined logarithm. The expression is undefined if it is a logarithm with non-positive
# integer base or non-positive integer argument
def negative_logarithm(expression):
    if expression.expression_type != ExpressionType.LOGARITHM:
        return False
    base = expression.base
    argument = expression.argument

    return ((base.expression_type == ExpressionType.CONSTANT and base.constant_type == ConstantType.INTEGER and
             base.value <= 0) or
            (argument.expression_type == ExpressionType.CONSTANT and argument.constant_type == ConstantType.INTEGER and
             argument.value <= 0))


# Checks if an expression is undefined according to at least one of three rules.
def undefined(expression):
    return (division_by_zero(expression) or exponential_negative_base(expression)
            or negative_logarithm(expression))


# Checking which of 1^1, 0^1, 1^0, 0^0 is undefined - "division by zero"
expr1 = Exponential(Constant(1), Constant(1))
expr2 = Exponential(Constant(0), Constant(1))
expr3 = Exponential(Constant(1), Constant(0))
expr4 = Exponential(Constant(0), Constant(0))
print(f'{expr1} undefined is {undefined(expr1)}')
print(f'{expr2} undefined is {undefined(expr2)}')
print(f'{expr3} undefined is {undefined(expr3)}')
print(f'{expr4} undefined is {undefined(expr4)}\n')


# Checking which of 1^(-1), e^(-6), 0^(-1), 0^(-6) is undefined - division by zero
expr1 = Exponential(Constant(1), Constant(-1))
expr2 = Exponential(Constant('e'), Constant(-6))
expr3 = Exponential(Constant(0), Constant(-1))
expr4 = Exponential(Constant(0), Constant(-6))
print(f'{expr1} undefined is {undefined(expr1)}')
print(f'{expr2} undefined is {undefined(expr2)}')
print(f'{expr3} undefined is {undefined(expr3)}')
print(f'{expr4} undefined is {undefined(expr4)}\n')


# Checking which of (-1)^(1+1), (-1)^e, (-1)^(-5) is undefined - exponent with negative base
expr1 = Exponential(Constant(-1), Sum([Constant(1), Constant(1)]))
expr2 = Exponential(Constant(-1), Constant('e'))
expr3 = Exponential(Constant(-1), Constant(-5))
print(f'{expr1} undefined is {undefined(expr1)}')
print(f'{expr2} undefined is {undefined(expr2)}')
print(f'{expr3} undefined is {undefined(expr3)}\n')


# Checking which of log_pi(1), log_3(x^2), log_(-1)(x), log_0(0), log_5(-3) is undefined
expr1 = Logarithm(Constant('pi'), Constant(1))
expr2 = Logarithm(Constant(3), Exponential(Variable(1), Constant(2)))
expr3 = Logarithm(Constant(-1), Variable(1))
expr4 = Logarithm(Constant(0), Constant(5))
expr5 = Logarithm(Constant(5), Constant(-3))
print(f'{expr1} undefined is {undefined(expr1)}')
print(f'{expr2} undefined is {undefined(expr2)}')
print(f'{expr3} undefined is {undefined(expr3)}')
print(f'{expr4} undefined is {undefined(expr4)}')
print(f'{expr5} undefined is {undefined(expr5)}')