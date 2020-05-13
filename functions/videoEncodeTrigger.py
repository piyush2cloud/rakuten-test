from database import dbHelper
from response import responseBuilder
import json
import boto3
import os
import base64
import sys
import time
import uuid

def handler(event, context):
    try:
        event["body"]=json.loads(event["body"])
        packagingId=event["body"]["packagingId"]
        videoStatus=event["body"]["videoStatus"]
        dashUrl=event["body"]["dashUrl"]
        keyVal=event["body"]["key"]
        kidVal=event["body"]["kid"]
        dbHelper.updateMediaPackagingData(packagingId, videoStatus, dashUrl, keyVal, kidVal)
    except Exception as e:
        return responseBuilder.buildResponse(500, json.dumps({'error':str(e)}))
    return responseBuilder.buildResponse(200, json.dumps({"message":"success"}))