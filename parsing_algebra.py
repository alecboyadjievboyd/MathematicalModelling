#Algebraic Parser

from Rational_model.polynomial import Polynomial
from Rational_model.constant_fraction import ConstantFraction
from Rational_model.fraction import Fraction
from Rational_model.product import Product
from Rational_model.sum import Sum
from Rational_model.exponential import Exponential
from Rational_model.polynomial_utils import make_monomial

def check_constant(input):

    i = 0

    if (input[0] == '-'):
        i = 1

    while (i < len(input)):
        if (input[i] >='0' and input[i] <= '9'):
            i += 1
    return int(input[:i])
    

def check_implicit(input):
    
    i = 0
    ans = True
    while (i < len(input)):

        if (input[i] >= '0' and input[i] <= '9'):
            ans = True
            i += 1

        elif(input[i] =='/' or input[i] == '-'):
            i += 1   
            ans = False 
            
        elif ((input[i] == 'x' or input[i] == '(') and ans):
            return i, True
        else:
            return i, False
    
    return i, False
    

def monomial(input):

    if (input[0] == "-"):
        return Product([Polynomial([ConstantFraction(-1)]), express_alg(input[1:])])
    
    if (input[0] == '(' and input[-1] == ')'):
        return express_alg(input[1:len(input)-1])
    
    if (input[0] >= '0' and input[0] <= '9'):
        return Polynomial([ConstantFraction(int(input), 1)])
    
    elif (input[0] == 'x'):
        return make_monomial(1)
        
def exp(input):

    bracket = 0
    if (input == ""):
        return
    for i in range(len(input)):
        if (input[i] == '('):
            bracket += 1
        elif (input[i] == ')'):
            bracket -= 1
        elif (input[i] == '^' and bracket == 0):
            return Exponential(monomial(input[:i]), check_constant(input[(i+1):])) 
        
    return monomial(input)

def fraction(input):

    bracket = 0 # we check brackets to ensure we are in the "top level" of the expression

    for i in range(len(input)):
        if (input[i] == '('):
            bracket += 1
        elif (input[i] == ')'):
            bracket -= 1
        elif (input[i] == '/' and bracket == 0):
            return Fraction(exp(input[:i]), fraction(input[(i+1):]))
        
    return exp(input)

def implicit(input):

    bracket = 0

    for i in range(len(input)):
        if (input[i] == '('):
            bracket += 1
        elif (input[i] == ')'):
            bracket -= 1
        elif ((input[i] >='0' and input[i] <= '9') and bracket == 0):
            j, split = check_implicit(input[i:])
            if ((i +j) < len(input) and split):
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
    x = express_alg(user_input)
    print(x)
