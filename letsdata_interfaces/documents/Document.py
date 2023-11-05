import json
from letsdata_interfaces.documents.DocumentType import DocumentType

'''
 * The "DocumentInterface" is the base interface for any document that can be returned by the user handlers. All other document interfaces and documents either extend or implement this interface.
 '''
class Document: 
    def __init__(self, documentType: DocumentType, documentId : str, recordType : str, partitionKey : str, documentMetadata : dict , documentKeyValuesMap : dict):
        self.documentType = documentType
        self.documentId = documentId
        self.recordType = recordType
        self.partitionKey = partitionKey
        self.documentMetadata = documentMetadata
        self.documentKeyValuesMap = documentKeyValuesMap

    def getDocumentType(self) -> str:
      return self.documentType

    '''
     * Gets the documentId for the document
     * @return documentId
     '''
    def getDocumentId(self) -> str:
      return self.documentId

    '''
     * Gets the record type of the document
     * @return the record type
     '''
    def getRecordType(self) -> str:
        return self.recordType
    
    '''
     * Gets any optional metadata for the document as a map
     * @return map of optional document metadata
    '''
    def getDocumentMetadata(self) -> dict:
       return self.documentMetadata

    '''
     * Interface method that serializes the document to string that can be written to the destination
     * @return serialized document as string
    '''
    def serialize(self) -> str:
        return json.dumps(self)
    
    '''
     * The partition key of the document - useful to determine the partition for the document that would be written to
     * @return the partition key for the document
    '''
    def getPartitionKey(self) -> str:
        return self.partitionKey
    
    '''
    '''
    def getDocumentKeyValuesMap(self) -> dict:
        return self.documentKeyValuesMap
    
