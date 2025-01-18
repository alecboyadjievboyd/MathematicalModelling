#Algebraic Parser

from Rational_model.polynomial import Polynomial
from Rational_model.constant_fraction import ConstantFraction
from Rational_model.fraction import Fraction
from Rational_model.product import Product
from Rational_model.sum import Sum
from Rational_model.polynomial_utils import make_monomial

def check_constant(input):
    ans = True
    i = 0
    while (i < len(input)):
        if (input[i] >='0' and input[i] <= '9'):
            i += 1
        elif (input[i] =='*'):
            ans = False
            break
        elif (input[i] == '/'):
            if (input[i+1] >= '0' and input[i+1] <= '9'):
                break  
            else:
                ans = False
                break        
        else: 
            break
    

def const(input):
    
    i = 0
    while (i < len(input)):
        if (input[i] =='/' or (input[i] >= '0' and input[i] <= '9')):
            i += 1
        else:
            break
    
    return i
    

def monomial(input):

    if (input[0] == "-"):
        return Product([Polynomial([ConstantFraction(-1)]), express_alg(input[1:])])
    
    if (input[0] == '(' and input[-1] == ')'):
        return express_alg(input[1:len(input)-1])
    
    if (input[0] >= '0' and input[0] <= '9'):
        return Polynomial([ConstantFraction(int(input), 1)])
    
    elif (input[0] == 'x'):
        numer = 1
        if (len(input) != 1):
            return make_monomial(int(input[2:]))
        else:
            return make_monomial(1)

def fraction(input):

    bracket = 0 # we check brackets to ensure we are in the "top level" of the expression

    for i in range(len(input)):
        if (input[i] == '('):
            bracket += 1
        elif (input[i] == ')'):
            bracket -= 1
        elif (input[i] == '/' and bracket == 0):
            return Fraction(monomial(input[:i]), fraction(input[(i+1):]))
        
    return monomial(input)

def implicit(input):

    bracket = 0

    for i in range(len(input)):
        if (input[i] == '('):
            bracket += 1
        elif (input[i] == ')'):
            bracket -= 1
        elif ((input[i] >='0' and input[i] <= '9') and bracket == 0):
            j = const(input[i:])
            if ((i +j) < len(input)):
                return Product([fraction(input[:i+j]), term(input[i+j:])])
            break
               
    return fraction(input)        

def term(input):

    bracket = 0 # we check brackets to ensure we are in the "top level" of the expression
    i = 0

    for i in range(len(input)):
        if (input[i] == '('):
            bracket += 1
        elif (input[i] == ')'):
            bracket -= 1
        elif (input[i] == '*' and bracket == 0):
            return Product([implicit(input[:i]), term(input[(i+1):])])
        
    return implicit(input)


def express_alg(input):
    
    c = 1
    i = 0
        
    bracket = 0
    
    for i in range(len(input)):
        if (input[i] == '('):
            bracket += 1
        elif (input[i] == ')'):
            bracket -= 1
        elif (input[i] == '+' and bracket == 0):
            return Sum([term(input[:i]), express_alg(input[i+1:])])
        elif (input[i] == '-' and bracket == 0):
            if (i != 0):
                if (input[i-1] != '/' and input[i-1] != '*' and input[i-1] != '^'):        
                    return Sum([term(input[:i]), express_alg(input[i:])])
    
    return term(input)

#input

if __name__ == '__main__':
    user_input = str(input("please input in ASCII math "))
    user_input = user_input.replace(" ", "")
    x = implicit(user_input)
    print(x)
