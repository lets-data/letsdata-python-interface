
import uuid
import json
from datetime import datetime
from collections import namedtuple
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
    The Implementation simply echoes the incoming record. You could add custom logic as needed.
    '''
    def parseMessage(self, streamArn : str, shardId : str, partitionKey : str, sequenceNumber : str, approximateArrivalTimestamp : int, data : bytearray) -> ParseDocumentResult:
        if data is None or len(data) <= 0:
            logger.error(f"record data is null or empty, returning error - streamArn: {streamArn}, shardId: {shardId}, partitionKey: {partitionKey}, sequenceNumber: {sequenceNumber}, approximateArrivalTimestamp: {approximateArrivalTimestamp}, data: {data}")
            error_doc = ErrorDoc(str(uuid.uuid4()), "KINESIS_ERROR", partitionKey, {}, {}, {"sequenceNumber": sequenceNumber}, {"sequenceNumber": sequenceNumber}, "empty message body")
            return ParseDocumentResult(None, error_doc, "ERROR")

        try:
            logger.debug(f"processing record - sequenceNumber: {sequenceNumber}")
            keyValuesMap = json.loads(data)
            logger.debug(f"returning success - docId: {keyValuesMap['documentId']}")
            return ParseDocumentResult(None, Document(DocumentType.Document, keyValuesMap['documentId'], "DOCUMENT", partitionKey, {}, keyValuesMap), "SUCCESS")
        except Exception as ex:
            logger.debug(f"Exception in reading the document - streamArn: {streamArn}, shardId: {shardId}, partitionKey: {partitionKey}, sequenceNumber: {sequenceNumber}, approximateArrivalTimestamp: {approximateArrivalTimestamp}, data: {data}, ex: {ex}")
            error_doc = ErrorDoc(str(uuid.uuid4()), "KINESIS_ERROR", partitionKey, {}, {}, {"sequenceNumber": sequenceNumber}, {"sequenceNumber": sequenceNumber}, f"Exception - {ex}")
            return ParseDocumentResult(None, error_doc, "ERROR")
    
