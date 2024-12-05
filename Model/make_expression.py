from Model.expression_type import ExpressionType
#other imports are only called when needed, to prevent circular imports

def MakeExpression(Etype, genarg): #ExpressionType and the generalised arguments
    if Etype == ExpressionType.ARCCOSINE:
        return Arccosine(genarg[0]) #genarg should contain only one element
    elif Etype == ExpressionType.ARCSINE:
        return Arcsine(genarg[0])
    elif Etype == ExpressionType.ARCTANGENT:
        return Arctangent(genarg[0])
    elif Etype == ExpressionType.CONSTANT:
        from Model.constant import Constant
        return Constant(genarg[0])
    elif Etype == ExpressionType.COSINE:
        return Cosine(genarg[0])
    elif Etype == ExpressionType.EXP:
        from Model.exp import Exp
        return Exp(genarg[0])
    elif Etype == ExpressionType.EXPONENTIAL:
        from Model.exponential import Exponential
        return Exponential(genarg[0], genarg[1]) #base=0, exponent=1
    elif Etype == ExpressionType.FRACTION:
        return Frac(genarg[0],genarg[1])
    elif Etype == ExpressionType.GENERALMULTIVAR:
        from Model.general_multivar import GeneralMultivar
        return GeneralMultivar(genarg[0])
    elif Etype == ExpressionType.GENERALSINGLEVAR:
        from Model.general_singlevar import GeneralSinglevar
        return GeneralSinglevar(genarg[0], genarg[1])
    elif Etype == ExpressionType.LOGARITHM:
        from Model.logarithm import Logarithm
        return Logarithm(genarg[0],genarg[1])
    elif Etype == ExpressionType.PRODUCT:
        from Model.product import Product
        return Product(genarg)
    elif Etype == ExpressionType.SINE:
        from Model.sine import Sine
        return Sine(genarg[0])
    elif Etype == ExpressionType.SUM:
        from Model.sum import Sum
        return Sum(genarg)
    elif Etype == ExpressionType.TANGENT:
        return Tangent(genarg[0])
    elif Etype == ExpressionType.VARIABLE:
        from Model.variable import Variable
        return Variable(genarg[0])