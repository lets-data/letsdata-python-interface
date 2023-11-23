from letsdata_interfaces.documents.Document import Document
from letsdata_interfaces.documents.DocumentType import DocumentType

class SingleDoc(Document):
    def __init__(self, documentType : DocumentType, documentId : str, recordType : str, partitionKey : str, documentMetadata : dict , documentKeyValuesMap : dict) -> None:
        super().__init__(documentType, documentId, recordType, partitionKey, documentMetadata, documentKeyValuesMap)
    
    def isSingleDoc()-> bool:
        return True
    
