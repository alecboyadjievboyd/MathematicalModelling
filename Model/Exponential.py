import Expression
import ExpressionType
import Product
import Sum
import Constant
import NaturalLogarithm

# Exponential function with an expression as a base and exponent
class Exponential(Expression):

    def __init__(self, base, exponent):
        super().__init__(ExpressionType.EXPONENTIAL)
        self.base = base
        self.exponent = exponent
    
    def __str__(self):
        return self.put_brackets(self.base) + "^" + self.put_brackets(self.exponent)
    
    def derivative(self, differential):
        return Product((self, 
                      Sum(( Product((self.exponent.derivative(differential), NaturalLogarithm(self.base))),
                          Product((self.exponent, Exponential(self.base, Constant(-1)), self.base.derivative(differential)))                         
                         ))
                      ))