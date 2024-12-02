from Model.constant import Constant
from Model.product import Product
from Model.logarithm import Logarithm


class NaturalLogarithm(Logarithm):
    def __init__(self, argument):
        super().__init__(Constant('e'), argument)
        
    def __str__(self):
        return f'ln({self.argument})'

    def isConstant(self):
        if self.isConstant is None:
            if self.argument.isConstant():
                self.isConstant = True
            else:
                self.isConstant = False
        return self.isConstant
    
    def derivative(self, differential):
        from Model.exponential import Exponential
        return Product([
            Exponential(self.argument, Constant(-1)),
            self.argument.derivative(differential)
        ])
