# Parser

from Model.integer import Integer
from Model.variable import Variable
from Model.exponential import Exponential
from Model.product import Product
from Model.sum import Sum
from Model.sine import Sine
from Model.cosine import Cosine
from Model.tangent import Tangent
from Model.logarithm import Logarithm
from Model.arccosine import Arccosine
from Model.arcsine import Arcsine
from Model.arctangent import Arctangent
from Model.pi import Pi
from Model.euler import Euler


def const(input):
    
    j = 0
    while (j <len(input)):
        if (input[j]<= '9' and input[j] >= '0'):
            j += 1
        else:
            break

    return j


def bracket(input):
    bracket = 0
    j = 0
    while (j < len(input)):
        if (input[j] == '('):
            bracket += 1
        elif (input[j] == ')' and bracket == 1):
            return j+1
        elif (input[j] == ')'):
            bracket -= 1
        j += 1


def log(input):
    j = 0

    if (input[0] == '('):
        j += bracket(input)            
    elif (input[0] == 'x'):
        j += 2 + const(input[2:])
    else:
        j += const(input)
    
    return j



def factor(input):

    if (input == ""):
        return
    
    start = 0

    while (start < len(input)):

        # This part is to check if we have reached a '^' if not we are done and we need to return
        # We shouldn't stop if we ended the last part at trig function so we check for that as well

        if (input[start] == '^'): 
            start += 1 

        elif (start != 0 and input[start-2] == 'g'):
            start += log(input[start:])

        elif (start != 0 and not (input[start-1] == 'n' or input[start-1] == 's')):
            return Product([exp(input[:start]), factor(input[start:])])
        
        # This part is to check what kind of thing we have    
                                
        if (input[start] >= '0' and input[start] <= '9'):

            start +=  const(input[start:]) 

        elif (input[start] == 'e'):
            start += 1
        
        elif (input[start] == 'p'):
            start += 2
        
        elif (input[start] == '('):

            start += bracket(input[start:])
      
        elif (input[start] == 'x'):
            start += 2 + const(input[start+2:])   

        elif (input[start] == 's' or input[start] == 't' or input[start] =='c'):
            start += 3

        elif (input[start] == 'l'):
            start += 4
            
        elif (input[start] == 'a'):
            start += 6
                 
    return exp(input)

    
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
            return Exponential(basic(input[:i]), exp(input[(i+1):])) 
        
    return basic(input)


def basic(input):
    func = input[:3]
    if (not (func == "sin" or func == "cos" or func == "tan" or func == "arc" or func == "log")):
        return unit(input)
    else:
        if (func == "arc"):
            func = input[:6]
            return elem(input[6:], func)
        return elem(input[3:], func)


def unit(input):

    if (input == ""):
        return
    elif (input[0] == '(' and input[-1] == ')'):
        return expression(input[1:len(input)-1])
    elif (input[0] == 'x'):
        return Variable(input[2:])
    elif (input[0] == 'e'):
        return  Euler()
    elif (input[0] == 'p'):
        return Pi()
    else:
        return Integer(int(input))


def elem(input, func):

    if (func == "arcsin"):
        return Arcsine(unit(input))    
    elif(func == "arccos"):
        return Arccosine(unit(input))
    elif (func == "arctan"):
        return Arctangent(unit(input))  
    elif (func == "sin"):
        return Sine(unit(input))
    elif (func == "cos"):
        return Cosine(unit(input))
    elif (func == "tan"):
        return Tangent(unit(input))
    elif (func == "log"):
        j = log(input[1:])
        return Logarithm(unit(input[1:j+1]),unit(input[j+1:]))
    else:
        return
     

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
            return Product([factor(input[:i]), Exponential(fraction(input[(i+1):]), Integer(-1))])
        
    return factor(input)


def term(input):

    if (input == ""):
        return

    bracket = 0 # we check brackets to ensure we are in the "top level" of the expression

    for i in range(len(input)):
        if (input[i] == '('):
            bracket += 1
        elif (input[i] == ')'):
            bracket -= 1
        elif (input[i] == '*' and bracket == 0):
            return Product([fraction(input[:i]), term(input[(i+1):])])
        
    return fraction(input)


def expression(input): 
    c = 0

    if (input == ""):
        return
    
    bracket = 0
    for i in range(len(input)):
        if (input[i] == '('):
            bracket += 1
        elif (input[i] == ')'):
            bracket -= 1
        elif (input[i] == '+' and bracket == 0):
            return Sum([term(input[:i]), expression(input[(i+1):])])
        elif (input[i] == '-' and bracket == 0):
            return Sum([term(input[:i]), Product([Integer(-1), expression(input[(i + 1):])])])
    
    return term(input)


#make sure input has no spaces use input = input.replace(" ", "")

user_input = str(input("please input in ASCII math "))
user_input = user_input.replace(" ", "")

x = expression(user_input)
print(x)


# recursion depth tester before stack overflow

"""

n = 141
word = "x_1*x_2"
for i in range(3, n+3):
    word = "("+ word+")*x_" + str(i)

x = term(word)
print(x)
"""
