from enum import Enum

class ParseDocumentResultStatus(str, Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    SKIP = "SKIP"

    @classmethod
    def fromValue(cls, enumValue):
        return cls(enumValue)