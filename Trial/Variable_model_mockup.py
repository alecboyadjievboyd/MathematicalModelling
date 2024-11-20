import abc
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
    
    def derivative(self, differential):
        if self.index == differential.index:
            return Constant(1)
        else:
            return Constant(0)

# Integer constant. Terminal expression.
class Constant(Expression):

    def __init__(self, value):
        super().__init__(ExpressionType.CONSTANT)
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def derivative(self, differential):
        return Constant(0)

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
    
    def derivative(self, differential):   
        return Sum( tuple(term.derivative(differential) for term in self.terms) )
            
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
    
#     def derivative(self, differential): #outputs derivative of f*g*h as f'*g*h + g'*f*h + h'*f*g
#         return Sum(tuple(
#             Product((self.factors[i].derivative(differential),) + tuple(self.factors[j] for j in range(len(self.factors)) if j!=i))
#             for i in range(len(self.factors))
#         ))
    def derivative(self, differential): #outputs derivative of f*g*h as f'*g*h + f*g'*h + f*g*h'
        return Sum(tuple(
            Product(
                tuple(self.factors[j] for j in range(len(self.factors)) if j<i) 
                + (self.factors[i].derivative(differential),) 
                + tuple(self.factors[j] for j in range(len(self.factors)) if j>i)
            ) 
            for i in range(len(self.factors))
        ))
    
# Exponential function with an expression as a base and exponent
class Exponential(Expression):

    def __init__(self, base, exponent):
        super().__init__(ExpressionType.EXPONENTIAL)
        self.base = base
        self.exponent = exponent
    
    def __str__(self):
        return self.put_brackets(self.base) + "^" + self.put_brackets(self.exponent)
    
    def derivative(self, differential):
        return Product((self, 
                      Sum(( Product((self.exponent.derivative(differential), ln(self.base))),
                          Product((self.exponent, Exponential(self.base, Constant(-1)), self.base.derivative(differential)))                         
                         ))
                      ))
    

class ln(Expression): #Tim here, I had to add this as it is needed when differentiating Exponential. Feel free to change stuff.
    def __init__(self, argument):
        super().__init__(ExpressionType.NATURALLOG)
        self.argument = argument
        
    def __str__(self):
        return f'ln({self.argument})'
    
    def derivative(self, differential):
        return Product((Exponential(self.argument, Constant(-1)), self.argument.derivative(differential)))
    
class GeneralMultivar(Expression):
    def __init__(self, symbol:str):
        super().__init__(ExpressionType.GENERALMULTIVAR)
        self.symbol = symbol
    
    def __str__(self):
        return self.symbol + "(x)"
    
    def derivative(self, differential):
        return GeneralMultivar(f"d{self.symbol}/d{differential}") # df/dx1
        
class GeneralSinglevar(Expression):
    def __init__(self, symbol:str, argument):
        super().__init__(ExpressionType.GENERALSINGLEVAR)
        self.symbol = symbol
        self.argument = argument

    def __str__(self):
        return self.symbol + '(' + self.argument.__str__() + ')'
    
    def derivative(self, differential):
            return Product((GeneralSinglevar(self.symbol + "\'", self.argument), self.argument.derivative(differential))) # f'
        
        
def D(function, differential = Variable(1)):
    return function.derivative(differential)


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

# dx/dy
print( Variable(1).derivative(Variable(2)))

# dx/dx
print( Variable(1).derivative(Variable(1)))

# derivative of constant
print(Constant(23).derivative(Variable(1)))

# general multivariable functions
genf = GeneralMultivar('f')
geng = GeneralMultivar('g')
genh = GeneralMultivar('h')
print(genf)
print(Exponential(genf, Sum((geng, genh))))
print(genf.derivative(Variable(1)))
print(genf.derivative(Variable(1)).derivative(Variable(2)))

# the function D
print(D(genf, Variable(1)))
print(D(D(genf, Variable(1)), Variable(2)))
print(D(genf))


# Derivative of sum
print(D(Sum((genf, geng, genh))))

# Derivative of product
print(D(Product((genf, geng, genh))))

# Derivative of exponential
print(D(Exponential(genf, genh)))
print(D(Exponential(Variable(1),Constant(-1))))
print(D(Exponential(Variable(1),Variable(1))))

# Problem with derivative of exponential
print(  D(Exponential(Constant(0),Variable(1)))  )

# ln
print( ln(Variable(1)) )
print( D(ln(genf)))
print( D(ln(Variable(1))))

# general singlevariable function
print( GeneralSinglevar('cot', Variable(1)) )
print( D(GeneralSinglevar('cot', genf)) )
