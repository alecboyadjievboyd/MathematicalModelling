import Expression
import ExpressionType
import Product

class GeneralSinglevar(Expression):
    def __init__(self, symbol:str, argument):
        super().__init__(ExpressionType.GENERALSINGLEVAR)
        self.symbol = symbol
        self.argument = argument

    def __str__(self):
        return self.symbol + '(' + self.argument.__str__() + ')'
    
    def derivative(self, differential):
            return Product((GeneralSinglevar(self.symbol + "\'", self.argument), self.argument.derivative(differential))) # f'