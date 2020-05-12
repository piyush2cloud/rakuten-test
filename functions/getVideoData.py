import json
import boto3
import requests
import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
import sys

def handler(event, context):
    try:
        #getting packageId and returning video information from it:
        packageId=getParamsValue("packageId", event)
        videoMetadata=videoHelper.readVideoData('packageId', packageId, os.environ["DYNAMO_TABLE_ENCODER_NAME"])
    except Exception as e:
        return responseBuilder.buildResponse(500, json.dumps(e))
    return responseBuilder.buildResponse(200, json.dumps(videoMetadata))

def getParamsValue(keyName, event):
    print(type(event))
    print(type(event["pathParameters"]))
    event=json.loads(event)
    return event["pathParameters"][keyName]
