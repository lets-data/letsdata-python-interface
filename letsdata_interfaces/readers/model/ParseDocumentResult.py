from letsdata_interfaces.readers.model import ParseDocumentResultStatus
from letsdata_interfaces.documents import Document
class ParseDocumentResult:

    def __init__(self, nextRecordType : str, document : Document, status : ParseDocumentResultStatus):
        self.nextRecordType = nextRecordType
        self.document = document
        self.status = status

    def getNextRecordType(self) -> str: 
        return self.nextRecordType
    
    def getDocument(self) -> Document:
        return self.document
    
    def getStatus(self) -> ParseDocumentResultStatus:
        return self.status
    
