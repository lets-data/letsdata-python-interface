from enum import Enum

class RecordHintType(str,Enum):
    OFFSET = "OFFSET"
    PATTERN = "PATTERN"

    @classmethod
    def fromValue(cls, enumValue):
        return cls(enumValue)