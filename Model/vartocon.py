#VARiable TO CONstant
#a brute force algorithm to replace variables by their associated constants, as needed for consim.
#does not check for variables inside the index of other variables (as that shouldn't be necessary)

from Model.expression import Expression
from Model.expression_type import ExpressionType
from Model.make_expression import MakeExpression

def Vartocon(expr: Expression):
    # try:
    if True:
        if expr.expression_type == ExpressionType.VARIABLE:
            return expr.index
        elif expr.expression_type == ExpressionType.FRACTION or expr.expression_type == ExpressionType.PI or expr.expression_type == ExpressionType.EULER:
            return expr    
        elif expr.expression_type == ExpressionType.INTEGER: #shouldn't occur, but for testing might be nice. 
            return expr
        elif expr.expression_type == ExpressionType.HYPERVARIABLE:
            return expr
        else:
            newarg = ()
            for arg in expr.genarg():
                newarg += (Vartocon(arg),)

            return MakeExpression(expr.expression_type, newarg)
    # except:
    #     raise Exception(f"Vartocon crashes on {expr}")
        