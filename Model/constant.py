from Model.expression import Expression
from Model.expression_type import ExpressionType
from enum import Enum
from Model.fraction import Frac


# Terminal constant value. Either integer or euler number or pi.
class Constant(Expression):

    def __init__(self, value):
        super().__init__(ExpressionType.CONSTANT)
        if type(value) == int:
            self.constant_type = ConstantType.INTEGER
            self.value = value
        elif value == 'e':
            self.constant_type = ConstantType.EULER
        elif value == 'pi':
            self.constant_type = ConstantType.PI
        else:
            raise Exception("Constant has to be integer or e or pi")

    def __str__(self):
        if type(self.value)==int:
            if self.value >= 0:
                return str(self.value)
            else:
                return f'({str(self.value)})'
        else: 
            return('pi or e')
        # match self.constant_type:
        #     case ConstantType.INTEGER:
        #         if self.value >= 0:
        #             return str(self.value)
        #         else:
        #             return f'({str(self.value)})'
        #     case ConstantType.PI:
        #         return 'pi'
        #     case ConstantType.EULER:
        #         return 'e'

    def __eq__(self, other):
        if self.expression_type != other.expression_type:
            return False
        if str(self) == str(other):
            return True
        else:
            return False

    def isConstant(self):
        return True

    def derivative(self, differential):
        return Constant(0)

    def pfsf(self):
        return Constant(self.value)

    def genarg(self):#needed for constant simplification (consim)
        if self.constant_type == ConstantType.INTEGER:
            return (self.value,)
        elif self.constant_type == ConstantType.EULER:
            return ('e')
        elif self.constant_type == ConstantType.PI:
            return ('pi')
        
    def consim(self):
        return Frac(self)

class ConstantType(Enum):
    INTEGER = 1
    PI = 2
    EULER = 3
