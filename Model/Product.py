from Expression import Expression
from expression_type import ExpressionType
from Sum import Sum

# Products of at least two expressions (factors)
class Product(Expression):

    def __init__(self, factors):
        super().__init__(ExpressionType.PRODUCT)
        self.factors = factors
    
    def __str__(self):
        string_expression = self.put_brackets(self.factors[0])
        for factor in self.factors[1:]:
            string_expression += " * " + self.put_brackets(factor)
        return string_expression
    
    # This function basically does a "mutual elimination" thing, cutting down copies of both lists until both copies are empty by removing
    # pairs of equivalent terms. 
    # If any elements cannot be removed from one or both lists then they are not equal.
    def __eq__(self, other):
        selfTerms = self.factors.copy()
        otherTerms = other.factors.copy()

        # Check if other contains all the terms of self
        for term1 in selfTerms[1:]:
            check = False
            for term2 in otherTerms[1:]:
                if term1 == term2:
                    otherTerms.pop(term2) # Match Found, no need to continue
                    selfTerms.pop(term1) # Same Logic
                    check = True
                    break; # Stop comparing because match has been found and pair eliminated
            if check == False: # No match has been found, so the lists of terms are not equal
                return False
            
        # Check if self contains all the terms of other
        for term1 in otherTerms[1:]:
            check = False
            for term2 in selfTerms[1:]:
                if term1 == term2:
                    selfTerms.pop(term2) # Match Found, no need to continue
                    otherTerms.pop(term1) # Same Logic
                    check = True
                    break; # Stop comparing because match has been found and pair eliminated
            if check == False: # No match has been found, so the lists of terms are not equal
                return False
            
        # If it has passed both of these, return true
        return True
    
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