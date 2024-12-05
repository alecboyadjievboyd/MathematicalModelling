from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.make_expression import MakeExpression
from Model.variable import Variable
from Model.fraction import Frac

def AskAlec(_):
    print("Alec! We need you!")


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
    
    def genarg(self):#needed for constant simplification (consim)
        return self.terms
    
    def consim(self): #constant simplify
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
                        # hasvar = True
                    varargs += (arg,)
            # if hasvar:
            varterms += (MakeExpression(term.expression_type, varargs),) #remake the term but with the variable arguments, and add the new term to the tuple of turns.

        #asking Alec to simplify the expression with variables  
        simvarterms = AskAlec(Sum(varterms)).terms # Does the simplification of a sum always return a sum? is AskAlec(Sum((x, (-1)x))) equal to a sum with one argument, Sum(( (1-1)x )), or to the single_sum_argument, the product (1-1)*x ?
        
        #the only things that are not simplified now should be the original fractions
        #we split the simvarterms between fraction terms and other terms
        fracsum = Frac(0)
        nonfracsvt = () #non fraction terms of simvarterms (hence the svt)
        for term in simvarterms:
            if term.expression_type == ExpressionType.FRACTION:
                fracsum += term
            else:
                nonfracsvt += (term, )

        return Sum(nonfracsvt + (fracsum,))

    
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
