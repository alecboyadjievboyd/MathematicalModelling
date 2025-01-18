from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.sum import Sum
from Model.integer import Integer
from Model.vartocon import Vartocon



# Products of at least two expressions (factors)
class Product(Expression):

    def __init__(self, factors):
        super().__init__(ExpressionType.PRODUCT)
        self.factors = list(factors)
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
            self.isconstant = True
            for factor in self.factors:
                if factor.isConstant() == False:
                    self.isconstant = False
                    break
        return self.isconstant
    
#     def derivative(self, differential): #outputs derivative of f*g*h as f'*g*h + g'*f*h + h'*f*g
#         return Sum(tuple(
#             Product((self.factors[i].derivative(differential),) + tuple(self.factors[j] for j in range(len(self.factors)) if j!=i))
#             for i in range(len(self.factors))
#         ))
    def derivative(self, differential, safeMode = False): #outputs derivative of f*g*h as f'*g*h + f*g'*h + f*g*h'
        return Sum(tuple(
            Product(
                tuple(self.factors[j] for j in range(len(self.factors)) if j<i) 
                + (self.factors[i].derivative(differential),) 
                + tuple(self.factors[j] for j in range(len(self.factors)) if j>i)
            ) 
            for i in range(len(self.factors))
        )).pfsf(safeMode)

    def genarg(self):#needed for constant simplification (consim)
        return self.factors
    
    def consim(self, safeMode = False):

        # return self #as it isn't finished yet

        from Model.variable import Variable
        from Model.exponential import Exponential
        from Model.fraction import Frac

        def AskAlec(x):
            try:
                # y = x.pfsf(safeMode)
                #print(f"Product.consim asks Alec: {x}")
                # print(f"Alec says: {y}")
                # return y
                return x.pfsf(safeMode)
            except:
                # print(f"Product.consim asks Alec: {x}")
                # print("Alec doesn't know")
                return x

        old = self
        #expanting inner products, i.e. (a*b)*c -> a*b*c. In case of products in producs in products (nesting with more than two products), this doesn't work unless we loop a few times by recalling consim, but they will eventually, inefficiently, be expanded. We have the old-new construction for this.
        expandfactors = [] 
        for factor in self.factors:
            if factor.expression_type == ExpressionType.PRODUCT:
                expandfactors += factor.factors
            else:
                expandfactors += (factor,)


        #simplifying the factors of the product (bottom up)
        simfactors = () #simplified factors
        for factor in expandfactors:
            # print(f"{factor} simplifies to {factor.consim(safeMode)}")
            simfactors += (factor.consim(safeMode),)
        
        def expception(expo): #exponentiation + inception(going down the layers)
            #If we have something like (2^3)^4, I think this would return 8^4 instead of whatever that is. Similarly, (2^3)^sin(1) returns 8^sin(1) instead of the required (?) x_8 ^sin(1). This is indeed the case, but due to the old-new construction we eventually get there. Or is it that we get there due to the consim of the factors, which consim their bases
            if expo.base.expression_type == ExpressionType.FRACTION:
                if expo.argument.expression_type == ExpressionType.INTEGER: #this won't happen. It would have already been simplified
                    return expo.base**expo.argument
                elif expo.argument.expression_type == ExpressionType.FRACTION: #this won't happen. It would have already been simplified
                    if expo.argument.den == Integer(1):
                        return expo.base**expo.argument
                    else:
                        return Exponential(Variable(expo.base), expo.argument) 
                else:
                    return Exponential(Variable(expo.base), expo.argument)
            else:
                if expo.base.expression_type == ExpressionType.EXPONENTIAL: 
                    return Exponential(expception(expo.base), expo.argument)
                else:
                    return Exponential(Variable(expo.base), expo.argument)
       
        #replacing stuff with variables.
        varfactors = () # replace expressions by variables
        fracprod = Frac(1) 
        for factor in simfactors:
            if factor.expression_type == ExpressionType.FRACTION:
                fracprod *= factor
            else:
                if factor.expression_type == ExpressionType.EXPONENTIAL:
                    varfactors += (expception(factor),)

                    # if factor.base.expression_type != ExpressionType.FRACTION:
                    #     varbase = Variable(factor.base)
                    # else:
                    #     varbase = factor.base
                    
                    # if factor.argument.expression_type != ExpressionType.FRACTION:
                    #     varexpo = Variable(factor.argument)
                    # else:
                    #     varexpo = factor.argument
                    
                    # varfactors += (Exponential(varbase, varexpo),)

                elif factor.expression_type == ExpressionType.SUM:
                    varterms = ()
                    for term in factor.terms:
                        varterms += (Variable(term), )
                    varfactors += (Sum(varterms),)
                else:
                    varfactors += (Variable(factor),)


        if fracprod == Frac(0):
            return Frac(0)

        #asking Alec to simplify the expression with variables  
        alecsim = AskAlec(Product(varfactors + (fracprod,)))

        #commented section till new = Vartocon(alecsim) is one bit, that should be more efficient than Vartocon, but is a lot less clean.
        # we_want_to_be_efficient_but_neglect_hypervariables = False
        # if we_want_to_be_efficient_but_neglect_hypervariables:
        #     if alecsim.expression_type == ExpressionType.SUM:
        #         alecterms = alecsim.terms
        #     elif alecsim.expression_type == ExpressionType.PRODUCT:
        #         alecterms = (alecsim,)
        #     else:
        #         alecterms = (alecsim,)

        #     # if alecsim.expression_type == ExpressionType.PRODUCT:
        #     #     alecfactors = alecsim.factors
        #     # else: #if alecsim.expression_type != ExpressionType.SUM:
        #     #     alecfactors = (alecsim,)

        #     #equivalent to Vartocon:
        #     def kicks(expo): #to keep the inception terminology concistent. A kick gets people one dream level lower (I am not a nerd, I googled this).
        #         if expo.base.expression_type == ExpressionType.VARIABLE:
        #             return Exponential(expo.base.index, expo.argument)
        #         elif expo.base.expression_type == ExpressionType.EXPONENTIAL:
        #             return Exponential( kicks(expo.base), expo.argument )
        #         else:
        #             return expo

        #     nonvarterms = ()
        #     for term in alecterms:
        #         alecfactors = ()
        #         if term.expression_type == ExpressionType.PRODUCT:
        #             alecfactors = term.factors
        #         else:
        #             alecfactors = (term,)

        #         nonvarfactors = ()
                
        #         for factor in alecfactors:
        #             if factor.expression_type == ExpressionType.VARIABLE:
        #                 factor = factor.index
        #             elif factor.expression_type == ExpressionType.EXPONENTIAL:
        #                 factor = kicks(factor)
        #             nonvarfactors += (factor,)

        #         if len(nonvarfactors) > 1:
        #             nonvarterms += (Product(nonvarfactors),)
        #         else: #==0
        #             nonvarterms += (nonvarfactors[0],)
                
        #     if len(nonvarterms) > 1:
        #         new =  Sum(nonvarterms)
        #     else: #==0
        #         new = nonvarterms[0]
        # else:
        new = Vartocon(alecsim)

        if old==new: #this is at least necessary for nested products. Also for expception
            return new
        else:
            return new.consim(safeMode)









        



    
    # To consolidate a product and remove one terms. (CONSIM WILL NEED TO USE THIS FOR CONSTANTS)
    def consolidate(self):
        
        popList = []
        appendList = []

        factors = self.factors.copy()

        #one Elimination + Consolidation step: If any of the terms are also products, we expand those products above.

        for index, term in enumerate(factors):
            # Note that the two statments can never trigger at the same time. 
            if (term.expression_type == ExpressionType.PRODUCT): #If one of the terms itself is a product. 
                popList.append(index) # Add the term to the removal list
                termsNew = term.consolidate() # Consolidate the inner product (incase there are any more nested products) + to clear zeros from the inner sum
                for term2 in termsNew.factors:
                    appendList.append(term2) # Add the extracted terms to the append list. 
            elif term == Integer(1):
                popList.append(index) # Remove one terms (we will do this again later but it is worth doing it now for efficiency)

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
    def pfsf(self, safeMode = False):
     
        from Model.exponential import Exponential
        
        # first simplify all factors to the max and then consolidate

        factorsPfsf = []

        for factor in self.factors:
            factorsPfsf.append(factor.pfsf(safeMode)) # Simplify all the terms

        factorsPfsf = Product(factorsPfsf).consolidate().factors 

        for factor in factorsPfsf:
            if factor.expression_type == ExpressionType.INTEGER and factor.value == 0:
                return Integer(0)

        # IF A FACTOR IS A SUM

        sumContained = False

        for factor in factorsPfsf:
            if factor.expression_type == ExpressionType.SUM: # If any of them are sums (in this case they must be multi-term sums because all factors have been simplified)
                sumContained = True

        if sumContained == True: # At least one factor is a sum
            return Product(factorsPfsf).multOut([]).pfsf(safeMode) # Will turn it into a sum and then call pfsf on it, meaning that each internal (sum free) product will then be simplified
        
        if sumContained == False:

            constList = []
            constIndex = []

            

            for index, factor in enumerate(factorsPfsf):
                if factor.isConstant():
                    constIndex.append(index)
                    constList.append(factor)
                elif factor.expression_type != ExpressionType.EXPONENTIAL: # if it is not an exponent (fully expected to be simplified)
                    factorsPfsf[index] = Exponential(factor, Integer(1)) # Make it exponent :)
            
            for index in sorted(constIndex, reverse = True): # Removing the constants from the front
                factorsPfsf.pop(index)    
            
            orderedFactors = []

            repeat = False

            if len(factorsPfsf) > 0: # there is at least one non-constant

                for factor in factorsPfsf:
                    if factor.base.expression_type == ExpressionType.EXPONENTIAL:
                        repeat = True # Make sure to repeat in case consolidation occurs

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

                    if factor.argument.expression_type == ExpressionType.SUM: # If not a sum, it was not joined and thus there is no need to simplify as it is already pfsf (for efficiency) THIS ALSO WILL DEAL WITH CONSTANT SIMP
                        factor.argument = factor.argument.pfsf(safeMode) # Simplify the exp

                    if factor.argument == Integer(1): # If it is a 1
                        orderedFactors[index] = factor.base # no need for an exponent

                    elif factor.argument == Integer(0): # If it is a zero
                        orderedFactors[index] = Integer(1) # Exponent resolves to a constant

                    
                    # if neither of these hold, the arg is not zero or one, so we leave it as is

            if len(constList) > 0:
                if len(constList) == 1:
                    orderedFactors.insert(0, constList[0])
                else:
                    orderedFactors.insert(0, Product(constList).consim(safeMode))

            for factor in orderedFactors:
                if (type(factor) != int and factor.expression_type == ExpressionType.INTEGER and factor.value == 0):
                    return Integer(0)
                elif (type(factor) != int and factor.expression_type == ExpressionType.FRACTION and factor.num == Integer(0)):
                    return Integer(0)
                elif (type(factor) == int and factor == 0):
                    return Integer(0)
            
                       
            if len(orderedFactors) == 0: # only one term
                return Integer(1)
            if len(orderedFactors) == 1: # only one term
                return orderedFactors[0]
            else:
                if repeat:
                    return Product(orderedFactors).pfsf(safeMode)
                return Product(orderedFactors)
    
