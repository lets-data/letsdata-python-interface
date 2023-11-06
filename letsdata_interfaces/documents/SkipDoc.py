from letsdata_interfaces.documents.SingleDoc import SingleDoc
from letsdata_interfaces.documents.DocumentType import DocumentType

class SkipDoc(SingleDoc):
    def __init__(self, documentId : str, recordType : str, partitionKey : str, documentMetadata : dict , documentKeyValuesMap : dict, errorStartoffsetMap : dict, errorEndoffsetMap: dict, skipMessage : str) -> None:
        super.__init__(DocumentType.SkipDoc, documentId, recordType, partitionKey, documentMetadata, documentKeyValuesMap)
        self.errorStartoffsetMap = errorStartoffsetMap
        self.errorEndoffsetMap = errorEndoffsetMap
        self.skipMessage = skipMessage

    
    '''
     * The erroneous record start offset (in bytes) of the error record in the files by file types
     * For 'Single File' and 'Single File State Machine' readers, there would be a single file type in the return map.
     * For example,
     *  {
     *      "CLICKSTREAMLOGS": "58965"
     *  }
     *  For 'Multiple File State Machine' readers, the return map should have offsets (in bytes) into each of the files.
     *  For example,
     *  {
     *      "METADATALOG": "58965",
     *      "DATALOG": "5484726",
     *  }
     * @return Map of &lt;FileType, RecordStartOffsetInBytes&gt;
    '''
    def getErrorStartOffsetMap(self) -> dict:
        return self.errorStartoffsetMap

    '''
     * The erroneous record end offset (in bytes) of the error record in the files by file types
     * For 'Single File' and 'Single File State Machine' readers, there would be a single file type in the return map.
     * For example,
     *  {
     *      "CLICKSTREAMLOGS": "58965"
     *  }
     *  For 'Multiple File State Machine' readers, the return map should have offsets (in bytes) into each of the files.
     *  For example,
     *  {
     *      "METADATALOG": "58965",
     *      "DATALOG": "5484726",
     *  }
     * @return Map of &lt;FileType, RecordEndOffsetInBytes&gt;
     '''
    def getErrorEndOffsetMap(self) -> dict:
        return self.errorEndoffsetMap

    '''
     * The error message string that will be captured in the error record
     * @return The error message string
    '''
    def getSkipMessage(self) -> str:
        return self.skipMessage