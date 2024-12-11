# Parser

# made for polynomials and integer coefficients
from Model.constant import Constant
from Model.variable import Variable
from Model.exponential import Exponential
from Model.product import Product
from Model.sum import Sum

def const(input,start):
    
    j = 0

    while (j <len(input)):
        if (input[j]<= '9' and input[j] >= '0'):
            j += 1
        else:
            break

    return input[:j], j + start

def bracket(input,start):
    bracket = 0
    j = 0
    while (j < len(input)):
        if (input[j] == '('):
            bracket += 1
        elif (input[j] == ')' and bracket == 1):
            return input[0:j+1], j+1 + start
        elif (input[j] == ')'):
            bracket -= 1
        j += 1
            

def factor(input):

    bracket = 0
    length =  0

    if (input == ""):
        return
    
    start = 0

    while (start < len(input)):
        if (input[start] >= '0' and input[0] <= '9'):

            a, c1 = const(input, start) 
            if (input[c1] == '^'):
                start = c1 + 1
            else:
                return Product(exp(input[:c1]), factor(input[c1:]))
        
        elif (input[start] == '('):

            a, c1 = bracket(input[start:],start)

            if (input[c1] == '^'):
                start = c1 + 1
            else:
                return(Product(exp(input[:c1]), factor(input[c1:])))
      
        elif (input[start] == 'x'):

            if (input[start +3] == '^'):
                start += 4

            else:
                return(Product(exp(input[:c1]), factor(input[c1:])))
            
        

        elif (input[start] == 's' or input[start] == 't' or input[start] =='c'):
            start += 3
                
    
    return exp(start)

    
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
            return Exponential(factor(input[:i]), expression(input[(i+1):]))
        
    return basic(input)



def basic():
    func = input[:3]
    if (not (func == "sin" or func == "cos" or func == "tan")):
        return unit(input)
    return elem(input, func)

def unit():
    pass

def elem():
    pass
     

def term(input):

    if (input == ""):
        return
    
    if (input[0] == '('):
        input = input[1:len(input)-1]

    bracket = 0 # we check brackets to ensure we are in the "top level" of the expression

    for i in range(len(input)):
        if (input[i] == '('):
            bracket += 1
        elif (input[i] == ')'):
            bracket -= 1
        elif (input[i] == '*' and bracket == 0):
            return Product([factor(input[:i]), term(input[(i+1):])])
        elif (input[i] == '/' and bracket == 0): # if we find a division sign at the top level, we split and check if we reach another multiplication sign at the top level
            slash_index = i
            factor1 = input[:slash_index]
            input_rest = input[slash_index+1:]
            for j in range(len(input_rest)):
                if (input_rest[j] == '('):
                    bracket += 1
                elif (input_rest[j] == ')'):
                    bracket -= 1
                elif (input_rest[j] == '*' and bracket == 0):
                    factor2 = input_rest[:j]
                    term_last = input_rest[j+1:]
                    return Product([factor(factor1), Exponential(factor(factor2), Constant(-1)), term(term_last)])
            return Product([factor(input[:i]), Exponential(factor(input[(i+1):]), Constant(-1))]) # if we don't find another multiplication sign, we return the division of the two factors
    
    return factor(input)


# make sure input has no spaces use input = input.replace(" ", "")

def expression(input): 
    c = 0

    if (input == ""):
        return
    
    if (input[0] == '('):
        input = input[1:len(input)-1]

    bracket = 0
    for i in range(len(input)):
        if (input[i] == '('):
            bracket += 1
        elif (input[i] == ')'):
            bracket -= 1
        elif (input[i] == '+' and bracket == 0):
            return Sum([term(input[:i]), expression(input[(i+1):])])
        elif (input[i] == '-' and bracket == 0):
            return Sum([term(input[:i]), Product([Constant(-1), expression(input[(i+1):])])])
    
    return term(input)


user_input = str(input("please input in ASCII math"))
user_input = user_input.replace(" ", "")
x = expression(user_input)

print(x)



""" 
def factor(input):

    if (input == ""):
        return
    
    if (input[0] == '('):
        return expression(input)
    
    else:
        l = []
        j = 0
        while (j < len(input)): 
            if (input[j] == 'x'):
                j+=2
                a = input[j]
                if (j+1 < len(input)):
                    if (input[j+1] == '^'):
                        j += 3
                        counter = 0
                        bracket = 1 
                        while (bracket > 0):
                            if (input[j+counter] == '('):
                                bracket += 1                            
                            elif(input[j+counter] == ')'):
                                bracket -= 1

                            counter += 1
                            
                        l.append(Exponential(Variable(a), expression(input[j:j+counter])))
                        j += counter
                        continue
                        
                l.append(Variable(a))

            elif (input[0]<= '9' and input[0] >= '0'):
                t = const(input)
                j += t[1]

                if (j+1 < len(input)):
                    if (input[j+1] == '^'):
                        j += 3
                        counter = 0
                        bracket = 1 
                        while (bracket > 0):
                            if (input[j+counter] == '('):
                                bracket += 1                            
                            elif(input[j+counter] == ')'):
                                bracket -= 1

                            counter += 1

                        l.append(Exponential(Constant(t[0]), expression(input[j:j+counter])))
                        j += counter
                        continue
                        
                l.append(Constant(t[0]))
                
            j += 1
        
        if (len(l) > 1):
            return Product(l)
        else:
            return l[0] 
"""

