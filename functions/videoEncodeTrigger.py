from database.dbHelper import DynamoManager
from response.responseBuilder import ResponseManager
import json
import boto3
import os
import base64
import sys
import time
import uuid

def handler(event, context):
    #response handler for returning responses
    responseHandler = ResponseManager()
    #Dynamo Db helper functions
    dbHelper=DynamoManager()
    try:
        event["body"]=json.loads(event["body"])
        packagingId=event["body"]["packagingId"]
        videoStatus=event["body"]["videoStatus"]
        dashUrl=event["body"]["dashUrl"]
        keyVal=event["body"]["key"]
        kidVal=event["body"]["kid"]
        dbHelper.updateMediaPackagingData(packagingId, videoStatus, dashUrl, keyVal, kidVal)
    except Exception as e:
        return responseHandler.buildResponse(500, json.dumps({'error':str(e)}))
    return responseHandler.buildResponse(200, json.dumps({"message":"success"}))