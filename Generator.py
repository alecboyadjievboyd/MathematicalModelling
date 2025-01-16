import random
import math
import multiprocessing

from Model.product import Product
from Model.sum import Sum
from Model.exponential import Exponential
from Model.logarithm import Logarithm
from Model.exp import Exp
from Model.arctangent import Arctangent
from Model.tangent import Tangent
from Model.sine import Sine
from Model.arcsine import Arcsine
from Model.cosine import Cosine
from Model.arccosine import Arccosine
from Model.variable import Variable
from Model.euler import Euler
from Model.pi import Pi
from Model.integer import Integer
from Model.expression_type import ExpressionType



def generate(depth, maxElements):

    if depth == 0:
        num = random.randint(0, 11)
        if num < 5:
            return Variable(1)
        if num > 7:
            return Integer(random.randint(-9,9))
        if num == 6:
            return Euler()
        if num == 7:
            return Pi()

    tryy = random.randint(0, 10)
    if tryy < 8:
        operation = random.choice([
            "Product",
            "Sum",
            "Exponential",
            "Logarithm"
            ])
    else:
        operation = random.choice([ 
            "Arctangent",
            "Tangent",
            "Sine",
            "Arcsine",
            "Cosine",
            "Arccosine"
        ])

    elementNum = random.randint(2, maxElements)

    if depth == 0:
        depth = 1

    if operation == "Product":
        factors = []
        i = 1
        while i <= elementNum:
            factors.append(generate(random.randint(0, depth - 1), maxElements)) 
            i = i+1
        
        return Product(factors)  # Replace [...] with appropriate arguments

    elif operation == "Sum":
        terms = []
        i = 1
        while i <= elementNum:
            terms.append(generate(random.randint(0, depth - 1), maxElements))
            i = i+1

        return Sum(terms)  # Replace [...] with appropriate arguments

    elif operation == "Exponential":
        return Exponential(generate(random.randint(0, depth - 1), maxElements), generate(random.randint(0, depth - 1), maxElements))  # Replace base, exponent with actual values

    elif operation == "Logarithm":
        return Logarithm(generate(random.randint(0, depth - 1), maxElements), generate(random.randint(0, depth - 1), maxElements))  # Replace base, argument with actual values

    elif operation == "Arctangent":
        return Arctangent(generate(random.randint(0, depth - 1), maxElements))  # Replace argument with actual value

    elif operation == "Tangent":
        return Tangent(generate(random.randint(0, depth - 1), maxElements))  # Replace argument with actual value

    elif operation == "Sine":
        return Sine(generate(random.randint(0, depth - 1), maxElements))  # Replace argument with actual value

    elif operation == "Arcsine":
        return Arcsine(generate(random.randint(0, depth - 1), maxElements))  # Replace argument with actual value

    elif operation == "Cosine":
        return Cosine(generate(random.randint(0, depth - 1), maxElements))  # Replace argument with actual value

    elif operation == "Arccosine":
        return Arccosine(generate(random.randint(0, depth - 1), maxElements))  # Replace argument with actual value

def evaluate(f, x):

    if f.expression_type == ExpressionType.INTEGER:
        return f.value
    
    if f.expression_type == ExpressionType.EULER:
        return 2.7182818284590452353602874713526624977572470937

    if f.expression_type == ExpressionType.PI:
        return 3.1415926535897932384626433832795028841971693994

    if f.expression_type == ExpressionType.VARIABLE:
        return x

    if f.expression_type == ExpressionType.FRACTION: # FRACTIONS ONLY CONTAIN INTEGERS
        from Model.fraction import Frac

        num = evaluate(f.num, x)
        den = evaluate(f.den, x)

        if num == 'undefined' or den == 'undefined' or den == 0:
            return 'undefined'

        try:
            return (num / den)
        except Exception:
            return 'undefined'

    if f.expression_type == ExpressionType.PRODUCT:
        value = 1
        for factor in f.factors:
            ev = evaluate(factor, x)
            if ev == 'undefined':
                return 'undefined'
            value = value * ev

        try:
            return value
        except Exception:
            return 'undefined'

    if f.expression_type == ExpressionType.SUM:
        value = 0
        for term in f.terms:
            ev = evaluate(term, x)
            if ev == 'undefined':
                return 'undefined'
            value = value + ev
        
        try:
            return value
        except Exception:
            return 'undefined'

    if f.expression_type == ExpressionType.EXPONENTIAL:
        baseEv = evaluate(f.base, x)
        argEv = evaluate(f.argument, x)

        try:
            return math.pow(baseEv, argEv)
        except Exception:
            return 'undefined'

    if f.expression_type == ExpressionType.LOGARITHM:
        baseEv = evaluate(f.base, x)
        argEv = evaluate(f.argument, x)

        try:
            return math.log(argEv, baseEv)
        except Exception:
            return 'undefined'

    if f.expression_type == ExpressionType.ARCTANGENT:
        
        argEv = evaluate(f.argument, x)

        try:
            return math.atan(argEv)
        except Exception:
            return 'undefined'

    if f.expression_type == ExpressionType.TANGENT:
        
        argEv = evaluate(f.argument, x)

        try:
            return math.tan(argEv)
        except Exception:
            return 'undefined'

    if f.expression_type == ExpressionType.SINE:
        
        argEv = evaluate(f.argument, x)

        try:
            return math.sin(argEv)
        except Exception:
            return 'undefined'

    if f.expression_type == ExpressionType.ARCSINE:
        
        argEv = evaluate(f.argument, x)

        try:
            return math.asin(argEv)
        except Exception:
            return 'undefined'

    if f.expression_type == ExpressionType.COSINE:
        
        argEv = evaluate(f.argument, x)

        try:
            return math.cos(argEv)
        except Exception:
            return 'undefined'

    if f.expression_type == ExpressionType.ARCCOSINE:
        
        argEv = evaluate(f.argument, x)

        try:
            return math.acos(argEv)
        except Exception:
            return 'undefined'

    else: 
        print("WHY THE FUCK")

def safeModeTest(depth, maxElements): # Generates a test case for safe mode
    
    obj = generate(depth, maxElements)

    print("Original: " + str(obj))

    try:
        objPfsf = obj.pfsf(False) # Non Safe Mode Simplification
    except RecursionError:
        print("Recursion Depth Error, Skipping...")
        return # Cannot test here, skip
    except Exception as e:
        print(f"Exception {e} occured, enter to continue")
        ignore = input()
        return
    
    print("Simplified: " + str(objPfsf))

    testValue = [random.uniform(-100, 100) for _ in range(10)] # A list of 10 test values between 1 and 100

    passed = False

    failValues = []

    for value in testValue:

        initValue = evaluate(obj, value)
        pfsfValue = evaluate(objPfsf, value)

        if initValue == 'undefined' and pfsfValue == 'undefined':
            passed = True

        elif initValue != 'undefined' and pfsfValue == 'undefined':
            passed = False
            failValues.append([value, initValue, pfsfValue])

        elif initValue == 'undefined' and pfsfValue != 'undefined':
            passed = True

        elif initValue != 'undefined' and pfsfValue != 'undefined':
            if initValue == 0:
                if abs(initValue - pfsfValue) < 0.01:
                    passed = True
                else:
                    passed = False

            elif abs(initValue - pfsfValue) / initValue < 0.01: # if there is less than a 1% difference (rounding errors)
                passed = True
            else: 
                passed = False # too big a difference to be accounted for in rounding errors
                failValues.append([value, initValue, pfsfValue])
    
    if passed:
        print("Trial Passed: These functions are numerically equivalent")
    else:
        print("Trial Failed: The following values were not equivalent")
        for item in failValues:
            print("For Value: " + str(item[0]) + ", the original function outputted '" + str(item[1]) + "' while the simplified function outputted '" + str(item[2]) + "'")
        print(" ")
        print("Continue with any character")
        ignore = input()
        print(" ")

    return

if __name__ == "__main__":
    count = 0
    failCount = 0
    while True:
        print(" ")
        count = count + 1
        print("RUNNING TEST NUMBER " + str(count))

        process = multiprocessing.Process(target=safeModeTest, args=(4,3))
        process.start()
        process.join(timeout = 10)

        if process.is_alive():
            print(f"Process took too long. Skip with character")
            ignore = input()
            count -= 1            
            process.terminate()  # Forcefully terminate the process
            process.join()  # Ensure the process cleanup is completed

        if process.exitcode != 0:
            print(f"Process crashed with exit code {process.exitcode}.")
            inp = 'bruh'
            while inp != 'y' and inp != 'n' and inp != 'r':
                print("Approve with 'y' reject with 'n', indicate recursion error with 'r")
                inp = input()
            if inp == 'n':
                failCount += 1
            if inp == 'r':
                count -= 1 #this is not a real problem

        
        ##safeModeTest(4, 3)


