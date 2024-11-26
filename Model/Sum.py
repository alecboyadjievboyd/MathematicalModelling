from Constant import Constant
from Expression import Expression
from expression_type import ExpressionType

# Sum of at least two expressions (terms)
class Sum(Expression):

    def __init__(self, terms):
        super().__init__(ExpressionType.SUM)
        self.terms = terms

    def __str__(self):
        string_expression = str(self.terms[0])
        for term in self.terms[1:]:
            string_expression += " + " + str(term)
        return string_expression
    
    # This function basically does a "mutual elimination" thing, cutting down copies of both lists until both copies are empty by removing
    # pairs of equivalent terms. 
    # If any elements cannot be removed from one or both lists then they are not equal.
    def __eq__(self, other):

        if (self.expression_type != other.expression_type):
            return False
        
        selfTerms = self.terms.copy()
        otherTerms = other.terms.copy()

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
            
    
    def pfsfSimple(self):   
     
        zeroList = []
        popList = []
        appendList = []
        #Zero Elimination + Consolidation step: If any of the terms are also sums, we expand those sums above.
        for term in self.terms[1:]:
            # Note that the two statments can never trigger at the same time. 
            if (term.expression_type == ExpressionType.SUM): #If one of the terms itself is a sum. 
                termsNew = term.pfsfSimple() # Simplify the inner sum (incase there are any more nested sums)
                popList.append(term) # Add the term to the removal list
                for term2 in termsNew.terms[1:]:
                    appendList.append(term2) # Add the extracted terms to the append list. 
            if term == Constant(0):
                zeroList(term) # Remove constant terms

        # After consolidated, combine like terms. We assume that all terms are already consolidated and pfsf 
        for term in self.terms[1:]: 



        