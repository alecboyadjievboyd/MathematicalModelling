from expression import Expression
from expression_type import ExpressionType
from enum import Enum


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
        match self.constant_type:
            case ConstantType.INTEGER:
                return str(self.value)
            case ConstantType.PI:
                return 'pi'
            case ConstantType.EULER:
                return 'e'

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


class ConstantType(Enum):
    INTEGER = 1
    PI = 2
    EULER = 3
