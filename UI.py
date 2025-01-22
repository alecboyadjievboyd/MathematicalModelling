import multiprocessing
from Model.variable import Variable
from Rational_model.polynomial_utils import divide_with_remainder, polynomial_gcd
from parsing import expression
from parsing_algebra import express_alg

def wrap_with_exception_handler(function):
    """
    Executes a given function and handles all the exceptions.
    :param function: function to be wrapped
    """
    try:
        function()
    except RecursionError:
        print("Recursion depth error! The resulting or intermediate expression is too long "
              "in simplified form or incorrectly inputted!")
    except Exception as e:
        print(f'An error occurred:\n{e}\nYour expression or operation '
              f'may be too complex or incorrectly inputted!')

def run_in_process(target_function):
    """
    Runs a given function in a separate process to avoid fatal errors. In case of fatal error, prints the exitcode.
    Target function is wrapped with exception handling function to handle exceptions properly
    :param target_function: function with execution of a chosen operation and printing the result
    """
    process = multiprocessing.Process(target=wrap_with_exception_handler(target_function))
    process.start()
    process.join()

    if process.exitcode != 0:
        print(
            f"Process crashed with exit code {process.exitcode}.\n"
            f"Your expression or operation may be too complex or incorrectly inputted!")

def ui_algebraic_model():
    """
    Gives prompts and outputs the results for algebraic model operations.
    """
    print("Would you like to use Safe Mode?")
    print("1. Yes  2. No")
    safe_mode = input()
    if safe_mode == '1':
        safe_mode = True
    elif safe_mode == '2':
        safe_mode = False
    else:
        print('Invalid option')
        return

    print("Which operation would you like to do")
    print("1. Differentiate  2. Simplify")
    operation = input()

    if operation == '1':
        print("Enter the index variable to differentiate with respect to")
        differentiation_index = input()
        if not differentiation_index.isdigit():
            print('Invalid option')
            return
        differentiation_index = int(differentiation_index)

        print("Enter the expression")
        user_expression = input()

        run_in_process(lambda: print(expression(user_expression.replace(" ", ""))
              .derivative(Variable(differentiation_index), safe_mode)),)

    elif operation == '2':
        print("Enter the expression")
        user_expression = input()

        run_in_process(lambda: print(expression(user_expression.replace(" ", ""))
              .pfsf(safe_mode)))

    else:
        print('Invalid option')
        return

def do_root_finding(input_expression):
    """
    Function for root finding of a polynomial. To be executed in a process
    :param input_expression polynomial in the string form
    """
    parsed_input = express_alg(input_expression.replace(" ", ""))
    parsed_input = parsed_input.simplify()

    roots = parsed_input.find_rational_roots()
    for root in roots:
        print(root, end='  ')

def do_division_with_remainder(input_expression1, input_expression2):
    """
    Function for division with remainder of two polynomials. To be executed in a process
    :param input_expression1: the first polynomial in the string form
    :param input_expression2: the second polynomial in the string form
    """
    dividend = express_alg(input_expression1.replace(" ", ""))
    dividend = dividend.simplify()

    divider = express_alg(input_expression2.replace(" ", ""))
    divider = divider.simplify()

    quotient, remainder = divide_with_remainder(dividend, divider)
    print("quotient: ", quotient)
    print("remainder: ", remainder)

def do_gcd(input_expression1, input_expression2):
    """
    Function for finding gcd of two polynomials. To be executed in a process
    :param input_expression1: the first polynomial in the string form
    :param input_expression2: the second polynomial in the string form
    """
    polynomial1 = express_alg(input_expression1.replace(" ", ""))
    polynomial1 = polynomial1.simplify()

    polynomial2 = express_alg(input_expression2.replace(" ", ""))
    polynomial2 = polynomial2.simplify()

    print('gcd: ', polynomial_gcd(polynomial1, polynomial2))

def ui_rational_model():
    """
    Gives prompts and outputs the results for rational model operations.
    """
    print("Which operation would you like to do?")
    print("1. Simplify  2. Simplify and factorize  3. Find roots")
    print("4. Divide with remainder  5. GCD")
    operation = input()

    if operation == '1':
        # User chooses to simplify an expression

        print("Enter the expression")
        user_input = input()
        run_in_process(lambda: print(express_alg(user_input.replace(" ", ""))
              .simplify()))

    elif operation == '2':
        # User chooses to simplify and factorize an expression

        print("Enter the expression")
        user_input = input()
        run_in_process(lambda: print(express_alg(user_input.replace(" ", ""))
              .get_standard_form()))

    elif operation == '3':
        # User chooses to find roots of a polynomial

        print("Enter the expression")
        user_input = input()
        run_in_process(lambda: do_root_finding(user_input))

    elif operation == '4':
        # User chooses to perform division with remainder on two polynomials

        print("Enter the dividend:")
        user_input1 = input()

        print("Enter the divider:")
        user_input2 = input()

        run_in_process(lambda: do_division_with_remainder(user_input1, user_input2))

    elif operation =='5':
        # User chooses to find gcd of two polynomials

        print("Enter the first polynomial:")
        user_input1 = input()

        print("Enter the second polynomial:")
        user_input2 = input()

        run_in_process(lambda: do_gcd(user_input1, user_input2))

    else:
        print("Invalid option")

if __name__ == "__main__":
    # Continuously gives user prompts to perform an operation on expression(s) with algebraic or rational model
    while True:

        print()
        print("Which model would you like to use?")
        print("1. Analytic Model  2. Rational Model 3. Terminate execution")
        model_choice = input()

        if model_choice == '1':
            ui_algebraic_model()
        elif model_choice == '2':
            ui_rational_model()
        elif model_choice == '3':
            break
        else:
            print("Invalid input. Enter correct model number")

