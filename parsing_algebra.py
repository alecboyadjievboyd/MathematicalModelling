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
    

def constant(input):
    numer = 1
    numer_index = 0
    denom = 1

    i = 0
    bool_num = False

    while (i < len(input)):
        if (input[i] >='0' and input[i] <= '9'):
            i += 1
        elif (input[i] == '/'):
            numer = input[:i]
            bool_num = True
            i += 1
            numer_index = i
        else: 
            break

    if bool_num:
        denom = input[numer_index:i]
    else:
        numer = input[:i]            

    return int(numer), int(denom), i


def monomial(input):
    if (input[0] == '(' and input[-1] == ')'):
        return express_alg(input[1:len(input)-1])
    
    if (input[0] >= '0' and input[0] <= '9'):
        numer,denom,i = constant(input)
        return Polynomial([ConstantFraction(numer, denom)])
    
    elif (input[0] == 'x'):
        numer = 1
        if (len(input) != 1):
            numer, denom, i = constant(input[2:])
        
        return make_monomial(numer)

def fraction(input):

    if (input == ""):
        return

    bracket = 0 # we check brackets to ensure we are in the "top level" of the expression

    for i in range(len(input)):
        if (input[i] == '('):
            bracket += 1
        elif (input[i] == ')'):
            bracket -= 1
        elif (input[i] == '/' and bracket == 0):
            return Fraction(monomial(input[:i]), fraction(input[(i+1):]))
        
    return monomial(input)


def term(input):

    if (input == ""):
        return

    bracket = 0 # we check brackets to ensure we are in the "top level" of the expression
    i = 0

    if (input[0] == "-"):
        return Product([Polynomial([ConstantFraction(-1)]), express_alg(input[1:])])

    if ((input[0] >= '0' and input[0] <= '9') and check_constant(input)):
            numer,denom,i = constant(input)

            if (i < len(input)):
                return Product([Polynomial([ConstantFraction(numer, denom)]),term(input[i:])])
            else:
                return Polynomial([ConstantFraction(numer,denom)])
          
    for i in range(len(input)):
        if (input[i] == '('):
            bracket += 1
        elif (input[i] == ')'):
            bracket -= 1
        elif (input[i] == '*' and bracket == 0):
            return Product([fraction(input[:i]), term(input[(i+1):])])
        
    return fraction(input)


def express_alg(input):
    
    c = 1
    i = 0

    if (input == ""):
        return
        
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
                return Sum([term(input[:i]), express_alg(input[i:])])
    
    return term(input)

#input

if __name__ == '__main__':
    user_input = str(input("please input in ASCII math "))
    user_input = user_input.replace(" ", "")
    x = express_alg(user_input)
    print(x)
