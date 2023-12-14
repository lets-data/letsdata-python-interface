
import uuid
from letsdata_interfaces.readers.model.RecordParseHint import RecordParseHint
from letsdata_interfaces.readers.model.RecordHintType import RecordHintType
from letsdata_interfaces.readers.model.ParseDocumentResultStatus import ParseDocumentResultStatus
from letsdata_interfaces.readers.model.ParseDocumentResult import ParseDocumentResult
from letsdata_interfaces.documents.Document import Document
from letsdata_interfaces.documents.DocumentType import DocumentType
from letsdata_interfaces.documents.ErrorDoc import ErrorDoc
from letsdata_utils.logging_utils import logger

class KinesisRecordReader:
    def __init__(self) -> None:
        pass
        
    '''
     The #Lets Data Kinesis Stream Reader uses this interface's implementation (also called as user data handlers) to transform the messages from Kinesis Stream record to a #Lets Data document. At a high level, the overall # Lets Data Kinesis reader design is as follows:

     * #Lets Data reads the records from the Kinesis stream and passes the message contents to the user data handlers.
     * The user data handlers transform this message and returns a document.
     * #Lets data writes the document to the write / error destinations and then checkpoints the task with the processed sequence number.
     * For any errors in # Lets Data Kinesis Stream Reader, or error docs being returned by the user data handler, #Lets Data looks at the reader configuration and determines 1./ whether to fail the task with error 2./ or write an error doc and continue processing
     * If the decision is to continue processing, the reader polls for next stream record.

     +---------------------+                              +---------------------+                        +---------------------+
     |                     | ------ Read Message -------> |    # Lets Data      |---- parseDocument ---> |  User Data Handler  |
     |                     |                              |   Kinesis Reader    |<---- document -------- |                     |
     |                     |                              |                     |                        +---------------------+
     | AWS Kinesis Stream  |                              |   Is Error Doc?     |
     |                     |                              |        |            |                        +---------------------+
     |                     |                              |        +---- yes ->-|---- write document --->|  Write Destination  |
     |                     |                              |        |            |                        +---------------------+
     +---------------------+                              |        |            |                        +---------------------+
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

     The Kinesis read connector configuration has details about the Kinesis read config and on dealing with failures.

     Parameters
     ----------
     streamArn : str
                 The Kinesis streamArn
     shardId   : str
                 The stream record's shardId
     partitionKey : str
                    The stream record's partition key
     sequenceNumber : str
                      The stream record's sequenceNumber
     approximateArrivalTimestamp : int 
                                   The stream record's approximateArrivalTimestamp
     data : bytearray
            The stream record's data payload as a ByteBuffer
     
     Returns
     -------
     ParseDocumentResult 
        ParseDocumentResult has the extracted document and the status (error, success or skip)
    '''
    def parseMessage(self, streamArn : str, shardId : str, partitionKey : str, sequenceNumber : str, approximateArrivalTimestamp : int, data : bytearray) -> ParseDocumentResult:
        raise(Exception("Not Yet Implemented"))
    
