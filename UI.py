import multiprocessing
from Model.variable import Variable
from Rational_model.polynomial_utils import divide_with_remainder, polynomial_gcd
from parsing import expression
from parsing_algebra import express_alg


def process_UIoperation(model_input, safeMode, operation_input, expression_input, diffIndex):
    try:
        if model_input == 1:
            if operation_input == 1:  # Differentiate
                parsed_input = expression(expression_input.replace(" ", ""))
                
                print(parsed_input.derivative(Variable(diffIndex), safeMode))

            elif operation_input == 2:  # Simplify
                parsed_input = expression(expression_input.replace(" ", ""))
                print(parsed_input.pfsf(safeMode))
            else:
                print("Invalid option")

        elif model_input == 2:
            if operation_input == 1:  # Simplify
                parsed_input = express_alg(expression_input.replace(" ", ""))
                print(parsed_input.simplify())
            elif operation_input == 2:  # Simplify and Factorize
                parsed_input = express_alg(expression_input.replace(" ", ""))
                print(parsed_input.get_standard_form())
            else:
                print("Invalid option")
        else:
            print("Invalid input. Enter correct model number")
    except RecursionError:
        print("There was a recursion depth error! Your expression or operation may be too complex or incorrectly inputted!")
    #except Exception as e:
        print(f"There was an error {e}! Your expression or operation may be too complex or incorrectly inputted!")


def UIoperation():
    print("Which model would you like to use")
    print("1. Analytic Model  2. Rational Model")
    model = int(input())

    print("Would you like to use Safe Mode?")
    print("1. Yes  2. No")
    safeMode = int(input())
    if safeMode == 1:
        safeMode = True
    if safeMode == 2:
        safeMode = False
    else:
        safeMode = False

    print("Which operation would you like to do")
    if model == 1:
        print("1. Differentiate  2. Simplify")
    elif model == 2:
        print("1. Simplify  2. Simplify and Factorize")
    else:
        print("Invalid model")
        return

    option = int(input())

    if model == 1 and option == 1:
        print("Enter the index variable to differentiate with respect to")
        diffIndex = int(input())
    else:
        diffIndex = None
    print("Enter the expression")
    user_expression = input()

    return model, safeMode, option, user_expression, diffIndex


if __name__ == "__main__":
    print(" ")
    while True:
        user_input = UIoperation()
        if user_input is None:
            continue

        model, safeMode, option, expression_input, diffIndex = user_input
        process = multiprocessing.Process(
            target=process_UIoperation, args=(model, safeMode, option, expression_input, diffIndex)
        )
        process.start()
        process.join()

        if process.exitcode != 0:
            print(f"Process crashed with exit code {process.exitcode}. Your expression or operation may be too complex or incorrectly inputted!")
