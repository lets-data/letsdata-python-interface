from enum import Enum

class DocumentType(str, Enum):
    CompositeDoc = "CompositeDoc"
    Document = "Document"
    ErrorDoc = "ErrorDoc"
    SingleDoc = "SingleDoc"
    SkipDoc = "SkipDoc"

    @classmethod
    def fromValue(cls, enumValue):
        return cls(enumValue)