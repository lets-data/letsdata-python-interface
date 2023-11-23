from letsdata_utils.logging_utils import logger
from letsdata_service.Service import ServiceRequest, LetsDataAuthParams, InterfaceNames
from letsdata_utils.validations import letsdata_assert
from letsdata_interfaces.readers.sagemaker.SagemakerVectorsInterface import SagemakerVectorsInterface


class SagemakerVectorsInterfaceService_ExtractDocumentElementsForVectorization(ServiceRequest):
    def __init__(self, requestId : str, letsDataAuth: LetsDataAuthParams, interfaceName : InterfaceNames, functionName : str, document : dict):
        super().__init__(requestId, letsDataAuth, interfaceName, functionName)
        self.document = document

    def execute(self):
        parser = SagemakerVectorsInterface()
        return  parser.extractDocumentElementsForVectorization(self.document)

class SagemakerVectorsInterfaceService_ConstructVectorDoc(ServiceRequest):
    def __init__(self, requestId : str, letsDataAuth: LetsDataAuthParams, interfaceName : InterfaceNames, functionName : str, documentInterface : dict, vectorsMap : dict):
        super().__init__(requestId, letsDataAuth, interfaceName, functionName)
        self.documentInterface = documentInterface
        self.vectorsMap = vectorsMap
    
    def execute(self):
        parser = SagemakerVectorsInterface()
        return  parser.constructVectorDoc(self.documentInterface, self.vectorsMap)

def getSagemakerVectorsInterfaceServiceRequest(requestId : str, letsDataAuth: LetsDataAuthParams, interfaceName : InterfaceNames, functionName : str, data : {}, batchedData : []):
    letsdata_assert(interfaceName == InterfaceNames.SagemakerVectorsInterface, "invalid interfaceName - expected SagemakerVectorsInterface, got "+str(interfaceName))
    letsdata_assert(letsDataAuth is not None, "invalid letsDataAuth - None")

    SagemakerVectorsInterfaceServiceInterfaceNames = set(["extractDocumentElementsForVectorization", "constructVectorDoc"])    

    if functionName not in SagemakerVectorsInterfaceServiceInterfaceNames:
            raise(Exception("lambda event - invalid functionName "+functionName+" for interface SagemakerVectorsInterfaceService"))
    
    if functionName == "extractDocumentElementsForVectorization":
        letsdata_assert(batchedData is None or len(batchedData) == 0, "invalid data - SagemakerVectorsInterfaceService.extractDocumentElementsForVectorization requires empty batchedData dictionary")
        letsdata_assert(isinstance(data, dict) and len(data) == 1, "invalid data - SagemakerVectorsInterfaceService.extractDocumentElementsForVectorization requires data keys [document]")
        
        letsdata_assert(not data['document'] is None, "invalid document - None - SagemakerVectorsInterfaceService.extractDocumentElementsForVectorization requires data keys [document]")
        letsdata_assert(isinstance(data['document'], dict), "invalid document - SagemakerVectorsInterfaceService.extractDocumentElementsForVectorization requires document value to be dict")

        return SagemakerVectorsInterfaceService_ExtractDocumentElementsForVectorization(requestId, letsDataAuth, interfaceName, functionName, data['document'])
    elif functionName == "constructVectorDoc":
        letsdata_assert(batchedData is None or len(batchedData) == 0, "invalid data - SagemakerVectorsInterfaceService.extractDocumentElementsForVectorization requires empty batchedData dictionary")
        letsdata_assert(isinstance(data, dict) and len(data) == 2, "invalid data - SagemakerVectorsInterfaceService.extractDocumentElementsForVectorization requires data keys [documentInterface, vectorsMap]")
        
        letsdata_assert(not data['documentInterface'] is None, "invalid documentInterface - None - SagemakerVectorsInterfaceService.extractDocumentElementsForVectorization requires data keys [documentInterface, vectorsMap]")
        letsdata_assert(isinstance(data['documentInterface'], dict), "invalid documentInterface - SagemakerVectorsInterfaceService.extractDocumentElementsForVectorization requires documentInterface value to be dict")

        return SagemakerVectorsInterfaceService_ConstructVectorDoc(requestId, letsDataAuth, interfaceName, functionName, data['documentInterface'], data['vectorsMap'])
    else:
        raise(Exception("Unknown functionName"))    
