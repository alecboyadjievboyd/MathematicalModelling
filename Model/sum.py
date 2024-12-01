from constant import Constant
from expression import Expression
from expression_type import ExpressionType

# Sum of at least two expressions (terms)
class Sum(Expression):

    def __init__(self, terms):
        super().__init__(ExpressionType.SUM)
        self.terms = terms
        self.isConstant = None

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

    def isConstant(self):
        if self.isConstant == None: 
            self.isConstant == True
            for term in self.terms:
                if term.isConstant == False:
                    self.isConstant == False
                    break
        return self.isConstant
            
    
    # def pfsfSimple(self):   
     
    #     zeroList = []
    #     popList = []
    #     appendList = []
    #     #Zero Elimination + Consolidation step: If any of the terms are also sums, we expand those sums above.
    #     for term in self.terms[1:]:
    #         # Note that the two statments can never trigger at the same time. 
    #         if (term.expression_type == ExpressionType.SUM): #If one of the terms itself is a sum. 
    #             termsNew = term.pfsfSimple() # Simplify the inner sum (incase there are any more nested sums)
    #             popList.append(term) # Add the term to the removal list
    #             for term2 in termsNew.terms[1:]:
    #                 appendList.append(term2) # Add the extracted terms to the append list. 
    #         if term == Constant(0):
    #             zeroList(term) # Remove constant terms

    #     # After consolidated, combine like terms. We assume that all terms are already consolidated and pfsf 
    #     for term in self.terms[1:]:
