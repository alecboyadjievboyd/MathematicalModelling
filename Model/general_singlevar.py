from expression import Expression
from expression_type import ExpressionType
from product import Product

class GeneralSinglevar(Expression):
    def __init__(self, symbol:str, argument):
        super().__init__(ExpressionType.GENERALSINGLEVAR)
        self.symbol = symbol
        self.argument = argument

    def __str__(self):
        return self.symbol + '(' + self.argument.__str__() + ')'
    
    def isConstant(self):
        return False
    
    def derivative(self, differential):
            return Product((GeneralSinglevar(self.symbol + "\'", self.argument), self.argument.derivative(differential))) # f'