#!/bin/sh

BUILD_STAGE=$1

if [[ $BUILD_STAGE == "test" ]]; then
    AWS_ACCOUNT_ID=223413462631
    echo build $BUILD_STAGE aws account id $AWS_ACCOUNT_ID
    PROFILE=
    REGION="--region us-east-1"
elif [[ $BUILD_STAGE == "prod" ]]; then
    AWS_ACCOUNT_ID=956943252347
    echo build $BUILD_STAGE aws account id $AWS_ACCOUNT_ID
    PROFILE="--profile devLetsData"
    REGION="--region us-east-1"
else
    echo "unknown build stage "
    echo $BUILD_STAGE    
    exit -1
fi

#build letsdata_python_bridge
echo "########## starting docker build letsdata_python_bridge ##############"
docker build --platform linux/amd64 -t letsdata_python_bridge:$BUILD_STAGE -f dockerfile .
echo "running docker letsdata_python_bridge"
docker run -e LETS_DATA_STAGE='Test' -p 9000:8080 letsdata_python_bridge:$BUILD_STAGE &
sleep 3
CONTAINER_ID=`docker ps|grep letsdata_python_bridge:$BUILD_STAGE|cut -d ' ' -f 1`
echo 'containerId: '$CONTAINER_ID
echo "testing letsdata_python_bridge"
RESPONSE=`curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"requestId":"65fff00b-460c-4055-a171-f0a8c2e4ae22","interface":"SingleFileParser","function":"getS3FileType","letsdataAuth":{"tenantId":"3c25bdbd-c2b1-4b74-9f6a-b18d23e6ade1","userId":"de9eb5a6-a06f-429f-8f75-9a438fe073e1","datasetName":"CommonCrawlDataset","datasetId":"78ce0aa2-9b8c-4534-9170-445d2cfd70af"},"data":{}}'`

echo "killing letsdata_python_bridge container"
docker kill $CONTAINER_ID
if [[ $RESPONSE == *"Not Yet Implemented"* ]]; then
    echo "letsdata_python_bridge test passed"
else
    echo "letsdata_python_bridge response is not expected"
    echo "response: "
    echo $RESPONSE    
    exit -1
fi

echo "uploading to ecr repo letsdata_python_bridge"
aws ecr get-login-password $REGION $PROFILE | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
#REPOSITORY_URI=`aws ecr create-repository --repository-name letsdata_python_functions --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE $REGION $PROFILE| jq .repository.repositoryUri`
REPOSITORY_URI=$AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/letsdata_python_functions
#echo "repository uri "$REPOSITORY_URI
docker tag letsdata_python_bridge:$BUILD_STAGE $REPOSITORY_URI:latest
docker push $REPOSITORY_URI:latest

#aws lambda update-function-code --function-name TestLetsDataPythonBridgeLambdaFunction --image-uri 223413462631.dkr.ecr.us-east-1.amazonaws.com/momento_lambda_functions:latest
#aws lambda invoke --function-name TestLetsDataPythonBridgeLambdaFunction --invocation-type RequestResponse --payload eyJyZXF1ZXN0SWQiOiI2NWZmZjAwYi00NjBjLTQwNTUtYTE3MS1mMGE4YzJlNGFlMjIiLCJpbnRlcmZhY2UiOiJTaW5nbGVGaWxlUGFyc2VyIiwiZnVuY3Rpb24iOiJnZXRTM0ZpbGVUeXBlIiwibGV0c2RhdGFBdXRoIjp7InRlbmFudElkIjoiM2MyNWJkYmQtYzJiMS00Yjc0LTlmNmEtYjE4ZDIzZTZhZGUxIiwidXNlcklkIjoiZGU5ZWI1YTYtYTA2Zi00MjlmLThmNzUtOWE0MzhmZTA3M2UxIiwiZGF0YXNldE5hbWUiOiJDb21tb25DcmF3bERhdGFzZXQiLCJkYXRhc2V0SWQiOiI3OGNlMGFhMi05YjhjLTQ1MzQtOTE3MC00NDVkMmNmZDcwYWYifSwiZGF0YSI6e319 ./out

echo "########## letsdata_python_bridge built ##############"
echo "########################"
echo "########################"
echo "########################"
