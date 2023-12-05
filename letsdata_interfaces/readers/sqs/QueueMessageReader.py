
import uuid
import json
from letsdata_interfaces.readers.model.RecordParseHint import RecordParseHint
from letsdata_interfaces.readers.model.RecordHintType import RecordHintType
from letsdata_interfaces.readers.model.ParseDocumentResultStatus import ParseDocumentResultStatus
from letsdata_interfaces.readers.model.ParseDocumentResult import ParseDocumentResult
from letsdata_interfaces.documents.Document import Document
from letsdata_interfaces.documents.DocumentType import DocumentType
from letsdata_interfaces.documents.ErrorDoc import ErrorDoc
from letsdata_utils.logging_utils import logger

class QueueMessageReader:
    def __init__(self) -> None:
        pass
        
    '''
    /**
     The Implementation simply echoes the incoming record. You could add custom logic as needed.

     * @param messageId The SQS message messageId
     * @param messageGroupId The SQS message messageGroupId
     * @param messageDeduplicationId The SQS message messageDeduplicationId
     * @param messageAttributes The SQS message messageAttributes
     * @param messageBody The SQS message messageBody
     * @return ParseDocumentResult which has the extracted document and the status (error, success or skip)
     */
     '''
    def parseMessage(self, messageId : str, messageGroupId : str, messageDeduplicationId : str, messageAttributes : {}, messageBody : str) -> ParseDocumentResult:
        if not messageBody.strip():
            logger.debug(f"message body is blank, returning error - messageId: {messageId}, messageGroupId: {messageGroupId}, messageDeduplicationId: {messageDeduplicationId}, messageAttributes: {messageAttributes}, messageBody: {messageBody}")
            error_doc = ErrorDoc(str(uuid.uuid4()), "SQS_ERROR", messageId, {}, {}, None, None, "empty message body")
            return ParseDocumentResult(None, error_doc, "ERROR")
        try:
            logger.debug(f"processing message - messageId: {messageId}")
            keyValuesMap = json.loads(messageBody)
            logger.debug(f"returning success - docId: {keyValuesMap['documentId']}")
            return ParseDocumentResult(str(uuid.uuid4()), Document(DocumentType.Document, keyValuesMap['documentId'], "DOCUMENT", keyValuesMap['partitionKey'], {}, keyValuesMap), "SUCCESS")
        except json.JSONDecodeError as ex:
            logger.debug(f"JSONDecodeError in reading the document - messageId: {messageId}, messageGroupId: {messageGroupId}, messageDeduplicationId: {messageDeduplicationId}, messageAttributes: {messageAttributes}, messageBody: {messageBody}")
            error_doc = ErrorDoc(str(uuid.uuid4()), None, f"JSONDecodeError - {ex.msg}", messageId, None, None, f"JSONDecodeError - {ex.msg}", messageBody)
            return ParseDocumentResult(None, error_doc, ParseDocumentResultStatus.ERROR)
    
