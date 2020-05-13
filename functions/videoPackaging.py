from database.dbHelper import DynamoManager
from response.responseBuilder import ResponseManager
from sqs.sqsHelper import SqsManager
import json
import boto3
import os
import sys
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
import time
import uuid

def handler(event, context):
    #response handler for returning responses
    responseHandler = ResponseManager()
    #Dynamo Db helper functions
    dbHelper=DynamoManager()
    try:
        event["body"]=json.loads(event["body"])
        input_content_id = getParamsValue('input_content_id', event)
        key = getParamsValue('key', event)
        kid = getParamsValue('kid', event)
        #Check Media Package has been sent. If already sent no need to send again.
        ##Getting Dbhelper for performing queries.
        if dbHelper.isVideoEncoded(input_content_id):
            return responseHandler.buildResponse(404, json.dumps({'message': 'Already Encoding Request Sent or in progress'}))
        else:
            videoMetadata=dbHelper.readVideoData('videoId', input_content_id, os.environ["DYNAMO_TABLE_NAME"])
            videoPath=videoMetadata["filePath"]
            packagingId=str(uuid.uuid1())
            #Media Package Write 
            dbHelper.writeMediaPackagingData(input_content_id, packagingId, "ENCODE_STARTED")
            #Creating a SQS Object which needs to pushed to amazon SQS. Later to be read by encoder instance
            sqsEventObject = {
                'videoPath': videoPath,
                'key': key,
                'kid': kid,
                'packagingId': packagingId,
                'videoId' : input_content_id
            }
            sqs_manager= SqsManager()
            sqs_manager.send_sqs_message(sqsEventObject)
    except Exception as e:
        return responseHandler.buildResponse(500, json.dumps({'error':str(e)}))

    return responseHandler.buildResponse(200, json.dumps({
        'packaged_content_id' : packagingId
    }))

def getParamsValue(keyName, event):
    return event["body"][keyName]
