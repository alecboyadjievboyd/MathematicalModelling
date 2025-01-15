from Model.variable import Variable
from Rational_model.polynomial_utils import divide_with_remainder, polynomial_gcd
from parsing import expression
from parsing_algebra import express_alg


print("Which model would you like to use")
print("1. Analytic Model  2. Rational Model")
model = int(input())


if model == 1:

    print("Which operation would you like to do")
    print("1. Differentiate  2. Simplify")
    option = int(input())
    print("Enter the expression")
    
    user_input = input()
    parsed_input = expression(user_input.replace(" ", ""))

    if option == 1:
        print(parsed_input.derivative(Variable(1)))

    elif option == 2:
        print(parsed_input.pfsf())

    else:
        print("Invalid option")

elif model == 2:
    
    print("Which operation would you like to do")
    print("1. Simplify  2. Simplify and factorize  3. Find roots")
    print("4. Divide with remainder  5. GCD")
    option = int(input())
    
    if option == 1:
        print("Enter the expression")
        user_input = input()
        parsed_input = express_alg(user_input.replace(" ", ""))

        print(parsed_input.simplify())

    elif option == 2:
        print("Enter the expression")
        user_input = input()
        parsed_input = express_alg(user_input.replace(" ", ""))

        print(parsed_input.get_standard_form())

    elif option == 3:
        print("Enter the expression")
        user_input = input()
        parsed_input = express_alg(user_input.replace(" ", ""))
        parsed_input = parsed_input.simplify()

        roots = parsed_input.find_rational_roots()
        for root in roots:
            print(root, end='  ')

    elif option == 4:
        print("Enter the dividend:")
        user_input = input()
        dividend = express_alg(user_input.replace(" ", ""))
        print("Enter the divider:")
        user_input = input()
        divider = express_alg(user_input.replace(" ", ""))

        dividend = dividend.simplify()
        divider = divider.simplify()

        quotient, remainder = divide_with_remainder(dividend, divider)
        print("quotient: ", quotient)
        print("remainder: ", remainder)
    elif option == 5:
        print("Enter the first polynomial:")
        user_input = input()
        polynomial1 = express_alg(user_input.replace(" ", ""))
        print("Enter the second polynomial:")
        user_input = input()
        polynomial2 = express_alg(user_input.replace(" ", ""))

        polynomial1 = polynomial1.simplify()
        polynomial2 = polynomial2.simplify()

        print('gcd: ', polynomial_gcd(polynomial1, polynomial2))

    else:
        print("Invalid option")

else:
    print("Invalid input. Enter correct model number")