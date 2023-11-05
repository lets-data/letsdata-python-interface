from enum import Enum

class Stage(Enum):
    Test = "Test"
    Prod = "Prod"

    @classmethod
    def fromValue(cls, enumValue):
        return cls(enumValue)
