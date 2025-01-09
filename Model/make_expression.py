from Model.expression_type import ExpressionType
#other imports are only called when needed, to prevent circular imports

def MakeExpression(Etype, genarg): #ExpressionType and the generalised arguments
    if Etype == ExpressionType.ARCCOSINE:
        from Model.arccosine import Arccosine
        return Arccosine(genarg[0]) #genarg should contain only one element
    elif Etype == ExpressionType.ARCSINE:
        from Model.arcsine import Arcsine
        return Arcsine(genarg[0])
    elif Etype == ExpressionType.ARCTANGENT:
        from Model.arctangent import Arctangent
        return Arctangent(genarg[0])
    elif Etype == ExpressionType.INTEGER:
        from Model.integer import Integer
        return Integer(genarg[0])
    elif Etype == ExpressionType.COSINE:
        from Model.cosine import Cosine
        return Cosine(genarg[0])
    elif Etype == ExpressionType.EULER:
        from Model.euler import Euler
        return Euler()
    elif Etype == ExpressionType.EXP:
        from Model.exp import Exp
        return Exp(genarg[0])
    elif Etype == ExpressionType.EXPONENTIAL:
        from Model.exponential import Exponential
        return Exponential(genarg[0], genarg[1]) #base=0, exponent=1
    elif Etype == ExpressionType.FRACTION:
        from Model.fraction import Frac
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
    elif Etype == ExpressionType.PI:
        from Model.pi import Pi
        return Pi()
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
        from Model.tangent import Tangent
        return Tangent(genarg[0])
    elif Etype == ExpressionType.VARIABLE:
        from Model.variable import Variable
        return Variable(genarg[0])