from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.constant import Constant
from Model.sum import Sum
from Model.product import Product
from Model.exponential import Exponential
from Model.fraction import Frac


def frac_constant_simplify(expression: Expression):
    if expression.expression_type == ExpressionType.CONSTANT:
        return Frac(expression)
    elif expression.expression_type == ExpressionType.FRACTION:#all below should eventually end up calling this
        return expression.simplify()
    elif expression.expression_type == ExpressionType.SUM:
        new_terms = ()
        for term in expression.terms:
            new_terms+= (frac_constant_simplify(term),) #These should all be Frac
        s = Frac(0) #s for sum, but we already defined both sum and Sum
        for term in new_terms:
            s += term
        return s.simplify()
    elif expression.expression_type == ExpressionType.PRODUCT: #compare to previous elif, == ExpressionType.SUM
        new_factors = ()
        for factor in expression.factors:
            new_factors += (frac_constant_simplify(factor),) #These should all be Frac
        p = Frac(1) #p for product, but we already defined both product and Product
        for factor in new_factors:
            p *= factor
        return p.simplify()
    elif expression.expression_type == ExpressionType.EXPONENTIAL:
        base = frac_constant_simplify(expression.base) #This should be Frac
        exponent = frac_constant_simplify(expression.exponent) #This should be Frac
        returnable = base**exponent
        return returnable.simplify()
        
    else:
        raise Exception("You are asking me to simplify something really scary")