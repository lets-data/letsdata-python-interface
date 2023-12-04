from enum import Enum

class DocumentType(str, Enum):
    Document = "Document"
    ErrorDoc = "ErrorDoc"
    SkipDoc = "SkipDoc"

    @classmethod
    def fromValue(cls, enumValue):
        return cls(enumValue)