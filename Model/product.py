from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.sum import Sum
from Model.constant import Constant


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
    
    def consim(self):
        print("make Product.consim")
        return self
    
    # To consolidate a product and remove one terms. (CONSIM WILL NEED TO USE THIS FOR CONSTANTS)
    def consolidate(self):
        
        popList = []
        appendList = []

        #one Elimination + Consolidation step: If any of the terms are also products, we expand those products above.

        for term in self.factors:
            # Note that the two statments can never trigger at the same time. 
            if (term.expression_type == ExpressionType.PRODUCT): #If one of the terms itself is a product. 
                popList.append(term) # Add the term to the removal list
                termsNew = term.consolidate() # Consolidate the inner product (incase there are any more nested products)
                for term2 in termsNew.terms:
                    appendList.append(term2) # Add the extracted terms to the append list. 
            elif term == Constant(1):
                popList.append(term) # Remove one terms (we will do this again later but it is worth doing it now for efficiency)

        for term in popList: # removing the internal sums and zero terms
            self.factors.pop(term)

        for term in appendList:
            self.factors.append(term)

    # We now define PFSF
    def pfsf(self):
        
        # first simplify all factors to the max and then consolidate

        # IF A FACTOR IS A SUM

        # separate the factors that are sums into a different list
        # multiply these sums, then multiply through the non-sum factors to all
        # you are now left with a large sum of terms. simply run pfsf on this sum and return that (it will call pfsf again on the terms which are products with no sum factors, thus leading to the next section)

        # IF NO FACTORS ARE SUMS

        # yippee, do ordering (in a similar way to sums). 
        # multiply the constants together and seperate
        # for the remaining factors, put everything into expression^expression form (similar to how we did c * f(x) form for sums)
        # compare lower expressions
        # put into a sorted list one by one by complexity comparison of bases (in the order of increasing complexity, not decreasing as in sums)
        # combine exponenents for identical bases (may not be the only compatible bases but usually will be)
        
        # once done, we go through and revert exponenets back to simplified form (i.e. return base only if exponent is 1 and return 1 if exponent is 0) and simplify constant exponents 
        # put the consim-ed constant in the front of the new product 
        # now we are basically done, just do a check if the product contains only one term and if not yippee!

        # this is slightly different from summation because the exponents may be functions not just constants and they can still be combined sensibly. this is due to PFSF definition, where sums are considered 
        # acceptable as an exponent but not part of a product

        return self
