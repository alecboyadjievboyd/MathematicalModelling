import abc
from enum import Enum

# Enumerator for types of expressions
class ExpressionType(Enum):
    MONOMIAL = 1
    SUM = 2
    PRODUCT = 3

# Abstract class of expression
class Expression(abc.ABC):

    def __init__(self, type):
        self.expression_type = type
    
    @abc.abstractmethod
    def __str__(self):
        pass

# Class for monomial expression
class Monomial(Expression):

    def __init__(self, coefficient, exponent):
        super().__init__(ExpressionType.MONOMIAL)
        self.coefficient = coefficient
        self.exponent = exponent

    def __str__(self):
        string_expression = ""
        string_expression += str(self.coefficient) if self.coefficient != 1 or self.exponent == 0 else ""

        match self.exponent:
            case 0:
                pass
            case 1:
                string_expression += "x"
            case _:
                string_expression += "x^" + str(self.exponent)

        return string_expression

# Class for sum of expressions
class Sum(Expression):

    def __init__(self, terms):
        super().__init__(ExpressionType.SUM)
        self.terms = terms

    def __str__(self):
        string_expression = str(self.terms[0])
        for term in self.terms[1:]:
            string_expression += " + " + str(term)
        return string_expression
            
# Class for products of expressions
class Product(Expression):

    def __init__(self, factors):
        super().__init__(ExpressionType.PRODUCT)
        self.factors = factors
    
    def put_brackets(self, expression):
        return "(" + str(expression) + ")" if expression.expression_type == ExpressionType.SUM else str(expression)
    
    def __str__(self):
        string_expression = self.put_brackets(self.factors[0])
        for factor in self.factors[1:]:
            string_expression += " * " + self.put_brackets(factor)
        return string_expression

# x^2
expr1 = Monomial(1, 2)
print(expr1)

# 2x + 4
expr2 = Sum([ Monomial(2, 1), Monomial(4, 0) ])
print(expr2)

# 3x * 2x
expr3 = Product([ Monomial(3, 1), Monomial(2, 1) ])
print(expr3)

# (x + 3) * x^3
expr4 = Product([ Sum([ Monomial(1, 1), Monomial(3, 0) ]), Monomial(1, 3) ])
print(expr4)

# 0x^4
expr5 = Monomial(0, 4)
print(expr5)

# 8
expr6 = Monomial(8, 0)
print(expr6)

# (8 + 7) * 3
expr7 = Product([ Sum([ Monomial(8, 0), Monomial(7, 0) ]), Monomial(3, 0) ])
print(expr7)

# x * ( x * (x * (x+1))) 
expr8 = Product([ Monomial(1, 1), Product([ Monomial(1, 1), Product([ Monomial(1, 1), Sum([ Monomial(1, 1), Monomial(1, 0)])])])])
print(expr8)