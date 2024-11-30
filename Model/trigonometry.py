from Expression import Expression
from expression_type import ExpressionType
from Sum import Sum
from Product import Product
from Constant import Constant
from Exponential import Exponential


# Cosine of an expression
class Cosine(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.COSINE)
        self.argument = argument
        self.isConstant = None
        
    def __str__(self):
        return f'cos({self.argument})'
    
    # THIS ONLY CHECKS PFSF FORM EQUIVALENCE
    def __eq__(self, other):
        if (self.expression_type != other.expression_type):
            return False
        if (str(self) == str(other)):
            return True
        else: return False

    def isConstant(self):
        if self.isConstant == None: 
            if self.argument.isConstant() == True:
                self.isConstant = True
            else:
                self.isConstant = False
        return self.isConstant
    
    def derivative(self, differential):
        
        return Product({Constant(-1), Sine(self.argument), self.argument.derivative(differential)})
    

# Sine of an expression
class Sine(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.SINE)
        self.argument = argument
        self.isConstant = None
        
    def __str__(self):
        return f'sin({self.argument})'
    
    # THIS ONLY CHECKS PFSF FORM EQUIVALENCE
    def __eq__(self, other):
        if (self.expression_type != other.expression_type):
            return False
        if (str(self) == str(other)):
            return True
        else: return False

    def isConstant(self):
        if self.isConstant == None: 
            if self.argument.isConstant() == True:
                self.isConstant = True
            else:
                self.isConstant = False
        return self.isConstant
    
    def derivative(self, differential):
        return Product({Cosine(self.argument), self.argument.derivative(differential)})
    

# Tangent of an expression
class Tangent(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.TANGENT)
        self.argument = argument
        self.isConstant = None
        
    def __str__(self):
        return f'tan({self.argument})'
    
    # THIS ONLY CHECKS PFSF FORM EQUIVALENCE
    def __eq__(self, other):
        if (self.expression_type != other.expression_type):
            return False
        if (str(self) == str(other)):
            return True
        else: return False

    def isConstant(self):
        if self.isConstant == None: 
            if self.argument.isConstant() == True:
                self.isConstant = True
            else:
                self.isConstant = False
        return self.isConstant
    
    def derivative(self, differential):
        return Product({Exponential(Cosine(self.argument), Constant(-2)), self.argument.derivative(differential)})
    
class Arcsine(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.ARCSINE)
        self.argument=argument
        self.isConstant = None
    
    def __str__(self):
        return f"arcsin({self.argument})"
    
    # THIS ONLY CHECKS PFSF FORM EQUIVALENCE
    def __eq__(self, other):
        if (self.expression_type != other.expression_type):
            return False
        if (str(self) == str(other)):
            return True
        else: return False

    def isConstant(self):
        if self.isConstant == None: 
            if self.argument.isConstant() == True:
                self.isConstant = True
            else:
                self.isConstant = False
        return self.isConstant

    def derivative(self, differential):
        return Product((
            Exponential(Sum((Constant(1), Product((Constant(-1), Exponential(self.argument, Constant(2))))))
                           , Product((Constant(-1), Exponential(Constant(2), Constant(-1)))) ),
                           self.argument.derivative(differential)))

class Arccosine(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.ARCCOSINE)
        self.argument=argument
        self.isConstant = None
    
    def __str__(self):
        return f"arccos({self.argument})"
    
    # THIS ONLY CHECKS PFSF FORM EQUIVALENCE
    def __eq__(self, other):
        if (self.expression_type != other.expression_type):
            return False
        if (str(self) == str(other)):
            return True
        else: return False

    def isConstant(self):
        if self.isConstant == None: 
            if self.argument.isConstant() == True:
                self.isConstant = True
            else:
                self.isConstant = False
        return self.isConstant

    def derivative(self, differential):
        return Product((Constant(-1),
            Exponential(Sum((Constant(1), Product((Constant(-1), Exponential(self.argument, Constant(2))))))
                           , Product((Constant(-1), Exponential(Constant(2), Constant(-1)))) ),
                           self.argument.derivative(differential)))
    
class Arctangent(Expression):
    def __init__(self, argument):
        super().__init__(ExpressionType.ARCTANGENT)
        self.argument=argument
        self.isConstant = None
    
    def __str__(self):
        return f"arctan({self.argument})"
    
    # THIS ONLY CHECKS PFSF FORM EQUIVALENCE
    def __eq__(self, other):
        if (self.expression_type != other.expression_type):
            return False
        if (str(self) == str(other)):
            return True
        else: return False

    def isConstant(self):
        if self.isConstant == None: 
            if self.argument.isConstant() == True:
                self.isConstant = True
            else:
                self.isConstant = False
        return self.isConstant

    def derivative(self, differential):
        return Product((
            Exponential(Sum((Constant(1), Exponential(self.argument, Constant(2)))),Constant(-1)), self.argument.derivative(differential)))