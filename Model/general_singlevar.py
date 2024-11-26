from Expression import Expression
from expression_type import ExpressionType
from Product import Product

class GeneralSinglevar(Expression):
    def __init__(self, symbol:str, argument):
        super().__init__(ExpressionType.GENERALSINGLEVAR)
        self.symbol = symbol
        self.argument = argument

    def __str__(self):
        return self.symbol + '(' + self.argument.__str__() + ')'
    
    def __eq__(self, other):
        if (self.expression_type != other.expression_type):
            return False
        return (self.symbol == other.symbol and self.argument == other.argument)
    
    def derivative(self, differential):
            return Product((GeneralSinglevar(self.symbol + "\'", self.argument), self.argument.derivative(differential))) # f'