import abc
from enum import Enum

# Enumerator for types of expressions
class ExpressionType(Enum):
    VARIABLE = 1
    CONSTANT = 2
    SUM = 3
    PRODUCT = 4
    EXPONENTIAL = 5

# Abstract class of expression
class Expression(abc.ABC):

    def __init__(self, type):
        self.expression_type = type
    
    def put_brackets(self, expression):
        if (expression.expression_type == ExpressionType.SUM or expression.expression_type == ExpressionType.PRODUCT):
            return "(" + str(expression) + ")"
        else:
            return str(expression)
    
    @abc.abstractmethod
    def __str__(self):
        pass

# Singular variables, without constants or exponents. Terminal expression.
class Variable(Expression):

    def __init__(self, index):
        super().__init__(ExpressionType.VARIABLE)
        self.index = index

    def __str__(self):
        return "x" + str(self.index)

# Integer constant. Terminal expression.
class Constant(Expression):

    def __init__(self, value):
        super().__init__(ExpressionType.CONSTANT)
        self.value = value

    def __str__(self):
        return str(self.value)

# Sum of at least two expressions (terms)
class Sum(Expression):

    def __init__(self, terms):
        super().__init__(ExpressionType.SUM)
        self.terms = terms

    def __str__(self):
        string_expression = str(self.terms[0])
        for term in self.terms[1:]:
            string_expression += " + " + str(term)
        return string_expression
            
# Products of at least two expressions (factors)
class Product(Expression):

    def __init__(self, factors):
        super().__init__(ExpressionType.PRODUCT)
        self.factors = factors
    
    def __str__(self):
        string_expression = self.put_brackets(self.factors[0])
        for factor in self.factors[1:]:
            string_expression += " * " + self.put_brackets(factor)
        return string_expression
    
# Exponential function with an expression as a base and exponent
class Exponential(Expression):

    def __init__(self, base, exponent):
        super().__init__(ExpressionType.EXPONENTIAL)
        self.base = base
        self.exponent = exponent
    
    def __str__(self):
        return self.put_brackets(self.base) + "^" + self.put_brackets(self.exponent)


# 8
expr1 = Constant(8)
print(expr1)

# x
expr2 = Variable(1)
print(expr2)

# 2x + 4
expr3 = Sum([ Product([ Constant(2), Variable(1) ]), Constant(4) ])
print(expr3)

# 3x * 2x
expr4 = Product([ Product([Constant(3), Variable(1)]), Product([ Constant(2), Variable(1) ]) ])
print(expr4)

# x^2
expr5 = Exponential(Variable(1), Constant(2))
print(expr5)

# 0x^4
expr6 = Product([ Constant(0), Exponential(Variable(1), Constant(4)) ])
print(expr6)

# (8 + 7) * 3
expr7 = Product([ Sum([ Constant(8), Constant(7) ]), Constant(3) ])
print(expr7)

# x * ( x * (x * (x+1))) 
expr8 = Product([ Variable(1), Product([ Variable(1), Product([ Variable(1), Sum([ Variable(1), Variable(1) ]) ]) ]) ])
print(expr8)