# Parser

# made for polynomials and integer coefficients
from Model.constant import Constant
from Model.variable import Variable
from Model.exponential import Exponential
from Model.product import Product
from Model.sum import Sum

def const(input):
    
    j = 0

    for j in range(len(input)):
        if (input[j]<= '9' and input[j] >= '0'):
            j += 1

    return input[0:j], j

 
def factor(input):

    if (input == ""):
        return
    
    if (input[0] == '('):
        return expression(input)
    
    else:
        l = []
        j = 0
        while (j < len(input)):  #python makes me sad could not use for loop in this place causes error
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
    

     
def term(input):
    c = 0

    if (input == ""):
        return
    
    if (input[0] == '('):
        input = input[1:len(input)-1]

    for i in range(len(input)):            
        if (input[i] == '*'):
            return Product([factor(input[:i]), term(input[(i+1):])])
    
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
    
    return term(input)


user_input = str(input("please input in ASCII math"))
user_input = user_input.replace(" ", "")
x = expression(user_input)

print(x)



