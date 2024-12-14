from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.sum import Sum
from Model.constant import Constant


# Products of at least two expressions (factors)
class Product(Expression):

    def __init__(self, factors):
        super().__init__(ExpressionType.PRODUCT)
        self.factors = factors
        self.isconstant = None

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
        if self.isconstant is None: 
            self.isconstant == True
            for factor in self.factors:
                if factor.isConstant() == False:
                    self.isconstant == False
                    break
        return self.isconstant
    
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
        #simplifying the factors of the product
        simfactors = ()
        for factor in self.factors:
            simfactors += (factor.consim())

        



    
    # To consolidate a product and remove one terms. (CONSIM WILL NEED TO USE THIS FOR CONSTANTS)
    def consolidate(self):
        
        popList = []
        appendList = []

        factors = self.factors.copy()

        #one Elimination + Consolidation step: If any of the terms are also products, we expand those products above.

        for index, term in enumerate(factors):
            # Note that the two statments can never trigger at the same time. 
            if (term.expression_type == ExpressionType.PRODUCT): #If one of the terms itself is a product. 
                popList.append(term) # Add the term to the removal list
                termsNew = term.consolidate() # Consolidate the inner product (incase there are any more nested products) + to clear zeros from the inner sum
                for term2 in termsNew.terms:
                    appendList.append(term2) # Add the extracted terms to the append list. 
            elif term == Constant(1):
                popList.append(term) # Remove one terms (we will do this again later but it is worth doing it now for efficiency)

        for index in sorted(popList, reverse = True): # removing the internal sums and zero terms
            factors.pop(index)

        for term in appendList:
            factors.append(term)

        return Product(factors)


    ## NOTE THAT THIS SHOULD ONLY BE CALLED IF ALL FACTORS ARE IN PFSF FORM ALREADY, MEANING ANY SUMS HAVE AT LEAST TWO TERMS, AT MOST A SINGLE CONSTANT TERM, AND NO NESTED SUMS
    ## Also pls call it with [] for the factors parameter

    def multOut(self, factors): 
        if len(self.factors) == 0: # this means everything have been computed and the recursive call has given [] from self.factors[1:]
            return Product(factors) # returns the product containting all of the factors
        
        if self.factors[0].expression_type != ExpressionType.SUM: # if the leading factor isnt a sum
            factors.append(self.factors[0]) #essenitally leave a running total of the non-sum terms
            return Product(self.factors[1:]).multOut(factors)
        
        else: # we now know it must be a sum
            newSumTerms = []
            for term in self.factors[0].terms:
                newSumTerms.append(Product(self.factors[1:]).multOut(factors + [term]))

                # newSumTerms.append(Product(factors, term, multOut(Product(self.factors[1:]), []))) # Since the trailing set of factors finds its place here, we empty the list to avoid duplication of factors

            return Sum(newSumTerms)

    # We now define PFSF
    def pfsf(self):
     
        from Model.exponential import Exponential
        
        # first simplify all factors to the max and then consolidate

        factorsPfsf = []

        for factor in self.factors:
            factorsPfsf.append(factor.pfsf()) # Simplify all the terms

        factorsPfsf = Product(factorsPfsf).consolidate().factors 

        # IF A FACTOR IS A SUM

        sumContained = False

        for factor in factorsPfsf:
            if factor.expression_type == ExpressionType.SUM: # If any of them are sums (in this case they must be multi-term sums because all factors have been simplified)
                sumContained = True

        if sumContained == True: # At least one factor is a sum

            return Product(factorsPfsf).multOut([]).pfsf() # Will turn it into a sum and then call pfsf on it, meaning that each internal (sum free) product will then be simplified
        
        if sumContained == False:

            constList = []
            constIndex = []

            

            for index, factor in enumerate(factorsPfsf):
                if factor.isConstant():
                    constIndex.append(index)
                    constList.append(factor)
                elif factor.expression_type != ExpressionType.EXPONENTIAL: # if it is not an exponent (fully expected to be simplified)
                    factorsPfsf[index] = Exponential(factor, Constant(1)) # Make it exponent :) 

            for index in sorted(constList, reverse = True): # Removing the constants from the front
                factorsPfsf.pop(index)      

            
            orderedFactors = []

            if len(factorsPfsf) > 0: # there is at least one non-constant
                # Now, without constants, all that is left to do is join like terms and order. 
                orderedFactors.append(factorsPfsf[0])      

                # Remember lesser complexity goes first
                for factor in factorsPfsf[1:]: # all remaining terms
                    added = False
                    for index, factorComp in enumerate(orderedFactors):
                        if factor.base == factorComp.base: # If the bases are equal
                            # We worry not about consolidating sums here, as we will pfsfify this at the end
                            factorComp.argument = Sum([factorComp.argument, factor.argument]) # Combine the arguments and join
                            added = True
                            break # we no longer need to compare with other terms
                        elif factor.base < factorComp.base: # This means that it is lesser in complexity than the current entry, which means it goes before it
                            orderedFactors.insert(index, factor) 
                            added = True
                            break # stop comparing because we have found its place
                        # If it is not <= it is > than the current entry and thus its place is farther to the right, continue the loop
                    # If it has still not been added, append it to the end (it must be < every other term in complexity)
                    if added == False:
                        orderedFactors.append(factor)

                # orderedFactors list is now ordered as per pfsf

                for index, factor in enumerate(orderedFactors):

                    if factor.argument.expression_type == ExpressionType.SUM: # If not a sum, it was not joined and thus there is no need to simplify as it is already pfsf (for efficiency)
                        factor.argument.pfsf() # Simplify the exp

                    if factor.argument == Constant(1): # If it is a 1
                        orderedFactors[index] = factor.base # no need for an exponent

                    elif factor.argument == Constant(0): # If it is a zero
                        orderedFactors[index] = Constant(1) # Exponent resolves to a constant
                    
                    # if neither of these hold, the arg is not zero or one, so we leave it as is

            # WHEN SIMPLIFIER EXISTS <3 DO THE FOLLOWING orderedFactors.insert(0, Product(constList).consim()) # Adding the simplified sum of constants to the sum

            if len(constList) > 0:
                orderedFactors.insert(0, Product(constList))
            
            if len(orderedFactors) == 1: # only one term
                return orderedFactors[0]
            else:
                return Sum(orderedFactors)
    
