import os
import sys
import traceback


from letsdata_utils.logging_utils import logger
from letsdata_utils.stage import Stage
# from letsdata_clients.sts_utils import LetsDataSTSSessionCredentialsProvider
# from letsdata_clients.secrets_manager_client import secrets_manager_client_cache_instance
# from letsdata_clients.momento_client import MomentoClientResponse

'''


    
def getMomentoAuthToken(letsDataAuthParams:LetsDataAuthParams, isDedicated : bool) -> str:
    # get the function's aws credentials
    lambda_aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
    lambda_aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    lambda_aws_session_token = os.environ['AWS_SESSION_TOKEN']

    # as of now, we are enabling direct access of the function to the momento arn for the user
    # in case of dedicated function, this is limited to the dataset's momento secret
    # in case of the data access function (non dedicated), this is allowed for all secrets that start with StageMomentoAuthToken*
    awsCredentials = {
        'AWSAccessKeyId': lambda_aws_access_key_id,
        'AWSSecretKey': lambda_aws_secret_access_key,
        'SessionToken': lambda_aws_session_token
    }

    # use function's credentials to get the momento auth token from secrets manager
    momento_auth_token = _getMomentoAuthTokenFromSecretsManager(letsDataAuthParams.momentoAuthTokenArn, awsCredentials)
    return momento_auth_token

def _getMomentoAuthTokenFromSecretsManager(momentoAuthTokenArn: str, awsCredentials: dict) -> str:
    secret_name = momentoAuthTokenArn
    logger.debug("momento_control_plane_lambda getting secret - momentoAuthTokenArn - secret_name: "+secret_name)
    secrets_manager_client = secrets_manager_client_cache_instance.get_secrets_manager_client_for_credentials("momentoAuthToken", awsCredentials['AWSAccessKeyId'], awsCredentials['AWSSecretKey'], awsCredentials['SessionToken'])
    momento_auth_token = secrets_manager_client.get_secret_value(secret_name)
    return momento_auth_token
'''


def return500ResponseFromException(err, response) -> dict:
    return {
        "StatusCode": 500,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            #"statusCode": str(response.status_code) if isinstance(response, MomentoClientResponse) and response.status_code is not None else "EXCEPTION",
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

'''
def isRequestAllowed(function, action, isDedicated) -> bool:
    if function == 'DataPlane':
        if isDedicated:
            return True
        else:
            raise(Exception("DataPlane requests are allowed for only dedicated endpoints"))
    elif function == 'ControlPlane':
        if action == "find":
            return True
        elif isDedicated:
            return True
        else:
            raise(Exception("ControlPlane requests other than find requests are allowed for only dedicated endpoints"))
    else:
        raise(Exception("Unknown function - expected [ControlPlane, DataPlane]"))
'''