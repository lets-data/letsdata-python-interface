
import uuid
from letsdata_interfaces.readers.model.RecordParseHint import RecordParseHint
from letsdata_interfaces.readers.model.RecordHintType import RecordHintType
from letsdata_interfaces.readers.model.ParseDocumentResultStatus import ParseDocumentResultStatus
from letsdata_interfaces.readers.model.ParseDocumentResult import ParseDocumentResult
from letsdata_interfaces.documents.Document import Document
from letsdata_interfaces.documents.DocumentType import DocumentType
from letsdata_interfaces.documents.ErrorDoc import ErrorDoc
from letsdata_utils.logging_utils import logger

class DynamoDBStreamsRecordReader:
    def __init__(self) -> None:
        pass
        
    '''
     The #LetsData DynamoDB Streams Record Reader uses this interface's implementation (also called as user data handlers) to transform the records from DynamoDB stream to a #LetsData document. At a high level, the overall #LetsData DynamoDB Stream reader design is as follows:

     * #LetsData reads the records from the DynamoDB stream from the specified location (sequenceNumber) and passes the record contents to the user data handlers.
     * The user data handlers transform this record and returns a document.
     * #LetsData writes the document to the write / error destinations and checkpoints the location (sequenceNumber) in DynamoDB stream.
     * For any errors in #LetsData DynamoDB Streams Reader, or error docs being returned by the user data handler, #LetsData looks at the reader configuration and determines 1./ whether to fail the task with error 2./ or write an error doc and continue processing
     * If the decision is to continue processing, the reader polls for next record in the stream.

     +---------------------+                              +---------------------+                        +---------------------+
     | AWS DynamoDB Stream | ------ Read Message -------> |    # Lets Data      |---- parseDocument ---> |  User Data Handler  |
     |       Shard         |                              |  DDB Stream Reader  |<---- document -------- |                     |
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

     The DynamoDB Streams read connector configuration has details about the DynamoDB Streams read and on dealing with failures.

     For detailed explanation of the parameters, see AWS docs:
        * https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_streams_Record.html
        * https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_streams_StreamRecord.html
     
     Parameters
     ----------
     streamArn : str
                      The Kinesis streamArn
     shardId   : str
                      The DynamoDB Shard Id
     eventId : str
                      A globally unique identifier for the event that was recorded in this stream record.
     eventName : str
                      The type of data modification that was performed on the DynamoDB table. INSERT | MODIFY | REMOVE
     identityPrincipalId : str
                      The userIdentity's principalId
     identityType : str
                      The userIdentity's principalType
     sequenceNumber : str
                      The sequence number of the stream record
     sizeBytes : str
                      The size of the stream record, in bytes
     streamViewType : str
                      The stream view type - NEW_IMAGE | OLD_IMAGE | NEW_AND_OLD_IMAGES | KEYS_ONLY
     approximateCreationDateTime : int 
                      The approximate date and time when the stream record was created, in UNIX epoch time format and rounded down to the closest second
     keys : str
                      The primary key attribute(s) for the DynamoDB item that was modified
     oldImage : str
                      The item in the DynamoDB table as it appeared before it was modified
     newImage : str
                      The item in the DynamoDB table as it appeared after it was modified
     
     Returns
     -------
     ParseDocumentResult 
        ParseDocumentResult has the extracted document and the status (error, success or skip)
    '''
    def parseRecord(self, streamArn : str, shardId : str, eventId : str, eventName : str, identityPrincipalId : str, identityType : str, sequenceNumber : str, sizeBytes : int, streamViewType : str, approximateCreationDateTime : int, keys : {}, oldImage : {}, newImage : {}) -> ParseDocumentResult:
        raise(Exception("Not Yet Implemented"))
    

