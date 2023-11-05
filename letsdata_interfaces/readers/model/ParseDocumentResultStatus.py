from enum import Enum

class ParseDocumentResultStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    SKIP = "SKIP"

    @classmethod
    def fromValue(cls, enumValue):
        return cls(enumValue)