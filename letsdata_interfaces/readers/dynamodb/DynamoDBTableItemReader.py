
import uuid
from letsdata_interfaces.readers.model.RecordParseHint import RecordParseHint
from letsdata_interfaces.readers.model.RecordHintType import RecordHintType
from letsdata_interfaces.readers.model.ParseDocumentResultStatus import ParseDocumentResultStatus
from letsdata_interfaces.readers.model.ParseDocumentResult import ParseDocumentResult
from letsdata_interfaces.documents.Document import Document
from letsdata_interfaces.documents.DocumentType import DocumentType
from letsdata_interfaces.documents.ErrorDoc import ErrorDoc
from letsdata_utils.logging_utils import logger

class DynamoDBTableItemReader:
    def __init__(self) -> None:
        pass
        
    '''
    The #LetsData DynamoDB Table Item Reader uses this interface's implementation (also called as user data handlers) to transform the records from DynamoDB Item to a #LetsData document. At a high level, the overall #LetsData DynamoDB Table Item Reader design is as follows:

        * #LetsData scans the DynamoDB table and passes the items to the user data handlers.
        * The user data handlers transform this record and returns a document.
        * #LetsData writes the document to the write / error destinations and checkpoints the DynamoDB table's location (lastEvaluatedKey)
        * For any errors in #LetsData DynamoDB Table Item Reader, or error docs being returned by the user data handler, #LetsData looks at the reader configuration and determines 1./ whether to fail the task with error 2./ or write an error doc and continue processing
        * If the decision is to continue processing, the reader polls for next record in the stream.

        +---------------------+                              +---------------------+                        +---------------------+
        | AWS DynamoDB Table  | ------ Read Items - -------> |    # Lets Data      |---- parseDocument ---> |  User Data Handler  |
        |       Scan          |                              |  DDB Table Reader   |<---- document -------- |                     |
        +---------------------+                              |                     |                        +---------------------+
                                                            |   Is Error Doc?     |
                                                            |        |            |                        +---------------------+
                                                            |        +---- yes ->-|---- write document --->|  Write Destination  |
                                                            |        |            |                        +---------------------+
                                                            |        |            |                        +---------------------+
                                                            |        +---- no -->-|---- write error ------>|  Error Destination  |
                                                            |        |            |                        +---------------------+
                                                            | Should Checkpoint?  |
                                                            |        |            |
                ---<------- Checkpoint Task --------<------|<- yes -+            |
                                                            |        |            |
                                                            |        |            |
                                                            | Throw on Error?     |
                                                            |<- yes -+            |
                                                            |        |            |
                                                            |        V            |
                                                            |  Throw on Error     |
                                                            +---------------------+

     Parameters
     ----------
     tableName : str
                      The DynamoDB tableName
     segmentNumber : str
                      The DynamoDB scan segment number
     keys : str
                      The primary key attribute(s) for the scanned DynamoDB item 
     item : str
                      The scanned DynamoDB table item  
     
     Returns
     -------
     ParseDocumentResult 
        ParseDocumentResult has the extracted document and the status (error, success or skip)
    '''
    def parseDynamoDBItem(self, tableName : str, segmentNumber : int, keys : {}, item : {}) -> ParseDocumentResult:
        raise(Exception("Not Yet Implemented"))
    

