
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
    TBA
    '''
    def parseMessage(self, streamArn : str, shardId : str, partitionKey : str, sequenceNumber : str, approximateArrivalTimestamp : int, data : bytearray) -> ParseDocumentResult:
        raise(Exception("Not Yet Implemented"))
    
