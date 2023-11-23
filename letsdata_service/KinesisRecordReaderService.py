
from letsdata_utils.logging_utils import logger
from letsdata_service.Service import ServiceRequest, LetsDataAuthParams, InterfaceNames
from letsdata_utils.validations import letsdata_assert
from letsdata_interfaces.readers.kinesis.KinesisRecordReader import KinesisRecordReader
    
class KinesisRecordReader_ParseMessage(ServiceRequest):
    def __init__(self, requestId: str, letsDataAuth: LetsDataAuthParams, interfaceName : InterfaceNames, functionName : str, streamArn : str, shardId : str, partitionKey : str, sequenceNumber : str, approximateArrivalTimestamp : int, data : str) -> None: 
        super().__init__(requestId, letsDataAuth, interfaceName, functionName)
        self.streamArn = streamArn
        self.shardId = shardId
        self.partitionKey = partitionKey
        self.sequenceNumber = sequenceNumber
        self.approximateArrivalTimestamp = approximateArrivalTimestamp
        dataBytes = bytearray(data, encoding="utf-8")
        self.byteArr = dataBytes
    
    def execute(self): 
        parser = KinesisRecordReader()
        return  parser.parseMessage(self.streamArn, self.shardId, self.partitionKey, self.sequenceNumber, self.approximateArrivalTimestamp, self.byteArr)

def getKinesisRecordReaderServiceRequest(requestId : str, letsDataAuth: LetsDataAuthParams, interfaceName : InterfaceNames, functionName : str, data : {}, batchedData : []):
    letsdata_assert(interfaceName == InterfaceNames.KinesisRecordReader, "invalid interfaceName - expected KinesisRecordReader, got "+str(interfaceName))
    letsdata_assert(letsDataAuth is not None, "invalid letsDataAuth - None")
    
    KinesisRecordReaderInterfaceNames = set(["parseMessage"])    

    if functionName not in KinesisRecordReaderInterfaceNames:
            raise(Exception("lambda event - invalid functionName "+functionName+" for interface KinesisRecordReader"))
    
    if functionName == "parseMessage":
        letsdata_assert(batchedData is None or len(batchedData) == 0, "invalid data - KinesisRecordReader.parseMessage requires empty batchedData dictionary")
        letsdata_assert(isinstance(data, dict) and len(data) == 6, "invalid data - KinesisRecordReader.parseMessage requires data keys [streamArn, shardId, partitionKey, sequenceNumber, approximateArrivalTimestamp, data]")
        
        letsdata_assert(not data['streamArn'] is None, "invalid streamArn - None - KinesisRecordReader.parseMessage requires data keys [streamArn, shardId, partitionKey, sequenceNumber, approximateArrivalTimestamp, data]")
        letsdata_assert(isinstance(data['streamArn'], str), "invalid streamArn - KinesisRecordReader.parseMessage requires streamArn value to be string")

        letsdata_assert(not data['shardId'] is None, "invalid shardId - None - KinesisRecordReader.parseMessage requires data keys [streamArn, shardId, partitionKey, sequenceNumber, approximateArrivalTimestamp, data]")
        letsdata_assert(isinstance(data['shardId'], str), "invalid shardId - KinesisRecordReader.parseMessage requires shardId value to be string")

        letsdata_assert(not data['partitionKey'] is None, "invalid partitionKey - None - KinesisRecordReader.parseMessage requires data keys [streamArn, shardId, partitionKey, sequenceNumber, approximateArrivalTimestamp, data]")
        letsdata_assert(isinstance(data['partitionKey'], str), "invalid partitionKey - KinesisRecordReader.parseMessage requires partitionKey value to be string")

        letsdata_assert(not data['sequenceNumber'] is None, "invalid sequenceNumber - None - KinesisRecordReader.parseMessage requires data keys [streamArn, shardId, partitionKey, sequenceNumber, approximateArrivalTimestamp, data]")
        letsdata_assert(isinstance(data['sequenceNumber'], str), "invalid sequenceNumber - KinesisRecordReader.parseMessage requires sequenceNumber value to be string")

        letsdata_assert(not data['approximateArrivalTimestamp'] is None, "invalid offsetBytes - None - SingleFileParser.parseMessage requires data keys [streamArn, shardId, partitionKey, sequenceNumber, approximateArrivalTimestamp, data]")
        letsdata_assert(isinstance(data['approximateArrivalTimestamp'], int), "invalid approximateArrivalTimestamp - SingleFileParser.parseMessage requires approximateArrivalTimestamp value to be int")
        
        letsdata_assert(not data['data'] is None, "invalid data - None - KinesisRecordReader.parseMessage requires data keys [streamArn, shardId, partitionKey, sequenceNumber, approximateArrivalTimestamp, data]")
        letsdata_assert(isinstance(data['data'], str), "invalid data - KinesisRecordReader.parseMessage requires data value to be str")

        return KinesisRecordReader_ParseMessage(requestId, letsDataAuth, interfaceName, functionName, data['streamArn'], data['shardId'], data['partitionKey'], data['sequenceNumber'], data['approximateArrivalTimestamp'], data['data'])
    else:
        raise(Exception("Unknown functionName"))
    
    