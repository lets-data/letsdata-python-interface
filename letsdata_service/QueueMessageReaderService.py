
from letsdata_utils.logging_utils import logger
from letsdata_service.Service import ServiceRequest, LetsDataAuthParams, InterfaceNames
from letsdata_utils.validations import letsdata_assert
from letsdata_interfaces.readers.sqs.QueueMessageReader import QueueMessageReader
    
class QueueMessageReader_ParseMessage(ServiceRequest):
    def __init__(self, requestId: str, letsDataAuth: LetsDataAuthParams, interfaceName : InterfaceNames, functionName : str, messageId : str, messageGroupId : str, messageDeduplicationId : str, messageAttributes : {}, messageBody : str) -> None: 
        super().__init__(requestId, letsDataAuth, interfaceName, functionName)
        self.messageId = messageId
        self.messageGroupId = messageGroupId
        self.messageDeduplicationId = messageDeduplicationId
        self.messageAttributes = messageAttributes
        self.messageBody = messageBody
    
    def execute(self): 
        parser = QueueMessageReader()
        return  parser.parseMessage(self.messageId, self.messageGroupId, self.messageDeduplicationId, self.messageAttributes, self.messageBody)

def getQueueMessageReaderServiceRequest(requestId : str, letsDataAuth: LetsDataAuthParams, interfaceName : InterfaceNames, functionName : str, data : {}, batchedData : []):
    letsdata_assert(interfaceName == InterfaceNames.QueueMessageReader, "invalid interfaceName - expected QueueMessageReader, got "+str(interfaceName))
    letsdata_assert(letsDataAuth is not None, "invalid letsDataAuth - None")
    
    QueueMessageReaderInterfaceNames = set(["parseMessage"])    

    if functionName not in QueueMessageReaderInterfaceNames:
            raise(Exception("lambda event - invalid functionName "+functionName+" for interface QueueMessageReader"))
    
    if functionName == "parseMessage":
        letsdata_assert(batchedData is None or len(batchedData) == 0, "invalid batchedData - QueueMessageReader.parseMessage requires empty batchedData dictionary")
        letsdata_assert(isinstance(data, dict) and len(data) >= 3 and len(data) <= 5, "invalid data - QueueMessageReader.parseMessage requires data keys [messageId, messageGroupId, messageDeduplicationId, messageAttributes, messageBody]")
        
        letsdata_assert(not data['messageId'] is None, "invalid messageId - None - QueueMessageReader.parseMessage requires data keys [messageId, messageAttributes, messageBody] and optionally [messageGroupId, messageDeduplicationId]")
        letsdata_assert(isinstance(data['messageId'], str), "invalid messageId - QueueMessageReader.parseMessage requires messageId value to be string")

        messageGroupId = None
        if 'messageGroupId' in data.keys():
            letsdata_assert(isinstance(data['messageGroupId'], str), "invalid messageGroupId - QueueMessageReader.parseMessage requires messageGroupId value to be string")
            messageGroupId = data['messageGroupId']

        messageDeduplicationId = None
        if 'messageDeduplicationId' in data.keys():
            letsdata_assert(isinstance(data['messageDeduplicationId'], str), "invalid messageDeduplicationId - QueueMessageReader.parseMessage requires messageDeduplicationId value to be string")
            messageDeduplicationId = data['messageDeduplicationId']
        
        letsdata_assert(not data['messageAttributes'] is None, "invalid messageAttributes - None - QueueMessageReader.parseMessage requires data keys [messageId, messageAttributes, messageBody] and optionally [messageGroupId, messageDeduplicationId]")
        letsdata_assert(isinstance(data['messageAttributes'], dict), "invalid messageAttributes - QueueMessageReader.parseMessage requires messageAttributes value to be string")
        
        letsdata_assert(not data['messageBody'] is None, "invalid messageBody - None - QueueMessageReader.parseMessage requires data keys [messageId, messageAttributes, messageBody] and optionally [messageGroupId, messageDeduplicationId]")
        letsdata_assert(isinstance(data['messageBody'], str), "invalid messageBody - QueueMessageReader.parseMessage requires messageBody value to be str")

        return QueueMessageReader_ParseMessage(requestId, letsDataAuth, interfaceName, functionName, data['messageId'], messageGroupId, messageDeduplicationId, data['messageAttributes'], data['messageBody'])
    else:
        raise(Exception("Unknown functionName"))
    