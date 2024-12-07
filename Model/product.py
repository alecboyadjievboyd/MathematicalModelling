from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.sum import Sum


# Products of at least two expressions (factors)
class Product(Expression):

    def __init__(self, factors):
        super().__init__(ExpressionType.PRODUCT)
        self.factors = factors
        self.isConstant = None

        self.primaryOrder = 4 # Monomial Product

        # Checks if any terms are functions

        for factor in self.factors:
            if factor.primaryOrder > 5: # product or sum of functions
                self.primaryOrder = 7 # Function prod
            if factor.primaryOrder == 5: # Term is function or greater
                if factor.secondaryOrder != 8: # Not an exponential (cannot be monomial)
                    self.primaryOrder = 7 # Function prod
                else: # Is exponential
                    if not ((factor.base.primaryOrder == 2) and factor.argument.isConstant()): # not a monomial
                        self.primaryOrder = 7 # Function prod
    
    def __str__(self):
        string_expression = self.put_brackets(self.factors[0])
        for factor in self.factors[1:]:
            string_expression += " * " + self.put_brackets(factor)
        return string_expression
    
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
                
        if (self.primaryOrder == other.primaryOrder): # Both products
            return max(self.factors) > max(other.factors)
        
        else: 
            return self.primaryOrder > other.primaryOrder # Ordering classes

    def isConstant(self):
        if self.isConstant == None: 
            self.isConstant == True
            for factor in self.factors:
                if factor.isConstant == False:
                    self.isConstant == False
                    break
        return self.isConstant
    
#     def derivative(self, differential): #outputs derivative of f*g*h as f'*g*h + g'*f*h + h'*f*g
#         return Sum(tuple(
#             Product((self.factors[i].derivative(differential),) + tuple(self.factors[j] for j in range(len(self.factors)) if j!=i))
#             for i in range(len(self.factors))
#         ))
    def derivative(self, differential): #outputs derivative of f*g*h as f'*g*h + f*g'*h + f*g*h'
        return Sum(tuple(
            Product(
                tuple(self.factors[j] for j in range(len(self.factors)) if j<i) 
                + (self.factors[i].derivative(differential),) 
                + tuple(self.factors[j] for j in range(len(self.factors)) if j>i)
            ) 
            for i in range(len(self.factors))
        ))

    def genarg(self):#needed for constant simplification (consim)
        return self.factors