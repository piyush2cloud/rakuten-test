import json
import boto3
import requests
import os
import base64
import sys
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
import responseBuilder
import videoHelper
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
        videoHelper.updateMediaPackagingData(packagingId, videoStatus, dashUrl, keyVal, kidVal)
    except Exception as e:
        return responseBuilder.buildResponse(500, json.dumps({'error':str(e)}))
    return responseBuilder.buildResponse(200, json.dumps({"message":"success"}))