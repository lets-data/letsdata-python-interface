from letsdata_interfaces.readers.model import RecordHintType 
from letsdata_utils.validations import letsdata_assert

class RecordParseHint:

    def __init__(self, recordHintType : RecordHintType, pattern : str, offset : int) -> None:
        self.recordHintType = recordHintType
        self.pattern = pattern
        self.offset = offset

    def  getRecordHintType(self) -> RecordHintType: 
        return self.recordHintType
    
    def getPattern(self) -> str: 
        letsdata_assert(self.recordHintType == RecordHintType.PATTERN, "getStringMatchPattern - invalid accessor called for recordHintType")
        return self.pattern
    
    def getOffset(self) -> int:
        letsdata_assert(self.recordHintType == RecordHintType.OFFSET, "getOffset - invalid accessor called for recordHintType")
        return self.offset
