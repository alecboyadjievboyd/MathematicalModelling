from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.product import Product
from Model.constant import Constant


# Sine of an expression
class Sine(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.SINE)
        self.argument = argument
        self.isConstant = None
        self.primaryOrder = 5 # Single Function
        self.secondaryOrder = 6 # Sin 
        
    def __str__(self):
        return f'sin({self.argument})'
    
    # THIS ONLY CHECKS PFSF FORM EQUIVALENCE
    def __eq__(self, other):
        if (self.expression_type != other.expression_type):
            return False
        if (str(self) == str(other)):
            return True
        else: return False

    def __gt__(self, other):

        if (self.isConstant() == False) and other.isConstant():
            return True
                
        if (self.primaryOrder == other.primaryOrder): # Both functions
            if (self.secondaryOrder == other.secondaryOrder): # Both sin
                return self.argument > other.argument
            else:
                return self.secondaryOrder > other.secondaryOrder # Ordering of functions
        else: 
            return self.primaryOrder > other.primaryOrder # Ordering classes

    def isConstant(self):
        if self.isConstant == None: 
            if self.argument.isConstant() == True:
                self.isConstant = True
            else:
                self.isConstant = False
        return self.isConstant
    
    def derivative(self, differential):
        from Model.cosine import Cosine
        return Product({Cosine(self.argument), self.argument.derivative(differential)})

    def genarg(self):#needed for constant simplification (consim)
        return (self.argument,)
    
    # def consim(self):
    #     simarg = self.argument.consim() #simplified argument
        
    #     if simarg == Frac('pi'):
    #         return Frac(-1)
        
    #     simvar = AskAlec(Sine(simarg))

