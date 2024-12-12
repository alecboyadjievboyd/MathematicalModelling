from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.make_expression import MakeExpression
from Model.variable import Variable
from Model.constant import Constant

def AskAlec(_):
    print("Alec! We need you!")


# Sum of at least two expressions (terms)
class Sum(Expression):

    def __init__(self, terms):
        super().__init__(ExpressionType.SUM)
        self.terms = terms
        self.isConstant = None
        self.primaryOrder = 3 # Monomial Sum

        # Checks if any terms are functions

        for term in self.terms:
            if term.primaryOrder > 5: # product or sum of functions
                self.primaryOrder = 6 # Function Sum
            if term.primaryOrder == 5: # Term is function or greater
                if term.secondaryOrder != 8: # Not an exponential (cannot be monomial)
                    self.primaryOrder = 6 # Function Sum
                else: # Is exponential
                    if not ((term.base.primaryOrder == 2) and term.argument.isConstant()): # not a monomial
                        self.primaryOrder = 6 # Function Sum

    def __str__(self):
        string_expression = str(self.terms[0])
        for term in self.terms[1:]:
            string_expression += " + " + str(term)
        return string_expression
    
    def derivative(self, differential):   
        return Sum( tuple(term.derivative(differential) for term in self.terms) )    
    
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
                
        if (self.primaryOrder == other.primaryOrder): # Both sums
            return max(self.terms) > max(other.terms)
        
        else: 
            return self.primaryOrder > other.primaryOrder # Ordering classes

    def isConstant(self):
        if self.isConstant == None: 
            self.isConstant == True
            for term in self.terms:
                if term.isConstant == False:
                    self.isConstant == False
                    break
        return self.isConstant
    
    def genarg(self):#needed for constant simplification (consim)
        return self.terms
    
    def consim(self): #constant simplify
        old = self #we will need this at the end

        #simplifying the terms of the sum (bottom up)
        simterms = () #simplified terms
        for term in self.terms:
            simterms += (term.consim(),)
        
        #replacing anything but fractions with variables
        varterms = () #replace expressions by variables
        for term in simterms:
            if term.expression_type != ExpressionType.FRACTION:
                varargs = () #tuple of arguments with anything but fractions replaced by variables
                for arg in term.genarg(): # the generalised arguments (so also base, power, terms, factors) of each term
                    if arg.expression_type != ExpressionType.FRACTION:
                        arg = Variable(arg) #replacing the argument by a variable (e.g. sqrt(3) becomes x_sqrt(3))
                    varargs += (arg,)
            varterms += (MakeExpression(term.expression_type, varargs),) #remake the term but with the variable arguments, and add the new term to the tuple of terms.

        #asking Alec to simplify the expression with variables  
        alecsim = AskAlec(Sum(varterms))
        if alecsim.expression_type == ExpressionType.SUM:
            alecterms = alecsim.terms
        else: #if alecsim.expression_type != ExpressionType.SUM:
            alecterms = (alecsim,)
        # simvarterms = alecsim.terms #= AskAlec(Sum(varterms)).terms # Does the simplification of a sum always return a sum? is AskAlec(Sum((x, (-1)x))) equal to a sum with one argument, Sum(( (1-1)x )), or to the single_sum_argument, the product (1-1)*x ?: the argument
        
        #We simplify each of the terms
        simalecterms = ()
        for term in alecterms:
            simalecterms += (term.consim(),) #Lets hope this doesn't cause a loop.

        #the only things that are not simplified now should be the original fractions
        #we split the simalecterms between fraction terms and other terms
        from Model.fraction import Frac
        fracsum = Frac(0)
        nonfracsat = () #non fraction terms of simalecterms (hence the sat)
        for term in simalecterms:
            if term.expression_type == ExpressionType.FRACTION:
                fracsum += term #recall that fractional addition gives the simplified sum
            else:
                nonfracsat += (term, )

        #recall we defined old
        if nonfracsat == ():
            new = fracsum.simplify()
        elif fracsum == Frac(0):
            if len(nonfracsat)==1:
                new = nonfracsat[0]
            else: #len(nonfracsvt)>1:
                new = Sum(nonfracsat)
        else:
            new = Sum( nonfracsat + (fracsum,) )
        
        if new == old: #equal in representation
            return new
        else:
            return new.consim() #We sure do hope this doesn't end up looping.

    # To consolidate a sum and remove zero terms. (CONSIM WILL NEED TO USE THIS FOR CONSTANTS)
    def consolidate(self):
        
        popList = []
        appendList = []

        #Zero Elimination + Consolidation step: If any of the terms are also sums, we expand those sums above.

        for term in self.terms:
            # Note that the two statments can never trigger at the same time. 
            if (term.expression_type == ExpressionType.SUM): #If one of the terms itself is a sum. 
                popList.append(term) # Add the term to the removal list
                termsNew = term.consolidate() # Consolidate the inner sum (incase there are any more nested sums)
                for term2 in termsNew.terms:
                    appendList.append(term2) # Add the extracted terms to the append list. 
            elif term == Constant(0):
                popList.append(term) # Remove zero terms (we will do this again later but it is worth doing it now for efficiency)

        for term in popList: # removing the internal sums and zero terms
            self.terms.pop(term)

        for term in appendList:
            self.terms.append(term)

    def pfsf(self):   

        from Model.product import Product

        termsPfsf = []
        for term in self.terms:
            termsPfsf.append(term.pfsf()) # Simplify all the terms

        # termsPsfs is now a simplified terms list that is entirely seperate from the original sum (deep copy + simplify)

        # For consolidation, make this into a sum, consolidate, and then pull terms
        termsPfsf = Sum(termsPfsf).consolidate().terms 

        # We now have a consolidated sum (containing no sums within it) that has no 0 terms and all terms are simplified by psfs
        

        constList = []

        # After consolidated, combine like terms and order

        # We first remove and arrange all of the constants + turn everything into the form product(c, stuff)
        for term in termsPfsf:
            if term.isConstant():
                constList.append(term)
            else:
                if term.expression_type == ExpressionType.PRODUCT: # if it is a product
                    if term.factors[0].isConstant() == False: # if it does not have a constant in front (remember that the constant will always be in front bc all terms are pfsf)
                        term.factors.insert(0, Constant(1)) # add a 1 to the front of the product 
                else: # if not a product
                    term = Product(Constant(1), term) # replace the term with a product of one and itself. 

        for term in constList:
            termsPfsf.pop(term)
        
        # Now, without constants, all that is left to do is join like terms and order. 
        orderedTerms = []
        orderedTerms.append(termsPfsf[0])

        # Remember greatest complexity goes first
        for term in termsPfsf[1:]: # all remaining terms
            added = False
            for index, termComp in enumerate(orderedTerms):
                if Product(term.factors[1:]) == Product(termComp.factors[1:]): # If the parts after the constants are equal
                    # We worry not about consolidating sums here, constant simplifier will do that for constants and we will call it at the end
                    termComp.factors[0] = Sum(termComp.factors[0], term.factors[0]) # Combine the coefficients into the ordered terms list and move on, we no longer worry about the term
                    added = True
                    break # we no longer need to compare with other terms
                elif Product(term.factors[1:]) > Product(termComp.factors[1:]): # This means that it is greater than the current entry, which means it goes before it
                    orderedTerms.insert(index, term) 
                    added = True
                    break # stop comparing because we have found its place
                # If it is not >= it is < than the current entry and thus its place is farther to the right
            # If it has still not been added, append it to the end (it must be < every other term in complexity)
            if added == False:
                orderedTerms.append(term)

        # NOTE - WE ASSUME FROM THIS POINT FORWARD THAT NONE OF THESE TERMS ARE CONSTANTS (i.e. f(x) + g(x) is never a constant unless both f(x) and g(x) are constants). THIS HOLDS FOR NOW BUT DOES NOT HOLD IN GENERAL
        # THINK COS^2 + SIN^2 = 1

        # WE NEED TO IMPLEMENT A LOGARITHM CHECK BEFORE THIS TO CONSOLIDATE Log_b(f(x)) + Log_b(g(x)) into Log_b(f + g (x)) if that is what we want to consider simplified, check later with group
        # In this case we will need to ensure that we can identify if f(x)g(x) = c i.e. g(x) = c * (f(x))^(-1)        

        # This is now fully ordered and basically pfsf. The last thing we need to do is to simplify products with 1s in the front and send all the constants to the constant simplifier 

        popList =  []

        for term in orderedTerms:
            term.factors[0].consim() # Simplify the front constant 
            if term.factors[0] == Constant(1): # If it is a 1
                term.factors.pop(term.factors[0]) # Remove the front factor
            elif term.factors[0] == Constant(0): # If it is a zero
                popList.append[term] # we will remove it
            
            # if neither of these hold, the front is a constant that is not zero or one, so we leave it as is

            if len(term.factors) == 1: # only one element left
                term = term.factors[0] # remove the product brackets essentially 
        
        for term in popList: # removing the zero terms
            orderedTerms.pop(term)

        # now all the terms are simplified to the max with their constants simplified. 

        # After this loop orderedTerms contains all of the terms in pfsf order and simplified. These terms are all non-constant. This means we can add our constant terms from earlier to the end

        orderedTerms.append(Sum(constList).consim()) # Adding the simplified sum of constants to the sum

        # we are finally done (please save me). We just need to do a quick return check

        if len(orderedTerms) == 1: # only one term
            return orderedTerms[0]
        else:
            return Sum(orderedTerms)



        # Thinking now of a way to do summative identities (ie cos^2 + sin^2 = 1). It could be done through the filtering where if one of the parts is identified and compared with another part, they are joined
