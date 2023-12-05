from letsdata_interfaces.readers.model.RecordParseHint import RecordParseHint
from letsdata_interfaces.readers.model.RecordHintType import RecordHintType
from letsdata_interfaces.readers.model.ParseDocumentResultStatus import ParseDocumentResultStatus
from letsdata_interfaces.readers.model.ParseDocumentResult import ParseDocumentResult
from letsdata_interfaces.documents.Document import Document
from letsdata_interfaces.documents.ErrorDoc import ErrorDoc
from letsdata_utils.logging_utils import logger
from letsdata_utils.validations import letsdata_assert
from letsdata_interfaces.documents.DocumentType import DocumentType
import re
from enum import Enum
from datetime import datetime
from collections import namedtuple

'''
    The parser interface for Single File Reader usecase. This is used when all the files are of a single type and the records in the file do not follow a state machine.
    This interface is where you tell us how to parse the individual records from the file. Since this is single file reader, there is no state machine maintained.
    
    This implementation parses the 'conversion' records from the Common Crawl Web Extraction Template (WET) files.

                Example: WET Files Record Layout:
                ---------------------------------

                'warcinfo' WARCINFO Header
                WARCINFO Payload

                'conversion' WARC Header
                'conversion' Payload

                'conversion' WARC Header
                'conversion' Payload

                'conversion' WARC Header
                'conversion' Payload

                ...
 '''
class SingleFileParser:
    def __init__(self) -> None:
        pass 

    '''
     * The filetype of the file - for the example we've used, we define the filetype (logical name) as "WET"
     * 
     * @return - The file type
     '''
    def getS3FileType(self) -> str:
        return "WET"

    '''
     * Given the filetype (WET) and filename (crawl-data/CC-MAIN-2022-21/segments/1652662509990.19/wet/CC-MAIN-20220516041337-20220516071337-00000.warc.wet.gz) from the manifest file, return the resolved filename if necessary.
     * In most cases, the resolved filename would be the same as the filename, but in some cases, you might need to prepend paths if the data in the s3 bucket is not in the root directory.
     * In this example, the manifest filename is fully qualified so we return it as is.
     *
     * @param s3FileType - the file type - example WET
     * @param fileName - the file name - example crawl-data/CC-MAIN-2022-21/segments/1652662509990.19/wet/CC-MAIN-20220516041337-20220516071337-00000.warc.wet.gz
     * @return - the resolved file name - example crawl-data/CC-MAIN-2022-21/segments/1652662509990.19/wet/CC-MAIN-20220516041337-20220516071337-00000.warc.wet.gz
     '''
    def getResolvedS3FileName(self, s3FileType : str,  fileName : str) -> str:
       return fileName


    '''
     * The record start pattern - to extract the records from the file, the parser needs to know the record start delimiter - it will search the file sequentially till it finds this delimiter and then from that point on, it will search for the end record delimiter.
     * Once it finds the end record delimiter, it will copy those bytes to the parse document function to create an extracted record
     *
     *      For example, here is an abbreviated WET file:
     *
     *      WET File:
     *      ---------
     * 
     *      WARC/1.0
     *      WARC-Type: conversion                                                   <--- we use this string as the start pattern
     *      WARC-Target-URI: http://023hrk.com/a/chanpinzhongxin/cp2/104.html
     *      WARC-Date: 2022-05-16T04:40:56Z
     *      WARC-Record-ID: <urn:uuid:f8a15ad2-9d24-42d6-8f7a-7d9431246752>
     *      WARC-Refers-To: <urn:uuid:5232afac-fb10-401c-b522-445db8bdbf2a>
     *      WARC-Block-Digest: sha1:M7TRGS3KUALFLHMGLJSDMER3FDP2Z2Q4
     *      WARC-Identified-Content-Language: zho
     *      Content-Type: text/plain
     *      Content-Length: 3710
     *      
     *      漫步肩关节_重庆鸿瑞铠体育设施有限公司
     *      网站地图
     *      加入收藏
     *      联系我们
     *      您好！欢迎访问重庆鸿瑞铠体育设施有限公司！
     *      优质环保原料
     *      更环保更安全
     *      施工保障
     *      流程严谨、匠心工艺
     *      使用年限
     *      高出平均寿命30%
     *      全国咨询热线
     *      ...
     *                                                                              <--- we use '\n\r\n\r\n' as the end pattern
     *
     *      WARC/1.0
     *      WARC-Type: conversion
     *      ...
     *
     *
     *
     * @param s3FileType - the filetype
     * @return - the record start pattern as a RecordParseHint object
     '''
    def getRecordStartPattern(self, s3FileType : str) -> RecordParseHint:
        return RecordParseHint(RecordHintType.PATTERN, "WARC-Type: conversion", -1)
        
    
    '''
     * The record end pattern - to extract the records from the file, the parser needs to know the record start delimiter - it will search the file sequentially till it finds this delimiter and then from that point on, it will search for the end record delimiter.
     * Once it finds the end record delimiter, it will copy those bytes to the parse document function to create an extracted record
     *
     * See above for file structure. We use '\n\r\n\r\n' as the end pattern
     * @param s3FileType - the filetype
     * @return - the record end pattern as a RecordParseHint object
     '''
    def getRecordEndPattern(self, s3FileType : str) -> RecordParseHint:
        return RecordParseHint(RecordHintType.PATTERN, "\n\r\n\r\n", -1)
    
    '''
     *  This function is called with the document contents in a byteArr and the startIndex and endIndex into the byteArr as the start and end of the record.
     *  The implementer is expected to construct the output record from these bytes.
     *
     *  The example implementation below parses the header key value pairs, extract the url as the docId, partitionKey and other headers as document attributes.
     *  We also extract the document text and return these as a document with Success status code.
     *
     * @param s3FileType - the filetype
     * @param s3Filename - the filename
     * @param offsetBytes - the offset bytes into the file
     * @param byteArr - the byteArr that has the contents of the record
     * @param startIndex - the start index of the record in the byteArr
     * @param endIndex - the end index of the record in the byteArr
     * @return - ParseDocumentResult which has the extracted record and the status (error, success or skip)
     '''
    def parseDocument(self, s3FileType : str, s3Filename : str, offsetBytes : int , byteArr : bytearray, startIndex : int, endIndex : int) -> ParseDocumentResult:
        headerEndIndex = byteArr.find(bytearray('\r\n\r\n', encoding="utf-8"), startIndex, endIndex)
        if headerEndIndex == -1:
            raise RuntimeError(f"Header end index not found in Http Response - start index: {startIndex}, end index: {endIndex}")

        headerMap = {}
        currIndex = startIndex
        while currIndex < headerEndIndex:
            logger.debug("loop iter - currIndex: "+str(currIndex)+", headerEndIndex: "+str(headerEndIndex))
            lineEndIndex = byteArr.find(bytearray('\r\n', encoding="utf-8"), currIndex, headerEndIndex)
            if lineEndIndex <= currIndex:
                logger.debug("lineEndIndex not found when parsing headers")
                break
            
            line = byteArr[currIndex:lineEndIndex].decode('utf-8').strip()
            logger.debug("parsed header line "+line)
            if line is None or line == "" or line.startswith("WARC/1.0"):
                currIndex = lineEndIndex+len(bytearray('\r\n', encoding="utf-8"))
            else:
                letsdata_assert(line.index(':') > 0, "invalid header line")
                keyValuePair = line.split(': ')
                headerKey = keyValuePair[0].strip()
                headerValue = keyValuePair[1].strip()
                logger.debug("parsed headerKey: "+headerKey+", headerValue: "+headerValue)
                headerMap[headerKey] = headerValue
                currIndex = lineEndIndex+len(bytearray('\r\n', encoding="utf-8"))
        
        logger.debug("parsed headerMap: "+str(headerMap))

        docKeyValueMap = {}

        currIndex = headerEndIndex
        docText = byteArr[currIndex:endIndex].decode('utf-8').strip()
        letsdata_assert(len(docText) > 0, "invalid docText")
        
        docKeyValueMap['docText'] = docText

        url = headerMap['WARC-Target-URI']
        letsdata_assert(len(url) > 0, "invalid url")
        docKeyValueMap['url'] = url
        docKeyValueMap['docId'] = url
        docKeyValueMap['partitionKey'] = url

        language = None
        if 'WARC-Identified-Content-Language' in headerMap.keys():
            language = headerMap['WARC-Identified-Content-Language']
            docKeyValueMap['language'] = language

        contentType = None
        if 'Content-Type' in headerMap.keys():
            contentType = headerMap['Content-Type']
            docKeyValueMap['contentType'] = contentType

        contentLength = None
        if 'Content-Length' in headerMap.keys():
            contentLength = headerMap['Content-Length']
            docKeyValueMap['contentLength'] = contentLength

        blockDigest = None
        if 'WARC-Block-Digest' in headerMap.keys():
            blockDigest = headerMap['WARC-Block-Digest']
            docKeyValueMap['blockDigest'] = blockDigest

        warcDate = None
        if 'WARC-Date' in headerMap.keys():
            warcDate = headerMap['WARC-Date']
            docKeyValueMap['warcDate'] = warcDate


        return ParseDocumentResult(None, Document(DocumentType.Document, url, "Content", url, {}, docKeyValueMap), ParseDocumentResultStatus.SUCCESS)
    