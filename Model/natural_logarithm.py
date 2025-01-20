from Model.integer import Integer
from Model.product import Product
from Model.logarithm import Logarithm
from Model.euler import Euler


class NaturalLogarithm(Logarithm):
    def __init__(self, argument):
        super().__init__(Euler(), argument)
        
    def __str__(self):
        return f'ln({self.argument})'

    def isConstant(self):
        if self.isconstant is None:
            if self.argument.isConstant():
                self.isconstant = True
            else:
                self.isconstant = False
        return self.isConstant
      
    # Should pull __gt__ and __eq__ from super
    
    def derivative(self, differential, safeMode = False):
        from Model.exponential import Exponential
        simpSelf = self.pfsf(safeMode)
        if simpSelf == self: # if no change
            return Product([
                Exponential(self.argument, Integer(-1)),
                self.argument.derivative(differential)
            ]).pfsf(safeMode)
        else:
            return simpSelf.derivative(differential, safeMode)
        

    def genarg(self):#needed for constant simplification (consim)
        return (self.argument,)