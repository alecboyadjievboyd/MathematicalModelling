from parsing import expression
from parsing_algebra import express_alg


print("Which model would you like to use")
print("1. Analytic Model  2. Rational Model")
model = int(input())


if (model == 1):

    print("Which operation would you like to do")
    print("1. Differentiate  2. Simplify")
    option = int(input())
    print("Enter the expression")
    
    user_input = input()
    parsed_input = expression(input)
    parsed_input = user_input.replace(" ", "")

    if (option == 1):
        pass
    elif (option == 2):
        pass
    else:
        print("Invalid option")
elif (model == 2):
    
    print("Which operation would you like to do")
    print("1. Simplify  2. Simplify and factorize  3. Find roots")
    print("4. Divide with remainder  5. GCD")
    option = int(input())

    
    if (option == 1):
        pass
    elif (option == 2):
        pass
    elif (option == 3):
        pass
    elif (option == 4):
        pass
    elif (option == 5): 
        pass     
    else:
        print("Invalid option")

else:
    print("Invalid input enter correct model number")