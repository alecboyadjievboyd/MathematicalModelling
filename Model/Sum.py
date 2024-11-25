import Expression
import ExpressionType

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
    
    def derivative(self, differential):   
        return Sum( tuple(term.derivative(differential) for term in self.terms) )