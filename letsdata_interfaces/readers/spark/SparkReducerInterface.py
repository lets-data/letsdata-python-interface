# letsdata imports
import uuid
import os
from letsdata_interfaces.readers.model.RecordParseHint import RecordParseHint
from letsdata_interfaces.readers.model.RecordHintType import RecordHintType
from letsdata_interfaces.readers.model.ParseDocumentResultStatus import ParseDocumentResultStatus
from letsdata_interfaces.readers.model.ParseDocumentResult import ParseDocumentResult
from letsdata_interfaces.documents.Document import Document
from letsdata_interfaces.documents.DocumentType import DocumentType
from letsdata_interfaces.documents.ErrorDoc import ErrorDoc
from letsdata_utils.logging_utils import logger
from letsdata_utils.secretmanager_util import SecretManagerUtil

# spark imports
from pyspark.sql import *
from pyspark.sql.types import MapType, StringType
from pyspark.sql.functions import col, split, expr, udf, regexp_replace, lit
from letsdata_utils.spark_utils import createSparkSession, readSparkDataframe, writeSparkDataframe

'''
LetsData's Spark interfaces are inspired by the original Google Map Reduce paper. We have defined a MAPPER interface and a REDUCER interface. Here is how they work to process a dataset using Spark.

Recall that a dataset's amount of work is defined by a manifest file. For example, for S3 read destination, this is essentially a list of files that need to be processed. 

     "manifestFile": {
          "manifestType": "S3ReaderTextManifestFile",
          "region": "us-east-1",
          "fileContents": "crawl-data/CC-MAIN-2023-50/segments/1700679099281.67/wet/CC-MAIN-20231128083443-20231128113443-00000.warc.wet.gz\n
                         crawl-data/CC-MAIN-2023-50/segments/1700679099281.67/wet/CC-MAIN-20231128083443-20231128113443-00001.warc.wet.gz\n
                         crawl-data/CC-MAIN-2023-50/segments/1700679099281.67/wet/CC-MAIN-20231128083443-20231128113443-00002.warc.wet.gz\n
                         crawl-data/CC-MAIN-2023-50/segments/1700679099281.67/wet/CC-MAIN-20231128083443-20231128113443-00003.warc.wet.gz",
          "readerType": "SPARKREADER"
     }

The manifest file above specifies 4 files that need to be processed. 

MAPPER Tasks
------------
     * Each of manifest files becomes a separate Mapper Task in LetsData. 
     * And each Mapper Task calls this mapper interface for its file. 
     * The mapper interface should implement any single partition operations (narrow transformations) 
     * The dataframe returned by the Mapper Task is written to S3 as an intermediate file by LetsData. 
     * In this example case, 4 manifest files -> 4 Mapper Tasks -> 4 intermediate files.

REDUCER Task
------------
     * LetsData creates a reducer task for any reduce operations for the dataset. 
     * The intermediate files from the mapper phase are read by the reducer, any multi-partition operations, shuffles, aggregates, joins or similar wide transformations are performed on the intermediate files.
     * The dataset returned by the Reducer Task is written to the dataset's write destination.
     * In this example case, 4 intermediate files from the mapper tasks -> 1 output file by the reducer task

                                                                                                                  ----- +
    +-----------------+     +-----------------+              +----------------------+      +----------------------+     |
    | Manifest File 1 | --> | LetsData Task 1 | -- mapper -> | SparkMapperInterface |--->  | Intermediate File 1  |     |
    +-----------------+     +-----------------+              +----------------------+      +----------------------+     |
    +-----------------+     +-----------------+              +----------------------+      +----------------------+     |      +----------+
    | Manifest File 2 | --> | LetsData Task 2 | -- mapper -> | SparkMapperInterface |--->  | Intermediate File 2  |      >---> |          |
    +-----------------+     +-----------------+              +----------------------+      +----------------------+      >---> |  Reducer |              +-----------------------+
    +-----------------+     +-----------------+              +----------------------+      +----------------------+      >---> |   Task   |-- reducer -> | SparkReducerInterface | --> Output File at Write Destination
    | Manifest File 3 | --> | LetsData Task 3 | -- mapper -> | SparkMapperInterface |--->  | Intermediate File 3  |      >---> |          |              +-----------------------+
    +-----------------+     +-----------------+              +----------------------+      +----------------------+     |      +----------+
    +-----------------+     +-----------------+              +----------------------+      +----------------------+     |
    | Manifest File 4 | --> | LetsData Task 4 | -- mapper -> | SparkMapperInterface |--->  | Intermediate File 4  |     |
    +-----------------+     +-----------------+              +----------------------+      +----------------------+     |        
                                                                                                                  ----- +
    Figure: Spark Dataset's Architecture Diagram                                                                                                                  
    ---------------------------------------------

LetsData Spark Compute Engine can run in a few different configurations:
     * MAPPER_AND_REDUCER: Mapper tasks are created for each manifest file and a single reducer task reduces these to an output file.  (This is what is discussed above and shown in the diagram)
     * MAPPER_ONLY: Mapper tasks are created for each manifest file and the output files are written at the write destination (no intermediate files and no reducer tasks.)
     * REDUCER_ONLY: Reducer task is created and all manifest files are read by this task, reduced and output files are written to write destination.  

What to do about errors, logs, metrics and checkpointing?

* logger is available, and logs would be sent to cloudwatch and made available. 
* metrics, no metrics support within the mapper interface yet. We generate some high level metrics. We will hopefully enable these soon. 
* errors: the letsdata dataset errors are currently not available for spark interfaces. You decide how you want to deal with errors. (Write separate error files (using same write credentials), log them to log file etc.). Any unhandled / terminal failures can be thrown as exceptions and the task will record these and transition to error state. 
* checkpointing: the letsdata checkpointing and restart from checkpoints is not available yet for spark interfaces. Interfaces run either completely or fail, in which case the intermediate progress isn't used for reduce. If rerun, the tasks will run from beginning and overwrite any intermediate progress. 
'''
class SparkReducerInterface:
   
   def __init__(self) -> None:
         pass
   
   '''
   This is the reducer interface. LetsData calls this interface with a list of read destination uris (s3 file links) for the files that'd be the inputs of the reducer task. User's spark transformation code is run and an output dataframe is created. 
   
   The code has default implementations for the following which wrap the user's spark transformation code:
     * the code has default credentials get
     * spark session setup 
     * read the file into the dataframe method calls for each file in the readUris - the dataframes are appended (union) to create a combined dataframe from all the input files
        <user's spark transformation code>
     * write output dataframe to the the write destination S3 bucket. 

   These default implementations can be used as is, advanced users may want to customize these as needed. 

   For example, the following read connector and write connector parameters would be sent via different function parameters (json annotated below)
     "readConnector": {
          "connectorDestination": "S3",                     # passed as the readDestination, if runSparkInterfaces is set to REDUCER_ONLY, otherwise system generated for the intermediate files output by the mapper
          "artifactImplementationLanguage": "python",
          "interfaceECRImageResourceLocation": "Customer",
          "interfaceECRImagePath": "151166716410.dkr.ecr.us-east-1.amazonaws.com/letsdata_python_functions:latest",
          "readerType": "SPARKREADER",
          "bucketName": "commoncrawl",
          "bucketResourceLocation": "Customer",
          "sparkFileFormat": "text",                        # passed as the readFormat, if runSparkInterfaces is set to REDUCER_ONLY, otherwise system specifies 'parquet', which is the format for the intermediate files output by the mapper
          "sparkReadOptions": {                             # passed as the readOptions, if runSparkInterfaces is set to REDUCER_ONLY, otherwise system specifies options for the intermediate files output by the mapper
               "lineSep": "\n\r\n\r\n"
          }
     }

     "manifestFile": {
          "readerType": "SPARKREADER",
          "manifestType": "S3ReaderTextManifestFile",
          "region": "us-east-1",
          "fileContents": "crawl-data/CC-MAIN-2023-50/segments/1700679099281.67/wet/CC-MAIN-20231128083443-20231128113443-00000.warc.wet.gz\n     
                         crawl-data/CC-MAIN-2023-50/segments/1700679099281.67/wet/CC-MAIN-20231128083443-20231128113443-00001.warc.wet.gz\n
                         crawl-data/CC-MAIN-2023-50/segments/1700679099281.67/wet/CC-MAIN-20231128083443-20231128113443-00002.warc.wet.gz\n
                         crawl-data/CC-MAIN-2023-50/segments/1700679099281.67/wet/CC-MAIN-20231128083443-20231128113443-00003.warc.wet.gz"

                                                            #   ['s3a://<bucketName>/<fileName1>', 
                                                            #     's3a://<bucketName>/<fileName2>', 
                                                            #     's3a://<bucketName>/<fileName3>', 
                                                            #     's3a://<bucketName>/<fileName4>'
                                                            #    ] 
                                                            # is passed as the readUris if runSparkInterfaces is set to REDUCER_ONLY, otherwise, similar uris for intermediate files output by the mapper are generated.

     }


     "writeConnector": {
          "connectorDestination": "S3",                     # passed as the writeDestination
          "resourceLocation": "LetsData",
          "writerType": "Spark",
          "sparkFileFormat": "json",                        # passed as the writeFormat
          "sparkWriteOptions": {"compression":"gzip"}       # passed as the writeOptions
     },

      
     Parameters
     ----------
     appName : str
                 The appName is a system generated spark app name
     readDestination : str
                 The readDestination for spark reducer - currently only S3 is supported. If run configuration is 'MAPPER_AND_REDUCER', intermediate s3 bucket is the read destination. If run configuration is 'REDUCER_ONLY', the dataset's readConnector s3 bucket is used as the readDestination.
     readUris : list of str
                 The list of readUris (the s3 file links) for that files that the reducer will read. If run configuration is 'MAPPER_AND_REDUCER', intermediate files outputted by the mapper are specified. If run configuration is 'REDUCER_ONLY', the dataset's readConnector s3 bucket and manifest's files are specified. 
     readFormat : str
                 The format of the file being read by the reducer. If run configuration is 'MAPPER_AND_REDUCER', system specifies these as 'parquet' for the intermediate files. If run configuration is 'REDUCER_ONLY', the dataset's readConnector sparkFileFormat is used. 
     readOptions : dict 
                 The options for the spark mapper's read. System specifies for 'MAPPER_AND_REDUCER' run config, dataset's readConnector's sparkReadOptions are used for run config 'REDUCER_ONLY'.  
     writeDestination : str
                 The writeDestination for spark reducer - currently only S3 is supported and is specified in the dataset's writeConnector. 
     writeUri : str
                 The writeUri for the writeDestination (the s3 file link) that the reducer will write the output file to, specified in the dataset's write destination bucket 
     writeFormat : str
                 The format of the file being written by the reducer, specified in dataset's writeConnector.sparkFileFormat attribute.  
     writeMode : str
                 The writeMode for spark reducer - currently defaults to 'overwrite'. 
     writeOptions : dict
                 The options for the spark mapper's write, specified in the writeConnector.sparkWriteOptions, for example, '{"compression":"gzip"}'. Different formats can have different options that can be specified here.  
     spark_credentials_secret_arn : str
                 The secret manager arn for credentials for reading and writing to the read / write buckets
     Returns
     -------
     void
        The function writes the data to write destination and does not return anything
   '''          
   def reducer(self, appName: str, readDestination : str, readUris : [str], readFormat: str, readOptions : dict, writeDestination : str, writeUri : str, writeFormat: str, writeMode: str, writeOptions : dict, spark_credentials_secret_arn : str):
        '''
        readCredentials = self.get_read_destination_credentials(os.environ['AWS_REGION'], spark_credentials_secret_arn)
        writeCredentials = self.get_write_destination_credentials(os.environ['AWS_REGION'], spark_credentials_secret_arn)
        spark = createSparkSession(appName, readDestination, writeDestination, readUris[0], writeUri, readCredentials, writeCredentials)
        dataframe = None
        for readUri in readUris:
          currDataFrame = readSparkDataframe(spark, readDestination, readUri, readFormat, readOptions)
          if dataframe == None:
              dataframe = currDataFrame
          else:
              dataframe.union(currDataFrame)
        '''
   
        # uncomment the spark session and dataframe read lines above and then add reducer code (if any) below to process the dataframe
        # also uncomment the spark write dataframe line down below
        raise(Exception("Not Yet Implemented"))
   
        # writeSparkDataframe(spark, writeDestination, writeUri, writeFormat, writeMode, writeOptions, dataframe)
   
   
   '''
   Helper function to get the credentials for reading the spark reducer read bucket from secret manager
   ''' 
   def get_read_destination_credentials(self, region, spark_credentials_secret_arn):
        return SecretManagerUtil.get_spark_aws_credentials(region, spark_credentials_secret_arn, "reducer", "read")
   
   '''
   Helper function to get the credentials for reading the spark reducer write bucket from secret manager
   ''' 
   def get_write_destination_credentials(self, region, spark_credentials_secret_arn):
        return SecretManagerUtil.get_spark_aws_credentials(region, spark_credentials_secret_arn, "reducer", "write")