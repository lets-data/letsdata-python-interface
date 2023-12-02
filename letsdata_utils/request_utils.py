import os, sys, traceback, json
from letsdata_utils.logging_utils import logger
from letsdata_utils.stage import Stage

def return500ResponseFromException(err, response) -> dict:
    return {
        "StatusCode": 500,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            "statusCode": "EXCEPTION",
            "errorMessage": str(err),
            "exception": {
                "errorMessage": str(err),
                "errorType": err.__class__.__name__,
                "stackTrace": ''.join(traceback.format_exception(*(sys.exc_info())))
            }
        }
    }

def getLambdaStageFromEnvironment() -> Stage: 
    stage = os.getenv('LETS_DATA_STAGE')
    return Stage.fromValue(stage)


def isLambdaFunctionDatasetMicroservice(context, stage) -> bool:
    invokedFunctionArn : str = context.invoked_function_arn
    return not invokedFunctionArn.endswith(stage.value+"LetsDataPythonBridgeLambdaFunction")

def getJsonObject(input : object):
    # if object is primitive type - return 
    if isinstance(input, str) or isinstance(input, int) or isinstance(input, float) or isinstance(input, bool) or input is None:
        return input
    try: 
        # if object is json serializable - return 
        jsonObject = json.dumps(input)
        return input
    except:
        
        # object is not json serializable. Iterate through the dictionary key value pairs and call getJsonObject for each value recursively
        try: 
            customDict = dict()
            for keyName in input.__dict__.keys():
                customDict[keyName] = getJsonObject(input.__dict__[keyName])
            return customDict
        except:
            logger.error("input has no  __dict__ - type: "+str(type(input)))
            raise
    
        # TODO handle lists