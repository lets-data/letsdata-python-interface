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
SINGLE_FILE_PARSER_RESPONSE=`curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"requestId":"65fff00b-460c-4055-a171-f0a8c2e4ae22","interface":"SingleFileParser","function":"getS3FileType","letsdataAuth":{"tenantId":"3c25bdbd-c2b1-4b74-9f6a-b18d23e6ade1","userId":"de9eb5a6-a06f-429f-8f75-9a438fe073e1","datasetName":"CommonCrawlDataset","datasetId":"78ce0aa2-9b8c-4534-9170-445d2cfd70af"},"data":{}}'`

QUEUE_MESSAGE_READER_RESPONSE=`curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"requestId":"65fff00b-460c-4055-a171-f0a8c2e4ae22","interface":"QueueMessageReader","function":"parseMessage","letsdataAuth":{"tenantId":"3c25bdbd-c2b1-4b74-9f6a-b18d23e6ade1","userId":"de9eb5a6-a06f-429f-8f75-9a438fe073e1","datasetName":"CommonCrawlDataset","datasetId":"78ce0aa2-9b8c-4534-9170-445d2cfd70af"},"data":{"messageId":"a9d196f6-2b5a-4a49-b095-73e1b950e251","messageGroupId":"dataset_name/data_date/logfile_1.gz","messageDeduplicationId":"dataset_name/data_date/logfile_1.gz","messageAttributes":{"attrib1":"value1","attrib2":"value2"},"messageBody":"WARC/1.0\nWARC-Type: request\nWARC-Date: 2022-01-16T09:37:04Z\nWARC-Record-ID: <urn:uuid:a565d4a1-daf1-4697-abfb-6c155d7ed2e6>\nContent-Length: 316\nContent-Type: application/http; msgtype=request\nWARC-Warcinfo-ID: <urn:uuid:6badabfb-3fa9-47c0-b0ef-ac4a71fd1456>\nWARC-IP-Address: 173.161.93.241\nWARC-Target-URI: http://01.deluxecleaning-services.com/\n\nGET / HTTP/1.1\nUser-Agent: CCBot/2.0 (https://commoncrawl.org/faq/)\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\nAccept-Language: en-US,en;q=0.5\nIf-Modified-Since: Thu, 21 Oct 2021 04:21:20 GMT\nAccept-Encoding: br,gzip\nHost: 01.deluxecleaning-services.com\nConnection: Keep-Alive\n\n\n\nWARC/1.0\nWARC-Type: response\nWARC-Date: 2022-01-16T09:37:04Z\nWARC-Record-ID: <urn:uuid:a2567d44-2052-4fbd-83af-dea76004f6dc>\nContent-Length: 11581\nContent-Type: application/http; msgtype=response\nWARC-Warcinfo-ID: <urn:uuid:6badabfb-3fa9-47c0-b0ef-ac4a71fd1456>\nWARC-Concurrent-To: <urn:uuid:a565d4a1-daf1-4697-abfb-6c155d7ed2e6>\nWARC-IP-Address: 173.161.93.241\nWARC-Target-URI: http://01.deluxecleaning-services.com/\nWARC-Payload-Digest: sha1:LLHZL7RSYU3WB32BJNRJSNGZATJW5JLY\nWARC-Block-Digest: sha1:Y3ZBLVGEXFKYBZIJPP7KJJMGF5N6OC5L\nWARC-Identified-Payload-Type: text/html"}}'`
KINESIS_RECORD_READER_RESPONSE=`curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"requestId":"65fff00b-460c-4055-a171-f0a8c2e4ae22","interface":"KinesisRecordReader","function":"parseMessage","letsdataAuth":{"tenantId":"3c25bdbd-c2b1-4b74-9f6a-b18d23e6ade1","userId":"de9eb5a6-a06f-429f-8f75-9a438fe073e1","datasetName":"CommonCrawlDataset","datasetId":"78ce0aa2-9b8c-4534-9170-445d2cfd70af"},"data":{"streamArn":"arn:aws:kinesis:us-east-1:223413462631:stream/letsdata-continuoustests-stream","shardId":"shardId-000000000006","partitionKey":"dataset_name/data_date/logfile_1.gz","sequenceNumber":"9223372036854775809","approximateArrivalTimestamp":1700763802123,"data":"WARC/1.0\nWARC-Type: request\nWARC-Date: 2022-01-16T09:37:04Z\nWARC-Record-ID: <urn:uuid:a565d4a1-daf1-4697-abfb-6c155d7ed2e6>\nContent-Length: 316\nContent-Type: application/http; msgtype=request\nWARC-Warcinfo-ID: <urn:uuid:6badabfb-3fa9-47c0-b0ef-ac4a71fd1456>\nWARC-IP-Address: 173.161.93.241\nWARC-Target-URI: http://01.deluxecleaning-services.com/\n\nGET / HTTP/1.1\nUser-Agent: CCBot/2.0 (https://commoncrawl.org/faq/)\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\nAccept-Language: en-US,en;q=0.5\nIf-Modified-Since: Thu, 21 Oct 2021 04:21:20 GMT\nAccept-Encoding: br,gzip\nHost: 01.deluxecleaning-services.com\nConnection: Keep-Alive\n\n\n\nWARC/1.0\nWARC-Type: response\nWARC-Date: 2022-01-16T09:37:04Z\nWARC-Record-ID: <urn:uuid:a2567d44-2052-4fbd-83af-dea76004f6dc>\nContent-Length: 11581\nContent-Type: application/http; msgtype=response\nWARC-Warcinfo-ID: <urn:uuid:6badabfb-3fa9-47c0-b0ef-ac4a71fd1456>\nWARC-Concurrent-To: <urn:uuid:a565d4a1-daf1-4697-abfb-6c155d7ed2e6>\nWARC-IP-Address: 173.161.93.241\nWARC-Target-URI: http://01.deluxecleaning-services.com/\nWARC-Payload-Digest: sha1:LLHZL7RSYU3WB32BJNRJSNGZATJW5JLY\nWARC-Block-Digest: sha1:Y3ZBLVGEXFKYBZIJPP7KJJMGF5N6OC5L\nWARC-Identified-Payload-Type: text/html"}}'`
SAGEMAKER_EXTRACT_RESPONSE=`curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"requestId":"65fff00b-460c-4055-a171-f0a8c2e4ae22","interface":"SagemakerVectorsInterface","function":"extractDocumentElementsForVectorization","letsdataAuth":{"tenantId":"3c25bdbd-c2b1-4b74-9f6a-b18d23e6ade1","userId":"de9eb5a6-a06f-429f-8f75-9a438fe073e1","datasetName":"CommonCrawlDataset","datasetId":"78ce0aa2-9b8c-4534-9170-445d2cfd70af"},"data":{"document":{"id":"318792f5-8bcb-4a77-b362-087520efb49c","url":"www.cnn.com","title":"Breaking News, Latest News and Videos | CNN","description":"View the latest news and breaking news today for U.S., world, weather, entertainment, politics and health at CNN.com.","keywords":"cnn news, daily news, breaking news, news today, current events","docText":"Article: US inflation means families are spending more than two years ago. The typical American household spent more in July than they did two years ago to buy the same goods and services, according to recent surveys. That figure underscores the cumulative impact high inflation has had on consumer finances — even as price growth has cooled considerably in recent months."}}}'`
SAGEMAKER_VECTORS_RESPONSE=`curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"requestId":"65fff00b-460c-4055-a171-f0a8c2e4ae22","interface":"SagemakerVectorsInterface","function":"constructVectorDoc","letsdataAuth":{"tenantId":"3c25bdbd-c2b1-4b74-9f6a-b18d23e6ade1","userId":"de9eb5a6-a06f-429f-8f75-9a438fe073e1","datasetName":"CommonCrawlDataset","datasetId":"78ce0aa2-9b8c-4534-9170-445d2cfd70af"},"data":{"documentInterface":{"id":"318792f5-8bcb-4a77-b362-087520efb49c","url":"www.cnn.com","title":"Breaking News, Latest News and Videos | CNN","description":"View the latest news and breaking news today for U.S., world, weather, entertainment, politics and health at CNN.com.","keywords":"cnn news, daily news, breaking news, news today, current events","docText":"Article: US inflation means families are spending more than two years ago. The typical American household spent more in July than they did two years ago to buy the same goods and services, according to recent surveys. That figure underscores the cumulative impact high inflation has had on consumer finances — even as price growth has cooled considerably in recent months."},"vectorsMap":{"PageTitle":[58.7,45.6,59.1,75.1],"PageDescription":[27.6,12,9.8,19,96,1.2,11.3,9.8,29.8,22.3,22.4,82.9,27.5,12.4,11.5,80.3,30.4],"PageKeywords":[31.8,48.4,2.4,98.3,28.4,55.5,15.3,79.3,81,12,56.4,56,13.7,46.4,2.9,46.5,65.2,70.7,13.1,59.8,63.8,22.4,15.2],"PageText":[96.3,79.8,18.2,37.8,85.6,83.6,68.3,54.5,95.9,64,32.6,36.4,68,93.1,40.2,61,98.2,52.7,26.2,31.1,26.9,35.2,16.8,25.3,97.7,81.6,87.9,21.5,72.4,12.1,27.4,83.9,81.9,60.1,5.5]}}}'`

echo "killing letsdata_python_bridge container"
docker kill $CONTAINER_ID
if [[ $SINGLE_FILE_PARSER_RESPONSE == *"Not Yet Implemented"* ]]; then
    echo "letsdata_python_bridge single file parser test passed"
else
    echo "letsdata_python_bridge single file parser response is not expected"
    echo "response: "
    echo $SINGLE_FILE_PARSER_RESPONSE    
    ERROR=TRUE
fi

if [[ $QUEUE_MESSAGE_READER_RESPONSE == *"Not Yet Implemented"* ]]; then
    echo "letsdata_python_bridge queue message reader test passed"
else
    echo "letsdata_python_bridge queue message reader response is not expected"
    echo "response: "
    echo $QUEUE_MESSAGE_READER_RESPONSE    
    ERROR=TRUE
fi

if [[ $KINESIS_RECORD_READER_RESPONSE == *"Not Yet Implemented"* ]]; then
    echo "letsdata_python_bridge kinesis record reader test passed"
else
    echo "letsdata_python_bridge kinesis record reader response is not expected"
    echo "response: "
    echo $KINESIS_RECORD_READER_RESPONSE    
    ERROR=TRUE
fi

if [[ $SAGEMAKER_EXTRACT_RESPONSE == *"Not Yet Implemented"* ]]; then
    echo "letsdata_python_bridge sagemaker extract test passed"
else
    echo "letsdata_python_bridge sagemaker extract response is not expected"
    echo "response: "
    echo $SAGEMAKER_EXTRACT_RESPONSE    
    ERROR=TRUE
fi

if [[ $SAGEMAKER_VECTORS_RESPONSE == *"Not Yet Implemented"* ]]; then
    echo "letsdata_python_bridge sagemaker vectors test passed"
else
    echo "letsdata_python_bridge sagemaker vectors response is not expected"
    echo "response: "
    echo $SAGEMAKER_VECTORS_RESPONSE    
    ERROR=TRUE
fi


if [[ $ERROR == *"TRUE"* ]]; then
    exit 1
else
    echo "all tests passed"
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
