from Model.expression_type import ExpressionType
from Model.expression import Expression
from Model.integer import Integer


# Singular variables, without constants or exponents. Terminal expression.
class Variable(Expression):

    def __init__(self, index):
        super().__init__(ExpressionType.VARIABLE)
        self.index = index
        self.primaryOrder = 2 #monomial
        self.secondaryOrder = None

    def __str__(self):
        return "x[" + str(self.index) +"]"
    
    def __eq__(self, other):
        if (self.expression_type != other.expression_type):
            return False
        
        return (self.index == other.index)
    
    def __gt__(self, other):

        if other.isConstant():
            return True

        if (self.primaryOrder == other.primaryOrder): # Both variables
            return self.index > other.index
        
        else: 
            return self.primaryOrder > other.primaryOrder # Ordering classes
    
    def derivative(self, differential):
        if self.index == differential.index:
            return Integer(1)
        else:
            return Integer(0)
        
    def isConstant(self):
        return False
        
    def pfsf(self, safeMode = False):
        return Variable(self.index) 

    def genarg(self):#needed for constant simplification (consim)
        return (self.index,)
    

#useful for testing consim (I need terminal expressions which cannot be manipulated)
class Hypervariable(Expression):

    def consim(self):
        return self

    def __init__(self, index):
        super().__init__(ExpressionType.HYPERVARIABLE)
        self.index = index
        self.primaryOrder = 2 #monomial
        self.secondaryOrder = None

    def __str__(self):
        return "h[" + str(self.index) +"]"
    
    def __eq__(self, other):
        if (self.expression_type != other.expression_type):
            return False
        
        return (self.index == other.index)
    
    def __gt__(self, other):

        if other.isConstant():
            return True

        if (self.primaryOrder == other.primaryOrder): # Both variables
            return self.index > other.index
        
        else: 
            return self.primaryOrder > other.primaryOrder # Ordering classes
    
    def derivative(self, differential):
        if self.index == differential.index:
            return Integer(1)
        else:
            return Integer(0)
        
    def isConstant(self):
        return False
        
    def pfsf(self, safeMode = False):
        return Variable(self.index) 

    def genarg(self):#needed for constant simplification (consim)
        return (self.index,)